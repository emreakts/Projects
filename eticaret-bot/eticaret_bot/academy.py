"""🎓 E-Ticarete Başlangıç Akademisi: sıfırdan başlayanlar için kısa dersler ve model seçme testi.

Ders metinleri Telegram HTML biçimindedir (<b>, <i>); içerikte '&', '<', '>' kullanılmamalı.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Lesson:
    title: str
    body: str
    takeaway: str  # dersin tek cümlelik özeti


LESSONS: tuple[Lesson, ...] = (
    Lesson(
        "E-ticaret nedir, hangi modeller var?",
        "E-ticaret, ürünü internetten satmaktır. Asıl fark <b>ürünün nereden geldiği</b> ve "
        "<b>stoğu kimin tuttuğu</b>dur:\n\n"
        "📦 <b>Stoklu satış:</b> Toptan alırsın, depolarsın, kendin gönderirsin. Marj iyi, ama baştan para "
        "bağlarsın ve satmazsa elinde kalır.\n\n"
        "🚚 <b>Dropshipping:</b> Stok tutmazsın. Sipariş gelince tedarikçi ürünü doğrudan müşteriye gönderir. "
        "Sermaye az, risk düşük; ama marj düşük, kalite ve kargo kontrolü sende değil.\n\n"
        "🏷 <b>Private label:</b> Hazır bir ürüne kendi markanı bastırırsın. Daha çok sermaye ister, "
        "ama marka değeri ve yüksek marj sağlar.\n\n"
        "🛠 <b>Kendi üretimin:</b> El emeği veya üretim. Rekabet farklılaşmayla kazanılır.\n\n"
        "💾 <b>Dijital ürün:</b> Şablon, kurs, e-kitap. Stok ve kargo yok, ama içerik üretmek gerekir.\n\n"
        "Bu bot ağırlıklı olarak <b>dropshipping</b> üzerine kurulu, çünkü en az sermayeyle "
        "öğrenerek başlamanın yolu bu.",
        "Dropshipping, stok riski almadan e-ticareti öğrenmenin en ucuz yolu.",
    ),
    Lesson(
        "Nerede satılır? Satış kanalları",
        "🏪 <b>Pazaryerleri</b> (Trendyol, Hepsiburada, Amazon, Etsy): Müşteri zaten orada. "
        "Trafik hazır, güven hazır. Karşılığında komisyon ödersin ve platformun kurallarına uyarsın.\n\n"
        "🌐 <b>Kendi siten</b> (Shopify, İkas, Ticimax): Marka ve müşteri verisi senin, komisyon düşük. "
        "Ama ziyaretçiyi sen getirmek zorundasın; bu da genelde reklam demek.\n\n"
        "📱 <b>Sosyal medya</b> (Instagram, TikTok): Ürünü video ile göstermek için güçlü. "
        "Satışı genelde siteye veya pazaryerine yönlendirerek yaparsın.\n\n"
        "🇹🇷 / 🌍 <b>Yurt içi mi yurt dışı mı?</b>\n"
        "• Yurt içi: Türkçe, kolay iade, hızlı kargo; rekabet ve fiyat baskısı yüksek.\n"
        "• Yurt dışı: döviz kazanırsın, pazar büyük; dil, gümrük, ödeme altyapısı ve kargo daha zor.\n\n"
        "Yeni başlayan için en düşük risk: <b>önce pazaryeri</b>, sonra kendi site.",
        "Pazaryeri hazır müşteri verir, kendi site marka ve marj verir.",
    ),
    Lesson(
        "Para nasıl kazanılır? Birim ekonomisi",
        "Ciro değil, <b>sipariş başına net kâr</b> önemlidir. Bir siparişte cebine kalan:\n\n"
        "<b>Net kâr</b> = Satış fiyatı − ürün maliyeti − komisyon − kargo − reklam − iade payı − vergi\n\n"
        "📌 <b>Örnek</b> (yurt içi, KDV hariç rakamlarla):\n"
        "Satış 500 TL, ürün 200 TL, komisyon 100 TL, kargo 50 TL, reklam 60 TL, iade payı 15 TL\n"
        "→ Net kâr = <b>75 TL</b> (marj %15)\n\n"
        "Aynı ürünü reklamsız satsaydın kâr 135 TL olurdu. Demek ki bir satış için reklama "
        "<b>en fazla 135 TL</b> harcayabilirsin. Buna <b>başa baş CPA</b> denir.\n\n"
        "🎯 <b>Altın kurallar</b>\n"
        "• Reklamla satıyorsan satış fiyatı, toplam maliyetin en az 2,5-3 katı olmalı.\n"
        "• Satış yapmak kâr etmek demek değildir; her ürünü önce hesapla.\n"
        "• Bottaki 💰 / 💵 Kâr Hesabı araçları bunu senin yerine yapar.",
        "Her üründe önce sipariş başı net kârı ve başa baş CPA'yı hesapla.",
    ),
    Lesson(
        "Ne satılır? Ürün seçiminin temelleri",
        "İyi ürün 6 testi geçer:\n\n"
        "1️⃣ <b>Talep var mı?</b> İnsanlar bunu arıyor ve alıyor mu? (yorum sayıları, aktif reklamlar, trendler)\n"
        "2️⃣ <b>Marj yeterli mi?</b> Tüm masraflardan sonra kâr kalıyor mu?\n"
        "3️⃣ <b>Rekabet aşılabilir mi?</b> Herkes aynı ürünü aynı fiyata mı satıyor?\n"
        "4️⃣ <b>Kargosu kolay mı?</b> Küçük, hafif, kırılmaz ürün daha az dert çıkarır.\n"
        "5️⃣ <b>İade riski düşük mü?</b> Beden, arıza, beklenti sorunu olan ürünler iade getirir.\n"
        "6️⃣ <b>Yasal mı?</b> Marka taklidi, izin gerektiren kategoriler (gıda, kozmetik, medikal) riskli.\n\n"
        "🔍 <b>Nereden fikir bulunur?</b> Pazaryeri çok satanlar, Google Trends, TikTok ve Instagram'da "
        "çok izlenen ürün videoları, Meta Ad Library'deki aktif reklamlar.\n\n"
        "Bottaki 🔍 Ürün Analizi, bir ürünü bu kriterlerle puanlar.",
        "Talep, marj, rekabet, kargo, iade ve yasal risk: altısını da kontrol etmeden ürün seçme.",
    ),
    Lesson(
        "Ürünü nereden bulursun? Tedarik",
        "🏭 <b>Üretici:</b> En ucuz fiyat, ama genelde yüksek minimum sipariş adedi ister.\n"
        "📦 <b>Toptancı:</b> Daha az adetle alım, fiyat biraz yüksek.\n"
        "🔗 <b>Dropshipping tedarikçisi:</b> Stok tutmazsın, sipariş başı ödersin. "
        "Yurt içinde XML bayilik veren firmalar, yurt dışında CJ Dropshipping, AliExpress (DSers), Spocket gibi platformlar.\n\n"
        "✅ <b>Tedarikçi seçerken</b>\n"
        "• En az 2-3 tedarikçiden fiyat ve teslim süresi al.\n"
        "• <b>Numune sipariş et</b>: kaliteyi ve paketlemeyi gözünle gör.\n"
        "• Stok güncelliğini sor: tükenmiş ürünü satmak iptal ve kötü puan demek.\n"
        "• İade ve hasarlı ürün sürecini yazılı netleştir.\n"
        "• Bir yedek tedarikçin olsun.",
        "Numune görmeden ve yedek tedarikçi bulmadan satışa başlama.",
    ),
    Lesson(
        "Yasal temeller (Türkiye)",
        "Düzenli ve kâr amaçlı satış yapıyorsan <b>vergi mükellefi</b> olman gerekir.\n\n"
        "🏢 <b>Şirket:</b> Başlangıçta genelde şahıs şirketi yeterli; ciro büyüyünce limited şirket "
        "düşünülür. Kararı bir <b>mali müşavirle</b> ver.\n"
        "🧾 <b>Fatura:</b> e-Arşiv / e-Fatura ile her satışa fatura kesilir.\n"
        "📄 <b>Mesafeli satış:</b> Mesafeli satış sözleşmesi, ön bilgilendirme formu ve iade politikası "
        "sitende olmalı. Müşterinin 14 gün cayma hakkı vardır.\n"
        "🔒 <b>KVKK:</b> Müşteri bilgisi topluyorsan aydınlatma metni ve gizlilik politikası gerekir.\n"
        "🗂 <b>ETBİS:</b> E-ticaret yapanların Ticaret Bakanlığı sistemine kaydı.\n\n"
        "ℹ️ Evde kendi el emeğini internetten satanlar için <i>esnaf muafiyeti</i> vardır; "
        "başkasının ürününü satmak (dropshipping dahil) bu kapsama girmez.\n\n"
        "Yurt dışına satışta (🅲 Global dalı) şirket ve ödeme yapısı farklıdır; o dalın rehberinde anlatılıyor.",
        "Satışa başlamadan önce mali müşavirle konuş, şirketini ve faturanı hazırla.",
    ),
    Lesson(
        "Listeleme ve pazarlama",
        "Müşteri ürünü elle tutamaz; <b>ürün sayfası her şeydir</b>.\n\n"
        "📝 <b>İyi bir listeleme</b>\n"
        "• <b>Başlık:</b> İnsanların aradığı kelimelerle başlar. Örnek: Marka + Ürün + Ana özellik + Varyant.\n"
        "• <b>Görseller:</b> En az 5 adet: beyaz fon, kullanım anı, detay, ölçü, paket içeriği. Video varsa daha iyi.\n"
        "• <b>Açıklama:</b> Özelliği değil faydayı anlat. 'Paslanmaz çelik' yerine 'yıllarca paslanmaz, bulaşık makinesinde yıkanır'.\n"
        "• <b>SSS ve yorumlar:</b> Kargo süresi, iade, kullanım sorularını önceden cevapla.\n\n"
        "📣 <b>Müşteriyi nasıl getirirsin?</b>\n"
        "• Pazaryeri içi reklam (sponsorlu ürün): en kolay başlangıç.\n"
        "• Meta (Instagram/Facebook) ve TikTok video reklamları: kendi site için ana yol.\n"
        "• Organik içerik: ücretsiz ama zaman ister; ürünün videosunu düzenli paylaş.\n\n"
        "Kural: önce <b>küçük bütçeyle test et</b>, işe yarayan reklamı büyüt.",
        "Ürün sayfası satışı yapar, reklam sadece müşteriyi kapıya getirir.",
    ),
    Lesson(
        "Operasyon ve müşteri memnuniyeti",
        "Satış başladıktan sonra işin yarısı operasyondur.\n\n"
        "🚚 <b>Kargo:</b> Siparişi hızlı gönder, takip numarasını hemen paylaş. "
        "Pazaryerleri geç kargoyu cezalandırır.\n"
        "💬 <b>Müşteri hizmetleri:</b> Sorulara 24 saat içinde cevap ver. Hazır cevap şablonları kullan.\n"
        "↩️ <b>İade:</b> Kuralların net olsun; sorunlu müşteriyle tartışma, çöz. Kötü yorum, kaybettiğin "
        "bir ürün bedelinden pahalıdır.\n"
        "⭐ <b>Yorum:</b> Memnun müşteriden yorum iste; yorumlar bir sonraki satışı getirir.\n"
        "📊 <b>Takip:</b> Haftada bir; ciro, net kâr, iade oranı, reklam getirisine bak. "
        "Zarar eden ürünü bırakmaktan korkma.",
        "Hızlı kargo, hızlı cevap ve net iade kuralı: mağaza puanın ve tekrar satışın buna bağlı.",
    ),
    Lesson(
        "İlk 30 gün planı",
        "📅 <b>1. hafta: Karar</b>\n"
        "• 🧭 'Bana uygun model' testini çöz, dalını seç.\n"
        "• Bütçeni ve haftalık ayıracağın zamanı yaz.\n"
        "• Mali müşavirle ilk görüşmeyi yap.\n\n"
        "📅 <b>2. hafta: Ürün</b>\n"
        "• 20 ürün fikri topla, 🔍 Ürün Analizi ile puanla.\n"
        "• En iyi 3 ürünün kâr hesabını yap.\n"
        "• Tedarikçilerden fiyat al, numune sipariş et.\n\n"
        "📅 <b>3. hafta: Mağaza</b>\n"
        "• Satış kanalını aç (pazaryeri hesabı veya Shopify).\n"
        "• Yasal metinleri ve ödeme altyapısını hazırla.\n"
        "• İlk ürünlerini listele.\n\n"
        "📅 <b>4. hafta: Test</b>\n"
        "• Küçük bütçeli reklam veya pazaryeri reklamı başlat.\n"
        "• Her gün sonuçları kaydet; çalışmayanı kapat, çalışanı büyüt.\n\n"
        "Bundan sonrası seçtiğin dalın 🧭 Adım Adım Rehberi'nde, adım adım.",
        "Ay sonunda hedef: seçilmiş bir ürün, açık bir mağaza ve ilk test sonuçları.",
    ),
)


# ---------- 🧭 Bana uygun model testi ----------

@dataclass(frozen=True)
class QuizQuestion:
    question: str
    options: tuple[tuple[str, dict[str, int]], ...]  # (etiket, {dal: puan})


QUIZ: tuple[QuizQuestion, ...] = (
    QuizQuestion(
        "💰 Başlangıç için ayırabileceğin toplam bütçe?",
        (
            ("25.000 TL altı", {"a": 2}),
            ("25.000 - 75.000 TL", {"a": 1, "b": 1}),
            ("75.000 TL üstü", {"b": 1, "c": 2}),
        ),
    ),
    QuizQuestion(
        "🇬🇧 İngilizce seviyen?",
        (
            ("Yok / çok az", {"a": 2}),
            ("Orta, idare ederim", {"b": 1, "c": 1}),
            ("İyi", {"b": 1, "c": 2}),
        ),
    ),
    QuizQuestion(
        "🏢 Yurt dışında şirket kurmaya ve dövizle aylık gider ödemeye hazır mısın?",
        (
            ("Hayır", {"a": 2, "b": 1}),
            ("Belki, araştırırım", {"b": 1, "c": 1}),
            ("Evet", {"c": 2}),
        ),
    ),
    QuizQuestion(
        "📣 Reklam yönetimi (Instagram, TikTok reklamları) hakkında ne düşünüyorsun?",
        (
            ("Uzak durmak isterim", {"a": 2, "b": 1}),
            ("Öğrenmeye açığım", {"b": 1, "c": 1}),
            ("Reklamla hızlı büyümek istiyorum", {"c": 2}),
        ),
    ),
    QuizQuestion(
        "⏰ Haftada ne kadar zaman ayırabilirsin?",
        (
            ("10 saatten az", {"a": 1, "b": 1}),
            ("10 - 25 saat", {"a": 1, "b": 1, "c": 1}),
            ("25 saatten fazla", {"c": 2}),
        ),
    ),
    QuizQuestion(
        "🎯 Asıl hedefin ne?",
        (
            ("Düşük riskli ek gelir", {"a": 2}),
            ("Döviz kazanmak", {"b": 2, "c": 1}),
            ("Hızlı büyüme, yüksek risk ve getiri", {"c": 2}),
        ),
    ),
)

QUIZ_REASONS = {
    "a": "Türkçe, düşük sermaye ve düşük riskle başlayabilirsin. Pazaryerlerinin hazır müşterisi var, "
    "yurt dışı şirket ve döviz gideri gerekmez.",
    "b": "Türk ürünlerini yurt dışına satarak döviz kazanırsın. Etsy ve Amazon'un hazır müşterisiyle, "
    "reklama çok yüklenmeden başlayabilirsin.",
    "c": "Bütçen, İngilizcen ve reklam isteğin global dropshipping için uygun. Pazar en büyüğü, "
    "ama yurt dışı şirket ve reklam bütçesi gerektirir.",
}


def quiz_scores(answers: str) -> dict[str, int]:
    """answers: her sorunun seçilen seçenek indeksi, ör. '021102'."""
    scores = {"a": 0, "b": 0, "c": 0}
    for q, ch in zip(QUIZ, answers):
        for branch, pts in q.options[int(ch)][1].items():
            scores[branch] += pts
    return scores


def recommend(answers: str) -> list[str]:
    """Dalları puana göre sıralar (eşitlikte daha düşük riskli dal önce: a, b, c)."""
    scores = quiz_scores(answers)
    return sorted(scores, key=lambda b: (-scores[b], b))
