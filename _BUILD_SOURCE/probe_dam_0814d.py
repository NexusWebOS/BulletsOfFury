#!/usr/bin/env python3
"""
probe_dam_0814d.py — Mike's item 5: "Stage 1 does not move the camera to the blown-up dam after
the helicopter boss dies."

    python3 _BUILD_SOURCE/probe_dam_0814d.py

MEASURED, not argued:

  1. WHERE IS THE DAM? Taken by diffing `jungle800_v3_intact.png` against
     `jungle800_v3_destroyed.png` — the rows that change ARE the dam, so this cannot be wrong
     about which part of the plate matters.
  2. WHERE IS THE CAMERA when the boss fight holds the scroll? `_masterSrcY` is the top visible
     master row and the level publishes it (0813c), so this is what the frame actually shows.
  3. DOES THE DAM EVER ENTER THE FRAME between the boss dying and the flyover taking over?

⚠ THE DAM IS AT THE TOP OF THE PLATE, i.e. at the END of the level: srcY DECREASES as a stage
runs, so the plate is consumed bottom-to-top. "The camera does not move to the dam" therefore
means srcY never reaches 0 — the dam sits above the visible window for the whole fight and the
stage ends without it ever being seen.
"""
import os, sys, base64, http.server, socketserver, threading, functools

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
PROOF = os.path.join(GAME, 'docs', 'proofs')


def serve(directory, port=0):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a, **k: None
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd.server_address[1], httpd.shutdown


def dam_band():
    """the rows where the two plates disagree strongly = the dam itself"""
    from PIL import Image, ImageChops
    import numpy as np
    a = Image.open(os.path.join(GAME, 'assets/game/jungle800_v3_intact.png')).convert('RGB')
    b = Image.open(os.path.join(GAME, 'assets/game/jungle800_v3_destroyed.png')).convert('RGB')
    d = np.array(ImageChops.difference(a, b)).sum(axis=2)
    rows = (d > 90).sum(axis=1)
    # ⚠ A LOW THRESHOLD SPREADS THE ANSWER ACROSS THE WHOLE PLATE. At `rows>20` this reported the
    # dam as master rows 0..2332 — half the level — because the two renders also differ mildly all
    # the way down the channel. The DAM is where they differ MOST, so take the rows carrying at
    # least a quarter of the peak row's changed pixels.
    peak = rows.max()
    nz = np.nonzero(rows >= max(40, peak * 0.25))[0]
    return (int(nz.min()), int(nz.max()), a.size[1]) if len(nz) else (None, None, a.size[1])


SETUP = r"""
() => {
  const out = {ok:false, err:null};
  try {
    ASSETS.ready = true;
    run.pilot = 'cole'; run.stage = 1; curStage = STAGES[0];
    beginStage(1); setState(GS.PLAY); player.reset(); player.invuln = 1e9;
    enemies.length = 0; eBullets.length = 0;

    /* run the level to the point the boss triggers, the way play does */
    /* ⚠ THE MINIBOSS FREEZES STAGE PROGRESSION (`stageTimer -= dt` while subBossActive), and a
       probe shoots nothing, so the boss NEVER arrives — 20,000 frames of simulated play returned
       `reached=false` and read as a broken trigger. Clear the mini the way a player would, so the
       stage clock runs on. */
    window.__toBoss = () => {
      let g = 0, minis = 0;
      while (!bossActive && g++ < 30000) {
        updatePlay(1/60); drawWorld(1/60);
        if (typeof subBossActive !== 'undefined' && subBossActive && subBoss && !subBoss.dead) {
          subBoss.hp = 0; subBoss.dead = true; subBoss.dying = 0; minis++;
        }
      }
      return { reached: bossActive, frames: g, minis, srcY: _masterSrcY, map: mapScroll };
    };
    window.__hold = (n) => {
      for (let i = 0; i < n; i++) { updatePlay(1/60); drawWorld(1/60); }
      return { srcY: _masterSrcY, map: mapScroll, state: state,
               dying: (boss ? boss.dying : -1), ending: stageEnding, broken: damBroken };
    };
    window.__kill = () => { if (boss) { boss.hp = 0; hitBoss(1); if (!boss.dead) bossDie(); } };
    out.ok = true;
  } catch(e){ out.err = String(e && e.message || e); }
  return out;
}
"""

GRAB = ("() => { const g = document.querySelector('#screen-area canvas')"
        " || document.querySelector('canvas'); return g ? g.toDataURL('image/png') : null; }")


def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(PROOF, exist_ok=True)

    d0, d1, plateH = dam_band()
    VH = 512
    print('the dam, measured by diffing the two plates:')
    print('  master rows %s..%s of %d   (top of the plate = END of the level)' % (d0, d1, plateH))

    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        r = pg.evaluate(SETUP)
        if not r.get('ok'):
            print('setup failed:', r.get('err')); b.close(); stop(); sys.exit(2)
        pg.wait_for_timeout(2000)

        arrive = pg.evaluate("() => window.__toBoss()")
        print('\nboss trigger:')
        print('  reached=%s after %d frames   visible master rows %.0f..%.0f' %
              (arrive['reached'], arrive['frames'], arrive['srcY'], arrive['srcY'] + VH))
        if not arrive['reached']:
            print('  the boss never triggered - nothing further was measured')
            b.close(); stop(); sys.exit(2)

        pg.evaluate("() => window.__kill()")
        samples = []
        for label, n in (('t=2s', 120), ('t=5s', 180), ('t=8s', 180), ('t=11s', 180)):
            s = pg.evaluate("(n) => window.__hold(n)", n)
            samples.append((label, s))
        png = pg.evaluate(GRAB)
        if png:
            open(os.path.join(PROOF, 'dam_0814d.png'), 'wb').write(base64.b64decode(png.split(',', 1)[1]))
        b.close()
    stop()

    print('\nafter the boss dies:')
    print('  %-6s %10s %10s %8s %8s %s' % ('t', 'srcY', 'dam in?', 'state', 'broken', 'dying'))
    seen = False
    for label, s in samples:
        top, bot = s['srcY'], s['srcY'] + VH
        inframe = (d1 is not None) and (top <= d1) and (bot >= d0)
        seen = seen or inframe
        print('  %-6s %10.0f %10s %8s %8s %.1f' %
              (label, top, 'YES' if inframe else 'no', s['state'], s['broken'], s['dying']))

    print('\ndam visible at any point after the kill: %s' % ('YES' if seen else 'NO'))
    print('frame saved to docs/proofs/dam_0814d.png')
    sys.exit(0 if seen else 1)


if __name__ == '__main__':
    main()
