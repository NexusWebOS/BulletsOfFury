#!/usr/bin/env python3
"""
probe_start_menu_1022.py - the game-mode START menu, and no BACK out of a game mode (Mike, 2026-10-22).

Real Chromium, the real loop stepped (TRAP_RAF + STEP), keys through real KeyboardEvents, a pad through a stubbed
navigator.getGamepads read by the game's own pollGamepad.
  1. B (pad b1), Escape and K do NOT leave difficulty, pilot select, the campaign hub or the live campaign map;
  2. the co-op seat rewind and the map's button bar still take B (moves inside a screen);
  3. P / pad START opens the menu with exactly the six rows; B and START close it; Enter does NOT open it;
  4. SAVE GAME writes a campaign slot from the map; arcade cannot save; LOAD GAME from pilot select opens the map;
  5. OPTIONS returns to the menu, not to the title;
  6. FORGE / LOADOUT opens the Forge without refilling the stage's upgrades, then the loadout, then the map;
  7. RETURN TO MENU reaches the title; QUIT GAME exits;
  8. busted arm: window.SM22_OFF=1 lets B leave pilot select again (the lock is what stops it);
  9. 0 page / console errors.
--shots writes proof frames to docs/proofs/start_menu_1022/.
"""
import os, sys, base64
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
N = {'ok': 0}; FAILS = []
SHOTS = '--shots' in sys.argv
OUT = os.path.join(ROOT, 'docs', 'proofs', 'start_menu_1022')
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

PAD = """() => {
  window.__pad={id:'probe pad', index:0, connected:true, mapping:'', axes:[0,0,0,0], buttons:Array.from({length:17},()=>({pressed:false,value:0}))};
  navigator.getGamepads=()=>[window.__pad];
  window.__press=(k)=>{ window.dispatchEvent(new KeyboardEvent('keydown',{key:k,bubbles:true})); window.__step(1); window.dispatchEvent(new KeyboardEvent('keyup',{key:k,bubbles:true})); };
  window.__btn=(i)=>{ window.__pad.buttons[i].pressed=true; window.__step(1); window.__pad.buttons[i].pressed=false; window.__step(1); };
}"""

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
        pg.evaluate(PAD)
        def settle(n=40): pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", n)
        def state(): return pg.evaluate("() => state")
        def press(k): pg.evaluate("(k) => window.__press(k)", k); settle()
        def btn(i): pg.evaluate("(i) => window.__btn(i)", i); settle()
        def ev(js, a=None): return pg.evaluate(js, a) if a is not None else pg.evaluate(js)
        def go(st, mode='arcade'):
            ev("(a) => { run.mode=a[1]; passwordDifficulty=false; coopOn=false; menuIndex=0; setState(a[0]); for(let i=0;i<70;i++) window.__step(1); }", [st, mode])
        def opened(): return ev("() => !!SM22.open")
        def shot(name):
            if not SHOTS: return
            os.makedirs(OUT, exist_ok=True)
            d = ev("() => document.getElementById('screen').toDataURL('image/png')")
            open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',')[1]))
        def backs(st, mode='arcade'):
            out = {}
            for name, act in (('b1', lambda: btn(1)), ('escape', lambda: press('escape')), ('k', lambda: press('k'))):
                go(st, mode); act(); out[name] = state()
            return out

        # ---- 1. no BACK out of a game mode
        for st, mode in (('diff', 'arcade'), ('pilot', 'arcade'), ('diff', 'campaign'), ('camphub', 'campaign'), ('pilot', 'campaign')):
            r = backs(st, mode)
            ok(all(v == st for v in r.values()), 'B / Escape / K stay on %s (%s) - %s' % (st, mode, r))
        r = backs('credits')
        ok(all(v == 'title' for v in r.values()), 'control: credits is not a game mode and still backs out (%s)' % r)

        # ---- 3. the menu on pilot select
        go('pilot')
        press('Enter'); ok(not opened(), 'Enter does not open the menu (it confirms; state %s)' % state())
        go('pilot'); press('p')
        ok(opened() and state() == 'pilot', 'P opens the menu over pilot select')
        rows = ev("() => SM22_ROWS.slice()")
        ok(rows == ['RETURN TO MENU', 'SAVE GAME', 'LOAD GAME', 'OPTIONS', 'FORGE / LOADOUT', 'QUIT GAME'], 'exactly the six rows (%s)' % rows)
        settle(60); shot('pilot_menu')
        btn(1); ok(not opened() and state() == 'pilot', 'B closes the menu and stays on pilot select')
        btn(9); ok(opened(), 'the pad START opens it'); settle(60); btn(9)
        ok(not opened(), 'and START closes it')
        # arcade: SAVE refuses with a reason
        btn(9); settle(60); ev("() => { SM22.sel=1; }"); press('j')
        ok(opened() and ev("() => SM22.mode") == 'root' and 'ARCADE' in ev("() => SM22.msg"), 'arcade SAVE GAME refuses with a reason (%s)' % ev("() => SM22.msg"))
        # OPTIONS returns to the menu
        ev("() => { SM22.sel=3; }"); press('j')
        ok(ev("() => SM22.mode") == 'options', 'OPTIONS opens inside the menu')
        settle(20); shot('pilot_options')
        btn(1)
        ok(opened() and ev("() => SM22.mode") == 'root' and state() == 'pilot', 'B on OPTIONS comes back to the menu, not the title (%s)' % state())
        # RETURN TO MENU
        settle(30); ev("() => { SM22.sel=0; }"); press('j')
        ok(state() == 'title' and not opened(), 'RETURN TO MENU reaches the title (%s)' % state())

        # ---- the live campaign map
        def live_map():
            ev("""() => { localStorage.removeItem('bof_campaign_slot0'); run.mode='campaign'; run.pilot='cole'; run.stage=2; coopOn=false;
                     campaign.unlockedMax=3; campaign._booted=true; campaign._introSeen=true; openStageSelect(2,{}); }""")
            for _ in range(40):
                settle(60)
                if ev("() => state===GS.STAGESEL && campPauseIsCampaignScreen() && !sselUnlockCine && sselBoot===0"): return True
            return False
        ok(live_map(), 'the campaign map goes live (state %s)' % state())
        r = {}
        for name, act in (('b1', lambda: btn(1)), ('escape', lambda: press('escape')), ('k', lambda: press('k'))):
            act(); r[name] = (state(), ev("() => cmap2.focus"))
        ok(all(v == ('stagesel', 'map') for v in r.values()), 'B / Escape / K stay on the live map and do not even open the bar (%s)' % r)
        # the bar still takes B (a move inside the screen)
        ev("() => { cmap2.focus='bar'; }"); btn(1)
        ok(state() == 'stagesel' and ev("() => cmap2.focus") == 'map', 'B on the button bar drops back to the map, still on the map')
        press('p'); ok(opened(), 'P opens the menu over the map')
        settle(60); shot('map_menu')
        ev("() => { SM22.sel=1; }"); press('j')
        ok(ev("() => SM22.mode") == 'save', 'SAVE GAME opens the slot list on the map')
        settle(30); shot('map_save'); press('j')
        saved = ev("() => !!localStorage.getItem('bof_campaign_slot0')")
        ok(saved and ev("() => SM22.mode") == 'root', 'it writes slot 1 and comes back to the menu (%s)' % ev("() => SM22.msg"))
        # FORGE / LOADOUT opens Decker's Upgrade Center (upgrade_center_1022.js); its Forge keeps the stage budget
        before = ev("() => { run.forgeCombos=0; run.forgeRespecs=1; return [run.forgeCombos, run.forgeRespecs]; }")
        ev("() => { SM22.sel=4; }"); press('j'); settle(60)
        ok(ev("() => UC22.open") and state() == 'stagesel', 'FORGE / LOADOUT opens Decker\'s Upgrade Center')
        ev("() => { UC22.sel=0; UC22.t=1; }"); press('j')
        after = ev("() => [state, run.forgeCombos, run.forgeRespecs]")
        ok(after[0] == 'forge' and after[1:] == before, 'its FORGE opens the Forge and keeps the stage budget %s (%s)' % (before, after))
        settle(40); shot('forge_from_map')
        press('p'); settle(160)
        ok(state() == 'stagesel' and ev("() => UC22.open"), 'Forge START comes back to the map and Decker (%s)' % state())
        ev("() => { UC22.sel=1; UC22.t=1; }"); press('j'); settle(40)
        ok(state() == 'loadout', 'its LOADOUT opens the loadout (%s)' % state())
        press('p'); settle(160)
        ok(state() == 'stagesel', 'loadout START comes back to the map (%s)' % state())
        ev("() => { UC22.open=false; UC22.focus=false; }")

        # ---- LOAD from pilot select
        go('pilot', 'arcade'); press('p'); settle(60)
        ev("() => { SM22.sel=2; }"); press('j')
        ok(ev("() => SM22.mode") == 'load', 'LOAD GAME opens the slot list from pilot select')
        ev("() => { SM22.slot.sel=1; }"); press('j'); settle(60)
        ok(state() == 'stagesel' and ev("() => run.mode") == 'campaign' and not opened(), 'loading slot 1 opens the campaign map (%s, %s)' % (state(), ev("() => run.mode")))

        # ---- 2. co-op seat rewind still takes B
        ev("() => { run.mode='arcade'; passwordDifficulty=false; coopOn=true; coopPick=1; setState(GS.PILOT); for(let i=0;i<70;i++) window.__step(1); }")
        btn(1)
        ok(state() == 'pilot' and ev("() => coopPick") == 0, 'co-op: B on P2 still hands the pick back to P1')
        ev("() => { coopOn=false; }")

        # ---- 8. busted arm
        ev("() => { window.SM22_OFF=1; }"); go('pilot'); btn(1)
        bust = state()
        ev("() => { window.SM22_OFF=0; }")
        ok(bust == 'diff', 'busted arm: with the lock off, B leaves pilot select again (%s)' % bust)

        # ---- QUIT GAME
        go('pilot'); press('p'); settle(60); ev("() => { SM22.sel=5; }"); press('j')
        ok(state() == 'exited', 'QUIT GAME exits (%s)' % state())

        real = [e for e in errs if 'favicon' not in e and 'AudioContext encountered an error' not in e]
        ok(not real, 'page/console errors: %d %s' % (len(real), real[:3]))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL ' + f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
