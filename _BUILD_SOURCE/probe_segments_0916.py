#!/usr/bin/env python3
"""
probe_segments_0916.py - ATTRIBUTE DEFERRED CANVAS COST TO THE DRAW THAT QUEUED IT.

    python _BUILD_SOURCE/probe_segments_0916.py --stage 9
    python _BUILD_SOURCE/probe_segments_0916.py --stage 3      # control

WHY THIS EXISTS -- AND IT CORRECTS AN EARLIER WRONG ANSWER IN THIS SAME INVESTIGATION.

  The CPU profile charged 82% of stage 9's frame to `A.blit`, and a direct timing trap agreed:
  229 ms per call, worst 756 ms. Both were measuring honestly and both were pointing at the wrong
  function. A micro-benchmark settled it -- that exact blit, that exact rect, out of that exact
  1024x9383 master, costs **0.005 ms** in a tight loop.

  Canvas2D rasterisation is DEFERRED. Draw calls are recorded and flushed later, and the flush is
  charged to whichever call happens to trigger it. `A.blit` was where the bill was PAID, not where
  it was INCURRED. A profiler cannot see that distinction, and neither can a stopwatch around one
  call -- which is why two independent measurements agreed on the same wrong function.

  The fix is to make the cost non-deferred while measuring: force a flush (`getImageData(0,0,1,1)`,
  which cannot be reordered past queued draws) after each draw phase, and time the phases. Then
  the cost lands where it was created.

⚠ THE FLUSH ITSELF COSTS SOMETHING, so every number here is inflated by a constant per segment.
  The BASELINE row measures that constant against an empty segment; subtract it before quoting a
  figure, and trust the RANKING over the absolute milliseconds.
"""
import argparse, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
sys.path.insert(0, ROOT)
from shoot import serve  # noqa: E402
from profile_space_0916 import SETUP, AUTOPILOT  # noqa: E402

# Named globals on the draw path. Anything absent is reported as such rather than skipped
# silently -- a segment that is quietly missing reads as "free", which is the same false
# negative this whole investigation has been walking into.
CANDIDATES = [
    'drawBG', 'drawPowerups', 'drawSpaceArmoryMines', 'drawScenery',
    'drawEnemy', 'drawBoss', 'drawSubBoss', 'drawBullets', 'drawPlayer',
    'drawEffects', '_drawEffectsInner', 'drawSmokeRings', 'drawNavalFlashes',
    's9WaterDraw', 'l5FieldDraw', 'l5RocksDraw', 'drawS9Void', 'drawS9VoidEnemy',
    'warpFxDraw', '_speedLines', 'drawScanlines', 'drawStarfield',
    'stageSceneryDraw', 'drawAnimTerrain', 'drawLevelMaster', 'orbBeamsDraw',
    'enemyShieldFxDraw', 'drawDeathDebris', 'drawMfx', 'drawHUDStrip',
]

TRAP = r"""
(names) => {
  if (window.__segTrap) return {already:true};
  const missing = [], hooked = [];
  window.__seg = {};
  // ⚠ FORCE THE FLUSH THROUGH THE REAL CONTEXT. getImageData is the cheapest op that cannot be
  // reordered past queued draws; 1x1 keeps the readback itself negligible.
  const flush = function(){ try { ctx.getImageData(0,0,1,1); } catch(_e){} };
  window.__segFlush = flush;

  for (const n of names) {
    const f = window[n];
    if (typeof f !== 'function') { missing.push(n); continue; }
    hooked.push(n);
    window['__segreal_'+n] = f;
    window[n] = function(){
      const t0 = performance.now();
      let r;
      try { r = window['__segreal_'+n].apply(this, arguments); }
      finally {
        flush();
        const S = window.__seg;
        const e = S[n] || (S[n] = {ms:0, calls:0});
        e.ms += performance.now() - t0;
        e.calls++;
      }
      return r;
    };
  }

  // BASELINE: what one flush costs on its own, called once per frame from the loop tail.
  const inner = window.loop;
  window.loop = function(){
    const r = inner.apply(this, arguments);
    const t0 = performance.now();
    flush();
    const S = window.__seg;
    const e = S['(flush baseline)'] || (S['(flush baseline)'] = {ms:0, calls:0});
    e.ms += performance.now() - t0; e.calls++;
    return r;
  };

  window.__segFrames0 = (window.__bofFrames|0);
  window.__segTrap = true;
  return {hooked:hooked.length, missing:missing};
}
"""

REPORT = r"""
() => {
  const S = window.__seg || {};
  const frames = Math.max(1, (window.__bofFrames|0) - (window.__segFrames0|0));
  const rows = Object.keys(S).map(k => ({
    name:k, ms:+(S[k].ms/frames).toFixed(2), calls:+(S[k].calls/frames).toFixed(1),
    msPerCall:+(S[k].ms/Math.max(1,S[k].calls)).toFixed(3)
  })).sort((a,b) => b.ms - a.ms);
  return {frames:frames, rows:rows};
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
        pg.wait_for_timeout(3500)
        info = pg.evaluate(TRAP, CANDIDATES)
        pg.wait_for_timeout(int(args.seconds * 1000))
        rep = pg.evaluate(REPORT)
        b.close()
    stop()

    print('=== stage %d : per-segment cost with a forced flush ===' % args.stage)
    print('  hooked %s of %d; not global: %s'
          % (info.get('hooked'), len(CANDIDATES), ', '.join(info.get('missing', [])[:12])))
    print('  %d drawn frames' % rep['frames'])
    print('')
    print('  %-26s %11s %9s %11s' % ('segment', 'ms/frame', 'calls/fr', 'ms/call'))
    for r in rep['rows'][:16]:
        print('  %-26s %11.2f %9.1f %11.3f' % (r['name'][:26], r['ms'], r['calls'],
                                               r['msPerCall']))
    base = next((r for r in rep['rows'] if r['name'] == '(flush baseline)'), None)
    if base:
        print('')
        print('  subtract ~%.2f ms/segment for the forced flush itself' % base['msPerCall'])


if __name__ == '__main__':
    main()
