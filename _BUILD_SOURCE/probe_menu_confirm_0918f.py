#!/usr/bin/env python3
"""
probe_menu_confirm_0918f.py - the A / J button presses every menu (Mike, 0918: "my A/J button doesnt press in the
menu's even when I map it").

Real Chromium, the real loop stepped frame by frame (TRAP_RAF + STEP), keys through real KeyboardEvents and a pad
through a stubbed navigator.getGamepads - the game's own pollGamepad reads it exactly as it reads a real pad.
  1. keyboard J confirms title -> mode select -> difficulty -> pilot, and RESUME in the pause menu;
  2. a STANDARD pad's A (b0) does the same;
  3. a SIX-BUTTON pad whose A reports as b2 (bound to CHARGE) confirms menus too;
  4. remapping b1 onto FIRE moves it off BOMB, and b1 then CONFIRMS instead of going BACK;
  5. B (b1 by default), Escape and K still go BACK;
  6. 0 page / console errors.
"""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
N = {'ok': 0}; FAILS = []
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
        br = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1000, 'height': 1100}); errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=90000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=90000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { window.__step=%s; }" % sh.STEP)
        pg.evaluate(PAD)
        def go(st):   # land on a screen and let it settle past its input delay
            pg.evaluate("(s) => { menuIndex=0; modeIndex=1; if(typeof diffIndex!=='undefined') diffIndex=1; setState(s); for(let i=0;i<50;i++) window.__step(1); }", st)
        def settle(n=40): pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", n)
        def state(): return pg.evaluate("() => state")
        def press(k): pg.evaluate("(k) => window.__press(k)", k); settle()
        def btn(i): pg.evaluate("(i) => window.__btn(i)", i); settle()

        # ---- 1. keyboard J
        chain = []
        go('title'); press('j'); chain.append(state())
        press('j'); chain.append(state())
        press('j'); chain.append(state())
        ok(chain == ['modesel', 'diff', 'pilot'], 'keyboard J confirms title -> mode -> difficulty (%s)' % chain)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; setState('paused'); for(let i=0;i<70;i++) window.__step(1); playPause.sel=0; }" % sh.STEP)
        press('j')
        ok(state() == 'play', 'keyboard J picks RESUME in the pause menu (%s)' % state())

        # ---- 2. a standard pad's A
        chain = []
        go('title'); btn(0); chain.append(state())
        btn(0); chain.append(state())
        ok(chain == ['modesel', 'diff'], "a standard pad's A (b0) confirms (%s)" % chain)

        # ---- 3. a six-button pad whose A reports as b2 (CHARGE)
        chain = []
        go('title'); btn(2); chain.append(state())
        btn(2); chain.append(state())
        btn(2); chain.append(state())
        ok(chain == ['modesel', 'diff', 'pilot'], 'a pad whose A reports as b2 confirms every menu (%s)' % chain)
        b5 = (go('diff'), btn(5), state())[2]
        ok(b5 == 'pilot', 'and as b5 (%s)' % b5)

        # ---- 4. remap b1 onto FIRE through the real options capture
        rb = pg.evaluate("""() => { setState(GS.OPTIONS); for(let i=0;i<40;i++) window.__step(1);
            rebindAction='fire'; rebindWho=1; window.__pad.buttons[1].pressed=true; window.__step(1); window.__pad.buttons[1].pressed=false; window.__step(1);
            return {fire:keybind.fire.slice(), bomb:keybind.bomb.slice(), armed:rebindAction}; }""")
        ok('pad_b1' in rb['fire'] and 'pad_b1' not in rb['bomb'] and rb['armed'] is None,
           'mapping b1 onto FIRE moves it off BOMB (fire %s, bomb %s)' % (rb['fire'], rb['bomb']))
        go('diff'); btn(1)
        ok(state() == 'pilot', 'and b1 then CONFIRMS a menu instead of going back (%s)' % state())
        # (next arm needs the default binds back)
        pg.evaluate("() => { for(const a in KEYBIND_DEFAULT) keybind[a]=KEYBIND_DEFAULT[a].slice(); }")

        # ---- 5. back still works
        backs = {}
        for name, act in (('b1', lambda: btn(1)), ('escape', lambda: press('escape')), ('k', lambda: press('k'))):
            go('diff'); act(); backs[name] = state()
        ok(all(v not in ('diff', 'pilot') for v in backs.values()), 'B (b1), Escape and K still go BACK off difficulty (%s)' % backs)

        real = [e for e in errs if 'favicon' not in e and 'AudioContext encountered an error' not in e]
        ok(not real, 'page/console errors: %d %s' % (len(real), real[:3]))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL ' + f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
