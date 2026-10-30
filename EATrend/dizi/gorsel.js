// Bölümün her sahnesi için görsel üretir (Gemini ya da OpenAI). Kullanım: node dizi/gorsel.js <dizi> <bölüm> [--mock] [--force] [--sahne N]
const fs = require('fs'), path = require('path');
const { loadEnv, bible, episode, episodeId, outDir, requirePlaywright, ROOT } = require('../lib');
loadEnv();

function charText(b, kimler) { return kimler.map(k => `${b.karakterler[k].ad}: ${b.karakterler[k].tarif}`).join('. '); }
function scenePrompt(b, s) {
  return `${b.stil}. Characters (keep them exactly consistent): ${charText(b, s.kimler)}. Setting: ${s.mekan}. Action: ${s.aksiyon}. Leave the lower third of the frame calm for subtitles.`;
}

async function gemini(prompt, refs) {
  const key = process.env.GEMINI_API_KEY; if (!key) throw new Error('GEMINI_API_KEY gerekli (Stüdyo → Ayarlar) ya da --mock kullan');
  const model = process.env.GEMINI_IMAGE_MODEL || 'gemini-2.5-flash-image';
  const parts = [...refs.map(r => ({ inlineData: { mimeType: 'image/png', data: fs.readFileSync(r).toString('base64') } })), { text: (refs.length ? 'Use the exact same characters as in the reference images. ' : '') + prompt }];
  const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
    method: 'POST', headers: { 'x-goog-api-key': key, 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents: [{ parts }], generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio: '9:16' } } })
  });
  const j = await r.json(); if (!r.ok) throw new Error('Gemini ' + r.status + ': ' + JSON.stringify(j.error || j).slice(0, 300));
  const part = (j.candidates?.[0]?.content?.parts || []).find(p => p.inlineData || p.inline_data);
  if (!part) throw new Error('Gemini görsel döndürmedi: ' + JSON.stringify(j).slice(0, 300));
  return Buffer.from((part.inlineData || part.inline_data).data, 'base64');
}
async function openai(prompt) {
  const key = process.env.OPENAI_API_KEY; if (!key) throw new Error('OPENAI_API_KEY gerekli (Stüdyo → Ayarlar) ya da --mock kullan');
  const r = await fetch('https://api.openai.com/v1/images/generations', { method: 'POST', headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: process.env.OPENAI_IMAGE_MODEL || 'gpt-image-1', prompt, size: '1024x1536', n: 1 }) });
  const j = await r.json(); if (!r.ok) throw new Error('OpenAI ' + r.status + ': ' + JSON.stringify(j.error || j).slice(0, 300));
  return Buffer.from(j.data[0].b64_json, 'base64');
}

// Deneme için sahte görsel: sahne metnini gösteren renkli kart
async function mockImages(items) {
  const { chromium } = requirePlaywright(); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const it of items) {
    const hue = (it.i * 55 + 200) % 360;
    await p.setContent(`<body style="margin:0;width:1080px;height:1920px;background:linear-gradient(160deg,hsl(${hue},55%,28%),hsl(${hue + 40},60%,12%));font:700 54px sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:center;padding:90px;box-sizing:border-box;gap:30px">
      <div style="font-size:40px;opacity:.6">SAHTE GÖRSEL · SAHNE ${it.i + 1}</div><div>${it.text.replace(/</g, '&lt;')}</div></body>`);
    await p.screenshot({ path: it.file });
  }
  await b.close();
}

(async () => {
  const [dizi, n] = process.argv.slice(2), mock = process.argv.includes('--mock') || process.argv.includes('--mock-gorsel'), force = process.argv.includes('--force');
  const only = process.argv.includes('--sahne') ? +process.argv[process.argv.indexOf('--sahne') + 1] - 1 : null;
  if (!dizi || !n) { console.error('kullanım: node dizi/gorsel.js <dizi> <bölüm> [--mock] [--force] [--sahne N]'); process.exit(1); }
  const b = bible(dizi), ep = episode(dizi, n), dir = outDir(episodeId(dizi, n));
  const todo = ep.sahneler.map((s, i) => ({ i, s, file: path.join(dir, `img-${i + 1}.png`) })).filter(x => (only === null || only === x.i) && (force || !fs.existsSync(x.file)));
  if (!todo.length) { console.log('Görseller zaten hazır (yeniden için --force)'); return; }
  if (mock) { await mockImages(todo.map(x => ({ ...x, text: x.s.aksiyon }))); console.log(todo.length + ' sahte görsel'); return; }
  const provider = process.env.IMAGE_PROVIDER || 'gemini', refDir = path.join(ROOT, 'out', 'seri-' + dizi); fs.mkdirSync(refDir, { recursive: true });
  const gen = provider === 'openai' ? (p) => openai(p) : (p, refs) => gemini(p, refs);
  // Gemini: karakter tutarlılığı için önce her karakterin referans görselini üret ve sonraki sahnelerde kullan
  const refOf = {};
  if (provider !== 'openai') for (const k of new Set(todo.flatMap(x => x.s.kimler))) {
    const f = path.join(refDir, `ref-${k}.png`); refOf[k] = f;
    if (!fs.existsSync(f)) { process.stdout.write(`Referans: ${b.karakterler[k].ad}\n`); fs.writeFileSync(f, await gemini(`${b.stil}. Character reference, full body, front view, neutral plain light background, single character: ${b.karakterler[k].tarif}`, [])); }
  }
  for (const x of todo) {
    process.stdout.write(`Sahne ${x.i + 1}/${ep.sahneler.length}\n`);
    fs.writeFileSync(x.file, await gen(scenePrompt(b, x.s), x.s.kimler.map(k => refOf[k]).filter(Boolean)));
  }
  console.log('Görseller hazır');
})().catch(e => { console.error(e.message); process.exit(1); });
