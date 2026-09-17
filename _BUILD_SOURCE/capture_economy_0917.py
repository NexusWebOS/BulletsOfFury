#!/usr/bin/env python3
"""
capture_economy_0917.py - THE CURRENCY ON FILM: a run ends, the score is banked, the Vault exchanges it,
the Armory sells a level, the Forge opens the weapon at that level, and the level-V gun flies.

Mike, 0917: "You use your high score points to purchase Furious Points ... All icons here should get
their level 1-5 upgrade generated variants, and upgraded projectiles."

Every input is a real key tap. One continuous recording, letterboxed onto one stage because the Forge
runs in the cinematic viewport and the menus at the play size.
"""
import os, sys, base64, subprocess, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, '_shots', 'economy_0917')
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
        " let c = window.__shotc; if(!c){ c = window.__shotc = document.createElement('canvas'); }"
        " if(c.width !== W || c.height !== H){ c.width = W; c.height = H; }"
        " const x = c.getContext('2d'); x.fillStyle = '#000'; x.fillRect(0, 0, W, H);"
        " if(hv) x.drawImage(h, 0, 0); if(ev) x.drawImage(e, hw, 0); x.drawImage(g, 0, rowH);"
        " return c.toDataURL('image/png'); }")
FLY = """(t) => { if(state !== 'play') return; player.dead = false; player.invuln = 0;
  const W = worldWidth(); player.x = W*0.5 + Math.sin(t*0.7)*W*0.24; player.y = 396 + Math.sin(t*1.2)*22; }"""
FEED = """() => { if(state !== 'play') return; if(typeof bossActive!=='undefined' && bossActive) return;
  const live = enemies.filter(e => !e.dead && e._dyingT == null).length;
  if(live < 5){ for(let i = live; i < 6; i++){ const e = spawnEnemy('drone', {x: 70 + (i*73) % 340, y: 80 + (i*41) % 140}); if(!e) break;
      e.x = 70 + (i*73) % 340; e.y = 80 + (i*41) % 140; e.shoots = false; e.vx = 0; e.vy = 0.3; e.hp = 22; e.maxhp = 22; e.score = 200; e.dropOk = false; } } }"""

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
        pg.wait_for_function("() => typeof setState==='function' && typeof drawArmory==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} achievementReload(); }")
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("""() => { diffKey='hard'; DIFF=difficultyForRun(run.mode,'hard'); run.lives=1; run.mode='arcade'; window.playerHit=function(){}; mapScroll=2100;
          run.weapon=0; run.wlevel=1; run.score=118400;
          XART.rdy('statpanel_full_0916'); for(const e of Object.keys(INFUSIONS)) for(const w of FORGE_WEAPONS) for(let l=1;l<=5;l++) XART.rdy('micon_forge_'+e+'_'+w+(l>1?'_'+l:''));
          for(const e of Object.keys(INFUSIONS)) XART.rdy('inf_'+e); }""")
        for _ in range(8): pg.evaluate(sh.STEP, [8]); pg.wait_for_timeout(440)
        key = pg.evaluate("() => (keybind.fire||['j'])[0]")
        pg.evaluate("() => { window.__step=%s; window.__fly=%s; window.__feed=%s; }" % (sh.STEP, FLY, FEED))
        t = [0.0]; n = [0]
        def frame():
            d = pg.evaluate(GRAB)
            if d: open(os.path.join(OUT, 'f%05d.png' % n[0]), 'wb').write(base64.b64decode(d.split(',', 1)[1])); n[0] += 1
        def run_for(seconds):
            for _ in range(int(seconds * FPS)):
                pg.evaluate("(t0) => { window.__feed(); for(let i=0;i<%d;i++){ window.__fly(t0+i/60); window.__step(1); } }" % SPF, t[0])
                frame(); t[0] += SPF / 60.0
        def tap(k, hold_frames=2, settle=0.5):
            pg.evaluate("([k]) => BOSSMODE.hold(k,true)", [k]); pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", hold_frames)
            pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [k]); run_for(settle)
        def cap(caption):
            st = pg.evaluate("() => ({s:state, bal:furiousBalance(), credit:scoreBankCredit(), msg:(typeof armory!=='undefined'&&armory&&state==='armory')?armory.msg:((typeof vault!=='undefined'&&vault&&state==='vault')?vault.msg:'')})")
            print('  %5.1fs  %-64s [%s | bal %d | credit %d | %r]' % (t[0], caption, st['s'], st['bal'], st['credit'], st['msg']), flush=True)
            log.append({'t': round(t[0], 1), 'caption': caption, 'state': st['s'], 'bal': st['bal'], 'credit': st['credit'], 'msg': st['msg']})

        # ---- the run's last seconds, then GAME OVER banks the score ----
        pg.evaluate("([k]) => BOSSMODE.hold(k, true)", [key])
        cap('a HARD run, 118,400 on the board'); run_for(3.0)
        pg.evaluate("([k]) => BOSSMODE.hold(k, false)", [key])
        pg.evaluate("() => { run.lives=0; triggerGameOver(); }")
        cap('GAME OVER - the score is BANKED: x1.5 HARD, x1.5 first run on this pilot'); run_for(4.5)
        # ---- THE VAULT: exchange ----
        pg.evaluate("() => { setState(GS.VAULT); vaultOpen(); }")
        cap('THE VAULT - EXCHANGE SCORE: the banked credit (the score kept ticking through the last seconds)'); run_for(2.4)
        tap(key, 2, 2.2);              cap('FIRE: +266 FURIOUS PTS')
        rows = pg.evaluate("() => vault.rows.length")
        for _ in range(rows - 1): tap('s', 2, 0.28)
        cap('DOWN to THE ARMORY'); run_for(0.8)
        tap(key, 2, 1.6);              cap('THE ARMORY - six weapon tabs, nine elements each, the badge at the level owned')
        tap('d', 2, 0.6); tap('d', 2, 0.6); tap('d', 2, 0.9); cap('RIGHT to the LASER')
        tap('s', 2, 0.5); tap('s', 2, 0.9);  cap('DOWN to TESLA BEAM - level I, level II costs 150')
        tap(key, 2, 2.0);              cap('FIRE: TESLA BEAM level II - the badge changes')
        tap(key, 2, 2.0);              cap('FIRE again: level III refused - the shortfall is named')
        tap('a', 2, 0.5); tap('a', 2, 0.5); tap('a', 2, 0.8); cap('LEFT back to the MACHINE GUN tab')
        pg.evaluate("() => { scoreBankDeposit(2400000,'furious','yuri'); scoreBankExchange(); }")
        cap('(a FURIOUS run on a second pilot banked and exchanged off camera: 2.4M x2 x1.5 = 7,200 points)'); run_for(1.0)
        for i in range(4): tap(key, 2, 1.1)
        cap('FIRE x4: INCENDIARY SLUGS II, III, IV, V - each level its own badge'); run_for(1.6)
        tap('k', 2, 1.2);              cap('BACK to the VAULT')
        # ---- THE FORGE opens the weapons at the owned levels ----
        pg.evaluate("() => { setState(GS.PLAY); run.forge={}; run.forgeElems={}; run.loadout=null; run.weapon=0; run.wlevel=1; run.lives=3; player.dead=false; forgeDiscover('lightning'); forgeDiscover('fire'); forgeStart(function(){ setState(GS.PLAY); }); }")
        run_for(2.4);                  cap('THE FORGE - two elements discovered in the field')
        pg.evaluate("() => { forge.sel=run.loadout.indexOf(0); }")
        tap(key, 2, 1.0); tap(key, 2, 1.0); cap('the machine gun: list, keep, element row')
        tap(key, 2, 1.8);              cap('FIRE on INCENDIARY: it opens at LEVEL V - the badge says so')
        pg.evaluate("() => { forge.sel=run.loadout.indexOf(3); }")
        tap(key, 2, 0.9); tap(key, 2, 0.9); tap('d', 2, 0.9); cap('the laser: VOLTAIC')
        tap(key, 2, 1.8);              cap('TESLA BEAM at LEVEL II')
        tap('c', 2, 1.8);              cap('RETINA: the Armory straight from the Forge')
        tap('k', 2, 1.4);              cap('BACK: the Forge is where you left it')
        tap('enter', 2, 0.4);          cap('CONTINUE')
        # ---- in play: the level-V gun ----
        pg.evaluate("() => { if(state!=='play'){ setState(GS.PLAY); } player.dead=false; enemies.length=0; forgeApply(); }")
        pg.evaluate("([k]) => BOSSMODE.hold(k, true)", [key])
        cap('INCENDIARY SLUGS V: bigger rounds, +2 damage each, on every shot'); run_for(5.0)
        pg.evaluate("([k]) => BOSSMODE.hold(k, false)", [key])
        fin = pg.evaluate("() => ({inf:run.infusion, icon:weaponIconKey(0,1), rounds:pBullets.filter(b=>b.kind==='mg').slice(0,2).map(b=>({w:b.w,dmg:b.dmg,inf:b._inf}))})")
        print('  final:', json.dumps(fin), flush=True)
        print('  captured %d frames, %d errors' % (n[0], len(errs)), flush=True)
        for e in errs[:6]: print('   !', e[:200])
        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} }")
        br.close()
    stop()
    json.dump(log, open(os.path.join(OUT, '_log.json'), 'w'), indent=2)
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    mp4 = os.path.join(OUT, 'BulletsOfFury_Economy_0917.mp4')
    subprocess.run([ff, '-y', '-framerate', str(FPS), '-i', os.path.join(OUT, 'f%05d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '28', '-preset', 'slow',
                    '-vf', 'scale=1224:768:force_original_aspect_ratio=decrease,pad=1224:768:(ow-iw)/2:(oh-ih)/2:color=black',
                    '-movflags', '+faststart', mp4], check=True, capture_output=True)
    print('mp4 -> %s (%.1f MB)' % (mp4, os.path.getsize(mp4) / 1e6))

if __name__ == '__main__':
    main()
