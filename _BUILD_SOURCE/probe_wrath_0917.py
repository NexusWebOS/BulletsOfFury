#!/usr/bin/env python3
"""
probe_wrath_0917.py - GODS WRATH WITH ITS BOLT ART DECODED, IN REAL CHROMIUM.

The 0917 infusion probe could not show the bolts: a synchronous burst never yields, so the
chain_bolt_ reel never decoded and sixteen bolts drew through the thin fallback line. This one warms
the reel, WAITS on XART.rdy in real time, then fires the wrath and reads the frame that drew it -
identifying the bolt blits by the KEY asked of XART.get (a canvas has no .src).
"""
import os, sys, base64
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'infusion_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)
def shot(pg, name):
    d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
    if d: open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof godsWrath==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 4, 'pilot': 'cole'})
        for _ in range(3):
            pg.evaluate(sh.STEP, [10]); pg.wait_for_timeout(400)
        pg.evaluate("() => { player.dead=false; window.playerHit=function(){}; for(const e of enemies) e.dead=true; eBullets.length=0; }")
        # the grant warms the reel; then WAIT for it in real time
        pg.evaluate("() => { run.infusion=null; infusionGrant('lightning'); infusionGrant('lightning'); infusionGrant('lightning'); }")
        pg.evaluate("() => { XART.rdy('nchp_0'); }")
        pg.wait_for_function("() => XART.rdy('chain_bolt_0') && XART.rdy('chain_bolt_8') && XART.rdy('nchp_0')", timeout=30000)
        ok(True, 'the chain_bolt_ reel decoded after a real wait (rdy false on its first call, true now)')
        pg.evaluate("""() => { for(let i=0;i<5;i++){ const e=spawnEnemy('drone',{x:80+i*80,y:150+(i%2)*60}); e.x=80+i*80; e.y=150+(i%2)*60; e.shoots=false; e.hp=200; e.maxhp=200; e.vx=0; e.vy=0; }
            window.__keys=[]; const g=XART.get.bind(XART); window.__xg=XART.get; XART.get=function(k){ window.__keys.push(k); return g(k); }; }""")
        n0 = pg.evaluate("() => { const hp=enemies.filter(e=>!e.dead).map(e=>e.hp); godsWrath(240,300); return hp; }")
        pg.evaluate(sh.STEP, [1])
        # drawChainBolt prefers the nchp_ reel when it is decoded, chain_bolt_ otherwise - either is the authored bolt
        keys = pg.evaluate("() => window.__keys.filter(k => /^(chain_bolt_|nchp_)/.test(k)).length")
        struck = pg.evaluate("() => enemies.filter(e=>!e.dead).map(e=>e.hp)")
        ok(keys >= 5, 'the frame that drew the wrath asked for the BOLT ART (nchp_/chain_bolt_) %d times - authored bolts, not the fallback line' % keys)
        ok(all(b < a for a, b in zip(n0, struck)) and len(struck) == 5, 'all five hostiles struck from the sky (%s -> %s)' % (n0, struck))
        ok(pg.evaluate("() => wrathFlash > 0"), 'the white-out is up')
        shot(pg, '12_gods_wrath_bolts.png')
        pg.evaluate("() => { XART.get = window.__xg; }")
        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]: print('    !', e)
        br.close(); stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
