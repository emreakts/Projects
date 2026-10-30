// Satırları karakterin kendi sesiyle okutur, kelime zamanlarını ve sahne aralıklarını çıkarır.
// Kullanım: node dizi/ses.js <dizi> <bölüm> [--mock]
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const { loadEnv, bible, episode, episodeId, outDir } = require('../lib');
loadEnv();
const GAP_LINE = 0.22, TAIL_SCENE = 0.35;
const plain = t => t.replace(/\[[^\]]*\]/g, ' ').replace(/\s+/g, ' ').trim();

function wordsFromAlignment(a) {
  const words = []; let cur = null, inTag = false;
  a.characters.forEach((ch, i) => {
    if (ch === '[') inTag = true;
    if (!inTag && !/\s/.test(ch)) { if (!cur) cur = { w: '', start: a.character_start_times_seconds[i] }; cur.w += ch; cur.end = a.character_end_times_seconds[i]; }
    else if (!inTag && cur) { words.push(cur); cur = null; }
    if (ch === ']') { inTag = false; if (cur) { words.push(cur); cur = null; } }
  });
  if (cur) words.push(cur); return words;
}
function mockLine(text, file) {
  let t = 0.1; const words = plain(text).split(' ').map(w => { const s = t; t += 0.17 + w.length * 0.04; const e = t; t += /[.,!?]$/.test(w) ? 0.35 : 0.04; return { w, start: s, end: e }; });
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'lavfi', '-i', `anoisesrc=d=${(t + 0.2).toFixed(2)}:c=brown:a=0.02`, '-f', 'wav', file]); return { words, file, fmt: 'wav' };
}
async function realLine(text, voice, file) {
  const key = process.env.ELEVENLABS_API_KEY; if (!key || !voice) throw new Error('ELEVENLABS_API_KEY ve karakterin ses ID\'si gerekli (Stüdyo → Ses) ya da --mock kullan');
  const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice}/with-timestamps`, { method: 'POST', headers: { 'xi-api-key': key, 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, model_id: process.env.ELEVENLABS_MODEL || 'eleven_v3', voice_settings: { stability: +(process.env.VOICE_STABILITY ?? 0.5), similarity_boost: +(process.env.VOICE_SIMILARITY ?? 0.8), style: +(process.env.VOICE_STYLE ?? 0.25), use_speaker_boost: true } }) });
  if (!r.ok) throw new Error('ElevenLabs ' + r.status + ': ' + (await r.text()).slice(0, 300));
  const j = await r.json(); fs.writeFileSync(file, Buffer.from(j.audio_base64, 'base64')); return { words: wordsFromAlignment(j.alignment), file, fmt: 'mp3' };
}
const dur = (f, fmt) => parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', '-f', fmt, f]).toString());

(async () => {
  const [dizi, n] = process.argv.slice(2), mock = process.argv.includes('--mock');
  if (!dizi || !n) { console.error('kullanım: node dizi/ses.js <dizi> <bölüm> [--mock]'); process.exit(1); }
  const b = bible(dizi), ep = episode(dizi, n), dir = outDir(episodeId(dizi, n)), tl = { words: [], scenes: [] }, inputs = [];
  let cursor = 0.0, total = ep.sahneler.reduce((a, s) => a + s.satirlar.length, 0), done = 0;
  for (let si = 0; si < ep.sahneler.length; si++) {
    const sc = ep.sahneler[si], sceneStart = cursor;
    for (let li = 0; li < sc.satirlar.length; li++) {
      const l = sc.satirlar[li], ch = b.karakterler[l.k]; if (!ch) throw new Error('Bilinmeyen karakter: ' + l.k);
      const voice = ch.ses || process.env.ELEVENLABS_VOICE_ID, file = path.join(dir, `line-${si + 1}-${li + 1}.${mock ? 'wav' : 'mp3'}`);
      const r = mock ? mockLine(l.m, file) : await realLine(l.m, voice, file);
      const first = r.words[0].start, shift = cursor - first + 0.05; // satırın ilk kelimesi imleçte başlasın
      for (const w of r.words) tl.words.push({ w: w.w, start: +(w.start + shift).toFixed(3), end: +(w.end + shift).toFixed(3), k: l.k, sc: si });
      inputs.push({ file, fmt: r.fmt, delay: Math.max(0, shift) });
      cursor = tl.words[tl.words.length - 1].end + GAP_LINE; process.stdout.write(`\rSatır ${++done}/${total}`);
    }
    const end = tl.words[tl.words.length - 1].end + TAIL_SCENE; tl.scenes.push({ start: si === 0 ? 0 : sceneStart, end }); cursor = end;
  }
  tl.duration = +(tl.scenes[tl.scenes.length - 1].end + 0.4).toFixed(3);
  const f = inputs.map((x, i) => `[${i}:a]adelay=${Math.round(x.delay * 1000)}:all=1[a${i}]`).join(';') + ';' + inputs.map((_, i) => `[a${i}]`).join('') + `amix=inputs=${inputs.length}:normalize=0:duration=longest[o]`;
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...inputs.flatMap(x => ['-i', x.file]), '-filter_complex', f, '-map', '[o]', '-ar', '44100', path.join(dir, 'voice.wav')]);
  fs.writeFileSync(path.join(dir, 'timeline.json'), JSON.stringify(tl, null, 1));
  console.log(`\n${episodeId(dizi, n)}: ${tl.words.length} kelime, ${tl.duration.toFixed(1)} sn`);
})().catch(e => { console.error(e.message); process.exit(1); });
