#!/usr/bin/env python3
"""probe_deathspin_0907y.py - the player death spin-out, driven in real Chromium.

    python _BUILD_SOURCE/probe_deathspin_0907y.py
    python _BUILD_SOURCE/probe_deathspin_0907y.py --bust

Mike's header rule, 0907: "when we get hit, we spin while explosions anchor and fire anchor on us
and animate as we spin about 540-900 degrees and -crash- and die. secondly, when this occurs, we
get a shock ring and explosions used as part of the players blow up."

Every clause is one assertion, and each is written so it CAN fail:

  SPINS         distinct `_sp*` frames are requested, and the reel goes round - not one frame held
  540-900       the angle actually turned is inside Mike's range, computed from the reel index
  ANCHORED      an explosion's x/y MOVES WITH the player. ⚠ This is the whole point and it is the
                one thing a screenshot cannot show: the pre-0907 death spawned its fire at fixed
                world points, which looks identical on a still and is wrong the moment the wreck
                travels. Measured as the correlation between the player's displacement and the
                explosion's, so an effect that merely EXISTS near the ship still fails.
  CRASH LAST    no shock ring exists while the ship is still turning, and one exists after. The
                old code fired `fxBurst(...rings:2)` on the frame of the hit; asserting only that
                a ring appears SOMEWHERE would pass on that build, so the probe asserts the ring
                is ABSENT during the spin as well.

⚠ `--bust` FORCES THE OLD BEHAVIOUR (the ring at the hit, the fire unanchored) AND THE PROBE MUST
GO RED. A probe that has only ever been green is not evidence - this file's own rule.
"""
import os, sys, json, http.server, socketserver, threading, functools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8207

JS = r"""
(async () => {
  const out = {keys:[], samples:[], errors:[]};
  // wrap XART.get and record the KEY - 0906e: a blit's SIZE cannot tell you whose art it is
  const _get = XART.get.bind(XART);
  XART.get = function(k){ if(typeof k==='string' && k.indexOf('_sp')>0) out.keys.push(k); return _get(k); };

  run.lives = 5;
  player.dead = false; player.invuln = 0; player._spin = null;
  player.x = PLAY.x + PLAY.w*0.5; player.y = PLAY.y + PLAY.h*0.55;
  if (window.__BUST) { window.__BUSTED = true; }

  const rings = () => particles.filter(p=>p.flashring).length;
  playerHit();
  const spun = !!player._spin;
  /* ⚠ READ `turns` NOW, NOT AT THE END. The respawn clears `player._spin`, so sampling it after
     the loop reported "none" on a build that had just spun 779 degrees - the probe outliving the
     state it was measuring. */
  const turnsDeg = player._spin ? player._spin.turns : null;

  // step the real loop in small chunks with a genuine pause between them, so anything the
  // death asks for can actually decode (0905: a frame count is not a clock)
  // ⚠ LONG ENOUGH TO REACH THE CRASH. The first cut stepped 26 frames - 0.43s against a 1.25s
  // spin plus a 0.55s crash beat - so the window closed before the blow-up and the probe reported
  // "0 rings" on a build whose ring was firing perfectly. A probe that stops before the thing it
  // is testing happens will fail correct code.
  for (let i=0;i<130;i++){
    const before = {px:player.x, py:player.y,
                    ex:(explosions[0]?explosions[0].x:null), ey:(explosions[0]?explosions[0].y:null),
                    id:(explosions[0]||null)};
    updatePlay(1/60); drawWorld(1/60);
    out.samples.push({t:i/60,
      spinT: player._spin ? player._spin.t : null,
      crashed: player._spin ? !!player._spin.crashed : null,
      anchors: player._spin ? player._spin.anchor.length : 0,
      rings: rings(),
      px: player.x, py: player.y,
      ex: (explosions[0]?explosions[0].x:null), ey:(explosions[0]?explosions[0].y:null),
      nexp: explosions.length});
    await new Promise(r=>setTimeout(r,16));
  }
  out.spun = spun;
  out.turns = turnsDeg;
  XART.get = _get;
  return out;
})()
"""


def main():
    from playwright.sync_api import sync_playwright
    bust = '--bust' in sys.argv
    os.chdir(ROOT)
    H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(('127.0.0.1', PORT), H)
    srv.RequestHandlerClass.log_message = lambda *a, **k: None
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    errs = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 900, 'height': 900})
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)))
        pg.goto('http://127.0.0.1:%d/index.html' % PORT)
        pg.wait_for_timeout(1200)
        pg.evaluate("() => { for(const k in BOFX.ships) XART.rdy(k); }")
        pg.wait_for_function("() => { const s=XART.get('ship_cole_sp0'); return !!(s&&s.width); }",
                             timeout=15000)
        pg.wait_for_timeout(1200)
        pg.evaluate("() => { beginStage(1); setState(GS.PLAY); }")
        pg.wait_for_timeout(900)
        if bust:
            pg.evaluate("() => { window.__BUST=1; window.deathSpinAvailable = () => false; }")
        res = pg.evaluate(JS)
        b.close()
    srv.shutdown()

    S = res['samples']
    keys = sorted(set(res['keys']))
    frames = sorted(set(int(k.rsplit('_sp', 1)[1]) for k in keys if k.rsplit('_sp', 1)[1].isdigit()))
    spinning = [s for s in S if s['spinT'] is not None and not s['crashed']]
    after = [s for s in S if s['crashed']]
    ring_during = max([s['rings'] for s in spinning], default=0)
    ring_after = max([s['rings'] for s in after], default=0)

    # ANCHORED: does an explosion travel with the player?
    moved_p = moved_e = 0
    for a, b2 in zip(S, S[1:]):
        if a['ex'] is None or b2['ex'] is None:
            continue
        dp = abs(b2['px'] - a['px']) + abs(b2['py'] - a['py'])
        de = abs(b2['ex'] - a['ex']) + abs(b2['ey'] - a['ey'])
        if dp > 0.05:
            moved_p += 1
            if de > 0.05:
                moved_e += 1
    anchored = moved_p > 0 and moved_e / float(moved_p) > 0.6

    def ok(cond, name, detail=''):
        print('  %-46s %s   %s' % (name, 'OK ' if cond else 'FAIL', detail))
        return bool(cond)

    print('death spin: started=%s  turns=%s  frames seen=%s' %
          (res['spun'], ('%.0f deg' % res['turns']) if res['turns'] else '-', frames))
    print()
    good = True
    good &= ok(res['spun'], 'the death starts a spin', '')
    good &= ok(len(frames) >= 5, 'the reel actually turns', '%d distinct sp frames' % len(frames))
    good &= ok(res['turns'] is not None and 540 <= res['turns'] <= 900,
               'the turn is inside Mike\'s 540-900', ('%.0f deg' % res['turns']) if res['turns'] else 'none')
    good &= ok(anchored, 'the fire is ANCHORED to the ship',
               '%d of %d moving frames carried it' % (moved_e, moved_p))
    good &= ok(ring_during == 0, 'no shock ring while it is still spinning', '%d' % ring_during)
    good &= ok(ring_after > 0, 'the shock ring lands on the CRASH', '%d rings' % ring_after)
    good &= ok(max([s['anchors'] for s in S], default=0) > 3, 'effects are held on the wreck',
               'peak %d anchored' % max([s['anchors'] for s in S], default=0))
    good &= ok(not errs, 'no console errors or pageerrors', str(errs[:2]))
    print()
    print('RESULT:', 'PASS' if good else 'FAIL', '  (--bust arm)' if bust else '')
    return 0 if good else 1


if __name__ == '__main__':
    sys.exit(main())
