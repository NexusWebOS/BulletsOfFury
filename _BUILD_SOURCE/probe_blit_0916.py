#!/usr/bin/env python3
"""
probe_blit_0916.py - WHO CALLS A.blit, HOW OFTEN, AND AT WHAT SIZE.

    python _BUILD_SOURCE/probe_blit_0916.py --stage 9 --seconds 6
    python _BUILD_SOURCE/probe_blit_0916.py --stage 3 --seconds 6     # control

The CPU profile (`profile_space_0916.py`) charges 82% of stage 9's frame -- 622 ms of it -- to
`A.blit` at game.js:1679, a function that is one `ctx.drawImage` of one atlas rect. It does not
appear in stage 3's top sixteen at all. A function that cheap costing that much is either being
called an enormous number of times or being asked to scale enormously, and those want opposite
fixes, so this measures both before anything is changed.

Counting is the right instrument HERE, unlike the case CLAUDE.md warns about ("a key-counting
probe is not a pixel probe") -- that warning is about proving something is VISIBLE. This is
proving something is EXPENSIVE, which is exactly what a call count and a scale factor answer.
"""
import argparse, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
sys.path.insert(0, ROOT)
from shoot import serve  # noqa: E402
from profile_space_0916 import SETUP, AUTOPILOT  # noqa: E402

TRAP = r"""
() => {
  if (window.__blitTrap) return true;
  // ⚠ `window.ASSETS` IS UNDEFINED WHILE BARE `ASSETS` WORKS. game.js declares it as a
  // module-scope const, so it lives in the global LEXICAL environment and is not a property of
  // window -- CLAUDE.md records the identical trap for `Snd`, and for `Snd.TAME`, where reading
  // it through window returned {} and made an assertion pass vacuously.
  const A = (typeof ASSETS !== 'undefined') ? ASSETS : null;
  if (!A || typeof A.blit !== 'function') return false;
  const real = A.blit.bind(A);
  window.__blitStats = {calls:0, frames0:(window.__bofFrames|0), by:{}};
  A.blit = function(n, x, y, w, h){
    const S = window.__blitStats;
    S.calls++;
    const t0 = performance.now();
    let r = S.by[n];
    if (!r) r = S.by[n] = {n:0, srcW:0, srcH:0, dstW:0, dstH:0, maxDst:0};
    r.n++;
    const f = A.frames[n];
    if (f) {
      const dw = w || f[2], dh = h || f[3];
      r.srcW = f[2]; r.srcH = f[3];
      r.dstW += dw; r.dstH += dh;
      const a = dw * dh;
      if (a > r.maxDst) r.maxDst = a;
    }
    const out = real(n, x, y, w, h);
    const dt = performance.now() - t0;
    r.ms = (r.ms || 0) + dt;
    if (dt > (r.worst || 0)) r.worst = dt;
    S.ms = (S.ms || 0) + dt;
    return out;
  };
  window.__blitTrap = true;
  return true;
}
"""

REPORT = r"""
() => {
  const S = window.__blitStats;
  if (!S) return null;
  const frames = Math.max(1, (window.__bofFrames|0) - S.frames0);
  const rows = Object.keys(S.by).map(k => {
    const r = S.by[k];
    return {key:k, calls:r.n, perFrame:r.n/frames,
            src:r.srcW+'x'+r.srcH,
            avgDst:Math.round(r.dstW/r.n)+'x'+Math.round(r.dstH/r.n),
            scale: r.srcW ? +( (r.dstW/r.n) / r.srcW ).toFixed(2) : 0,
            px: Math.round((r.dstW/r.n)*(r.dstH/r.n)*r.n/frames),
            msPerFrame: +((r.ms||0)/frames).toFixed(2),
            msPerCall: +((r.ms||0)/r.n).toFixed(3),
            worst: +((r.worst||0)).toFixed(2)};
  }).sort((a,b) => b.px - a.px);
  rows.sort((a,b) => b.msPerFrame - a.msPerFrame);
  return {frames:frames, calls:S.calls, perFrame:S.calls/frames,
          msPerFrame:+((S.ms||0)/frames).toFixed(2),
          imgW: ((typeof ASSETS!=='undefined' && ASSETS.img && ASSETS.img.naturalWidth)|0),
          imgH: ((typeof ASSETS!=='undefined' && ASSETS.img && ASSETS.img.naturalHeight)|0),
          rows:rows.slice(0,20)};
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=int, default=9)
    ap.add_argument('--seconds', type=float, default=6)
    ap.add_argument('--pilot', default='cole')
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
        r = pg.evaluate(SETUP, {'stage': args.stage, 'pilot': args.pilot})
        if not r.get('ok'):
            print('setup failed:', r.get('err')); b.close(); stop(); sys.exit(1)
        pg.evaluate(AUTOPILOT)
        pg.wait_for_timeout(4000)
        if not pg.evaluate(TRAP):
            print('could not trap A.blit'); b.close(); stop(); sys.exit(1)
        pg.wait_for_timeout(int(args.seconds * 1000))
        rep = pg.evaluate(REPORT)
        b.close()
    stop()

    if not rep:
        print('no stats'); return
    print('=== stage %d : A.blit over %d drawn frames ===' % (args.stage, rep['frames']))
    print('  %d calls total, %.0f per frame\n' % (rep['calls'], rep['perFrame']))
    print('  A.img is %dx%d' % (rep['imgW'], rep['imgH']))
    print('  A.blit total: %.2f ms/frame' % rep['msPerFrame'])
    print('')
    print('  %-22s %7s %8s %9s %11s %10s %9s' % ('atlas frame', 'calls', '/frame', 'src',
                                                 'ms/frame', 'ms/call', 'worst'))
    for r in rep['rows']:
        print('  %-22s %7d %8.1f %9s %11.2f %10.3f %9.2f'
              % (r['key'][:22], r['calls'], r['perFrame'], r['src'],
                 r['msPerFrame'], r['msPerCall'], r['worst']))
    tot = sum(r['px'] for r in rep['rows'])
    print('\n  fill rate from A.blit: %.1f Mpx/frame (the canvas itself is 0.98 Mpx)'
          % (tot / 1e6))


if __name__ == '__main__':
    main()
