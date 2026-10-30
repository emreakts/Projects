// Tek komut: node make-dizi.js <dizi> <bölüm> [--mock]   (görsel → ses → video)
const { execFileSync } = require('child_process'); const [dizi, n] = process.argv.slice(2), mock = process.argv.includes('--mock') ? ['--mock'] : [];
for (const s of [['dizi/gorsel.js', ...mock], ['dizi/ses.js', ...mock], ['render/render-dizi.js']]) execFileSync('node', [s[0], dizi, n, ...s.slice(1)], { stdio: 'inherit', cwd: __dirname });
