"""Birim başına kâr / fiyatlama hesaplayıcı.

Varsayımlar (basitleştirilmiş model):
- Tüm tutarlar KDV dahil girilir ve hepsi aynı KDV oranına tabidir.
- Masraflardaki KDV indirilebilir kabul edilir, yani hesaplar KDV hariç tutarlarla yapılır.
- Pazaryeri komisyonu KDV dahil satış fiyatı üzerinden kesilir.
- İade edilen ürün sağlam döner; iadenin maliyeti gidiş ve dönüş kargosudur.
- Gelir/kurumlar vergisi dahil değildir.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProfitInput:
    sale_price: float  # satış fiyatı (KDV dahil)
    unit_cost: float  # ürün alış maliyeti (KDV dahil)
    commission_pct: float  # pazaryeri komisyonu %
    shipping: float  # sipariş başı kargo (KDV dahil)
    ad_cost: float  # satış başı reklam harcaması (KDV dahil)
    packaging: float = 0.0  # paketleme (KDV dahil)
    return_rate_pct: float = 0.0  # iade oranı %
    vat_pct: float = 20.0  # KDV oranı %


@dataclass(frozen=True)
class ProfitResult:
    net_revenue: float  # KDV hariç ciro
    total_cost: float  # KDV hariç toplam maliyet
    net_profit: float
    margin_pct: float  # net kâr / KDV hariç ciro
    roi_pct: float  # net kâr / ürün maliyeti
    breakeven_roas: float | None  # reklamsız kâr <= 0 ise None
    vat_payable: float  # satış başı ödenecek tahmini KDV


def _net(amount: float, vat_pct: float) -> float:
    return amount / (1 + vat_pct / 100)


def calculate(inp: ProfitInput) -> ProfitResult:
    v = inp.vat_pct
    revenue = _net(inp.sale_price, v)
    product = _net(inp.unit_cost, v)
    commission = _net(inp.sale_price * inp.commission_pct / 100, v)
    shipping = _net(inp.shipping, v)
    ads = _net(inp.ad_cost, v)
    packaging = _net(inp.packaging, v)
    returns = inp.return_rate_pct / 100 * 2 * shipping

    total_cost = product + commission + shipping + ads + packaging + returns
    profit = revenue - total_cost
    profit_before_ads = profit + ads

    gross_costs = inp.unit_cost + inp.sale_price * inp.commission_pct / 100 + inp.shipping + inp.ad_cost + inp.packaging
    vat_payable = (inp.sale_price - gross_costs) * v / (100 + v)

    return ProfitResult(
        net_revenue=revenue,
        total_cost=total_cost,
        net_profit=profit,
        margin_pct=profit / revenue * 100 if revenue else 0.0,
        roi_pct=profit / product * 100 if product else 0.0,
        breakeven_roas=inp.sale_price / profit_before_ads if profit_before_ads > 0 else None,
        vat_payable=vat_payable,
    )


def suggest_price(inp: ProfitInput, target_margin_pct: float) -> float | None:
    """Hedef net marjı sağlayan KDV dahil satış fiyatı. Komisyon + marj %100'ü aşarsa None."""
    v = inp.vat_pct
    c = inp.commission_pct / 100
    m = target_margin_pct / 100
    if 1 - c - m <= 0:
        return None
    shipping = _net(inp.shipping, v)
    fixed = (
        _net(inp.unit_cost, v)
        + shipping
        + _net(inp.ad_cost, v)
        + _net(inp.packaging, v)
        + inp.return_rate_pct / 100 * 2 * shipping
    )
    return fixed * (1 + v / 100) / (1 - c - m)
