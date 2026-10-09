"""🅰️ Yurt içi XML dropshipping: Türk tedarikçi (XML bayilik) → Trendyol / Hepsiburada."""

from __future__ import annotations

from ..calc import tl_profit
from ..core.branch import Branch, Field, FormTool
from ..core.scoring import Criterion
from ..formatting import fmt_num, fmt_pct, fmt_tl
from .yurtici_roadmap import BRANCH_ID, STAGES


SUMMARY = (
    "🅰️ <b>Yurt İçi Dropshipping</b>: Türk tedarikçinin XML ürün listesini entegrasyon yazılımıyla "
    "Trendyol mağazana bağlarsın; sipariş gelince ürünü tedarikçi gönderir."
)

CRITERIA = (
    Criterion(
        key="marj",
        question="💰 Tahmini net kâr marjın ne kadar? (tüm masraflar düşüldükten sonra)",
        options=(("%15 altı", 1), ("%15-25", 2), ("%25-35", 3), ("%35-50", 4), ("%50 üstü", 5)),
        weight=3,
        tip="Marj düşük: daha ucuz tedarikçi ara, set/paket satış yap ya da fiyatı yükselt. "
        "Kâr hesaplayıcıyla gerçek marjını kontrol et.",
        hard_flag=True,
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
        hard_flag=True,
    ),
)


# ---------- 💰 Kâr hesabı (TL) ----------

PROFIT_FIELDS = (
    Field("sale_price", "🏷 Satış fiyatı (KDV dahil, TL)?", kind="positive"),
    Field("unit_cost", "📦 Tedarikçi alış fiyatı (KDV dahil, TL)?"),
    Field("commission_pct", "🏪 Pazaryeri komisyonu (%)? Kendi siten ise ödeme komisyonunu yaz (ör. 3).", kind="pct"),
    Field("shipping", "🚚 Sipariş başı kargo ücreti (KDV dahil, TL)?"),
    Field("ad_cost", "📣 Satış başı reklam harcaması (TL)? Bilmiyorsan 0 yaz.", default=0.0),
    Field("packaging", "🎁 Paketleme maliyeti (TL)? Yoksa 0 yaz.", default=0.0),
    Field("return_rate_pct", "↩️ Tahmini iade oranı (%)? Bilmiyorsan 5 yaz.", default=5.0, kind="pct"),
    Field("vat_pct", "🧾 KDV oranı (%)? Çoğu ürün için 20.", default=20.0, kind="pct"),
)


def profit_report(values: dict[str, float]) -> str:
    inp = tl_profit.ProfitInput(**values)
    r = tl_profit.calculate(inp)
    status = "✅ Kârlı" if r.net_profit > 0 else "❌ Zarar ediyorsun"
    lines = [
        "💰 <b>Birim Kâr Analizi</b>\n",
        f"Satış fiyatı: {fmt_tl(inp.sale_price)}",
        f"KDV hariç ciro: {fmt_tl(r.net_revenue)}",
        f"Toplam maliyet (KDV hariç): {fmt_tl(r.total_cost)}",
        f"Ödenecek tahmini KDV: {fmt_tl(r.vat_payable)}",
        "",
        f"<b>Net kâr: {fmt_tl(r.net_profit)}</b> ({status})",
        f"Net marj: {fmt_pct(r.margin_pct)}",
        f"Ürün maliyetine göre getiri (ROI): {fmt_pct(r.roi_pct)}",
    ]
    if r.breakeven_roas is not None:
        lines.append(
            f"Başa baş ROAS: <b>{fmt_num(r.breakeven_roas)}</b>"
            "\n<i>(Reklama harcadığın her 1 TL bundan az ciro getiriyorsa zarar edersin)</i>"
        )
    else:
        lines.append("Başa baş ROAS: reklamsız bile zarar var, önce maliyet/fiyatı düzelt.")

    lines.append("\n🎯 <b>Hedef marja göre önerilen satış fiyatı</b>")
    for target in (15, 25, 35):
        price = tl_profit.suggest_price(inp, target)
        lines.append(f"• %{target} marj: " + (fmt_tl(price) if price else "komisyon çok yüksek, ulaşılamaz"))

    if r.margin_pct < 15:
        lines.append("\n⚠️ Marj %15'in altında. İade, kampanya ve beklenmedik masraflar kârını silebilir.")
    lines.append("\n<i>Not: Gelir/kurumlar vergisi dahil değildir. Basitleştirilmiş hesaptır.</i>")
    return "\n".join(lines)


BRANCH = Branch(
    id=BRANCH_ID,
    title="🅰️ Yurt İçi Dropshipping",
    summary=SUMMARY,
    ready=True,
    stages=STAGES,
    criteria=CRITERIA,
    tools=(FormTool("kar", "💰 Kâr Hesabı", "💰 Kâr Hesabı (TL)", PROFIT_FIELDS, profit_report),),
)
