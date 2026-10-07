"""Ürün seçimi puanlama modülü.

Kullanıcı her kriter için bir seçenek seçer, her seçeneğin 1-5 arası puanı vardır.
Kriterlerin ağırlıklarına göre 0-100 arası toplam skor ve karar üretilir.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Criterion:
    key: str
    question: str
    options: tuple[tuple[str, int], ...]  # (etiket, puan 1-5)
    weight: int
    tip: str  # puan düşükse verilecek tavsiye


CRITERIA: tuple[Criterion, ...] = (
    Criterion(
        key="marj",
        question="💰 Tahmini net kâr marjın ne kadar? (tüm masraflar düşüldükten sonra)",
        options=(("%15 altı", 1), ("%15-25", 2), ("%25-35", 3), ("%35-50", 4), ("%50 üstü", 5)),
        weight=3,
        tip="Marj düşük: daha ucuz tedarikçi ara, set/paket satış yap ya da fiyatı yükselt. "
        "Kâr hesaplayıcıyla gerçek marjını kontrol et.",
    ),
    Criterion(
        key="talep",
        question="📈 Talep durumu nasıl? (Google Trends, pazaryeri yorum sayıları, arama hacmi)",
        options=(("Çok düşük", 1), ("Düşük", 2), ("Orta", 3), ("Yüksek", 4), ("Çok yüksek", 5)),
        weight=3,
        tip="Talep zayıf: pazaryerlerinde en çok satanlara ve yorum sayılarına bak, "
        "talebi kanıtlanmış bir alt kategoriye kay.",
    ),
    Criterion(
        key="rekabet",
        question="⚔️ Rekabet ne durumda? (aynı ürünü satan satıcı sayısı, büyük markalar)",
        options=(("Çok yoğun", 1), ("Yoğun", 2), ("Orta", 3), ("Az", 4), ("Çok az", 5)),
        weight=2,
        tip="Rekabet yoğun: ürünü farklılaştır (paket, renk, aksesuar, marka/ambalaj) "
        "ya da daha dar bir niş hedefle.",
    ),
    Criterion(
        key="trend",
        question="📊 Trend yönü nasıl?",
        options=(("Düşüşte", 1), ("Durgun", 3), ("Yükselişte", 5)),
        weight=2,
        tip="Trend düşüşte: büyük stok yapma, küçük partilerle test et.",
    ),
    Criterion(
        key="sezon",
        question="🗓 Sezonluk bir ürün mü?",
        options=(("Sadece belirli aylarda", 2), ("Kısmen sezonluk", 3), ("Yıl boyu satılır", 5)),
        weight=1,
        tip="Sezonluk ürün: sezon bitmeden stok eritme planı yap, yanına yıl boyu satan bir ürün ekle.",
    ),
    Criterion(
        key="kargo",
        question="📦 Boyut / ağırlık / kırılganlık?",
        options=(("Büyük, ağır veya kırılgan", 1), ("Orta", 3), ("Küçük, hafif, sağlam", 5)),
        weight=2,
        tip="Kargo zor: desi maliyetini hesaba kat, sağlam paketleme ve kırılma iadesi payı ekle.",
    ),
    Criterion(
        key="iade",
        question="↩️ İade riski? (beden uyumsuzluğu, arıza, beklentiyi karşılamama)",
        options=(("Yüksek", 1), ("Orta", 3), ("Düşük", 5)),
        weight=2,
        tip="İade riski yüksek: detaylı beden tablosu/ölçü, gerçek fotoğraf ve video kullan; "
        "fiyata iade payı ekle.",
    ),
    Criterion(
        key="fiyat",
        question="🏷 Satış fiyatı aralığı?",
        options=(("150 TL altı", 2), ("150-500 TL", 4), ("500-2.000 TL", 5), ("2.000 TL üstü", 3)),
        weight=1,
        tip="Fiyat aralığı ideal değil: çok ucuz üründe kargo kârı yer, çok pahalıda "
        "dönüşüm yavaşlar. Paketleyerek ya da bölerek ortalama sepeti ayarla.",
    ),
    Criterion(
        key="tedarik",
        question="🏭 Tedarik güvenilirliği?",
        options=(("Tek kaynak / belirsiz", 1), ("Orta", 3), ("Birden fazla güvenilir tedarikçi", 5)),
        weight=1,
        tip="Tedarik riskli: en az bir yedek tedarikçi bul, numune iste, teslim sürelerini yazılı al.",
    ),
    Criterion(
        key="yasal",
        question="⚖️ Yasal risk? (marka/patent, CE belgesi, gıda/kozmetik/medikal izinleri)",
        options=(("Riskli", 1), ("Emin değilim", 3), ("Sorunsuz", 5)),
        weight=2,
        tip="Yasal risk var: marka tescili (TÜRKPATENT), CE ve gerekli izinleri kontrol etmeden satışa başlama.",
    ),
)

# Bu kriterlerde en düşük puan, toplam skor ne olursa olsun "girme" kararı verdirir.
HARD_RED_FLAGS = ("marj", "yasal")


@dataclass
class ScoreResult:
    score: int  # 0-100
    verdict: str
    red_flags: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)  # düşük puanlı kriterler için tavsiyeler


def get_criterion(key: str) -> Criterion:
    for c in CRITERIA:
        if c.key == key:
            return c
    raise KeyError(key)


def evaluate(answers: dict[str, int]) -> ScoreResult:
    """answers: kriter anahtarı -> seçilen puan (1-5). Tüm kriterler cevaplanmış olmalı."""
    missing = [c.key for c in CRITERIA if c.key not in answers]
    if missing:
        raise ValueError(f"Eksik kriterler: {', '.join(missing)}")

    total_weight = sum(c.weight for c in CRITERIA)
    weighted = sum(c.weight * (answers[c.key] - 1) / 4 for c in CRITERIA)
    score = round(weighted / total_weight * 100)

    red_flags = [get_criterion(k).tip for k in HARD_RED_FLAGS if answers[k] == 1]
    weaknesses = [c.tip for c in CRITERIA if answers[c.key] <= 2 and c.key not in HARD_RED_FLAGS]

    if red_flags or score < 50:
        verdict = "❌ Girme. Bu ürün şu haliyle riskli."
    elif score < 70:
        verdict = "⚠️ Dikkatli test et. Küçük stok ve düşük bütçeli reklamla dene."
    else:
        verdict = "✅ Gir. Güçlü bir aday, test siparişiyle başla."

    return ScoreResult(score=score, verdict=verdict, red_flags=red_flags, weaknesses=weaknesses)
