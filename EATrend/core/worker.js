// Otomasyon işçisi: senaryo → görsel → ses → video üretir, otomatik bölüm açar, yüklemeleri yapar.
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const store = require('./store'), ai = require('./ai'), pub = require('./publish');
const ROOT = store.ROOT; let busy = false, ctx = null;
const STEPS = [['senaryo', 10], ['gorsel', 50], ['ses', 15], ['video', 25]];

function exec(args, onLine) { return new Promise(res => { const p = spawn('node', args, { cwd: ROOT }); let log = ''; const f = d => { const s = d.toString(); log += s; const l = s.split(/[\r\n]+/).filter(Boolean).pop(); if (l) onLine(l); }; p.stdout.on('data', f); p.stderr.on('data', f); p.on('close', c => res({ code: c, log })); }); }
const today = () => new Date().toDateString();
const hasGemini = () => !!ai.readEnv().GEMINI_API_KEY;

function create({ demo, kaynak = 'otomatik' }) {
  const db = store.load(); if (!demo && !hasGemini()) throw new Error('Gerçek bölüm için Gemini anahtarı gerekli (Ayarlar). Denemek için Demo modunu aç.');
  const n = store.nextN(); db.episodes[n] = { n, durum: 'kuyrukta', asama: 'senaryo', yuzde: 0, baslik: '(senaryo yazılıyor)', olusturma: Date.now(), kaynak, demo: !!demo, deneme: 0 }; store.save(); store.log(`Bölüm ${n} sıraya alındı${demo ? ' (demo)' : ''}`); return n;
}
function requeue(n, from) { const e = store.load().episodes[n]; Object.assign(e, { durum: 'kuyrukta', asama: from, yuzde: 0, hata: null, deneme: 0 }); store.save(); }

async function produce(e) {
  const db = store.load(), A = db.ayarlar, set = (asama, yuzde, extra = {}) => { Object.assign(e, { asama, yuzde: Math.min(99, Math.round(yuzde)), ...extra }); store.save(); };
  const base = k => STEPS.slice(0, k).reduce((a, s) => a + s[1], 0), n = e.n, mock = e.demo ? ['--mock-gorsel'] : [];
  e.durum = 'uretiliyor'; store.save();
  try {
    if (!store.hasFile(n) || e.asama === 'senaryo') {
      set('senaryo', 2); const ep = await ai.yaz(n, { demo: e.demo, note: e.not }); fs.writeFileSync(store.file(n), JSON.stringify(ep, null, 2));
      Object.assign(e, { baslik: ep.baslik, ...ai.meta(ep) }); store.log(`Bölüm ${n} senaryosu yazıldı: ${ep.baslik}`);
    } else if (!e.aciklama) { const ep = JSON.parse(fs.readFileSync(store.file(n), 'utf8')); Object.assign(e, ai.meta(ep)); }
    const runs = [['gorsel', ['dizi/gorsel.js', 'alsat', n, ...mock]], ['ses', ['dizi/ses.js', 'alsat', n]], ['video', ['render/render-dizi.js', 'alsat', n]]];
    for (const [name, args] of runs) { const k = STEPS.findIndex(s => s[0] === name); set(name, base(k)); const r = await exec(args.map(String), l => { e.detay = l.slice(0, 140); });
      if (r.code !== 0) throw new Error((r.log.trim().split('\n').pop() || name + ' hatası').slice(0, 300)); }
    Object.assign(e, { durum: 'onay_bekliyor', asama: 'hazir', yuzde: 100, hata: null, detay: '', uretim: Date.now() }); store.save(); store.log(`Bölüm ${n} hazır, onay bekliyor`);
  } catch (err) { e.deneme = (e.deneme || 0) + 1; Object.assign(e, { durum: 'hata', hata: String(err.message || err).slice(0, 300) }); store.save(); store.log(`Bölüm ${n} hata: ${e.hata}`); }
}

function nextSlot(excludeN) {
  const db = store.load(), used = new Set(Object.values(db.episodes).filter(x => x.n !== excludeN && x.yayin && x.yayin.zaman).map(x => Math.floor(x.yayin.zaman / 60000)));
  const now = Date.now() + 10 * 60000;
  for (let d = 0; d < 60; d++) for (const hm of [...db.ayarlar.saatler].sort()) { const [h, m] = hm.split(':').map(Number), t = new Date(); t.setDate(t.getDate() + d); t.setHours(h, m || 0, 0, 0); if (t.getTime() > now && !used.has(Math.floor(t.getTime() / 60000))) return t.getTime(); }
  return now + 86400000;
}

async function tick() {
  if (!ctx) return; const db = store.sync(), A = db.ayarlar;
  // 1) yüklemeler ve yayın zamanı geçenler (üretimden bağımsız)
  for (const e of Object.values(db.episodes)) {
    if (e.durum !== 'planlandi' || !e.yayin) continue; const y = e.yayin;
    if (A.platformlar.youtube && pub.ytReady() && y.youtube && y.youtube.durum === 'bekliyor' && Date.now() >= (y.sonDeneme || 0) + 600000) {
      y.sonDeneme = Date.now(); try { const r = await pub.ytUpload({ baslik: e.ytBaslik || e.baslik, aciklama: e.aciklama, etiketler: e.etiketler }, path.join(store.outDir(e.n), store.id(e.n) + '.mp4'), y.zaman); y.youtube = { durum: 'yuklendi', ...r }; store.log(`Bölüm ${e.n} YouTube'a yüklendi (${new Date(y.zaman).toLocaleString('tr-TR')} için zamanlandı)`); }
      catch (err) { y.youtube = { durum: 'bekliyor', hata: String(err.message).slice(0, 250), deneme: (y.youtube.deneme || 0) + 1 }; store.log(`Bölüm ${e.n} YouTube hatası: ${y.youtube.hata}`); } store.save();
    }
    if (Date.now() >= y.zaman) { e.durum = y.youtube && y.youtube.durum === 'yuklendi' ? 'yayinlandi' : 'paylasim_bekliyor'; store.save(); store.log(`Bölüm ${e.n}: ${e.durum === 'yayinlandi' ? 'yayınlandı' : 'paylaşım zamanı geldi (elle paylaş)'}`); }
  }
  if (busy || ctx.job.state === 'running') return;
  // 2) sıradaki üretim
  const q = Object.values(db.episodes).filter(e => e.durum === 'kuyrukta').sort((a, b) => a.n - b.n)[0];
  if (q) { busy = true; ctx.job.state = 'running'; ctx.job.what = 'otomasyon'; ctx.job.progress = `Bölüm ${q.n} üretiliyor`; try { await produce(q); } finally { busy = false; ctx.job.state = 'idle'; } return; }
  // 3) otomatik yeni bölüm
  if (A.otomatik) {
    const bekleyen = Object.values(db.episodes).filter(e => ['kuyrukta', 'uretiliyor', 'onay_bekliyor'].includes(e.durum)).length;
    const bugun = Object.values(db.episodes).filter(e => e.kaynak === 'otomatik' && new Date(e.olusturma).toDateString() === today()).length;
    if (bekleyen < A.tampon && bugun < A.gunlukUretim && (A.demo || hasGemini())) { try { create({ demo: A.demo }); } catch (err) { store.log('Otomatik üretim durdu: ' + err.message); A.otomatik = false; store.save(); } }
  }
}
function start(c) { ctx = c; store.sync(); for (const e of Object.values(store.load().episodes)) if (e.durum === 'uretiliyor') { e.durum = 'kuyrukta'; } store.save(); setInterval(() => tick().catch(err => store.log('Worker hatası: ' + err.message)), 4000); }
module.exports = { start, create, requeue, nextSlot, hasGemini };
