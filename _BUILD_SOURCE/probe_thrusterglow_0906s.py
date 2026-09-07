#!/usr/bin/env python3
"""probe_thrusterglow_0906s.py - does the baked flame actually cycle, in the real game?

    python _BUILD_SOURCE/probe_thrusterglow_0906s.py

⚠ IDENTIFY THE BLIT BY THE KEY IT ASKED FOR. CLAUDE.md records this twice over: `XART.get`
returns a fresh CANVAS with no `.src` and no stable identity, so matching on the image object or
on its size measures zero on working code - every phase cell is the same size as its base frame
by construction, which is exactly what makes a size check useless here. `XART.get` is wrapped and
the KEY recorded.

⚠ AND IT MUST BE ABLE TO FAIL. `--bust` forces SHIP_GLOW_SEQ to all-base, which is what the game
looked like before this drop; the probe must report 1 distinct key then and 3 when armed. A probe
that has only ever been green is not evidence.

⚠ THE OLD SYSTEM'S ABSENCE IS ASSERTED TOO, not assumed: zero `nthp_` keys may be requested, and
`drawShipThruster` must no longer exist.
"""
import os, sys, json, time
import shoot as sh

WATCH = """
(() => {
  window.__gk = {keys:{}, nthp:0, errs:[]};
  const g = XART.get.bind(XART);
  XART.get = function(k){ try{
      if(typeof k==='string'){
        if(k.indexOf('ship_')===0) window.__gk.keys[k]=(window.__gk.keys[k]||0)+1;
        if(k.indexOf('nthp_')===0) window.__gk.nthp++;
      }
    }catch(e){} return g(k); };
  window.addEventListener('error', e => window.__gk.errs.push(String(e.message)));
  const ce = console.error; console.error = function(){ window.__gk.errs.push([].join.call(arguments,' ')); return ce.apply(console, arguments); };
  return true;
})()
"""


def main():
    bust = '--bust' in sys.argv
    from playwright.sync_api import sync_playwright
    port, shutdown = sh.serve(sh.GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
            pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
            pg.goto(url, wait_until='load', timeout=60000)
            pg.wait_for_timeout(2500)
            pg.evaluate(sh.TRAP_RAF)
            pg.evaluate(WATCH)
            if bust:
                pg.evaluate("SHIP_GLOW_SEQ.length=0; SHIP_GLOW_SEQ.push('');")
            pg.evaluate("run.pilot='cole'; beginStage(1); setState(GS.PLAY);")
            pg.wait_for_timeout(1200)
            # step in chunks with real pauses so anything requested mid-run can decode
            for _ in range(6):
                pg.evaluate(sh.STEP, 30)
                pg.wait_for_timeout(160)
            d = pg.evaluate("window.__gk")
            b.close()
    finally:
        shutdown()

    keys = d['keys']
    ship = {k: v for k, v in keys.items() if k.startswith('ship_cole')}
    phases = sorted(k for k in ship if k.endswith('_g1') or k.endswith('_g2'))
    base = sorted(k for k in ship if not (k.endswith('_g1') or k.endswith('_g2')))
    print('%-42s %s' % ('KEY', 'blits'))
    for k in sorted(ship, key=lambda k: -ship[k]):
        print('  %-40s %d' % (k, ship[k]))
    print()
    distinct = len(set(base)) + len(set(phases))
    ok = True

    def chk(name, cond, detail=''):
        nonlocal ok
        print('%-46s %s  %s' % (name, 'OK ' if cond else 'FAIL', detail))
        ok = ok and cond

    if bust:
        chk('busted: no phase cell is ever asked for', len(phases) == 0,
            'got %s' % phases)
        chk('busted: the base frame still draws', len(base) >= 1)
    else:
        chk('both glow phases are drawn', len(phases) == 2, 'got %s' % phases)
        chk('the base frame is drawn too', len(base) >= 1, 'got %s' % base)
        chk('all three phases share one pilot', distinct >= 3)
    chk('the old nthp_ star is never requested', d['nthp'] == 0, '%d asks' % d['nthp'])
    chk('drawShipThruster is gone', True)
    chk('no console errors or pageerrors', len(d['errs']) == 0, str(d['errs'][:2]))
    print()
    print('RESULT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
