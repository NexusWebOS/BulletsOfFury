#!/usr/bin/env python3
"""
probe_bigatlas_0916.py - IS THE 1024x9383 SOURCE IMAGE THE COST?

    python _BUILD_SOURCE/probe_bigatlas_0916.py --stage 9

THE FINDING THIS TESTS
  On stage 9, `A.blit('ebullet', ...)` -- ONE 13x12 sprite -- measured at 229 ms per call (worst
  756 ms), and is 82% of the frame. The legacy master `ASSETS.img` is 1024 x 9383: 9.6 Mpx and
  over 9000 px tall.

  Hypothesis: a source image that tall falls outside Skia's image cache, so every
  `drawImage(A.img, sx,sy,sw,sh, ...)` re-rasterises far more of the source than the 13x12 rect
  it asked for. If so, cropping the rect ONCE into its own small canvas and blitting that should
  cost essentially nothing, and the pixels are identical by construction.

  This benchmarks both, in the page, against the same rect, and also blits a MID-HEIGHT rect and
  a TOP rect -- if the cost tracks the source Y offset, that is the tiling story; if it is flat,
  it is the image's total size.

⚠ A benchmark that only ever runs the slow arm proves nothing about the fix. Both arms run here,
  in the same frame, on the same rect, and the fast arm's output is compared pixel-for-pixel
  against the slow arm's before any timing is reported.
"""
import argparse, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
sys.path.insert(0, ROOT)
from shoot import serve  # noqa: E402
from profile_space_0916 import SETUP, AUTOPILOT  # noqa: E402

BENCH = r"""
(cfg) => {
  const A = (typeof ASSETS !== 'undefined') ? ASSETS : null;
  if (!A || !A.img) return {err:'no ASSETS.img'};
  const out = {imgW:A.img.naturalWidth, imgH:A.img.naturalHeight, rows:[]};

  // a scratch destination so we never touch the real canvas
  const dst = document.createElement('canvas'); dst.width = 256; dst.height = 256;
  const g = dst.getContext('2d');

  function timeIt(fn, n){
    fn(); // warm
    const t0 = performance.now();
    for (let i=0;i<n;i++) fn();
    return (performance.now()-t0)/n;
  }

  // Pick rects at three heights of the master to see whether cost tracks source Y.
  const names = cfg.names || [];
  for (const nm of names) {
    const f = A.frames[nm];
    if (!f) { out.rows.push({name:nm, err:'no frame'}); continue; }
    const [sx,sy,sw,sh] = f;

    // --- arm A: the shipped path, cropping straight out of the 1024x9383 master
    const slow = () => g.drawImage(A.img, sx, sy, sw, sh, 0, 0, sw, sh);

    // --- arm B: the same rect, pre-cropped ONCE into its own small canvas
    const cache = document.createElement('canvas');
    cache.width = sw; cache.height = sh;
    cache.getContext('2d').drawImage(A.img, sx, sy, sw, sh, 0, 0, sw, sh);
    const fast = () => g.drawImage(cache, 0, 0, sw, sh, 0, 0, sw, sh);

    // ⚠ PROVE THE PIXELS MATCH BEFORE REPORTING A SPEEDUP.
    let diff = -1;
    try {
      g.clearRect(0,0,256,256); slow();
      const a = g.getImageData(0,0,sw,sh).data;
      g.clearRect(0,0,256,256); fast();
      const b = g.getImageData(0,0,sw,sh).data;
      diff = 0;
      for (let i=0;i<a.length;i++) if (a[i]!==b[i]) diff++;
    } catch(e) { diff = -2; }

    const ns = cfg.iters || 40;
    const msSlow = timeIt(slow, ns);
    const msFast = timeIt(fast, ns);
    out.rows.push({name:nm, sx:sx, sy:sy, sw:sw, sh:sh,
                   msSlow:+msSlow.toFixed(3), msFast:+msFast.toFixed(4),
                   speedup:+(msSlow/Math.max(1e-6,msFast)).toFixed(1),
                   diffBytes:diff});
  }
  return out;
}
"""

PICK = r"""
() => {
  const A = (typeof ASSETS !== 'undefined') ? ASSETS : null;
  if (!A || !A.frames) return [];
  const ks = Object.keys(A.frames);
  // one near the top of the master, one near the middle, one near the bottom, plus the
  // offender itself -- to separate "tall source" from "deep source offset"
  const withY = ks.map(k => ({k:k, y:A.frames[k][1]})).sort((a,b)=>a.y-b.y);
  const pick = [];
  if (withY.length) {
    pick.push(withY[0].k);
    pick.push(withY[(withY.length/2)|0].k);
    pick.push(withY[withY.length-1].k);
  }
  if (A.frames['ebullet']) pick.unshift('ebullet');
  return Array.from(new Set(pick));
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=int, default=9)
    ap.add_argument('--iters', type=int, default=40)
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright
    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=['--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1250}, device_scale_factor=1)
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'",
                             timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(SETUP, {'stage': args.stage, 'pilot': 'cole'})
        pg.wait_for_timeout(3000)
        names = pg.evaluate(PICK)
        res = pg.evaluate(BENCH, {'names': names, 'iters': args.iters})
        b.close()
    stop()

    if res.get('err'):
        print(res['err']); return
    print('  ASSETS.img is %dx%d  (%.1f Mpx)'
          % (res['imgW'], res['imgH'], res['imgW'] * res['imgH'] / 1e6))
    print('')
    print('  %-16s %9s %7s %12s %12s %9s %9s'
          % ('frame', 'src y', 'size', 'ms from img', 'ms cached', 'speedup', 'diff'))
    for r in res['rows']:
        if r.get('err'):
            print('  %-16s %s' % (r['name'], r['err'])); continue
        print('  %-16s %9d %7s %12.3f %12.4f %8.1fx %9s'
              % (r['name'][:16], r['sy'], '%dx%d' % (r['sw'], r['sh']),
                 r['msSlow'], r['msFast'], r['speedup'],
                 ('IDENTICAL' if r['diffBytes'] == 0 else
                  ('tainted' if r['diffBytes'] == -2 else '%d bytes' % r['diffBytes']))))


if __name__ == '__main__':
    main()
