// Senaryo üretimi: Gemini (metin) + yedek şablon (demo). Çıktıyı doğrular ve kasa hesabını düzeltir.
const fs = require('fs'), path = require('path');
const store = require('./store');
const readEnv = () => { const o = {}; const f = path.join(store.ROOT, '.env'); if (fs.existsSync(f)) for (const l of fs.readFileSync(f, 'utf8').split('\n')) { const m = l.match(/^\s*([A-Z_]+)\s*=\s*(.*)\s*$/); if (m) o[m[1]] = m[2]; } return o; };
const bible = () => JSON.parse(fs.readFileSync(path.join(store.SERI, 'bible.json'), 'utf8'));
const TR = s => s.toLocaleUpperCase('tr');
const bin = x => x % 1000 === 0 ? `${x / 1000} bin` : String(x);

async function geminiText(prompt) {
  const e = readEnv(), key = e.GEMINI_API_KEY; if (!key) throw new Error('Gemini anahtarı yok (Ayarlar)');
  const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${e.GEMINI_TEXT_MODEL || 'gemini-2.5-flash'}:generateContent`, { method: 'POST', headers: { 'x-goog-api-key': key, 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }], generationConfig: { responseMimeType: 'application/json', temperature: 1 } }) });
  const j = await r.json(); if (!r.ok) throw new Error('Gemini ' + r.status + ': ' + JSON.stringify(j.error || j).slice(0, 240));
  const t = j.candidates?.[0]?.content?.parts?.map(p => p.text).join('') || ''; if (!t) throw new Error('Gemini boş yanıt verdi');
  return JSON.parse(t.replace(/^```json\s*|```$/g, '').trim());
}

function history(n) {
  const eps = Object.values(store.load().episodes).filter(e => e.n < n && store.hasFile(e.n)).sort((a, b) => a.n - b.n).slice(-6);
  const items = eps.map(e => { try { return JSON.parse(fs.readFileSync(store.file(e.n), 'utf8')); } catch { return null; } }).filter(Boolean);
  const last = items.at(-1), kasa = last ? ([...last.sahneler].reverse().find(s => s.kasa)?.kasa.sonra ?? 100000) : 100000;
  return { basliklar: items.map(b => `PART ${b.bolum}: ${b.baslik}`), kasa };
}

function promptFor(n, note) {
  const b = bible(), h = history(n);
  return `Sen bir YouTube Shorts komedi dizisi yazarısın. Dizi: "${b.dizi}" (kurgusal, tamamen hayal ürünü). İki karakter var:
- bidik (Bıdık): ${b.karakterler.bidik.tarif}. Atılgan, hesapsız, aşırı özgüvenli.
- zipir (Zıpır): ${b.karakterler.zipir.tarif}. Temkinli, sürekli endişeli ama sonunda hep haklı çıkan.
Konu: iki arkadaş İstanbul'da eşya al-sat yapıyor, para ("kasa") artıp azalıyor.
Şimdi PART ${n} bölümünü yaz. Önceki bölümler: ${h.basliklar.join(' | ') || 'yok (ilk bölüm)'}. Kasa şu an ${h.kasa} TL. Önceki bölümlerdeki eşyaları TEKRARLAMA.
Kurallar:
- Toplam 5 veya 6 sahne, her sahnede 2-3 replik, her replik en fazla 12 kelime. Tüm bölüm 55 saniyeyi geçmesin (yaklaşık 100 kelime).
- Şakalı, hızlı tempolu, her sahnede küçük bir tırmanış, sonda sürpriz ya da bir sonraki bölüme merak uyandıran bir kanca.
- Replikler Türkçe. Duygu etiketleri köşeli parantezle, sadece şunlar: [heyecanlı] [şüpheli] [şaşkın] [gülerek] [bıkkın] [coşkulu] [fısıltıyla] [kendinden emin] [üzgün].
- "mekan" ve "aksiyon" alanları İngilizce, görsel üretimi için canlı ve somut betimleme (karakterlerin görünüşünü yazma, sadece ne yaptıklarını ve ortamı yaz).
- Gerçek kişi, marka, siyaset, şiddet, yetişkin içerik yok. Gerçek hayattaki YouTuber karakterlerini taklit etme.
- "kasa" her sahnede: once (sahne başı), sonra (sahne sonu). İlk sahnenin once değeri ${h.kasa}. Alış kasayı düşürür, tamir masrafı düşürür, satış artırır. Sayılar tutarlı olsun.
- "baslik": en fazla 70 karakter, BÜYÜK HARF, merak uyandıran, bir iki emoji değil, sadece yazı; sonunda ünlem olabilir.
${note ? `- Önceki taslağa şu geri bildirim verildi, bunu dikkate al: ${note}\n` : ''}
SADECE geçerli JSON döndür, şu şema:
{"baslik":"...","sahneler":[{"mekan":"...","aksiyon":"...","satirlar":[{"k":"bidik","m":"[heyecanlı] ..."},{"k":"zipir","m":"..."}],"kasa":{"once":0,"sonra":0}}]}`;
}

// Yapıyı doğrula ve düzelt
function normalize(raw, n) {
  const b = bible(), h = history(n); if (!raw || !Array.isArray(raw.sahneler)) throw new Error('Senaryo biçimi geçersiz');
  let S = raw.sahneler.slice(0, 7).map(s => ({ mekan: String(s.mekan || '').slice(0, 300), aksiyon: String(s.aksiyon || '').slice(0, 300),
    satirlar: (s.satirlar || []).filter(l => b.karakterler[l.k] && typeof l.m === 'string' && l.m.trim()).slice(0, 3).map(l => ({ k: l.k, m: l.m.trim().slice(0, 140) })), kasa: s.kasa }));
  S = S.filter(s => s.mekan && s.aksiyon && s.satirlar.length); if (S.length < 3) throw new Error('Senaryoda en az 3 geçerli sahne olmalı');
  const words = S.reduce((a, s) => a + s.satirlar.reduce((x, l) => x + l.m.replace(/\[[^\]]*\]/g, '').trim().split(/\s+/).length, 0), 0);
  if (words > 130) throw new Error(`Senaryo çok uzun (${words} kelime), Shorts için kısa olmalı`);
  let cur = h.kasa; for (const s of S) { const so = Number(s.kasa && s.kasa.sonra); const sonra = Number.isFinite(so) && so >= 0 ? Math.round(so) : cur; s.kasa = { once: cur, sonra }; cur = sonra; s.kimler = [...new Set(s.satirlar.map(l => l.k))]; }
  const baslik = TR(String(raw.baslik || `PART ${n}`)).replace(/[^\p{L}\p{N} '!?.,:-]/gu, '').slice(0, 80).trim() || `PART ${n}`;
  return { dizi: 'alsat', bolum: n, baslik, sahneler: S.map(s => ({ kimler: s.kimler, mekan: s.mekan, aksiyon: s.aksiyon, satirlar: s.satirlar, kasa: s.kasa })) };
}

// Demo / yedek: şablondan senaryo
const ITEMS = [
  { ad: 'eski scooter', kusur: 'farı bile yok', alis: 40000, tamir: 5000, satis: 58000, yer: 'a narrow sunny Istanbul side street with a tea house, an old rusty scooter at the curb', ek: 'a grumpy old neighbor in a vest holding a tea glass' },
  { ad: 'antika piyano', kusur: 'yarısı çalışmıyor', alis: 30000, tamir: 8000, satis: 52000, yer: 'a cluttered second-hand furniture shop with a dusty upright piano', ek: 'a tall stern shop owner with reading glasses' },
  { ad: 'kamp karavanı', kusur: 'kapısı kapanmıyor', alis: 90000, tamir: 12000, satis: 135000, yer: 'a parking lot by the sea with an old small camper van', ek: 'a cheerful fisherman holding a bucket' },
  { ad: 'vintage bisiklet', kusur: 'zinciri yok', alis: 12000, tamir: 2000, satis: 21000, yer: 'a sunny cobblestone street with a vintage bicycle leaning on a wall', ek: 'a university student with a backpack' },
  { ad: 'eski televizyon', kusur: 'ekranı çatlak', alis: 6000, tamir: 1500, satis: 14000, yer: 'a flea market stall full of old electronics and a big tube television', ek: 'a talkative market seller with a mustache-less friendly smile' },
  { ad: 'deri koltuk takımı', kusur: 'yırtıkları var', alis: 25000, tamir: 4000, satis: 41000, yer: 'a warehouse sale with worn leather sofas stacked together', ek: 'a bored warehouse worker eating simit' },
  { ad: 'motorlu tekne', kusur: 'motoru ses çıkarıyor', alis: 70000, tamir: 9000, satis: 108000, yer: 'a small marina on the Bosphorus with an old motorboat tied to the dock', ek: 'a retired captain in a white cap' },
  { ad: 'espresso makinesi', kusur: 'buharı kaçırıyor', alis: 9000, tamir: 1000, satis: 19000, yer: 'a tiny cafe closing down, a big old espresso machine on the counter', ek: 'a sad cafe owner wiping the counter' }
];
function mockEpisode(n) {
  const h = history(n), it = ITEMS[(n - 1) % ITEMS.length], next = ITEMS[n % ITEMS.length], k0 = h.kasa, k1 = k0 - it.alis, k2 = k1 - it.tamir, k3 = k2 + it.satis;
  const raw = { baslik: [`${it.ad} aldık, komşuyu şaşırttık!`, `${it.ad} bizi zengin etti mi?`, `${it.ad} aldık, herkes şok oldu!`][n % 3], sahneler: [
    { mekan: it.yer, aksiyon: 'both men crouching and inspecting it, the shorter one thrilled, the tall one doubtful', satirlar: [{ k: 'bidik', m: `[heyecanlı] Zıpır, bak bak! Bu ${it.ad} tam bize göre!` }, { k: 'zipir', m: `[şüpheli] Bıdık, bunun ${it.kusur}.` }], kasa: { once: k0, sonra: k0 } },
    { mekan: it.yer, aksiyon: `the shorter man haggling with ${it.ek}, the tall man nervously holding an envelope of cash`, satirlar: [{ k: 'bidik', m: `${bin(it.alis)} verelim, hemen alalım.` }, { k: 'zipir', m: '[fısıltıyla] Bıdık, kasada o kadar yok!' }, { k: 'bidik', m: '[kendinden emin] Sen karışma, ben hallederim.' }], kasa: { once: k0, sonra: k1 } },
    { mekan: 'a small messy garage full of tools and spare parts', aksiyon: 'both men covered in grease proudly showing the repaired item, the tall one wiping his glasses', satirlar: [{ k: 'zipir', m: '[şaşkın] Çalıştı! Gerçekten çalıştı!' }, { k: 'bidik', m: '[gülerek] Ben demedim mi? Bu iş bende.' }], kasa: { once: k1, sonra: k2 } },
    { mekan: 'a sunny Istanbul waterfront promenade with seagulls', aksiyon: 'the shorter man shaking hands with a happy buyer, the tall man counting cash with wide eyes', satirlar: [{ k: 'bidik', m: `${bin(it.satis)}, söz verdik, bitti!` }, { k: 'zipir', m: '[coşkulu] Kasa doldu, inanamıyorum!' }], kasa: { once: k2, sonra: k3 } },
    { mekan: `Istanbul at sunset, ${next.yer}`, aksiyon: 'both men staring at the next big find with huge eyes, the short one pointing, the tall one covering his face', satirlar: [{ k: 'bidik', m: `[heyecanlı] Zıpır, sıradaki iş ${next.ad}!` }, { k: 'zipir', m: '[bıkkın] Yine mi Bıdık? Yine mi?' }], kasa: { once: k3, sonra: k3 } }] };
  return normalize(raw, n);
}

function meta(ep) { const b = bible(); return { aciklama: `${ep.baslik}\n\n${b.dizi}, Part ${ep.bolum}. Kurgusal komedi dizisidir; karakterler ve olaylar tamamen hayal ürünüdür. Bu video yapay zekâ ile üretilmiştir.\n\n#shorts #alsat #komedi #yapayzeka #dizi`, etiketler: ['shorts', 'alsat', 'komedi', 'yapay zeka', 'dizi'] }; }

async function yaz(n, { demo, note }) {
  if (demo) return mockEpisode(n);
  let err; for (let i = 0; i < 2; i++) { try { return normalize(await geminiText(promptFor(n, note ? note + (err ? ' | ' + err.message : '') : err ? 'Önceki deneme hatalıydı: ' + err.message : '')), n); } catch (e) { err = e; if (/anahtar|Gemini 4/.test(e.message)) break; } }
  throw err;
}
module.exports = { yaz, meta, readEnv, history };
