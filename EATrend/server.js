// EATrend Stüdyo: yerel web arayüzü. Sadece bu bilgisayardan erişilir (127.0.0.1).
const http = require('http'), fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const ROOT = __dirname, PORT = +process.env.PORT || 3000, ENVF = path.join(ROOT, '.env');
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.json': 'application/json', '.mp4': 'video/mp4', '.wav': 'audio/wav', '.png': 'image/png' };
const idOk = s => typeof s === 'string' && /^[a-z0-9-]{1,60}$/.test(s);

function readEnv() { const o = {}; if (fs.existsSync(ENVF)) for (const l of fs.readFileSync(ENVF, 'utf8').split('\n')) { const m = l.match(/^\s*([A-Z_]+)\s*=\s*(.*)\s*$/); if (m) o[m[1]] = m[2]; } return o; }
function writeEnv(patch) { const o = { ...readEnv(), ...patch }; fs.writeFileSync(ENVF, Object.entries(o).map(([k, v]) => `${k}=${v}`).join('\n') + '\n'); }
const storyFile = id => path.join(ROOT, 'content/stories', id + '.json');
const send = (res, code, body, type = 'application/json') => { res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store' }); res.end(type === 'application/json' ? JSON.stringify(body) : body); };
const readBody = req => new Promise(r => { let b = ''; req.on('data', c => { b += c; if (b.length > 2e6) req.destroy(); }); req.on('end', () => { try { r(JSON.parse(b || '{}')); } catch { r({}); } }); });

async function el(p, opts = {}) {
  const key = readEnv().ELEVENLABS_API_KEY; if (!key) return { status: 401, json: { detail: { message: 'Önce ElevenLabs API anahtarını kaydet.' } } };
  const r = await fetch('https://api.elevenlabs.io' + p, { ...opts, headers: { 'xi-api-key': key, 'Content-Type': 'application/json' } });
  let json = null; try { json = await r.json(); } catch {} return { status: r.status, json };
}
const errMsg = j => (j && j.detail && (j.detail.message || (typeof j.detail === 'string' ? j.detail : ''))) || 'Bilinmeyen hata';

// Tek seferde tek iş: ses ya da video üretimi
const job = { state: 'idle', what: '', id: '', progress: '', log: '' };
function runJob(what, id, args) {
  if (job.state === 'running') return false;
  Object.assign(job, { state: 'running', what, id, progress: 'Başlıyor…', log: '' });
  const p = spawn('node', args, { cwd: ROOT });
  const onData = d => { const s = d.toString(); job.log += s; const last = s.split(/[\r\n]+/).filter(Boolean).pop(); if (last) job.progress = last; };
  p.stdout.on('data', onData); p.stderr.on('data', onData);
  p.on('close', c => { job.state = c === 0 ? 'done' : 'error'; if (c !== 0) job.progress = (job.log.split('\n').find(l => /^(ElevenLabs|Error|.*gerekli)/.test(l)) || 'Hata oluştu').slice(0, 300); });
  return true;
}

const routes = {
  'GET /api/state': async () => { const e = readEnv(); return { hasKey: !!e.ELEVENLABS_API_KEY, keyHint: e.ELEVENLABS_API_KEY ? '…' + e.ELEVENLABS_API_KEY.slice(-4) : '', voiceId: e.ELEVENLABS_VOICE_ID || '', hasGemini: !!e.GEMINI_API_KEY, hasOpenai: !!e.OPENAI_API_KEY, imageProvider: e.IMAGE_PROVIDER || 'gemini', sesSaglayici: e.SES_SAGLAYICI || 'edge', model: e.ELEVENLABS_MODEL || 'eleven_v3', stability: +(e.VOICE_STABILITY ?? 0.5), similarity: +(e.VOICE_SIMILARITY ?? 0.8), style: +(e.VOICE_STYLE ?? 0.25) }; },
  'POST /api/settings': async (req, res, b) => { const p = {}; if (b.apiKey) p.ELEVENLABS_API_KEY = String(b.apiKey).trim(); if (b.geminiKey) p.GEMINI_API_KEY = String(b.geminiKey).trim(); if (b.openaiKey) p.OPENAI_API_KEY = String(b.openaiKey).trim(); if (b.sesSaglayici) p.SES_SAGLAYICI = b.sesSaglayici === 'elevenlabs' ? 'elevenlabs' : 'edge'; if (b.imageProvider) p.IMAGE_PROVIDER = b.imageProvider === 'openai' ? 'openai' : 'gemini';
    for (const [k, e] of [['voiceId', 'ELEVENLABS_VOICE_ID'], ['model', 'ELEVENLABS_MODEL'], ['stability', 'VOICE_STABILITY'], ['similarity', 'VOICE_SIMILARITY'], ['style', 'VOICE_STYLE']]) if (b[k] !== undefined && b[k] !== '') p[e] = String(b[k]).trim();
    writeEnv(p); return { ok: true }; },
  'GET /api/voices': async () => { const r = await el('/v1/voices'); if (r.status !== 200) return { error: errMsg(r.json), status: r.status };
    return { voices: r.json.voices.map(v => ({ id: v.voice_id, name: v.name, category: v.category, labels: Object.values(v.labels || {}).join(', '), preview: v.preview_url })) }; },
  'GET /api/shared': async (req, res, b, q) => { const u = new URLSearchParams({ language: 'tr', page_size: '30', sort: 'trending', ...(q.q ? { search: q.q } : {}), ...(q.use ? { use_cases: q.use } : {}) });
    const r = await el('/v1/shared-voices?' + u); if (r.status !== 200) return { error: errMsg(r.json), status: r.status };
    return { voices: (r.json.voices || []).map(v => ({ id: v.voice_id, owner: v.public_owner_id, name: v.name, desc: (v.description || '').slice(0, 140), labels: [v.gender, v.age, v.accent, v.use_case].filter(Boolean).join(', '), preview: v.preview_url })) }; },
  'POST /api/shared/add': async (req, res, b) => { if (!/^[\w-]+$/.test(b.owner || '') || !/^[\w-]+$/.test(b.voiceId || '')) return { error: 'Geçersiz ses' };
    const r = await el(`/v1/voices/add/${b.owner}/${b.voiceId}`, { method: 'POST', body: JSON.stringify({ new_name: b.name || 'EATrend ses' }) });
    if (r.status !== 200) return { error: errMsg(r.json), status: r.status }; writeEnv({ ELEVENLABS_VOICE_ID: r.json.voice_id }); return { ok: true, voiceId: r.json.voice_id }; },
  'GET /api/stories': async () => ({ stories: fs.readdirSync(path.join(ROOT, 'content/stories')).filter(f => f.endsWith('.json')).map(f => { const j = JSON.parse(fs.readFileSync(path.join(ROOT, 'content/stories', f), 'utf8')); return { id: f.slice(0, -5), baslik: j.baslik }; }) }),
  'GET /api/story': async (req, res, b, q) => idOk(q.id) && fs.existsSync(storyFile(q.id)) ? JSON.parse(fs.readFileSync(storyFile(q.id), 'utf8')) : { error: 'Bulunamadı' },
  'POST /api/story': async (req, res, b) => { if (!idOk(b.id) || !b.story || typeof b.story.metin !== 'string' || !Array.isArray(b.story.sahneler)) return { error: 'Geçersiz hikaye' };
    b.story.id = b.id; fs.writeFileSync(storyFile(b.id), JSON.stringify(b.story, null, 2)); return { ok: true }; },
  'POST /api/story/new': async (req, res, b) => { const id = (b.baslik || '').toLocaleLowerCase('tr').replace(/ğ/g, 'g').replace(/ü/g, 'u').replace(/ş/g, 's').replace(/ı/g, 'i').replace(/ö/g, 'o').replace(/ç/g, 'c').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 50);
    if (!id || fs.existsSync(storyFile(id))) return { error: 'Başlık boş ya da bu hikaye zaten var' };
    const s = { id, baslik: b.baslik, etiket: '#trend', tema: 'gece', kaynak: '', metin: 'Buraya hikayenin metnini yaz. [sakin] Duygu notlarını köşeli parantezle ekleyebilirsin. Takip et, yarın yeni bir trend.',
      sahneler: [{ tip: 'hook', kelime: 0, metin: b.baslik, vurgu: '' }, { tip: 'kapanis', ankraj: 'Takip et', metin: 'Yarın yeni bir trend', buton: 'Takip et' }] };
    fs.writeFileSync(storyFile(id), JSON.stringify(s, null, 2)); return { ok: true, id }; },
  'POST /api/voice': async (req, res, b) => idOk(b.id) && runJob('voice', b.id, ['voice/tts.js', b.id, ...(b.mock ? ['--mock'] : [])]) ? { ok: true } : { error: 'Başka bir iş sürüyor ya da geçersiz hikaye' },
  'POST /api/render': async (req, res, b) => idOk(b.id) && runJob('render', b.id, ['make.js', b.id, ...(b.mock ? ['--mock'] : [])]) ? { ok: true } : { error: 'Başka bir iş sürüyor ya da geçersiz hikaye' },
  'GET /api/dizi': async () => { const d = path.join(ROOT, 'content/series/alsat'); return { bible: JSON.parse(fs.readFileSync(path.join(d, 'bible.json'), 'utf8')), bolumler: fs.readdirSync(d).filter(f => /^\d+\.json$/.test(f)).map(f => +f.slice(0, -5)).sort((a, b) => a - b) }; },
  'POST /api/dizi/bible': async (req, res, b) => { const f = path.join(ROOT, 'content/series/alsat/bible.json'), cur = JSON.parse(fs.readFileSync(f, 'utf8'));
    for (const [k, v] of Object.entries(b.karakterler || {})) if (cur.karakterler[k]) { if (typeof v.ses === 'string' && /^[\w-]*$/.test(v.ses)) cur.karakterler[k].ses = v.ses; if (typeof v.tarif === 'string') cur.karakterler[k].tarif = v.tarif.slice(0, 600); }
    if (typeof b.stil === 'string') cur.stil = b.stil.slice(0, 800); fs.writeFileSync(f, JSON.stringify(cur, null, 2)); return { ok: true }; },
  'GET /api/dizi/bolum': async (req, res, b, q) => { const f = path.join(ROOT, 'content/series/alsat', String(+q.n).padStart(3, '0') + '.json'); return +q.n > 0 && fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, 'utf8')) : { error: 'Bölüm yok' }; },
  'POST /api/dizi/bolum': async (req, res, b) => { const n = +b.n; if (!(n > 0 && n < 1000) || !b.ep || !Array.isArray(b.ep.sahneler) || !b.ep.sahneler.length || !b.ep.sahneler.every(x => Array.isArray(x.satirlar) && x.satirlar.length && typeof x.mekan === 'string' && Array.isArray(x.kimler))) return { error: 'Geçersiz bölüm' };
    b.ep.dizi = 'alsat'; b.ep.bolum = n; fs.writeFileSync(path.join(ROOT, 'content/series/alsat', String(n).padStart(3, '0') + '.json'), JSON.stringify(b.ep, null, 2)); return { ok: true }; },
  'POST /api/dizi/job': async (req, res, b) => { const n = +b.n, m = b.mock ? ['--mock'] : []; if (!(n > 0 && n < 1000)) return { error: 'Geçersiz bölüm' };
    const cmd = { gorsel: ['dizi/gorsel.js', 'alsat', n, ...m, ...(b.force ? ['--force'] : [])], ses: ['dizi/ses.js', 'alsat', n, ...m], video: ['render/render-dizi.js', 'alsat', n], hepsi: ['make-dizi.js', 'alsat', n, ...m] }[b.kind];
    if (!cmd) return { error: 'Geçersiz iş' }; return runJob('dizi-' + b.kind, 'alsat-' + String(n).padStart(3, '0'), cmd.map(String)) ? { ok: true } : { error: 'Başka bir iş sürüyor' }; },
  'GET /api/job': async () => ({ state: job.state, what: job.what, id: job.id, progress: job.progress })
};

http.createServer(async (req, res) => {
  const u = new URL(req.url, 'http://x'), key = req.method + ' ' + u.pathname;
  try {
    if (routes[key]) { const b = req.method === 'POST' ? await readBody(req) : {}; return send(res, 200, await routes[key](req, res, b, Object.fromEntries(u.searchParams))); }
    let rel = u.pathname === '/' ? '/web/index.html' : u.pathname;
    if (!/^\/(web|out)\//.test(rel)) return send(res, 404, 'yok', 'text/plain');
    const f = path.normalize(path.join(ROOT, rel)); if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) return send(res, 404, 'yok', 'text/plain');
    const stat = fs.statSync(f), type = MIME[path.extname(f)] || 'application/octet-stream', range = req.headers.range;
    if (range) { const [s, e] = range.replace('bytes=', '').split('-'), a = +s, z = e ? +e : stat.size - 1;
      res.writeHead(206, { 'Content-Type': type, 'Content-Range': `bytes ${a}-${z}/${stat.size}`, 'Accept-Ranges': 'bytes', 'Content-Length': z - a + 1 }); return fs.createReadStream(f, { start: a, end: z }).pipe(res); }
    res.writeHead(200, { 'Content-Type': type, 'Content-Length': stat.size, 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-store' }); fs.createReadStream(f).pipe(res);
  } catch (e) { send(res, 500, { error: String(e.message || e) }); }
}).listen(PORT, '127.0.0.1', () => console.log(`\nEATrend Stüdyo hazır: http://localhost:${PORT}\n(kapatmak için bu pencerede Ctrl+C)`));
