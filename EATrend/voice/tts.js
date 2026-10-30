// Metni sese çevirir, kelime zamanlarını çıkarır, uzun boşlukları kısaltır.
// Kullanım: node voice/tts.js <storyId> [--mock]
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const { loadEnv, story, outDir } = require('../lib');
loadEnv();
const MAX_GAP = 0.5, KEEP_GAP = 0.3;

// "[üzgün] Merhaba dünya." -> kelime listesi (etiketler sese gider, altyazıya girmez)
const plainText = t => t.replace(/\[[^\]]*\]/g, ' ').replace(/\s+/g, ' ').trim();

function wordsFromAlignment(a) {
  const words = []; let cur = null, inTag = false;
  a.characters.forEach((ch, i) => {
    if (ch === '[') inTag = true;
    if (!inTag && !/\s/.test(ch)) {
      if (!cur) cur = { w: '', start: a.character_start_times_seconds[i] };
      cur.w += ch; cur.end = a.character_end_times_seconds[i];
    } else if (!inTag && cur) { words.push(cur); cur = null; }
    if (ch === ']') { inTag = false; if (cur) { words.push(cur); cur = null; } }
  });
  if (cur) words.push(cur);
  return words;
}

function mockWords(text) {
  let t = 0.2; return plainText(text).split(' ').map(w => {
    const s = t; t += 0.18 + w.length * 0.04; const e = t;
    t += /[.,!?]$/.test(w) ? 0.45 : 0.04; return { w, start: s, end: e };
  });
}

async function elevenlabs(text) {
  const key = process.env.ELEVENLABS_API_KEY, voice = process.env.ELEVENLABS_VOICE_ID;
  if (!key || !voice) throw new Error('ELEVENLABS_API_KEY ve ELEVENLABS_VOICE_ID gerekli (.env) ya da --mock kullan');
  const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice}/with-timestamps`, {
    method: 'POST', headers: { 'xi-api-key': key, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text, model_id: process.env.ELEVENLABS_MODEL || 'eleven_v3',
      voice_settings: { stability: +(process.env.VOICE_STABILITY ?? 0.5), similarity_boost: +(process.env.VOICE_SIMILARITY ?? 0.8), style: +(process.env.VOICE_STYLE ?? 0.25), use_speaker_boost: true }
    })
  });
  if (!r.ok) throw new Error('ElevenLabs ' + r.status + ': ' + (await r.text()).slice(0, 300));
  const j = await r.json();
  return { audio: Buffer.from(j.audio_base64, 'base64'), words: wordsFromAlignment(j.alignment) };
}

// Kelimeler arası MAX_GAP'ten uzun sessizlikleri KEEP_GAP'e indirir; ses ve zamanlar birlikte kayar.
function tightenGaps(words, rawAudio, outWav, totalDur) {
  const keep = []; let from = 0, shift = 0; const out = [];
  words.forEach((w, i) => {
    const prevEnd = i ? words[i - 1].end : 0, gap = w.start - prevEnd;
    if (i && gap > MAX_GAP) {
      const cut = gap - KEEP_GAP;
      keep.push([from, prevEnd + KEEP_GAP / 2]); from = w.start - KEEP_GAP / 2; shift += cut;
    }
    out.push({ w: w.w, start: +(w.start - shift).toFixed(3), end: +(w.end - shift).toFixed(3) });
  });
  keep.push([from, totalDur]);
  const f = keep.map((k, i) => `[0:a]atrim=${k[0].toFixed(3)}:${k[1].toFixed(3)},asetpts=PTS-STARTPTS[a${i}]`).join(';')
    + ';' + keep.map((_, i) => `[a${i}]`).join('') + `concat=n=${keep.length}:v=0:a=1[o]`;
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', rawAudio, '-filter_complex', f, '-map', '[o]', '-ar', '44100', outWav]);
  return out;
}

(async () => {
  const id = process.argv[2], mock = process.argv.includes('--mock');
  if (!id) { console.error('kullanım: node voice/tts.js <storyId> [--mock]'); process.exit(1); }
  const s = story(id), dir = outDir(id), raw = path.join(dir, 'raw.audio');
  let words;
  if (mock) {
    words = mockWords(s.metin);
    const dur = words[words.length - 1].end + 0.6;
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anoisesrc=d=' + dur + ':c=brown:a=0.02', '-f', 'wav', raw]);
  } else {
    const r = await elevenlabs(s.metin); fs.writeFileSync(raw, r.audio); words = r.words;
  }
  const dur = parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', '-f', mock ? 'wav' : 'mp3', raw]).toString());
  const tight = tightenGaps(words, raw, path.join(dir, 'voice.wav'), dur);
  fs.writeFileSync(path.join(dir, 'words.json'), JSON.stringify(tight, null, 1));
  console.log(`${id}: ${tight.length} kelime, ${tight[tight.length - 1].end.toFixed(1)} sn`);
})().catch(e => { console.error(e.message); process.exit(1); });
