#!/usr/bin/env python3
"""
probe_infusion_carriers_0917.py - THE LASER AND THE MISSILES WEAR THE ELEMENT, IN REAL CHROMIUM.

Mike, 0917: "Combinations could be incendiary bullets, lightning bullets, ice bullets or lasers or
missiles."

The MG and spread already went through p87Draw with the element's palette. This drives the other two
carriers: a live beam (the ONE persistent beam object) and a real missile, and asks the palette
helper what it was asked to build - identified by KEY and by the element's own body colour, the way
this repo identifies every blit (XART.get returns a canvas with no .src).
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

TRAP = """() => {
  window.__pal = [];
  const o = xartPalette;
  window.__palOrig = o;
  xartPalette = function(k, m){ window.__pal.push([k, m]); return o(k, m); };
}"""

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof infusionGrant==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 2, 'pilot': 'cole'})
        for _ in range(4):
            pg.evaluate(sh.STEP, [10]); pg.wait_for_timeout(400)
        pg.evaluate("() => { player.dead=false; player.invuln=0; for(const e of enemies) e.shoots=false; window.playerHit=function(){}; }")
        # warm the beam reel and the pilot's missile plate, then WAIT (rdy is false on its first call)
        pg.evaluate("() => { for(let f=0;f<6;f++) XART.rdy('nlz_2_b'+f); XART.rdy(pilotMissileKey(false)); }")
        pg.wait_for_function("() => XART.rdy('nlz_2_b0') && XART.rdy(pilotMissileKey(false))", timeout=20000)
        pg.evaluate(TRAP)

        # ---- the beam -----------------------------------------------------------------------------
        fire_body = pg.evaluate("() => INFUSIONS.fire.body")
        pg.evaluate("() => { run.infusion=null; infusionGrant('fire'); run.weapon=3; run.wlevels[3]=2; run.wlevel=2; pBullets.length=0; }")
        w3 = pg.evaluate("() => WEAPONS[3] && (WEAPONS[3].kind||WEAPONS[3].name||WEAPONS[3])")
        pg.evaluate("() => { player.fireCd=0; pShoot(); }")
        pg.evaluate(sh.STEP, [2])
        beam = pg.evaluate("() => { const b=pBullets.find(q=>q.kind==='beam'); return b?{inf:b._inf, lv:b.lv}:null; }")
        ok(beam and beam['inf'] == 'fire', 'a live beam carries the infusion (%s, slot 3 = %s)' % (beam, w3))
        asks = pg.evaluate("() => window.__pal.filter(p => /^nlz_/.test(p[0]))")
        ok(any(a[1] == fire_body for a in asks), 'and the beam plate was palette-swapped to FIRE\'s body colour (%d beam swaps, %s)' % (len(asks), sorted(set(a[1] for a in asks))))
        shot(pg, '03_fire_beam.png')
        # a new pickup RE-stamps the same persistent beam
        pg.evaluate("() => { run.infusion=null; infusionGrant('ice'); window.__pal=[]; }")
        pg.evaluate(sh.STEP, [2])
        beam2 = pg.evaluate("() => { const b=pBullets.find(q=>q.kind==='beam'); return b?b._inf:null; }")
        ice_body = pg.evaluate("() => INFUSIONS.ice.body")
        asks2 = pg.evaluate("() => window.__pal.filter(p => /^nlz_/.test(p[0])).map(p=>p[1])")
        ok(beam2 == 'ice' and ice_body in asks2, 'picking ICE re-stamps the SAME beam object and it swaps to ice (%s, %s)' % (beam2, sorted(set(asks2))))
        pg.evaluate("() => { for(const b of pBullets) if(b.kind==='beam') b.dead=true; pBullets.length=0; }")

        # ---- the missiles ------------------------------------------------------------------------
        mk = pg.evaluate("() => pilotMissileKey(false)")
        pg.evaluate("() => { run.infusion=null; infusionGrant('lightning'); window.__pal=[]; pBullets.push({kind:'missile', x:player.x, y:player.y-40, vx:0, vy:-6, ang:-Math.PI/2, dmg:10, t:0.1, seat:1}); }")
        pg.evaluate(sh.STEP, [2])
        m = pg.evaluate("() => { const b=pBullets.find(q=>q.kind==='missile'); return b?b._inf:null; }")
        lb = pg.evaluate("() => INFUSIONS.lightning.body")
        asks3 = pg.evaluate("() => window.__pal")
        ok(m == 'lightning', 'a missile carries the infusion (%s)' % m)
        ok(any(a[0] == mk and a[1] == lb for a in asks3), 'and the pilot\'s missile plate (%s) was swapped to LIGHTNING\'s body (%s)' % (mk, sorted(set(a[1] for a in asks3))))
        shot(pg, '04_lightning_missile.png')
        # control: no infusion, no swap of the missile plate
        pg.evaluate("() => { run.infusion=null; pBullets.length=0; window.__pal=[]; pBullets.push({kind:'missile', x:player.x, y:player.y-40, vx:0, vy:-6, ang:-Math.PI/2, dmg:10, t:0.1, seat:1}); }")
        pg.evaluate(sh.STEP, [2])
        asks4 = pg.evaluate("() => window.__pal.filter(p => p[0]===%r)" % mk)
        ok(len(asks4) == 0, 'CONTROL: with no infusion the missile plate is not swapped (%d)' % len(asks4))

        pg.evaluate("() => { xartPalette = window.__palOrig; }")
        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]: print('    !', e)
        br.close(); stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
