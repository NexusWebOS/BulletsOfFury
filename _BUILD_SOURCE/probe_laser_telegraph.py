"""probe_laser_telegraph.py - backlog item 7, behaviour half.

Mike: "it should flash for 3 seconds on/off and an alert symbol of ours should pop up above the
enemy, go from the yellow to red with the sound".

⚠ THIS PROBE WATCHES THE CONSOLE, NOT JUST THE STATE. Every state draw in this game runs under a
try/catch that logs `draw error in state <s>` and moves on - so a ReferenceError in the new symbol
draw costs no crash, no dropped frames and no visible failure: the symbol simply never appears and
the game holds 60fps. That is the 0902a `_dialogueReady` class of bug and nothing but the console
catches it.

Asserts, on the real Stage-3 boss:
  * the warn is Mike's 3.00s, not the authored 1.00
  * the draw ASKS FOR nwarn_yield in the first 60% and nwarn_alert after it (recorded by wrapping
    XART.get - XART.get returns a canvas with no .src, so a blit cannot be identified any other way)
  * the sign blinks rather than sitting solid
  * zero page/console errors
"""
import os, sys, base64, importlib.util, json

spec = importlib.util.spec_from_file_location("shoot", os.path.abspath('_BUILD_SOURCE/shoot.py'))
sh = importlib.util.module_from_spec(spec); spec.loader.exec_module(sh)
from playwright.sync_api import sync_playwright

OUT = 'docs/proofs/laser_telegraph_0905'; os.makedirs(OUT, exist_ok=True)
CAP = "() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }"
HOOK = """() => { window.__k=[]; const o=XART.get.bind(XART);
  XART.get=function(k){ if(typeof k==='string') window.__k.push(k); return o(k); }; return true; }"""

port, stop = sh.serve(sh.GAME)
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 960, 'height': 1040})
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:180]))
    pg.on('console', lambda m: errs.append('console: ' + m.text[:180]) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
    pg.wait_for_function("() => typeof state!=='undefined' && (window.__bofFrames|0) > 4", timeout=120000)
    pg.evaluate(sh.TRAP_RAF)
    pg.evaluate("() => { ASSETS.ready = true; }")
    pg.evaluate(sh.SETUP, {'state': 'PLAY', 'pilot': 'cole', 'stage': 3, 'invuln': True})
    pg.evaluate("""()=>{ run.stage=3; curStage=STAGES[2]; player.dead=false; player.invuln=1e9;
      stagePlan=[]; enemies.length=0; eBullets.length=0;
      spawnBoss('cryospear'); if(boss){ boss.enter=false; boss.x=240; boss.y=150; } }""")
    pg.wait_for_timeout(1200); pg.evaluate(sh.STEP, 30); pg.wait_for_timeout(400)

    # warm both plates before judging - XART.rdy is false on its first call
    for _ in range(12):
        pg.evaluate("()=>{XART.rdy('nwarn_yield');XART.rdy('nwarn_alert');}")
        pg.evaluate(sh.STEP, 3); pg.wait_for_timeout(90)
    rdy = pg.evaluate("()=>({y:XART.rdy('nwarn_yield'),r:XART.rdy('nwarn_alert')})")
    print('symbol plates ready:', rdy, flush=True)

    pg.evaluate("""()=>{ boss._l23Beam=null;
      l23BossBeamStart(boss,'rime',['TL','C','TR'],
        [Math.PI/2-0.31, Math.PI/2, Math.PI/2+0.31], 1.00, 1.05, 0.24, 48); }""")
    warm = pg.evaluate("()=>{const B=boss._l23Beam;return B?B.warm:null;}")
    print('authored warm 1.00 -> effective warm:', warm, flush=True)

    early, late, blink_off, maxf = [], [], 0, 0.0
    for i in range(70):
        pg.evaluate(HOOK)
        pg.evaluate(sh.STEP, 2); pg.wait_for_timeout(55)
        st = pg.evaluate("""()=>{ const B=boss&&boss._l23Beam; const ks=window.__k||[];
          return {t:B?+B.t.toFixed(2):null, rel:B?!!B.released:null,
                  y:ks.indexOf('nwarn_yield')>=0, r:ks.indexOf('nwarn_alert')>=0}; }""")
        if st['t'] is None: break
        f = st['t'] / warm
        maxf = max(maxf, f)
        if not st['rel']:
            if not st['y'] and not st['r']: blink_off += 1
            if f < 0.55: early.append((st['y'], st['r']))
            elif f < 0.98: late.append((st['y'], st['r']))
        if i in (4, 44):
            d = pg.evaluate(CAP)
            if d: open(os.path.join(OUT, 'warn_%s.png' % ('yellow' if i == 3 else 'red')), 'wb').write(
                base64.b64decode(d.split(',', 1)[1]))

    y_early = sum(1 for y, r in early if y); r_early = sum(1 for y, r in early if r)
    y_late  = sum(1 for y, r in late if y);  r_late  = sum(1 for y, r in late if r)
    print('first 55%% of warn : yellow %d, red %d' % (y_early, r_early), flush=True)
    print('last  45%% of warn : yellow %d, red %d' % (y_late, r_late), flush=True)
    print('frames with the sign blinked OFF: %d' % blink_off, flush=True)
    print('max warn fraction reached: %.2f' % (maxf,), flush=True)
    print('errors:', errs[:4] if errs else 'none', flush=True)
    b.close()
stop()

fails = []
if not warm or abs(warm - 3.00) > 0.001: fails.append('warn is %s, not Mike\'s 3.00' % warm)
if y_early == 0: fails.append('the YELLOW sign never drew in the first half')
if r_early != 0: fails.append('the RED sign drew too early')
if r_late == 0:  fails.append('the sign never went RED')
if blink_off == 0: fails.append('the sign never blinked off - it is solid, not flashing')
if errs: fails.append('errors (a swallowed draw error hides the symbol): %s' % errs[:2])
print('\n' + ('PASS - 3s telegraph, yellow then red, blinking, no errors' if not fails
              else 'FAIL:\n  ' + '\n  '.join(fails)))
sys.exit(1 if fails else 0)
