#!/usr/bin/env python3
"""
probe_debugmode.py - DRIVE THE DEBUG MODE THE WAY MIKE WILL (drop 0910a).

    python3 _BUILD_SOURCE/probe_debugmode.py --out /tmp/dbg

Real Chromium, real index.html, real keyboard events. Proves, with pixels and page state:

  1. the title has NO debug button until UP UP DOWN DOWN A B C is typed on the keyboard
  2. after the code: the button is there, F2 / clicking it opens the debug menu
  3. picking a fight from the MENU (arrow + enter, not the API) lands in that fight with the
     right boss spawned after the game's own warning
  4. R starts the recorder and R stops it; a webm blob comes back
  5. killing the boss runs the cook-off, the fly-off, and fades back to the DEBUG menu
  6. a MINIBOSS fight does the same through its own death reel
  7. index.html?bossmode=1 boots itself into GS.BMHOST with no keypress, and window.BOSSMODE
     can start / snapshot / stop a fight from outside

Written against shoot.py's server / rAF trap / stepper so it measures the same renderer.
"""
import os, sys, time, argparse, base64, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/dbg'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME)
    errs=[]; fails=[]; n_ok=[0]
    def ok(cond, msg):
        if cond: n_ok[0]+=1; print('  ok  ', msg)
        else: fails.append(msg); print('  FAIL', msg)
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
        pg=b.new_page(viewport={'width':1100,'height':1200}, device_scale_factor=1, accept_downloads=True)
        pg.on('pageerror', lambda e: errs.append('pageerror: '+str(e)[:200]))
        pg.on('console', lambda m: errs.append('console.error: '+m.text[:200]) if m.type=='error' else None)
        pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(shoot.TRAP_RAF); pg.wait_for_timeout(50)
        pg.evaluate(shoot.SETUP, {'state':'TITLE','pilot':'cole','stage':1,'invuln':False})
        def step(n):
            while n>0:
                k=min(60,n); e=pg.evaluate(shoot.STEP,k)
                if e: print('  step threw:', e); fails.append('step threw '+e); return
                pg.wait_for_timeout(15); n-=k
        def grab(name):
            d=pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
            with open(os.path.join(a.out,name),'wb') as f: f.write(base64.b64decode(d.split(',',1)[1]))
        def J(expr): return pg.evaluate('() => ('+expr+')')
        def press(key, frames=4):
            pg.keyboard.down(key); step(frames); pg.keyboard.up(key); step(frames)

        # 1. no button before the code
        step(30); grab('01_title_locked.png')
        ok(J("typeof debugUnlocked!=='undefined' && debugUnlocked===false"), 'debugUnlocked starts false')
        # a wrong sequence must not unlock
        for k in ['ArrowUp','ArrowUp','ArrowDown','KeyA','KeyB','KeyC']: press(k)
        ok(J("debugUnlocked===false"), 'a wrong sequence (U U D A B C) does not unlock')
        # 2. the code
        for k in ['ArrowUp','ArrowUp','ArrowDown','ArrowDown','KeyA','KeyB','KeyC']: press(k)
        step(20); grab('02_title_unlocked.png')
        ok(J("debugUnlocked===true"), 'UP UP DOWN DOWN A B C unlocks')
        ok(J("state==='title'"), 'still on the title after the code (state=%s)' % J('state'))
        # F2 opens the menu
        press('F2'); step(10); grab('03_debug_menu.png')
        ok(J("state==='debugmenu'"), 'F2 opens the debug menu (state=%s)' % J('state'))
        nf=J('debugFightList().length'); ok(nf>=16, 'fight list has %d entries' % nf)
        # 3. pick STAGE 1 BOSS by keyboard: row 0 col 1 is the default; Enter
        press('Enter'); step(5)
        ok(J("state==='play' && debugFight && debugFight.stage===1 && debugFight.role==='boss'"), 'Enter launches the stage-1 boss fight (state=%s)' % J('state'))
        ok(J("warnT>0 && warnKind==='boss'"), 'the game\'s own boss warning is raised (warnT=%.2f)' % J('warnT'))
        step(200); grab('04_s1_boss.png')
        ok(J("bossActive && boss && boss.kind==='damkeeper'"), 'the stage-1 boss is up: %s' % J("boss?boss.kind+'/'+boss.name:null"))
        ok(J("enemies.length<=2"), 'no wave enemies poured in (enemies=%d)' % J('enemies.length'))
        # 4. R records
        press('KeyR'); step(2)
        ok(J("debugRecActive()"), 'R starts the recorder')
        for i in range(6): step(30); pg.wait_for_timeout(120)
        grab('05_s1_boss_recording.png')
        press('KeyR')
        pg.wait_for_function("() => !debugRecActive()", timeout=5000)
        pg.wait_for_function("() => debugRec.last!=null", timeout=8000)
        last=J("({name:debugRec.last.name,size:debugRec.last.size,dur:debugRec.last.dur})")
        ok(last['size']>1000, 'R stops it and a webm comes back: %s %d bytes %.1fs' % (last['name'], last['size'], last['dur']))
        # the clip is the whole cabinet: hud strip + equip box + play canvas, laid out like shoot.py's capture
        geom=J("({W:debugRec.cv.width, H:debugRec.cv.height, screenW:cv.width, screenH:cv.height, hudH:(document.getElementById('hud')||{}).height})")
        ok(geom['H']>geom['screenH'] and geom['W']>=geom['screenW'], 'and it captured the COMPOSITE, not the play canvas alone: %dx%d against a %dx%d screen' % (geom['W'],geom['H'],geom['screenW'],geom['screenH']))
        lit=J("(function(){ const x=debugRec.cv.getContext('2d'); const d=x.getImageData(0,0,debugRec.cv.width,Math.max(1,debugRec.cv.height-cv.height)).data; let n=0; for(let i=0;i<d.length;i+=4) if(d[i]+d[i+1]+d[i+2]>60) n++; return n; })()")
        ok(lit>2000, 'the HUD row of the recorded frame carries real pixels, not black (%d lit)' % lit)
        # 5. kill -> cook-off -> fly-off -> fade -> menu
        J('BOSSMODE.kill()'); step(3)
        ok(J("boss && boss.dead && bossDefeated"), 'boss dead, stage ending')
        step(150); grab('06_s1_cookoff.png')
        seen=set()
        for i in range(30):
            step(30); seen.add(J('state'))
            if J("state==='debugmenu'"): break
        grab('07_back_to_menu.png')
        ok('flyover' in seen, 'the fly-off ran (states seen: %s)' % ','.join(sorted(seen)))
        ok('debugfade' in seen, 'then the fade')
        ok(J("state==='debugmenu' && debugFight===null"), 'and it ends on the debug menu (state=%s)' % J('state'))
        ok(J("boss===null && enemies.length===0"), 'the fight was cleaned up behind it')
        # 6. a miniboss, via the menu: down to stage 2, left to MINI, enter
        press('ArrowDown'); press('ArrowLeft'); press('Enter'); step(5)
        ok(J("state==='play' && debugFight && debugFight.stage===2 && debugFight.role==='mini'"), 'stage-2 MINI launched from the menu')
        step(220); grab('08_s2_mini.png')
        ok(J("subBossActive && subBoss && subBoss.kind==='magmaward'"), 'the stage-2 mini is up: %s' % J("subBoss?subBoss.kind+'/'+subBoss.name:null"))
        J('BOSSMODE.kill()'); step(3)
        ok(J("subBoss && subBoss.dead"), 'mini dead')
        seen=set()
        for i in range(40):
            step(30); seen.add(J('state'))
            if J("state==='debugmenu'"): break
        grab('09_mini_back.png')
        ok('flyover' in seen and J("state==='debugmenu'"), 'mini death -> fly-off -> menu (states: %s)' % ','.join(sorted(seen)))
        # a death: the continue screen must not strand us
        press('ArrowDown'); press('ArrowRight'); press('Enter'); step(200)
        ok(J("bossActive"), 'stage-3 boss up for the death test')
        pg.evaluate("() => { run.lives=0; run.shield=0; player.invuln=0; if(typeof special!=='undefined') special=null; playerHit(); }")
        seen=set()
        for i in range(40):
            step(30); seen.add(J('state'))
            if J("state==='debugmenu'"): break
        ok(J("state==='debugmenu'"), 'dying in a debug fight returns to the menu too (states: %s)' % ','.join(sorted(seen)))
        # back out
        press('Backspace'); step(5)
        ok(J("state==='title'"), 'BACKSPACE leaves the menu for the title')
        # 7. the host
        pg2=b.new_page(viewport={'width':700,'height':800})
        pg2.on('pageerror', lambda e: errs.append('host pageerror: '+str(e)[:200]))
        pg2.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1', wait_until='load', timeout=60000)
        try:
            pg2.wait_for_function("() => window.BOSSMODE && BOSSMODE.state==='bmhost'", timeout=60000)
            ok(True, 'the host boots itself into bmhost with no keypress')
        except Exception as e:
            ok(False, 'host never reached bmhost: state=%s' % pg2.evaluate("() => window.BOSSMODE?BOSSMODE.state:'no api'"))
        pg2.wait_for_timeout(300)
        r=pg2.evaluate("() => BOSSMODE.start(4,'boss','yuri')")
        ok(r is True, 'BOSSMODE.start(4, boss, yuri) accepted')
        pg2.wait_for_function("() => BOSSMODE.snapshot().bossActive", timeout=15000)
        s=pg2.evaluate("() => BOSSMODE.snapshot()")
        ok(s['boss'] and s['boss']['ship']=='stormsovereign' and s['fight']['stage']==4, 'host snapshot: %s hp %s/%s pilot %s' % (s['boss']['name'], s['boss']['hp'], s['boss']['maxhp'], pg2.evaluate("() => run.pilot")))
        d=pg2.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
        open(os.path.join(a.out,'10_host_fight.png'),'wb').write(base64.b64decode(d.split(',',1)[1]))
        # a live override moves the name and the hull box on the running boss
        pg2.evaluate("() => BOSSMODE.override.apply('stormsovereign', {name:'STORM TEST', w:200, h:200})")
        pg2.wait_for_timeout(100)
        s=pg2.evaluate("() => BOSSMODE.snapshot()")
        ok(s['boss']['name']=='STORM TEST' and s['boss']['w']==200, 'override applied to the LIVE boss: %s w=%s' % (s['boss']['name'], s['boss']['w']))
        pg2.evaluate("() => BOSSMODE.override.reset('stormsovereign')")
        s=pg2.evaluate("() => BOSSMODE.snapshot()")
        ok(s['boss']['name']=='STORM SOVEREIGN MK II' and s['boss']['w']==286, 'reset restores the shipped row: %s w=%s' % (s['boss']['name'], s['boss']['w']))
        pg2.evaluate("() => BOSSMODE.stop()")
        pg2.wait_for_function("() => BOSSMODE.state==='bmhost'", timeout=10000)
        ok(True, 'BOSSMODE.stop() returns the host to bmhost')
        ok(pg2.evaluate("() => localStorage.getItem('bof_bossmode')")=='{}', 'a reset leaves no override saved')
        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:10]: print('   ', e)
    print('shots ->', a.out)
    sys.exit(1 if fails else 0)

if __name__=='__main__':
    main()
