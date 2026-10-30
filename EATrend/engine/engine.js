// EATrend çizim motoru v2: modern, koyu tema, kinetik tipografi. renderAt(t) deterministiktir.
const W = 1080, H = 1920;
const cv = document.getElementById('c'), g = cv.getContext('2d');
const C = { bg1: '#0a0d1a', bg2: '#1a1040', ink: '#f5f7ff', mute: 'rgba(245,247,255,.62)', lime: '#c6ff3d', pink: '#ff3d8b', cyan: '#3de0ff', card: 'rgba(255,255,255,.07)', stroke: 'rgba(255,255,255,.14)' };
const FONT = '"SF Pro Display","Helvetica Neue",Inter,Arial,sans-serif';
let story = null, words = [], duration = 0, scenes = [];

const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const ease = p => { p = clamp(p); return 1 - Math.pow(1 - p, 3); };
const back = p => { p = clamp(p); const c = 1.70158; return 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); };
const norm = s => s.toLocaleLowerCase('tr').replace(/[^\p{L}\p{N}]/gu, '');

function rr(x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
function text(s, x, y, size, color, o = {}) {
  g.font = `${o.w || 800} ${size}px ${FONT}`; g.textAlign = o.a || 'center'; g.textBaseline = 'middle';
  g.fillStyle = color; if (o.glow) { g.shadowColor = o.glow; g.shadowBlur = 40; }
  g.fillText(s, x, y); g.shadowBlur = 0;
}
function wrap(s, maxW, size, w = 800) {
  g.font = `${w} ${size}px ${FONT}`; const out = []; let line = '';
  for (const wd of s.split(' ')) { const t = line ? line + ' ' + wd : wd; if (g.measureText(t).width > maxW && line) { out.push(line); line = wd; } else line = t; }
  if (line) out.push(line); return out;
}

function background(t) {
  const gr = g.createLinearGradient(0, 0, W, H); gr.addColorStop(0, C.bg1); gr.addColorStop(1, C.bg2);
  g.fillStyle = gr; g.fillRect(0, 0, W, H);
  const blobs = [[0.2, 0.25, 520, C.pink, 0.9, 0.7], [0.85, 0.55, 600, C.cyan, 0.6, 1.1], [0.3, 0.9, 560, C.lime, 0.5, 0.5]];
  blobs.forEach(([bx, by, r, col, sp, ph], i) => {
    const x = (bx + Math.sin(t * 0.35 * sp + ph) * 0.12) * W, y = (by + Math.cos(t * 0.3 * sp + ph * 2) * 0.08) * H;
    const rg = g.createRadialGradient(x, y, 0, x, y, r); rg.addColorStop(0, col + '55'); rg.addColorStop(1, col + '00');
    g.fillStyle = rg; g.fillRect(0, 0, W, H);
  });
  g.strokeStyle = 'rgba(255,255,255,.035)'; g.lineWidth = 2;
  for (let x = 0; x <= W; x += 90) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, H); g.stroke(); }
  for (let y = ((t * 20) % 90); y <= H; y += 90) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }
}

function chrome(t, prog) {
  rr(60, 90, 250, 78, 39); g.fillStyle = C.card; g.fill(); g.strokeStyle = C.stroke; g.lineWidth = 2; g.stroke();
  g.fillStyle = C.lime; g.beginPath(); g.arc(104, 129, 10 + Math.sin(t * 4) * 2, 0, 7); g.fill();
  text('EATrend', 135, 130, 38, C.ink, { a: 'left' });
  if (story.etiket) { g.font = `700 34px ${FONT}`; const tw = g.measureText(story.etiket).width + 56; rr(W - 60 - tw, 90, tw, 78, 39); g.fillStyle = C.lime; g.fill(); text(story.etiket, W - 60 - tw / 2, 130, 34, '#0a0d1a', { w: 800 }); }
  rr(60, 1830, W - 120, 8, 4); g.fillStyle = 'rgba(255,255,255,.15)'; g.fill();
  rr(60, 1830, Math.max(8, (W - 120) * prog), 8, 4); g.fillStyle = C.lime; g.fill();
}

// --- sahne tipleri (lt: sahne başlangıcından beri geçen saniye)
function sHook(s, lt, T) {
  const lines = wrap(s.metin, 900, 124), accent = norm(s.vurgu || '');
  let k = 0, y = 760 - lines.length * 80;
  lines.forEach((ln, li) => {
    const ws = ln.split(' '); g.font = `900 124px ${FONT}`;
    const sp = g.measureText(' ').width, widths = ws.map(w => g.measureText(w).width);
    let x = (W - (widths.reduce((a, b) => a + b, 0) + sp * (ws.length - 1))) / 2;
    ws.forEach((w, i) => {
      const p = back((lt - k * 0.09) / 0.45), a = clamp((lt - k * 0.09) / 0.25);
      g.save(); g.globalAlpha = a; g.translate(x + widths[i] / 2, y + 80 * li + (1 - p) * 60); g.scale(0.7 + 0.3 * p, 0.7 + 0.3 * p);
      text(w, 0, 0, 124, accent && norm(w) === accent ? C.lime : C.ink, { w: 900, glow: accent && norm(w) === accent ? C.lime : 0 }); g.restore();
      x += widths[i] + sp; k++;
    });
    y += 70;
  });
}
function sStat(s, lt) {
  const p = ease(lt / 1.2), v = (s.deger * p), cx = W / 2, cy = 800;
  g.lineWidth = 36; g.lineCap = 'round'; g.strokeStyle = 'rgba(255,255,255,.1)'; g.beginPath(); g.arc(cx, cy, 330, 0, 7); g.stroke();
  const ring = g.createLinearGradient(cx - 330, cy, cx + 330, cy); ring.addColorStop(0, C.pink); ring.addColorStop(1, C.lime);
  g.strokeStyle = ring; g.beginPath(); g.arc(cx, cy, 330, -Math.PI / 2, -Math.PI / 2 + 2 * Math.PI * clamp((s.oran ?? 0.75) * p), false); g.stroke();
  text(Number.isInteger(s.deger) ? Math.round(v) : v.toFixed(1), cx, cy - 20, 220, C.ink, { w: 900, glow: C.lime });
  text(s.birim || '', cx, cy + 130, 64, C.lime, { w: 800 });
  g.globalAlpha = ease((lt - 0.3) / 0.5); wrap(s.etiket || '', 820, 56, 700).forEach((l, i) => text(l, cx, 1230 + i * 74, 56, C.mute, { w: 700 })); g.globalAlpha = 1;
}
function sListe(s, lt, T) {
  const n = s.maddeler.length, top = 560;
  if (s.baslik) text(s.baslik, W / 2, 450, 68, C.mute, { w: 700 });
  s.maddeler.forEach((m, i) => {
    const at = m.t ?? i * 0.9, p = back((lt - at) / 0.5); if (lt < at) return;
    const y = top + i * 220, x = 80 + (1 - ease((lt - at) / 0.4)) * 400;
    g.save(); g.globalAlpha = clamp((lt - at) / 0.3); rr(x, y, W - 160, 190, 40); g.fillStyle = C.card; g.fill(); g.strokeStyle = C.stroke; g.lineWidth = 2; g.stroke();
    g.beginPath(); g.arc(x + 95, y + 95, 52 * (0.8 + 0.2 * p), 0, 7); g.fillStyle = [C.lime, C.pink, C.cyan][i % 3]; g.fill();
    text(String(i + 1), x + 95, y + 98, 56, '#0a0d1a', { w: 900 });
    wrap(m.m, W - 160 - 230, 56, 800).slice(0, 2).forEach((l, li, arr) => text(l, x + 180, y + 95 + (li - (arr.length - 1) / 2) * 66, 56, C.ink, { a: 'left', w: 800 }));
    g.restore();
  });
}
function sBar(s, lt) {
  const max = Math.max(...s.veri.map(v => v.deger)), n = s.veri.length, bw = 700;
  if (s.baslik) text(s.baslik, W / 2, 450, 68, C.mute, { w: 700 });
  s.veri.forEach((v, i) => {
    const at = i * 0.5, p = ease((lt - at) / 0.9), y = 600 + i * 210;
    text(v.etiket, 90, y, 52, C.ink, { a: 'left', w: 700 });
    rr(90, y + 45, bw + 120, 70, 35); g.fillStyle = 'rgba(255,255,255,.08)'; g.fill();
    const w = Math.max(70, (bw + 120) * (v.deger / max) * p); rr(90, y + 45, w, 70, 35);
    const gr = g.createLinearGradient(90, 0, 90 + w, 0); gr.addColorStop(0, C.pink); gr.addColorStop(1, [C.lime, C.cyan, C.lime][i % 3]); g.fillStyle = gr; g.fill();
    text((v.birim ? Math.round(v.deger * p) + v.birim : Math.round(v.deger * p)), 90 + w - 30, y + 80, 40, '#0a0d1a', { a: 'right', w: 900 });
  });
}
function sKapanis(s, lt) {
  const p = back(lt / 0.6);
  g.save(); g.translate(W / 2, 760); g.scale(p, p);
  wrap(s.metin, 880, 110).forEach((l, i, a) => text(l, 0, (i - (a.length - 1) / 2) * 130, 110, C.ink, { w: 900 }));
  g.restore();
  const bp = back((lt - 0.5) / 0.5); if (lt > 0.5) { g.save(); g.translate(W / 2, 1180); g.scale(bp, bp); rr(-260, -60, 520, 120, 60); g.fillStyle = C.lime; g.fill(); text(s.buton || 'Takip et', 0, 4, 56, '#0a0d1a', { w: 900 }); g.restore(); }
}
const TYPES = { hook: sHook, stat: sStat, liste: sListe, bar: sBar, kapanis: sKapanis };

function subtitles(wi) {
  g.font = `800 68px ${FONT}`;
  const wd = w => g.measureText(w.w + ' ').width; let grp = 0, n;
  const take = a => { let c = 0, s = 0; while (a + c < words.length && c < 4 && (c === 0 || s + wd(words[a + c]) <= 900)) { s += wd(words[a + c]); c++; } return c; };
  while (true) { n = take(grp); if (wi < grp + n) break; grp += n; }
  const chunk = words.slice(grp, grp + n), ws = chunk.map(wd), tot = ws.reduce((a, b) => a + b, 0);
  rr((W - tot) / 2 - 40, 1565, tot + 80, 130, 65); g.fillStyle = 'rgba(10,13,26,.72)'; g.fill(); g.strokeStyle = C.stroke; g.lineWidth = 2; g.stroke();
  let x = (W - tot) / 2; g.textAlign = 'left';
  chunk.forEach((w, k) => { g.fillStyle = grp + k === wi ? C.lime : C.ink; g.font = `800 68px ${FONT}`; g.fillText(w.w, x, 1632); x += ws[k]; });
}

function renderAt(t) {
  const cur = words.findIndex(w => w.start <= t && t < w.end);
  const wi = cur !== -1 ? cur : (t >= duration ? words.length - 1 : Math.max(0, words.findIndex(w => w.end > t)));
  background(t); chrome(t, clamp(t / duration));
  let sc = scenes[0]; for (const s of scenes) if (t >= s.t0) sc = s;
  const lt = Math.max(0, t - sc.t0), prev = scenes[scenes.indexOf(sc) - 1];
  g.save(); const fade = clamp(lt / 0.25); g.globalAlpha = fade; g.translate(0, (1 - ease(lt / 0.35)) * 40);
  (TYPES[sc.tip] || sHook)(sc, lt); g.restore();
  subtitles(wi);
}

// Sahne başlangıcı: kelime indeksi (kelime) ya da cümle (ankraj) ile verilir
function resolve(sc) {
  if (sc.ankraj) {
    const a = sc.ankraj.split(/\s+/).map(norm);
    for (let i = 0; i < words.length; i++) if (a.every((x, k) => words[i + k] && norm(words[i + k].w) === x)) return words[i].start;
    console.warn('ankraj bulunamadı: ' + sc.ankraj);
  }
  return (words[sc.kelime || 0] || words[0]).start;
}
window.loadStory = (s, ws) => { story = s; words = ws; duration = ws[ws.length - 1].end; scenes = s.sahneler.map(sc => ({ ...sc, t0: resolve(sc) })).sort((a, b) => a.t0 - b.t0); };
window.renderAt = renderAt; window.getDuration = () => duration;
