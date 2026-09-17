#!/usr/bin/env python3
"""
probe_fusion_0917.py - FUSION, IN REAL CHROMIUM.

Mike, 0917: "surprise me with some fun upgrades".

A level-3 element replaced by a DIFFERENT one detonates once across the screen before the new
element takes the gun: every on-screen hostile takes the burst and BOTH elements' touch, named by
the pair (fire+ice is THERMAL SHOCK). Picking the same element again still just caps, and a
level-2 element replaced does nothing - the fusion is the reward for holding a named combination
and trading it away.
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

ARM = """() => { player.dead=false; window.playerHit=function(){}; for(const e of enemies) e.dead=true; pBullets.length=0; eBullets.length=0; floaters.length=0; run._fusionN=0;
  for(let i=0;i<4;i++){ const e=spawnEnemy('drone',{x:90+i*100,y:170}); e.x=90+i*100; e.y=170; e.shoots=false; e.hp=300; e.maxhp=300; e.vx=0; e.vy=0; e._burn=0; e._frozen=0; }
  return enemies.filter(e=>!e.dead).length; }"""
READ = """() => ({ n: run._fusionN|0, inf: run.infusion ? run.infusion.elem+':'+run.infusion.lv : null,
  hp: enemies.filter(e=>!e.dead).map(e=>e.hp), burn: enemies.filter(e=>!e.dead).map(e=>+(e._burn>0)), frozen: enemies.filter(e=>!e.dead).map(e=>e._frozen|0),
  txt: floaters.map(f=>f.txt), flash: wrathFlash })"""

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof infusionFusion==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 2, 'pilot': 'cole'})
        for _ in range(3):
            pg.evaluate(sh.STEP, [10]); pg.wait_for_timeout(400)

        ok(pg.evaluate("() => infusionFusionName('fire','ice')==='THERMAL SHOCK' && infusionFusionName('ice','fire')==='THERMAL SHOCK' && infusionFusionName('toxic','kinetic')==='FUSION'"),
           'the pair is named both ways round, and an unnamed pair is a plain FUSION')

        # ---- fire L3 -> ice: THERMAL SHOCK -----------------------------------------------------------
        n0 = pg.evaluate(ARM)
        pg.evaluate("() => { run.infusion=null; infusionGrant('fire'); infusionGrant('fire'); infusionGrant('fire'); }")
        pg.evaluate("() => { infusionGrant('ice'); }")
        r = pg.evaluate(READ)
        ok(r['n'] == 1 and r['inf'] == 'ice:1', 'fire L3 replaced by ice FUSES once, then ice takes the gun at level 1 (%s, %s)' % (r['n'], r['inf']))
        ok(len(r['hp']) == 4 and all(h < 300 for h in r['hp']), 'every hostile on screen takes the burst (%s)' % r['hp'])
        ok(all(r['burn']) and all(f >= 1 for f in r['frozen']), 'and BOTH elements\' touch - burning AND a freeze stack (%s / %s)' % (r['burn'], r['frozen']))
        ok('THERMAL SHOCK' in r['txt'] and r['flash'] > 0, 'named THERMAL SHOCK, with the white-out (%s)' % r['txt'])
        pg.evaluate(sh.STEP, [2]); shot(pg, '13_thermal_shock.png')

        # ---- controls ---------------------------------------------------------------------------------
        pg.evaluate(ARM)
        pg.evaluate("() => { run.infusion=null; infusionGrant('fire'); infusionGrant('fire'); infusionGrant('ice'); }")
        r2 = pg.evaluate(READ)
        ok(r2['n'] == 0 and r2['inf'] == 'ice:1' and all(h == 300 for h in r2['hp']), 'CONTROL: fire L2 replaced by ice does NOT fuse (%s, %s)' % (r2['n'], r2['inf']))
        pg.evaluate(ARM)
        pg.evaluate("() => { run.infusion=null; infusionGrant('fire'); infusionGrant('fire'); infusionGrant('fire'); infusionGrant('fire'); }")
        r3 = pg.evaluate(READ)
        ok(r3['n'] == 0 and r3['inf'] == 'fire:3', 'CONTROL: the same element again just caps at 3, no fusion (%s, %s)' % (r3['n'], r3['inf']))
        # chrome in the pair mirrors the screen
        pg.evaluate(ARM)
        pg.evaluate("() => { for(let i=0;i<10;i++) eBullets.push({x:40+i*40, y:120, vx:0, vy:2, kind:'pellet', dead:false, r:3}); run.infusion=null; infusionGrant('chrome'); infusionGrant('chrome'); infusionGrant('chrome'); infusionGrant('lightning'); }")
        r4 = pg.evaluate("() => ({ n: run._fusionN|0, dead: eBullets.filter(q=>q.dead).length, mirrors: pBullets.filter(q=>q._mirror).length, txt: floaters.map(f=>f.txt) })")
        ok(r4['n'] == 1 and r4['dead'] == 10 and r4['mirrors'] == 10 and 'TESLA MIRROR' in r4['txt'], 'chrome L3 + lightning = TESLA MIRROR, and the whole screen is mirrored (%s)' % r4)

        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]: print('    !', e)
        br.close(); stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
