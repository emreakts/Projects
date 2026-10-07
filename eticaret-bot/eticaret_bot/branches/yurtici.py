"""🅰️ Yurt içi dropshipping (XML bayilik): Türk tedarikçiler + pazaryerleri / kendi site.

Şimdilik genel e-ticaret yol haritası, ürün analizi ve TL kâr hesabıyla çalışır.
XML dropshipping'e özel içerik bu dalın kendi çalışma turunda eklenecek.
"""

from ..calc import tl_profit
from ..core.branch import Branch, Field, FormTool
from ..core.roadmap import make_stage
from ..core.scoring import Criterion
from ..formatting import fmt_num, fmt_pct, fmt_tl

BRANCH_ID = "a"

SUMMARY = (
    "🅰️ <b>Yurt İçi Dropshipping (XML Bayilik)</b>\n\n"
    "Türk tedarikçiler ürün, fiyat ve stok bilgisini XML ile paylaşır; sen bunları kendi sitene "
    "veya Trendyol / Hepsiburada / N11'e çekip kâr ekleyerek satarsın. Sipariş gelince tedarikçi "
    "ürünü müşteriye gönderir.\n\n"
    "⚠️ Pazaryerleri 2-3 iş gününde kargo bekler, bu yüzden yurt içi tedarikçi şart. "
    "Tükenen ürün yüzünden iptal mağaza puanını düşürür.\n\n"
    "🚧 <i>Bu dal ön sürümde: araçlar genel e-ticaret içeriğiyle çalışıyor, XML dropshipping'e "
    "özel içerik sıradaki çalışma turunda gelecek.</i>"
)

STAGES = (
    make_stage(
        BRANCH_ID,
        "model",
        "1️⃣ İş Modeli ve Hedef",
        "Önce neyi, kime, hangi kanaldan satacağını netleştir. Yeni başlıyorsan pazaryeri ile "
        "başlamak (hazır trafik) en düşük riskli yoldur; kendi sitesi marka ve marj için sonradan eklenir.",
        [
            "Aylık bütçeni ve ayırabileceğin zamanı belirle",
            "Satış modelini seç: stoklu / dropshipping / kendi üretim / private label",
            "Kanalı seç: pazaryeri (Trendyol, Hepsiburada, Amazon TR, N11) ve/veya kendi site",
            "İlk 3 ay için gerçekçi ciro ve kâr hedefi yaz",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "urun",
        "2️⃣ Ürün Seçimi",
        "Talebi kanıtlanmış, marjı yüksek, kargosu kolay ürün ara. Her adayı 🔍 Ürün Analizi ile puanla, "
        "💰 Kâr Hesapla ile gerçek kârını gör.",
        [
            "En az 10 ürün adayı listele (pazaryeri çok satanlar, Google Trends, TikTok/Instagram)",
            "Her adayı Ürün Analizi ile puanla",
            "En iyi 3 aday için kâr hesabı yap",
            "Rakiplerin yorumlarındaki şikayetleri not al (farklılaşma fırsatı)",
            "1 ana ürün / ürün grubu seç",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "tedarik",
        "3️⃣ Tedarikçi",
        "Yerli toptancılar hızlı teslim ve kolay iade sağlar; Alibaba/1688 daha ucuzdur ama gümrük, "
        "süre ve kalite riski taşır. Numune görmeden toplu sipariş verme.",
        [
            "En az 3 tedarikçi bul ve fiyat teklifi al",
            "Numune sipariş et, kaliteyi ve paketlemeyi kontrol et",
            "Minimum sipariş adedi, teslim süresi ve ödeme şartlarını yazılı al",
            "Yedek tedarikçi belirle",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "yasal",
        "4️⃣ Yasal Süreç (Türkiye)",
        "Düzenli satış için vergi mükellefiyeti gerekir. Başlangıçta şahıs şirketi genelde yeterlidir; "
        "ciro büyüyünce limited şirkete geçiş değerlendirilir. Detaylar için bir mali müşavirle çalış.",
        [
            "Mali müşavir ile görüş, şahıs mı limited mi karar ver",
            "Vergi levhası al (şirket kuruluşu)",
            "e-Fatura / e-Arşiv faturaya geç (GİB portal veya entegratör)",
            "KVKK aydınlatma metni, gizlilik politikası hazırla",
            "Mesafeli satış sözleşmesi, ön bilgilendirme formu, iade/iptal politikası hazırla",
            "Ürün belgelerini kontrol et (CE, marka tescili, gerekli izinler)",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "magaza",
        "5️⃣ Mağaza Kurulumu",
        "Pazaryerinde satıcı paneli açmak en hızlı başlangıçtır. Kendi site için İkas, Ticimax, "
        "Shopify veya WooCommerce seçenekleri var; ödeme için iyzico/PayTR, kargo için anlaşmalı firma gerekir.",
        [
            "Pazaryeri satıcı hesabı aç ve belgelerini yükle",
            "(Kendi site) Platformu seç ve alan adı al",
            "(Kendi site) Ödeme altyapısını bağla (iyzico, PayTR vb.)",
            "Kargo firmasıyla anlaş, desi fiyatlarını al",
            "Logo, mağaza adı ve temel görsel kimliği hazırla",
            "Yasal metinleri mağazaya ekle",
            "Test siparişi ver: ödeme, fatura, kargo akışını baştan sona dene",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "listeleme",
        "6️⃣ Ürün Listeleme",
        "Başlık arama yapılan kelimelerle başlamalı; görseller satışın yarısıdır. Açıklamada fayda, "
        "ölçü, malzeme ve kullanım bilgisini net ver.",
        [
            "Anahtar kelime araştırması yap (pazaryeri arama önerileri)",
            "SEO uyumlu başlık yaz: Marka + Ürün + Ana özellik + Varyant",
            "En az 5 kaliteli görsel (beyaz fon, kullanım, detay, ölçü)",
            "Fayda odaklı açıklama ve özellik listesi yaz",
            "Varyantları (renk/beden) ve stokları doğru gir",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "pazarlama",
        "7️⃣ Pazarlama",
        "Küçük bütçeyle test et, kazanan reklamı büyüt. Başa baş ROAS değerini Kâr Hesapla ile öğren; "
        "altında kalan reklamlar zarar ettirir.",
        [
            "Başa baş ROAS değerini hesapla",
            "Pazaryeri içi reklamla (sponsorlu ürün) başla",
            "Instagram / TikTok hesabı aç, haftalık içerik takvimi hazırla",
            "Meta veya Google reklamlarında düşük bütçeli test kampanyası aç",
            "İlk müşterilerden yorum iste",
            "Mikro influencer işbirliği dene",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "operasyon",
        "8️⃣ Operasyon",
        "Hızlı kargo ve hızlı cevap, pazaryeri puanını ve satışları doğrudan etkiler.",
        [
            "Siparişleri aynı gün / 24 saat içinde kargoya ver",
            "Stok takip yöntemi kur (tablo veya entegrasyon)",
            "Müşteri sorularına hazır cevap şablonları oluştur",
            "İade sürecini ve iade ürün kontrolünü tanımla",
            "Haftalık stok sayımı ve yeniden sipariş noktası belirle",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "buyume",
        "9️⃣ Analiz ve Büyüme",
        "Ölçmediğini büyütemezsin. Kârlı ürün ve kanalı bul, oraya yüklen.",
        [
            "Haftalık KPI takibi: ciro, net kâr, ROAS, dönüşüm oranı, sepet ortalaması",
            "Ürün bazında kârlılığı çıkar, zarar edenleri ele",
            "Kazanan ürünün varyant / tamamlayıcı ürünlerini ekle",
            "Yeni bir kanal aç (ikinci pazaryeri veya kendi site)",
            "E-posta / WhatsApp ile tekrar satın alma kampanyası kur",
        ],
    ),
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
