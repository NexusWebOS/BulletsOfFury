#!/usr/bin/env python3
"""
probe_lasarab_0916.py - INTERLEAVED A/B OF THE BAKED GLOW, IN ONE BROWSER SESSION.

    python _BUILD_SOURCE/probe_lasarab_0916.py --stage 9
    python _BUILD_SOURCE/probe_lasarab_0916.py --stage 5 --rounds 4

WHY INTERLEAVED, AND WHY THIS REPLACES THE EARLIER NUMBERS
  Sequential runs on this machine drift. The same build, same stage, measured minutes apart, gave
  43.5 and then 34.3 fps; the control stage ranged 34.8 to 56.5 across the session. Any before/after
  taken as two separate runs is therefore reporting machine load as much as the change.

  Both code paths already exist in the shipped build: `drawBullets` uses the baked plate when
  `spaceLaserGlowCanvas` returns one, and falls back to the original per-round `shadowBlur` when it
  returns null. So the A/B needs no patching and no second build -- stubbing that one function
  selects the OLD path exactly, in the same page, seconds apart. The arms alternate and repeat, so
  a drift that affects one affects both.

⚠ THE FALLBACK ARM IS THE REAL OLD CODE, not an imitation of it: it is the same `ctx.shadowColor` /
  `ctx.shadowBlur=7` / `drawImage(lp, ...)` the file shipped before this drop, kept deliberately as
  the path a context that refuses a scratch canvas would take.
"""
import argparse, os, statistics, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
sys.path.insert(0, ROOT)
from shoot import serve  # noqa: E402
from profile_space_0916 import SETUP, AUTOPILOT  # noqa: E402

ARM = r"""
(useBaked) => {
  if (!window.__abReal) {
    if (typeof spaceLaserGlowCanvas !== 'function') return 'no spaceLaserGlowCanvas';
    window.__abReal = spaceLaserGlowCanvas;
  }
  // window[name] assignment works here because game.js declares these with `function`, whose
  // binding IS a property of the global object (unlike its `const`s -- see the ASSETS note).
  window.spaceLaserGlowCanvas = useBaked ? window.__abReal : function(){ return null; };
  return true;
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=int, default=9)
    ap.add_argument('--rounds', type=int, default=4)
    ap.add_argument('--secs', type=float, default=4.0)
    ap.add_argument('--pilot', default='cole')
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright
    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    old, new = [], []
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

        got = pg.evaluate(ARM, True)
        if got is not True:
            print(got); b.close(); stop(); sys.exit(1)

        # ⚠ COUNT THE LASER ROUNDS ALIVE IN EACH WINDOW, OR THE OLD ARM LOOKS FINE AT RANDOM.
        # The cost is per ROUND ON SCREEN. A 4-second window that happens to catch a lull -- the
        # ship between bursts, or rounds that have all flown off the top -- measures the old path
        # at 60 fps, which is true and completely uninformative. The first run of this A/B
        # reported "old" at 0.7, 8.2, 8.7 and then 60.0, and only the round count explains it.
        SAMPLE = """() => {
            let n = 0;
            try { for (const b of pBullets) if (b && b.kind === 'spaceLaser' && !(b._launchDelay > 0)) n++; }
            catch(_e){}
            return n;
        }"""

        def measure():
            f0 = pg.evaluate("() => (window.__bofFrames|0)")
            t0 = time.time()
            peak = 0
            steps = max(1, int(args.secs / 0.4))
            for _ in range(steps):
                pg.wait_for_timeout(400)
                peak = max(peak, pg.evaluate(SAMPLE))
            w = time.time() - t0
            f1 = pg.evaluate("() => (window.__bofFrames|0)")
            return ((f1 - f0) / w if w else 0), peak

        print('  stage %d, %d rounds x %.1fs per arm, alternating' % (args.stage, args.rounds,
                                                                     args.secs))
        for i in range(args.rounds):
            # ⚠ ALTERNATE THE ORDER each round so a warm-up or a cool-down cannot favour one arm.
            order = [(False, old), (True, new)] if (i % 2 == 0) else [(True, new), (False, old)]
            for baked, bucket in order:
                pg.evaluate(ARM, baked)
                pg.wait_for_timeout(600)      # let the field settle after the switch
                bucket.append(measure())
            print('    round %d:  old %5.1f fps (peak %3d rounds)   new %5.1f fps (peak %3d rounds)'
                  % (i + 1, old[-1][0], old[-1][1], new[-1][0], new[-1][1]))
        b.close()
    stop()

    # Only windows that actually had laser rounds on screen say anything about this change.
    LIVE = 20
    o_live = [f for f, n in old if n >= LIVE]
    n_live = [f for f, n in new if n >= LIVE]
    print('')
    if not o_live or not n_live:
        print('  NOT ENOUGH LOADED WINDOWS (need >= %d live rounds in both arms).' % LIVE)
        print('  old windows: %s' % ', '.join('%.1f fps/%d' % (f, n) for f, n in old))
        print('  new windows: %s' % ', '.join('%.1f fps/%d' % (f, n) for f, n in new))
        return
    mo, mn = statistics.median(o_live), statistics.median(n_live)
    print('  counting only windows with >= %d laser rounds on screen:' % LIVE)
    print('  OLD (per-round shadowBlur)  median %5.1f fps   from %d windows  range %.1f - %.1f'
          % (mo, len(o_live), min(o_live), max(o_live)))
    print('  NEW (baked halo plate)      median %5.1f fps   from %d windows  range %.1f - %.1f'
          % (mn, len(n_live), min(n_live), max(n_live)))
    if mo > 0:
        print('')
        print('  >>> %.1fx faster' % (mn / mo))


if __name__ == '__main__':
    main()
