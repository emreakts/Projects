"""Global dropshipping için sipariş başı kâr hesabı (USD).

Varsayımlar:
- Gümrük vergisi ürün maliyeti üzerinden yüzde olarak hesaplanır (DDP fiyata dahilse 0 girilir).
- İadelerde ürün geri alınmaz, para iade edilir; dropshipping'de yaygın uygulama budur.
  Bu yüzden iade oranı kadar ciro kaybedilir, maliyetler yine de oluşur.
- Gelir/kurumlar vergisi ve ABD satış vergisi dahil değildir.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GlobalInput:
    sale_price: float  # müşterinin ödediği fiyat (kargo dahil)
    product_cost: float  # tedarikçi ürün fiyatı
    shipping: float  # tedarikçinin kargo ücreti
    duty_pct: float = 0.0  # ürün maliyeti üzerinden gümrük %
    payment_fee_pct: float = 3.5  # ödeme sağlayıcı komisyonu %
    refund_rate_pct: float = 5.0  # iade/chargeback oranı %
    other: float = 0.0  # uygulama, abonelik vb. sabit giderlerin sipariş başı payı
    cpa: float = 0.0  # satış başı reklam maliyeti


@dataclass(frozen=True)
class GlobalResult:
    landed_cost: float  # ürün + kargo + gümrük
    profit_before_ads: float  # = başa baş CPA
    net_profit: float
    margin_pct: float
    markup: float  # satış fiyatı / landed cost
    breakeven_roas: float | None


def calculate(inp: GlobalInput) -> GlobalResult:
    landed = inp.product_cost + inp.shipping + inp.product_cost * inp.duty_pct / 100
    fees = inp.sale_price * inp.payment_fee_pct / 100
    refunds = inp.sale_price * inp.refund_rate_pct / 100
    before_ads = inp.sale_price - landed - fees - refunds - inp.other
    profit = before_ads - inp.cpa
    return GlobalResult(
        landed_cost=landed,
        profit_before_ads=before_ads,
        net_profit=profit,
        margin_pct=profit / inp.sale_price * 100 if inp.sale_price else 0.0,
        markup=inp.sale_price / landed if landed else 0.0,
        breakeven_roas=inp.sale_price / before_ads if before_ads > 0 else None,
    )


def suggest_price(inp: GlobalInput, target_margin_pct: float) -> float | None:
    """Girilen CPA ile hedef net marjı sağlayan satış fiyatı. Ulaşılamıyorsa None."""
    variable = (inp.payment_fee_pct + inp.refund_rate_pct + target_margin_pct) / 100
    if variable >= 1:
        return None
    landed = inp.product_cost + inp.shipping + inp.product_cost * inp.duty_pct / 100
    return (landed + inp.other + inp.cpa) / (1 - variable)
