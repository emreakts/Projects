// Uygulama API'si: panel, onay kuyruğu, bölümler, ayarlar, YouTube bağlantısı.
const fs = require('fs'), path = require('path'), { spawnSync } = require('child_process');
const store = require('./store'), ai = require('./ai'), worker = require('./worker'), pub = require('./publish');
const nOf = b => { const n = +b.n; if (!Number.isInteger(n) || n < 1 || n > 9999) throw new Error('Geçersiz bölüm'); const e = store.load().episodes[n]; if (!e) throw new Error('Bölüm yok'); return e; };
const rm = f => fs.rmSync(f, { recursive: true, force: true });
function clean(n, from) { const d = store.outDir(n); if (!fs.existsSync(d)) return; const id = store.id(n);
  const del = { gorsel: ['img-*', 'mock.flag', 'ref-*', 'line-*', 'voice.wav', 'timeline.json', id + '.mp4'], ses: ['line-*', 'voice.wav', 'timeline.json', id + '.mp4'], video: [id + '.mp4'], senaryo: ['*'] }[from] || [];
  for (const f of fs.readdirSync(d)) if (del.some(p => p === '*' || (p.endsWith('*') ? f.startsWith(p.slice(0, -1)) : f === p))) rm(path.join(d, f)); }
let edgeOk = null; const edge = () => edgeOk ??= spawnSync('python3', ['-c', 'import edge_tts']).status === 0;
const ep = e => ({ n: e.n, id: store.id(e.n), durum: e.durum, baslik: e.ytBaslik || e.baslik, aciklama: e.aciklama || '', asama: e.asama, yuzde: e.yuzde || 0, detay: e.detay || '', hata: e.hata || '', demo: !!e.demo, yayin: e.yayin || null, olusturma: e.olusturma, ...store.pubInfo(e) });

module.exports = (port) => ({
  'GET /api/app/ozet': async () => { const db = store.sync(), A = db.ayarlar, E = Object.values(db.episodes), env = ai.readEnv(), say = d => E.filter(e => e.durum === d).length;
    return { sayilar: { onay: say('onay_bekliyor'), uretim: E.filter(e => ['kuyrukta', 'uretiliyor'].includes(e.durum)).length, planli: say('planlandi'), yayin: say('yayinlandi'), paylasim: say('paylasim_bekliyor'), hata: say('hata') },
      aktif: E.filter(e => ['kuyrukta', 'uretiliyor'].includes(e.durum)).sort((a, b) => a.n - b.n).map(ep), planli: E.filter(e => e.durum === 'planlandi').sort((a, b) => a.yayin.zaman - b.yayin.zaman).map(ep),
      ayarlar: A, hazirlik: { gemini: !!env.GEMINI_API_KEY, ses: (env.SES_SAGLAYICI || 'edge') === 'elevenlabs' ? !!env.ELEVENLABS_API_KEY : edge(), sesTur: env.SES_SAGLAYICI || 'edge', ytAyar: pub.ytConfigured(), ytBagli: pub.ytReady() },
      log: db.log.slice(-25).reverse(), sonrakiSlot: worker.nextSlot() }; },
  'GET /api/app/bolumler': async () => ({ bolumler: Object.values(store.sync().episodes).sort((a, b) => b.n - a.n).map(ep) }),
  'GET /api/app/bolum': async (r, s, b, q) => { const e = nOf({ n: q.n }); let sc = null; try { sc = JSON.parse(fs.readFileSync(store.file(e.n), 'utf8')); } catch {} const o = fs.existsSync(store.outDir(e.n)) ? fs.readdirSync(store.outDir(e.n)).filter(f => /^img-\d+\.png$/.test(f)).sort() : [];
    return { ...ep(e), senaryo: sc, gorseller: o.map(f => `/out/${store.id(e.n)}/${f}`), etiketler: e.etiketler || [], slotOneri: worker.nextSlot(e.n) }; },
  'POST /api/app/uret': async (r, s, b) => { const n = worker.create({ demo: !!b.demo, kaynak: 'elle-panel' }); return { ok: true, n }; },
  'POST /api/app/onayla': async (r, s, b) => { const e = nOf(b), db = store.load(), A = db.ayarlar; if (e.durum !== 'onay_bekliyor') throw new Error('Bu bölüm onaya hazır değil');
    const info = store.pubInfo(e); if (!info.video) throw new Error('Video yok'); if (info.mock) throw new Error('Sahte (test) görselli bölüm yayınlanamaz. Gerçek görselle yeniden üret.');
    if (b.baslik) e.ytBaslik = String(b.baslik).slice(0, 95); if (typeof b.aciklama === 'string') e.aciklama = b.aciklama.slice(0, 4000);
    const zaman = b.zaman ? +new Date(b.zaman) : worker.nextSlot(e.n); if (!(zaman > Date.now())) throw new Error('Yayın zamanı gelecekte olmalı');
    e.durum = 'planlandi'; e.yayin = { zaman, youtube: A.platformlar.youtube && pub.ytReady() ? { durum: 'bekliyor' } : null }; store.save(); store.log(`Bölüm ${e.n} onaylandı, ${new Date(zaman).toLocaleString('tr-TR')} için planlandı`); return { ok: true, zaman }; },
  'POST /api/app/reddet': async (r, s, b) => { const e = nOf(b); if (e.durum === 'uretiliyor') throw new Error('Üretim sürerken reddedilemez');
    if (b.yenidenYaz) { e.not = String(b.not || '').slice(0, 400); clean(e.n, 'senaryo'); rm(store.file(e.n)); worker.requeue(e.n, 'senaryo'); store.log(`Bölüm ${e.n} reddedildi, yeniden yazılıyor`); } else { e.durum = 'reddedildi'; store.save(); store.log(`Bölüm ${e.n} reddedildi`); } return { ok: true }; },
  'POST /api/app/yeniden': async (r, s, b) => { const e = nOf(b); if (e.durum === 'uretiliyor') throw new Error('Üretim sürüyor'); const from = ['senaryo', 'gorsel', 'ses', 'video'].includes(b.from) ? b.from : 'gorsel';
    if (from !== 'senaryo' && !store.hasFile(e.n)) throw new Error('Senaryo yok'); if (from === 'senaryo') { clean(e.n, 'senaryo'); rm(store.file(e.n)); } else clean(e.n, from); e.demo = b.demo === undefined ? e.demo : !!b.demo;
    if (!e.demo && !worker.hasGemini() && ['gorsel', 'senaryo'].includes(from)) throw new Error('Gerçek üretim için Gemini anahtarı gerekli (Ayarlar)'); worker.requeue(e.n, from); store.log(`Bölüm ${e.n} yeniden üretiliyor (${from})`); return { ok: true }; },
  'POST /api/app/sil': async (r, s, b) => { const e = nOf(b); if (e.durum === 'uretiliyor') throw new Error('Üretim sürerken silinemez'); rm(store.file(e.n)); rm(store.outDir(e.n)); delete store.load().episodes[e.n]; store.save(); store.log(`Bölüm ${e.n} silindi`); return { ok: true }; },
  'POST /api/app/paylasildi': async (r, s, b) => { const e = nOf(b); e.durum = 'yayinlandi'; store.save(); store.log(`Bölüm ${e.n} elle paylaşıldı olarak işaretlendi`); return { ok: true }; },
  'GET /api/app/paket': async (r, s, b, q) => { const e = nOf({ n: q.n }); return { baslik: e.ytBaslik || e.baslik, aciklama: e.aciklama || '', video: `/out/${store.id(e.n)}/${store.id(e.n)}.mp4` }; },
  'POST /api/app/ayarlar': async (r, s, b) => { const A = store.load().ayarlar, i = (v, a, z) => Math.min(z, Math.max(a, Math.round(+v) || a));
    if (b.otomatik !== undefined) { if (b.otomatik && !b.demo && !(b.demo === undefined && A.demo) && !worker.hasGemini()) throw new Error('Otomasyon için Gemini anahtarı gerekli (Ayarlar). Denemek için Demo modunu aç.'); A.otomatik = !!b.otomatik; }
    if (b.demo !== undefined) A.demo = !!b.demo; if (b.tampon !== undefined) A.tampon = i(b.tampon, 1, 10); if (b.gunlukUretim !== undefined) A.gunlukUretim = i(b.gunlukUretim, 1, 10);
    if (Array.isArray(b.saatler)) { const s2 = b.saatler.filter(x => /^([01]\d|2[0-3]):[0-5]\d$/.test(x)).slice(0, 6); if (!s2.length) throw new Error('Geçerli saat yok (örn. 21:00)'); A.saatler = s2; }
    if (b.platformlar) A.platformlar = { ...A.platformlar, youtube: !!b.platformlar.youtube }; store.save(); return { ok: true, ayarlar: A }; },
  'POST /api/app/yt-ayar': async (r, s, b) => { const p = {}; if (b.clientId) p.YT_CLIENT_ID = String(b.clientId).trim(); if (b.clientSecret) p.YT_CLIENT_SECRET = String(b.clientSecret).trim(); pub.setEnv(p); return { ok: true }; },
  'GET /api/app/yt-baglan': async () => ({ url: pub.authUrl(port) }),
  'GET /oauth/google/callback': async (r, s, b, q) => { try { if (q.error) throw new Error(q.error); await pub.callback(port, q.code, q.state); return { __redirect: '/?yt=ok' }; } catch (e) { return { __html: `<meta charset=utf-8><body style="font:16px sans-serif;background:#090c15;color:#eee;padding:40px"><h2>YouTube bağlantısı başarısız</h2><p>${String(e.message).replace(/</g, '&lt;')}</p><a style="color:#ffb547" href="/">Geri dön</a>` }; } }
});
