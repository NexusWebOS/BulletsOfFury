#!/usr/bin/env python3
"""
probe_killpoints_0917.py - ARCADE KILL POINTS, IN REAL CHROMIUM.

Mike, 0917: "Begin wiring up text for when you kill enemies of how many points you gained per kill
arcade style with our font."

Kills an enemy on stage 1 through the real damage path and reads the floater back: it must be
tagged as a score floater, carry a '+', rise, and be drawn through the STAGE font (stageText),
not through the canvas BOFmil fallback the old floater used. The screenshot is taken INSIDE the
frame that draws it - a frame taken after the run shows nothing (0916 escape-arrow lesson).
"""
import os, sys, base64
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'killpoints_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)
def shot(pg, name):
    d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
    if d: open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof killEnemy==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        # let the stage art land - a synchronous burst never yields to the network
        for _ in range(4):
            pg.evaluate(sh.STEP, [10]); pg.wait_for_timeout(400)
        pg.wait_for_function("() => typeof curFontArt==='function' && !!curFontArt()", timeout=20000)

        # spawn a plain unit in view and kill it through the real path
        info = pg.evaluate("""() => {
          const e = spawnEnemy('drone', {x: 240, y: 260}); if(!e) return null;
          e.x = 240; e.y = 260; e.score = e.score || 150;
          floaters.length = 0;
          window.__st = []; const _o = stageText;
          window.__stOrig = _o;
          stageText = function(a, t, cx, cy, H, col){ window.__st.push({t:String(t), cx, cy, H, col}); return _o.apply(this, arguments); };
          /* ENG-05 (0915): a fresh hull SURVIVES its first lethal hit at 1hp, and the second finishes
             it. One 9999 is the no-one-shot rule working; the kill is two hits by design. */
          hitEnemy(e, 9999); hitEnemy(e, 9999);
          return {score: e.score, dead: !!(e.dead || e._dyingT != null)}; }""")
        ok(info and info['dead'], 'a unit killed through the real damage path (%s)' % info)
        fl = pg.evaluate("() => floaters.map(f => ({txt:f.txt, score:!!f.score, col:f.color, y:f.y}))")
        print('  floaters:', fl)
        sc = [f for f in fl if f['score']]
        ok(len(sc) == 1, 'exactly ONE score floater is pushed for the kill (%d)' % len(sc))
        ok(sc and sc[0]['txt'].startswith('+') and sc[0]['txt'][1:].isdigit(),
           'and it reads as arcade points: %r' % (sc[0]['txt'] if sc else None))
        y0 = sc[0]['y'] if sc else None

        # draw one frame and see the floater go through the STAGE font
        pg.evaluate("() => { window.__st = []; }")
        pg.evaluate(sh.STEP, [1])
        calls = pg.evaluate("() => window.__st.filter(q => q.t.startsWith('+'))")
        ok(len(calls) >= 1, 'the frame drew it through stageText - the stage face, not canvas BOFmil (%d calls)' % len(calls))
        ok(calls and calls[0]['H'] > 10, 'with the arcade POP - taller than rest size on its first frame (H %.1f)' % (calls[0]['H'] if calls else -1))
        shot(pg, '01_kill.png')

        pg.evaluate(sh.STEP, [6])
        y1 = pg.evaluate("() => (floaters.find(f => f.score) || {}).y")
        ok(y1 is not None and y0 is not None and y1 < y0 - 2, 'and it RISES (%s -> %s)' % (y0, y1))
        pg.evaluate("() => { window.__st = []; }")
        pg.evaluate(sh.STEP, [1])
        later = pg.evaluate("() => window.__st.filter(q => q.t.startsWith('+'))")
        ok(later and abs(later[0]['H'] - (10 if not sc[0]['txt'][1:].isdigit() or int(sc[0]['txt'][1:]) < 1000 else 13)) < 0.6,
           'settling to rest size after the pop (H %.1f)' % (later[0]['H'] if later else -1))

        # a big kill is a bigger, hotter number
        big = pg.evaluate("""() => { const e = spawnEnemy('drone', {x: 300, y: 300}); e.x=300; e.y=300; e.score = 1500;
            floaters.length = 0; hitEnemy(e, 9999); hitEnemy(e, 9999); const f = floaters.find(q => q.score); return f ? {txt:f.txt, big:!!f.big, col:f.color} : null; }""")
        ok(big and big['big'] and big['col'] != sc[0]['col'], 'a 1,500-point kill is tagged BIG and coloured hotter (%s)' % big)

        pg.evaluate(sh.STEP, [70])
        ok(pg.evaluate("() => floaters.filter(f => f.score).length") == 0, 'and they leave on their own')

        # ---- the KILL CHAIN (0917): kills within 1.2s of stage time multiply ----------------------------
        ch = pg.evaluate("""() => { floaters.length=0; run._lastKillT=null; run._chain=0; const s0=run.score|0; stageTimer=10;
            const k=(x)=>{ const e=spawnEnemy('drone',{x:x,y:260}); e.x=x; e.y=260; e.score=200; hitEnemy(e,9999); hitEnemy(e,9999); };
            k(200); stageTimer=10.5; k(240); stageTimer=11.0; k(280);
            const a=floaters.filter(f=>f.score).map(f=>f.txt);
            stageTimer=14.0; k(320);     // 3s later: the chain breaks
            return {txt:a, last: floaters.filter(f=>f.score).slice(-1)[0].txt, chain: run._chain, bonus: (run.score|0)-s0}; }""")
        ok(ch['txt'] == ['+200', '+200 x2', '+200 x3'], 'three kills 0.5s apart on the STAGE clock chain x2, x3 (%s)' % ch['txt'])
        ok(ch['last'] == '+200' and ch['chain'] == 1, 'a kill 3s later breaks the chain (%s)' % ch['last'])
        ok(ch['bonus'] - 4*200 == 50 + 100, 'the chain pays a quarter of the kill per step on top of the four kills themselves: 50 + 100 (%d - 800)' % ch['bonus'])
        pg.evaluate("() => { stageText = window.__stOrig; }")
        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]: print('    !', e)
        br.close(); stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
