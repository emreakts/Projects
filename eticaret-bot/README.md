# E-Ticaret Asistanı (Telegram Botu)

E-ticaret sürecini baştan sona yöneten Telegram botu: iş modeli, ürün seçimi, tedarik, yasal süreç,
mağaza kurulumu, listeleme, pazarlama, operasyon ve büyüme. Hedef pazar şu an Türkiye.

## Özellikler (v0.1)

| Özellik | Ne yapar |
|---|---|
| 🗺 Yol Haritası | 9 aşama, 47 adım. İşaretlediğin adımları kaydeder, ilerlemeni gösterir |
| 📍 Sıradaki Adım | Şu an ne yapman gerektiğini söyler, tek tıkla tamamlandı yaparsın |
| 🔍 Ürün Analizi | 10 kriter (marj, talep, rekabet, trend, sezon, kargo, iade, fiyat, tedarik, yasal) ile 0-100 skor, karar ve tavsiyeler |
| 💰 Kâr Hesapla | KDV, komisyon, kargo, reklam, paketleme, iade dahil net kâr, marj, ROI, başa baş ROAS ve hedef marja göre önerilen fiyat |

## Kurulum

1. Telegram'da [@BotFather](https://t.me/BotFather)'a `/newbot` yaz ve token'ı al.
2. Kur ve çalıştır:

```bash
cd eticaret-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="BotFather'dan aldığın token"
python -m eticaret_bot
```

3. Telegram'da botunu aç ve `/start` yaz.

İlerleme verisi `eticaret_bot.db` (SQLite) dosyasında tutulur, yolu `ETICARET_DB` ile değiştirilebilir.

## Komutlar

`/start` `/menu` `/yolharitasi` `/siradaki` `/urun` `/kar` `/iptal` `/sifirla` `/yardim`

## Testler

```bash
pip install -r requirements-dev.txt
python -m pytest
```

## Proje yapısı

```
eticaret_bot/
  bot.py              Telegram akışları (menü, konuşmalar)
  storage.py          SQLite ilerleme kaydı
  formatting.py       Türkçe sayı okuma/yazma
  modules/
    roadmap.py        Aşamalar ve kontrol listeleri
    product_score.py  Ürün puanlama kriterleri
    profit_calc.py    Kâr ve fiyat hesapları
```

İş mantığı `modules/` altında Telegram'dan bağımsızdır, böylece ileride web paneli veya başka kanal eklenebilir.

## Planlanan

- Yapay zekâ ile ürün açıklaması, SEO başlık ve reklam metni üretimi
- Tedarikçi değerlendirme ve maliyet karşılaştırma
- Stok ve sipariş takibi, pazaryeri API entegrasyonları (Trendyol, Hepsiburada)
- Haftalık KPI raporu ve hatırlatmalar
