"""E-ticaret yol haritası: sıfırdan büyümeye kadar aşamalar ve kontrol listeleri."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    id: str
    text: str


@dataclass(frozen=True)
class Stage:
    id: str
    title: str
    guide: str
    tasks: tuple[Task, ...]


def _stage(sid: str, title: str, guide: str, tasks: list[str]) -> Stage:
    return Stage(sid, title, guide, tuple(Task(f"{sid}.{i}", t) for i, t in enumerate(tasks, 1)))


STAGES: tuple[Stage, ...] = (
    _stage(
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
    _stage(
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
    _stage(
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
    _stage(
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
    _stage(
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
    _stage(
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
    _stage(
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
    _stage(
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
    _stage(
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

ALL_TASK_IDS = tuple(t.id for s in STAGES for t in s.tasks)


def get_stage(stage_id: str) -> Stage:
    for s in STAGES:
        if s.id == stage_id:
            return s
    raise KeyError(stage_id)


def stage_progress(stage: Stage, done: set[str]) -> tuple[int, int]:
    return sum(t.id in done for t in stage.tasks), len(stage.tasks)


def next_task(done: set[str]) -> tuple[Stage, Task] | None:
    """Sırayla ilk tamamlanmamış görevi döndürür; hepsi bittiyse None."""
    for s in STAGES:
        for t in s.tasks:
            if t.id not in done:
                return s, t
    return None


def progress_bar(done_count: int, total: int, width: int = 10) -> str:
    filled = round(width * done_count / total) if total else 0
    return "▓" * filled + "░" * (width - filled) + f" {done_count}/{total}"
