#!/usr/bin/env python3
"""
probe_forge_sequence_0917b.py - Mike's whole post-boss sequence, driven by real key taps in Chromium.

  debrief (the conversion counted on it) -> POWERS GAINED -> THE FORGE (traced hex pointer + menu arrow,
  no square) -> THE FORGING 0-100% -> THE PRODUCT (its REAL rounds in the glass) -> THE LOADOUT (six bays,
  the scrolling pool) -> fade -> the next stage.

Also the crash: index.html opened from file:// and walked to the pilot screen, 0 page errors.
Every frame is saved to docs/proofs/forge_sequence_0917b/.
"""
import os, sys, base64, json, pathlib
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, 'docs', 'proofs', 'forge_sequence_0917b')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        # ---------------------------------------------------------------- 0. file:// - the crash
        pf = br.new_page(viewport={'width': 1000, 'height': 1200})
        ferr = []
        pf.on('pageerror', lambda e: ferr.append('page:' + str(e)))
        pf.on('console', lambda m: ferr.append('console:' + m.text) if m.type == 'error' and 'getImageData' in m.text else None)
        pf.goto(pathlib.Path(os.path.join(ROOT, 'index.html')).as_uri(), wait_until='load', timeout=60000)
        pf.wait_for_function("() => typeof setState==='function'", timeout=60000)
        pf.wait_for_timeout(2500)
        pf.evaluate("() => { try{ setState(GS.PILOT); }catch(_){ } }")
        pf.wait_for_timeout(4000)
        derr = pf.evaluate("() => { const t=document.body.innerText||''; return /DRAW ERROR/.test(t); }")
        framesA = pf.evaluate("() => window.__bofFrames|0"); pf.wait_for_timeout(1500); framesB = pf.evaluate("() => window.__bofFrames|0")
        ok(not ferr, 'file:// pilot screen: 0 taint errors (%s)' % ferr[:2])
        ok(not derr, 'file:// pilot screen: no DRAW ERROR banner')
        ok(framesB > framesA, 'file:// pilot screen: the loop is still running (%d -> %d frames)' % (framesA, framesB))
        d = pf.evaluate("() => { const c=document.getElementById('screen'); try{ return c.toDataURL('image/png'); }catch(e){ return null; } }")
        if d: open(os.path.join(OUT, '00_file_pilot.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        pf.close()

        # ---------------------------------------------------------------- the sequence, over http
        pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof drawForging==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} achievementReload(); }")
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; run.mode='arcade'; run.lives=9; }" % sh.STEP)
        def step(n): pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", n)
        def tap(k, hold=2, settle=6):
            pg.evaluate("([k]) => BOSSMODE.hold(k,true)", [k]); step(hold)
            pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [k]); step(settle)
        def shot(name):
            d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
            if d: open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        def warm(keys):
            pg.evaluate("(ks) => ks.forEach(k=>{ try{ XART.rdy(k); }catch(_){ } })", keys)
            for _ in range(20):
                if pg.evaluate("(ks) => ks.every(k=>{ try{ return XART.rdy(k); }catch(_){ return true; } })", keys): break
                pg.wait_for_timeout(250)
        def settle(n=4):
            for _ in range(n): step(6); pg.wait_for_timeout(200)
        st = lambda: pg.evaluate("() => state")
        K = pg.evaluate("() => ({fire:(keybind.fire||['j'])[0], left:'arrowleft', right:'arrowright', up:'arrowup', down:'arrowdown', start:'enter', back:'escape'})")

        # the boss dropped two combinations for the machine gun this stage
        pg.evaluate("() => { forgeComboGrant('fire',0); forgeComboGrant('ice',0); run.stage=1; run.score=23456; stageStats.scoreStart=0; run._fpLevelDone=false; }")
        warm(['statpanel_full_0916','forge_chamber_0917b','loadout_bays_0917b','inf_fire','inf_ice','nsel_arrow_y','micon_forge_fire_0','micon_forge_fire_0_2','ship_cole','nia_icons'])

        # ---- 1. the debrief says the conversion
        pg.evaluate("() => { drawStageClear._init=false; drawStageClear._res=null; drawStageClear._unShown=false; setState(GS.STAGECLEAR); }")
        for _ in range(12): step(15); pg.wait_for_timeout(120)
        conv = pg.evaluate("() => run._fpLevel")
        ok(conv and conv['fp'] == 23 and conv['score'] == 23456, 'the debrief converted the level: 23,456 -> +23 FURIOUS PTS (%s)' % json.dumps(conv))
        shot('01_debrief_conversion')

        # ---- 2. CONTINUE -> POWERS GAINED, its own screen (0917c). Stage 1 unlocks no weapon, so the weapons
        # page skips itself; the powers page shows ELEMENTS only - fire and ice, no weapon, no product name.
        tap(K['fire']); settle(); tap(K['fire']); settle()
        ok(st() == 'powers', 'CONTINUE opens POWERS GAINED (%s)' % st())
        el = pg.evaluate("() => powersScr ? powersScr.elems : null")
        ok(el == ['fire', 'ice'], 'one bay per ELEMENT the boss gave: %s' % el)
        drawn = pg.evaluate("""() => { const ks=[]; const o=XART.get; XART.get=function(k){ ks.push(k); return o.apply(this,arguments); };
                               try{ window.__step(1); } finally{ XART.get=o; } return ks; }""")
        ok(not any(k.startswith('micon_forge_') for k in drawn), 'and it draws no forged product badge (what it can make is not shown)')
        for _ in range(8): step(20); pg.wait_for_timeout(100)
        shot('02_powers_gained')

        # ---- 3. -> the Forge; FIRE on the MG slot opens its elements; the selector is traced, not a square
        tap(K['fire']); settle(6)
        ok(st() == 'forge', 'the powers page hands on to THE FORGE (%s)' % st())
        pg.evaluate("() => { forge.sel=Math.max(0,(run.loadout||[]).indexOf(0)); }"); step(2)
        tap(K['fire']); settle(3)
        ok(pg.evaluate("() => forge && forge.row===1"), 'FIRE on the machine-gun slot opens its element row')
        # the square is gone: trap strokeRect during one frame of the element row
        # [!] the achievement TOAST (the stage clear just awarded some) draws over every screen and strokes its
        # own card - so the claim is counted on the strokes whose caller is the FORGE, never on all of them
        sq = pg.evaluate("""() => { const who=[]; const o=ctx.strokeRect; ctx.strokeRect=function(){ who.push(String(new Error().stack)); return o.apply(this,arguments); };
                              try{ window.__step(1); } finally{ ctx.strokeRect=o; } return {forge:who.filter(s=>/drawForge/.test(s)).length, all:who.length}; }""")
        ok(sq['forge'] == 0, 'no square selector is stroked by the Forge on its element row (%d of %d strokeRects)' % (sq['forge'], sq['all']))
        trace = pg.evaluate("() => Object.keys(_forgeTrace).filter(k=>k.indexOf('inf_')===0).length")
        ok(trace > 0, 'the hexagon pointer was traced off the element badge (%d trace canvases)' % trace)
        arrow = pg.evaluate("""() => { let n=0; const o=XART.get; XART.get=function(k){ if(/^nsel_arrow/.test(k)) n++; return o.apply(this,arguments); };
                              try{ window.__step(1); } finally{ XART.get=o; } return n; }""")
        ok(arrow > 0, 'the menu arrow is drawn under the highlighted element (%d asks)' % arrow)
        shot('03_forge_selector')
        blink = pg.evaluate("""() => { const s=new Set(); const t0=performance.now(); for(let i=0;i<12;i++){ s.add(Math.floor((t0+i*40)/1000*FSEL_BLINK)%2); } return s.size; }""")
        ok(blink == 2 and pg.evaluate("() => FSEL_BLINK") >= 10, 'the pointer blinks rapidly (%d Hz)' % pg.evaluate("() => FSEL_BLINK"))

        # ---- 4. FIRE welds: THE FORGING, 0-100%
        tap(K['fire'], settle=2)
        ok(st() == 'forging', 'FIRE on an element opens THE FORGING (%s)' % st())
        ok(pg.evaluate("() => run.forge && run.forge[0] && run.forge[0].elem"), 'and the machine gun carries the element')
        seen = set()
        for i in range(24):
            step(6); seen.add(pg.evaluate("() => forging?forging.pct:-9"))
            if i == 12: shot('04_forging_midweld')
        pcts = sorted(x for x in seen if x >= 0)
        ok(pcts and pcts[0] < 40 and max(pcts) >= 60, 'the weld counts up through the percentages (%s..%s)' % (pcts[:1], pcts[-1:]))
        for _ in range(20): step(6)
        ok(pg.evaluate("() => forging && forging.pct")== 100, 'and reaches 100%%')
        shot('05_forged_flash')
        for _ in range(10): step(6)
        ok(st() == 'forged', 'then THE PRODUCT screen (%s)' % st())

        # ---- 5. the product: its REAL rounds, in the glass
        for _ in range(6): step(15); pg.wait_for_timeout(150)
        P = pg.evaluate("() => { const p=forging&&forging.preview; return p?{fired:p.fired, live:p.bullets.length, err:p.err, kinds:[...new Set(p.bullets.map(b=>b.kind))], inf:[...new Set(p.bullets.map(b=>b._inf))]}:null; }")
        ok(P and P['fired'] > 3 and P['live'] > 0 and not P['err'], 'pShoot fired the forged weapon into the preview (%s)' % json.dumps(P))
        ok(P and 'fire' in (P['inf'] or []), 'and its rounds WEAR the element (%s)' % (P and P['inf']))
        leak = pg.evaluate("() => ({pb:pBullets.length, eb:eBullets.length, w:run.weapon})")
        ok(leak['pb'] == 0, 'nothing the preview fired leaked into the live round list (%s)' % json.dumps(leak))
        shot('06_product_preview')

        # ---- 6. -> THE LOADOUT
        tap(K['fire']); settle(4)
        ok(st() == 'loadout', 'CONTINUE opens THE LOADOUT (%s)' % st())
        for _ in range(4): step(10); pg.wait_for_timeout(150)
        shot('07_loadout')
        pool = pg.evaluate("() => loadoutScr.pool.length")
        pg.evaluate("() => { loadoutScr.sel=(run.loadout||[]).findIndex(w=>!FORGE_FIXED[w]); }"); step(2)
        tap(K['fire']); settle(2)
        ok(pg.evaluate("() => loadoutScr.row===1"), 'FIRE on a bay opens the pool (%d weapons)' % pool)
        a0 = pg.evaluate("() => loadoutScr.psel"); tap(K['right']); a1 = pg.evaluate("() => loadoutScr.psel")
        ok(pool < 2 or a1 == (a0 + 1) % pool, 'one RIGHT moves exactly one icon (%d -> %d)' % (a0, a1))
        shot('08_loadout_pool')
        tap(K['back']); settle(2)
        ok(pg.evaluate("() => loadoutScr.row===0"), 'BACK closes the pool')

        # ---- 7. START fades to the next level
        tap(K['start'], settle=2)
        ok(pg.evaluate("() => loadoutScr && loadoutScr.exitT>=0"), 'START begins the fade')
        step(20); shot('09_fade')
        for _ in range(4): step(15)
        ok(st() not in ('loadout', 'forge', 'forging', 'forged', 'unlocks', 'powers', 'stageclear', 'title'), 'and the fade hands on to the next stage (%s)' % st())

        # ---- 8. WEAPONS GAINED is the weapons page (the stage-2 fire orb)
        pg.evaluate("() => { unlocksStart(unlockRowsFor(2,'cole'), function(){ setState(GS.PLAY); }); }")
        for _ in range(10): step(20); pg.wait_for_timeout(100)
        rw = pg.evaluate("() => unlocks.rows")
        ok(rw and rw[0][0] == 'FIRE ORB' and all(len(r) < 4 or r[3] != 'power' for r in rw), 'WEAPONS GAINED carries the weapon unlocks only (%s)' % json.dumps(rw))
        shot('10_weapons_gained')
        pg.evaluate("() => { unlocks=null; setState(GS.PLAY); player.dead=false; player.invuln=0; enemies.length=0; eBullets.length=0; powerups.length=0; }")

        # ---- 9. the bonus pickups, collected by flying into them
        warm(['fury_coin_0917c','fury_bomb_0917c','timed_bomb_0917c','score_bullet_100','score_bullet_250','score_bullet_500','score_bullet_1000'])
        pg.evaluate("""() => { let i=0; for(const v of [100,250,500,1000]) powerups.push({x:player.x-90+i++*60,y:player.y-150,vy:0,t:0,kind:'scorechip',val:v,w:18,h:30,bob:0});
                                powerups.push({x:player.x+160,y:player.y-150,vy:0,t:0,kind:'furybomb',w:24,h:24,bob:0});
                                powerups.push({x:player.x+220,y:player.y-150,vy:0,t:0,kind:'timebomb',w:24,h:24,bob:0}); }""")
        step(6); shot('11_bonus_pickups')
        sc0 = pg.evaluate("() => run.score|0")
        pg.evaluate("() => { const p=powerups.find(q=>q.kind==='scorechip'&&q.val===500); p.x=player.x; p.y=player.y; }"); step(3)
        ok(pg.evaluate("() => run.score|0") - sc0 == 500, 'flying into the 500 bullet scores exactly 500')
        # the fury bomb, with enemies on screen
        pg.evaluate("() => { for(let i=0;i<5;i++){ try{ spawnEnemy('drone', camLeftX()+60+i*70, 120+i*20); }catch(_){ } } for(const e of enemies){ e.shoots=false; } }")
        step(4)
        n0 = pg.evaluate("() => enemies.filter(e=>!e.dead&&e._dyingT==null).length")
        pg.evaluate("() => { const p=powerups.find(q=>q.kind==='furybomb'); p.x=player.x; p.y=player.y; }"); step(2)
        n1 = pg.evaluate("() => enemies.filter(e=>!e.dead&&e._dyingT==null).length")
        ok(n0 >= 3 and n1 == 0, 'the FURY BOMB, collected, blows up everything on screen (%d -> %d)' % (n0, n1))
        step(4); shot('12_fury_bomb')
        # the timed bomb: armed on pickup, beeps, then the wave
        pg.evaluate("() => { powerups.length=0; for(let i=0;i<5;i++){ try{ spawnEnemy('drone', camLeftX()+60+i*70, 100+i*25); }catch(_){ } } for(const e of enemies){ e.shoots=false; }"
                    " powerups.push({x:player.x,y:player.y,vy:0,t:0,kind:'timebomb',w:24,h:24,bob:0});"
                    " powerups.push({x:player.x+120,y:player.y-120,vy:0,t:0,kind:'crate',hp:5,w:30,h:30,wtype:1,bob:0}); }")
        step(3)
        ok(pg.evaluate("() => !!timeBomb"), 'the TIMED BOMB arms when collected')
        beeps = []
        for i in range(12):
            step(15); beeps.append(pg.evaluate("() => timeBomb ? timeBomb.beeps : -1"))
            if i == 8: shot('13_timed_bomb_fuse')
        ok(max(beeps) >= 8, 'and beeps faster and faster (%s)' % beeps)
        for _ in range(10): step(4)
        shot('14_timed_bomb_wave')
        for _ in range(10): step(6)
        rest = pg.evaluate("() => ({alive:enemies.filter(e=>!e.dead&&e._dyingT==null).length, crate:powerups.some(p=>p.kind==='crate'&&!p.dead)})")
        ok(rest['alive'] == 0 and not rest['crate'], 'the wave took every enemy and broke the crate open (%s)' % json.dumps(rest))

        real = [e for e in errs if 'favicon' not in e]
        ok(not real, 'page/console errors across the whole sequence: %d %s' % (len(real), real[:3]))
        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} }")
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL ' + f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
