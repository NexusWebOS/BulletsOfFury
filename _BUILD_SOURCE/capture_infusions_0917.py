#!/usr/bin/env python3
"""
capture_infusions_0917.py - THE WEAPON COMBINATION SYSTEM, ON FILM.

Mike: "show me this new weapon combination system in action."

One continuous stage-1 run, real waves, real enemies, the trigger held, captured as frames and
encoded to MP4. The infusions are GRANTED on a schedule rather than waited for - a 5% kill drop
would leave most of the reel showing nothing - but everything after the grant is the live game:
the banner, the palette on the rounds, the on-hit effect, the equipped-box badge, the named level-3.

⚠ STAGE 1, NOT 2: stage 2's hulls are FIRE-typed, so a fire infusion there is 50% ABSORBED (ENG-12)
and the reel demonstrates the absorb rule instead of the weapon.

⚠ AND IT IS SHOT OVER STAGE 1'S DESERT, NOT ITS OPENING WATER, FOR ONE MEASURED REASON. The
water orb and its shards are a pale ice-white, and stage 1's ocean measures 98% blue-dominant at
mean rgb 28/71/215 - the orb vanished into it. probe_waterorb_0917.py proved 239 orb-frames alive,
every one element-stamped, in a picture where the orb cannot be seen: state right, pixels
unreadable. That is 0905e's rule (an alert must contrast with the FIELD, not match the beam)
applied to a showcase. Scanned live (scan_stage1_bed_0917.py): mapScroll 2400-3200 is 0% blue at
mean rgb ~180/140/87, so the reel opens on sand and stays there.

⚠ EVERY FRAME IS A SEPARATE `evaluate`, WHICH IS ALSO WHAT LETS ART DECODE (0905). A synchronous
burst never yields, so a reel captured inside one evaluate would be a film of undecoded plates.
⚠ AND ALL THREE CANVASES ARE COMPOSITED (0809m) - #hud, #equipcv, #screen - or the reel loses the
EQUIPPED box, which is where the infusion badge and its level pips live.
"""
import os, sys, base64, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, '_shots', 'infusions_0917')
FPS = 15
MAP_SCROLL0 = 2100        # measured: stage 1 is orange desert from ~1200 to ~3300

GRAB = ("() => {"
        " const g = document.querySelector('#screen-area canvas') || document.querySelector('canvas');"
        " if(!g) return null;"
        " const h = document.querySelector('#hud'), e = document.querySelector('#equipcv');"
        " if(!h && !e) return g.toDataURL('image/png');"
        " const hw = h ? h.width : 0, hh = h ? h.height : 0;"
        " const ew = e ? e.width : 0, eh = e ? e.height : 0;"
        " const rowH = Math.max(hh, eh), W = Math.max(hw + ew, g.width), H = rowH + g.height;"
        " let c = window.__shotc;"
        " if(!c){ c = window.__shotc = document.createElement('canvas'); }"
        " if(c.width !== W || c.height !== H){ c.width = W; c.height = H; }"
        " const x = c.getContext('2d');"
        " x.fillStyle = '#000'; x.fillRect(0, 0, W, H);"
        " if(h) x.drawImage(h, 0, 0);"
        " if(e) x.drawImage(e, hw, 0);"
        " x.drawImage(g, 0, rowH);"
        " return c.toDataURL('image/png'); }")

# the pilot: weaving, trigger held, kept alive (this is a showcase, not a survival run)
PILOT = """(t) => {
  player.dead = false; player.invuln = 0;
  const W = worldWidth();
  player.x = W*0.5 + Math.sin(t*0.8)*W*0.30;
  player.y = 390 + Math.sin(t*1.5)*32;
  player.fireCd = 0; pShoot();
}"""

# enemies to shoot at, topped up so the reel is never an empty screen
# CHROMIUM mirrors ENEMY fire - with an empty sky it has nothing to turn around, so its beat
# seeds real enemy rounds above the pilot.
ENEMY_FIRE = """() => {
  for(let i = 0; i < 14; i++){
    eBullets.push({x: 60 + (i*31) % 360, y: 110 + (i*23) % 120, vx: 0, vy: 1.6,
                   kind: 'pellet', w: 8, h: 8, r: 4, dead: false, t: 0});
  }
}"""

FEED = """() => {
  const live = enemies.filter(e => !e.dead && e._dyingT == null).length;
  if(live < 5){
    for(let i = live; i < 6; i++){
      const e = spawnEnemy('drone', {x: 70 + (i*73) % 340, y: 90 + (i*37) % 130});
      if(!e) break;
      e.x = 70 + (i*73) % 340; e.y = 90 + (i*37) % 130;
      e.shoots = false; e.vx = 0; e.vy = 0.25; e.dropOk = false;
      e.hp = 26; e.maxhp = 26; e.score = 150;
    }
  }
}"""

# The element the beat is SUPPOSED to be showing, re-asserted every captured frame. Belt and
# braces beside e.dropOk=false: a showcase beat must show what its caption says. FUSION is
# deliberately unpinned - trading the element away IS that beat.
PIN = """([el, lv]) => {
  const cur = run.infusion ? run.infusion.elem : null;
  const clv = run.infusion ? (run.infusion.lv|0) : 0;
  if(cur !== el || clv < lv){ run.infusion = null; for(let i=0;i<lv;i++) infusionGrant(el); }
}"""

# beat: (seconds, what to do at the start of it, caption for the log)
BEATS = [
    (2.5, None,                                   'the machine gun, plain'),
    (3.5, ('grant', 'fire', 1),                   'INCENDIARY - the rounds turn and the target burns'),
    (3.5, ('grant', 'fire', 2),                   'FIREBURST - a hit detonates into its neighbours'),
    (3.5, ('grant', 'lightning', 3),              'VOLTAIC -> GODS WRATH - the sky comes down'),
    (3.5, ('weapon', 3, 'kinetic', 3),            'KINETIC on the laser - the giant beam'),
    (4.0, ('weapon', 0, 'chrome', 3),             'CHROMIUM - enemy fire turned back as your own'),
    (3.5, ('weapon', 5, 'water', 2),              'the WATER ORB'),
    (4.5, ('fuse', 'ice'),                        'FUSION - a level-3 element traded away detonates'),
]
ENEMY_FIRE_BEATS = {5}          # index of the CHROMIUM beat: keep real enemy rounds in the air

def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith('.png'): os.remove(os.path.join(OUT, f))
    port, stop = sh.serve(sh.GAME)
    n = 0
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof infusionGrant==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { diffKey='hard'; DIFF=difficultyForRun(run.mode,'hard'); run.lives=9; window.playerHit=function(){}; }")
        pg.evaluate("(v) => { mapScroll = v; }", MAP_SCROLL0)
        # let the stage art land, and warm what the showcase will ask for
        pg.evaluate("() => { XART.rdy('nchp_0'); XART.rdy('chain_bolt_0'); XART.rdy('fx0825_ice_orb'); for(let f=0;f<6;f++) XART.rdy('nlz_2_b'+f); for(const e of ['fire','ice','lightning','kinetic','chrome','water']) XART.rdy('inf_'+e); }")
        for _ in range(6):
            pg.evaluate(sh.STEP, [8]); pg.wait_for_timeout(450)
        pg.evaluate("() => { window.__step = %s; window.__pilot = %s; window.__feed = %s; }" % (sh.STEP, PILOT, FEED))

        t = 0.0
        for secs, act, caption in BEATS:
            if act:
                if act[0] == 'grant':
                    pg.evaluate("([el, times]) => { for(let i=0;i<times;i++) infusionGrant(el); }", [act[1], act[2]])
                elif act[0] == 'weapon':
                    pg.evaluate("([w, el, lv]) => { run.weapon=w; run.wlevels[w]=Math.max(2, run.wlevels[w]||0); run.wlevel=run.wlevels[w];"
                                " for(const b of pBullets) b.dead=true; pBullets.length=0;"
                                " run.infusion=null; for(let i=0;i<lv;i++) infusionGrant(el); }", [act[1], act[2], act[3]])
                elif act[0] == 'fuse':
                    pg.evaluate("(el) => { run.weapon=0; run.wlevels[0]=Math.max(2, run.wlevels[0]||0); run.wlevel=run.wlevels[0];"
                                " run.infusion=null; for(let i=0;i<3;i++) infusionGrant('fire'); infusionGrant(el); }", act[1])
            pin = None
            if act and act[0] == 'grant':    pin = [act[1], act[2]]
            elif act and act[0] == 'weapon': pin = [act[2], act[3]]
            bed = pg.evaluate("() => ({ms: Math.round(mapScroll)})")
            print('  %5.1fs  [map %5d]  %s' % (t, bed['ms'], caption), flush=True)
            bi = BEATS.index((secs, act, caption))
            for fi in range(int(secs * FPS)):
                if bi in ENEMY_FIRE_BEATS and fi % 6 == 0: pg.evaluate(ENEMY_FIRE)
                if pin: pg.evaluate(PIN, pin)
                # one evaluate per captured frame - the boundary that lets art decode
                pg.evaluate("(t0) => { window.__feed(); for(let i=0;i<4;i++){ window.__pilot(t0 + i/60); window.__step(1); } }", t)
                d = pg.evaluate(GRAB)
                if d:
                    open(os.path.join(OUT, 'f%04d.png' % n), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
                    n += 1
                t += 4 / 60.0
        print('captured %d frames, %d page errors' % (n, len(errs)), flush=True)
        for e in errs[:5]: print('   !', e)
        br.close()
    stop()

    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    mp4 = os.path.join(OUT, 'BulletsOfFury_Infusions_0917.mp4')
    subprocess.run([ff, '-y', '-framerate', str(FPS), '-i', os.path.join(OUT, 'f%04d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
                    '-crf', '18', mp4], check=True, capture_output=True)
    print('mp4 -> %s (%.1f MB)' % (mp4, os.path.getsize(mp4) / 1e6))

if __name__ == '__main__':
    main()
