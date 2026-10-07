# Dropshipping Asistanı (Telegram Botu)

Dropshipping'in tüm modellerini baştan sona yöneten Telegram botu. Bot 3 dala ayrılır, her dalın
kendi yol haritası, ürün kriterleri ve hesaplama araçları vardır.

| Dal | Model | Durum |
|---|---|---|
| 🅰️ Yurt İçi | Türk tedarikçi (XML bayilik) → Trendyol, Hepsiburada, kendi site | Ön sürüm (genel e-ticaret içeriği) |
| 🅱️ E-İhracat | Türk ürünleri → Etsy, Amazon, Shopify ile yurt dışına (ETGB) | Hazırlanıyor |
| 🅲 Global | Shopify + CJ / AliExpress / ABD depolu tedarikçiler → ABD, UK, AB, CA, AU | ✅ Hazır |

## 🅲 Global Dropshipping

- **🗺 Yol Haritası:** 8 aşama, 46 adım. Hedef pazar ve bütçe, yurt dışı şirket ve ödeme
  (LLC, EIN, Stripe), ürün araştırması, tedarikçi ve DDP kargo, Shopify mağaza, reklam testi,
  operasyon, ölçekleme
- **🔍 Ürün Analizi:** 10 kriter: wow etkisi, fiyat çarpanı, fiyat aralığı, talep kanıtı,
  doygunluk, video kreatif kolaylığı, teslim süresi, boyut, iade ve yasal risk
- **💵 Kâr Hesabı (USD):** Gümrük, ödeme komisyonu, iade/chargeback dahil. Başa baş CPA,
  başa baş ROAS, fiyat çarpanı ve hedef marja göre fiyat
- **📊 Reklam Testi:** Harcama, gösterim, tıklama, sepete ekleme ve satın almaya göre
  kapat / devam / ölçekle kararı ve huni teşhisi (kreatif, ürün sayfası, ödeme adımı)

2026 kuralları içerikte yer alır: ABD'de 800 $ gümrük muafiyetinin kalkması, AB'de ürün başına
3 € gümrük, Türkiye'de Stripe/PayPal olmaması ve Shopify Payments'ın yabancılara kısıtlamaları.

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

`/start` `/menu` `/a` `/b` `/c` `/iptal` `/sifirla` `/yardim`

## Testler

```bash
pip install -r requirements-dev.txt
python -m pytest
```

## Proje yapısı

```
eticaret_bot/
  bot.py              Telegram akışları (menüler, konuşmalar); dallardan bağımsız
  storage.py          SQLite ilerleme kaydı
  formatting.py       Türkçe sayı okuma/yazma
  core/               Ortak motorlar: yol haritası, puanlama, dal ve form tanımları
  calc/               Hesaplar: tl_profit, global_profit, ad_test
  branches/           Dallar: yurtici (A), eihracat (B), global_ds (C)
```

Yeni dal veya araç eklemek için `branches/` altında bir `Branch` tanımlamak yeterli; bot menüleri
ve akışları otomatik oluşur.

## Planlanan

- 🅰️ Yurt içi: XML tedarikçi akışı, fiyat/stok senkronu, pazaryeri kuralları
- 🅱️ E-ihracat: ETGB, Etsy/Amazon süreçleri, uluslararası kargo hesabı
- 🅲 Global: tedarikçi karşılaştırma, reklam metni/hook üretimi, haftalık KPI raporu
