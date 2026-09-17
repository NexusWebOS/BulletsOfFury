#!/usr/bin/env python3
"""
probe_waterorb_0917.py - DOES THE WATER ORB ACTUALLY APPEAR?

The showcase reel's WATER ORB beat was ambiguous in its contact sheet and in a zoom of one frame:
orange pellets in flight and no visible orb. That is exactly the "occlusion is not a missing draw"
trap one step over - a crop taken at the wrong instant cannot tell "the orb is not there" from
"the orb is above the crop". So this asks the engine three separate questions and then takes a
picture of a frame in which an orb is provably alive:

  1. does slot 5 push kind:'orb' at all with the water element held?
  2. does the round wear the element (b._inf === 'water')?
  3. does a draw ask for orb ART on that frame - identified by the KEY, never by size?

⚠ XART.get RETURNS A FRESH CANVAS WITH NO .src, so a blit is identified by wrapping XART.get and
recording the key asked for (CLAUDE.md, three times over).
"""
import os, sys, base64, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, 'docs', 'proofs', 'infusion_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

TRAP = """() => {
  window.__orbKeys = {};
  const g = XART.get.bind(XART);
  XART.get = function(k){ if(/orb|fx0825|ice/i.test(String(k))) window.__orbKeys[k]=(window.__orbKeys[k]|0)+1; return g(k); };
}"""

PILOT = """(t) => {
  player.dead=false; player.invuln=0;
  const W = worldWidth();
  player.x = W*0.5 + Math.sin(t*0.8)*W*0.22; player.y = 390;
  player.fireCd = 0; pShoot();
}"""

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof infusionGrant==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.playerHit=function(){}; run.lives=9; }")
        # touch the orb art and WAIT - rdy() is false on its first call, and that call is the load
        pg.evaluate("() => { XART.rdy('fx0825_ice_orb'); XART.rdy('micon_iceorb_3'); }")
        for _ in range(6):
            pg.evaluate(sh.STEP, [8]); pg.wait_for_timeout(400)
        pg.evaluate(TRAP)
        # the showcase's own beat, verbatim
        pg.evaluate("""() => {
          run.weapon=5; run.wlevels[5]=Math.max(2, run.wlevels[5]||0); run.wlevel=run.wlevels[5];
          for(const b of pBullets) b.dead=true; pBullets.length=0;
          run.infusion=null; infusionGrant('water'); infusionGrant('water');
        }""")
        pg.evaluate("() => { window.__step=%s; window.__pilot=%s; window.__orbSeen=0; window.__orbInf=0; window.__shard=0; }" % (sh.STEP, PILOT))

        best = None
        t = 0.0
        for i in range(60):
            pg.evaluate("""(t0) => {
              for(let k=0;k<4;k++){ window.__pilot(t0+k/60); window.__step(1);
                for(const b of pBullets){ if(b.kind==='orb'){ window.__orbSeen++; if(b._inf==='water') window.__orbInf++; }
                                          if(b.kind==='shard') window.__shard++; } }
            }""", t)
            t += 4/60.0
            st = pg.evaluate("""() => { const o=pBullets.filter(b=>b.kind==='orb');
              return {n:o.length, x:o[0]?o[0].x:null, y:o[0]?o[0].y:null, inf:o[0]?(o[0]._inf||null):null,
                      wv:o[0]?(o[0]._wvar||null):null, camX:(typeof _camEff!=='undefined'?_camEff:camX)}; }""")
            if st['n'] > 0 and (best is None or st['y'] < best['y']):
                d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
                if d: best = dict(st); best['png'] = d
        res = pg.evaluate("() => ({orb:window.__orbSeen|0, inf:window.__orbInf|0, shard:window.__shard|0, keys:window.__orbKeys, elem:run.infusion?run.infusion.elem+':'+run.infusion.lv:null})")
        print(json.dumps({k: v for k, v in res.items() if k != 'keys'}))
        print('  orb art keys asked:', json.dumps(res['keys']))
        print('  errors:', len(errs))
        for e in errs[:4]: print('   !', e)

        ok(res['elem'] == 'water:2', 'the WATER infusion is held at level 2 (%s)' % res['elem'])
        ok(res['orb'] > 0, 'slot 5 with water held puts kind:orb in pBullets (%d orb-frames)' % res['orb'])
        ok(res['inf'] > 0 and res['inf'] == res['orb'], 'every live orb wears the element (_inf water on %d of %d)' % (res['inf'], res['orb']))
        ok(res['shard'] > 0, 'the orb sprays shards - the second carrier (%d shard-frames)' % res['shard'])
        ok(any('orb' in k for k in res['keys']), 'a draw asked for ORB ART by key: %s' % ','.join(list(res['keys'])[:4]))
        ok(best is not None, 'a frame was captured with an orb provably alive')
        ok(len(errs) == 0, 'no page or console errors (%d)' % len(errs))

        if best:
            p = os.path.join(OUT, '13_water_orb.png')
            open(p, 'wb').write(base64.b64decode(best['png'].split(',', 1)[1]))
            print('  orb at world (%.0f, %.0f), camX %.0f, variant %s -> %s'
                  % (best['x'], best['y'], best['camX'], best['wv'], p))
            # and a zoom on the orb itself, in SCREEN space (world - camX), the trap this repo has hit six times
            try:
                from PIL import Image
                im = Image.open(p).convert('RGBA')
                sx = (best['x'] - best['camX']) * (im.width / 480.0)
                sy = best['y'] * (im.height / 512.0)
                r = 120 * (im.width / 480.0)
                box = (max(0, int(sx-r)), max(0, int(sy-r)), min(im.width, int(sx+r)), min(im.height, int(sy+r)))
                bg = Image.new('RGBA', (box[2]-box[0], box[3]-box[1]), (0, 0, 0, 255))
                bg.paste(im.crop(box), (0, 0), im.crop(box))     # composite, never convert() (0906v)
                z = os.path.join(OUT, '13_water_orb_zoom.png')
                bg.resize((bg.width*2, bg.height*2), Image.NEAREST).save(z)
                print('  zoom ->', z)
            except Exception as ex:
                print('  (zoom skipped:', ex, ')')
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
