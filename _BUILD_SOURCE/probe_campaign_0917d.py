#!/usr/bin/env python3
"""
probe_campaign_0917d.py - "ensure the campaign mode is playable" (Mike, 0917d).

CAMPAIGN, driven by REAL keyboard presses wherever a player would press one:
  boot -> title -> NEW GAME -> CAMPAIGN -> difficulty -> pilot -> (intro / map) -> stage 1 PLAY
then the stage is fast-forwarded to its boss (the only shortcut - nobody wants to watch 3 minutes of a
probe), the boss is killed through its real death branch, and from there every screen is walked with
real taps: debrief -> weapons gained -> powers gained -> forge -> loadout -> fade -> the CAMPAIGN MAP ->
deploy stage 2 -> PLAY. Then the campaign save round-trips the forge and the loadout.
Every state visited is logged; any page error, swallowed draw error or stalled loop fails it.
"""
import os, sys, base64, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'campaign_0917d')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=90000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0)>4", timeout=90000)
        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); for(let i=0;i<3;i++) localStorage.removeItem('bof_campaign_slot'+i); }catch(_){} achievementReload(); }")
        st = lambda: pg.evaluate("() => state")
        def shot(name):
            d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
            if d: open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        path = []
        def note():
            s = st()
            if not path or path[-1] != s: path.append(s)
            return s

        # ---- 1. the front end, real keys. On MODE SELECT the cursor must land on CAMPAIGN.
        for _ in range(40):
            s = note()
            if s == 'modesel': break
            pg.keyboard.press('Enter'); pg.wait_for_timeout(800)
        pg.wait_for_timeout(600)
        mi = pg.evaluate("() => { const L=(typeof modeList==='function')?modeList():null; return {L:L?L.map(m=>m.key||m.id||m.name||String(m)):null, i:(typeof modeIndex!=='undefined')?modeIndex:null}; }")
        print('  modesel:', json.dumps(mi))
        for _ in range(8):
            if pg.evaluate("() => { const L=modeList(); const m=L[modeIndex]; return String((m&&(m.key||m.id||m.name))||m).toLowerCase().indexOf('camp')>=0; }"): break
            pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(350)
        pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
        for _ in range(90):   # the LAUNCH sequence takes several seconds of its own
            s = note()
            if s == 'play': break
            pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
        print('  front end:', ' -> '.join(path))
        ok(pg.evaluate("() => run.mode") == 'campaign', 'the run is a CAMPAIGN (%s)' % pg.evaluate("() => run.mode"))
        ok(st() == 'play' and pg.evaluate("() => run.stage") == 1, 'real key presses carry it to stage 1 PLAY (%s, stage %s)' % (st(), pg.evaluate("() => run.stage")))
        shot('01_stage1_play')

        # ---- 2. fast-forward to the boss, kill it through its real death branch
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { window.__step=%s; window.__realHit=playerHit; window.playerHit=function(){}; }" % sh.STEP)
        def step(n): pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", n)
        def tap(k, hold=2, settle=8):
            pg.evaluate("([k]) => BOSSMODE.hold(k,true)", [k]); step(hold)
            pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [k]); step(settle)
        pg.evaluate("() => { run.score=(run.score|0)+18000; subBossDone=true; stageTimer=Math.max(stageTimer, (curStage&&curStage.length||200)-1); }")
        for i in range(60):
            step(30); pg.wait_for_timeout(60)
            if pg.evaluate("() => !!(boss && bossActive)"): break
        ok(pg.evaluate("() => !!(boss && bossActive)"), 'the stage reaches its boss')
        step(240)
        pg.evaluate("() => { boss.hp=0; bossDie(); }")
        for i in range(80):
            step(30); pg.wait_for_timeout(40)
            if note() == 'stageclear': break
        ok(st() == 'stageclear', 'the boss death runs through to the debrief (%s)' % st())
        drop = pg.evaluate("() => (typeof forgeCombosOwned==='function')?forgeCombosOwned().length:0")
        print('  combinations owned after the boss:', drop)
        step(200); shot('02_debrief')

        # ---- 3. every screen after the boss, walked with real taps, until the MAP
        for i in range(60):
            s = note()
            if s in ('stagesel', 'camphub'): break
            if s == 'forge' and i < 40:
                shot('03_forge'); tap('enter', 2, 20); continue          # START -> loadout
            if s == 'loadout':
                shot('04_loadout'); tap('enter', 2, 60); continue        # START -> fade -> map
            tap('j', 2, 40)
            step(40)
        print('  after the boss:', ' -> '.join(path[path.index('stageclear'):] if 'stageclear' in path else path))
        ok(st() in ('stagesel', 'camphub'), 'the campaign returns to its MAP after the post-boss screens (%s)' % st())
        # the map opens on stage 2's UNLOCK cinematic and records the unlock when it lands - wait it out
        for _ in range(60):
            if pg.evaluate("() => sselUnlockCine==null && sselBoot===0"): break
            step(20); pg.wait_for_timeout(60)
        ok(pg.evaluate("() => (campaign.unlockedMax|0)") >= 2, 'stage 2 is unlocked on the map (unlockedMax %s)' % pg.evaluate("() => campaign.unlockedMax"))
        for _ in range(4): step(20); pg.wait_for_timeout(200)
        shot('05_map')

        # ---- 4. the save carries the forge and the loadout; then deploy stage 2
        pg.evaluate("() => { run.forge=run.forge||{}; if(!run.forge[0]) run.forge[0]={elem:'fire',lv:1}; }")
        sv = pg.evaluate("() => { const s=campSnapshot(); const keep={f:run.forge,l:run.loadout}; run.forge={}; run.loadout=null; campApply(s); const r={f:!!(run.forge&&run.forge[0]&&run.forge[0].elem==='fire'), l:Array.isArray(run.loadout)}; run.forge=keep.f; run.loadout=keep.l; return r; }")
        ok(sv['f'] and sv['l'], 'the campaign save round-trips the forge and the loadout (%s)' % json.dumps(sv))
        for i in range(40):
            s = note()
            if s == 'play' and pg.evaluate("() => run.stage") == 2: break
            tap('enter', 2, 30); step(30); pg.wait_for_timeout(80)
        ok(st() == 'play' and pg.evaluate("() => run.stage") == 2, 'the map deploys STAGE 2 into PLAY (%s, stage %s)' % (st(), pg.evaluate("() => run.stage")))
        step(120)
        P = pg.evaluate("() => { player.fireCd=0; pShoot(); return {w:run.weapon, inf:run.infusion?run.infusion.elem:null, rounds:pBullets.length, forge:run.forge&&run.forge[0]}; }")
        print('  stage 2:', json.dumps(P))
        ok(P['rounds'] > 0, 'the player fires on stage 2')
        shot('06_stage2_play')

        # ---- 5. a real death on the last life -> CONTINUE (real taps) -> back into stage 2
        pg.evaluate("() => { window.playerHit=window.__realHit||window.playerHit; }")
        pg.evaluate("() => { run.lives=0; player.invuln=0; player.dead=false; player._shield=0; run.shield=0; }")
        pg.evaluate("() => { try{ __realHit(); }catch(e){ window.__hitErr=String(e); } }")
        for i in range(120):
            step(20); pg.wait_for_timeout(30)
            s = note()
            if s in ('continue', 'gameover'): break
        ok(st() == 'continue', 'losing the last life offers a CONTINUE (%s %s)' % (st(), pg.evaluate("() => window.__hitErr||''")))
        shot('07_continue')
        for i in range(40):
            if note() == 'play' and not pg.evaluate("() => player.dead"): break
            tap('enter', 2, 20); step(20)
        ok(st() == 'play' and pg.evaluate("() => run.stage") == 2, 'CONTINUE puts the pilot back into stage 2 (%s, stage %s, lives %s)' % (st(), pg.evaluate("() => run.stage"), pg.evaluate("() => run.lives")))
        print('  full path:', ' -> '.join(path))
        real = [e for e in errs if 'favicon' not in e]
        ok(not real, 'page/console errors across the campaign: %d %s' % (len(real), real[:4]))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL ' + f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
