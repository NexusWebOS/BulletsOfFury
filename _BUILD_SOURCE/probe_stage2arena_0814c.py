#!/usr/bin/env python3
"""
probe_stage2arena_0814c.py — Mike's items 6 and 7, which live in the same fight.

    python3 _BUILD_SOURCE/probe_stage2arena_0814c.py

  item 6  "Stage 2 boss projectiles - Mike calls them awful."
          `_shipShot` pushes `kind:'eshot'`, which was in NEITHER FIRETYPES nor PROJ, so every
          round every ship boss fires fell through the draw chain to `circle(3.4)` + `circle(1.6)`
          — two flat vector circles. Measured here as: which art keys the volley asks for, and
          how many raw `ctx.arc` calls the bullet pass makes.

  item 7  "Stage came sliding in instead of the lava continuing. Needs a constant-scrolling lava
          section for the fire boss."
          `_bossHold` pins `mapScroll` for the fight, so the bed cycled frames while travelling
          nowhere. Measured as: does the lava scroll advance while the level's does not.

⚠ THE ARC COUNT IS SCOPED TO THE BULLET PASS, NOT THE FRAME. The HUD, the gauge and half a dozen
FX draw arcs every frame; counting the whole frame would report a number that never reaches zero
and means nothing. `ctx.arc` is counted only across `drawEnemyBullets`.

⚠ AND IT ASSERTS THE FALLBACK IS GONE, NOT JUST THAT GOOD ART APPEARED. Those are different
claims: the chain could resolve authored art for SOME rounds and still drop others onto circles,
which is what a partial fix looks like and is invisible if you only check that mfx_ was asked for.
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


SETUP = r"""
() => {
  const out = {ok:false, err:null};
  try {
    ASSETS.ready = true;
    run.pilot = 'cole'; run.stage = 2; curStage = STAGES[1];
    beginStage(2); setState(GS.PLAY); player.reset(); player.invuln = 1e9;
    enemies.length = 0; eBullets.length = 0; pBullets.length = 0;
    spawnBoss(curStage.boss);
    if (!boss) { out.err = 'no stage-2 boss'; return out; }
    boss.enter = false; boss.y = 120;

    /* count arcs ONLY across the enemy-bullet pass, and log every art key it asks for */
    let inBullets = false;
    window.__arcs = 0; window.__keys = new Set();
    const _arc = ctx.arc.bind(ctx);
    ctx.arc = function(){ if (inBullets) window.__arcs++; return _arc.apply(ctx, arguments); };
    const _get = XART.get.bind(XART);
    XART.get = function(k){ if (inBullets) window.__keys.add(k); return _get(k); };
    /* ⚠ THE PASS IS `drawBullets`, AND IT DRAWS BOTH SIDES. There is no `drawEnemyBullets` in
       this engine — the enemy chain is the back half of the same function (the `_ebSmooth` note
       marks where it starts). Scoping to it therefore also catches PLAYER rounds, which is why
       the arc count is only meaningful with pBullets cleared, as the setup above does. */
    const _deb = window.drawBullets;
    if (typeof _deb === 'function') {
      window.drawBullets = function(){ inBullets = true;
        try { return _deb.apply(null, arguments); } finally { inBullets = false; } };
    } else { out.err = 'drawBullets is not a global'; return out; }

    window.__measure = () => {
      const map0 = mapScroll;
      const lava0 = (typeof _arenaLavaScroll !== 'undefined') ? _arenaLavaScroll : null;
      /* ⚠ drawWorld MUST RUN EVERY FRAME, not just at the end: `mapScroll` and the arena's lava
         clock are both advanced inside `drawLevelMaster`, so a loop of bare `updatePlay` measures
         both as +0 and reports the lava as dead. That is the shape of this engine, not a bug. */
      for (let i = 0; i < 240; i++) { updatePlay(1/60); drawWorld(1/60); }   // 4s: several volleys
      pBullets.length = 0;                 // the arc count below is about ENEMY rounds only
      window.__arcs = 0; window.__keys.clear();
      drawWorld(1/60);
      return {
        arcs: window.__arcs,
        keys: [...window.__keys],
        bullets: eBullets.length,
        mapDelta: mapScroll - map0,
        lavaDelta: (lava0 === null) ? null : (_arenaLavaScroll - lava0),
        floorDy: (typeof _masterSrcY !== 'undefined') ? _masterSrcY : null
      };
    };
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
        pg.wait_for_timeout(1800)                       # let the lava and bullet art decode
        m = pg.evaluate("() => window.__measure()")
        png = pg.evaluate(GRAB)
        if png:
            open(os.path.join(PROOF, 'stage2arena_0814c.png'), 'wb').write(
                base64.b64decode(png.split(',', 1)[1]))
        b.close()
    stop()

    art = sorted([k for k in m['keys'] if k.startswith('mfx_')])
    fails = 0

    print('\n=== ITEM 6 - the boss round ===')
    print('  enemy bullets on screen : %d' % m['bullets'])
    print('  authored mfx_ keys asked: %d  %s' % (len(art), ', '.join(art[:5])))
    print('  raw ctx.arc in the pass : %d   (the flat-circle fallback)' % m['arcs'])
    if m['bullets'] <= 0:
        print('  FAIL  the boss fired nothing — nothing was measured'); fails += 1
    elif not art:
        print('  FAIL  no authored projectile art was asked for'); fails += 1
    elif m['arcs'] > 0:
        print('  FAIL  %d rounds still fell through to circles' % m['arcs']); fails += 1
    else:
        print('  OK    authored art, and the circle fallback is never reached')

    print('\n=== ITEM 7 - the lava keeps going ===')
    print('  level scroll over 4s    : %+.1f px  (held by the fight)' % m['mapDelta'])
    print('  lava scroll over 4s     : %s' % ('%+.1f px' % m['lavaDelta'] if m['lavaDelta'] is not None else 'ABSENT'))
    # ⚠ NaN COMPARES FALSE AGAINST EVERYTHING, SO IT PASSED EVERY CHECK BELOW. The first run of
    # this probe called `drawWorld()` with no dt, poisoning mapScroll, and printed "+nan px  OK".
    # A probe that cannot fail on a broken number is not measuring one.
    if any(v is None or v != v for v in (m['mapDelta'], m['lavaDelta'])):
        print('  FAIL  a scroll figure is NaN or absent - nothing was measured'); fails += 1
    elif m['lavaDelta'] < 100:
        print('  FAIL  the lava is not travelling'); fails += 1
    elif m['mapDelta'] >= m['lavaDelta']:
        print('  FAIL  the level is moving as much as the lava - the fight is not holding'); fails += 1
    else:
        print('  OK    the lava flows while the level is held')

    print('\nframe saved to docs/proofs/stage2arena_0814c.png')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
