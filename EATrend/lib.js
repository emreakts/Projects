const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const ROOT = __dirname;
function loadEnv() {
  const f = path.join(ROOT, '.env'); if (!fs.existsSync(f)) return;
  for (const l of fs.readFileSync(f, 'utf8').split('\n')) {
    const m = l.match(/^\s*([A-Z_]+)\s*=\s*(.*)\s*$/); if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
  }
}
function story(id) { return JSON.parse(fs.readFileSync(path.join(ROOT, 'content/stories', id + '.json'), 'utf8')); }
function outDir(id) { const d = path.join(ROOT, 'out', id); fs.mkdirSync(d, { recursive: true }); return d; }
function requirePlaywright() {
  try { return require('playwright'); } catch {}
  const g = execFileSync('npm', ['root', '-g']).toString().trim();
  return require(path.join(g, 'playwright'));
}
module.exports = { ROOT, loadEnv, story, outDir, requirePlaywright };

// --- Dizi (al-sat) yardımcıları
const SERIES = path.join(ROOT, 'content/series');
function bible(dizi) { return JSON.parse(fs.readFileSync(path.join(SERIES, dizi, 'bible.json'), 'utf8')); }
function episodeFile(dizi, n) { return path.join(SERIES, dizi, String(n).padStart(3, '0') + '.json'); }
function episode(dizi, n) { return JSON.parse(fs.readFileSync(episodeFile(dizi, n), 'utf8')); }
function episodeId(dizi, n) { return dizi + '-' + String(n).padStart(3, '0'); }
module.exports = { ...module.exports, bible, episode, episodeFile, episodeId, SERIES };

// --- Ücretsiz ses (Edge TTS): duygu etiketlerini hız/ton/ses ayarına çevirir
const TAG_PROSODY = { 'heyecanlı': [12, 10, 0], 'coşkulu': [12, 12, 0], 'şaşkın': [6, 12, 0], 'gülerek': [8, 10, 0], 'şüpheli': [-8, -8, 0], 'bıkkın': [-10, -10, 0], 'üzgün': [-10, -10, -5], 'sakin': [-6, -4, 0], 'merak': [4, 6, 0], 'vurgulu': [0, 4, 0], 'kendinden emin': [-3, -4, 0], 'fısıltıyla': [-10, -2, -40] };
const num = s => parseFloat(String(s || '0').replace(/[^\d.+-]/g, '')) || 0;
const sgn = (n, u) => (n >= 0 ? '+' : '-') + Math.abs(Math.round(n)) + u;
function edgeSpeak(text, base, outFile) {
  const { spawnSync } = require('child_process'), tag = (text.match(/\[([^\]]+)\]/) || [])[1], p = TAG_PROSODY[(tag || '').toLocaleLowerCase('tr')] || [0, 0, 0];
  const plain = text.replace(/\[[^\]]*\]/g, ' ').replace(/\s+/g, ' ').trim();
  const r = spawnSync('python3', [path.join(ROOT, 'voice/edge.py'), base.ses || 'tr-TR-AhmetNeural', sgn(num(base.hiz) + p[0], '%'), sgn(num(base.ton) + p[1], 'Hz'), sgn(num(base.seviye) + p[2], '%'), outFile], { input: plain, encoding: 'utf8', maxBuffer: 1e7 });
  if (r.status !== 0) throw new Error((r.stderr || 'Edge ses hatası').trim().split('\n').pop());
  return JSON.parse(r.stdout);
}
module.exports = { ...module.exports, edgeSpeak };
