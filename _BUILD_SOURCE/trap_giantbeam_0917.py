#!/usr/bin/env python3
"""
trap_giantbeam_0917.py - WHAT IS DRAWING THE GREY BOX ON THE KINETIC GIANT BEAM?

Replacing the laser's procedural muzzle orb revealed a slate rectangle behind the beam on the
KINETIC giant beam only - previously hidden under the 153px disc the orb drew there. Four
hypotheses were plausible and all four were guesses, so this records what the frame actually
draws instead.

⚠ WRAP THE CONTEXT INSTANCE, NOT CanvasRenderingContext2D.prototype - ctx carries its own
drawImage and a prototype trap records ZERO on a draw that is provably running (0905h).
Every blit and every fillRect on the frame is logged with its destination rect and the live
composite mode, then filtered to the band around the ship.
"""
import os, sys, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

TRAP = """() => {
  const c = document.getElementById('screen'); const x = c.getContext('2d');
  window.__ops = [];
  const di = x.drawImage.bind(x), fr = x.fillRect.bind(x);
  x.drawImage = function(im){
    const a = Array.prototype.slice.call(arguments, 1);
    let d = null;
    if(a.length >= 8) d = {x:a[4], y:a[5], w:a[6], h:a[7]};
    else if(a.length >= 4) d = {x:a[0], y:a[1], w:a[2], h:a[3]};
    else if(a.length >= 2) d = {x:a[0], y:a[1], w:(im.naturalWidth||im.width||0), h:(im.naturalHeight||im.height||0)};
    if(window.__rec && d) window.__ops.push({op:'blit', d:d, gco:x.globalCompositeOperation,
      ga:+(x.globalAlpha||0).toFixed(2), sw:(im.naturalWidth||im.width||0), sh:(im.naturalHeight||im.height||0),
      tagged: im.__tag||null});
    return di.apply(null, arguments);
  };
  x.fillRect = function(rx, ry, rw, rh){
    if(window.__rec) window.__ops.push({op:'fillRect', d:{x:rx,y:ry,w:rw,h:rh},
      gco:x.globalCompositeOperation, ga:+(x.globalAlpha||0).toFixed(2), style:String(x.fillStyle)});
    return fr(rx, ry, rw, rh);
  };
}"""

def main():
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof laserMuzzleArt==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.playerHit=function(){}; enemies.length=0; mapScroll=2400; }")
        pg.evaluate("() => { XART.rdy('nwp_lfi_laser_start'); }")
        for _ in range(6):
            pg.evaluate(sh.STEP, [8]); pg.wait_for_timeout(420)
        pg.evaluate(TRAP)
        pg.evaluate("() => { window.__step = %s; }" % sh.STEP)
        key = pg.evaluate("() => { const b=BOSSMODE.binds(); return (b&&b.fire&&b.fire[0])||'j'; }")
        pg.evaluate("""([k]) => {
          run.weapon=3; run.wlevels[3]=3; run.wlevel=3;
          for(const b of pBullets) b.dead=true; pBullets.length=0;
          run.infusion=null; for(let i=0;i<3;i++) infusionGrant('kinetic');
          player.x=worldWidth()*0.5; player.y=380; player.fireCd=0;
          BOSSMODE.hold(k,true);
        }""", [key])
        pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", 40)
        info = pg.evaluate("""() => {
          const bm = pBullets.filter(b=>b.kind==='beam')[0] || null;
          return {beam: bm?{x:bm.x,y:bm.y,w:bm.w,h:bm.h,inf:bm._inf||null}:null,
                  camX:(typeof _camEff!=='undefined'?_camEff:camX), px:player.x, py:player.y};
        }""")
        print('  beam:', json.dumps(info))
        pg.evaluate("() => { window.__rec = true; window.__ops = []; }")
        pg.evaluate("() => window.__step(1)")
        pg.evaluate("() => { window.__rec = false; }")
        ops = pg.evaluate("() => window.__ops")
        print('  ops on one frame:', len(ops))

        # WORLD space, not canvas space. drawWorld runs under translate(-camX) and a scale, so the
        # destination args handed to drawImage are WORLD coordinates and the CTM converts them.
        # Converting them probe-side is this repo's oldest trap and it caught me here too: the
        # first cut filtered at (world-camX)*2 and found ZERO draws on a frame with 346 of them.
        sx = info['px']; sy = info['py']
        print('  ship at world (%.0f, %.0f)' % (sx, sy))
        near = []
        for o in ops:
            d = o['d']
            if not d or not d.get('w'):
                continue
            # anything drawn WIDER than 60 canvas px whose box contains the nozzle
            # the scanline pass is 480x1 black rects across the whole field, drawn LAST and in
            # bulk - it swamped the tail of the log and hid everything this trap is for
            if d['w'] >= 470 and d['h'] <= 2:
                continue
            if d['w'] >= 30 and d['x'] <= sx <= d['x'] + d['w'] and d['y'] - 40 <= sy <= d['y'] + d['h'] + 120:
                near.append(o)
        print('  --- wide draws covering the nozzle ---')
        for o in near[-24:]:
            d = o['d']
            print('   %-8s dst %7.1f,%7.1f %7.1fx%-7.1f  gco %-12s a%.2f  %s'
                  % (o['op'], d['x'], d['y'], d['w'], d['h'], o['gco'], o['ga'],
                     o.get('style') or ('src %dx%d' % (o.get('sw') or 0, o.get('sh') or 0))))
        print('  errors:', len(errs))
        for e in errs[:3]: print('   !', e)
        br.close()
    stop()

if __name__ == '__main__':
    main()
