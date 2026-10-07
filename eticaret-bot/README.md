# Dropshipping Asistanı (Telegram Botu)

Dropshipping'in tüm modellerini baştan sona yöneten Telegram botu. Bot 3 dala ayrılır, her dalın
kendi yol haritası, ürün kriterleri ve hesaplama araçları vardır.

| Dal | Model | Durum |
|---|---|---|
| 🅰️ Yurt İçi | Türk tedarikçi (XML bayilik) → Trendyol, Hepsiburada, kendi site | Ön sürüm (genel e-ticaret içeriği) |
| 🅱️ E-İhracat | Türk ürünleri → Etsy, Amazon, Shopify ile yurt dışına (ETGB) | Hazırlanıyor |
| 🅲 Global | Shopify + CJ / AliExpress / ABD depolu tedarikçiler → ABD, UK, AB, CA, AU | ✅ Hazır |

## 🅲 Global Dropshipping

- **🧭 Adım Adım Rehber:** Seni ilk tamamlanmamış adıma götürür. Her adımda numaralı
  "📋 Nasıl yapılır" talimatları, ilgili araca kısayol, önceki/sonraki adım ve
  "✅ Tamamladım, sıradakine geç" butonu var.
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

## Kendi Telegram botuna bağlama

1. Telegram'da [@BotFather](https://t.me/BotFather)'a `/newbot` yaz ve token'ı al
   (zaten botun varsa `/mybots` → botun → *API Token*).
2. `eticaret-bot` klasöründe `.env.example` dosyasını kopyalayıp adını `.env` yap ve token'ı yaz:

   ```
   TELEGRAM_BOT_TOKEN=123456789:ABC...
   ```

   ⚠️ Token bir şifredir: kimseyle paylaşma, `.env` dosyası git'e gönderilmez.

3. Çalıştır:

   ```bash
   cd eticaret-bot
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   python -m eticaret_bot
   ```

4. Telegram'da botuna `/start` yaz. Bot, bu komut çalıştığı sürece cevap verir.

### 7/24 çalıştırma (sunucu)

Bilgisayarın kapanınca bot da durur. Sürekli açık kalması için bir sunucuda (VPS) Docker ile çalıştır:

```bash
cd eticaret-bot
docker build -t dropshipping-bot .
docker run -d --name dropshipping-bot --restart unless-stopped \
  --env-file .env -v dropshipping-data:/data dropshipping-bot
```

Kullanıcı ilerlemesi `dropshipping-data` volume'unda saklanır, güncellemede kaybolmaz.

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
