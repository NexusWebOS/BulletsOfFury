"""Real Chromium visual QA for the standalone art pack, using shoot.py's server."""
from pathlib import Path
import hashlib
import json
from playwright.sync_api import sync_playwright
import shoot

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots/raiden_reference_1024'
PACK = ROOT / 'art-packs/raiden-reference-1024'
OUT.mkdir(parents=True, exist_ok=True)
errors, checks = [], []


def check(name, passed, detail=None):
    checks.append(dict(name=name, passed=bool(passed), detail=detail))
    print(('PASS ' if passed else 'FAIL ') + name, flush=True)


PIXELS = r"""async () => {
 const results = [];
 for (const asset of ART_PACK.assets) {
  for (const resolution of ['native','master']) {
   const image = new Image(); image.src = asset[resolution]; await image.decode();
   const canvas = document.createElement('canvas');
   canvas.width=image.naturalWidth; canvas.height=image.naturalHeight;
   const ctx=canvas.getContext('2d',{willReadFrequently:true});
   ctx.imageSmoothingEnabled=false; ctx.drawImage(image,0,0);
   const pixels=ctx.getImageData(0,0,canvas.width,canvas.height).data;
   let visible=0, transparent=0, edge=0, bright=0;
   for(let i=0;i<pixels.length;i+=4) {
    const x=(i/4)%canvas.width, y=Math.floor(i/4/canvas.width), a=pixels[i+3];
    if(a>=64) {visible++; if(x===0||y===0||x===canvas.width-1||y===canvas.height-1) edge++;}
    if(a===0) transparent++;
    if(a>192&&pixels[i]>220&&pixels[i+1]>220&&pixels[i+2]>220) bright++;
   }
   const expected=asset[resolution+'_size'];
   results.push({id:asset.id,resolution,width:canvas.width,height:canvas.height,visible,transparent,edge,bright,
    ok:canvas.width===expected[0]&&canvas.height===expected[1]&&canvas.width%2===0&&canvas.height%2===0&&visible>20&&transparent>20&&edge===0});
  }
 }
 const sheets=[];
 for(const sheet of ART_PACK.sheets) {
  const im=new Image();im.src=sheet.path;await im.decode();
  sheets.push({path:sheet.path,ok:im.naturalWidth===sheet.size[0]&&im.naturalHeight===sheet.size[1]});
 }
 return {results,sheets};
}"""


port, stop = shoot.serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='msedge', args=['--mute-audio'])
        page = browser.new_page(viewport={'width': 1480, 'height': 1100}, device_scale_factor=1)
        page.on('pageerror', lambda e: errors.append('page: ' + str(e)))
        page.on('console', lambda e: errors.append('console: ' + e.text) if e.type == 'error' else None)
        page.on('requestfailed', lambda r: errors.append('request: ' + r.url + ' ' + str(r.failure)))
        page.goto(f'http://127.0.0.1:{port}/art-packs/raiden-reference-1024/index.html')
        page.wait_for_function('window.artPackReady === true')
        pixels = page.evaluate(PIXELS)
        (OUT / 'pixel-report.json').write_text(json.dumps(pixels, indent=2) + '\n')
        check('104 actual PNGs decoded and drawn in Chromium; even frames, transparent margins, no opaque edge clipping',
              len(pixels['results']) == 104 and all(r['ok'] for r in pixels['results']),
              [r for r in pixels['results'] if not r['ok']])
        check('All six sheets decode at their registered dimensions', all(s['ok'] for s in pixels['sheets']))
        for group, count in [('projectiles', 24), ('lasers', 12), ('enemies', 16)]:
            page.click(f'.tabs button[data-group={group}]')
            page.wait_for_function('Array.from(document.querySelectorAll("#grid img")).every(im=>im.complete&&im.naturalWidth>0)')
            check(f'{group}: {count} visible sprite cards', page.locator('#grid .card').count() == count)
            page.screenshot(path=str(OUT / f'gallery-{group}.png'), full_page=True)
        page.click('.tabs button[data-group=lasers]')
        page.click('[data-id=green_helix] .sprite-button')
        page.wait_for_function('document.querySelector("#detail-image").complete&&document.querySelector("#detail-image").naturalWidth>0')
        check('Detail viewer opens correct master PNG', page.locator('#detail[open]').count() == 1 and page.locator('#detail-title').inner_text() == 'Green Helix')
        page.screenshot(path=str(OUT / 'gallery-detail.png'))
        page.click('#close')
        for ground in ['jungle', 'sand', 'sea', 'check', 'dark']:
            page.select_option('#background', ground)
            check(f'Background switch: {ground}', page.locator('#grid').get_attribute('data-ground') == ground)
        page.click('.tabs button[data-group=enemies]')
        page.set_viewport_size({'width': 390, 'height': 844})
        page.screenshot(path=str(OUT / 'gallery-mobile.png'), full_page=True)
        check('Mobile has no horizontal overflow', page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
        check('Native PNG download points to actual asset', page.locator('[data-id=steel_interceptor] .card-meta a').get_attribute('href') == 'native/enemies/steel_interceptor.png')
        browser.close()
finally:
    stop()

baseline = json.loads((OUT / 'game-baseline.json').read_text())
check('Shipping game files retain their starting hashes', all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == digest for p, digest in baseline.items()))
check('No browser page, console or failed request errors', not errors, errors)
report = dict(passed=sum(c['passed'] for c in checks), failed=sum(not c['passed'] for c in checks), checks=checks)
(OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
print(f"FINAL SUMMARY: {report['passed']} passed / {report['failed']} failed", flush=True)
raise SystemExit(bool(report['failed']))
