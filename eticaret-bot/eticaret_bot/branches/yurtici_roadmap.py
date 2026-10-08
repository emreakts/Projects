"""🅰️ Yurt içi XML dropshipping yol haritası: Türk tedarikçi (XML bayilik) → Trendyol / Hepsiburada.

Yasal ve vergisel adımlar genel bilgilendirmedir; kesin karar için mali müşavir görüşü alınmalı.
"""

from __future__ import annotations

from ..core.roadmap import make_stage

BRANCH_ID = "a"

STAGES = (
    make_stage(
        BRANCH_ID,
        "plan",
        "1️⃣ Plan",
        "İlk ay hedefin: tek pazaryeri, tek kategori, az sayıda ürünle sistemi çalıştırmak.",
        [
            (
                "Kanalı seç: Trendyol ile başla",
                [
                    "İlk kanal olarak Trendyol'u seç: Türkiye'nin en büyük pazaryerlerinden, mağaza açmak ücretsiz.",
                    "Hepsiburada, N11 gibi kanalları sistem oturduktan sonra ekle; ilk ay tek kanala odaklan.",
                ],
            ),
            (
                "Kategori seç (tek kategori ile başla)",
                [
                    "Trendyol'da ilgini çeken 3 kategoriye bak; çok satanlarda yorum sayısı yüksek ürünleri not et.",
                    "Kargosu kolay, beden derdi olmayan kategorileri tercih et (ör. ev-mutfak, evcil hayvan, hobi, oto aksesuar).",
                    "Komisyon oranı yüksek kategorilerden kaçın; Trendyol satıcı panelinde kategori komisyonlarını kontrol et.",
                    "Tek kategori seç; tedarikçini bu kategoriye göre arayacaksın.",
                ],
            ),
            (
                "Bütçeni yaz",
                [
                    "Şirket kuruluşu ve ilk aylar için mali müşavir ücreti.",
                    "KEP adresi ve e-fatura/e-arşiv hizmet ücreti (yıllık).",
                    "XML entegrasyon yazılımı aylık ücreti.",
                    "Pazaryeri reklamı için küçük bir test bütçesi.",
                    "Toplamı yaz ve bu parayı ilk 3 ayda kâr beklemeden harcayabileceğinden emin ol.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "sirket",
        "2️⃣ Şirket ve Yasal Hazırlık",
        "Trendyol bireysel hesapla satışa izin vermez; vergi levhası olan bir şirket gerekir.",
        [
            (
                "Mali müşavirle görüş ve şahıs şirketi aç",
                [
                    "Bir mali müşavir bul (tanıdık tavsiyesi veya online muhasebe firmaları).",
                    "Faaliyet olarak internetten perakende satış (e-ticaret) kodunu sor.",
                    "Başlangıç için genelde şahıs şirketi yeterli; ciro büyüyünce limited şirket konuşulur.",
                    "Müşavir vergi dairesi kaydını yapar; vergi levhanı al.",
                ],
            ),
            (
                "e-Arşiv / e-Fatura kullanmaya başla",
                [
                    "Her satışa fatura kesmen gerekir; müşavirinle e-arşiv/e-fatura sağlayıcısı seç.",
                    "Seçeceğin entegrasyon yazılımının bu fatura sağlayıcısıyla çalıştığını kontrol et (faturalar otomatik kesilsin).",
                ],
            ),
            (
                "KEP adresi al",
                [
                    "KEP (kayıtlı elektronik posta) adresini PTT veya BTK onaylı bir sağlayıcıdan al.",
                    "Kaynaklar şahıs şirketleri için zorunluluk konusunda çelişiyor; başvuruda takılmamak için baştan almak en güvenlisi.",
                ],
            ),
            (
                "Şirket adına banka hesabı (IBAN) aç",
                [
                    "Hesap unvanı vergi levhasındaki unvanla birebir aynı olmalı; Trendyol hakedişleri bu IBAN'a yatırır.",
                    "Kişisel hesabınla karıştırma; tüm alış-satışlar şirket hesabından geçsin.",
                ],
            ),
            (
                "ETBİS kaydını yap",
                [
                    "Ticaret Bakanlığı'nın E-Ticaret Bilgi Sistemi'ne (ETBİS) kaydın gerekip gerekmediğini müşavirine sor ve gerekiyorsa kaydol.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "tedarik",
        "3️⃣ XML Tedarikçi",
        "XML bayilikte tedarikçi ürün, fiyat ve stok listesini bir XML linkiyle verir; sipariş gelince ürünü müşterine o gönderir.",
        [
            (
                "Kategorinde XML bayilik veren 3 tedarikçi bul",
                [
                    "Google'da '<kategori> xml bayilik' ve '<kategori> dropshipping tedarikçi' diye ara.",
                    "XML bayilik platformlarına ve toptancı sitelerine bak; her biri farklı kategorilerde güçlüdür.",
                    "Trendyol'da kategorindeki satıcılara bak: aynı ürünü çok satıcı aynı görselle satıyorsa ortak bir tedarikçi vardır.",
                    "En az 3 aday tedarikçiyi listele.",
                ],
            ),
            (
                "Tedarikçiye şartları sor ve yazılı al",
                [
                    "Bayi fiyatı ve tavsiye edilen satış fiyatı ne?",
                    "Stok ve fiyat XML'de ne sıklıkla güncelleniyor? (saatlik olmalı; günlük güncelleme iptal riski demek)",
                    "Siparişi kaç saatte kargoya veriyor? (Trendyol hızlı kargo bekler; aynı gün veya 24 saat ideal)",
                    "Pakete kendi faturası veya fiyat etiketi koyuyor mu? (koymamalı)",
                    "İade gelen ürün nereye dönüyor, bedel nasıl iade ediliyor?",
                    "Siparişler entegrasyonla otomatik mi iletiliyor, yoksa elle mi giriyorsun?",
                ],
            ),
            (
                "Numune sipariş et",
                [
                    "En çok satmayı düşündüğün 2-3 ürünü kendi adresine sipariş et.",
                    "Kontrol et: ürün kalitesi, paketleme, kargo süresi, pakette tedarikçiye ait fatura/broşür var mı.",
                    "Ürün fotoğraf ve videolarını çek; listelemede kullanırsın.",
                ],
            ),
            (
                "Ana tedarikçini ve yedeğini seç",
                [
                    "Stok güncelleme sıklığı ve kargo hızı en iyi olanı ana tedarikçi yap.",
                    "Aynı ürünlere sahip ikinci bir tedarikçiyi yedek olarak not et.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "magaza",
        "4️⃣ Trendyol Mağazası",
        "Başvuru online yapılır; eksiksiz evrakla onay genelde birkaç iş günü sürer.",
        [
            (
                "Trendyol satıcı başvurusu yap",
                [
                    "partner.trendyol.com adresindeki satıcı formunu doldur.",
                    "Hazırla: vergi levhası, kimlik, şirket adına IBAN, KEP adresi; şirket türüne göre imza beyannamesi/sirküsü.",
                    "Satıcı sözleşmesini istenen şekilde imzala ve yükle.",
                    "Güncel belge listesini başvuru ekranından teyit et; şartlar değişebiliyor.",
                ],
            ),
            (
                "Mağaza ayarlarını tamamla",
                [
                    "Mağaza adı ve logosu: kısa, akılda kalıcı ve kategorinle uyumlu.",
                    "Kargo ayarları: Trendyol'un anlaşmalı kargo seçeneklerini ve desi fiyatlarını incele.",
                    "İade adresini tedarikçinle konuştuğun şekilde gir.",
                    "Fatura ayarlarında e-arşiv/e-fatura entegrasyonunu bağla.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "entegrasyon",
        "5️⃣ XML Entegrasyonu",
        "Trendyol XML dosyasını doğrudan kabul etmez; tedarikçi XML'i ile mağazan arasında bir entegrasyon yazılımı gerekir.",
        [
            (
                "Entegrasyon yazılımı seç",
                [
                    "XML bayilik / pazaryeri entegrasyonu yapan yazılımları karşılaştır; çoğu aylık ücretlidir.",
                    "Sor: tedarikçimin XML'ini destekliyor mu, stok-fiyat kaç dakikada bir güncelleniyor, siparişleri tedarikçiye iletiyor mu, fatura kesiyor mu?",
                    "Deneme süresi olan bir yazılımla başla.",
                ],
            ),
            (
                "XML'i bağla ve fiyat kuralını kur",
                [
                    "Tedarikçinin verdiği XML linkini yazılıma ekle.",
                    "Fiyat kuralını kur: bayi fiyatının üzerine komisyon, kargo, KDV ve kâr payını ekleyen bir formül.",
                    "Doğru oranı bulmak için 💰 Kâr Hesabı ile birkaç ürünü hesapla; kuralı buna göre ayarla.",
                ],
            ),
            (
                "Kategori ve özellik eşleştirmesini yap",
                [
                    "Tedarikçinin kategorilerini Trendyol kategorileriyle eşleştir.",
                    "Zorunlu özellikleri (marka, renk, beden, materyal vb.) doldur; eksik özellikli ürün yayına alınmaz.",
                    "Varyantların (renk/beden) doğru eşleştiğini kontrol et.",
                ],
            ),
            (
                "Küçük bir pilot grupla yayına al",
                [
                    "İlk etapta 20-50 ürünle başla; binlerce ürünü birden yükleme.",
                    "Trendyol panelinde ürünlerin onaylandığını, fiyat ve stokların doğru göründüğünü kontrol et.",
                    "Bir ürünün stoğunu tedarikçi tarafında değiştirip senkronizasyonun çalıştığını test et.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "listeleme",
        "6️⃣ Listeleme ve Fiyat",
        "Aynı XML'i birçok satıcı kullanır; farkı başlık, görsel ve doğru fiyat yaratır.",
        [
            (
                "Ürün başlıklarını düzenle",
                [
                    "Format: Marka + Ürün adı + Ana özellik + Varyant.",
                    "Trendyol arama çubuğuna ürün adını yaz; çıkan önerileri başlığa ekle.",
                    "Tedarikçinin hazır başlığını aynen kullanma; aynı başlıklı yüzlerce ürün arasında kaybolursun.",
                ],
            ),
            (
                "Görsel ve açıklamayı güçlendir",
                [
                    "Numunede çektiğin gerçek fotoğrafları ekle.",
                    "Açıklamaya ölçü, malzeme, kullanım ve paket içeriğini net yaz.",
                    "Sık sorulacak soruları açıklamada önceden cevapla.",
                ],
            ),
            (
                "Fiyatları kontrol et",
                [
                    "💰 Kâr Hesabı ile her ana ürünün net kârını kontrol et.",
                    "Rakip satıcıların fiyatına bak; zarar etmeden rekabet edebiliyor musun?",
                    "Kâr çıkmayan ürünleri yayından kaldır.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "siparis",
        "7️⃣ Sipariş ve Hizmet Puanı",
        "Trendyol hizmet puanı; zamanında kargo, iptal ve iade oranlarına bakar. Puan düşerse ürünlerin aramada geriye düşer.",
        [
            (
                "İlk siparişi uçtan uca takip et",
                [
                    "Sipariş düştüğünde entegrasyonun siparişi tedarikçiye ilettiğini kontrol et.",
                    "Kargo takip numarasının Trendyol'a geçtiğini ve faturanın kesildiğini doğrula.",
                    "Müşteriye ulaştığında süreyi not et.",
                ],
            ),
            (
                "Günlük kontrol rutini kur",
                [
                    "Her sabah: yeni siparişler, kargoya verilmeyenler, müşteri soruları.",
                    "Tedarikçide tükenen ama mağazanda görünen ürün var mı kontrol et; iptal en büyük puan kaybıdır.",
                    "Müşteri sorularını 24 saat içinde cevapla.",
                ],
            ),
            (
                "İade sürecini çalıştır",
                [
                    "İade talebi gelince ürünün tedarikçiye mi sana mı döneceğini kontrol et.",
                    "Tedarikçiden bedel iadesini takip et.",
                    "İade sebeplerini not al; aynı sebeple çok iade gelen ürünü kaldır.",
                ],
            ),
        ],
    ),
    make_stage(
        BRANCH_ID,
        "buyume",
        "8️⃣ Satış ve Büyüme",
        "Satan ürünü bul, ona yüklen; satmayanı temizle.",
        [
            (
                "Trendyol reklamıyla test et",
                [
                    "En iyi 5 ürününe küçük günlük bütçeyle sponsorlu ürün reklamı aç.",
                    "Reklam harcamasını ve gelen satışı her gün not et; 💰 Kâr Hesabı'na satış başı reklam maliyetini gir.",
                    "Kârlı olmayan reklamı kapat.",
                ],
            ),
            (
                "Kampanyalara katıl ve yorum topla",
                [
                    "Trendyol'un kampanya tekliflerini kâr hesabıyla değerlendir; zararına kampanyaya girme.",
                    "Memnun müşterilerin yorumu bir sonraki satışı getirir; ürün kalitesini koru.",
                ],
            ),
            (
                "Haftalık temizlik ve büyüme",
                [
                    "Satmayan ve kâr etmeyen ürünleri kaldır.",
                    "Satan ürünlerin benzerlerini ve tamamlayıcılarını ekle.",
                    "Sistem oturunca ikinci pazaryerini (Hepsiburada, N11) aynı entegrasyonla aç.",
                ],
            ),
        ],
    ),
)
