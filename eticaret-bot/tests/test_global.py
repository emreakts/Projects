import pytest

from eticaret_bot.calc import ad_test, global_profit


def test_global_profit():
    inp = global_profit.GlobalInput(
        sale_price=40, product_cost=8, shipping=5, duty_pct=50, payment_fee_pct=5, refund_rate_pct=5, other=1, cpa=10
    )
    r = global_profit.calculate(inp)
    # landed = 8 + 5 + 4 = 17; ücret 2, iade 2, diğer 1 -> reklamsız 18, net 8
    assert r.landed_cost == pytest.approx(17)
    assert r.profit_before_ads == pytest.approx(18)
    assert r.net_profit == pytest.approx(8)
    assert r.margin_pct == pytest.approx(20)
    assert r.breakeven_roas == pytest.approx(40 / 18)


def test_global_suggest_price_hits_margin():
    inp = global_profit.GlobalInput(sale_price=1, product_cost=8, shipping=5, duty_pct=30, cpa=12)
    price = global_profit.suggest_price(inp, 20)
    r = global_profit.calculate(global_profit.GlobalInput(**{**inp.__dict__, "sale_price": price}))
    assert r.margin_pct == pytest.approx(20)


def test_global_unprofitable():
    r = global_profit.calculate(global_profit.GlobalInput(sale_price=10, product_cost=9, shipping=5))
    assert r.breakeven_roas is None
    assert global_profit.suggest_price(global_profit.GlobalInput(10, 1, 1, refund_rate_pct=60), 50) is None


def _ad(**kw):
    base = dict(spend=10, impressions=2000, clicks=40, add_to_carts=2, purchases=0, breakeven_cpa=20)
    return ad_test.evaluate(ad_test.AdInput(**{**base, **kw}))


def test_ad_early_no_sales_continue():
    assert _ad().decision.startswith("⏳")


def test_ad_low_ctr_change_creative():
    r = _ad(clicks=5)
    assert r.decision.startswith("🔁")
    assert any("Tıklama oranı" in d for d in r.diagnoses)


def test_ad_kill_after_spending_without_sales():
    assert _ad(spend=45).decision.startswith("❌")
    assert _ad(spend=30, add_to_carts=0).decision.startswith("❌")
    assert _ad(spend=30, add_to_carts=3).decision.startswith("⏳")


def test_ad_scale_and_profitable():
    assert _ad(spend=60, purchases=5).decision.startswith("🚀")  # CPA 12
    assert _ad(spend=36, purchases=2).decision.startswith("✅")  # CPA 18
    assert _ad(spend=48, purchases=2).decision.startswith("⚠️ Sınırda")  # CPA 24
    assert _ad(spend=70, purchases=2).decision.startswith("❌")  # CPA 35, 3.5x harcama
    assert _ad(spend=50, purchases=1).decision.startswith("⚠️ Zararda")  # CPA 50, 2.5x harcama


def test_ad_funnel_diagnoses():
    r = _ad(clicks=100, add_to_carts=1)
    assert any("sepete eklemiyorlar" in d for d in r.diagnoses)
    r = _ad(add_to_carts=10, purchases=1, spend=15)
    assert any("Sepete ekleyip" in d for d in r.diagnoses)


def test_ad_requires_breakeven():
    with pytest.raises(ValueError):
        _ad(breakeven_cpa=0)
