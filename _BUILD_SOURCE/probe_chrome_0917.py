#!/usr/bin/env python3
"""
probe_chrome_0917.py - CHROMIUM and the cross-element GEYSERS, in real Chromium.

Mike, 0917: "chromium energy upgrades" and "new geyser attacks like Fire, Water and Lightning geyser
type effects".

CHROMIUM: a hit mirrors enemy rounds near the impact back up the screen as the player's own; at level
3 a KILL mirrors every round on screen. Asserted on the pools: eBullets lose them, pBullets gain them,
and the gained ones are stamped _mirror and fly UP. GEYSERS: a soaked target (water has hit it) killed
by fire raises a FIRE geyser; by lightning a LIGHTNING geyser; water at level 3 its own.
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

ARM = """() => {
  player.dead=false; player.invuln=0; window.playerHit=function(){};
  for(const e of enemies){ e.dead=true; }
  pBullets.length=0; eBullets.length=0; geysers.length=0;
}"""
SPAWN = """(hp) => { const e=spawnEnemy('drone',{x:240,y:200}); e.x=240; e.y=200; e.shoots=false; e.hp=hp; e.maxhp=hp; e._fresh=false; e._noOneShot=false; return e; }"""

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof chromeMirror==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 2, 'pilot': 'cole'})
        for _ in range(3):
            pg.evaluate(sh.STEP, [10]); pg.wait_for_timeout(400)

        ok(pg.evaluate("() => INFUSIONS.chrome && INFUSIONS.chrome.named[3]==='MIRROR SHELL' && infusionPool().indexOf('chrome')>=0"),
           'CHROMIUM is in the table and in the pool (no gate)')
        ok(pg.evaluate("() => /infusion_0917/.test(XART._src['inf_chrome']||'')"), 'its badge is registered')

        # ---- level 1: a hit mirrors the rounds NEAR the impact, and only those ----------------------
        pg.evaluate(ARM)
        pg.evaluate("""() => { run.infusion=null; infusionGrant('chrome');
            const e = (%s)(400);
            for(let i=0;i<6;i++) eBullets.push({x:e.x-20+i*8, y:e.y+10, vx:0, vy:2, kind:'pellet', dead:false, r:3});
            eBullets.push({x:e.x+200, y:e.y+150, vx:0, vy:2, kind:'pellet', dead:false, r:3});   // far away: must survive
            window.__e=e; }""" % SPAWN)
        r = pg.evaluate("""() => { const e=window.__e; _dmgBullet={kind:'mg',_inf:'chrome',x:e.x,y:e.y+5,vx:0,vy:-8,dmg:4}; hitEnemy(e,4); _dmgBullet=null;
            return {deadNear: eBullets.slice(0,6).filter(q=>q.dead).length, farAlive: !eBullets[6].dead,
                    mirrors: pBullets.filter(q=>q._mirror).length, up: pBullets.filter(q=>q._mirror&&q.vy<0).length}; }""")
        ok(r['deadNear'] == 6 and r['farAlive'], 'level 1: the six rounds beside the impact are mirrored, the far one is not (%s)' % r)
        ok(r['mirrors'] == 6 and r['up'] == 6, 'and six mirror shards leave, all flying UP (%s)' % r)
        pg.evaluate(sh.STEP, [1]); shot(pg, '05_chrome_mirror.png')

        # ---- level 3 kill: MIRROR SHELL turns the whole screen ---------------------------------------
        pg.evaluate(ARM)
        pg.evaluate("""() => { run.infusion=null; infusionGrant('chrome'); infusionGrant('chrome'); infusionGrant('chrome');
            const e = (%s)(1);
            for(let i=0;i<30;i++) eBullets.push({x:20+i*15, y:60+(i%%7)*50, vx:0, vy:2, kind:'pellet', dead:false, r:3});
            window.__e=e; }""" % SPAWN)
        r3 = pg.evaluate("""() => { const e=window.__e; _dmgBullet={kind:'mg',_inf:'chrome',x:e.x,y:e.y+5,vx:0,vy:-8,dmg:50}; hitEnemy(e,50); hitEnemy(e,50); _dmgBullet=null;
            return {lv: run.infusion.lv, dead: eBullets.filter(q=>q.dead).length, mirrors: pBullets.filter(q=>q._mirror).length, killed: !!(e.dead||e._dyingT!=null)}; }""")
        ok(r3['lv'] == 3 and r3['killed'] and r3['dead'] == 30 and r3['mirrors'] == 30, 'level 3 MIRROR SHELL on a kill: all 30 rounds on screen mirrored (%s)' % r3)

        # ---- the geysers ----------------------------------------------------------------------------
        for elem, expect in (('fire', 'fire'), ('lightning', 'lightning')):
            pg.evaluate(ARM)
            pg.evaluate("""() => { run.infusion=null; infusionGrant('%s'); infusionGrant('%s'); const e=(%s)(1); e._soaked=2.0; window.__e=e; }""" % (elem, elem, SPAWN))
            g = pg.evaluate("""() => { const e=window.__e; _dmgBullet={kind:'mg',_inf:'%s',x:e.x,y:e.y+5,vx:0,vy:-8,dmg:50}; hitEnemy(e,50); hitEnemy(e,50); _dmgBullet=null;
                return geysers.map(q=>q.kind); }""" % elem)
            ok(g == [expect], 'a SOAKED target killed by %s raises a %s geyser (%s)' % (elem, expect, g))
        pg.evaluate(ARM)
        pg.evaluate("""() => { run.infusion=null; infusionGrant('fire'); infusionGrant('fire'); const e=(%s)(1); window.__e=e; }""" % SPAWN)
        g0 = pg.evaluate("""() => { const e=window.__e; _dmgBullet={kind:'mg',_inf:'fire',x:e.x,y:e.y+5,vx:0,vy:-8,dmg:50}; hitEnemy(e,50); hitEnemy(e,50); _dmgBullet=null; return geysers.length; }""")
        ok(g0 == 0, 'CONTROL: a DRY target killed by fire raises none (%d)' % g0)
        # the geyser hurts what crosses it
        pg.evaluate(ARM)
        h = pg.evaluate("""() => { geyserSpawn(240,300,'lightning'); const e=(%s)(60); e.x=240; e.y=240; const hp0=e.hp;
            for(let i=0;i<20;i++) geyserTick(1/60); return [hp0, e.hp, geysers[0].kind]; }""" % SPAWN)
        ok(h[1] < h[0], 'a lightning geyser hurts a unit standing in its column (%s)' % h)
        pg.evaluate(sh.STEP, [1]); shot(pg, '06_lightning_geyser.png')

        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]: print('    !', e)
        br.close(); stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
