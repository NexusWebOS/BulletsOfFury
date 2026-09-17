#!/usr/bin/env python3
"""
probe_lasermuzzle_0917.py - the laser muzzle, OLD vs NEW, at every tier and on the giant beam.

Mike: "we need generated laser muzzle's for the pilots, that looks bad."

Nothing was generated. `nwp_lfi_laser_start` is an authored laser origin flare that had never
been drawn; it replaces the two `ctx.arc` circles. This renders both paths side by side at all
five laser tiers plus the KINETIC giant beam, which is the case he photographed.

⚠ THE BUSTED ARM IS THE POINT. A probe that has only ever been green is not evidence (CLAUDE.md),
so the OLD path is forced by reassigning `laserMuzzleArt` to return null - a top-level function
declaration is a reassignable binding - and both pictures are saved from the same build.

⚠ AND IT FIRES THROUGH THE REAL TRIGGER (`BOSSMODE.hold`), never `player.fireCd=0; pShoot()`.
The forced route fires at 60Hz whatever the cadence says - measured at 10x the real rate in
probe_firerate_0917.py - and a muzzle flash photographed at 10x cadence is not the muzzle flash.
"""
import os, sys, base64, io, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

OUT = os.path.join(ROOT, 'docs', 'proofs', 'lasermuzzle_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

CASES = [(1, None, 'LASER L1'), (2, None, 'LASER L2'), (3, None, 'LASER L3'),
         (4, None, 'LASER L4'), (5, None, 'LASER L5'), (3, 'kinetic', 'GIANT BEAM (kinetic L3)')]

def grab(pg):
    d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
    im = Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGBA')
    bg = Image.new('RGBA', im.size, (0, 0, 0, 255)); bg.paste(im, (0, 0), im)
    return bg

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    shots = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof laserMuzzleArt==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.playerHit=function(){}; run.lives=9; enemies.length=0; mapScroll=2400; }")
        pg.evaluate("() => { XART.rdy('nwp_lfi_laser_start'); XART.rdy('nwp_lfi_laser_hit'); }")
        for _ in range(6):
            pg.evaluate(sh.STEP, [8]); pg.wait_for_timeout(450)
        rdy = pg.evaluate("() => XART.rdy('nwp_lfi_laser_start')")
        ok(rdy, 'the authored muzzle plate nwp_lfi_laser_start is registered and decoded')
        art = pg.evaluate("() => { const a=laserMuzzleArt('#7fd0ff'); return a?{w:a.width,h:a.height}:null; }")
        ok(art is not None, 'laserMuzzleArt returns a canvas (%s)' % art)

        # how much violet survives the clean? measured on the plate the engine will draw
        spill = pg.evaluate("""() => {
          const a = laserMuzzleArt(null); if(!a) return null;
          const x = a.getContext('2d'), d = x.getImageData(0,0,a.width,a.height).data;
          let tot=0, vio=0;
          for(let i=0;i<d.length;i+=4){ if(d[i+3]<8) continue; tot++;
            if(d[i]>d[i+1]+18 && d[i+2]>d[i+1]+28) vio++; }
          return {tot:tot, vio:vio}; }""")
        print('  spill after clean: %d violet of %d opaque' % (spill['vio'], spill['tot']))
        ok(spill['vio'] == 0, 'the chroma spill is converted to a black edge (0 violet px of %d)' % spill['tot'])
        ok(spill['tot'] > 3000, 'and the ART SURVIVED the clean - %d opaque px remain (plate is ~6,049)' % spill['tot'])

        fire_key = pg.evaluate("() => { const b=BOSSMODE.binds(); return (b&&b.fire&&b.fire[0])||'j'; }")
        pg.evaluate("() => { window.__step = %s; }" % sh.STEP)

        for arm in ('new', 'old'):
            if arm == 'old':
                pg.evaluate("() => { window.__realMuz = laserMuzzleArt; laserMuzzleArt = function(){ return null; }; }")
            for lv, inf, name in CASES:
                pg.evaluate("""([lv, inf]) => {
                  run.weapon=3; run.wlevels[3]=lv; run.wlevel=lv;
                  for(const b of pBullets) b.dead=true; pBullets.length=0;
                  run.infusion=null; if(inf){ for(let i=0;i<3;i++) infusionGrant(inf); }
                  player.x=worldWidth()*0.5; player.y=380; player.fireCd=0;
                }""", [lv, inf])
                pg.evaluate("([k]) => BOSSMODE.hold(k,true)", [fire_key])
                pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", 40)
                shots[(arm, name)] = grab(pg)
                pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [fire_key])
            if arm == 'old':
                pg.evaluate("() => { laserMuzzleArt = window.__realMuz; }")

        print('  errors:', len(errs))
        for e in errs[:4]: print('   !', e)
        ok(len(errs) == 0, 'no page or console errors (%d)' % len(errs))
        br.close()
    stop()

    # crop tight on the ship's nozzle: the muzzle is what changed, nothing else
    CW, CH = 300, 300
    W, H = shots[('new', CASES[0][2])].size
    cx, cy = W // 2, int(H * 0.78)
    cols, rows_n = len(CASES), 2
    sheet = Image.new('RGB', (cols * CW, rows_n * (CH + 22)), (10, 10, 14))
    d = ImageDraw.Draw(sheet)
    for r, arm in enumerate(('old', 'new')):
        for c, (lv, inf, name) in enumerate(CASES):
            im = shots[(arm, name)]
            box = (max(0, cx - CW // 2), max(0, cy - CH // 2), min(W, cx + CW // 2), min(H, cy + CH // 2))
            sheet.paste(im.crop(box).convert('RGB'), (c * CW, r * (CH + 22) + 22))
            d.text((c * CW + 6, r * (CH + 22) + 5),
                   ('OLD (two arcs)  ' if arm == 'old' else 'NEW (authored)  ') + name, fill=(235, 220, 150))
    p = os.path.join(OUT, '_muzzle_old_vs_new.png')
    sheet.save(p); print('  ->', p)
    json.dump({'cases': [c[2] for c in CASES]}, open(os.path.join(OUT, '_index.json'), 'w'), indent=2)
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
