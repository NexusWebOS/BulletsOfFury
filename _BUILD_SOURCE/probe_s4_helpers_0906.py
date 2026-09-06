#!/usr/bin/env python3
"""probe_s4_helpers_0906.py - do the Storm Sovereign's helpers spin, and do they stay put?

Mike, 0906, on the stage-4 boss: "chainguns on helpers need to rotate 360 degrees to appear
spinning, needs bigger bullets. helpers should not scroll with the screen, they remain where
they are."

Two claims, two different kinds of evidence:

  SPINNING  is a picture, so it takes a picture. Four frames at different points of the reel,
            contact-sheeted. A blit count would say "the barrel art was asked for" and CLAUDE.md
            already records three green key-counting probes on one invisible sprite.
  STAYING PUT is a number: move the CAMERA and see whether the helpers move with it. That is the
            whole of "scroll with the screen", and it cannot be judged from a screenshot at all.

⚠ THE CAMERA TEST MUST MOVE camX WITHOUT MOVING THE BOSS. Driving the player sideways moves both,
and a helper that tracked the boss would then look world-fixed. camX is set directly.
"""
import sys, os, io, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot as sh
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

WARM = """() => { const w=[]; for(let i=0;i<8;i++){w.push('s4w_helper_dual_'+i);w.push('s4w_final_chaingun_'+i);}
  w.push('s4w_boss_idle'); window.__w=w; for(const k of w){try{XART._touch(k);}catch(e){}} return w.length; }"""
READY = """() => { const ks=window.__w||[]; let n=0; for(const k of ks) if(XART.rdy(k)) n++; return ks.length?n/ks.length:1; }"""

SETUPBOSS = """() => {
  try{
    /* spawnBoss takes the KIND as an argument - calling it bare gives kind:undefined and builds
       the generic 160x120 hull with no _s4war rig, which reads as "the boss has no helpers". */
    spawnBoss(curStage.boss); if(!boss||!boss._s4war) return {ok:false,err:'no s4war rig, kind='+(boss&&boss.kind)};
    bossActive=true; boss.x=worldWidth()*0.5; boss.y=150; boss._drawY=150;
    stage4CoreTurretSpawnMissing(boss,0.99);
    const S=boss._s4war;
    for(const t of S.coreTurrets){ t.materialize=1; t.spawnT=1; t.state='fire'; t.stateT=0.5; t.reelSpeed=42; }
    return {ok:true, n:S.coreTurrets.length, W:worldWidth(), VW:VW};
  }catch(e){ return {ok:false, err:String(e)}; }
}"""
POS = """() => { const S=boss._s4war; return {camX:camX, t:S.coreTurrets.map(q=>({side:q.side,x:Math.round(q.x*10)/10})) }; }"""
SETCAM = """(v) => { camX=v; return camX; }"""
SPINSET = """(v) => { for(const t of boss._s4war.coreTurrets) t.spin=v; return v; }"""
CLEAR = """() => { const c=document.getElementById('screen'); c.getContext('2d').clearRect(0,0,c.width,c.height); }"""
DRAW = """() => { try{ drawWorld(1/60); return true; }catch(e){ return String(e); } }"""
GRAB = """() => document.getElementById('screen').toDataURL('image/png')"""


def main():
    port, stop = sh.serve(sh.GAME)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            pg = br.new_page(viewport={'width': 480, 'height': 512})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto('http://127.0.0.1:%d/index.html' % port)
            pg.wait_for_function('typeof ASSETS!=="undefined" && typeof loop==="function"', timeout=30000)
            pg.wait_for_timeout(2500)
            pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 4, 'pilot': 'cole', 'invuln': True})
            pg.evaluate(WARM)
            try:
                pg.wait_for_function('(' + READY + ')() >= 0.99', timeout=20000)
            except Exception:
                pass
            print('helper art ready: %.0f%%' % (pg.evaluate(READY) * 100))
            pg.evaluate(sh.TRAP_RAF)
            pg.evaluate(sh.STEP, 10)
            r = pg.evaluate(SETUPBOSS)
            if not r.get('ok'):
                raise SystemExit('boss setup failed: %s' % r)
            print('%d helpers, world %d, viewport %d' % (r['n'], r['W'], r['VW']))

            # --- claim 2: do they move with the camera? ---
            print('\n--- "helpers should not scroll with the screen" -----------------------------')
            rows = []
            for cam in (0, 100, 200):
                pg.evaluate(SETCAM, cam)
                pg.evaluate(sh.STEP, 6)
                rows.append(pg.evaluate(POS))
            for row in rows:
                print('  camX %-4s helpers at world x %s' % (row['camX'], [t['x'] for t in row['t']]))
            xs = [tuple(t['x'] for t in row['t']) for row in rows]
            fixed = len(set(xs)) == 1
            print('  -> %s' % ('WORLD-FIXED: identical at every camera position'
                               if fixed else '** THEY STILL SLIDE WITH THE CAMERA **'))
            onscreen = all(row['camX'] <= t['x'] <= row['camX'] + r['VW'] for row in rows for t in row['t'])
            print('  -> %s' % ('both stay inside the view at every camera position'
                               if onscreen else '** A HELPER GOES OFF SCREEN - it would be unkillable **'))

            # --- claim 1: do the barrels actually rotate? ---
            pg.evaluate(SETCAM, 100)
            shots = []
            for f in (0, 2, 4, 6):
                pg.evaluate(SPINSET, f)
                pg.evaluate(CLEAR)
                d = pg.evaluate(DRAW)
                if d is not True:
                    print('\n** draw threw: %s' % d); break
                im = Image.open(io.BytesIO(base64.b64decode(pg.evaluate(GRAB).split(',', 1)[1])))
                shots.append((f, im))
            br.close()
    finally:
        stop()

    if shots:
        H = shots[0][1].height
        cw = shots[0][1].width
        out = Image.new('RGBA', (cw * len(shots), H + 24), (10, 9, 16, 255))
        d = ImageDraw.Draw(out)
        for i, (f, im) in enumerate(shots):
            out.paste(im, (i * cw, 0))
            d.text((i * cw + 6, H + 5), 'spin frame %d' % f, fill=(235, 240, 250))
        out.save('docs/S4_HELPER_SPIN_0906.png')
        print('\nwrote docs/S4_HELPER_SPIN_0906.png')
    if errs:
        print('\n** %d page errors, first: %s' % (len(errs), errs[0][:200]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
