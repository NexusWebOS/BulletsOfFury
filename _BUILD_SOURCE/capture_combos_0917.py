#!/usr/bin/env python3
"""
capture_combos_0917.py - THE COMBINATION SYSTEM, INCLUDING THE MOMENT YOU FIND OUT WHAT YOU GOT.

Mike: "show me the weapon combination system in-action via video when you find out what you've
unlocked, and what you can combine and the lists and all."

So this reel opens on the part the previous one skipped: a REAL infusion pickup falling, being
collected, and the game telling you what it is - the hex badge on the ground, the arcade banner,
and the element badge appearing in the EQUIPPED box. Only then does it tour the combinations.

⚠ THE PICKUPS ARE REAL DROPS, not `infusionGrant` calls. `dropPowerup(x, y, 'infuse')` is the
forced kind killDrop uses, so what falls is the same object a kill would leave, and collecting it
runs the same `applyPowerup` path - banner, badge and all. Granting the element directly would
show the effect and skip the entire "find out what you've unlocked" half of the ask.

⚠ THE TRIGGER IS HELD THROUGH THE REAL INPUT PATH (`BOSSMODE.hold`) - never `player.fireCd = 0`,
which fires once per FRAME (10x measured, probe_firerate_0917.py).

⚠ SHOT OVER THE DESERT BAND (mapScroll 2100+): stage 1's ocean is 98% blue-dominant and the pale
elements - ice, kinetic, chrome, water - vanish into it.
"""
import os, sys, base64, subprocess, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, '_shots', 'combos_0917')
FPS = 15
SPF = 4
MAP_SCROLL0 = 2100

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

FLY = """(t) => {
  player.dead = false; player.invuln = 0;
  const W = worldWidth();
  player.x = W*0.5 + Math.sin(t*0.6)*W*0.20;
  player.y = 400 + Math.sin(t*1.1)*18;
}"""

# steer the ship ONTO a falling pickup so it is really collected
CHASE = """(t) => {
  player.dead = false; player.invuln = 0;
  const p = powerups.filter(q => !q.dead && q.kind === 'infuse')[0];
  if(p){ player.x += (p.x - player.x) * 0.20; player.y += (p.y + 26 - player.y) * 0.16; }
  else { const W = worldWidth(); player.x = W*0.5 + Math.sin(t*0.6)*W*0.20; player.y = 400; }
}"""

FEED = """() => {
  const live = enemies.filter(e => !e.dead && e._dyingT == null).length;
  if(live < 4){
    for(let i = live; i < 5; i++){
      const e = spawnEnemy('drone', {x: 80 + (i*77) % 320, y: 80 + (i*43) % 130});
      if(!e) break;
      e.x = 80 + (i*77) % 320; e.y = 80 + (i*43) % 130;
      e.shoots = false; e.vx = 0; e.vy = 0.3;
      e.hp = 24; e.maxhp = 24; e.score = 200; e.dropOk = false;
    }
  }
}"""

DROP = """([el]) => {
  /* the same object a kill leaves: dropPowerup's forced 'infuse' kind, with the element chosen
     so the reel can caption it.
     ⚠ AND run.infusion IS NOT CLEARED HERE. The first cut cleared it before every drop so the
     pickup would be a 'real grant' - which reset the level to 1 every time and silently deleted
     the two beats the reel exists for: a second pickup LEVELLING UP, and a different element at
     L3 FUSING. The log read 'fire L1' three drops running and looked fine. Let the pickup path
     do what it does in a real run. */
  const roll = infusionRoll;
  infusionRoll = function(){ return el; };
  window.__allowDrop = true;
  try{ dropPowerup(worldWidth()*0.5, 150, 'infuse'); }
  finally { infusionRoll = roll; window.__allowDrop = false; }
}"""

WEAPON = """([w, lv]) => {
  run.weapon = w; run.wlevels[w] = lv; run.wlevel = lv;
  run.missileLevel = (w === 2) ? lv : 0; run._chainRev = 0;
  for(const b of pBullets) b.dead = true; pBullets.length = 0;
}"""

# (seconds, kind, payload, caption)
BEATS = [
    (2.0, 'weapon', [0, 3],        'the machine gun, no element'),
    (3.2, 'drop',   ['fire'],      'A PICKUP FALLS - collect it and the game names it'),
    (2.4, 'hold',   None,          'INCENDIARY L1 - the badge is now in the EQUIPPED box'),
    (2.6, 'drop',   ['fire'],      'a second of the same element LEVELS IT UP'),
    (2.6, 'drop',   ['fire'],      'FIREBURST - level 3, the named combination'),
    (3.0, 'weapon', [1, 3],        'the SAME element on the SPREAD - it rides the carrier'),
    (3.0, 'weapon', [3, 3],        'and on the LASER'),
    (3.0, 'weapon', [2, 3],        'and on the MISSILES'),
    (3.2, 'drop',   ['lightning'], 'a DIFFERENT element at level 3 FUSES - THERMAL/VOLT names'),
    (3.0, 'weapon', [0, 3],        'VOLTAIC on the machine gun'),
    (2.8, 'drop',   ['lightning'], 'level 2'),
    (3.4, 'drop',   ['lightning'], 'GODS WRATH - the sky comes down on a kill'),
    (3.0, 'drop',   ['kinetic'],   'KINETIC - and on the laser it is the GIANT BEAM'),
    (3.0, 'weapon', [3, 3],        'SONIC WAVE / giant beam'),
    (3.2, 'drop',   ['chrome'],    'CHROMIUM - enemy fire mirrored back as your own'),
]

def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith('.png'): os.remove(os.path.join(OUT, f))
    port, stop = sh.serve(sh.GAME)
    log = []
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
        pg.evaluate("() => { diffKey='hard'; DIFF=difficultyForRun(run.mode,'hard'); run.lives=9;"
                    " window.playerHit=function(){}; mapScroll=%d; }" % MAP_SCROLL0)
        # ⚠ THE LIVE STAGE IS STILL RUNNING ITS WAVES, AND THOSE KILLS DROP THEIR OWN
        # INFUSIONS - stage 1's bias is KINETIC, so a kinetic badge walked into the middle of
        # the lightning beats and the reel captioned it wrong. Only the reel's own scripted
        # pickups are allowed to exist; everything else the game would drop is refused.
        pg.evaluate("""() => {
          const dp = dropPowerup;
          dropPowerup = function(){ if(!window.__allowDrop) return; return dp.apply(this, arguments); };
        }""")
        pg.evaluate("""() => {
          XART.rdy('nwp_lfi_laser_start'); XART.rdy('chain_bolt_0'); XART.rdy('fx0825_ice_orb');
          for(let f=0;f<6;f++) XART.rdy('nlz_3_b'+f);
          for(const e of ['fire','ice','lightning','kinetic','chrome','water','prism','toxic','dark']) XART.rdy('inf_'+e);
        }""")
        for _ in range(8):
            pg.evaluate(sh.STEP, [8]); pg.wait_for_timeout(440)

        key = pg.evaluate("() => { const b=BOSSMODE.binds(); return (b&&b.fire&&b.fire[0])||'j'; }")
        pg.evaluate("() => { window.__step=%s; window.__fly=%s; window.__chase=%s; window.__feed=%s; }"
                    % (sh.STEP, FLY, CHASE, FEED))
        pg.evaluate("([k]) => BOSSMODE.hold(k, true)", [key])
        print('  trigger held on %r (real input path)' % key, flush=True)

        t = [0.0]; n = [0]
        def run_for(seconds, chase):
            mover = 'window.__chase' if chase else 'window.__fly'
            for _ in range(int(seconds * FPS)):
                pg.evaluate("(t0) => { window.__feed(); for(let i=0;i<%d;i++){ %s(t0+i/60); window.__step(1); } }"
                            % (SPF, mover), t[0])
                d = pg.evaluate(GRAB)
                if d:
                    open(os.path.join(OUT, 'f%05d.png' % n[0]), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
                    n[0] += 1
                t[0] += SPF / 60.0

        for secs, kind, payload, caption in BEATS:
            chase = False
            if kind == 'weapon':
                pg.evaluate(WEAPON, payload)
            elif kind == 'drop':
                pg.evaluate(DROP, payload)
                chase = True                       # fly onto it so it is genuinely collected
            t0 = t[0]
            run_for(secs, chase)
            st = pg.evaluate("() => ({inf: run.infusion?run.infusion.elem+' L'+(run.infusion.lv|0):'none',"
                             " pk: powerups.filter(p=>!p.dead&&p.kind==='infuse').length})")
            print('  %5.1fs  %-58s  -> %s%s' % (t0, caption, st['inf'],
                  '   (UNCOLLECTED PICKUP STILL ON SCREEN)' if st['pk'] else ''), flush=True)
            log.append({'t': round(t0, 1), 'caption': caption, 'infusion_after': st['inf']})

        st = pg.evaluate("() => ({inf: run.infusion?run.infusion.elem+' L'+(run.infusion.lv|0):'none'})")
        print('  final infusion: %s' % st['inf'], flush=True)
        pg.evaluate("([k]) => BOSSMODE.hold(k, false)", [key])
        print('  captured %d frames, %d errors' % (n[0], len(errs)), flush=True)
        for e in errs[:6]: print('   !', e[:200])
        br.close()
    stop()

    json.dump(log, open(os.path.join(OUT, '_log.json'), 'w'), indent=2)
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    mp4 = os.path.join(OUT, 'BulletsOfFury_Combos_0917.mp4')
    subprocess.run([ff, '-y', '-framerate', str(FPS), '-i', os.path.join(OUT, 'f%05d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '26', '-preset', 'slow',
                    '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2', '-movflags', '+faststart', mp4],
                   check=True, capture_output=True)
    print('mp4 -> %s (%.1f MB)' % (mp4, os.path.getsize(mp4) / 1e6))

if __name__ == '__main__':
    main()
