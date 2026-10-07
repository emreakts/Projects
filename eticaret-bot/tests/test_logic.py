import pytest

from eticaret_bot.formatting import fmt_tl, parse_number
from eticaret_bot.modules import product_score, profit_calc, roadmap


def _answers(score_fn):
    return {c.key: score_fn(c) for c in product_score.CRITERIA}


def test_perfect_product_scores_100():
    r = product_score.evaluate(_answers(lambda c: max(s for _, s in c.options)))
    assert r.score == 100
    assert r.verdict.startswith("✅")
    assert not r.red_flags


def test_low_margin_is_hard_red_flag_even_with_high_score():
    answers = _answers(lambda c: 5)
    answers["marj"] = 1
    r = product_score.evaluate(answers)
    assert r.score >= 70
    assert r.verdict.startswith("❌")
    assert r.red_flags


def test_middle_product_is_test_verdict():
    r = product_score.evaluate(_answers(lambda c: 3))
    assert r.score == 50
    assert r.verdict.startswith("⚠️")


def test_missing_criteria_raises():
    with pytest.raises(ValueError):
        product_score.evaluate({"marj": 5})


def test_option_scores_in_range():
    for c in product_score.CRITERIA:
        assert all(1 <= s <= 5 for _, s in c.options)


def test_profit_calculation():
    inp = profit_calc.ProfitInput(
        sale_price=600, unit_cost=240, commission_pct=20, shipping=60, ad_cost=0, vat_pct=20
    )
    r = profit_calc.calculate(inp)
    # ciro 500, ürün 200, komisyon 100, kargo 50 -> kâr 150
    assert r.net_revenue == pytest.approx(500)
    assert r.net_profit == pytest.approx(150)
    assert r.margin_pct == pytest.approx(30)
    assert r.roi_pct == pytest.approx(75)
    assert r.breakeven_roas == pytest.approx(4)
    # KDV: (600 - 240 - 120 - 60) * 20/120 = 30
    assert r.vat_payable == pytest.approx(30)


def test_suggest_price_hits_target_margin():
    inp = profit_calc.ProfitInput(
        sale_price=1, unit_cost=240, commission_pct=20, shipping=60, ad_cost=30,
        packaging=6, return_rate_pct=5,
    )
    price = profit_calc.suggest_price(inp, 25)
    r = profit_calc.calculate(profit_calc.ProfitInput(**{**inp.__dict__, "sale_price": price}))
    assert r.margin_pct == pytest.approx(25)


def test_suggest_price_impossible():
    inp = profit_calc.ProfitInput(sale_price=100, unit_cost=50, commission_pct=80, shipping=0, ad_cost=0)
    assert profit_calc.suggest_price(inp, 25) is None


def test_unprofitable_has_no_breakeven_roas():
    inp = profit_calc.ProfitInput(sale_price=100, unit_cost=120, commission_pct=10, shipping=20, ad_cost=0)
    assert profit_calc.calculate(inp).breakeven_roas is None


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


def test_fmt_tl():
    assert fmt_tl(1250.5) == "1.250,50 TL"


def test_roadmap_ids_unique_and_next_task():
    assert len(set(roadmap.ALL_TASK_IDS)) == len(roadmap.ALL_TASK_IDS)
    stage, task = roadmap.next_task(set())
    assert task.id == roadmap.ALL_TASK_IDS[0]
    stage, task = roadmap.next_task({roadmap.ALL_TASK_IDS[0]})
    assert task.id == roadmap.ALL_TASK_IDS[1]
    assert roadmap.next_task(set(roadmap.ALL_TASK_IDS)) is None


def test_callback_data_within_telegram_limit():
    # Telegram callback_data en fazla 64 bayt
    for tid in roadmap.ALL_TASK_IDS:
        assert len(f"done:{tid}".encode()) <= 64
