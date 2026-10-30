// Dizi bölümünü videoya çevirir. Kullanım: node render/render-dizi.js <dizi> <bölüm>
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const { ROOT, bible, episode, episodeId, outDir, requirePlaywright } = require('../lib');
const FPS = 30;
(async () => {
  const [dizi, n] = process.argv.slice(2); if (!dizi || !n) { console.error('kullanım: node render/render-dizi.js <dizi> <bölüm>'); process.exit(1); }
  const id = episodeId(dizi, n), dir = outDir(id), ep = episode(dizi, n), tl = JSON.parse(fs.readFileSync(path.join(dir, 'timeline.json'), 'utf8'));
  const urls = ep.sahneler.map((_, i) => 'file://' + path.join(dir, `img-${i + 1}.png`));
  const missing = urls.filter(u => !fs.existsSync(u.slice(7))); if (missing.length) { console.error('Eksik görsel var, önce görselleri üret.'); process.exit(1); }
  const { chromium } = requirePlaywright(); const browser = await chromium.launch(), page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(ROOT, 'engine/dizi.html'));
  await page.evaluate(([s, b, t, u]) => window.loadEpisode(s, b, t, u), [ep, bible(dizi), tl, urls]);
  const total = Math.ceil((await page.evaluate(() => window.getDuration())) * FPS), video = path.join(dir, `${id}.mp4`);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-i', path.join(dir, 'voice.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11,apad',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-t', String(total / FPS), video], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise(r => ff.on('close', r)), canvas = page.locator('#c');
  for (let f = 0; f < total; f++) {
    await page.evaluate(t => window.renderAt(t), f / FPS);
    if (!ff.stdin.write(await canvas.screenshot({ type: 'jpeg', quality: 92 }))) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 30 === 0) process.stdout.write(`\r${f}/${total} kare`);
  }
  ff.stdin.end(); await done; await browser.close(); console.log('\n' + video);
})().catch(e => { console.error(e); process.exit(1); });
