"""Reklam testi değerlendirmesi: metriklerden kapat / devam / ölçekle kararı.

Eşikler dropshipping topluluğunda yaygın kullanılan pratik kurallardır, kesin değildir.
Karar, harcamanın başa baş CPA'ya (sipariş başı reklamsız kâr) oranına göre verilir.
"""

from __future__ import annotations

from dataclasses import dataclass, field

LOW_CTR_PCT = 1.0  # link tıklama oranı bunun altındaysa kreatif zayıf
LOW_ATC_RATE_PCT = 5.0  # tıklayanların sepete ekleme oranı
LOW_CHECKOUT_RATE_PCT = 20.0  # sepete ekleyenlerin satın alma oranı
HIGH_CPM = 40.0  # $
MIN_IMPRESSIONS = 1000  # bundan azsa oranlar anlamlı değil


@dataclass(frozen=True)
class AdInput:
    spend: float
    impressions: float
    clicks: float  # link tıklaması
    add_to_carts: float
    purchases: float
    breakeven_cpa: float


@dataclass
class AdResult:
    decision: str
    reason: str
    ctr_pct: float | None
    cpc: float | None
    cpm: float | None
    cpa: float | None
    diagnoses: list[str] = field(default_factory=list)


def _ratio(a: float, b: float) -> float | None:
    return a / b if b else None


def evaluate(inp: AdInput) -> AdResult:
    if inp.breakeven_cpa <= 0:
        raise ValueError("Başa baş CPA sıfırdan büyük olmalı")

    ctr = _ratio(inp.clicks, inp.impressions)
    ctr_pct = ctr * 100 if ctr is not None else None
    cpm = inp.spend / inp.impressions * 1000 if inp.impressions else None
    cpa = _ratio(inp.spend, inp.purchases)
    spend_ratio = inp.spend / inp.breakeven_cpa  # harcama kaç "başa baş CPA" ediyor

    low_ctr = inp.impressions >= MIN_IMPRESSIONS and ctr_pct is not None and ctr_pct < LOW_CTR_PCT
    diagnoses = []
    if inp.impressions >= MIN_IMPRESSIONS:
        if low_ctr:
            diagnoses.append("Tıklama oranı düşük: ilk 3 saniyedeki hook ve kreatif zayıf, yeni video dene.")
        if cpm is not None and cpm > HIGH_CPM:
            diagnoses.append("CPM yüksek: kitle çok dar veya kreatif kalitesi düşük, geniş hedeflemeyi dene.")
    if inp.clicks >= 30 and inp.add_to_carts / inp.clicks * 100 < LOW_ATC_RATE_PCT:
        diagnoses.append("Tıklıyorlar ama sepete eklemiyorlar: ürün sayfası, fiyat veya teklif ikna etmiyor.")
    if inp.add_to_carts >= 5 and inp.purchases / inp.add_to_carts * 100 < LOW_CHECKOUT_RATE_PCT:
        diagnoses.append(
            "Sepete ekleyip almıyorlar: ödeme adımı, kargo ücreti/süresi veya güven sorunu var."
        )

    if inp.purchases == 0:
        if spend_ratio < 1:
            if low_ctr:
                decision, reason = "🔁 Kreatifi değiştir", "Satış yok ve tıklama oranı çok düşük."
            else:
                decision, reason = "⏳ Devam et", "Henüz başa baş CPA kadar harcanmadı, veri yetersiz."
        elif spend_ratio < 2 and inp.add_to_carts > 0:
            decision, reason = "⏳ Son şans", "Sepete ekleme var ama satış yok. 2x başa baş CPA'ya kadar izle."
        else:
            decision, reason = "❌ Kapat", "Başa baş CPA'nın katları harcandı ve satış yok."
    else:
        assert cpa is not None
        if cpa <= inp.breakeven_cpa * 0.7 and inp.purchases >= 3:
            decision, reason = "🚀 Ölçekle", "CPA başa başın belirgin altında. Bütçeyi 2-3 günde bir %20-30 artır."
        elif cpa <= inp.breakeven_cpa:
            decision, reason = "✅ Kârlı, devam", "CPA başa başın altında. Yeni kreatiflerle güçlendir."
        elif cpa <= inp.breakeven_cpa * 1.3:
            decision, reason = "⚠️ Sınırda", "CPA başa başın biraz üstünde. Kreatif, teklif veya fiyatı optimize et."
        elif spend_ratio >= 3:
            decision, reason = "❌ Kapat", "CPA başa başın çok üstünde ve yeterli veri var."
        else:
            decision, reason = "⚠️ Zararda", "CPA yüksek. Optimize et, düzelmezse kapat."

    return AdResult(
        decision=decision,
        reason=reason,
        ctr_pct=ctr_pct,
        cpc=_ratio(inp.spend, inp.clicks),
        cpm=cpm,
        cpa=cpa,
        diagnoses=diagnoses,
    )
