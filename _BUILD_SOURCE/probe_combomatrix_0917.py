#!/usr/bin/env python3
"""
probe_combomatrix_0917.py - EVERY CARRIER x EVERY ELEMENT, photographed in the live game.

Mike: "what you can combine and the lists and all ... I need to see the projectiles, the icons."

An infusion is not a weapon slot - it layers an element onto whatever CARRIER is held. So the
thing to show is the MATRIX: five carriers down, nine elements across, each cell a real frame of
the real rounds in flight.

⚠ FIRED THROUGH THE REAL TRIGGER (`BOSSMODE.hold`), never `player.fireCd = 0; pShoot()`. The
forced route fires once per FRAME - 10x the real cadence, measured in probe_firerate_0917.py -
and a screen of rounds at 10x density is not a picture of the weapon.

⚠ BOTH GATED ELEMENTS ARE OPENED HONESTLY: water needs the LASER MIST unlock and dark needs
NEW GAME +, so the probe sets the run flags those gates read rather than editing the gate.

⚠ AND THE LASER IS ONE PERSISTENT 'beam' OBJECT, so its cell is captured while the beam BURNS
rather than after a volley - the other four carriers emit a round per beat.
"""
import os, sys, base64, io, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

OUT = os.path.join(ROOT, 'docs', 'proofs', 'combos_0917')
ELEMS = ['fire', 'ice', 'lightning', 'prism', 'toxic', 'kinetic', 'chrome', 'water', 'dark']
#  (weapon slot, level, label)
CARRIERS = [(0, 3, 'MACHINE GUN'), (1, 3, 'SPREAD'), (3, 3, 'LASER'), (2, 3, 'MISSILES'), (5, 3, 'ORB')]
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    cells = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof infusionGrant==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        # open BOTH gates the way the game opens them, not by editing infusionGateOpen
        pg.evaluate("""() => {
          window.playerHit=function(){}; run.lives=9; enemies.length=0; mapScroll=2400;
          run.ngplus = true;
          try{ if(typeof laserMistUnlock==='function') laserMistUnlock(); }catch(_){}
          if(typeof run.laserMist!=='undefined') run.laserMist = true;
        }""")
        pg.evaluate("() => { XART.rdy('nwp_lfi_laser_start'); XART.rdy('fx0825_ice_orb'); for(let f=0;f<6;f++) XART.rdy('nlz_3_b'+f); }")
        for _ in range(7):
            pg.evaluate(sh.STEP, [8]); pg.wait_for_timeout(430)

        pool = pg.evaluate("() => infusionPool()")
        print('  element pool with both gates open:', pool)
        ok(len(pool) == 9, 'all nine elements are reachable once the gates are open (%d)' % len(pool))

        key = pg.evaluate("() => { const b=BOSSMODE.binds(); return (b&&b.fire&&b.fire[0])||'j'; }")
        pg.evaluate("() => { window.__step = %s; }" % sh.STEP)

        for w, lv, cname in CARRIERS:
            for el in ELEMS:
                pg.evaluate("""([w, lv, el]) => {
                  run.weapon=w; run.wlevels[w]=lv; run.wlevel=lv;
                  run.missileLevel = (w===2)?lv:0;
                  for(const b of pBullets) b.dead=true; pBullets.length=0;
                  if(typeof zaps!=='undefined') zaps.length=0;
                  run.infusion=null; for(let i=0;i<3;i++) infusionGrant(el);
                  player.x=worldWidth()*0.5; player.y=430; player.fireCd=0;
                }""", [w, lv, el])
                pg.evaluate("([k]) => BOSSMODE.hold(k,true)", [key])
                # long enough for several beats of the slowest carrier to be in the air at once
                pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", 46)
                d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
                st = pg.evaluate("() => ({n:pBullets.length, inf:run.infusion?run.infusion.elem+':'+run.infusion.lv:null,"
                                 " tagged:pBullets.filter(b=>b._inf).length})")
                pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [key])
                im = Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGBA')
                bg = Image.new('RGBA', im.size, (0, 0, 0, 255)); bg.paste(im, (0, 0), im)
                cells[(cname, el)] = (bg, st)
            print('  %-12s done' % cname, flush=True)

        # every cell must have had the element ON the rounds, not merely in run.infusion
        bad = [(c, e) for (c, e), (_, st) in cells.items() if st['tagged'] == 0]
        ok(not bad, 'every carrier/element cell had rounds WEARING the element (%d blank: %s)'
           % (len(bad), bad[:6]))
        print('  errors:', len(errs))
        for e in errs[:5]: print('   !', e[:180])
        ok(len(errs) == 0, 'no page or console errors (%d)' % len(errs))
        br.close()
    stop()

    # crop the firing lane: the ship sits at y 430 of 512, rounds travel up
    W, H = cells[(CARRIERS[0][2], ELEMS[0])][0].size
    sx, sy = W // 2, int(H * 0.86)
    CW, CH = 210, 300
    HDR = 22
    sheet = Image.new('RGB', (CW * len(ELEMS) + 130, (CH + HDR) * len(CARRIERS) + HDR), (10, 10, 14))
    d = ImageDraw.Draw(sheet)
    for c, el in enumerate(ELEMS):
        d.text((130 + c * CW + 6, 5), el.upper(), fill=(255, 236, 160))
    for r, (w, lv, cname) in enumerate(CARRIERS):
        y = HDR + r * (CH + HDR)
        d.text((6, y + CH // 2), cname, fill=(180, 220, 255))
        for c, el in enumerate(ELEMS):
            im = cells[(cname, el)][0]
            box = (max(0, sx - CW // 2), max(0, sy - CH), min(W, sx + CW // 2), min(H, sy))
            sheet.paste(im.crop(box).convert('RGB'), (130 + c * CW, y))
    p = os.path.join(OUT, '_combo_matrix.png')
    sheet.save(p); print('  ->', p, sheet.size)
    json.dump({'elements': ELEMS, 'carriers': [c[2] for c in CARRIERS]},
              open(os.path.join(OUT, '_index.json'), 'w'), indent=2)
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
