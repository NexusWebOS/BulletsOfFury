#!/usr/bin/env python3
"""
probe_giantbeam_0917.py - THE GIANT BEAM, IN REAL CHROMIUM.

Mike, 0917: "giant laser beams like the fireboss has".

A KINETIC infusion on the laser widens the column x1.5 / x2.0 / x2.5. Three things have to agree
or it is a picture of a wide beam over a thin one: the beam object's width, the width the draw
blits (read off the context's OWN drawImage - a prototype trap records nothing, 0905h), and the
hit test - a unit 38px off the beam's centre line (the drone is 29 wide, so the plain beam's reach is
11+14.5=25.5px and the level-3 giant's 27.5+14.5=42) is missed by the plain beam and burned by the giant one.
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

ARM = """() => { player.dead=false; player.invuln=0; window.playerHit=function(){};
  for(const e of enemies) e.dead=true; pBullets.length=0; eBullets.length=0; stageTimer=5;
  run.weapon=3; run.wlevels[3]=2; run.wlevel=2; player.fireCd=0; }"""
TRAP = """() => { window.__blits=[]; const o=ctx.drawImage; window.__diOrig=o;
  ctx.drawImage=function(im){ const a=arguments; window.__blits.push({w: a.length>=9 ? a[7] : a[3], h: a.length>=9 ? a[8] : a[4], iw: im&&im.width, ih: im&&im.height}); return o.apply(this,a); }; }"""

def fire(pg):
    pg.evaluate("() => { player.fireCd=0; pShoot(); }")
    return pg.evaluate("() => { const b=pBullets.find(q=>q.kind==='beam'); return b ? {w:b.w, lv:b.lv, inf:b._inf} : null; }")

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
        for _ in range(3):
            pg.evaluate(sh.STEP, [10]); pg.wait_for_timeout(400)
        pg.evaluate("() => { for(let f=0;f<6;f++) XART.rdy('nlz_2_b'+f); }")
        pg.wait_for_function("() => XART.rdy('nlz_2_b0')", timeout=20000)

        # ---- the object -------------------------------------------------------------------------------
        pg.evaluate(ARM); pg.evaluate("() => { run.infusion=null; }")
        plain = fire(pg)
        ok(plain and abs(plain['w'] - 22) < 0.01, 'plain level-2 beam is 22 wide (14+lv*4) (%s)' % plain)
        widths = []
        for n in (1, 2, 3):
            pg.evaluate(ARM); pg.evaluate("() => { run.infusion=null; for(let i=0;i<%d;i++) infusionGrant('kinetic'); }" % n)
            widths.append(fire(pg)['w'])
        ok([round(w, 2) for w in widths] == [33, 44, 55], 'KINETIC widens it x1.5 / x2.0 / x2.5 by level (%s)' % [round(w, 1) for w in widths])
        pg.evaluate(ARM); pg.evaluate("() => { run.infusion=null; infusionGrant('fire'); }")
        f = fire(pg)
        ok(f and abs(f['w'] - 22) < 0.01, 'CONTROL: a FIRE infusion leaves the width alone (%s)' % f)

        # ---- the draw ---------------------------------------------------------------------------------
        def blit_w(inf_n):
            pg.evaluate(ARM); pg.evaluate("() => { run.infusion=null; for(let i=0;i<%d;i++) infusionGrant('kinetic'); }" % inf_n)
            fire(pg); pg.evaluate(TRAP); pg.evaluate(sh.STEP, [1])
            ws = pg.evaluate("() => window.__blits.filter(b => b.iw===XART.get('nlz_2_b0').width && b.h>200).map(b => b.w)")
            pg.evaluate("() => { ctx.drawImage = window.__diOrig; }")
            return ws
        w0 = blit_w(0); w3 = blit_w(3)
        ok(w0 and w3 and abs(w3[0] / w0[0] - 2.5) < 0.05, 'and the beam plate is BLITTED 2.5x wider at level 3 (%s -> %s)' % (w0, w3))
        shot(pg, '08_giant_beam.png')

        # ---- the hit test -----------------------------------------------------------------------------
        def burns(inf_n):
            pg.evaluate(ARM); pg.evaluate("() => { run.infusion=null; for(let i=0;i<%d;i++) infusionGrant('kinetic'); }" % inf_n)
            return pg.evaluate("""() => { const e=spawnEnemy('drone',{x:player.x+38,y:220}); e.x=player.x+38; e.y=220; e.shoots=false; e.hp=900; e.maxhp=900; e.vx=0; e.vy=0;
                const hp0=e.hp; for(let i=0;i<20;i++){ player.fireCd=0; pShoot(); updatePlay(1/60); }
                return [hp0, e.hp, Math.round(e.x-player.x)]; }""")
        b0 = burns(0); b3 = burns(3)
        ok(b0[1] == b0[0], 'a unit 38px off the centre line is MISSED by the plain beam - reach 25.5 (%s)' % b0)
        ok(b3[1] < b3[0], 'and BURNED by the giant one - reach 42, the hit test reads the same width (%s)' % b3)

        # ---- SONIC WAVE: kinetic level 3 on the machine gun releases Cole's wave every 24th round ----
        def waves(inf_n, rounds=60):
            pg.evaluate(ARM); pg.evaluate("() => { run.weapon=0; run.wlevels[0]=2; run.wlevel=2; run._kinN=0; run.infusion=null; for(let i=0;i<%d;i++) infusionGrant('kinetic'); }" % inf_n)
            return pg.evaluate("""(n) => { let waves=0; for(let i=0;i<n;i++){ player.fireCd=0; pShoot(); updatePlay(1/60); waves+=pBullets.filter(q=>q.kind==='sonic'&&!q._seen).map(q=>{q._seen=1;return 1;}).length; } return [waves, run._kinN|0]; }""", rounds)
        w3 = waves(3); w2 = waves(2)
        # the proof frame: kill the persistent beam left by the earlier cases, fire exactly 24 kinetic rounds
        # and read the frame with the wave in flight
        pg.evaluate(ARM); pg.evaluate("() => { for(const b of pBullets) b.dead=true; pBullets.length=0; run.weapon=0; run.wlevels[0]=2; run.wlevel=2; run._kinN=0; run.infusion=null; for(let i=0;i<3;i++) infusionGrant('kinetic'); }")
        pg.evaluate("() => { for(let i=0;i<24;i++){ player.fireCd=0; pShoot(); updatePlay(1/60); } }")
        pg.evaluate(sh.STEP, [3])
        live = pg.evaluate("() => pBullets.filter(q=>q.kind==='sonic'&&!q.dead).length")
        ok(live >= 1, 'a sonic wave is in flight for the proof frame (%d)' % live)
        ok(w3[0] >= 2 and w3[1] >= 48, 'KINETIC L3 on the machine gun releases a SONIC WAVE every 24th round (%d waves from %d rounds)' % (w3[0], w3[1]))
        ok(w2[0] == 0, 'CONTROL: level 2 releases none (%d)' % w2[0])
        shot(pg, '10_sonic_wave.png')

        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]: print('    !', e)
        br.close(); stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
