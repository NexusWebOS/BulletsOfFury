"""probe_optback_0903.py - the OPTIONS rebind owns every key while PRESS KEY is lit.

Mike (0903): "in the options menu, while assigning buttons, pressing b/back should not exit us back to the
main menu until we are done mapping our button."

Real Chromium, real index.html, keys delivered as keydown events. Four cases: backspace mid-rebind BINDS and
stays on the screen; escape mid-rebind cancels the capture only; k mid-rebind binds; backspace with nothing
armed leaves OPTIONS through optCancel (the snapshot is restored). Prints PASS/FAIL.

    python _BUILD_SOURCE/probe_optback_0903.py
"""
spec = importlib.util.spec_from_file_location("shoot", os.path.abspath('_BUILD_SOURCE/shoot.py'))
sh = importlib.util.module_from_spec(spec); spec.loader.exec_module(sh)
from playwright.sync_api import sync_playwright
port, stop = sh.serve(sh.GAME)
KEY = "(k)=>{ window.dispatchEvent(new KeyboardEvent('keydown',{key:k,code:k,bubbles:true})); window.dispatchEvent(new KeyboardEvent('keyup',{key:k,code:k,bubbles:true})); }"
with sync_playwright() as p:
    b = p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    pg = b.new_page(viewport={'width':960,'height':1040}); errs=[]
    pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.goto('http://127.0.0.1:%d/index.html'%port, wait_until='load', timeout=120000)
    pg.wait_for_function("() => typeof state!=='undefined' && (window.__bofFrames|0) > 4", timeout=120000)
    pg.evaluate(sh.TRAP_RAF); pg.evaluate("() => { ASSETS.ready = true; }")
    pg.evaluate("() => { setState(GS.OPTIONS); optSnapshot(); menuIndex=0; }"); pg.evaluate(sh.STEP, 5)
    def snap(): return pg.evaluate("() => ({state: state, opt: state===GS.OPTIONS, title: state===GS.TITLE, rebind: rebindAction, fire: keybind.fire.slice(), bomb: keybind.bomb.slice()})")
    s0=snap(); print(' start          :', s0)
    # 1. arm a rebind on FIRE, then press BACKSPACE (a back key): must stay in OPTIONS and bind it
    pg.evaluate("() => { rebindAction='fire'; rebindWho=1; }"); pg.evaluate(sh.STEP, 1)
    pg.evaluate(KEY, 'Backspace'); pg.evaluate(sh.STEP, 2); s1=snap(); print(' back mid-rebind:', s1)
    # 2. arm BOMB, press ESCAPE: cancels the capture only, stays in OPTIONS, bomb unchanged
    pg.evaluate("() => { rebindAction='bomb'; rebindWho=1; }"); pg.evaluate(sh.STEP, 1)
    pg.evaluate(KEY, 'Escape'); pg.evaluate(sh.STEP, 2); s2=snap(); print(' esc mid-rebind :', s2)
    # 3. arm FIRE again, press K (keyboard back): must bind, not exit
    pg.evaluate("() => { rebindAction='fire'; rebindWho=1; }"); pg.evaluate(sh.STEP, 1)
    pg.evaluate(KEY, 'k'); pg.evaluate(sh.STEP, 2); s3=snap(); print(' k mid-rebind   :', s3)
    # 4. no capture, press BACKSPACE: leaves OPTIONS through CANCEL (snapshot restored)
    pg.evaluate(KEY, 'Backspace'); pg.evaluate(sh.STEP, 2); s4=snap(); print(' back, no rebind:', s4)
    ok = s1['opt'] and s1['rebind'] is None and s1['fire'][0]=='backspace' and s2['opt'] and s2['rebind'] is None and s2['bomb']==s0['bomb'] and s3['opt'] and s3['fire'][0]=='k' and s4['title'] and s4['fire']==s0['fire']
    print(' RESULT:', 'PASS' if ok else 'FAIL', '| page errors:', errs[:2])
    b.close()
stop()
