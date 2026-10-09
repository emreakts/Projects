import pytest

from eticaret_bot.branches import global_ds, yurtici
from eticaret_bot.calc import tl_profit
from eticaret_bot.core import roadmap, scoring
from eticaret_bot.formatting import fmt_tl, fmt_usd, parse_number


def _answers(criteria, score_fn):
    return {c.key: score_fn(c) for c in criteria}


def test_perfect_product_scores_100():
    crit = global_ds.CRITERIA
    r = scoring.evaluate(crit, _answers(crit, lambda c: max(s for _, s in c.options)))
    assert r.score == 100
    assert r.verdict.startswith("✅")
    assert not r.red_flags


@pytest.mark.parametrize("key", ["markup", "yasal"])
def test_hard_flag_blocks_even_with_high_score(key):
    crit = global_ds.CRITERIA
    answers = _answers(crit, lambda c: max(s for _, s in c.options))
    answers[key] = 1
    r = scoring.evaluate(crit, answers)
    assert r.score >= 70
    assert r.verdict.startswith("❌")
    assert r.red_flags


def test_middle_product_is_test_verdict():
    crit = yurtici.CRITERIA
    r = scoring.evaluate(crit, _answers(crit, lambda c: 3))
    assert r.score == 50
    assert r.verdict.startswith("⚠️")


def test_missing_criteria_raises():
    with pytest.raises(ValueError):
        scoring.evaluate(global_ds.CRITERIA, {"wow": 5})


def test_tl_profit_calculation():
    inp = tl_profit.ProfitInput(
        sale_price=600, unit_cost=240, commission_pct=20, shipping=60, ad_cost=0, vat_pct=20
    )
    r = tl_profit.calculate(inp)
    # ciro 500, ürün 200, komisyon 100, kargo 50 -> kâr 150
    assert r.net_revenue == pytest.approx(500)
    assert r.net_profit == pytest.approx(150)
    assert r.margin_pct == pytest.approx(30)
    assert r.roi_pct == pytest.approx(75)
    assert r.breakeven_roas == pytest.approx(4)
    # KDV: (600 - 240 - 120 - 60) * 20/120 = 30
    assert r.vat_payable == pytest.approx(30)


def test_tl_suggest_price_hits_target_margin():
    inp = tl_profit.ProfitInput(
        sale_price=1, unit_cost=240, commission_pct=20, shipping=60, ad_cost=30,
        packaging=6, return_rate_pct=5,
    )
    price = tl_profit.suggest_price(inp, 25)
    r = tl_profit.calculate(tl_profit.ProfitInput(**{**inp.__dict__, "sale_price": price}))
    assert r.margin_pct == pytest.approx(25)


def test_tl_suggest_price_impossible():
    inp = tl_profit.ProfitInput(sale_price=100, unit_cost=50, commission_pct=80, shipping=0, ad_cost=0)
    assert tl_profit.suggest_price(inp, 25) is None


@pytest.mark.parametrize(
    "text,expected",
    [("1.250,50", 1250.5), ("249,90", 249.9), ("1.250", 1250), ("12.5", 12.5), ("%18", 18), ("89 TL", 89)],
)
def test_parse_number(text, expected):
    assert parse_number(text) == pytest.approx(expected)


@pytest.mark.parametrize("text", ["abc", "-5", ""])
def test_parse_number_invalid(text):
    with pytest.raises(ValueError):
        parse_number(text)


def test_formatters():
    assert fmt_tl(1250.5) == "1.250,50 TL"
    assert fmt_usd(1250.5) == "$1.250,50"
    assert fmt_usd(-3) == "-$3,00"


def test_next_task_order():
    stages = global_ds.STAGES
    ids = roadmap.task_ids(stages)
    assert roadmap.next_task(stages, set())[1].id == ids[0]
    assert roadmap.next_task(stages, {ids[0]})[1].id == ids[1]
    assert roadmap.next_task(stages, set(ids)) is None
