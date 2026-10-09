"""🅲 Global dropshipping yol haritası: aşamalar, görevler ve her görev için "Nasıl yapılır" rehberi.

Yasal ve vergisel adımlar genel bilgilendirmedir; kesin karar için mali müşavir / avukat görüşü alınmalı.
"""

from __future__ import annotations

from ..core.roadmap import enrich, make_stage

BRANCH_ID = "c"

_BASE = (
    make_stage(
        BRANCH_ID,
        "pazar",
        "1️⃣ Hedef Pazar ve Bütçe",
        "Test edilen ürünlerin çoğu tutmaz; bütçeni 3-5 ürün testine yetecek şekilde planla. "
        "ABD en büyük pazar ama gümrük maliyeti en yüksek olanlardan; UK, CA ve AU iyi alternatifler.",
        [
            (
                "Hedef pazarı seç (ABD, UK, AB, CA, AU) ve o pazarın gümrük kuralını öğren",
                [
                    "🇺🇸 ABD: en büyük pazar, reklam maliyeti en yüksek. 800 $ muafiyeti kalktı; Çin'den gelen her pakete gümrük uygulanıyor, DDP veya ABD deposu şart.",
                    "🇬🇧 UK: İngilizce, reklam daha ucuz. 135 £ altı gönderilerde %20 KDV'yi satıcı tahsil eder, UK KDV kaydı gerekir.",
                    "🇪🇺 AB: 1 Temmuz 2026'dan beri 150 € altı gönderilerde ürün başına 3 € gümrük var. KDV için IOSS kaydı (aracı kurum üzerinden) kullanılır.",
                    "🇨🇦🇦🇺 Kanada / Avustralya: İngilizce, rekabet daha az; ülkenin kendi vergi kaydı kurallarını kontrol et.",
                    "Tek pazarla başla. Meta Ad Library'de o ülkeyi seçip nişindeki reklam yoğunluğuna bak.",
                ],
            ),
            (
                "Mağaza tipine karar ver: tek ürün, niş mağaza veya genel mağaza (öneri: niş)",
                [
                    "Genel mağaza: her şey satılır, test hızlı ama güven ve dönüşüm düşük.",
                    "Niş mağaza (ör. evcil hayvan, mutfak, fitness): aynı kitleye birden çok ürün, upsell kolay, marka hissi var. Başlangıç için önerilen bu.",
                    "Tek ürün mağaza: dönüşüm en yüksek ama her yeni ürün testi yeni mağaza demek.",
                    "İlk 3-5 ürün testini aynı mağazada yapabileceğin bir niş seç.",
                ],
            ),
            (
                "Test bütçesi ayır: ürün başına en az 300-500 $ reklam + 2-3 aylık sabit giderler",
                [
                    "Sabit giderleri listele: Shopify planı, alan adı, uygulama abonelikleri, şirket ve registered agent yıllık ücretleri.",
                    "Toplam bütçe ≈ (aylık sabit gider × 3) + (ürün başı test bütçesi × 3-5 ürün) + numune siparişleri.",
                    "💵 Kâr Hesabı ile başa baş CPA'nı öğren; reklam başına test bütçesi en az bunun 2-3 katı olmalı.",
                    "Bu parayı kaybetmeyi göze alabileceğin miktarda tut; ilk ayda kâr bekleme.",
                ],
            ),
            (
                "Mali müşavirle, yurt dışı şirket kazancının Türkiye'de nasıl beyan edileceğini konuş",
                [
                    "Türkiye'de yerleşik olduğun için yurt dışı şirketinden elde ettiğin kazanç Türkiye'de de vergilendirilebilir.",
                    "Müşavire sor: LLC kârını nasıl beyan ederim, kontrol edilen yabancı kurum kuralları beni etkiler mi, Türkiye'ye para transferinde neye dikkat etmeliyim?",
                    "ABD tarafı: yabancı sahipli tek üyeli LLC'ler her yıl IRS'e Form 5472 + pro forma 1120 vermek zorunda. Kaçırmanın cezası çok yüksek; şirket kurma servisleri genelde bunu da yapar.",
                    "Konuşmanın sonunda yazılı bir yol haritası iste.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "sirket",
        "2️⃣ Yurt Dışı Şirket ve Ödeme",
        "Stripe ve PayPal Türkiye'de yok. En yaygın yol: ABD LLC + EIN + şirket adına ABD banka hesabı "
        "+ ödeme sağlayıcısı. Shopify Payments 2026'da ABD'de fiziksel varlığı olmayan yabancıları "
        "sıkça reddediyor; yedek planın olsun.",
        [
            (
                "Şirket ülkesini seç (ABD LLC veya UK Ltd)",
                [
                    "ABD LLC: Stripe ve ABD bankalarına erişim. Eyalet olarak genelde Wyoming (düşük yıllık ücret) veya New Mexico (yıllık rapor yok) seçilir; Delaware daha pahalıdır, yatırımcı almayacaksan gerekmez.",
                    "UK Ltd: Companies House üzerinden hızlı kurulur ama İngiltere kurumlar vergisi ve muhasebe yükümlülüğü getirir.",
                    "Karşılaştır: kuruluş + yıllık maliyet, vergi yükü, banka ve ödeme sağlayıcısı erişimi.",
                    "Seçimi mali müşavirinle birlikte netleştir.",
                ],
            ),
            (
                "Şirketi kur (kendin veya şirket kurma servisiyle)",
                [
                    "Servislerle (Stripe Atlas, doola, Firstbase vb.) kurulum, registered agent ve EIN tek pakette yapılır.",
                    "Kendin kuracaksan: eyaletin resmi sitesinden Articles of Organization doldur ve bir registered agent tut.",
                    "Hazırla: şirket adı (mağaza markanla uyumlu), pasaport, adres bilgisi.",
                    "Belgeleri sakla: Articles of Organization ve Operating Agreement banka ve ödeme başvurularında istenir.",
                ],
            ),
            (
                "EIN al (SSN yoksa IRS'e SS-4 formuyla telefon/faks veya servis üzerinden)",
                [
                    "EIN, şirketin ABD vergi numarasıdır; banka ve Stripe için şart.",
                    "SSN'in yoksa IRS'in online başvurusunu kullanamazsın: Form SS-4'ü doldurup faksla gönder veya ABD dışından telefonla başvur.",
                    "Şirket kurma servisi kullanıyorsan EIN genelde pakete dahildir.",
                    "Gelen EIN onay mektubunu (CP 575) sakla, her başvuruda istenir.",
                ],
            ),
            (
                "Şirket adına banka hesabı aç (Mercury, Relay, Wise Business vb.)",
                [
                    "Online bankalara başvur; genelde istenen: şirket kuruluş belgeleri, EIN mektubu, pasaport, adres kanıtı.",
                    "Bankalar yabancı sahipli şirket kabul politikalarını değiştirebilir; reddedilirsen başka bir seçenek dene.",
                    "Kişisel ve şirket parasını asla karıştırma; tüm gelir ve giderler şirket hesabından geçsin.",
                ],
            ),
            (
                "Ödeme sağlayıcısına başvur (Shopify Payments, Stripe, PayPal Business)",
                [
                    "Başvurudan önce mağazayı bitir: politikalar, iletişim bilgisi ve ürünler hazır olsun. Yarım mağaza reddedilir.",
                    "Önce Shopify Payments'ı dene, en sorunsuz seçenek bu.",
                    "Reddedilirse Shopify'ın ödeme ayarlarındaki uyumlu üçüncü taraf sağlayıcılara başvur; bu durumda Shopify plana göre ek işlem ücreti keser.",
                    "Yanına PayPal Business ekle; birçok müşteri PayPal ile ödemeyi tercih eder.",
                    "Alternatif: Stripe'ı doğrudan destekleyen bir platform (ör. WooCommerce) kullanmak.",
                ],
            ),
            (
                "Kazancı Türkiye'ye aktarma ve beyan yöntemini netleştir",
                [
                    "Akış genelde şöyle: ödeme sağlayıcısı → ABD şirket hesabı → döviz transferi → Türkiye'deki hesabın.",
                    "Transfer servislerinin kur ve ücretlerini karşılaştır.",
                    "Her transferin açıklamasını ve belgesini tut; müşavirinin istediği formatta arşivle.",
                ],
            ),
            (
                "Satış vergisi (ABD sales tax) ve AB KDV (IOSS) yükümlülüklerini kontrol et",
                [
                    "ABD: satış vergisi eyalet bazındadır. Çoğu eyalette yıllık 100.000 $ satış gibi eşikler var; eşiği geçince o eyalette kayıt ve tahsilat gerekir.",
                    "Shopify'ın vergi raporları hangi eyalette eşiğe yaklaştığını gösterir; düzenli kontrol et.",
                    "AB'ye satıyorsan 150 € altı siparişler için IOSS kaydı ile KDV'yi satışta tahsil et.",
                    "UK'ye satıyorsan 135 £ altı gönderiler için UK KDV kaydı gerekir.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "urun",
        "3️⃣ Ürün Araştırması",
        "Kazanan ürün: ilk bakışta 'vay' dedirtir veya net bir sorunu çözer, mağazalarda kolay bulunmaz, "
        "maliyetinin en az 3 katına satılır, 25-70 $ aralığındadır, hafiftir ve markalı değildir.",
        [
            (
                "Meta Ad Library ve TikTok'ta son 30 günde artan reklamları tara",
                [
                    "facebook.com/ads/library → hedef ülke → 'Tüm reklamlar'. Nişinle ilgili kelimeler ve 'free shipping', '50% off' gibi ifadelerle ara.",
                    "Aynı ürün için çok sayıda aktif reklam varyasyonu varsa o mağaza bütçe harcıyor demektir; muhtemelen kârlı satıyor.",
                    "TikTok Creative Center → Top Ads ve trend ürünlere bak; #tiktokmademebuyit etiketini tara.",
                    "Her ürün için not al: reklam linki, mağaza, ilk reklam tarihi, varyasyon sayısı.",
                ],
            ),
            (
                "20 aday ürün listesi çıkar",
                [
                    "Bir tablo aç. Kolonlar: ürün, kaynak link, tedarikçi fiyatı, tahmini satış fiyatı, rakip mağaza, aktif reklam sayısı, notlar.",
                    "Ek kaynaklar: CJ Dropshipping trend ürünleri, AliExpress çok satanlar, Amazon 'Movers & Shakers'.",
                    "Sadece nişine uyan ürünleri listeye al.",
                ],
            ),
            (
                "Her adayı 🔍 Ürün Analizi ile puanla",
                [
                    "Bu dalın ana menüsünden 🔍 Ürün Analizi'ni aç ve her ürünü tek tek puanla.",
                    "70 ve üzeri skor alanları ayır; 'Kritik sorun' çıkanları direkt ele.",
                    "50-69 arası ürünler yedek listede kalsın.",
                ],
            ),
            (
                "En iyi 3-5 adayın 💵 Kâr Hesabını yap (gümrük dahil)",
                [
                    "Tedarikçinin hedef ülkeye DDP kargo fiyatını kullan; DDP değilse gümrük yüzdesini gir.",
                    "Başa baş CPA'yı not al. Başa baş CPA'sı çok düşük ürünler (ör. 10-15 $ altı) reklamla zor kârlı olur.",
                    "Fiyat çarpanı 3x'in altındaysa fiyatı veya paket teklifini yeniden düşün.",
                ],
            ),
            (
                "Rakip mağazaları incele: fiyat, teklif, ürün sayfası, yorumlar",
                [
                    "Rakibin fiyatını, paket tekliflerini (2 al 1 bedava vb.) ve vaat ettiği kargo süresini not et.",
                    "Ürün sayfasının yapısına bak: başlık, video, fayda maddeleri, SSS.",
                    "Yorumlardaki şikayetleri oku; bunlar senin farklılaşma fırsatın.",
                    "Kopyalama, daha iyisini yap: daha net teklif, daha iyi video, daha hızlı kargo.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "tedarik",
        "4️⃣ Tedarikçi ve Kargo",
        "CJ Dropshipping (kendi depoları, ABD deposu, DDP gönderim), DSers (AliExpress), AutoDS, Zendrop, "
        "Spocket (ABD/AB depolu tedarikçiler). Gümrük her pakete uygulandığı için DDP gönderim veya "
        "hedef ülke deposu seç; yoksa müşteri kapıda vergi öder, iade ve chargeback patlar.",
        [
            (
                "En az 2 tedarikçiden ürün + kargo fiyatı ve teslim süresi al",
                [
                    "CJ: ürün linkiyle 'sourcing request' aç. AliExpress: DSers üzerinden ürün ve tedarikçi karşılaştır. ABD depolu: Spocket veya Zendrop kataloğuna bak.",
                    "Her tedarikçiye sor: birim fiyat, hedef ülkeye kargo ücreti, işlem süresi, teslim süresi, DDP mi, hasar/kayıp politikası.",
                    "Cevapları tabloya yaz ve yan yana karşılaştır.",
                ],
            ),
            (
                "Gönderimin DDP olduğunu ve gümrük maliyetini yazılı teyit et",
                [
                    "Tedarikçiye açıkça sor: 'Bu gönderim DDP mi? Gümrük vergileri fiyata dahil mi? Müşteri teslimatta ek ödeme yapacak mı?'",
                    "Cevabı yazılı (mesaj veya e-posta) al ve sakla.",
                    "DDP değilse gümrük yüzdesini öğren ve 💵 Kâr Hesabı'na gir.",
                ],
            ),
            (
                "Test siparişi ver: kalite, paketleme, teslim süresi",
                [
                    "Kendi adresine veya hedef ülkede bir tanıdığına sipariş ver.",
                    "Ölç: işlem süresi, toplam teslim süresi, takip numarası çalışıyor mu, paket ve ürün durumu.",
                    "Ürünü gelir gelmez videoya çek; bu görüntüler en iyi reklam malzemen olur.",
                ],
            ),
            (
                "Pakette fiyat, fatura veya tedarikçi logosu olmamasını sağla",
                [
                    "Tedarikçiye not geç: 'No invoice, no price, no logo in the package.'",
                    "CJ gibi platformlarda nötr veya özel ambalaj seçeneklerini kontrol et.",
                    "Test siparişinde bu talimata uyulup uyulmadığını kontrol et.",
                ],
            ),
            (
                "Ürün tutarsa özel ajan veya ABD depo stoğu seçeneğini araştır",
                [
                    "Günde düzenli sipariş almaya başlayınca (ör. 10-20+) özel tedarik ajanı daha ucuz ve hızlı olur.",
                    "ABD deposuna toplu stok göndermek teslim süresini birkaç güne indirir.",
                    "Stok yaparken nakit akışını hesapla; 2-4 haftalık satışa yetecek kadar başla.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "magaza",
        "5️⃣ Shopify Mağaza",
        "Müşteri markanı tanımıyor; güveni sayfa kazanır. Net kargo süresi, açık iade politikası, "
        "gerçek iletişim bilgisi ve güçlü ürün sayfası şart.",
        [
            (
                "Shopify hesabı aç ve plan seç",
                [
                    "shopify.com üzerinden deneme hesabı aç; dönem dönem ilk aylar için indirimli promosyonlar oluyor.",
                    "Başlangıç için en temel plan yeterli.",
                    "Mağaza adını nişine ve şirket adına uygun seç.",
                ],
            ),
            (
                "Alan adı al, profesyonel e-posta kur",
                [
                    "Kısa, akılda kalıcı bir .com alan adı al (Shopify'dan veya bir alan adı firmasından).",
                    "Alan adını Shopify'a bağla.",
                    "support@alanadin.com gibi bir e-posta kur (Google Workspace, Zoho vb.); Gmail adresi güven vermez.",
                ],
            ),
            (
                "Hızlı bir tema kur ve marka kimliğini (logo, renk) hazırla",
                [
                    "Shopify'ın ücretsiz, hızlı temalarından biriyle (ör. Dawn) başla.",
                    "Logo ve favicon'u Canva gibi bir araçla hazırla; 2 ana renk seç.",
                    "Trafiğin çoğu mobilden gelir; her değişikliği önce telefonda kontrol et.",
                ],
            ),
            (
                "Zorunlu sayfalar: Refund, Shipping, Privacy, Terms, Contact, About",
                [
                    "Shopify Ayarlar → Politikalar bölümünden şablonları oluştur ve kendine göre düzenle.",
                    "Shipping Policy'ye gerçek işlem ve teslim sürelerini yaz; olduğundan kısa gösterme.",
                    "Contact sayfasına destek e-postanı ve bir iletişim formu koy.",
                    "Tüm sayfaları mağazanın alt menüsüne (footer) linkle.",
                ],
            ),
            (
                "Ürün sayfası: fayda başlıkları, GIF/video, karşılaştırma, SSS, yorumlar",
                [
                    "Ürün başlığı net olsun; altına 3-5 fayda maddesi yaz (özellik değil, faydayı anlat).",
                    "Ürünü çalışırken gösteren GIF veya video ekle.",
                    "Sorun → çözüm bölümü ve 'bizim ürün vs diğerleri' karşılaştırması ekle.",
                    "SSS'de kargo süresi, iade ve kullanım sorularını cevapla.",
                    "Yorum uygulamasıyla sadece gerçek yorumları göster. ABD'de sahte yorum FTC kuralıyla yasak, ceza riski var.",
                ],
            ),
            (
                "Tedarikçi uygulamasını bağla (CJ, DSers, AutoDS) ve ürünü içe aktar",
                [
                    "Shopify App Store'dan tedarikçinin uygulamasını kur ve hesabını bağla.",
                    "Ürünü içe aktar; başlık, açıklama ve görselleri kendi sayfana göre düzenle.",
                    "Varyantları (renk, beden) tedarikçideki doğru ürünlerle eşleştir; yanlış eşleştirme yanlış ürün gönderir.",
                ],
            ),
            (
                "Fiyat, karşılaştırma fiyatı ve paket/upsell teklifini ayarla",
                [
                    "💵 Kâr Hesabı'ndaki önerilen fiyatı kullan.",
                    "Karşılaştırma (üstü çizili) fiyatı gerçekçi tut; hiç satılmamış sahte bir 'eski fiyat' yasal risk taşır.",
                    "Paket teklifi ekle: '2 al %15 indirim' gibi; sepet ortalamasını yükseltir.",
                ],
            ),
            (
                "Ödeme ve kargo ayarlarını yap, uçtan uca test siparişi ver",
                [
                    "Kargo ayarlarında sadece hedef ülkelerine gönderim aç.",
                    "Kargoyu fiyata dahil edip 'ücretsiz kargo' sunmak genelde dönüşümü artırır.",
                    "Shopify'ın test ödeme moduyla test siparişi ver, sonra gerçek kartla küçük bir sipariş verip iade et.",
                    "Müşteriye giden e-postaları (sipariş onayı, kargo bildirimi) kontrol et.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "reklam",
        "6️⃣ Reklam ve Test",
        "Video reklam ana silah. Ürün başına 3-5 farklı kreatifle, günlük 20-50 $ bütçeyle test et. "
        "Başa baş CPA'nın 2-3 katı harcayıp satış alamayan reklamı kapat.",
        [
            (
                "Meta Business, reklam hesabı, Pixel ve Conversions API kur",
                [
                    "business.facebook.com üzerinden bir işletme hesabı aç; Facebook sayfası ve Instagram hesabını bağla.",
                    "Reklam hesabını aç: para birimi USD, saat dilimi hedef pazarın.",
                    "Shopify'da 'Facebook & Instagram' uygulamasını kur; Pixel ve Conversions API otomatik bağlanır.",
                    "Events Manager'da test siparişiyle 'Purchase' olayının geldiğini doğrula; alan adını doğrula.",
                ],
            ),
            (
                "TikTok Ads hesabı ve Pixel kur (opsiyonel)",
                [
                    "ads.tiktok.com üzerinden reklam hesabı aç.",
                    "Shopify'ın TikTok uygulamasıyla Pixel'i bağla.",
                    "Organik TikTok hesabı da aç; ürün videolarını organik paylaşmak ücretsiz test sağlar.",
                ],
            ),
            (
                "3-5 farklı video kreatif hazırla (farklı hook'lar, UGC tarzı)",
                [
                    "İlk 3 saniye (hook) her şeydir: sorunu göster, sonucu göster ya da şaşırtıcı bir kullanım göster.",
                    "15-30 saniye, dikey (9:16) ve altyazılı videolar hazırla; çoğu kişi sessiz izler.",
                    "Test siparişinde çektiğin görüntüleri kullan veya UGC içerik üreticisiyle çalış.",
                    "Her video farklı bir hook ile başlasın; böylece hangisinin çalıştığını görürsün.",
                ],
            ),
            (
                "💵 Kâr Hesabı ile başa baş CPA ve ROAS'ı öğren",
                [
                    "Bu dalın 💵 Kâr Hesabı aracını aç ve gerçek maliyetlerini gir.",
                    "Başa baş CPA ve başa baş ROAS'ı not et.",
                    "Kural: bir reklam başa baş CPA'nın 2-3 katını harcayıp satış getirmediyse kapatılır.",
                ],
            ),
            (
                "Test kampanyasını aç (geniş hedefleme, satın alma optimizasyonu)",
                [
                    "Kampanya hedefi: Satış (Sales), dönüşüm olayı: Purchase.",
                    "Geniş hedefleme kullan: sadece ülke ve gerekiyorsa yaş/cinsiyet; Meta'nın algoritması kitleyi bulur.",
                    "Her kreatifi ayrı reklam olarak koy; günlük 20-50 $ bütçeyle başla.",
                    "İlk 48-72 saat ayarlara dokunma; algoritmanın öğrenmesine izin ver.",
                ],
            ),
            (
                "Her gün 📊 Reklam Testi ile kapat / devam / ölçekle kararı ver",
                [
                    "Ads Manager'dan her reklamın harcama, gösterim, link tıklaması, sepete ekleme ve satın alma sayılarını al.",
                    "📊 Reklam Testi aracına gir ve verdiği kararı uygula.",
                    "Günde bir kez bak; saatlik değişiklik yapmak testi bozar.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "operasyon",
        "7️⃣ Sipariş ve Müşteri Hizmetleri",
        "Yüksek iade ve chargeback oranı ödeme hesabını kapattırabilir. Takip numarasını hızlı yükle, "
        "sorulara 24 saat içinde dön, sorunlu siparişi tartışmadan çöz.",
        [
            (
                "Otomatik sipariş iletimini (auto-fulfill) aç",
                [
                    "Tedarikçi uygulamanda (CJ, DSers, AutoDS) otomatik sipariş ve ödemeyi aç.",
                    "Tedarikçi bakiyeni veya kartını hazır tut; ödenmemiş sipariş gönderilmez.",
                    "Her gün bir kez 'ödeme bekleyen' veya 'hatalı' siparişleri kontrol et.",
                ],
            ),
            (
                "Takip numarası senkronunu ve sipariş takip sayfasını kur",
                [
                    "Uygulamanın takip numarası senkronu açık olsun; sipariş Shopify'da otomatik 'gönderildi' olsun.",
                    "Mağazaya bir sipariş takip sayfası uygulaması ekle; müşteri 'siparişim nerede' diye yazmadan durumu görsün.",
                ],
            ),
            (
                "Destek şablonları hazırla: kargo nerede, iade, hasarlı ürün",
                [
                    "Hazır cevaplar yaz: 'Siparişim nerede?', 'Hasarlı geldi', 'İade istiyorum', 'Adresimi değiştirmek istiyorum'.",
                    "Her mesaja 24 saat içinde cevap ver; geç cevap chargeback'e döner.",
                    "Kibar, net ve çözüm odaklı ol; tartışma kazanmaya çalışma.",
                ],
            ),
            (
                "Hasar/kayıp sürecini tedarikçiyle netleştir (fotoğrafla yeniden gönderim)",
                [
                    "Müşteriden hasarın fotoğrafını veya videosunu iste.",
                    "Tedarikçiye ilet; yeniden gönderim veya iade talep et.",
                    "Ürünü Çin'e geri göndertmek genelde ürün bedelinden pahalıdır; çoğu durumda iade yapıp ürünü müşteride bırakmak daha mantıklı.",
                ],
            ),
            (
                "Chargeback ve dispute'ları haftalık kontrol et",
                [
                    "Ödeme sağlayıcının panelindeki 'Disputes' bölümünü haftada en az bir kez kontrol et.",
                    "Kanıt gönder: teslim kaydı olan takip numarası, müşteriyle yazışmalar, politika sayfaların.",
                    "Chargeback oranını %1'in altında tutmaya çalış; yüksek oran hesabın kapanmasına yol açabilir.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "olcek",
        "8️⃣ Ölçekleme ve Marka",
        "Kazanan ürünü bulunca sırayla: bütçeyi artır, yeni kreatif ve kitle ekle, sepet ortalamasını "
        "yükselt, sonra tedariki ve markayı güçlendir.",
        [
            (
                "Kazanan reklam setinin bütçesini 2-3 günde bir %20-30 artır",
                [
                    "Ani büyük artışlar algoritmayı sıfırlar; kademeli artır.",
                    "Artıştan sonra CPA başa başın üstüne çıkarsa bütçeyi bir önceki seviyeye geri çek.",
                    "Kazanan reklamı yeni bir kampanyaya kopyalayarak da büyütebilirsin.",
                ],
            ),
            (
                "Yeni kreatif, yeni ülke ve yeni kanal ile yatay büyü",
                [
                    "Her hafta yeni hook'larla yeni videolar test et; reklamlar zamanla yıpranır.",
                    "Aynı dili konuşan yeni bir ülke ekle (ör. ABD'den sonra UK, CA, AU).",
                    "TikTok veya Google Shopping gibi ikinci bir kanal dene.",
                ],
            ),
            (
                "Sepet ortalamasını artır: paket, upsell, satın alma sonrası teklif",
                [
                    "Adet indirimleri ekle: 2 alana %10, 3 alana %20 gibi.",
                    "Ödeme sayfasında tamamlayıcı ürün öner.",
                    "Satın alma sonrası tek tıkla ek ürün teklifi sun.",
                    "Ücretsiz kargo eşiğini sepet ortalamasının biraz üstüne koy.",
                ],
            ),
            (
                "E-posta/SMS akışları kur (sepet terk, satın alma sonrası)",
                [
                    "Klaviyo veya Shopify Email gibi bir araçla başla.",
                    "Akışlar: hoş geldin, sepet terk (2-3 e-posta), satın alma sonrası, geri kazanma.",
                    "SMS gönderiyorsan müşterinin açık iznini al.",
                ],
            ),
            (
                "Toplu stokla ABD deposuna geç, teslim süresini kısalt",
                [
                    "CJ'nin ABD deposu veya bir 3PL ile anlaş.",
                    "2-4 haftalık satışa yetecek stokla başla; satış hızına göre yenile.",
                    "Teslim süresi kısaldıkça iade, şikayet ve chargeback düşer.",
                ],
            ),
            (
                "Markalı ambalaj veya private label'a geç",
                [
                    "Logolu kutu veya kart gibi özel ambalajla başla.",
                    "Satışlar oturunca ürünün üzerine kendi logonu bastır (private label).",
                    "Kendi ürün fotoğraf ve videolarını çek; markalı ürün daha yüksek fiyata satılır ve zor kopyalanır.",
                ],
            ),
        ],
    ),
)


# ---------- Ders alanları ve botun araştırıp sunduğu seçenekler ----------
# Kaynak: 2026 tarihli eyalet ücret karşılaştırmaları, tedarikçi platform karşılaştırmaları ve niş
# raporları. Ücretler kaynaklar arasında farklı olabildiği için yaklaşık verildi.

EXTRA = {
    "c.pazar.1": {
        "text": "Hedef pazarını seç",
        "why": "Gümrük, kargo, ödeme ve reklam maliyetin bu karara göre değişir.",
        "options": [
            {
                "key": "us",
                "title": "🇺🇸 ABD",
                "lines": [
                    "En büyük pazar, en fazla müşteri ve ürün verisi",
                    "800 $ gümrük muafiyeti kalktı: Çin'den gelen her paket gümrüklü; DDP veya ABD deposu şart",
                    "Reklam maliyeti en yüksek pazar",
                ],
            },
            {
                "key": "uk",
                "title": "🇬🇧 İngiltere",
                "lines": [
                    "İngilizce, ABD'ye göre daha ucuz reklam",
                    "135 £ altı gönderilerde %20 KDV'yi satıcı tahsil eder; UK KDV kaydı gerekir",
                ],
            },
            {
                "key": "eu",
                "title": "🇪🇺 Avrupa Birliği",
                "lines": [
                    "Büyük pazar ama çok dilli; ülke ülke reklam ve çeviri gerekir",
                    "1 Temmuz 2026'dan beri 150 € altı gönderilerde ürün başına 3 € gümrük; KDV için IOSS kaydı",
                ],
            },
            {
                "key": "cau",
                "title": "🇨🇦🇦🇺 Kanada / Avustralya",
                "lines": [
                    "İngilizce, rekabet ABD'den az, sepet ortalaması iyi",
                    "Pazar daha küçük; kargo süreleri ve ülkenin vergi kuralları kontrol edilmeli",
                ],
            },
        ],
        "how": ["Tek pazarla başla; sistem oturunca aynı dili konuşan ikinci pazarı ekle."],
    },
    "c.pazar.2": {
        "text": "Mağaza tipini seç",
        "why": "Mağaza tipi; güveni, dönüşüm oranını ve yeni ürün test etme hızını belirler.",
        "options": [
            {
                "key": "nis",
                "title": "Niş mağaza (önerilen)",
                "lines": [
                    "Tek bir ilgi alanı (ör. evcil hayvan, mutfak): aynı kitleye birden çok ürün",
                    "Upsell kolay, marka hissi var; ürün testleri aynı mağazada yapılır",
                ],
            },
            {
                "key": "tek",
                "title": "Tek ürün mağazası",
                "lines": [
                    "Dönüşüm en yüksek; sayfa tamamen tek ürüne odaklı",
                    "Her yeni ürün testi yeni bir mağaza demek",
                ],
            },
            {
                "key": "genel",
                "title": "Genel mağaza",
                "lines": [
                    "Her şey satılır, test çok hızlı",
                    "Güven ve dönüşüm düşük; marka oluşmaz",
                ],
            },
        ],
    },
    "c.pazar.3": {
        "why": "Test edilen ürünlerin çoğu tutmaz; bütçen 3-5 testi kaldırmalı.",
        "done": "Toplam test bütçen ve aylık sabit giderin yazılı.",
    },
    "c.pazar.4": {
        "why": "Türkiye'de yerleşik olarak yurt dışı şirketten kazanç elde etmenin vergi sonuçları var.",
        "done": "Müşavirinden yazılı bir yol haritası aldın.",
    },
    "c.sirket.1": {
        "text": "Şirketini nerede kuracağını seç",
        "why": "Stripe/PayPal Türkiye'de yok; ödeme alabilmek için yurt dışı şirket gerekir.",
        "options": [
            {
                "key": "nm",
                "title": "New Mexico LLC (en ucuz)",
                "lines": [
                    "Kuruluş yaklaşık 50 $; yıllık eyalet ücreti ve yıllık rapor yok",
                    "Eksi: eyalet hukuku Wyoming kadar yerleşik değil",
                ],
            },
            {
                "key": "wy",
                "title": "Wyoming LLC (en yaygın)",
                "lines": [
                    "Kuruluş yaklaşık 100 $ + yıllık yaklaşık 60 $",
                    "Yabancılar için en çok tercih edilen; eyalet gelir vergisi yok",
                ],
            },
            {
                "key": "de",
                "title": "Delaware LLC",
                "lines": [
                    "Kuruluş yaklaşık 110 $ + yıllık 300-400 $ (kaynaklar çelişiyor)",
                    "Yatırımcı almayacaksan genelde gereksiz pahalı",
                ],
            },
            {
                "key": "uk",
                "title": "İngiltere Ltd",
                "lines": [
                    "Kuruluşu hızlı; Stripe UK kullanılabilir",
                    "İngiltere kurumlar vergisi ve yıllık hesap yükümlülüğü getirir",
                ],
            },
        ],
        "how": [
            "ABD seçeneklerinde her yıl ayrıca kayıtlı temsilci (registered agent) ücreti var (yaklaşık 100-200 $).",
            "Seçimini mali müşavirinle netleştir.",
        ],
    },
    "c.sirket.2": {
        "text": "Şirketini kur",
        "done": "Şirketin kuruldu ve kuruluş belgelerin elinde.",
        "options": [
            {
                "key": "servis",
                "title": "Şirket kurma servisiyle",
                "lines": [
                    "Stripe Atlas, doola, Firstbase gibi servisler kuruluş + kayıtlı temsilci + EIN'i paketler",
                    "Artı: kolay ve hızlı; Eksi: paket ücreti eyalet ücretinin üstüne eklenir",
                ],
            },
            {
                "key": "kendin",
                "title": "Kendin kur",
                "lines": [
                    "Eyaletin resmi sitesinden kuruluş belgesini doldurur, kayıtlı temsilciyi ayrı tutarsın",
                    "Artı: daha ucuz; Eksi: İngilizce form ve yazışma gerekir, EIN'i ayrıca alırsın",
                ],
            },
        ],
    },
    "c.sirket.3": {
        "why": "EIN, şirketin ABD vergi numarasıdır; banka ve ödeme sağlayıcıları ister.",
        "done": "EIN onay mektubun (CP 575) elinde.",
    },
    "c.sirket.4": {
        "text": "Şirket adına ABD banka hesabı aç",
        "done": "Şirket adına banka hesabın açıldı.",
        "options": [
            {
                "key": "mercury",
                "title": "Mercury",
                "lines": [
                    "Online ABD bankacılık; LLC'ler arasında yaygın",
                    "Yabancı sahipli şirket kabul politikasını başvurmadan kontrol et",
                ],
            },
            {
                "key": "relay",
                "title": "Relay",
                "lines": [
                    "Online işletme hesabı; birden fazla alt hesap ile bütçe ayırma kolay",
                    "Yabancı sahipli şirket kabul politikasını başvurmadan kontrol et",
                ],
            },
            {
                "key": "wise",
                "title": "Wise Business",
                "lines": [
                    "Çok dövizli hesap; Türkiye'ye para transferi kolay",
                    "Bazı ödeme sağlayıcıları ABD banka hesabı şartı arayabilir; kontrol et",
                ],
            },
        ],
        "warn": "Bankalar kabul politikalarını değiştirebiliyor; reddedilirsen diğer seçeneği dene.",
    },
    "c.sirket.5": {
        "text": "Ödeme sağlayıcını seç ve başvur",
        "done": "En az bir ödeme sağlayıcın onaylandı.",
        "options": [
            {
                "key": "shopify",
                "title": "Shopify Payments",
                "lines": [
                    "En sorunsuz entegrasyon, ek işlem ücreti yok",
                    "2026'da ABD'de fiziksel/operasyonel varlığı olmayan yabancıları sık reddediyor",
                ],
            },
            {
                "key": "stripe",
                "title": "Stripe (LLC + EIN ile)",
                "lines": [
                    "SSN olmadan LLC + EIN + ABD banka hesabıyla açılabiliyor",
                    "Shopify'da üçüncü taraf ödeme kullanınca plana göre ek işlem ücreti kesilir",
                ],
            },
            {
                "key": "paypal",
                "title": "PayPal Business (ek olarak)",
                "lines": [
                    "Birçok müşteri PayPal ile ödemeyi tercih eder; dönüşümü artırır",
                    "Ana ödeme yöntemi değil, yanına ek olarak kullan",
                ],
            },
        ],
        "how": ["Başvurudan önce mağazanı bitir: politikalar, iletişim ve ürünler hazır olsun."],
    },
    "c.sirket.6": {
        "why": "Para trafiği belgeli olmazsa vergi ve banka tarafında sorun yaşarsın.",
        "done": "Transfer akışın ve belge arşivleme düzenin belli.",
    },
    "c.sirket.7": {
        "why": "Eşikleri geçince satış vergisi tahsil etmezsen sonradan ceza ve geriye dönük vergi çıkar.",
        "done": "Hangi pazarda hangi vergi kaydının gerektiğini biliyorsun.",
    },
    "c.urun.1": {
        "text": "Nişini seç",
        "done": "Nişini seçtin ve o nişteki aktif reklamları taradın.",
        "why": "Niş; ürün araştırmanı, reklam kitleni ve mağaza tasarımını belirler.",
        "options": [
            {
                "key": "pet",
                "title": "Evcil hayvan",
                "lines": [
                    "2026 raporlarında en tutarlı önerilen niş; tekrar eden alım",
                    "Kişiselleştirilmiş aksesuar ve akıllı pet ürünleri marjı yükseltir",
                ],
            },
            {
                "key": "ev",
                "title": "Ev düzeni ve dekor",
                "lines": [
                    "Düzenleyici, mum, duvar dekoru gibi hafif ürünler; kısa videoda iyi görünür",
                    "Büyük mobilyadan kaçın: kargo ve iade pahalı",
                ],
            },
            {
                "key": "saglik",
                "title": "Sağlık ve wellness aksesuarı",
                "lines": [
                    "Masaj/toparlanma aletleri, uyku ürünleri, fitness aksesuarları büyüyor",
                    "Dikkat: sağlık iddiaları reklam platformlarında ve yasal olarak denetlenir",
                ],
            },
            {
                "key": "outdoor",
                "title": "Outdoor ve seyahat",
                "lines": [
                    "Valiz düzenleyici, kamp ekipmanı, seyahat aksesuarı",
                    "Sezonluk dalgalanma olabilir; yaz öncesi güçlü",
                ],
            },
            {
                "key": "eko",
                "title": "Çevre dostu ürünler",
                "lines": [
                    "Yeniden kullanılabilir ev ürünleri, bambu ürünler",
                    "Bilinçli tüketici daha yüksek fiyat ödemeye hazır",
                ],
            },
        ],
        "how": [
            "Seçtiğin nişte Meta Ad Library'de (facebook.com/ads/library) hedef ülkeni seçip ara; aynı ürün için çok sayıda aktif reklam varsa o ürün para kazandırıyor demektir.",
            "TikTok Creative Center'da Top Ads ve trend ürünlere bak.",
        ],
        "warn": "Niş listeleri yön gösterir; satın almadan önce Google Trends ve aktif reklamlarla talebi kendi pazarında doğrula.",
    },
    "c.urun.2": {
        "text": "{secim:c.urun.1|Nişinde} 20 aday ürün listesi çıkar",
        "done": "20 adaylık listen hazır.",
    },
    "c.urun.3": {"done": "Her adayın skoru yazılı; 70 altı elendi."},
    "c.urun.4": {
        "why": "Reklamla satışta başa baş CPA'sı düşük ürün zarar ettirir.",
        "done": "En iyi 3-5 ürünün başa baş CPA'sı ve fiyat çarpanı belli.",
    },
    "c.urun.5": {"done": "Rakiplerden 3 güçlü ve 3 zayıf yön not ettin."},
    "c.tedarik.1": {
        "text": "Tedarikçi platformunu seç",
        "done": "En iyi 3 ürünün fiyat ve teslim süreleri not edildi.",
        "why": "Kargo süresi ve ürün kalitesi iade, şikayet ve chargeback oranını doğrudan belirler.",
        "options": [
            {
                "key": "cj",
                "title": "CJ Dropshipping",
                "lines": [
                    "Aylık ücret yok; ürün, kargo ve isteğe bağlı hizmetler için ödersin",
                    "ABD depoları var; Çin hattında 7-15 gün sürebilir, ABD deposundaki ürünleri seç",
                    "Uygun: en düşük maliyetle başlamak isteyenler",
                ],
            },
            {
                "key": "spocket",
                "title": "Spocket",
                "lines": [
                    "ABD/AB tedarikçileri; yurt içi teslim yaklaşık 2-6 gün (en hızlı)",
                    "Aylık yaklaşık 40-60 $; katalog daha dar",
                    "Uygun: hızlı kargoyla güven kazanmak isteyenler",
                ],
            },
            {
                "key": "zendrop",
                "title": "Zendrop",
                "lines": [
                    "Ücretsiz plan (sipariş başı ücretli) veya aylık yaklaşık 49-79 $",
                    "ABD stoklu ürünlerde 5-8 gün; her ürün ABD'de stoklu değil",
                ],
            },
            {
                "key": "dsers",
                "title": "DSers (AliExpress)",
                "lines": [
                    "Ücretsiz planda 3.000 ürüne kadar; AliExpress siparişlerini otomatikleştirir",
                    "Kendi deposu yok; kargo süresi AliExpress satıcısına bağlı, daha yavaş",
                ],
            },
        ],
        "how": [
            "Seçtiğin platformda en iyi 3 ürünün için ürün + hedef ülkeye kargo fiyatı ve teslim süresini not et.",
            "Ürünü en az 2 kaynaktan karşılaştır.",
        ],
        "warn": "Fiyatlar ve süreler kaynaklara göre değişiyor; platformun kendi sitesinden güncelini kontrol et.",
    },
    "c.tedarik.2": {
        "why": "DDP değilse müşteri kapıda vergi öder; iade ve chargeback patlar.",
        "done": "DDP olduğunu ya da gümrük oranını yazılı olarak aldın.",
    },
    "c.tedarik.3": {"done": "Test siparişi geldi; kalite ve süre kabul edilebilir."},
    "c.tedarik.4": {"done": "Test paketinde fiyat, fatura veya logo yoktu."},
    "c.tedarik.5": {"done": "Ölçekleme için ajan veya depo seçeneğin belli."},
    "c.magaza.1": {"done": "Shopify hesabın açık."},
    "c.magaza.2": {"done": "Alan adın bağlı ve destek e-postan çalışıyor."},
    "c.magaza.3": {"done": "Tema, logo ve renkler hazır; mobilde kontrol ettin."},
    "c.magaza.4": {
        "why": "Ödeme sağlayıcıları ve reklam platformları bu sayfalar olmadan hesabı onaylamaz.",
        "done": "6 sayfa da yayında ve alt menüde linkli.",
    },
    "c.magaza.5": {"done": "Ana ürün sayfan video, fayda maddeleri ve SSS ile hazır."},
    "c.magaza.6": {
        "text": "{secim:c.tedarik.1|Tedarikçi} uygulamasını bağla ve ürünü içe aktar",
        "done": "Ürün mağazada, varyantlar tedarikçiyle eşleşik.",
    },
    "c.magaza.7": {"done": "Fiyat ve paket teklifi Kâr Hesabı'na göre ayarlı."},
    "c.magaza.8": {"done": "Test siparişi uçtan uca sorunsuz geçti."},
    "c.reklam.1": {
        "why": "Pixel ve Conversions API olmadan Meta kimin satın aldığını öğrenemez; reklam optimize olmaz.",
        "done": "Events Manager'da Purchase olayı görünüyor.",
    },
    "c.reklam.2": {"done": "TikTok Pixel bağlı (veya bu adımı bilinçli olarak atladın)."},
    "c.reklam.3": {
        "why": "Reklamda kazanan çoğu zaman üründen çok ilk 3 saniyedir.",
        "done": "3-5 farklı hook ile başlayan videon hazır.",
    },
    "c.reklam.4": {"done": "Başa baş CPA ve ROAS değerlerin not edildi."},
    "c.reklam.5": {"done": "Test kampanyan yayında."},
    "c.reklam.6": {"done": "Bir hafta boyunca her gün karar verdin."},
    "c.operasyon.1": {"done": "Siparişler tedarikçiye otomatik gidiyor."},
    "c.operasyon.2": {"done": "Takip numaraları otomatik geçiyor, takip sayfası yayında."},
    "c.operasyon.3": {"done": "En az 4 hazır cevap şablonun var."},
    "c.operasyon.4": {"done": "Hasar/kayıp durumunda ne yapılacağı tedarikçiyle yazılı."},
    "c.operasyon.5": {
        "why": "Yüksek chargeback oranı ödeme hesabının kapanmasına yol açabilir.",
        "done": "Dispute kontrolü haftalık rutininde.",
    },
    "c.olcek.1": {"done": "Bütçe kademeli arttı, CPA başa başın altında kaldı."},
    "c.olcek.2": {"done": "En az bir yeni kreatif, ülke veya kanal test edildi."},
    "c.olcek.3": {"done": "Paket veya upsell teklifi yayında."},
    "c.olcek.4": {"done": "Sepet terk ve satın alma sonrası akışları çalışıyor."},
    "c.olcek.5": {"done": "Kazanan ürün hedef ülke deposundan gönderiliyor."},
    "c.olcek.6": {"done": "Markalı ambalaj veya private label için tedarikçiyle anlaştın."},
}

STAGES = enrich(_BASE, EXTRA)
