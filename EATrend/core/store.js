// Basit dosya tabanlı veritabanı: bölümler, ayarlar, etkinlik günlüğü.
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..'), F = path.join(ROOT, 'data', 'db.json'), SERI = path.join(ROOT, 'content/series/alsat');
const DEF = { otomatik: false, demo: false, tampon: 2, gunlukUretim: 1, saatler: ['21:00'], platformlar: { youtube: true } };
let db = null;
const load = () => { if (db) return db; try { db = JSON.parse(fs.readFileSync(F, 'utf8')); } catch { db = {}; } db.episodes ??= {}; db.log ??= []; db.ayarlar = { ...DEF, ...(db.ayarlar || {}), platformlar: { ...DEF.platformlar, ...((db.ayarlar || {}).platformlar || {}) } }; return db; };
const save = () => { fs.mkdirSync(path.dirname(F), { recursive: true }); const t = F + '.tmp'; fs.writeFileSync(t, JSON.stringify(db, null, 1)); fs.renameSync(t, F); };
const log = m => { load().log.push({ t: Date.now(), m }); if (db.log.length > 200) db.log.splice(0, db.log.length - 200); save(); };
const id = n => 'alsat-' + String(n).padStart(3, '0'), file = n => path.join(SERI, String(n).padStart(3, '0') + '.json'), outDir = n => path.join(ROOT, 'out', id(n));
const hasFile = n => fs.existsSync(file(n)), isMock = n => fs.existsSync(path.join(outDir(n), 'mock.flag'));

// Diskteki bölümleri veritabanıyla eşle
function sync() {
  load(); let ch = false;
  for (const f of fs.readdirSync(SERI)) { const m = f.match(/^(\d+)\.json$/); if (!m) continue; const n = +m[1];
    if (!db.episodes[n]) { let b = {}; try { b = JSON.parse(fs.readFileSync(path.join(SERI, f), 'utf8')); } catch {} db.episodes[n] = { n, durum: 'taslak', baslik: b.baslik || '', olusturma: Date.now(), kaynak: 'elle' }; ch = true; } }
  for (const e of Object.values(db.episodes)) { if (hasFile(e.n)) { try { const b = JSON.parse(fs.readFileSync(file(e.n), 'utf8')); if (b.baslik && b.baslik !== e.baslik) { e.baslik = b.baslik; ch = true; } } catch {} } }
  if (ch) save(); return db;
}
const nextN = () => Math.max(0, ...Object.keys(load().episodes).map(Number), ...fs.readdirSync(SERI).map(f => +(f.match(/^(\d+)\.json$/) || [0, 0])[1])) + 1;
const pubInfo = e => { const o = outDir(e.n), mp4 = path.join(o, id(e.n) + '.mp4'); return { video: fs.existsSync(mp4), mock: isMock(e.n) }; };
module.exports = { load, save, log, sync, id, file, outDir, hasFile, isMock, nextN, pubInfo, ROOT, SERI };
