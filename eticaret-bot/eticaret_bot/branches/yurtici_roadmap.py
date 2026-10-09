"""🅰️ Yurt içi XML dropshipping: sıfırdan ilk satışa kadar adım adım kurs.

Akış: Türk tedarikçi (XML bayilik) → entegrasyon yazılımı → Trendyol mağazası.
Yasal ve vergisel adımlar genel bilgilendirmedir; kesin karar için mali müşavir görüşü alınmalı.
Panel menü adları zamanla değişebilir; talimatlar bunu belirterek yazıldı.
"""

from __future__ import annotations

from ..core.roadmap import enrich, make_stage

BRANCH_ID = "a"

_BASE = (
    make_stage(
        BRANCH_ID,
        "hazirlik",
        "1️⃣ Hazırlık",
        "Kanal belli: Trendyol. Bu aşamada ne satacağına ve ne kadar harcayacağına karar veriyorsun.",
        [
            {
                "text": "Satacağın kategoriyi seç",
                "why": "Tedarikçini, entegrasyonunu ve reklamını bu karara göre seçeceksin; tek kategoriyle başlamak işi yönetilebilir kılar.",
                "how": [
                    "Yukarıdaki seçenekleri karşılaştır; kararsızsan mutfak gereçleri veya evcil hayvan ile başla.",
                    "İstersen seçmeden önce trendyol.com'da o kategoride 'En çok satan' sıralamasına bakıp birkaç ürünü not al.",
                ],
                "warn": "Tek bir ürüne değil, bir kategoriye karar veriyorsun; ürünleri daha sonra tedarikçinin listesinden seçeceksin.",
            },
            {
                "text": "Bütçeni ve zamanını planla",
                "why": "Hangi masrafın ne zaman geleceğini bilirsen yarı yolda kalmazsın.",
                "how": [
                    "Bir not aç ve kalemleri yaz: mali müşavir (aylık), şirket açılış masrafları (noter imza beyannamesi, damga vergisi vb.), KEP (yıllık), e-arşiv fatura hizmeti, entegrasyon yazılımı (aylık), numune ürünler, ilk reklam bütçesi.",
                    "Her kalem için 2-3 yerden fiyat al; açılış masraflarının toplamını müşavire soracaksın.",
                    "Şahıs şirketi açınca her ay Bağ-Kur primi ödersin; 1 Ocak 2026'dan itibaren genç girişimci prim desteği kalktı, bunu bütçeye ekle.",
                    "Haftada kaç saat ayırabileceğini yaz; ilk ay için haftada en az 10 saat ayırman gerekir.",
                ],
                "warn": "İlk 2-3 ay kâr bekleme; bu parayı öğrenme maliyeti olarak gör.",
                "done": "Toplam başlangıç bütçen ve aylık sabit giderin yazılı.",
            },
        ],
    ),
    make_stage(
        BRANCH_ID,
        "sirket",
        "2️⃣ Şirketini Kur",
        "Trendyol bireysel hesapla satışa izin vermez; vergi levhası olan bir şirket gerekir. Başlangıç için şahıs şirketi yeterli.",
        [
            {
                "text": "Mali müşavir bul ve anlaş",
                "why": "Şirket açılışı, beyannameler ve Bağ-Kur kaydını müşavir yapar; vergi hatası yapmamanın en kısa yolu.",
                "how": [
                    "Tanıdıklarından tavsiye iste veya Google'da 'e-ticaret mali müşavir' + şehrin diye ara; online muhasebe firmaları da seçenek.",
                    "En az 3 müşavire aşağıdaki mesajı gönder ve teklif al.",
                    "29 yaşını doldurmadıysan genç girişimci gelir vergisi istisnasını sor (şahıs şirketlerinde, 3 yıl).",
                    "Ücreti ve hizmeti en uygun olanla sözleşme imzala; açılış için gereken belge listesini iste.",
                ],
                "template": (
                    "Merhaba, Trendyol üzerinden dropshipping ile satış yapmak için şahıs şirketi açmak istiyorum. "
                    "Şirket açılışı ve aylık muhasebe ücretinizi, açılışta ödenecek diğer masrafları ve gerekli belgeleri "
                    "öğrenebilir miyim? E-ticaret / pazaryeri müşterileriniz var mı? Teşekkürler."
                ),
                "done": "Bir müşavirle anlaştın ve açılış için belge listesini aldın.",
            },
            {
                "text": "Şirket türünü seç, şirketini aç ve vergi levhanı al",
                "why": "Vergi levhası olmadan Trendyol başvurusu yapılamaz ve fatura kesilemez.",
                "how": [
                    "İşe başlama bildirimi e-Devlet şifrenle Dijital Vergi Dairesi (dijital.gib.gov.tr) üzerinden yapılır; genelde bunu müşavirin yapar.",
                    "Faaliyet kodu olarak internet üzerinden perakende satışı (e-ticaret) seçin; doğru kodu müşavirinle netleştir.",
                    "İş yeri adresi olarak ev adresini kullanabilirsin (kira sözleşmesi veya tapu istenebilir) ya da sanal ofis kiralayabilirsin.",
                    "Vergi dairesi adresine yoklamaya gelebilir; o gün adreste ol.",
                    "Kimliğinle notere gidip imza beyannamesi çıkar.",
                    "Bağ-Kur kaydı işe başlamayla otomatik açılır; e-Tebligat adresin tanımlanır.",
                ],
                "done": "Vergi levhanın PDF'i elinde ve vergi numaran belli.",
            },
            {
                "text": "e-Arşiv fatura altyapısını kur",
                "why": "Trendyol'daki her satışa fatura kesmek zorundasın.",
                "how": [
                    "Müşavirinle fatura yöntemini seç: GİB'in ücretsiz portalında her faturayı elle kesersin, az siparişte yeterli olur.",
                    "Bir özel e-fatura/e-arşiv sağlayıcısı seçersen faturalar entegrasyon yazılımından otomatik kesilir; dropshipping'de önerilen bu.",
                    "Seçeceğin entegrasyon yazılımının hangi fatura sağlayıcılarıyla çalıştığını önceden sor.",
                    "Bir test faturası kes; unvan, vergi numarası ve adresin doğru görünüyor mu kontrol et.",
                ],
                "done": "Fatura kesebiliyorsun (test faturası başarılı).",
            },
            {
                "text": "KEP adresi al",
                "why": "Şahıs şirketleri için yasal zorunluluk olmasa da pazaryeri başvurularında fiilen isteniyor.",
                "how": [
                    "BTK yetkili bir KEP sağlayıcısı seç: PTT KEP en bilineni, özel sağlayıcıların fiyatları farklı.",
                    "Sağlayıcının sitesinden online ön başvuru yap; kimlik ve vergi bilgilerin istenir.",
                    "E-imzan yoksa sözleşmeyi ıslak imzayla tamamlamak için şubeye gitmen gerekebilir.",
                    "Yıllık abonelik ücretini öde ve aktif olan KEP adresini not et.",
                ],
                "done": "Aktif bir KEP adresin var.",
            },
            {
                "text": "Şirket adına banka hesabı aç",
                "why": "Trendyol satış paranı (hakedişi) şirket adına açılmış IBAN'a yatırır.",
                "how": [
                    "Vergi levhan ve kimliğinle bankaya git veya mobil uygulamadan ticari hesap başvurusu yap.",
                    "Ticari vadesiz TL hesabı aç ve IBAN'ını al.",
                    "Hesap unvanının vergi levhasındaki unvanla birebir aynı olduğunu kontrol et.",
                    "Entegrasyon yazılımı ve reklam ödemeleri için şirket kartı (sanal kart olabilir) al.",
                ],
                "warn": "Kişisel hesabınla şirket parasını karıştırma; tüm alış ve satışlar şirket hesabından geçsin.",
                "done": "Şirket adına IBAN'ın var ve unvan vergi levhasıyla aynı.",
            },
        ],
    ),
    make_stage(
        BRANCH_ID,
        "tedarik",
        "3️⃣ Tedarikçini Bul",
        "XML bayilikte tedarikçi ürün, fiyat ve stok listesini bir XML linkiyle verir; sipariş gelince ürünü müşterine o gönderir.",
        [
            {
                "text": "{secim:a.hazirlik.1|Kategorin} için XML veren tedarikçileri listele",
                "how": [
                    "Google'da şu aramaları yap: '{secim:a.hazirlik.1|<kategori>} xml bayilik', '{secim:a.hazirlik.1|<kategori>} dropshipping tedarikçi', '{secim:a.hazirlik.1|<kategori>} toptan xml'.",
                    "XML bayilik platformlarına ve büyük toptancı sitelerine bak; 'bayi ol' veya 'XML bayilik' sayfalarını bul.",
                    "Trendyol'da kategorindeki ürünlere bak: aynı ürünü aynı görselle çok satıcı satıyorsa arkasında ortak bir tedarikçi vardır; ürün adını Google'da aratarak ona ulaşabilirsin.",
                    "Her aday için not al: site, ürün sayısı, bayilik ücreti, iletişim bilgisi.",
                ],
                "warn": "Yüksek peşin üyelik ücreti isteyen veya kargo süresi ve stok güncellemesi hakkında net cevap vermeyen tedarikçiden uzak dur.",
                "done": "En az 3 aday tedarikçi listende.",
            },
            {
                "text": "Tedarikçilere şartları sor",
                "why": "Dropshipping'de mağaza puanını tedarikçinin hızı ve stok doğruluğu belirler.",
                "how": [
                    "Aşağıdaki mesajı her adaya WhatsApp veya e-posta ile gönder.",
                    "Cevapları bir tabloya yaz ve yan yana karşılaştır.",
                    "Kırmızı bayraklar: stok günde bir güncelleniyorsa, sipariş 48 saatten geç kargoya veriliyorsa, pakete kendi faturasını koyuyorsa, iade süreci belirsizse.",
                ],
                "template": (
                    "Merhaba, Trendyol'da satış yapan bir şahıs şirketiyim; XML bayiliğiniz hakkında bilgi almak istiyorum:\n"
                    "1. Bayilik ücreti veya minimum alım şartı var mı?\n"
                    "2. XML'de stok ve fiyat ne sıklıkla güncelleniyor?\n"
                    "3. Sipariş kaç saat içinde kargoya veriliyor, hangi kargo firmasıyla?\n"
                    "4. Pakete sizin faturanız veya fiyat etiketiniz giriyor mu? İsimsiz paketleme yapıyor musunuz?\n"
                    "5. Siparişleri entegrasyon yazılımı üzerinden otomatik alabiliyor musunuz? Hangi yazılımlarla çalışıyorsunuz?\n"
                    "6. İade gelen ürün nasıl işleniyor, bedel kaç günde iade ediliyor?\n"
                    "7. Faturanızı bana nasıl kesiyorsunuz?"
                ),
                "done": "En az 2 tedarikçiden yazılı cevap aldın.",
            },
            {
                "text": "Numune sipariş et",
                "how": [
                    "Satmayı düşündüğün 2-3 ürünü kendi adresine sipariş et.",
                    "Not al: sipariş kaç saatte kargoya verildi, kaç günde geldi?",
                    "Paketi aç: ürün kalitesi nasıl, içinde tedarikçinin broşürü veya faturası var mı?",
                    "Ürünü fotoğrafla ve kısa video çek; listelemede ve reklamda kullanacaksın.",
                ],
                "done": "Numuneler geldi; kalite ve kargo süresi seni tatmin etti.",
            },
            {
                "text": "Tedarikçini seç ve XML linkini al",
                "how": [
                    "Stok güncelleme, kargo hızı ve numune kalitesi en iyi olanı ana tedarikçi yap.",
                    "Bayilik başvurusunu tamamla: vergi levhası ve şirket bilgilerin istenir.",
                    "Bayi panelinden XML linkini al ve güvenli bir yere kaydet.",
                    "İkinci en iyi tedarikçiyi yedek olarak not et.",
                ],
                "done": "Bayi hesabın açık ve XML linkin elinde.",
            },
        ],
    ),
    make_stage(
        BRANCH_ID,
        "magaza",
        "4️⃣ Trendyol Mağazanı Aç",
        "Mağaza açmak ücretsiz; başvuru online yapılır, eksiksiz belgelerle onay genelde birkaç iş günü sürer.",
        [
            {
                "text": "Satıcı başvuru formunu doldur",
                "how": [
                    "partner.trendyol.com adresine gir ve satıcı başvuru formunu aç.",
                    "Şirket türü olarak şahıs şirketini seç; vergi numaranı, vergi daireni ve unvanını vergi levhasında yazdığı gibi gir.",
                    "KEP adresini, şirket IBAN'ını, telefonunu ve e-postanı yaz.",
                    "Satış yapacağın kategoriyi seç.",
                    "E-posta ve telefon doğrulamasını tamamla.",
                ],
                "warn": "Unvan, IBAN hesap adı ve vergi levhası birebir aynı olmalı; başvurunun en sık reddedilme sebebi bu.",
                "done": "Başvurun gönderildi.",
            },
            {
                "text": "Belgeleri yükle ve sözleşmeyi imzala",
                "how": [
                    "İstenen belgeleri hazırla: vergi levhası, kimlik, imza beyannamesi ve şirket adına IBAN.",
                    "Satıcı sözleşmesini ekrandaki talimata göre imzala ve yükle; şartlar zamanla değişebiliyor.",
                    "Onay e-postasını bekle; eksik belge e-postası gelirse aynı gün tamamla.",
                ],
                "done": "Mağazan onaylandı ve satıcı paneline giriş yapabiliyorsun.",
            },
            {
                "text": "Mağaza ayarlarını yap",
                "how": [
                    "Mağaza adını ve logonu ekle: kısa, akılda kalıcı ve kategorinle uyumlu olsun.",
                    "Sevkiyat ve iade adreslerini gir; iade adresini tedarikçinle konuştuğun şekilde ayarla.",
                    "Kargo ayarlarında Trendyol'un anlaşmalı kargo seçeneklerini ve desi fiyatlarını incele; tedarikçinin kullandığı firmayla uyumlu olanı seç.",
                    "Fatura ayarlarında e-arşiv sağlayıcını bağla.",
                    "Sağ üstte mağaza adına tıkla → Hesap Bilgilerim → Entegrasyon Bilgileri: Satıcı ID, API Key ve API Secret buradadır, bir sonraki aşamada lazım olacak.",
                ],
                "warn": "Menü adları zamanla değişebilir; bulamazsan panelin arama kutusunu veya yardım merkezini kullan.",
                "done": "Mağaza adı, logo, adresler, kargo ve fatura ayarları tamam.",
            },
        ],
    ),
    make_stage(
        BRANCH_ID,
        "entegrasyon",
        "5️⃣ Tedarikçini Mağazana Bağla",
        "Trendyol XML dosyasını doğrudan kabul etmez; entegrasyon yazılımı tedarikçinin XML'ini okuyup ürünleri, stokları ve fiyatları mağazana taşır.",
        [
            {
                "text": "Entegrasyon yazılımı seç",
                "how": [
                    "Google'da 'XML Trendyol entegrasyonu' diye ara ve 3 yazılımın sitesine bak.",
                    "Tedarikçine 'hangi entegrasyon yazılımıyla çalışan bayileriniz var?' diye sor; uyumlu olanı öne al.",
                    "Her yazılıma sor: tedarikçimin XML'ini destekliyor mu, stok ve fiyat kaç dakikada bir güncelleniyor, siparişleri tedarikçiye otomatik iletiyor mu, fatura sağlayıcımla çalışıyor mu, aylık ücret ve ürün limiti ne?",
                    "Deneme süresi olanla başla.",
                ],
                "done": "Bir entegrasyon yazılımında hesabın var.",
            },
            {
                "text": "Trendyol'u yazılıma bağla",
                "how": [
                    "Trendyol panelinde sağ üstte mağaza adına tıkla → Hesap Bilgilerim → Entegrasyon Bilgileri.",
                    "Satıcı ID, API Key ve API Secret'ı kopyala (bunları sadece yönetici hesabı görür).",
                    "Entegrasyon yazılımında Trendyol bağlantısı bölümüne bu 3 bilgiyi yapıştır, kaydet ve bağlantıyı test et.",
                ],
                "warn": "API Key ve Secret şifre gibidir; kimseyle mesajla paylaşma, ekran görüntüsünü gönderme.",
                "done": "Yazılım Trendyol'un bağlı olduğunu gösteriyor.",
            },
            {
                "text": "XML'i ekle ve fiyat kuralını kur",
                "how": [
                    "Yazılımın tedarikçi/XML ekleme bölümüne tedarikçinin XML linkini yapıştır ve ürünlerin çekildiğini gör.",
                    "💰 Kâr Hesabı ile 3 örnek ürün hesapla: tedarikçi fiyatı, komisyon, kargo ve KDV'ye göre hangi fiyatta kâr ediyorsun?",
                    "Bu hesaba göre yazılımda fiyat kuralı kur (ör. bayi fiyatına yüzde ve sabit tutar ekleyerek).",
                    "Kategorilere göre komisyon farklıysa kategori bazında ayrı kural kur.",
                ],
                "done": "Ürünler yazılımda görünüyor ve satış fiyatları kâr bırakıyor.",
            },
            {
                "text": "Kategori ve özellikleri eşleştir",
                "how": [
                    "Tedarikçinin her kategorisini Trendyol'daki karşılığıyla eşleştir.",
                    "Zorunlu özellikleri doldur: marka, renk, materyal, ölçü vb.; eksik özellikli ürün onaylanmaz.",
                    "Ürünlerin markası Trendyol'da kayıtlı değilse nasıl gönderileceğini yazılımın destek ekibine sor.",
                    "Renk ve beden varyantlarının tek ürün altında toplandığını kontrol et.",
                ],
                "done": "Seçtiğin ürünlerin tüm zorunlu alanları dolu.",
            },
            {
                "text": "İlk 20-50 ürünü yayına al",
                "how": [
                    "Tüm kataloğu değil, kategorinin en iyi 20-50 ürününü seç (numunesini gördüklerin dahil).",
                    "Yazılımdan Trendyol'a gönder.",
                    "Trendyol panelinde ürünlerin onay durumunu takip et; reddedilenlerin sebebini oku ve düzelt.",
                    "Bir ürünün stoğu tedarikçide değişince birkaç saat içinde Trendyol'da da değiştiğini kontrol et.",
                ],
                "warn": "Binlerce ürünü birden yükleme; hatalar çoğalır ve kontrol edemezsin.",
                "done": "Ürünlerin Trendyol'da satışta ve stok senkronu çalışıyor.",
            },
        ],
    ),
    make_stage(
        BRANCH_ID,
        "listeleme",
        "6️⃣ Ürünlerini Satılabilir Yap",
        "Aynı XML'i birçok satıcı kullanır; farkı başlık, görsel ve doğru fiyat yaratır.",
        [
            {
                "text": "Başlıkları düzenle",
                "how": [
                    "Formatı kullan: Marka + Ürün adı + Ana özellik + Varyant.",
                    "Trendyol arama çubuğuna ürünün adını yaz; çıkan önerilerdeki kelimeleri başlığa ekle.",
                    "Örnek: 'Paslanmaz Çelik Sebze Doğrayıcı 5 Bıçaklı Mutfak Rendesi Yeşil'.",
                    "Tedarikçinin hazır başlığını aynen kullanma; aynı başlıklı yüzlerce ürün arasında kaybolursun.",
                ],
                "done": "İlk 20 ürününün başlığı düzenlendi.",
            },
            {
                "text": "Görsel ve açıklamaları güçlendir",
                "how": [
                    "İlk görsel beyaz fonda ve net olsun; numunede çektiğin gerçek fotoğrafları ekle.",
                    "Ölçüleri gösteren bir görsel ekle; iade sebeplerinin başında 'beklediğimden küçük/büyük' gelir.",
                    "Açıklamaya fayda, ölçü, malzeme, kullanım ve paket içeriğini net yaz.",
                    "Müşterinin soracağı soruları açıklamada önceden cevapla.",
                ],
                "done": "En iyi 10 ürününün görsel ve açıklaması güncel.",
            },
            {
                "text": "Fiyatlarını rakiplere göre kontrol et",
                "how": [
                    "Her ana ürünü Trendyol'da arat; aynı ürünü satan diğer satıcıların fiyatına bak.",
                    "💰 Kâr Hesabı ile rakip fiyatından satarsan ne kadar kâr kaldığını hesapla.",
                    "Zarar ettiren ürünleri yayından kaldır; fiyatı kâr bırakan ürünlere odaklan.",
                ],
                "done": "Yayındaki her ürün kâr bırakan bir fiyatta.",
            },
        ],
    ),
    make_stage(
        BRANCH_ID,
        "ilksatis",
        "7️⃣ İlk Satışını Al",
        "Trendyol hizmet puanı; zamanında kargo, iptal ve iade oranına bakar. Puan düşerse ürünlerin aramada geriye düşer.",
        [
            {
                "text": "Ürünlerini görünür yap",
                "how": [
                    "Satıcı panelindeki reklam bölümünden en iyi 3-5 ürünün için ürün reklamı aç; günlük küçük bir bütçeyle başla.",
                    "Panelde sunulan kampanyaları 💰 Kâr Hesabı ile hesapla; sadece kâr bırakanlara katıl.",
                    "Ürün linklerini kendi sosyal medya hesaplarında paylaş.",
                    "Reklam harcamasını ve gelen satışları her gün not et; satış başı reklam maliyetini Kâr Hesabı'na gir.",
                ],
                "warn": "Kendine veya tanıdıklarına sipariş verdirip yorum yaptırmak Trendyol kurallarına aykırıdır; mağazan kapatılabilir.",
                "done": "Reklamın açık ve ürünlerin görüntülenme alıyor.",
            },
            {
                "text": "İlk siparişi uçtan uca işle",
                "how": [
                    "Sipariş gelince hem Trendyol panelinde hem entegrasyon yazılımında gördüğünü doğrula.",
                    "Siparişin tedarikçiye iletildiğini kontrol et; otomatik gitmediyse tedarikçinin bayi panelinden elle gir.",
                    "Faturanın kesilip Trendyol'a yüklendiğini kontrol et.",
                    "Kargo takip numarasının Trendyol'a geçtiğini ve siparişin zamanında kargoya verildiğini takip et.",
                    "Teslimattan sonra müşteriden gelen soru veya sorun varsa hemen çöz.",
                ],
                "done": "İlk siparişin müşteriye teslim edildi. 🎉",
            },
            {
                "text": "Günlük kontrol rutinini başlat",
                "how": [
                    "Her sabah 15 dakika ayır.",
                    "Kontrol et: yeni siparişler, henüz kargoya verilmeyenler, müşteri soruları, iade talepleri.",
                    "Müşteri sorularını 24 saat içinde cevapla.",
                    "Tedarikçide tükenmiş ama mağazanda satışta görünen ürün var mı bak; iptal, puanını en çok düşüren şeydir.",
                ],
                "done": "Bir hafta boyunca her gün kontrol yaptın.",
            },
            {
                "text": "İadeleri doğru yönet",
                "how": [
                    "İade talebi gelince ürünün tedarikçiye mi sana mı döneceğini kontrol et.",
                    "Ürün tedarikçiye ulaşınca bedel iadesini takip et.",
                    "İade sebeplerini not al; aynı sebeple çok iade alan ürünü kaldır veya açıklamasını düzelt.",
                ],
                "done": "İade süreci tedarikçinle sorunsuz işliyor.",
            },
        ],
    ),
    make_stage(
        BRANCH_ID,
        "buyume",
        "8️⃣ Büyüt",
        "Satan ürünü bul, ona yüklen; satmayanı temizle.",
        [
            {
                "text": "Haftalık raporunu çıkar",
                "how": [
                    "Her hafta not et: sipariş sayısı, ciro, iade sayısı, reklam harcaması.",
                    "En çok satan 5 ürünün net kârını 💰 Kâr Hesabı ile kontrol et.",
                    "Reklam harcaması kârdan fazlaysa o reklamı kapat.",
                ],
                "done": "İlk haftalık raporun yazılı.",
            },
            {
                "text": "Satanı çoğalt, satmayanı temizle",
                "how": [
                    "Satan ürünlerin farklı renk, model ve tamamlayıcı ürünlerini tedarikçinin listesinden ekle.",
                    "30 gündür hiç satmayan ürünleri kaldır.",
                    "Satan ürünlerin başlık ve görsellerini daha da iyileştir.",
                ],
                "done": "Ürün listen satış verisine göre güncellendi.",
            },
            {
                "text": "İkinci pazaryerini aç",
                "how": [
                    "Sistem oturunca Hepsiburada veya N11'e aynı belgelerle başvur.",
                    "Entegrasyon yazılımında yeni kanalı ekle; aynı XML ve fiyat kurallarıyla ürünleri gönder.",
                    "Komisyonlar farklı olduğu için fiyat kuralını o kanala göre ayrıca hesapla.",
                ],
                "done": "İkinci pazaryerinde de satıştasın.",
            },
        ],
    ),
)


# ---------- Botun araştırıp sunduğu seçenekler (karar adımları) ----------
# Kaynak: 2026 tarihli pazaryeri/entegratör rehberleri ve firma sayfaları. Komisyon ve fiyatlar
# kaynaklar arasında farklılık gösterdiği için aralık olarak verildi; kullanıcıya teyit ettirilir.

_KOMISYON_NOTU = "Komisyon oranları kaynaklara göre; güncelini satıcı panelinden teyit et."

OPTIONS = {
    "a.hazirlik.1": {
        "options": [
            {
                "key": "mutfak",
                "title": "Mutfak gereçleri",
                "lines": [
                    "Örnek: doğrayıcı, saklama kabı, organizer, pratik mutfak aletleri",
                    "Komisyon: yaklaşık %11-19",
                    "Artı: her evde ihtiyaç, beden derdi yok, video ile kolay anlatılır",
                    "Eksi: cam/porselen kırılma riski taşır; kırılmayan ürünleri seç",
                ],
                "pick": _KOMISYON_NOTU,
            },
            {
                "key": "pet",
                "title": "Evcil hayvan ürünleri",
                "lines": [
                    "Örnek: mama kabı, tasma, oyuncak, tımar ürünleri, kedi kumu aksesuarları",
                    "Komisyon: yaklaşık %15-18",
                    "Artı: tekrar eden alım, sadık müşteri; XML veren pet tedarikçileri mevcut",
                    "Eksi: mama gibi ağır ürünlerde kargo maliyeti yüksek",
                ],
                "pick": _KOMISYON_NOTU,
            },
            {
                "key": "evduzen",
                "title": "Ev düzenleme ve dekorasyon",
                "lines": [
                    "Örnek: düzenleyici kutular, askılar, dekoratif objeler, mum, duvar dekoru",
                    "Komisyon: Ev ve Yaşam altında yaklaşık %11-22",
                    "Artı: geniş ürün yelpazesi, hafif ürünler, görselle iyi satılır",
                    "Eksi: rekabet yüksek; başlık ve görselle fark yaratman gerekir",
                ],
                "pick": _KOMISYON_NOTU,
            },
            {
                "key": "oto",
                "title": "Oto aksesuar",
                "lines": [
                    "Örnek: araç içi düzenleyici, telefon tutucu, temizlik ürünleri, koltuk aksesuarı",
                    "Komisyon: yaklaşık %16,5",
                    "Artı: dayanıklı, küçük ürünler; iade oranı genelde düşük",
                    "Eksi: araç modeline özel ürünlerde uyumsuzluk iadesi olabilir",
                ],
                "pick": _KOMISYON_NOTU,
            },
            {
                "key": "telefon",
                "title": "Telefon aksesuarı",
                "lines": [
                    "Örnek: kılıf, ekran koruyucu, şarj kablosu, araç tutucu",
                    "Komisyon: alt kategoriye göre %15-27 (geniş aralık)",
                    "Artı: yüksek arama hacmi, hafif ve ucuz kargo",
                    "Eksi: fiyat rekabeti sert; model uyumsuzluğu iadesi çok",
                ],
                "pick": _KOMISYON_NOTU,
            },
        ]
    },
    "a.hazirlik.2": {
        "options": [
            {
                "key": "ekonomik",
                "title": "Ekonomik başlangıç",
                "lines": [
                    "Fatura: GİB'in ücretsiz e-arşiv portalı (faturaları elle kesersin)",
                    "Entegrasyon: XML bayilik odaklı uygun fiyatlı bir araç",
                    "Reklam: ilk ay yok, sadece ürün kalitesi ve fiyatla",
                    "Uygun: günde birkaç siparişe kadar; zamanın bol, bütçen kısıtlı",
                ],
                "pick": "Sonraki adımlarda bu kombinasyona uygun seçenekleri öne çıkaracağım.",
            },
            {
                "key": "dengeli",
                "title": "Dengeli (önerilen)",
                "lines": [
                    "Fatura: özel e-arşiv sağlayıcısı (faturalar otomatik kesilir)",
                    "Entegrasyon: XML destekli, sipariş aktaran bir yazılım",
                    "Reklam: en iyi 3-5 ürüne küçük günlük bütçe",
                    "Uygun: çoğu yeni başlayan için doğru denge",
                ],
                "pick": "Sonraki adımlarda bu kombinasyona uygun seçenekleri öne çıkaracağım.",
            },
            {
                "key": "hizli",
                "title": "Hızlı büyüme",
                "lines": [
                    "Fatura: özel e-arşiv sağlayıcısı + muhasebe programı",
                    "Entegrasyon: çok kanallı, kapsamlı entegrasyon yazılımı",
                    "Reklam: düzenli reklam bütçesi, ikinci pazaryerine erken geçiş",
                    "Uygun: bütçesi olan ve haftada 20+ saat ayırabilenler",
                ],
                "pick": "Sonraki adımlarda bu kombinasyona uygun seçenekleri öne çıkaracağım.",
            },
        ]
    },
    "a.sirket.1": {
        "options": [
            {
                "key": "yerel",
                "title": "Yerel mali müşavir",
                "lines": [
                    "Artı: yüz yüze görüşme, belgeleri elden teslim, kişisel takip",
                    "Eksi: e-ticaret deneyimi olmayabilir; mutlaka sor",
                ],
                "pick": "Aşağıdaki hazır mesajı birkaç müşavire gönder ve teklifleri karşılaştır.",
            },
            {
                "key": "online",
                "title": "Online muhasebe / müşavirlik hizmeti",
                "lines": [
                    "Artı: şirket açılışı genelde online, e-ticaret müşterisi çok, fiyatlar şeffaf",
                    "Eksi: daha az kişisel; paket dışı işler ek ücretli olabilir",
                ],
                "pick": "Aşağıdaki hazır mesajı birkaç firmaya gönder ve paket içeriklerini karşılaştır.",
            },
        ]
    },
    "a.sirket.2": {
        "options": [
            {
                "key": "sahis",
                "title": "Şahıs şirketi (önerilen)",
                "lines": [
                    "Kuruluşu hızlı ve ucuz; Trendyol başvurusu için yeterli",
                    "29 yaş altıysan genç girişimci gelir vergisi istisnası sadece şahıs şirketinde var",
                    "Eksi: borçlardan şahsen sorumlusun; ciro büyüyünce limitede geçiş konuşulur",
                ],
            },
            {
                "key": "limited",
                "title": "Limited şirket",
                "lines": [
                    "Sorumluluk şirket sermayesiyle sınırlı, kurumsal görünüm",
                    "Eksi: kuruluş ve muhasebe daha pahalı ve uzun; ilk ay için genelde gereksiz",
                ],
            },
        ]
    },
    "a.sirket.3": {
        "options": [
            {
                "key": "gib",
                "title": "GİB e-Arşiv Portalı",
                "lines": [
                    "Ücretsiz; GİB'in sitesinden elle fatura kesersin",
                    "Eksi: her siparişte elle işlem; günde birkaç siparişi geçince zorlaşır",
                    "Uygun: ekonomik başlangıç kombinasyonu",
                ],
                "pick": "Satışlar artınca özel sağlayıcıya geçmeyi planla.",
            },
            {
                "key": "ozel",
                "title": "Özel e-arşiv sağlayıcısı",
                "lines": [
                    "Faturalar entegrasyon yazılımından veya pazaryerinden otomatik kesilir",
                    "Örnek sağlayıcılar: Paraşüt, BirFatura, Logo, Uyumsoft, İzibiz",
                    "Ücretlendirme: kontör veya abonelik; e-ticaret modülü ayrı ücretli olabilir",
                    "Uygun: dengeli ve hızlı büyüme kombinasyonları",
                ],
                "pick": "Seçeceğin entegrasyon yazılımının bu sağlayıcıyla çalıştığını teyit et.",
            },
        ]
    },
    "a.sirket.4": {
        "options": [
            {
                "key": "ptt",
                "title": "PTT KEP",
                "lines": [
                    "En bilinen sağlayıcı; online ön başvuru, gerekirse şubede imza",
                    "Yıllık abonelik ücreti var",
                ],
            },
            {
                "key": "ozel",
                "title": "Özel KEP sağlayıcısı",
                "lines": [
                    "BTK yetkili özel şirketler; fiyatlar sağlayıcıya göre değişir",
                    "Bazıları tamamen online başvuru sunar (e-imza ile)",
                ],
            },
        ]
    },
    "a.tedarik.1": {
        "options": [
            {
                "key": "pet1",
                "title": "Pet tedarikçi adayları",
                "when": "a.hazirlik.1=pet",
                "lines": [
                    "Bir 2025 sonu listesinde XML bayilik veren olarak geçenler: Petibom, Petzztedarik, Hızlımama",
                    "Aktif olup olmadıklarını ve şartlarını sitelerinden kontrol et",
                ],
                "pick": "Şimdi bu adaylara bir sonraki adımdaki hazır mesajı gönder.",
            },
            {
                "key": "ev1",
                "title": "Ev ve yaşam tedarikçi adayları",
                "when": "a.hazirlik.1=evduzen",
                "lines": [
                    "Listelerde ev/yaşam ürünleri için XML verdiği belirtilenler: Evidea (mobilya, ev tekstili, dekorasyon), Turuncix (ev ve yaşam dahil çok kategori)",
                    "Aktif olup olmadıklarını ve şartlarını sitelerinden kontrol et",
                ],
                "pick": "Şimdi bu adaylara bir sonraki adımdaki hazır mesajı gönder.",
            },
            {
                "key": "platform",
                "title": "Çok kategorili XML platformları",
                "lines": [
                    "Birçok toptancının ürününü tek XML'de toplayan platformlar; ürün çeşidi geniş",
                    "Google: 'xml bayilik' ve 'dropshipping xml tedarikçi' aramalarında üst sıralar",
                    "Dikkat: aynı XML'i çok satıcı kullanır; fiyat rekabeti yüksek olur",
                ],
                "pick": "Platformlardan 2-3 tanesine kaydol ve kategorindeki ürün sayısına bak.",
            },
            {
                "key": "uzman",
                "title": "Kategori uzmanı toptancı",
                "lines": [
                    "Sadece senin kategorinde ürün satan toptancı veya ithalatçı",
                    "Bulma yolu: Trendyol'da çok satıcının aynı görselle sattığı ürünün adını Google'da arat",
                    "Artı: daha az rakip, daha iyi fiyat ve stok bilgisi",
                ],
                "pick": "Bulduğun 2-3 toptancıya bir sonraki adımdaki hazır mesajı gönder.",
            },
        ]
    },
    "a.entegrasyon.1": {
        "options": [
            {
                "key": "xmlodak",
                "title": "XML bayilik odaklı uygun fiyatlı araçlar",
                "lines": [
                    "Tedarikçi XML'ini Trendyol'a aktarmaya odaklı; aylık birkaç yüz TL'den başlayan paketler bulunuyor",
                    "Uygun: ekonomik başlangıç kombinasyonu",
                    "Sor: sipariş aktarımı ve fatura entegrasyonu pakete dahil mi?",
                ],
            },
            {
                "key": "entegra",
                "title": "Entegra",
                "lines": [
                    "Karşılaştırmalarda XML desteği öne çıkıyor; çok kanallı",
                    "Bir karşılaştırma sitesine göre yıllık başlangıç yaklaşık 35 bin TL; öğrenme eğrisi yüksek",
                    "Uygun: hızlı büyüme kombinasyonu",
                ],
            },
            {
                "key": "stockmount",
                "title": "StockMount",
                "lines": [
                    "XML + API ile otomatik stok ve fiyat senkronu sunduğu belirtiliyor",
                    "Uygun: dengeli kombinasyon; güncel fiyatı firmadan iste",
                ],
            },
            {
                "key": "dopigo",
                "title": "Dopigo",
                "lines": [
                    "14 gün ücretsiz deneme; sipariş, e-fatura, kargo ve stok senkronu",
                    "Sitesinde XML'den bahsetmiyor; tedarikçi XML'ini destekleyip desteklemediğini sor",
                ],
            },
        ],
        "warn": (
            "Sentos kendi sitesinde dropshipping modeline uygun olmadığını belirtiyor; XML dropshipping için seçme.",
            "Fiyatlar kaynaklar arasında farklı; karar vermeden önce güncel, KDV dahil fiyat iste.",
        ),
    },
}

STAGES = enrich(_BASE, OPTIONS)
