const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const source = 'C:/Users/Mdogg/Videos/2026-08-30 00-03-57.mp4';
  const outDir = path.resolve('docs/proofs/stage1_video_0830');
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args: ['--allow-file-access-from-files'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const fileUrl = 'file:///' + source.replace(/\\/g, '/').replace(/ /g, '%20');
  await page.goto(fileUrl, { waitUntil: 'load', timeout: 30000 });
  await page.waitForFunction(() => {
    const v = document.querySelector('video');
    return Number.isFinite(v.duration) && v.videoWidth > 0;
  }, null, { timeout: 30000 });
  for (const t of [42, 43, 44, 44.5, 45, 46, 47, 48, 49, 50, 52, 55, 58, 62]) {
    await page.evaluate(async (time) => {
      const v = document.querySelector('video');
      await new Promise((resolve, reject) => {
        const done = () => { v.removeEventListener('seeked', done); resolve(); };
        v.addEventListener('seeked', done, { once: true });
        v.currentTime = time;
        setTimeout(() => reject(new Error('seek timeout at ' + time)), 8000);
      });
    }, t);
    await page.locator('video').screenshot({ path: path.join(outDir, `t_${String(t).replace('.', '_')}.png`) });
  }
  await browser.close();
})();
