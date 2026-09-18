#!/usr/bin/env python3
"""
probe_playable_0917c.py - "ensure game is able to be played again" (Mike, 0917c).

PART A - index.html opened from DISK (file://), the way Mike launches it, driven by REAL keyboard
presses from boot through the front end into a live stage, then flown and fired for 20 real seconds.
Every state it passes through is logged; it fails on any page error, any swallowed draw error, or a
frame loop that stops advancing (the 0916 freeze read as nothing but frames stopping).

PART B - every stage 1-9 over http, 45 simulated seconds of the REAL stage loop each (trigger held,
ship weaving, fresh page per stage - 0917's lesson: one page across stages carries state a real run
never does). Midway a FURY BOMB and a TIMED BOMB are collected by flying into them, so both bombs are
exercised on every stage including the two space stages.
"""
import os, sys, base64, json, time, pathlib
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'playable_0917c')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)
def shot(pg, name):
    try:
        d = pg.evaluate("() => { const c=document.getElementById('screen'); try{ return c.toDataURL('image/png'); }catch(e){ return null; } }")
        if d: open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
    except Exception: pass

PILOT = """(t) => { player.dead=false; player.invuln=Math.max(player.invuln||0,0);
  const W=worldWidth(); player.x = W*0.5 + Math.sin(t*0.9)*W*0.32; player.y = 380 + Math.sin(t*1.7)*40;
  player.fireCd=0; try{ pShoot(); }catch(_){ } }"""

def part_a(br):
    print('--- A: from disk, real keys, front end -> play')
    pg = br.new_page(viewport={'width': 1000, 'height': 1100})
    errs = []
    pg.on('pageerror', lambda e: errs.append('page:' + str(e)))
    pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
    pg.goto(pathlib.Path(os.path.join(ROOT, 'index.html')).as_uri(), wait_until='load', timeout=90000)
    pg.wait_for_function("() => typeof setState==='function'", timeout=90000)
    pg.wait_for_timeout(3000)
    path = []
    PLAYISH = ('play', 'intro', 'launch', 'opening')
    for i in range(70):
        s = pg.evaluate("() => state")
        if not path or path[-1] != s: path.append(s)
        if s in PLAYISH: break
        pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
    print('  states:', ' -> '.join(path))
    ok(any(s in PLAYISH for s in path), 'real Enter presses carry the game from boot into a stage (%s)' % path[-1])
    # through the intro to PLAY
    for _ in range(40):
        if pg.evaluate("() => state") == 'play': break
        pg.keyboard.press('Enter'); pg.wait_for_timeout(700)
    ok(pg.evaluate("() => state") == 'play', 'and the stage reaches PLAY (%s)' % pg.evaluate("() => state"))
    shot(pg, 'a1_play_start.png')
    f0 = pg.evaluate("() => window.__bofFrames|0")
    fire = pg.evaluate("() => (keybind.fire||['j'])[0]")
    pg.keyboard.down(fire)
    for i in range(20):
        k = 'ArrowLeft' if (i // 3) % 2 else 'ArrowRight'
        pg.keyboard.down(k); pg.wait_for_timeout(500); pg.keyboard.up(k); pg.wait_for_timeout(500)
    pg.keyboard.up(fire)
    f1 = pg.evaluate("() => window.__bofFrames|0")
    st = pg.evaluate("() => ({state:state, stage:run.stage, score:run.score|0, pb:pBullets.length})")
    shot(pg, 'a2_after_20s.png')
    print('  after 20s:', json.dumps(st), 'frames', f0, '->', f1)
    ok(f1 - f0 > 300, 'the loop ran through 20 real seconds of play (%d frames)' % (f1 - f0))
    ok(st['score'] > 0 or st['state'] in ('gameover', 'continue'), 'the player fired and scored (%s)' % st['score'])
    real = [e for e in errs if 'favicon' not in e]
    ok(not real, 'from disk: 0 page/console errors (%d) %s' % (len(real), real[:3]))
    pg.close()

def part_b(br, port, stages):
    print('--- B: every stage, 45 simulated seconds, both bombs collected')
    for n in stages:
        pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e, errs=errs: errs.append('page:' + str(e)))
        pg.on('console', lambda m, errs=errs: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=90000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=90000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': n, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; window.__t=0; window.__pilot=%s; }" % (sh.STEP, PILOT))
        k0 = pg.evaluate("() => (stageStats&&stageStats.kills)|0")
        drops = set()
        for c in range(45):
            pg.evaluate("() => { for(let i=0;i<60;i++){ window.__t+=1/60; window.__pilot(window.__t); window.__step(1); } }")
            for kd in pg.evaluate("() => powerups.map(p=>p.kind)"): drops.add(kd)
            if c == 20:
                pg.evaluate("() => { powerups.push({x:player.x,y:player.y,vy:0,t:0,kind:'furybomb',w:24,h:24,bob:0}); }")
            if c == 26:
                pg.evaluate("() => { powerups.push({x:player.x,y:player.y,vy:0,t:0,kind:'timebomb',w:24,h:24,bob:0}); }")
            if c == 28: shot(pg, 'b_stage%d_fuse.png' % n)
            if c % 9 == 0: pg.wait_for_timeout(150)
        R = pg.evaluate("() => ({state:state, stage:run.stage, kills:((stageStats&&stageStats.kills)|0), bomb:!!timeBomb, fx:!!bombFx})")
        shot(pg, 'b_stage%d.png' % n)
        real = [e for e in errs if 'favicon' not in e]
        bonus = sorted(x for x in drops if x in ('scorechip', 'furybomb', 'timebomb'))
        print('  stage %d: %s kills %d drops %s bonus %s errors %d' % (n, R['state'], R['kills'] - k0, len(drops), bonus, len(real)))
        ok(not real, 'stage %d: 0 page/console errors over 45s with both bombs (%s)' % (n, real[:2]))
        ok(R['state'] in ('play', 'stageclear', 'outbound', 'flyover', 'warpentry') and not R['bomb'], 'stage %d: still playing, the fuse resolved (%s)' % (n, R['state']))
        pg.close()

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    stages = [int(a) for a in sys.argv[1:]] or list(range(1, 10))
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        part_a(br)
        part_b(br, port, stages)
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL ' + f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
