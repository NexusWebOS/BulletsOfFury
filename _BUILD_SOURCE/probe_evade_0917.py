#!/usr/bin/env python3
"""
probe_evade_0917.py - ORDINARY AIR UNITS ROLL OUT OF THE LANE ON HARD AND UP, IN REAL CHROMIUM.

Mike, 0917: "continue improving my boss and enemy AI".

A plain drone on stage 2 with a live player round rising under it. On EASY and NORMAL it must not
move a pixel for it (those stages play exactly as tuned); on INSANITY it commits to a sidestep
and the displacement must STICK through the live loop - a pattern that re-asserts x every frame
would make the evade a per-frame jitter that nets to zero, which is the thing this probe exists to
catch. The cooldown holds afterwards, a tank never evades, and a unit on the world edge rolls
inward.
"""
import os, sys, base64
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'evade_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)
def shot(pg, name):
    d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
    if d: open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

ARM = """() => { player.dead=false; player.invuln=0; window.playerHit=function(){};
  for(const e of enemies) e.dead=true; pBullets.length=0; eBullets.length=0; stageTimer=5; }"""
SPAWN = """(x) => { const e=spawnEnemy('drone',{x:x,y:180}); e.x=x; e.y=180; e.shoots=false; e.hp=500; e.maxhp=500; e.vy=0; e.vx=0; e._evCd=0; return {w:e.w, type:e.type}; }"""
ROUND = """() => { const e=enemies.find(q=>!q.dead); pBullets.push({x:e.x+2, y:e.y+60, vx:0, vy:-9, w:4, h:10, dmg:0, kind:'mg', lv:1, t:0, seat:1, _inf:null}); return e.x; }"""

def run_case(pg, diff, x=240):
    pg.evaluate(ARM)
    pg.evaluate("(d) => { diffKey=d; DIFF=difficultyForRun(run.mode,d); }", diff)
    pg.evaluate(SPAWN, x)
    x0 = pg.evaluate(ROUND)
    xs = []
    for _ in range(12):                       # 0.2s of live loop, a frame at a time
        pg.evaluate(sh.STEP, [1])
        xs.append(pg.evaluate("() => { const e=enemies.find(q=>!q.dead); return e?e.x:null; }"))
    evn = pg.evaluate("() => { const e=enemies.find(q=>!q.dead); return e?(e._evN|0):-1; }")
    return x0, xs, evn

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof enemyEvadeTick==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 2, 'pilot': 'cole'})
        for _ in range(3):
            pg.evaluate(sh.STEP, [10]); pg.wait_for_timeout(400)
        pg.evaluate("() => { Math.random=function(){ return 0.01; }; }")   # every read commits where p>0

        info = pg.evaluate(SPAWN, 240)
        ok(pg.evaluate("() => enemyEvadeEligible(enemies.find(q=>!q.dead))"), 'a stage-2 drone is an eligible air unit (%s)' % info)
        ok(pg.evaluate("() => EVADE_DIFF.easy===0 && EVADE_DIFF.normal===0 && EVADE_DIFF.hard>0 && EVADE_DIFF.insanity>EVADE_DIFF.furious"),
           'EASY and NORMAL never evade; HARD < FURIOUS < INSANITY')

        for diff in ('easy', 'normal'):
            x0, xs, evn = run_case(pg, diff)
            ok(all(abs(x - x0) < 0.5 for x in xs if x is not None) and evn == 0,
               '%s: the drone holds its lane with a round rising under it (max |dx| %.2f, evades %d)' % (diff.upper(), max(abs(x - x0) for x in xs if x is not None), evn))

        x0, xs, evn = run_case(pg, 'insanity')
        dx = [x - x0 for x in xs if x is not None]
        ok(evn == 1 and abs(dx[-1]) >= 14, 'INSANITY: the drone commits ONE evade and the sidestep STICKS through the live loop (dx after 12 frames %.1f)' % dx[-1])
        ok(all(abs(dx[i+1]) >= abs(dx[i]) - 0.5 for i in range(len(dx)-1)), 'monotonic - no pattern re-asserting x under it (%s)' % [round(d, 1) for d in dx])
        ok(dx[-1] < 0, 'and it rolls AWAY from the round\'s side (the round was 2px right of it)')
        shot(pg, '01_insanity_sidestep.png')
        # the cooldown: a second round right after the roll does not re-trigger
        pg.evaluate(ROUND)
        n2 = pg.evaluate("() => { for(let i=0;i<10;i++) enemyEvadeTick(enemies.find(q=>!q.dead), 1/60); return enemies.find(q=>!q.dead)._evN|0; }")
        ok(n2 == 1, 'the cooldown holds: a second round straight after does not re-trigger (%d)' % n2)

        # the edge case: a unit on the left edge rolls INWARD whatever side the round is on
        x0, xs, evn = run_case(pg, 'insanity', x=30)
        ok(evn == 1 and xs[-1] > x0, 'a unit at the left edge rolls inward (%.1f -> %.1f)' % (x0, xs[-1]))

        # tanks never evade
        pg.evaluate(ARM)
        t = pg.evaluate("""() => { const e=spawnEnemy('sandtank',{x:240,y:300}); if(!e) return null; e.x=240; e.y=300; e.shoots=false;
            pBullets.push({x:242, y:360, vx:0, vy:-9, w:4, h:10, dmg:0, kind:'mg', lv:1, t:0, seat:1, _inf:null});
            for(let i=0;i<10;i++) enemyEvadeTick(e, 1/60); return {elig: enemyEvadeEligible(e), n: e._evN|0, vk: e._vkind}; }""")
        ok(t is None or (not t['elig'] and t['n'] == 0), 'a tank never evades (%s)' % t)

        pg.evaluate("() => { diffKey='normal'; DIFF=difficultyForRun(run.mode,'normal'); }")
        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]: print('    !', e)
        br.close(); stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
