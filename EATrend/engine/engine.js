// Deterministik çizim motoru: renderAt(t) her saniye için aynı kareyi çizer.
const W = 1080, H = 1920;
const cv = document.getElementById('c'), g = cv.getContext('2d');
const INK = '#2b2118', GOLD = '#d4a017';
let story = null, words = [], duration = 0;

function rnd(seed) { const x = Math.sin(seed * 127.1) * 43758.5453; return x - Math.floor(x); }
// Elle çizilmiş hissi: sabit tohumlu hafif titreme
function wob(s, a) { return (rnd(s) - 0.5) * a; }
function line(x1, y1, x2, y2, seed, w = 5) {
  g.lineWidth = w; g.lineCap = 'round'; g.strokeStyle = INK; g.beginPath();
  const mx = (x1 + x2) / 2 + wob(seed, 6), my = (y1 + y2) / 2 + wob(seed + 1, 6);
  g.moveTo(x1, y1); g.quadraticCurveTo(mx, my, x2, y2); g.stroke();
}
const ease = p => p < 0 ? 0 : p > 1 ? 1 : p * p * (3 - 2 * p);

const POSES = {
  dur:    { armL: [-0.5, 0.2], armR: [0.5, 0.2], legL: [-0.2, 0], legR: [0.2, 0] },
  yuru:   null, // zamana göre hesaplanır
  yukari: { armL: [-0.6, -0.4], armR: [0.6, -0.4], legL: [-0.2, 0], legR: [0.2, 0], bak: -1 },
  egil:   { armL: [-0.2, 0.9], armR: [0.4, 0.8], legL: [-0.3, 0], legR: [0.3, 0], egil: 0.35 }
};

function figure(x, y, poz, t, seed) {
  let p = POSES[poz] || POSES.dur;
  if (poz === 'yuru') {
    const s = Math.sin(t * 6) * 0.5;
    p = { armL: [-0.4 - s, 0.3], armR: [0.4 + s, 0.3], legL: [-0.3 - s, 0], legR: [0.3 + s, 0] };
  }
  const breathe = Math.sin(t * 2 + seed) * 4;
  const hip = [x, y], tilt = (p.egil || 0), neck = [x + tilt * 90, y - 200 + breathe];
  const head = [neck[0] + tilt * 30, neck[1] - 50 + (p.bak ? p.bak * 4 : 0)];
  line(hip[0], hip[1], neck[0], neck[1], seed, 6);
  g.lineWidth = 5; g.strokeStyle = INK; g.fillStyle = '#f3ead8';
  g.beginPath(); g.arc(head[0], head[1], 46, 0, 7); g.fill(); g.stroke();
  const arm = (a, k) => { const sx = neck[0], sy = neck[1] + 30; line(sx, sy, sx + Math.sin(a[0]) * 110, sy + Math.cos(a[0]) * 110 * (a[1] < 0 ? -1 : 1) * 0.9 + a[1] * 20, seed + k, 5); };
  arm(p.armL, 2); arm(p.armR, 3);
  line(hip[0], hip[1], hip[0] + Math.sin(p.legL[0]) * 150, hip[1] + 160, seed + 4, 5);
  line(hip[0], hip[1], hip[0] + Math.sin(p.legR[0]) * 150, hip[1] + 160, seed + 5, 5);
}

function bowl(x, y, o, tSince) {
  const r = 90;
  const half = (dx, dy, rot, left) => {
    g.save(); g.translate(x + dx, y + dy); g.rotate(rot);
    g.lineWidth = 6; g.strokeStyle = INK; g.fillStyle = '#e6d3a8'; g.beginPath();
    g.arc(0, 0, r, left ? Math.PI * 0.5 : Math.PI * 1.5 - Math.PI, left ? Math.PI * 1.5 : Math.PI * 0.5 + Math.PI, false);
    g.closePath(); g.fill(); g.stroke(); g.restore();
  };
  const bowlPath = () => { g.beginPath(); g.moveTo(-r, -30); g.quadraticCurveTo(-r, r, 0, r); g.quadraticCurveTo(r, r, r, -30); g.closePath(); };
  if (o.kirik || o.metal || o.altin) {
    const open = o.metal || o.altin ? 0 : 1;
    const k = Math.min(tSince / 0.4, 1);
    const spread = (tSince === Infinity ? 1 : ease(k)) * 22 * open;
    for (const side of [-1, 1]) {
      g.save(); g.translate(x + side * spread, y + (ease(k) * 8 * open));
      g.rotate(side * 0.06 * ease(k) * open);
      g.beginPath(); side < 0 ? (g.rect(-r - 5, -60, r + 5, 200)) : (g.rect(0, -60, r + 5, 200)); g.clip();
      bowlPath(); g.fillStyle = '#e6d3a8'; g.fill(); g.lineWidth = 6; g.strokeStyle = INK; g.stroke();
      g.restore();
    }
    if (o.metal || o.altin) { // çatlak çizgisi
      g.strokeStyle = o.altin ? GOLD : '#777'; g.lineWidth = o.altin ? 10 : 8; g.beginPath();
      g.moveTo(x, y - 30); g.lineTo(x - 12, y + 20); g.lineTo(x + 8, y + 55); g.lineTo(x - 4, y + r); g.stroke();
      if (o.altin) { g.shadowColor = GOLD; g.shadowBlur = 30; g.stroke(); g.shadowBlur = 0; }
    }
  } else {
    g.save(); g.translate(x, y); bowlPath(); g.fillStyle = '#e6d3a8'; g.fill(); g.lineWidth = 6; g.strokeStyle = INK; g.stroke(); g.restore();
  }
}

function sceneAt(i) {
  let s = story.sahneler[0];
  for (const sc of story.sahneler) if (i >= sc.kelime) s = sc;
  return s;
}

function renderAt(t) {
  const idx = Math.max(0, words.findIndex(w => w.end > t));
  const cur = words.findIndex(w => w.start <= t && t < w.end);
  const wi = cur === -1 ? (t >= duration ? words.length - 1 : idx) : cur;
  const sc = sceneAt(wi);
  g.fillStyle = sc.bg; g.fillRect(0, 0, W, H);
  g.strokeStyle = 'rgba(43,33,24,.15)'; g.lineWidth = 3; g.beginPath(); g.moveTo(0, 1180); g.lineTo(W, 1180); g.stroke();
  const sceneStart = (words[sc.kelime] || words[0]).start;
  const local = t - sceneStart;
  for (const a of sc.aktorler) figure(a.x * W, 1020, a.poz, t, a.id.length * 7);
  for (const e of sc.esyalar) {
    const ev = (sc.olaylar || []).find(o => o.hedef === e.id && o.yap === 'kir');
    let o = { ...e }, since = Infinity;
    if (ev && words[ev.kelime]) { since = t - words[ev.kelime].start; o.kirik = since >= 0; if (since < 0) since = -1; }
    bowl(e.x * W, 1020 + 80, o, since);
  }
  // Altyazı: ekrana sığan gruplar (en fazla 4 kelime), aktif kelime vurgulu
  g.font = '700 76px sans-serif'; g.textAlign = 'left'; g.textBaseline = 'middle';
  const MAXW = 940, wd = w => g.measureText(w.w + ' ').width;
  let grp = 0;
  while (true) { // wi'yi içeren grubu bul
    let n = 0, wsum = 0;
    while (grp + n < words.length && n < 4 && (n === 0 || wsum + wd(words[grp + n]) <= MAXW)) { wsum += wd(words[grp + n]); n++; }
    if (wi < grp + n) break; grp += n;
  }
  let n = 0, wsum = 0;
  while (grp + n < words.length && n < 4 && (n === 0 || wsum + wd(words[grp + n]) <= MAXW)) { wsum += wd(words[grp + n]); n++; }
  const chunk = words.slice(grp, grp + n), widths = chunk.map(wd);
  let x = (W - widths.reduce((a, b) => a + b, 0)) / 2;
  chunk.forEach((w, k) => {
    g.lineWidth = 14; g.strokeStyle = '#fff'; g.strokeText(w.w, x, 1500);
    g.fillStyle = (grp + k === wi) ? GOLD : INK; g.fillText(w.w, x, 1500); x += widths[k];
  });
  g.font = '600 48px sans-serif'; g.textAlign = 'center'; g.fillStyle = 'rgba(43,33,24,.55)'; g.fillText(story.baslik, W / 2, 200);
}

window.loadStory = (s, ws) => { story = s; words = ws; duration = ws[ws.length - 1].end; };
window.renderAt = renderAt;
window.getDuration = () => duration;
