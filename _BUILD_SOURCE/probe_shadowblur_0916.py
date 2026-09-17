#!/usr/bin/env python3
"""
probe_shadowblur_0916.py - A/B: IS `ctx.shadowBlur` THE COST IN drawBullets?

    python _BUILD_SOURCE/probe_shadowblur_0916.py --stage 9
    python _BUILD_SOURCE/probe_shadowblur_0916.py --stage 1 --weapon 3 --wlevel 5   # the laser

Segment timing with a forced flush puts stage 9's frame at:

    drawBullets   663 ms/frame     (drawMfx 290 ms of it)
    drawBG          3 ms/frame     <- the space background is innocent
    everything else under 3 ms

CLAUDE.md already measured this class once: the Magma Ward's fireballs drew through
`shadowBlur=10` under `'lighter'`, ~32 a frame, at **78 ms/frame**, and caching the glow gave the
same pixels at 2.6 ms. It then records that `drawBullets` still sets `shadowBlur` in 46 places
and names it the next optimisation target.

This is the confirming experiment, not more reasoning: run the same scene twice, identical in
every respect except that the second run makes `ctx.shadowBlur` a no-op, and compare fps.

⚠ THE SUPPRESSED ARM DELIBERATELY LOOKS WRONG. Pinning shadowBlur to 0 removes the glow -- that
  is the point; it is a diagnostic, not a proposed fix. Nothing here is a patch to ship.
"""
import argparse, os, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
sys.path.insert(0, ROOT)
from shoot import serve  # noqa: E402
from profile_space_0916 import SETUP, AUTOPILOT  # noqa: E402

# ⚠ ctx CARRIES ITS OWN PROPERTIES, and CLAUDE.md records that patching
# CanvasRenderingContext2D.prototype traps NOTHING here -- measured, hasOwnProperty(ctx,'drawImage')
# is true. So the override goes on the INSTANCE. shadowBlur is an accessor on the prototype, so
# redefining it on the instance shadows it for every writer.
SUPPRESS = r"""
() => {
  try {
    let sink = 0;
    Object.defineProperty(ctx, 'shadowBlur', {
      configurable: true,
      get(){ return 0; },
      set(v){ sink = v; }          // swallow every write
    });
    window.__sbSuppressed = true;
    return true;
  } catch(e) { return String(e && e.message || e); }
}
"""

COUNT = r"""
() => {
  if (window.__sbCount) return true;
  window.__sbWrites = 0;
  const proto = Object.getPrototypeOf(ctx);
  const d = Object.getOwnPropertyDescriptor(proto, 'shadowBlur');
  if (!d || !d.set) return false;
  Object.defineProperty(ctx, 'shadowBlur', {
    configurable: true,
    get(){ return d.get.call(ctx); },
    set(v){ window.__sbWrites++; d.set.call(ctx, v); }
  });
  window.__sbCount = true;
  return true;
}
"""

# ⚠ THE WRITE COUNT IS NOT THE COST, AND ASSUMING IT WAS COST A WRONG ANSWER.
# Stage 9 writes shadowBlur 167 times a frame at 1.4 fps; stage 1 with the laser writes 135 times
# a frame at 55.6 fps. Nearly the same count, forty times the cost. A shadow's price is the blur
# RADIUS and the AREA under it, so the useful trace records the value written and the size of the
# draw that follows it, bucketed by the JS line that set it.
TRACE = r"""
() => {
  if (window.__sbTrace) return true;
  const proto = Object.getPrototypeOf(ctx);
  const d = Object.getOwnPropertyDescriptor(proto, 'shadowBlur');
  if (!d || !d.set) return false;
  window.__sbBy = {};
  window.__sbCur = 0;
  Object.defineProperty(ctx, 'shadowBlur', {
    configurable: true,
    get(){ return d.get.call(ctx); },
    set(v){
      window.__sbCur = v;
      if (v > 0) {
        let site = '?';
        try {
          const st = (new Error()).stack.split('\n');
          for (let i=1;i<st.length;i++){
            if (st[i].indexOf('game.js') >= 0) {
              const m = st[i].match(/at\s+([^\s(]+).*game\.js:(\d+):/);
              site = m ? (m[1] + ':' + m[2]) : st[i].trim();
              break;
            }
          }
        } catch(_e){}
        const e = window.__sbBy[site] || (window.__sbBy[site] = {n:0, sum:0, max:0, area:0});
        e.n++; e.sum += v; if (v > e.max) e.max = v;
      }
      d.set.call(ctx, v);
    }
  });
  // charge the drawn AREA to whichever site last set a non-zero blur
  const realDraw = ctx.drawImage;
  ctx.drawImage = function(){
    if (window.__sbCur > 0) {
      const a = arguments;
      let w = 0, h = 0;
      if (a.length >= 9) { w = a[7]; h = a[8]; }
      else if (a.length >= 5) { w = a[3]; h = a[4]; }
      else if (a[0]) { w = a[0].naturalWidth || a[0].width || 0; h = a[0].naturalHeight || a[0].height || 0; }
      window.__sbArea = (window.__sbArea || 0) + (w * h);
      window.__sbDraws = (window.__sbDraws || 0) + 1;
    }
    return realDraw.apply(ctx, arguments);
  };
  window.__sbTrace = true;
  return true;
}
"""

TRACE_REPORT = r"""
() => {
  const by = window.__sbBy || {};
  const frames = Math.max(1, (window.__bofFrames|0) - (window.__sbFrames0|0));
  const rows = Object.keys(by).map(k => ({
    site:k, perFrame:+(by[k].n/frames).toFixed(1),
    avg:+(by[k].sum/by[k].n).toFixed(1), max:by[k].max
  })).sort((a,b)=>b.perFrame-a.perFrame);
  return {frames:frames, rows:rows.slice(0,14),
          blurredDrawsPerFrame:+(((window.__sbDraws||0))/frames).toFixed(1),
          blurredMpxPerFrame:+(((window.__sbArea||0)/frames/1e6).toFixed(2))};
}
"""


def run(stage, seconds, pilot, weapon, wlevel, mode):
    """mode: 'normal' | 'count' | 'suppress'"""
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
        r = pg.evaluate(SETUP, {'stage': stage, 'pilot': pilot})
        if not r.get('ok'):
            print('setup failed:', r.get('err')); b.close(); stop(); sys.exit(1)
        pg.evaluate(AUTOPILOT)
        if weapon is not None:
            pg.evaluate("(w) => { run.weapon = w; }", weapon)
        if wlevel is not None:
            pg.evaluate("(l) => { run.wlevel = l; }", wlevel)
        pg.wait_for_timeout(4000)

        if mode == 'suppress':
            got = pg.evaluate(SUPPRESS)
            if got is not True:
                print('  suppress failed:', got)
        elif mode == 'count':
            if not pg.evaluate(COUNT):
                print('  could not count shadowBlur writes')
        elif mode == 'trace':
            if not pg.evaluate(TRACE):
                print('  could not trace shadowBlur')
            pg.evaluate("() => { window.__sbFrames0 = (window.__bofFrames|0); }")

        f0 = pg.evaluate("() => (window.__bofFrames|0)")
        t0 = time.time()
        pg.wait_for_timeout(int(seconds * 1000))
        wall = time.time() - t0
        f1 = pg.evaluate("() => (window.__bofFrames|0)")
        writes = pg.evaluate("() => (window.__sbWrites|0)")
        trace = pg.evaluate(TRACE_REPORT) if mode == 'trace' else None
        b.close()
    stop()
    frames = f1 - f0
    return frames / wall if wall else 0, frames, writes, trace


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=int, default=9)
    ap.add_argument('--seconds', type=float, default=7)
    ap.add_argument('--pilot', default='cole')
    ap.add_argument('--weapon', type=int, default=None)
    ap.add_argument('--wlevel', type=int, default=None)
    ap.add_argument('--trace', action='store_true')
    args = ap.parse_args()

    label = 'stage %d' % args.stage
    if args.weapon is not None:
        label += ' weapon %d tier %s' % (args.weapon, args.wlevel)

    print('=== %s ===' % label)
    fps_n, fr_n, _, _t = run(args.stage, args.seconds, args.pilot, args.weapon, args.wlevel,
                             'normal')
    print('  shipped                  %6.1f fps  (%d frames)' % (fps_n, fr_n))

    fps_c, fr_c, writes, _t = run(args.stage, args.seconds, args.pilot, args.weapon,
                                  args.wlevel, 'count')
    per_frame = (writes / fr_c) if fr_c else 0
    print('  counting writes          %6.1f fps  -- %d shadowBlur writes, %.0f per frame'
          % (fps_c, writes, per_frame))

    fps_s, fr_s, _, _t = run(args.stage, args.seconds, args.pilot, args.weapon, args.wlevel,
                             'suppress')
    print('  shadowBlur SUPPRESSED    %6.1f fps  (%d frames)' % (fps_s, fr_s))

    if fps_n > 0:
        print('')
        print('  >>> suppressing shadowBlur is %.1fx faster (%.1f -> %.1f fps)'
              % (fps_s / fps_n, fps_n, fps_s))
        if fps_s / fps_n < 1.5:
            print('  >>> that is NOT the dominant cost here -- look elsewhere before caching glows')

    if args.trace:
        _f, _fr, _w, tr = run(args.stage, args.seconds, args.pilot, args.weapon, args.wlevel,
                              'trace')
        if tr:
            print('')
            print('  blurred draws: %.1f per frame, %.2f Mpx per frame under a shadow'
                  % (tr['blurredDrawsPerFrame'], tr['blurredMpxPerFrame']))
            print('  %-54s %9s %7s %6s' % ('site that set shadowBlur', 'per frame', 'avg', 'max'))
            for r in tr['rows']:
                print('  %-54s %9.1f %7.1f %6.0f' % (r['site'][:54], r['perFrame'], r['avg'],
                                                     r['max']))


if __name__ == '__main__':
    main()
