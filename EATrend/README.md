# EATrend

Otomatik animasyon hikaye videosu üretim hattı (Atakan Tech'in "Claude Code ile Otomatik Animasyon Hesabı" videosundaki sistem). İçerik: güncel trend konuları, modern kinetik tipografi tasarımı.

```
metin + duygu notları ──► voice/tts.js ──► ses + kelime zamanları (boşluklar kısaltılır)
                                              │
engine/ (tarayıcıda JS çizim) ◄───────────────┘
        │  Playwright kare kare screenshot
        ▼
render/render.js ──► FFmpeg (kareler + ses, loudnorm) ──► out/<id>/<id>.mp4
```

## Kullanım (Stüdyo, terminalsiz)

Mac'te `baslat.command` dosyasına çift tıkla (ya da `npm start`), tarayıcıda `http://localhost:3000` açılır. Ses seçimi, hikaye düzenleme, ses dinleme ve video üretimi oradan yapılır.

## Kullanım (terminal)

```bash
cp .env.example .env        # ElevenLabs anahtarı ve ses ID'si
npm install
node make.js kisa-video-beyni --mock   # sahte sesle test (anahtar gerekmez)
node make.js kisa-video-beyni          # gerçek ElevenLabs sesi
```

- `content/topics.json`: 30 günlük konu tablosu. 4 tür dönüşümlü: filozof, ilişki, psikoloji, hayat. Kaynaklar elle doğrulanmadan `dogrulandi: true` yapma.
- `content/stories/<id>.json`: metin (`[sakin]`, `[fısıltıyla]` gibi duygu notlarıyla) ve sahne tanımları. Sahne tipleri: hook, stat, liste, bar, kapanis. Sahne başlangıcı `ankraj` (metinden bir ifade) ya da `kelime` (indeks) ile verilir.
- Videoları tek tek üret, paralel render bilgisayarı çökertebilir.

## Sırada

- [ ] Gerçek ses ile test, `[etiket]` davranışının kontrolü
- [ ] Çizim stili ve karakter geliştirme
- [ ] Admin panel: takvim + dakikada bir saat kontrolü (21:00)
- [ ] Instagram Graph API (profesyonel hesap + Meta app) ve YouTube Data API (Google onayı)

## Ücretsiz ses (varsayılan)

Ses kaynağı varsayılan olarak Microsoft Edge'in ücretsiz Türkçe sesleridir (anahtar gerekmez). Kurulum: `pip3 install edge-tts`.
Karakterlerin sesleri `content/series/alsat/bible.json` içinde `edge` alanındadır (ses, hız, ton). Duygu etiketleri hız/ton ayarına çevrilir.
ElevenLabs'e geçmek için Stüdyo'da "Ses kaynağı"nı değiştir ya da `.env`'e `SES_SAGLAYICI=elevenlabs` yaz.

## Otomatik web uygulaması

`baslat.command` (ya da `npm start`) → `http://localhost:3000`

- **Panel:** durum, otomatik pilot, üretim hattı, planlı yayınlar.
- **Onay merkezi:** hazır bölümleri izle, başlık/açıklama/saati düzenle, onayla ya da reddet (geri bildirimle yeniden yazdır).
- **Otomasyon:** Gemini ile senaryo → görsel → ses → video. Tampon kadar bölüm hazırlar, onayladıkların YouTube'a gizli yüklenir ve `publishAt` ile planlanan saatte yayınlanır.
- **Güvenlik kuralları:** sahte (demo) görselli bölüm yayınlanamaz; sahte görseller gerçek üretimde asla yeniden kullanılmaz; her açıklamaya "yapay zekâ ile üretilmiştir" notu eklenir.
- Veriler `data/db.json` içinde (gitignore'da). Manuel düzenleme için `/web/studyo.html`.
