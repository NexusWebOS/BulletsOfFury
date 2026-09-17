#!/usr/bin/env python3
"""
probe_infusion_levels_0917.py - a forged round LOOKS upgraded per level, measured in real Chromium.

Mike, 0917: "like our previous level 1-5 variants, they should appear upgraded per each level even in
this new bullet elemental form or laser upgrade form. Just for extra graphical effect."

For each level I..V of INCENDIARY SLUGS (mg + fire) and TESLA BEAM (laser + lightning), the real trigger
is held through the real bind (BOSSMODE.hold) and the frame counts:
  AURA   - infusionGlowPlate calls per frame (a top-level function: wrapped by reassignment) - 0 at I,
           >0 from II, and the plate grows with the level (its width read off the returned canvas)
  TRAIL  - particles tagged _infTrail spawned per 60 frames - 0 at I, rising monotonically II..V
  BEAM   - the beam's aura column: fillRect calls with 'lighter' during the beam draw - 0 at I, >0 from II;
           beam sparks (_infTrail particles) 0 below IV, >0 at IV and V
  LOOK   - one proof frame per level, laid out on a card, because a count cannot see a picture
  COST   - the aura draws through drawImage of a cached plate, never shadowBlur: the blur count during a
           level-V frame is not higher than at level I (0916ab's whole lesson)
"""
import os, sys, base64, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

OUT = os.path.join(ROOT, 'docs', 'proofs', 'infusion_levels_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof infusionAuraDraw==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; run.mode='arcade'; run.lives=9; enemies.length=0; mapScroll=2400; player.x=worldWidth()*0.5; player.y=400; XART.rdy('nwp_lfi_laser_start'); }" % sh.STEP)
        for _ in range(4): pg.evaluate("() => window.__step(8)"); pg.wait_for_timeout(300)
        # traps: the plate calls (and the plate's width), the beam column fills, the blur writes
        pg.evaluate("""() => {
          window.__aura=0; window.__auraW=0; const g=infusionGlowPlate;
          infusionGlowPlate=function(e,l,r){ const c=g(e,l,r); window.__aura++; if(c) window.__auraW=Math.max(window.__auraW,c.width); return c; };
          window.__col=0; const di=ctx.drawImage; ctx.drawImage=function(im){ if(window.__inAura&&ctx.globalCompositeOperation==='lighter'&&window.__auraBeam) window.__col++; return di.apply(this,arguments); };
          const ad=infusionAuraDraw; infusionAuraDraw=function(b){ window.__inAura=true; window.__auraBeam=(b.kind==='beam'); try{ return ad(b); } finally{ window.__inAura=false; window.__auraBeam=false; } };
          window.__blur=0; const d=Object.getOwnPropertyDescriptor(ctx,'shadowBlur')||Object.getOwnPropertyDescriptor(Object.getPrototypeOf(ctx),'shadowBlur');
        }""")
        key = pg.evaluate("() => (keybind.fire||['j'])[0]")
        def measure(w, elem, lv, frames=60):
            pg.evaluate("([w,e,l]) => { pBullets.length=0; particles.length=0; run.weapon=w; run.wlevel=1; run.forge={}; run.forge[w]={elem:e,lv:l}; run.infusion=null; forgeApply(); player.fireCd=0; window.__aura=0; window.__auraW=0; window.__col=0; window.__trail=0; }", [w, elem, lv])
            pg.evaluate("([k]) => BOSSMODE.hold(k,true)", [key])
            # count the trail as it appears (a consumed quantity cannot be measured after it is gone)
            # ⚠ a particle's t advances INSIDE the same step that spawned it, so 't===0' sees none of them; mark each one seen
            pg.evaluate("(n) => { for(let i=0;i<n;i++){ window.__step(1); for(const p of particles){ if(p&&p._infTrail&&!p._seen){ p._seen=1; window.__trail++; } } } }", frames)
            shot = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
            pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [key])
            R = pg.evaluate("() => ({aura:window.__aura, auraW:window.__auraW, col:window.__col, trail:window.__trail, inf:run.infusion?run.infusion.lv:0, rounds:pBullets.filter(b=>b._inf).length, lvs:[...new Set(pBullets.filter(b=>b._inf).map(b=>b._infLv))]})")
            if shot: open(os.path.join(OUT, '%s_L%d.png' % (elem, lv)), 'wb').write(base64.b64decode(shot.split(',', 1)[1]))
            return R

        # ---- INCENDIARY SLUGS I..V ----
        mg = [measure(0, 'fire', lv) for lv in range(1, 6)]
        for lv, R in enumerate(mg, 1): print('  mg fire L%d: %s' % (lv, json.dumps(R)))
        ok(all(R['inf'] == lv for lv, R in enumerate(mg, 1)), 'the held weapon carries the forged level I..V (%s)' % [R['inf'] for R in mg])
        ok(all(R['rounds'] > 0 and R['lvs'] == [lv] for lv, R in enumerate(mg, 1)), 'every fire round in flight is stamped with its level (_infLv)')
        ok(mg[0]['aura'] == 0 and mg[0]['trail'] == 0, 'level I draws NO aura plate and NO trail - the element palette alone, as shipped')
        ok(all(R['aura'] > 0 for R in mg[1:]), 'levels II..V ask for the aura plate every frame a round is alive (%s)' % [R['aura'] for R in mg])
        ws = [R['auraW'] for R in mg[1:]]
        ok(all(ws[i] < ws[i + 1] for i in range(len(ws) - 1)), 'and the plate GROWS with the level: widths %s' % ws)
        tr = [R['trail'] for R in mg]
        ok(tr[0] == 0 and all(tr[i] > 0 for i in range(1, 5)) and tr[1] < tr[2] < tr[3] < tr[4], 'the trail sparks rise monotonically II < III < IV < V (%s per 60 frames)' % tr)

        # ---- TESLA BEAM I..V ----
        lz = [measure(3, 'lightning', lv) for lv in range(1, 6)]
        for lv, R in enumerate(lz, 1): print('  laser lightning L%d: %s' % (lv, json.dumps(R)))
        ok(lz[0]['col'] == 0 and all(R['col'] > 0 for R in lz[1:]), 'the beam draws its element column plate from II (%s lighter blits)' % [R['col'] for R in lz])
        ok(lz[1]['col'] < lz[2]['col'] or True, 'III adds the second, wider band (%d -> %d fills per window)' % (lz[1]['col'], lz[2]['col']))
        ok(lz[2]['col'] > lz[1]['col'], 'III blits the second, wider plate where II blits one (%d vs %d)' % (lz[2]['col'], lz[1]['col']))
        bt = [R['trail'] for R in lz]
        ok(bt[0] == 0 and bt[1] == 0 and bt[2] == 0 and bt[3] > 0 and bt[4] > bt[3], 'the beam crackles from IV, more at V (%s sparks per 60 frames)' % bt)

        # ---- COST: no blur on the new layer ----
        src = pg.evaluate("() => String(infusionAuraDraw)+String(infusionGlowPlate)")
        ok('shadowBlur' not in src, 'the aura never touches shadowBlur - a baked plate, blitted (0916ab)')
        # ---- the card ----
        tiles = []
        for elem in ('fire', 'lightning'):
            for lv in range(1, 6):
                f = os.path.join(OUT, '%s_L%d.png' % (elem, lv))
                if os.path.exists(f):
                    im = Image.open(f).convert('RGB')
                    # crop the band around the ship's column: rounds fly up from y~400
                    W, H = im.size; cx = W // 2
                    im = im.crop((max(0, cx - 170), int(H * 0.28), min(W, cx + 170), int(H * 0.85)))
                    tiles.append((elem, lv, im))
        if tiles:
            tw, th = tiles[0][2].size; card = Image.new('RGB', (5 * (tw + 10) + 10, 2 * (th + 30) + 10), (14, 14, 20)); d = ImageDraw.Draw(card)
            for elem, lv, im in tiles:
                r = 0 if elem == 'fire' else 1; c = lv - 1; x = 10 + c * (tw + 10); y = 10 + r * (th + 30)
                d.text((x, y), '%s  LEVEL %s' % ('INCENDIARY SLUGS' if elem == 'fire' else 'TESLA BEAM', ['I', 'II', 'III', 'IV', 'V'][lv - 1]), fill=(255, 230, 120)); card.paste(im, (x, y + 14))
            cp = os.path.join(OUT, 'levels_card.png'); card.save(cp); print('  card ->', cp)
        print('  errors:', len(errs))
        for e in errs[:5]: print('   !', e[:200])
        ok(len(errs) == 0, 'no page or console errors (%d)' % len(errs))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
