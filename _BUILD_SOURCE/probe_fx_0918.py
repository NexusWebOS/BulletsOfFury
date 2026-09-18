#!/usr/bin/env python3
"""
probe_fx_0918.py - the generated effects, in real Chromium on a live stage.

  1. a level-IV INCENDIARY machine gun fired (pShoot) into live drones: the fire BURST is spawned by
     infusionOnHit and drawn, the burning units wear the animated FIRE, and the art keys asked for prove it
     (XART.get wrapped, the KEY recorded - never .src, CLAUDE.md);
  2. all nine element bursts laid out mid-animation for the eye;
  3. the three geysers raised to full height - they must draw the generated column, reach GEYSER_H, and
     hurt a unit standing in their lane;
  4. 0 page / console errors.
Frames: docs/proofs/fx_0918/.
"""
import os, sys, base64, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'fx_0918')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)
KEYS = ['efx_burst_%s' % e for e in ['fire','ice','lightning','prism','toxic','kinetic','water','chrome','dark']] + ['efx_burn'] + ['efx_geyser_%s' % g for g in ['fire','water','lightning']]

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=90000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=90000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 2, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; }" % sh.STEP)
        def step(n): pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", n)
        def shot(name):
            d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
            if d: open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        pg.evaluate("(ks) => ks.forEach(k=>XART.rdy(k))", KEYS)
        for _ in range(30):
            if pg.evaluate("(ks) => ks.every(k=>XART.rdy(k))", KEYS): break
            pg.wait_for_timeout(250)
        ok(pg.evaluate("(ks) => ks.every(k=>XART.rdy(k))", KEYS), 'all 13 generated effect strips decode')
        rec = "() => { window.__keys={}; const o=XART.get; window.__oget=o; XART.get=function(k){ window.__keys[k]=(window.__keys[k]|0)+1; return o.apply(this,arguments); }; }"
        unrec = "() => { XART.get=window.__oget; return window.__keys; }"

        # ---- 1. the incendiary gun into live drones
        pg.evaluate("() => { enemies.length=0; eBullets.length=0; run.weapon=0; run.wlevel=3; run.infusion={elem:'fire',lv:4,hits:0};"
                    " for(let i=0;i<4;i++){ try{ const e=spawnEnemy('drone', player.x-90+i*60, 170); if(e){ e.shoots=false; e.hp=e.maxhp=400; e.vx=0; e.vy=0; } }catch(_){ } }"
                    " for(const e of enemies){ e.shoots=false; e.hp=400; e.maxhp=400; } }")
        pg.evaluate(rec)
        for i in range(40):
            pg.evaluate("() => { for(const e of enemies){ e.vx=0; e.vy=0; if(e.y>200) e.y=170; } player.fireCd=0; pShoot(); window.__step(1); window.__step(1); }")
        k = pg.evaluate(unrec)
        st = pg.evaluate("() => ({bursts:efxBursts.length, burning:enemies.filter(e=>e._burn>0).length, alive:enemies.length})")
        print('  gun:', json.dumps(st), {x: k.get(x, 0) for x in ['efx_burst_fire', 'efx_burn']})
        ok(k.get('efx_burst_fire', 0) > 0, 'the incendiary rounds draw the generated FIRE BURST where they land (%d blits)' % k.get('efx_burst_fire', 0))
        ok(k.get('efx_burn', 0) > 0 and st['burning'] > 0, 'burning units wear the animated FIRE (%d blits, %d burning)' % (k.get('efx_burn', 0), st['burning']))
        shot('01_incendiary_hits')

        # ---- 2. all nine bursts, mid-animation
        pg.evaluate("() => { enemies.length=0; efxBursts=[]; const L=camLeftX(); const E=['fire','ice','lightning','prism','toxic','kinetic','water','chrome','dark']; E.forEach((e,i)=>{ const b=efxBurst(e, L+80+(i%3)*150, 110+Math.floor(i/3)*120, 96); b.t=0.12; }); }")
        pg.evaluate(rec); step(1); k = pg.evaluate(unrec)
        drawn = [e for e in ['fire','ice','lightning','prism','toxic','kinetic','water','chrome','dark'] if k.get('efx_burst_' + e, 0) > 0]
        ok(len(drawn) == 9, 'all nine element bursts draw (%s)' % drawn)
        shot('02_all_bursts')

        # ---- 3. the geysers
        pg.evaluate("() => { efxBursts=[]; geysers=[]; const L=camLeftX(); geyserSpawn(L+100,470,'fire'); geyserSpawn(L+240,470,'water'); geyserSpawn(L+380,470,'lightning');"
                    " try{ const e=spawnEnemy('drone', L+100, 300); if(e){ e.shoots=false; e.hp=e.maxhp=500; window.__gt=e; } }catch(_){ } }")
        hp0 = pg.evaluate("() => window.__gt ? window.__gt.hp : -1")
        pg.evaluate(rec)
        for _ in range(20):
            pg.evaluate("() => { if(window.__gt){ window.__gt.vx=0; window.__gt.vy=0; window.__gt.y=300; window.__gt.x=camLeftX()+100; } window.__step(1); }")
        k = pg.evaluate(unrec)
        G = pg.evaluate("() => geysers.map(g=>({k:g.kind, h:Math.round(g.h)}))")
        hp1 = pg.evaluate("() => window.__gt ? window.__gt.hp : -1")
        print('  geysers:', json.dumps(G), 'target hp', hp0, '->', hp1)
        ok(all(k.get('efx_geyser_' + g, 0) > 0 for g in ['fire', 'water', 'lightning']), 'all three geysers draw the generated column')
        ok(G and all(g['h'] >= 300 for g in G), 'and erupt to take up a section of the screen (%s)' % [g['h'] for g in G])
        ok(hp1 < hp0, 'a unit standing in the fire geyser lane is burned (%s -> %s)' % (hp0, hp1))
        shot('03_geysers')
        for _ in range(90): step(1)   # a geyser lives GEYSER_LIFE + 0.2 s = 1.7 s
        ok(pg.evaluate("() => geysers.length") == 0, 'and the geysers end')

        real = [e for e in errs if 'favicon' not in e]
        ok(not real, 'page/console errors: %d %s' % (len(real), real[:3]))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL ' + f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
