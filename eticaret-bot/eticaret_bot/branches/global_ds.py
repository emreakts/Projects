"""🅲 Global dropshipping: Shopify + Çin / hedef ülke depolu tedarikçiler + Meta/TikTok reklamları.

Türkiye'den yönetilen, ABD / UK / AB / CA / AU müşterilerine satış yapan model.
"""

from ..calc import ad_test, global_profit
from ..core.branch import Branch, Field, FormTool
from ..core.roadmap import make_stage
from ..core.scoring import Criterion
from ..formatting import fmt_num, fmt_pct, fmt_usd

BRANCH_ID = "c"

SUMMARY = (
    "🅲 <b>Global Dropshipping</b>\n\n"
    "Shopify mağazası kurup ürünleri CJ Dropshipping, DSers (AliExpress), AutoDS, Zendrop veya "
    "Spocket gibi tedarikçilerden doğrudan müşteriye gönderirsin. Satışlar çoğunlukla Meta ve "
    "TikTok video reklamlarıyla gelir. Hedef pazar ABD, İngiltere, AB, Kanada, Avustralya.\n\n"
    "⚠️ <b>2026'da bilmen gerekenler</b>\n"
    "• Stripe ve PayPal Türkiye'de yok. Ödeme almak için genelde ABD LLC veya UK Ltd şirketi gerekir.\n"
    "• Shopify Payments, ABD'de fiziksel/operasyonel varlığı olmayan yabancıları sıkça reddediyor. "
    "Stripe ise LLC + EIN ile SSN olmadan açılabiliyor.\n"
    "• ABD'nin 800 $ gümrük muafiyeti kalktı: Çin'den gelen her paket gümrük vergisine tabi. "
    "DDP (vergiler dahil) gönderim veya ABD deposu şart.\n"
    "• AB, 1 Temmuz 2026'dan beri 150 € altı gönderilerde ürün başına 3 € gümrük alıyor.\n\n"
    "Gümrük oranları sık değişiyor, tedarikçiden her ürün için güncel DDP fiyatı iste."
)

STAGES = (
    make_stage(
        BRANCH_ID,
        "pazar",
        "1️⃣ Hedef Pazar ve Bütçe",
        "Test edilen ürünlerin çoğu tutmaz; bütçeni 3-5 ürün testine yetecek şekilde planla. "
        "ABD en büyük pazar ama gümrük maliyeti en yüksek olanlardan; UK, CA ve AU iyi alternatifler.",
        [
            "Hedef pazarı seç (ABD, UK, AB, CA, AU) ve o pazarın gümrük kuralını öğren",
            "Mağaza tipine karar ver: tek ürün, niş mağaza veya genel mağaza (öneri: niş)",
            "Test bütçesi ayır: ürün başına en az 300-500 $ reklam + 2-3 aylık sabit giderler",
            "Mali müşavirle, yurt dışı şirket kazancının Türkiye'de nasıl beyan edileceğini konuş",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "sirket",
        "2️⃣ Yurt Dışı Şirket ve Ödeme",
        "En yaygın yol: ABD LLC (Wyoming, Delaware, New Mexico) + EIN + şirket adına ABD banka hesabı "
        "+ Stripe. Shopify Payments reddedilirse üçüncü taraf ödeme sağlayıcısı kullanılır; Shopify bu "
        "durumda plana göre ek işlem ücreti keser. Şirket kurma servisleri (Stripe Atlas, doola, Firstbase vb.) "
        "süreci kolaylaştırır.",
        [
            "Şirket ülkesini seç (ABD LLC veya UK Ltd)",
            "Şirketi kur (kendin veya şirket kurma servisiyle)",
            "EIN al (SSN yoksa IRS'e SS-4 formuyla telefon/faks veya servis üzerinden)",
            "Şirket adına banka hesabı aç (Mercury, Relay, Wise Business vb.)",
            "Ödeme sağlayıcısına başvur (Shopify Payments, Stripe, PayPal Business)",
            "Kazancı Türkiye'ye aktarma ve beyan yöntemini netleştir",
            "Satış vergisi (ABD sales tax) ve AB KDV (IOSS) yükümlülüklerini kontrol et",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "urun",
        "3️⃣ Ürün Araştırması",
        "Kazanan ürün: ilk bakışta 'vay' dedirtir veya net bir sorunu çözer, mağazalarda kolay bulunmaz, "
        "maliyetinin en az 3 katına satılır, 25-70 $ aralığındadır, hafiftir ve markalı değildir. "
        "Kaynaklar: Meta Ad Library, TikTok Creative Center, CJ/AliExpress trend listeleri, ürün casusu araçları.",
        [
            "Meta Ad Library ve TikTok'ta son 30 günde artan reklamları tara",
            "20 aday ürün listesi çıkar",
            "Her adayı 🔍 Ürün Analizi ile puanla",
            "En iyi 3-5 adayın 💵 Kâr Hesabını yap (gümrük dahil)",
            "Rakip mağazaları incele: fiyat, teklif, ürün sayfası, yorumlar",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "tedarik",
        "4️⃣ Tedarikçi ve Kargo",
        "CJ Dropshipping (kendi depoları, ABD deposu, DDP gönderim), DSers (AliExpress), AutoDS, Zendrop, "
        "Spocket (ABD/AB depolu tedarikçiler). Gümrük artık her pakete uygulandığı için DDP gönderim veya "
        "hedef ülke deposu seç; yoksa müşteri kapıda vergi öder, iade ve chargeback patlar.",
        [
            "En az 2 tedarikçiden ürün + kargo fiyatı ve teslim süresi al",
            "Gönderimin DDP olduğunu ve gümrük maliyetini yazılı teyit et",
            "Test siparişi ver: kalite, paketleme, teslim süresi",
            "Pakette fiyat, fatura veya tedarikçi logosu olmamasını sağla",
            "Ürün tutarsa özel ajan veya ABD depo stoğu seçeneğini araştır",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "magaza",
        "5️⃣ Shopify Mağaza",
        "Müşteri markanı tanımıyor; güveni sayfa kazanır. Net kargo süresi, açık iade politikası, "
        "gerçek iletişim bilgisi ve güçlü ürün sayfası şart.",
        [
            "Shopify hesabı aç ve plan seç",
            "Alan adı al, profesyonel e-posta kur",
            "Hızlı bir tema kur ve marka kimliğini (logo, renk) hazırla",
            "Zorunlu sayfalar: Refund, Shipping, Privacy, Terms, Contact, About",
            "Ürün sayfası: fayda başlıkları, GIF/video, karşılaştırma, SSS, yorumlar",
            "Tedarikçi uygulamasını bağla (CJ, DSers, AutoDS) ve ürünü içe aktar",
            "Fiyat, karşılaştırma fiyatı ve paket/upsell teklifini ayarla",
            "Ödeme ve kargo ayarlarını yap, uçtan uca test siparişi ver",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "reklam",
        "6️⃣ Reklam ve Test",
        "Video reklam ana silah. Ürün başına 3-5 farklı kreatifle, günlük 20-50 $ bütçeyle test et. "
        "Karar için 📊 Reklam Testi aracını her gün kullan; başa baş CPA'nın 2-3 katı harcayıp satış "
        "alamayan reklamı kapat.",
        [
            "Meta Business, reklam hesabı, Pixel ve Conversions API kur",
            "TikTok Ads hesabı ve Pixel kur (opsiyonel)",
            "3-5 farklı video kreatif hazırla (farklı hook'lar, UGC tarzı)",
            "💵 Kâr Hesabı ile başa baş CPA ve ROAS'ı öğren",
            "Test kampanyasını aç (geniş hedefleme, satın alma optimizasyonu)",
            "Her gün 📊 Reklam Testi ile kapat / devam / ölçekle kararı ver",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "operasyon",
        "7️⃣ Sipariş ve Müşteri Hizmetleri",
        "Yüksek iade ve chargeback oranı ödeme hesabını kapattırabilir. Takip numarasını hızlı yükle, "
        "sorulara 24 saat içinde dön, sorunlu siparişi tartışmadan çöz.",
        [
            "Otomatik sipariş iletimini (auto-fulfill) aç",
            "Takip numarası senkronunu ve sipariş takip sayfasını kur",
            "Destek şablonları hazırla: kargo nerede, iade, hasarlı ürün",
            "Hasar/kayıp sürecini tedarikçiyle netleştir (fotoğrafla yeniden gönderim)",
            "Chargeback ve dispute'ları haftalık kontrol et",
        ],
    ),
    make_stage(
        BRANCH_ID,
        "olcek",
        "8️⃣ Ölçekleme ve Marka",
        "Kazanan ürünü bulunca sırayla: bütçeyi artır, yeni kreatif ve kitle ekle, sepet ortalamasını "
        "yükselt, sonra tedariki ve markayı güçlendir.",
        [
            "Kazanan reklam setinin bütçesini 2-3 günde bir %20-30 artır",
            "Yeni kreatif, yeni ülke ve yeni kanal ile yatay büyü",
            "Sepet ortalamasını artır: paket, upsell, satın alma sonrası teklif",
            "E-posta/SMS akışları kur (sepet terk, satın alma sonrası)",
            "Toplu stokla ABD deposuna geç, teslim süresini kısalt",
            "Markalı ambalaj veya private label'a geç",
        ],
    ),
)

CRITERIA = (
    Criterion(
        key="wow",
        question="🤩 Ürün ilk bakışta dikkat çekiyor mu veya net bir sorunu çözüyor mu?",
        options=(("Hayır, sıradan", 1), ("Biraz", 3), ("Kesinlikle, 'vay' dedirtiyor", 5)),
        weight=3,
        tip="Wow etkisi zayıf: videoda dikkat çekmeyen ürün reklamda kaybolur. Önce/sonra veya sorun/çözüm gösterebileceğin ürün seç.",
    ),
    Criterion(
        key="markup",
        question="💰 Satış fiyatı, toplam maliyetin (ürün + kargo + gümrük) kaç katı?",
        options=(("2x altı", 1), ("2-2,5x", 2), ("2,5-3x", 3), ("3-4x", 4), ("4x üstü", 5)),
        weight=3,
        tip="Çarpan düşük: reklam maliyetini kaldıramazsın. En az 3x hedefle; paket teklifi veya daha ucuz tedarikçi dene.",
        hard_flag=True,
    ),
    Criterion(
        key="fiyat",
        question="🏷 Satış fiyatı aralığı (USD)?",
        options=(("15 $ altı", 1), ("15-25 $", 3), ("25-70 $", 5), ("70-150 $", 3), ("150 $ üstü", 2)),
        weight=2,
        tip="Fiyat aralığı ideal değil: ucuz üründe reklam kârı yer, pahalıda dürtüsel alım azalır. 25-70 $ en rahat bölge.",
    ),
    Criterion(
        key="kanit",
        question="📈 Talep kanıtı var mı? (aktif reklamlar, TikTok görüntülenmeleri, yorumlar)",
        options=(("Yok", 1), ("Zayıf", 2), ("Orta", 3), ("Güçlü", 5)),
        weight=3,
        tip="Talep kanıtı zayıf: Meta Ad Library'de bu ürünle haftalardır reklam veren mağaza ara; yoksa pazarı sen eğitmek zorunda kalırsın.",
    ),
    Criterion(
        key="doygunluk",
        question="🛒 Ürün Amazon/Walmart/Temu'da ucuza kolayca bulunuyor mu?",
        options=(("Her yerde ucuzu var", 1), ("Yaygın", 3), ("Zor bulunuyor", 5)),
        weight=2,
        tip="Pazar doygun: müşteri fiyatı karşılaştırıp başka yerden alır. Paket, aksesuar veya farklı bir açıyla sun.",
    ),
    Criterion(
        key="kreatif",
        question="🎬 Video reklamda kolay ve etkileyici gösterilebilir mi?",
        options=(("Zor", 1), ("Orta", 3), ("Kolay ve etkileyici", 5)),
        weight=2,
        tip="Kreatif zor: kullanımı 3 saniyede gösterilemeyen ürünü reklamla satmak pahalıdır.",
    ),
    Criterion(
        key="teslim",
        question="🚚 Hedef pazara teslim süresi?",
        options=(("15 günden fazla", 1), ("8-15 gün", 3), ("7 gün altı / yerel depo", 5)),
        weight=2,
        tip="Teslim uzun: iade, şikayet ve chargeback artar. Hedef ülke deposu olan tedarikçi bul.",
    ),
    Criterion(
        key="boyut",
        question="📦 Boyut / ağırlık / kırılganlık?",
        options=(("Büyük, ağır veya kırılgan", 1), ("Orta", 3), ("Küçük, hafif, sağlam", 5)),
        weight=1,
        tip="Kargo zor: uluslararası kargo ve hasar maliyeti kârı yer.",
    ),
    Criterion(
        key="iade",
        question="↩️ İade riski? (beden, arıza, beklentiyi karşılamama)",
        options=(("Yüksek", 1), ("Orta", 3), ("Düşük", 5)),
        weight=2,
        tip="İade riski yüksek: beden/arıza sorunu olan ürünlerde dropshipping iadesi pahalıdır, test siparişiyle kaliteyi doğrula.",
    ),
    Criterion(
        key="yasal",
        question="⚖️ Marka/patent veya kısıtlı kategori riski? (markalı ürün, sağlık iddiası, çocuk ürünü, batarya/sıvı)",
        options=(("Riskli", 1), ("Emin değilim", 3), ("Sorunsuz", 5)),
        weight=2,
        tip="Yasal risk: markalı/taklit ürün ve kısıtlı kategoriler reklam hesabını ve ödeme hesabını kapattırır.",
        hard_flag=True,
    ),
)


# ---------- 💵 Kâr hesabı ----------

PROFIT_FIELDS = (
    Field("sale_price", "🏷 Satış fiyatı ($)? Müşterinin ödediği toplam tutar.", kind="positive"),
    Field("product_cost", "📦 Tedarikçi ürün fiyatı ($)?"),
    Field("shipping", "🚚 Tedarikçi kargo ücreti ($)?"),
    Field(
        "duty_pct",
        "🛃 Gümrük vergisi, ürün maliyetinin yüzde kaçı?\n"
        "• Kargo DDP ve vergi fiyata dahilse 0\n"
        "• Çin → ABD: ürüne göre değişir, tedarikçiden öğren\n"
        "• AB: ürün başına ~3 € sabit; onu kargoya ekleyip buraya 0 yaz",
        default=0.0,
        kind="pct",
    ),
    Field("payment_fee_pct", "💳 Ödeme komisyonu (%)? Bilmiyorsan 3,5.", default=3.5, kind="pct"),
    Field("refund_rate_pct", "↩️ İade/chargeback oranı (%)? Bilmiyorsan 5.", default=5.0, kind="pct"),
    Field("other", "🧩 Sipariş başı diğer giderler ($)? (uygulama abonelikleri vb.) Yoksa 0.", default=0.0),
    Field("cpa", "📣 Satış başı reklam maliyeti, CPA ($)? Bilmiyorsan - yaz, başa baş CPA'yı hesaplarım.", default=0.0),
)


def profit_report(values: dict[str, float]) -> str:
    inp = global_profit.GlobalInput(**values)
    r = global_profit.calculate(inp)
    lines = [
        "💵 <b>Sipariş Başı Kâr Analizi</b>\n",
        f"Satış fiyatı: {fmt_usd(inp.sale_price)}",
        f"Toplam maliyet (ürün + kargo + gümrük): {fmt_usd(r.landed_cost)}",
        f"Fiyat çarpanı: <b>{fmt_num(r.markup)}x</b>",
        "",
        f"Reklamsız kâr: {fmt_usd(r.profit_before_ads)}",
    ]
    if r.breakeven_roas is None:
        lines.append("\n❌ Reklamsız bile zarar ediyorsun. Fiyatı artır veya maliyeti düşür.")
    else:
        lines += [
            f"🎯 Başa baş CPA: <b>{fmt_usd(r.profit_before_ads)}</b>",
            "<i>(Bir satış için reklama bundan fazla harcarsan zarar edersin)</i>",
            f"🎯 Başa baş ROAS: <b>{fmt_num(r.breakeven_roas)}</b>",
        ]
    if inp.cpa:
        status = "✅ Kârlı" if r.net_profit > 0 else "❌ Zarar"
        lines += [
            "",
            f"Reklam sonrası net kâr: <b>{fmt_usd(r.net_profit)}</b> ({status})",
            f"Net marj: {fmt_pct(r.margin_pct)}",
        ]

    lines.append("\n🏷 <b>Önerilen satış fiyatları</b>")
    lines.append(f"• 3x çarpan: {fmt_usd(r.landed_cost * 3)}")
    if inp.cpa:
        for target in (15, 25):
            price = global_profit.suggest_price(inp, target)
            lines.append(f"• %{target} net marj (bu CPA ile): " + (fmt_usd(price) if price else "ulaşılamaz"))
    else:
        lines.append("<i>CPA girersen hedef net marja göre fiyat da önerebilirim.</i>")

    if r.markup < 2.5:
        lines.append("\n⚠️ Çarpan 2,5x'in altında. Reklamla satışta bu marj genelde yetmez.")
    lines.append("\n<i>Gelir vergisi ve ABD satış vergisi dahil değildir.</i>")
    return "\n".join(lines)


# ---------- 📊 Reklam testi ----------

AD_FIELDS = (
    Field("spend", "💸 Toplam reklam harcaması ($)?", kind="positive"),
    Field("impressions", "👀 Gösterim sayısı?"),
    Field("clicks", "👆 Link tıklaması sayısı?"),
    Field("add_to_carts", "🛒 Sepete ekleme sayısı? Bilmiyorsan 0.", default=0.0),
    Field("purchases", "✅ Satın alma sayısı?"),
    Field("breakeven_cpa", "🎯 Başa baş CPA ($)? 💵 Kâr Hesabı'ndan öğrenebilirsin.", kind="positive"),
)


def ad_report(values: dict[str, float]) -> str:
    inp = ad_test.AdInput(**values)
    r = ad_test.evaluate(inp)
    lines = [
        "📊 <b>Reklam Testi Sonucu</b>\n",
        f"Karar: <b>{r.decision}</b>",
        r.reason,
        "",
        f"CTR: {fmt_pct(r.ctr_pct) if r.ctr_pct is not None else '-'}",
        f"CPC: {fmt_usd(r.cpc) if r.cpc is not None else '-'}",
        f"CPM: {fmt_usd(r.cpm) if r.cpm is not None else '-'}",
        f"CPA: {fmt_usd(r.cpa) if r.cpa is not None else 'satış yok'} "
        f"(başa baş: {fmt_usd(inp.breakeven_cpa)})",
    ]
    if r.diagnoses:
        lines.append("\n🩺 <b>Teşhis</b>")
        lines += [f"• {d}" for d in r.diagnoses]
    lines.append("\n<i>Eşikler yaygın pratik kurallardır; kararı kendi verinle birlikte değerlendir.</i>")
    return "\n".join(lines)


BRANCH = Branch(
    id=BRANCH_ID,
    title="🅲 Global Dropshipping",
    summary=SUMMARY,
    ready=True,
    stages=STAGES,
    criteria=CRITERIA,
    tools=(
        FormTool("kar", "💵 Kâr Hesabı", "💵 Kâr Hesabı (USD)", PROFIT_FIELDS, profit_report),
        FormTool("reklam", "📊 Reklam Testi", "📊 Reklam Testi", AD_FIELDS, ad_report),
    ),
)
