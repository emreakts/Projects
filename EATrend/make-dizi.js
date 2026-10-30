// Tek komut: node make-dizi.js <dizi> <bölüm> [--mock] [--eksik]
// --eksik: hazır görselleri ve güncel sesi yeniden üretmez, sadece eksik adımları tamamlar.
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const { episodeFile, episodeId, ROOT } = require('./lib');
const [dizi, n] = process.argv.slice(2), mock = process.argv.includes('--mock') ? ['--mock'] : [], eksik = process.argv.includes('--eksik');
const tl = path.join(ROOT, 'out', episodeId(dizi, n), 'timeline.json');
const sesGuncel = eksik && fs.existsSync(tl) && fs.statSync(tl).mtimeMs > fs.statSync(episodeFile(dizi, n)).mtimeMs;
const steps = [['dizi/gorsel.js', ...mock], ...(sesGuncel ? [] : [['dizi/ses.js', ...mock]]), ['render/render-dizi.js']];
if (sesGuncel) console.log('Ses güncel, yeniden üretilmiyor');
for (const s of steps) execFileSync('node', [s[0], dizi, n, ...s.slice(1)], { stdio: 'inherit', cwd: __dirname });
