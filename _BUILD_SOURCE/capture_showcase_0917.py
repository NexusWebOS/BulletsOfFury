#!/usr/bin/env python3
"""
capture_showcase_0917.py - ONE LIVE RUN: every projectile, the boss, the debrief, the stat screen.

Mike: "Please show me an end stat screen, LIVE RECORDED in-game of what we can do currently, the
projectiles you made, etc."

One continuous stage-1 run. Real waves, real kills, real score, and at the end the REAL stage
clear: the boss dies, the flyover plays, the debrief totals what actually happened in the run and
the NEW WEAPONS UNLOCKED page follows it.

⚠ THE TRIGGER IS HELD THROUGH THE REAL INPUT PATH (`BOSSMODE.hold`), NEVER `player.fireCd = 0`.
That is the whole of Mike's "the bullets are firing too fast" on the infusion reel: its autopilot
called the muzzle directly and zeroed the cooldown, firing once per FRAME. Measured in
probe_firerate_0917.py: 180 rounds/s forced against 18 through the trigger - 10x. Holding the key
means `_weaponCadence()` owns the gun exactly as it does for a player.

⚠ ALL THREE CANVASES ARE COMPOSITED (#hud, #equipcv, #screen) or the reel loses the score, the
lives and the EQUIPPED box - which is most of what a stat run is about.

⚠ ONE `evaluate` PER CAPTURED FRAME. A synchronous burst never yields and nothing decodes (0905);
that boundary is what lets the boss's art arrive mid-run.
"""
import os, sys, base64, subprocess, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, '_shots', 'showcase_0917')
FPS = 15
STEPS_PER_FRAME = 4                     # 4 game frames per captured frame -> 15fps of 60fps play
MAP_SCROLL0 = 2100                      # the desert band; see capture_infusions_0917.py

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

# framing only - the ship's POSITION is placed, its GUN is not touched
FLY = """(t) => {
  if(state !== 'play') return;
  player.dead = false; player.invuln = 0;
  const W = worldWidth();
  player.x = W*0.5 + Math.sin(t*0.7)*W*0.26;
  player.y = 392 + Math.sin(t*1.3)*26;
}"""

FEED = """() => {
  if(state !== 'play') return;
  if(typeof bossActive!=='undefined' && bossActive) return;
  const live = enemies.filter(e => !e.dead && e._dyingT == null).length;
  if(live < 5){
    for(let i = live; i < 6; i++){
      const e = spawnEnemy('drone', {x: 70 + (i*73) % 340, y: 80 + (i*41) % 140});
      if(!e) break;
      e.x = 70 + (i*73) % 340; e.y = 80 + (i*41) % 140;
      e.shoots = false; e.vx = 0; e.vy = 0.3;
      e.hp = 22; e.maxhp = 22; e.score = 200;
      e.dropOk = false;              /* a live pickup would swap the weapon mid-beat */
    }
  }
}"""

WEAPON = """([w, lv, el, elv]) => {
  run.weapon = w; run.wlevels[w] = lv; run.wlevel = lv;
  run.missileLevel = (w === 2) ? lv : 0;
  run._chainRev = 0;
  for(const b of pBullets) b.dead = true; pBullets.length = 0;
  run.infusion = null;
  if(el){ for(let i = 0; i < (elv||1); i++) infusionGrant(el); }
}"""

#  seconds, (weapon, level, element, element level), caption
BEATS = [
    (3.0, (0, 2, None, 0),        'MACHINE GUN - real cadence, 6 beats a second'),
    (3.0, (1, 3, None, 0),        'SPREAD FIRE'),
    (3.5, (2, 3, None, 0),        'HOMING MISSILES'),
    (3.5, (3, 3, None, 0),        'LASER - the new authored muzzle flare'),
    (3.0, (7, 3, None, 0),        'CHAINGUN - it spins up as you hold it'),
    (3.5, (5, 3, None, 0),        'ICE ORB and its shards'),
    (3.0, (8, 3, None, 0),        'LIGHTNING ORB'),
    (3.5, (0, 3, 'fire', 2),      'INFUSION: FIREBURST on the machine gun'),
    (3.5, (3, 3, 'kinetic', 3),   'INFUSION: KINETIC on the laser - the giant beam'),
    (3.5, (0, 3, 'chrome', 3),    'INFUSION: CHROMIUM - enemy fire mirrored back'),
]
BOSS_HOLD = 7.0          # let the Overlord-X entrance and gauge fill play
DEATH_HOLD = 11.0        # the boss death set-piece runs ~9.4s
CLEAR_HOLD = 9.0         # the debrief
UNLOCK_HOLD = 7.0        # and the NEW WEAPONS UNLOCKED page

def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith('.png'): os.remove(os.path.join(OUT, f))
    port, stop = sh.serve(sh.GAME)
    n = 0
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
        # warm what the run will ask for, then let it decode in REAL time
        pg.evaluate("""() => {
          XART.rdy('nwp_lfi_laser_start'); XART.rdy('fx0825_ice_orb'); XART.rdy('chain_bolt_0');
          for(let f=0;f<6;f++) XART.rdy('nlz_3_b'+f);
          for(const e of ['fire','ice','lightning','kinetic','chrome','water']) XART.rdy('inf_'+e);
          if(typeof warmStage==='function') try{ warmStage(1); }catch(_){}
        }""")
        for _ in range(8):
            pg.evaluate(sh.STEP, [8]); pg.wait_for_timeout(450)

        key = pg.evaluate("() => { const b=BOSSMODE.binds(); return (b&&b.fire&&b.fire[0])||'j'; }")
        pg.evaluate("() => { window.__step=%s; window.__fly=%s; window.__feed=%s; }" % (sh.STEP, FLY, FEED))
        pg.evaluate("([k]) => BOSSMODE.hold(k, true)", [key])     # trigger DOWN for the whole run
        print('  trigger held on bind %r - the real input path' % key, flush=True)

        t = [0.0]
        def run_for(seconds, label):
            frames = int(seconds * FPS)
            for _ in range(frames):
                pg.evaluate("(t0) => { window.__feed(); for(let i=0;i<%d;i++){ window.__fly(t0+i/60); window.__step(1); } }"
                            % STEPS_PER_FRAME, t[0])
                d = pg.evaluate(GRAB)
                if d:
                    open(os.path.join(OUT, 'f%05d.png' % run_for.n[0]), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
                    run_for.n[0] += 1
                t[0] += STEPS_PER_FRAME / 60.0
        run_for.n = [0]

        for secs, wep, caption in BEATS:
            pg.evaluate(WEAPON, list(wep))
            st = pg.evaluate("() => ({s:state, k:(stageStats&&stageStats.kills)|0, sc:run.score|0})")
            print('  %5.1fs  %-52s  [%s kills %d score %d]' % (t[0], caption, st['s'], st['k'], st['sc']), flush=True)
            log.append({'t': round(t[0], 1), 'caption': caption, 'kills': st['k'], 'score': st['sc']})
            run_for(secs, caption)

        # ---- the real boss, the real death, the real debrief -------------------------
        pg.evaluate(WEAPON, [0, 5, None, 0])
        pg.evaluate("() => { enemies.length=0; if(typeof spawnBoss==='function') spawnBoss(curStage.boss); }")
        print('  %5.1fs  BOSS: %s' % (t[0], pg.evaluate("() => (typeof boss!=='undefined'&&boss)?(boss.kind||'?'):'none'")), flush=True)
        run_for(BOSS_HOLD, 'boss arrival')

        # force-kill is the DEATH BRANCH, not hp=1 + a hit: a barrier absorbs that (0910a)
        pg.evaluate("() => { if(typeof boss!=='undefined' && boss){ boss.hp=0; if(typeof bossDie==='function') bossDie(); } }")
        print('  %5.1fs  boss killed - death set-piece, flyover, debrief' % t[0], flush=True)
        run_for(DEATH_HOLD, 'boss death')

        st = pg.evaluate("() => ({s:state})")
        print('  %5.1fs  state after the death: %s' % (t[0], st['s']), flush=True)
        run_for(CLEAR_HOLD, 'stage clear')

        st = pg.evaluate("() => ({s:state})")
        print('  %5.1fs  state on the debrief: %s' % (t[0], st['s']), flush=True)
        # CONTINUE off the debrief -> the NEW WEAPONS UNLOCKED page
        pg.evaluate("([k]) => { Input.injectTap(k); }", [key])
        run_for(UNLOCK_HOLD, 'unlocks')
        st = pg.evaluate("() => ({s:state, k:(stageStats&&stageStats.kills)|0, sc:run.score|0})")
        print('  %5.1fs  final state %s, %d kills, score %d' % (t[0], st['s'], st['k'], st['sc']), flush=True)
        log.append({'t': round(t[0], 1), 'caption': 'FINAL', 'state': st['s'], 'kills': st['k'], 'score': st['sc']})

        pg.evaluate("([k]) => BOSSMODE.hold(k, false)", [key])
        n = run_for.n[0]
        print('  captured %d frames, %d errors' % (n, len(errs)), flush=True)
        for e in errs[:6]: print('   !', e[:200])
        br.close()
    stop()

    json.dump(log, open(os.path.join(OUT, '_log.json'), 'w'), indent=2)
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    mp4 = os.path.join(OUT, 'BulletsOfFury_Showcase_0917.mp4')
    subprocess.run([ff, '-y', '-framerate', str(FPS), '-i', os.path.join(OUT, 'f%05d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', '-preset', 'slow',
                    '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2', '-movflags', '+faststart', mp4],
                   check=True, capture_output=True)
    print('mp4 -> %s (%.1f MB)' % (mp4, os.path.getsize(mp4) / 1e6))

if __name__ == '__main__':
    main()
