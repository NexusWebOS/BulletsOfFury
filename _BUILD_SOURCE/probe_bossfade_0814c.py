#!/usr/bin/env python3
"""
probe_bossfade_0814c.py — Mike's item 8: "Bosses do not die into explosions - they should vanish
with the explosion taking over. Only stage 1 does this."

    python3 _BUILD_SOURCE/probe_bossfade_0814c.py

WHAT IT MEASURES, per stage, in real Chromium on real frames: **how much the boss DRAW puts on
the canvas at each moment of its death**, and whether the explosion is still running when it
stops.

`ctx.drawImage` is wrapped and counted only for the duration of the `drawBoss()` call, so the
figure is the boss's own contribution and nothing else's — the HUD, the terrain and the blasts
are all outside the window.

    t=0.5s   solid    the hull is fully drawn, first blasts landing
    t=3.0s   ZERO     the hull is gone
             and explosions/particles are still non-zero, i.e. it VANISHED rather than
             everything having stopped

⚠ THE SECOND HALF OF THAT IS THE POINT. "0 boss pixels" is also what a frozen game looks like, so
the live explosion count is what separates "the explosion took over" from "nothing is happening".

⚠ AND IT DOES NOT ASK `bossDeathAlpha` WHAT IT THINKS. A probe that recomputes the thing under
test asserts its own arithmetic — CLAUDE.md records probe_seam.py doing exactly that and calling
a 160px offset clean. This counts draw calls the real frame made.
"""
import os, sys, http.server, socketserver, threading, functools

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))


def serve(directory, port=0):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a, **k: None
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd.server_address[1], httpd.shutdown


RUN = r"""
(cfg) => {
  const out = {ok:false, err:null, kind:null};
  try {
    ASSETS.ready = true;
    run.stage = cfg.stage; run.pilot = 'cole';
    curStage = STAGES[cfg.stage-1];
    beginStage(cfg.stage); setState(GS.PLAY);
    player.reset(); player.invuln = 1e9;
    enemies.length = 0; eBullets.length = 0; pBullets.length = 0;

    spawnBoss(curStage.boss);
    if (!boss) { out.err = 'no boss for stage ' + cfg.stage; return out; }
    out.kind = boss.kind || curStage.boss;
    boss.enter = false;                 // skip the entrance; the death is what is under test
    boss.y = 140;

    /* count drawImage ONLY while drawBoss is running, so the figure is the boss's own draw */
    let inBoss = false, n = 0;
    const _di = ctx.drawImage.bind(ctx);
    ctx.drawImage = function(){ if (inBoss) n++; return _di.apply(ctx, arguments); };
    const _db = window.drawBoss;
    window.drawBoss = function(){ inBoss = true; try { return _db.apply(null, arguments); }
                                  finally { inBoss = false; } };

    /* ⚠ `hitBoss` CANNOT KILL A MODULAR BOSS (probe fault, drop 0814c). Its first lines are
       `if(boss.modular){ modularHit(dmg); return; }` — it returns BEFORE the `hp<=0 -> bossDie()`
       check, because a modular unit dies when its parts are ruined, not on a pool. Killing stage
       8 that way left `dead` false and `dying` at 0 forever, which the probe reported as the
       stage-8 boss refusing to die. It was the probe refusing to kill it.
       The game's own force-kill is `boss.hp=0; bossDie();` — use that. */
    window.__killBoss = () => { boss.hp = 0; hitBoss(1); if (!boss.dead) bossDie(); };
    window.__sample = (secs) => {
      /* step to an absolute point in the death clock, then take ONE frame's boss draw count.
         ⚠ HARD-CAPPED. The first cut was `while (boss.dying < secs)` with no bound, and a stage
         whose boss never advances that clock hangs the page — which surfaces as the whole probe
         timing out with no output at all, i.e. as a broken harness rather than as a finding. */
      let guard = 0;
      while (boss && boss.dying < secs && guard++ < 4000) { updatePlay(1/60); }
      const stalled = (guard >= 4000);
      n = 0;
      drawWorld();
      return { drawn: n, stalled,
               dying: boss ? boss.dying : -1,
               explosions: (typeof explosions !== 'undefined') ? explosions.length : -1,
               particles: (typeof particles !== 'undefined') ? particles.length : -1 };
    };
    out.ok = true;
  } catch(e) { out.err = String(e && e.message || e); }
  return out;
}
"""


def main():
    from playwright.sync_api import sync_playwright

    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    rows, fails = [], 0

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        for stage in range(1, 9):
            pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
            pg.goto(url, wait_until='load', timeout=60000)
            pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=45000)
            pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)

            r = pg.evaluate(RUN, {'stage': stage})
            if not r.get('ok'):
                print('stage %d setup failed: %s' % (stage, r.get('err')))
                fails += 1; pg.close(); continue

            pg.wait_for_timeout(1200)                    # let the boss art decode
            pg.evaluate("() => window.__killBoss()")
            early = pg.evaluate("(s) => window.__sample(s)", 0.5)
            late = pg.evaluate("(s) => window.__sample(s)", 3.0)

            alive = max(late['explosions'], late['particles'])
            stalled = early.get('stalled') or late.get('stalled')
            good = (early['drawn'] > 0 and late['drawn'] == 0 and alive > 0 and not stalled)
            if not good:
                fails += 1
            rows.append((stage, r.get('kind'), early['drawn'], late['drawn'], alive, good,
                         'STALLED' if stalled else ''))
            pg.close()
        b.close()
    stop()

    print('\n%-6s %-18s %10s %10s %14s' %
          ('STAGE', 'BOSS', 't=0.5s', 't=3.0s', 'FX still live'))
    print('-' * 74)
    for (stage, kind, e, l, alive, good, note) in rows:
        print('%-6d %-18s %10d %10d %14d   %s %s' %
              (stage, kind or '?', e, l, alive, 'OK ' if good else 'FAIL', note))
    print('\nt=0.5s / t=3.0s are drawImage calls made BY drawBoss in that one frame.')
    print('The hull must be solid early, ZERO late, with the explosion still running.')
    print('%d of %d stages hand the boss over to its explosion' % (len(rows) - fails, len(rows)))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
