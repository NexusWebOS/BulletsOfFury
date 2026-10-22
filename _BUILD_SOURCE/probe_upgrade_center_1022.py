#!/usr/bin/env python3
"""
probe_upgrade_center_1022.py - Decker's Upgrade Center on the campaign map (Mike, 2026-10-22).

Real Chromium, the real loop stepped (TRAP_RAF + STEP), keys through real KeyboardEvents.
  1. the landmark draws next to Fury HQ (its island blitted while the map is up);
  2. UP from Stage 1 flies the jet to it; DOWN and B fly back to Stage 1; FIRE there never deploys a stage;
  3. FIRE enters: Decker's screen with THE FORGE / SELECT YOUR LOADOUT / LEAVE;
  4. THE FORGE opens the real Forge and keeps the stage's upgrade budget; its START comes back to the
     map with the jet still parked and Decker's screen open again;
  5. SELECT YOUR LOADOUT opens the real loadout; its START comes back the same way; LEAVE closes;
  6. a click on the island takes the jet there, a second click enters;
  7. the START menu's FORGE / LOADOUT row opens the same screen;
  8. busted arm: window.UC22_OFF=1 - UP from Stage 1 no longer reaches it;
  9. 0 page / console errors.
--shots writes proof frames to docs/proofs/upgrade_center_1022/.
"""
import os, sys, base64
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
N = {'ok': 0}; FAILS = []
SHOTS = '--shots' in sys.argv
OUT = os.path.join(ROOT, 'docs', 'proofs', 'upgrade_center_1022')
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

def main():
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1100, 'height': 900}); errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=90000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=90000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { window.__step=%s; }" % sh.STEP)
        pg.evaluate("""() => { window.__press=(k)=>{ window.dispatchEvent(new KeyboardEvent('keydown',{key:k,bubbles:true})); window.__step(1);
                       window.dispatchEvent(new KeyboardEvent('keyup',{key:k,bubbles:true})); }; }""")
        def settle(n=40): pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", n)
        def real(n=4):
            for _ in range(n): settle(15); pg.wait_for_timeout(250)
        def ev(js, a=None): return pg.evaluate(js, a) if a is not None else pg.evaluate(js)
        def state(): return ev("() => state")
        def press(k): ev("(k) => window.__press(k)", k); settle()
        def shot(name):
            if not SHOTS: return
            os.makedirs(OUT, exist_ok=True)
            d = ev("() => document.getElementById('screen').toDataURL('image/png')")
            open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',')[1]))
        def live_map(cur=1):
            ev("""(c) => { window.UC22_OFF=0; UC22.focus=false; UC22.open=false; UC22.pending=false; window.sselCommitted=false;
                     run.mode='campaign'; run.pilot='decker'; run.stage=c; coopOn=false;
                     campaign.unlockedMax=3; campaign.bonusUnlocked=false; campaign._booted=true; campaign._introSeen=true; openStageSelect(c,{}); }""", cur)
            for _ in range(40):
                settle(60)
                if ev("() => state===GS.STAGESEL && campPauseIsCampaignScreen() && !sselUnlockCine && sselBoot===0"):
                    ev("() => { sselCursor=1; }"); real(2); return True
            return False

        ok(live_map(), 'the campaign map goes live (%s)' % state())
        # 1. drawn next to Fury HQ
        ev("""() => { window.__ucBlits=0; const g=XART.get; window.__ucG=g;
                 XART.get=function(k){ if(k==='uc22_island') window.__ucBlits++; return g.apply(this,arguments); }; }""")
        real(2)
        blits = ev("() => window.__ucBlits"); ev("() => { XART.get=window.__ucG; }")
        ok(blits > 0, 'the Upgrade Center island draws on the map (%d asks)' % blits)
        hq = ev("() => cmap2World('hq')"); uc = ev("() => UC22.pos")
        ok(abs(uc['x'] - hq['x']) < 500 and abs(uc['y'] - hq['y']) < 120, 'it sits beside Fury HQ (HQ %s, center %s)' % (hq, uc))
        # 2. travel there and back
        press('w'); real(6)
        sp = ev("() => [UC22.focus, sselShip&&Math.round(sselShip.x), sselShip&&Math.round(sselShip.y), sselShip&&sselShip.cur]")
        pt = ev("() => uc22Point()")
        ok(sp[0] and sp[3] == 'uc' and abs(sp[1] - pt['x']) < 12 and abs(sp[2] - pt['y']) < 12, 'UP from Stage 1 flies the jet to the Upgrade Center (%s -> %s)' % (sp, pt))
        cam = ev("() => cmap2.cam"); scr = ev("() => [cmap2ToScreen(cmap2World('hq').x,cmap2World('hq').y), cmap2ToScreen(UC22.pos.x,UC22.pos.y)]")
        ok(all(-20 < p['x'] < 500 and 30 < p['y'] < 330 for p in scr), 'the camera frames Fury HQ and the center together (%s)' % scr)
        shot('map_upgrade_center')
        press('s'); real(3)
        ok(not ev("() => UC22.focus") and ev("() => sselCursor") == 1, 'DOWN flies back to Stage 1')
        press('w'); real(2); press('escape'); real(2)
        ok(not ev("() => UC22.focus") and state() == 'stagesel', 'B flies back to Stage 1 and stays on the map (%s)' % state())
        # 3. enter
        press('w'); real(3); press('j'); real(3)
        ok(ev("() => UC22.open") and state() == 'stagesel' and not ev("() => !!window.sselCommitted"), 'FIRE enters the center and deploys nothing (%s)' % state())
        rows = ev("() => UC22_ROWS.slice()")
        ok(rows == ['THE FORGE', 'SELECT YOUR LOADOUT', 'LEAVE'], 'Decker offers %s' % rows)
        real(4); shot('decker_screen')
        # 4. the Forge
        before = ev("() => { run.forgeCombos=1; run.forgeRespecs=0; return [run.forgeCombos, run.forgeRespecs]; }")
        ev("() => { UC22.sel=0; }"); press('j'); real(2)
        after = ev("() => [state, run.forgeCombos, run.forgeRespecs]")
        ok(after[0] == 'forge' and after[1:] == before, 'THE FORGE opens the Forge with the stage budget %s (%s)' % (before, after))
        real(2); shot('forge_from_center')
        press('p'); real(4)
        for _ in range(20):
            if ev("() => UC22.open"): break
            real(1)
        ok(state() == 'stagesel' and ev("() => UC22.open && UC22.focus"), 'Forge START comes back to the map with Decker open again (%s)' % state())
        # 5. the loadout
        ev("() => { UC22.sel=1; UC22.t=1; }"); press('j'); real(2)
        ok(state() == 'loadout', 'SELECT YOUR LOADOUT opens the loadout (%s)' % state())
        press('p'); real(4)
        for _ in range(20):
            if ev("() => UC22.open"): break
            real(1)
        ok(state() == 'stagesel' and ev("() => UC22.open"), 'loadout START comes back to Decker (%s)' % state())
        ev("() => { UC22.sel=2; UC22.t=1; }"); press('j'); real(2)
        ok(not ev("() => UC22.open") and ev("() => UC22.focus") and state() == 'stagesel', 'LEAVE closes the screen, the jet still parked there')
        # 6. the mouse
        press('s'); real(3)
        # the close camera on Stage 1 does not show the island, so frame it the way the boot overview does
        # and drive the map's own input function with a real press edge on the pointer
        def click():
            return ev("""() => { cmap2.cam={x:680,y:330,z:.5}; const q=cmap2ToScreen(UC22.pos.x,UC22.pos.y);
                         Object.assign(Input.mouse,{x:q.x,y:q.y,active:true,inside:true,down:false}); Rival24.mapInput();
                         Input.mouse.down=true; const used=Rival24.mapInput(); Input.mouse.down=false; Rival24.mapInput(); return used; }""")
        u1 = click()
        ok(u1 and ev("() => UC22.focus") and not ev("() => UC22.pending||UC22.open"), 'a click on the island takes the jet there')
        click(); real(3)
        ok(ev("() => UC22.open"), 'a second click enters')
        press('escape'); real(2)
        ok(not ev("() => UC22.open"), 'B leaves the screen')
        # 7. the START menu row
        press('s'); real(3)
        press('p'); real(3)
        ev("() => { SM22.sel=4; SM22.t=1; }"); press('j'); real(4)
        ok(ev("() => UC22.open") and not ev("() => SM22.open") and state() == 'stagesel', "the START menu's FORGE / LOADOUT opens Decker's screen")
        press('escape'); real(2)
        # 8. busted arm
        press('s'); real(2)
        ev("() => { window.UC22_OFF=1; UC22.focus=false; sselCursor=1; }"); real(1); press('w'); real(3)
        ok(not ev("() => UC22.focus"), 'busted arm: with UC22_OFF the center cannot be reached')
        ev("() => { window.UC22_OFF=0; }")
        bad = [e for e in errs if 'favicon' not in e and 'AudioContext encountered an error' not in e]
        ok(not bad, 'page/console errors: %d %s' % (len(bad), bad[:3]))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL ' + f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
