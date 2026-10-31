// Çizim sayfasını kare kare gezip FFmpeg'e verir, sesi ekler, ses seviyesini ayarlar.
// Kullanım: node render/render.js <storyId>   (önce voice/tts.js çalışmış olmalı)
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const { ROOT, story, outDir, requirePlaywright } = require('../lib');
const FPS = 30;

(async () => {
  const id = process.argv[2]; if (!id) { console.error('kullanım: node render/render.js <storyId>'); process.exit(1); }
  const dir = outDir(id), words = JSON.parse(fs.readFileSync(path.join(dir, 'words.json'), 'utf8'));
  const { chromium } = requirePlaywright();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(ROOT, 'engine/index.html'));
  await page.evaluate(([s, w]) => window.loadStory(s, w), [story(id), words]);
  const dur = await page.evaluate(() => window.getDuration()) + 0.5, total = Math.ceil(dur * FPS);

  const video = path.join(dir, `${id}.mp4`);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-i', path.join(dir, 'voice.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11,apad',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-t', String(dur), video],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise(r => ff.on('close', r));
  const canvas = page.locator('#c');
  for (let f = 0; f < total; f++) {
    await page.evaluate(t => window.renderAt(t), f / FPS);
    const buf = await canvas.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 60 === 0) process.stdout.write(`\r${f}/${total} kare`);
  }
  ff.stdin.end(); await done; await browser.close();
  console.log(`\n${video}`);
})().catch(e => { console.error(e); process.exit(1); });
