# EATrend

Otomatik animasyon hikaye videosu üretim hattı (Atakan Tech'in "Claude Code ile Otomatik Animasyon Hesabı" videosundaki sistem).

```
metin + duygu notları ──► voice/tts.js ──► ses + kelime zamanları (boşluklar kısaltılır)
                                              │
engine/ (tarayıcıda JS çizim) ◄───────────────┘
        │  Playwright kare kare screenshot
        ▼
render/render.js ──► FFmpeg (kareler + ses, loudnorm) ──► out/<id>/<id>.mp4
```

## Kullanım

```bash
cp .env.example .env        # ElevenLabs anahtarı ve ses ID'si
npm install
node make.js kintsugi --mock   # sahte sesle test (anahtar gerekmez)
node make.js kintsugi          # gerçek ElevenLabs sesi
```

- `content/topics.json`: 30 günlük konu tablosu. 4 tür dönüşümlü: filozof, ilişki, psikoloji, hayat. Kaynaklar elle doğrulanmadan `dogrulandi: true` yapma.
- `content/stories/<id>.json`: metin (`[sakin]`, `[fısıltıyla]` gibi duygu notlarıyla) ve sahne tanımları (kelime indeksine bağlı).
- Videoları tek tek üret, paralel render bilgisayarı çökertebilir.

## Sırada

- [ ] Gerçek ses ile test, `[etiket]` davranışının kontrolü
- [ ] Çizim stili ve karakter geliştirme
- [ ] Admin panel: takvim + dakikada bir saat kontrolü (21:00)
- [ ] Instagram Graph API (profesyonel hesap + Meta app) ve YouTube Data API (Google onayı)
