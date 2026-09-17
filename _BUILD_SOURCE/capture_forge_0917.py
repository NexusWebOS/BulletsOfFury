#!/usr/bin/env python3
"""
capture_forge_0917.py - THE FORGE ON FILM: discover, clear the stage, combine, re-spec, load out,
and fly the forged gun into the next level.

Mike, 0917: "I wanted to see the in between stage screen of weapons being unlocked, weapons being
combined, etc. how this system and set works before your next level."

One continuous recording, every input a REAL KEY TAP through the game's bind table:

  stage 1  - two real infusion pickups are collected (INCENDIARY, VOLTAIC) - that is how an
             element is DISCOVERED for the Forge
  boss     - the Overlord-X dies, the death set-piece and flyover play
  debrief  - STAGE 1 COMPLETE, the real numbers
  THE FORGE- FIRE on the machine gun -> the element row -> FIRE on INCENDIARY:
               MACHINE GUN becomes INCENDIARY SLUGS, badge in the box
             -> the LASER + VOLTAIC = TESLA BEAM
             -> a third combine is REFUSED (two per stage)
             -> CHARGE re-specs the laser back
             -> DOWN swaps a loadout slot (eight unlocked, six may drop)
             -> START continues
  stage 2  - the machine gun is INCENDIARY SLUGS from the first frame: the badge in the EQUIPPED
             box, the name, and fire on every round - permanent, no pickup needed

⚠ THE TRIGGER IS HELD THROUGH THE REAL INPUT PATH (BOSSMODE.hold) - never player.fireCd=0, which
fires once per FRAME (10x, probe_firerate_0917.py).
⚠ ONLY THE REEL'S OWN PICKUPS MAY EXIST - the live stage's kills drop their own infusions (stage
1's bias is kinetic) and one walked into the last reel's captions.
"""
import os, sys, base64, subprocess, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, '_shots', 'forge_0917')
FPS = 15
SPF = 4

GRAB = ("() => {"
        " const g = document.querySelector('#screen-area canvas') || document.querySelector('canvas');"
        " if(!g) return null;"
        " const h = document.querySelector('#hud'), e = document.querySelector('#equipcv');"
        " const hv = h && h.offsetParent !== null && h.width > 0 && getComputedStyle(h).visibility !== 'hidden';"
        " const ev = e && e.offsetParent !== null && e.width > 0 && getComputedStyle(e).visibility !== 'hidden';"
        " if(!hv && !ev) return g.toDataURL('image/png');"
        " const hw = hv ? h.width : 0, hh = hv ? h.height : 0;"
        " const ew = ev ? e.width : 0, eh = ev ? e.height : 0;"
        " const rowH = Math.max(hh, eh), W = Math.max(hw + ew, g.width), H = rowH + g.height;"
        " let c = window.__shotc;"
        " if(!c){ c = window.__shotc = document.createElement('canvas'); }"
        " if(c.width !== W || c.height !== H){ c.width = W; c.height = H; }"
        " const x = c.getContext('2d');"
        " x.fillStyle = '#000'; x.fillRect(0, 0, W, H);"
        " if(hv) x.drawImage(h, 0, 0);"
        " if(ev) x.drawImage(e, hw, 0);"
        " x.drawImage(g, 0, rowH);"
        " return c.toDataURL('image/png'); }")

FLY = """(t) => {
  if(state !== 'play') return;
  player.dead = false; player.invuln = 0;
  const p = powerups.filter(q => !q.dead && q.kind === 'infuse')[0];
  if(p){ player.x += (p.x - player.x) * 0.22; player.y += (p.y + 26 - player.y) * 0.18; return; }
  const W = worldWidth();
  player.x = W*0.5 + Math.sin(t*0.7)*W*0.24;
  player.y = 396 + Math.sin(t*1.2)*22;
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
      e.hp = 22; e.maxhp = 22; e.score = 200; e.dropOk = false;
    }
  }
}"""

DROP = """([el]) => {
  const roll = infusionRoll; infusionRoll = function(){ return el; };
  window.__allowDrop = true;
  try{ dropPowerup(worldWidth()*0.5, 150, 'infuse'); }
  finally { infusionRoll = roll; window.__allowDrop = false; }
}"""

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
        pg.wait_for_function("() => typeof setState==='function' && typeof forgeStart==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("""() => {
          diffKey='hard'; DIFF=difficultyForRun(run.mode,'hard'); run.lives=9; run.mode='arcade';
          window.playerHit=function(){}; mapScroll=2100;
          /* eight weapons unlocked so the loadout has a choice to make; the unlock EQUIPS the chaingun,
             so the hand goes back on the machine gun (probe_forge_0917's lesson) */
          chaingunUnlock(); laserMistUnlock(); run.weapon=0; run.wlevel=1; run.wlevels[0]=2;
          const dp = dropPowerup;
          dropPowerup = function(){ if(!window.__allowDrop) return; return dp.apply(this, arguments); };
          XART.rdy('statpanel_full_0916'); XART.rdy('nwp_lfi_laser_start'); XART.rdy('chain_bolt_0');
          for(const e of Object.keys(INFUSIONS)) XART.rdy('inf_'+e);
        }""")
        for _ in range(8):
            pg.evaluate(sh.STEP, [8]); pg.wait_for_timeout(440)

        key = pg.evaluate("() => { const b=BOSSMODE.binds(); return (b&&b.fire&&b.fire[0])||'j'; }")
        pg.evaluate("() => { window.__step=%s; window.__fly=%s; window.__feed=%s; }" % (sh.STEP, FLY, FEED))
        t = [0.0]; n = [0]
        def frame():
            d = pg.evaluate(GRAB)
            if d:
                open(os.path.join(OUT, 'f%05d.png' % n[0]), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
                n[0] += 1
        def run_for(seconds, fire=True):
            for _ in range(int(seconds * FPS)):
                pg.evaluate("(t0) => { window.__feed(); for(let i=0;i<%d;i++){ window.__fly(t0+i/60); window.__step(1); } }" % SPF, t[0])
                frame(); t[0] += SPF / 60.0
        def tap(k, hold_frames=2, settle=0.5):
            pg.evaluate("([k]) => BOSSMODE.hold(k,true)", [k])
            pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", hold_frames)
            pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [k])
            run_for(settle, False)
        def cap(caption):
            st = pg.evaluate("() => ({s:state, inf:run.infusion?run.infusion.elem+' L'+(run.infusion.lv|0):'none', f:JSON.stringify(run.forge||{})})")
            print('  %5.1fs  %-62s [%s | %s | forge %s]' % (t[0], caption, st['s'], st['inf'], st['f']), flush=True)
            log.append({'t': round(t[0], 1), 'caption': caption, 'state': st['s'], 'infusion': st['inf'], 'forge': st['f']})
        def until(pred, cap_s):
            for _ in range(int(cap_s * FPS)):
                if pg.evaluate(pred): return True
                run_for(1.0 / FPS)
            return False

        # ---- stage 1: fight, discover two elements ---------------------------------------------
        pg.evaluate("([k]) => BOSSMODE.hold(k, true)", [key])
        cap('STAGE 1 - the machine gun, bare'); run_for(2.5)
        pg.evaluate(DROP, ['fire']);      cap('an INCENDIARY pickup - collected: DISCOVERED'); run_for(3.2)
        pg.evaluate(DROP, ['lightning']); cap('a VOLTAIC pickup - the second element');         run_for(3.2)
        # ---- the boss, the death, the debrief ---------------------------------------------------
        pg.evaluate("() => { enemies.length=0; run.infusion=null; if(typeof spawnBoss==='function') spawnBoss(curStage.boss); }")
        cap('the OVERLORD-X arrives'); run_for(6.5)
        pg.evaluate("() => { if(typeof boss!=='undefined'&&boss){ boss.hp=0; bossDie(); } }")
        cap('boss down - the death set-piece and the flyover');
        until("() => state==='stageclear'", 24)
        pg.evaluate("([k]) => BOSSMODE.hold(k, false)", [key])
        cap('STAGE 1 COMPLETE - the debrief'); run_for(5.5)
        # ⚠ TAP UNTIL THE STATE CHANGES, NEVER A BLIND SECOND PRESS. After 5.5s the debrief is
        # already fully revealed, so ONE press exits it and opens the Forge - and the first cut's
        # unconditional second press was then the Forge's own CONTINUE, which left it before a
        # single frame of it was filmed. The reel showed stage 2's launch where the Forge should
        # have been; forgeVisible() was true the whole time (measured at the debrief).
        for _ in range(8):
            tap('enter', 2, 0.6)
            if pg.evaluate("() => state==='forge'"): break
            run_for(1.6)
        # ---- THE FORGE --------------------------------------------------------------------------
        cap('THE FORGE - six loadout boxes, nine elements, two discovered'); run_for(3.2)
        tap('j', 2, 1.4);             cap('FIRE on the MACHINE GUN - pick an element')
        tap('j', 2, 1.6);             cap('INCENDIARY SLUGS - the machine gun is forged, level 1'); run_for(1.6)
        tap('d', 2, 0.5); tap('d', 2, 0.5); tap('d', 2, 0.8); cap('over to the LASER')
        tap('j', 2, 1.0); tap('d', 2, 1.0); cap('VOLTAIC for the laser')
        tap('j', 2, 1.6);             cap('TESLA BEAM - both combines spent'); run_for(1.4)
        tap('j', 2, 1.8);             cap('a THIRD combine - refused, two per stage')
        tap('h', 2, 1.8);             cap('CHARGE: re-spec the laser - it is a LASER again')
        tap('s', 2, 1.8);             cap('DOWN: swap this loadout slot - eight unlocked, six may drop')
        run_for(1.2)
        tap('enter', 2, 0.4);         cap('START: continue to stage 2')
        # ---- stage 2: the forged gun from the first frame ---------------------------------------
        until("() => state==='play' && (run.stage|0)===2", 40)
        pg.evaluate("() => { player.dead=false; enemies.length=0; }")
        pg.evaluate("([k]) => BOSSMODE.hold(k, true)", [key])
        cap('STAGE 2 - INCENDIARY SLUGS from the first shot, no pickup needed'); run_for(5.5)
        pg.evaluate("([k]) => BOSSMODE.hold(k, false)", [key])
        fin = pg.evaluate("() => ({w:run.weapon, nm:weaponDisplayName(run.weapon), inf:run.infusion?run.infusion.elem+':'+run.infusion.lv:null, pool:crateWeaponPool(), tagged:pBullets.filter(b=>b._inf==='fire').length})")
        print('  final:', json.dumps(fin), flush=True)
        print('  captured %d frames, %d errors' % (n[0], len(errs)), flush=True)
        for e in errs[:6]: print('   !', e[:200])
        pg.evaluate("() => { try{ localStorage.removeItem(CHAINGUN_UNLOCK_KEY); localStorage.removeItem(LASER_MIST_UNLOCK_KEY); }catch(_){} }")
        br.close()
    stop()
    json.dump(log, open(os.path.join(OUT, '_log.json'), 'w'), indent=2)
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    mp4 = os.path.join(OUT, 'BulletsOfFury_Forge_0917.mp4')
    subprocess.run([ff, '-y', '-framerate', str(FPS), '-i', os.path.join(OUT, 'f%05d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '27', '-preset', 'slow',
                    # ⚠ THE FRAMES CHANGE SIZE MID-REEL: PLAY composites the HUD row over the 960-wide
                    # field, the debrief and the Forge run in the cinematic viewport (a wider canvas, no
                    # HUD). A video stream needs ONE size, so every frame is fitted and letterboxed onto
                    # the same 1836x1152 stage; ffmpeg re-inits its filter graph at each size change.
                    '-vf', 'scale=1836:1152:force_original_aspect_ratio=decrease,pad=1836:1152:(ow-iw)/2:(oh-ih)/2:color=black',
                    '-movflags', '+faststart', mp4],
                   check=True, capture_output=True)
    print('mp4 -> %s (%.1f MB)' % (mp4, os.path.getsize(mp4) / 1e6))

if __name__ == '__main__':
    main()
