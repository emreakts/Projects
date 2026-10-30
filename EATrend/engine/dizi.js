// Dizi motoru: tam ekran görsel + yavaş kamera hareketi + konuşan karakterin altyazısı + kasa sayacı.
const W = 1080, H = 1920, cv = document.getElementById('c'), g = cv.getContext('2d');
const FONT = '"SF Pro Display","Helvetica Neue",Inter,Arial,sans-serif';
let st, bible, tl, imgs = [], hasKasa = false;
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const ease = p => 1 - Math.pow(1 - clamp(p), 3), back = p => { p = clamp(p); const c = 1.70158; return 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); };
const rr = (x, y, w, h, r) => { g.beginPath(); g.roundRect(x, y, w, h, r); };
const fmt = n => Math.round(n).toLocaleString('tr-TR');
function text(s, x, y, size, color, o = {}) { g.font = `${o.w || 800} ${size}px ${FONT}`; g.textAlign = o.a || 'center'; g.textBaseline = 'middle'; g.fillStyle = color; g.fillText(s, x, y); }
function wrap(s, maxW, size, w = 900) { g.font = `${w} ${size}px ${FONT}`; const out = []; let line = ''; for (const wd of s.split(' ')) { const t = line ? line + ' ' + wd : wd; if (g.measureText(t).width > maxW && line) { out.push(line); line = wd; } else line = t; } if (line) out.push(line); return out; }

function drawImage(i, lt, dur, alpha = 1) {
  const img = imgs[i]; if (!img) { g.fillStyle = '#111'; g.fillRect(0, 0, W, H); return; }
  const p = clamp(lt / Math.max(dur, 1)), dir = i % 2 ? -1 : 1, zoom = 1.05 + 0.1 * p, s = Math.max(W / img.width, H / img.height) * zoom;
  const w = img.width * s, h = img.height * s, x = (W - w) / 2 + dir * (p - 0.5) * 60, y = (H - h) / 2 - (p - 0.5) * 50;
  g.globalAlpha = alpha; g.drawImage(img, x, y, w, h); g.globalAlpha = 1;
}
function kasaAt(t, si) {
  let cur = null; for (let i = 0; i <= si; i++) if (st.sahneler[i].kasa) cur = st.sahneler[i].kasa.once;
  const k = st.sahneler[si].kasa; if (!k) return { v: cur, d: 0 };
  const sc = tl.scenes[si], p = ease((t - (sc.start + (sc.end - sc.start) * 0.35)) / 0.9);
  return { v: k.once + (k.sonra - k.once) * p, d: (k.sonra - k.once) * p };
}
function chrome(t, si) {
  rr(48, 84, 330, 84, 42); g.fillStyle = 'rgba(0,0,0,.55)'; g.fill();
  text(bible.kisa, 48 + 36, 126, 40, '#ffb547', { a: 'left', w: 900 });
  g.font = `900 40px ${FONT}`; const w = g.measureText(bible.kisa).width; text('PART ' + st.bolum, 48 + 36 + w + 18, 126, 40, '#fff', { a: 'left', w: 800 });
  if (hasKasa) {
    const { v, d } = kasaAt(t, si); if (v === null) return;
    rr(W - 48 - 480, 84, 480, 84, 42); g.fillStyle = 'rgba(0,0,0,.55)'; g.fill();
    text('KASA', W - 48 - 450, 126, 28, 'rgba(255,255,255,.6)', { a: 'left', w: 800 }); text(fmt(v) + ' TL', W - 48 - 30, 126, 40, '#fff', { a: 'right', w: 900 });
    if (Math.abs(d) > 1) { const up = d > 0, label = (up ? '+' : '−') + fmt(Math.abs(d)) + ' TL'; rr(W - 48 - 300, 180, 300, 66, 33); g.fillStyle = up ? '#16a34a' : '#dc2626'; g.fill(); text(label, W - 48 - 150, 214, 34, '#fff', { w: 900 }); }
  }
}
function title(t) {
  if (t > 2.4) return; const a = t < 0.2 ? t / 0.2 : t > 2 ? 1 - (t - 2) / 0.4 : 1, p = back(t / 0.5);
  g.fillStyle = `rgba(0,0,0,${0.45 * a})`; g.fillRect(0, 0, W, H); g.save(); g.globalAlpha = a; g.translate(W / 2, 820); g.scale(0.85 + 0.15 * p, 0.85 + 0.15 * p);
  const ls = wrap(st.baslik, 900, 96); ls.forEach((l, i) => { g.lineWidth = 16; g.strokeStyle = '#000'; g.lineJoin = 'round'; g.font = `900 96px ${FONT}`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.strokeText(l, 0, (i - (ls.length - 1) / 2) * 112); text(l, 0, (i - (ls.length - 1) / 2) * 112, 96, '#fff', { w: 900 }); });
  g.restore();
}
function subtitles(wi) {
  const cur = tl.words[wi], same = i => tl.words[i] && tl.words[i].k === cur.k && tl.words[i].sc === cur.sc;
  let a = wi; while (same(a - 1)) a--; // konuşmanın başı
  let grp = a; g.font = `900 78px ${FONT}`;
  const wd = w => g.measureText(w.w + ' ').width; const take = s => { let c = 0, sum = 0; while (same(s + c) && c < 4 && (c === 0 || sum + wd(tl.words[s + c]) <= 900)) { sum += wd(tl.words[s + c]); c++; } return c; };
  let n; while (true) { n = take(grp); if (wi < grp + n) break; grp += n; }
  const ch = bible.karakterler[cur.k], chunk = tl.words.slice(grp, grp + n), ws = chunk.map(wd), tot = ws.reduce((x, y) => x + y, 0), y = 1480;
  g.font = `800 38px ${FONT}`; const nw = g.measureText(ch.ad).width + 52; rr((W - nw) / 2, y - 150, nw, 62, 31); g.fillStyle = ch.renk; g.fill(); text(ch.ad, W / 2, y - 119, 38, '#101010', { w: 900 });
  let x = (W - tot) / 2; chunk.forEach((w, k) => { g.font = `900 78px ${FONT}`; g.textAlign = 'left'; g.textBaseline = 'middle'; g.lineWidth = 16; g.lineJoin = 'round'; g.strokeStyle = '#000'; g.strokeText(w.w, x, y); g.fillStyle = grp + k === wi ? ch.renk : '#fff'; g.fillText(w.w, x, y); x += ws[k]; });
}
function renderAt(t) {
  let si = tl.scenes.findIndex((s, i) => t < s.end || i === tl.scenes.length - 1); const sc = tl.scenes[si], lt = t - sc.start;
  g.fillStyle = '#000'; g.fillRect(0, 0, W, H);
  if (si > 0 && lt < 0.3) drawImage(si - 1, tl.scenes[si - 1].end - tl.scenes[si - 1].start, tl.scenes[si - 1].end - tl.scenes[si - 1].start);
  drawImage(si, lt, sc.end - sc.start, si > 0 ? clamp(lt / 0.3) : 1);
  const v = g.createLinearGradient(0, 0, 0, H); v.addColorStop(0, 'rgba(0,0,0,.45)'); v.addColorStop(0.25, 'rgba(0,0,0,0)'); v.addColorStop(0.6, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.6)'); g.fillStyle = v; g.fillRect(0, 0, W, H);
  chrome(t, si); title(t);
  let wi = tl.words.findIndex(w => w.start <= t && t < w.end); if (wi === -1) { const nx = tl.words.findIndex(w => w.start > t); wi = nx === -1 ? tl.words.length - 1 : nx; }
  if (t >= 2.4 || wi >= 0) if (t >= 2.4) subtitles(wi);
}
window.loadEpisode = async (story, b, timeline, urls) => {
  st = story; bible = b; tl = timeline; hasKasa = story.sahneler.some(s => s.kasa);
  imgs = await Promise.all(urls.map(u => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.onerror = () => r(null); i.src = u; })));
};
window.renderAt = renderAt; window.getDuration = () => tl.duration;
