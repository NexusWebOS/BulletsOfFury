#!/usr/bin/env python3
"""
probe_lasersizes_0916.py - HOW MANY DISTINCT (key, colour, size) DOES THE SPACE LASER DRAW?

    python _BUILD_SOURCE/probe_lasersizes_0916.py --stage 9

This sizes the cache BEFORE the cache is written. The fix for game.js:44780 is the Magma Ward's:
bake the glow once into a canvas and blit that instead of re-blurring per round. Whether that is
a good idea depends entirely on how many distinct baked canvases it implies -- a handful is free,
a thousand is a memory leak wearing a speedup.

It also decides whether the cache key can use the EXACT float size. Quantising `_lh` to an
integer would be simpler and would change the drawn size of every pulse by up to half a pixel;
Mike owns the art, so the cache is only worth doing if it can be pixel-exact.
"""
import argparse, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
sys.path.insert(0, ROOT)
from shoot import serve  # noqa: E402
from profile_space_0916 import SETUP, AUTOPILOT  # noqa: E402

TRAP = r"""
() => {
  if (window.__lsTrap) return false;
  window.__ls = {combos:{}, calls:0, bh:{}};
  const realCanvas = window.spaceLaserPulseCanvas;
  if (typeof realCanvas !== 'function') return 'no spaceLaserPulseCanvas';
  // The draw derives its size from b.h. Sample the bullets directly each frame rather than
  // wrapping the draw, so nothing about the draw path changes while measuring it.
  const inner = window.loop;
  window.loop = function(){
    const r = inner.apply(this, arguments);
    try {
      if (typeof pBullets !== 'undefined') {
        for (const b of pBullets) {
          if (!b || b.kind !== 'spaceLaser' || b._launchDelay > 0) continue;
          const lv = Math.max(1, Math.min(5, b.lv||1));
          const key = 'laser_' + lv + '_pulse_' + (((b.pulse||0)&1) ? 'short' : 'long');
          const lp = realCanvas(key);
          const lh = Math.max(20, Math.min(30, (b.h||24)*0.72));
          const lw = lp ? lh*(lp.width/lp.height) : lh*0.55;
          const col = (typeof SPACE_LASER_COL!=='undefined')
                      ? SPACE_LASER_COL[Math.max(0,Math.min(4,lv-1))] : '?';
          const ck = key + '|' + col + '|' + lw.toFixed(3) + 'x' + lh.toFixed(3);
          window.__ls.combos[ck] = (window.__ls.combos[ck]|0) + 1;
          window.__ls.bh[String(b.h)] = (window.__ls.bh[String(b.h)]|0) + 1;
          window.__ls.calls++;
        }
      }
    } catch(_e){}
    return r;
  };
  window.__lsTrap = true;
  return true;
}
"""

REPORT = r"""
() => {
  const L = window.__ls || {combos:{}, calls:0, bh:{}};
  const ks = Object.keys(L.combos).sort((a,b)=>L.combos[b]-L.combos[a]);
  return {distinct: ks.length, calls: L.calls,
          top: ks.slice(0,12).map(k => ({k:k, n:L.combos[k]})),
          bh: Object.keys(L.bh).sort().map(h => ({h:h, n:L.bh[h]}))};
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=int, default=9)
    ap.add_argument('--seconds', type=float, default=8)
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
        pg.evaluate(AUTOPILOT)
        got = pg.evaluate(TRAP)
        if got is not True:
            print('trap:', got)
        pg.wait_for_timeout(int(args.seconds * 1000))
        rep = pg.evaluate(REPORT)
        b.close()
    stop()

    print('  %d spaceLaser draws sampled' % rep['calls'])
    print('  %d DISTINCT (key | colour | wxh) combinations' % rep['distinct'])
    print('')
    for r in rep['top']:
        print('    %-52s %6d' % (r['k'][:52], r['n']))
    print('')
    print('  distinct b.h values: %s' % ', '.join('%s (x%d)' % (r['h'], r['n']) for r in rep['bh']))


if __name__ == '__main__':
    main()
