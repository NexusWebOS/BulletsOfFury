#!/usr/bin/env python3
"""
probe_ngplus_0917.py - NEW GAME +, IN REAL CHROMIUM.

Mike, 0917: "Dark Matter ... can be only be used in New Game +, a new button you will create and
unlock/make visible after we beat the campaign on any difficulty."

Three claims, each driven through the live screen with real key taps:
  1. before the final clear the row is ABSENT - not locked, not greyed, not there (cursor wraps
     over five rows, the draw asks for no NG+ plate, the mouse has nothing to hit);
  2. after the final clear it is the sixth row, drawn from its own plate, and confirming it lands on
     the CAMPAIGN hub with run.ngplus true - and picking CAMPAIGN afterwards clears it;
  3. the flag opens the DARK MATTER gate (infusionPool gains 'dark' on an eligible stage), survives a
     campaign save/load round trip, and a password (arcade) start drops it.
"""
import os, sys, base64
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'ngplus_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)
def shot(pg, name):
    d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
    if d: open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

TRAP = """() => {
  window.__keys = [];
  const g = XART.get.bind(XART);
  XART.get = function(k){ window.__keys.push(k); return g(k); };
}"""

def tap(pg, key, frames=3):
    pg.keyboard.press(key)
    pg.evaluate(sh.STEP, [frames])

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof modeList==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { try{ localStorage.removeItem(BONUS_MODE_UNLOCK_KEY); }catch(e){} bonusModesUnlocked=false; }")
        pg.evaluate(sh.SETUP, {'state': 'MODESEL', 'stage': 1, 'pilot': 'cole'})
        # touch every pill and give the loose files real time to decode (the synchronous burst never yields)
        pg.evaluate("() => { for(const it of MODE_ITEMS) XART.rdy(it.pill); }")
        for _ in range(4):
            pg.evaluate(sh.STEP, [10]); pg.wait_for_timeout(400)
        pg.evaluate("() => { modeIndex=0; stateT=1; }")

        # ---- 1. hidden before the final clear -----------------------------------------------------
        n_locked = pg.evaluate("() => modeList().length")
        ok(n_locked == 5 and pg.evaluate("() => MODE_ITEMS.length") == 6,
           'before the final clear the screen walks FIVE rows of a six-row table (%d)' % n_locked)
        pg.evaluate(TRAP)
        pg.evaluate(sh.STEP, [2])
        asked = pg.evaluate("() => window.__keys.filter(k => k==='mode_ngplus_0917').length")
        ok(asked == 0, 'and the draw never asks for the NEW GAME + plate (%d)' % asked)
        for _ in range(5): tap(pg, 'w')      # five UPs from row 0 wrap over five rows and come home
        ok(pg.evaluate("() => modeIndex") == 0, 'five UP presses wrap the five-row menu back to CAMPAIGN')
        shot(pg, '01_locked_five_rows.png')

        # ---- 2. the sixth row after the final clear -----------------------------------------------
        pg.evaluate("() => { run.mode='campaign'; run.stage=CAMPAIGN_STAGES; }")
        ok(pg.evaluate("() => bonusModesUnlockFromCampaign()"), 'the final campaign clear unlocks it (the same signal BOSS RUSH uses)')
        pg.evaluate("() => { run.stage=1; modeIndex=0; }")
        pg.evaluate("() => { XART.rdy('mode_ngplus_0917'); }")
        pg.wait_for_function("() => XART.rdy('mode_ngplus_0917')", timeout=20000)
        ok(pg.evaluate("() => modeList().length") == 6, 'six rows now')
        ok(pg.evaluate("() => modeList()[5].mode==='ngplus' && modeItemOpen(modeList()[5])"), 'the sixth is NEW GAME + and it is OPEN (not a placeholder)')
        pg.evaluate("() => { window.__keys=[]; }")
        pg.evaluate(sh.STEP, [2])
        asked = pg.evaluate("() => window.__keys.filter(k => k==='mode_ngplus_0917').length")
        ok(asked >= 1, 'and the draw blits it from its own plate (%d asks)' % asked)
        rows = pg.evaluate("() => drawModeSelect._rows.map(r => [r.y, r.h])")
        gaps = [rows[i+1][0]-rows[i+1][1]/2 - (rows[i][0]+rows[i][1]/2) for i in range(len(rows)-1)]
        ok(len(rows) == 6 and min(gaps) >= 4 and rows[-1][0]+rows[-1][1]/2 < 472 and rows[0][0]-rows[0][1]/2 > 60,
           'six rows laid out from their own heights: no overlap, inside the field (gaps %s, last bottom %.0f)' % ([round(g) for g in gaps], rows[-1][0]+rows[-1][1]/2))
        tap(pg, 'w')                           # UP from row 0 wraps to the LAST row: NEW GAME +
        ok(pg.evaluate("() => modeIndex") == 5, 'UP from CAMPAIGN wraps onto NEW GAME + (index %d)' % pg.evaluate("() => modeIndex"))
        shot(pg, '02_unlocked_six_rows.png')
        pg.evaluate("() => { run.ngplus=false; }")
        tap(pg, 'Enter', 1)
        for _ in range(40):                    # the white flash runs, then the callback fires
            pg.evaluate(sh.STEP, [3])
            if pg.evaluate("() => state") != 'modesel': break
        st = pg.evaluate("() => ({state, mode: run.mode, ng: !!run.ngplus, coop: !!coopOn})")
        ok(st['state'] == 'camphub' and st['mode'] == 'campaign' and st['ng'] and not st['coop'],
           'CONFIRM lands on the campaign hub with run.ngplus TRUE (%s)' % st)
        shot(pg, '03_camphub_ngplus.png')

        # picking plain CAMPAIGN afterwards must clear it (the coopOn lesson: assign on every branch)
        pg.evaluate("() => { setState(GS.MODESEL); modeIndex=0; stateT=1; }")
        pg.evaluate(sh.STEP, [2])
        tap(pg, 'Enter', 1)
        for _ in range(40):
            pg.evaluate(sh.STEP, [3])
            if pg.evaluate("() => state") != 'modesel': break
        ok(pg.evaluate("() => state==='camphub' && !run.ngplus"), 'and picking CAMPAIGN afterwards clears the flag')

        # ---- 3. the gate, the save, the password ---------------------------------------------------
        pool = pg.evaluate("""() => { const s=run.stage; run.stage=2; run.ngplus=false; const a=infusionPool().indexOf('dark');
            run.ngplus=true; const b=infusionPool().indexOf('dark'); run.stage=s; return [a,b]; }""")
        ok(pool[0] < 0 and pool[1] >= 0, 'DARK MATTER is in the drop pool only with the flag (%s)' % pool)
        rt = pg.evaluate("""() => { run.mode='campaign'; run.ngplus=true; campWriteSlot(2); run.ngplus=false;
            const s=campReadSlot(2); const r=campApply(s); const a=!!run.ngplus;
            run.ngplus=false; s.ngplus=false; campApply(s); return [r,a,!!run.ngplus]; }""")
        ok(rt[0] and rt[1] and not rt[2], 'a campaign save carries it and a plain save does not (%s)' % rt)
        pg.evaluate("() => { try{ localStorage.removeItem(campSlotKey(2)); }catch(e){} }")
        pw_ = pg.evaluate("() => { run.ngplus=true; startRun(3); return [run.mode, !!run.ngplus]; }")
        ok(pw_[0] == 'arcade' and not pw_[1], 'a password start is arcade and drops the flag (%s)' % pw_)

        pg.evaluate("() => { try{ localStorage.removeItem(BONUS_MODE_UNLOCK_KEY); }catch(e){} }")
        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]: print('    !', e)
        br.close(); stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
