const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const ROOT = __dirname;
function loadEnv() {
  const f = path.join(ROOT, '.env'); if (!fs.existsSync(f)) return;
  for (const l of fs.readFileSync(f, 'utf8').split('\n')) {
    const m = l.match(/^\s*([A-Z_]+)\s*=\s*(.*)\s*$/); if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
  }
}
function story(id) { return JSON.parse(fs.readFileSync(path.join(ROOT, 'content/stories', id + '.json'), 'utf8')); }
function outDir(id) { const d = path.join(ROOT, 'out', id); fs.mkdirSync(d, { recursive: true }); return d; }
function requirePlaywright() {
  try { return require('playwright'); } catch {}
  const g = execFileSync('npm', ['root', '-g']).toString().trim();
  return require(path.join(g, 'playwright'));
}
module.exports = { ROOT, loadEnv, story, outDir, requirePlaywright };
