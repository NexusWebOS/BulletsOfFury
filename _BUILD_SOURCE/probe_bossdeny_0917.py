#!/usr/bin/env python3
"""
probe_bossdeny_0917.py - BOSS DENIAL, IN REAL CHROMIUM.

Mike, 0917: "continue improving my boss and enemy AI".

The BLACKSTEEL RAPTOR's lance (three lanes, one safe) and the SIEGE EMBER's broadside (one half then the
other) are driven through the real shipBossAttack with the player parked in a lane. On NORMAL the
safe lane follows the authored beat whatever the player does; on INSANITY (every pick denies) the
safe lane is never the player's and the bank falls on the player's half first. Asserted on the
ROUNDS that left the hull, grouped by lane - not on a flag.
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

LANES = """(n) => { const W=worldWidth(); const c=new Array(n).fill(0);
  for(const q of eBullets){ if(q.dead) continue; c[Math.min(n-1,Math.floor(Math.max(0,q.x)/W*n))]++; } return c; }"""

def volley(pg, pat, lane_n, player_lane, step, vy, w):
    """the pattern's OWN rounds, identified at the muzzle: _shipShot is wrapped and every call the
    pattern makes is recorded with the authored (unscaled) velocity and width it asked for. Other
    mounts fire on their own beats with other numbers and are counted as `other`."""
    return pg.evaluate("""([pat, n, pl, step, vy, w]) => { const W=worldWidth();
      player.x = W*(pl+0.5)/n; eBullets.length=0;
      const b = subBoss; b._sbStep = step-1; b._sbPat=null; b._denied=null; b.fireCd=0; b._l23Beam=null;
      if(!window.__ssOrig){ window.__ssOrig=_shipShot; _shipShot=function(x,y,vx,vy,w,o){ (window.__ss||(window.__ss=[])).push([x,y,vx,vy,w]); return window.__ssOrig.apply(this,arguments); }; }
      window.__ss=[];
      shipBossAttack(b);
      const c=new Array(n).fill(0); let other=0;
      for(const q of window.__ss){ if(Math.abs(q[3]-vy)>0.01 || q[4]!==w){ other++; continue; } c[Math.min(n-1,Math.floor(Math.max(0,q[0])/W*n))]++; }
      return {lanes:c, other, denied:b._denied, pat:b._sbPat, step:b._sbStep, ph: b._sbPhase}; }""", [pat, lane_n, player_lane, step, vy, w])

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof bossDenies==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 3, 'pilot': 'cole'})
        for _ in range(3):
            pg.evaluate(sh.STEP, [10]); pg.wait_for_timeout(400)
        pg.evaluate("() => { player.dead=false; window.playerHit=function(){}; for(const e of enemies) e.dead=true; }")

        # ---- the lance (BLACKSTEEL RAPTOR - ALTBOSS6, pat 'lance', still spawnable by kind) ----------
        sp = pg.evaluate("() => { spawnSubBoss('blacksteel'); return subBoss ? {ship: subBoss._ship, pat: SHIPBOSS[subBoss._ship].pat} : null; }")
        ok(sp and sp['ship'] == 'blacksteel' and sp['pat'] == 'lance', 'the BLACKSTEEL RAPTOR spawned with the lance (%s)' % sp)
        # the lance is the Raptor's SECOND phase (pats:['stormbolts','lance']) - drop it into phase 2
        pg.evaluate("() => { subBoss.y=90; subBoss._entering=false; subBoss.hp=Math.floor(subBoss.maxhp*0.30); subBoss._sbPhase=shipBossPhase(subBoss); }")
        ok(pg.evaluate("() => shipBossPhase(subBoss)") >= 1, 'at 30%% hp the Raptor is in its lance phase (phase %s)' % pg.evaluate("() => shipBossPhase(subBoss)"))
        pg.evaluate("() => { diffKey='normal'; DIFF=difficultyForRun(run.mode,'normal'); }")
        # NORMAL: the safe lane follows the beat (step%3) whatever the player does
        beat_ok = True; seen = []
        for step in (1, 2, 3):
            for pl in (0, 2):
                r = volley(pg, 'lance', 3, pl, step, 2.3, 10)
                if r['pat'] != 'lance': continue
                safe = [i for i, c in enumerate(r['lanes']) if c == 0]
                seen.append((step, pl, safe, r['denied']))
                if safe != [step % 3] or r['denied']: beat_ok = False
        ok(seen and beat_ok, 'NORMAL: the safe lane follows the authored beat, blind to the player (%s)' % seen)
        # INSANITY: every pick denies - the safe lane is never the player's
        pg.evaluate("() => { diffKey='insanity'; DIFF=difficultyForRun(run.mode,'insanity'); }")
        deny_ok = True; seen = []
        for step in (1, 2, 3, 4):
            for pl in (0, 1, 2):
                r = volley(pg, 'lance', 3, pl, step, 2.3, 10)
                if r['pat'] != 'lance': continue
                safe = [i for i, c in enumerate(r['lanes']) if c == 0]
                seen.append((step, pl, safe))
                if r['denied'] != 'lance' or len(safe) != 1 or safe[0] == pl or sum(r['lanes']) != 6: deny_ok = False
        ok(seen and deny_ok, 'INSANITY: the safe lane is NEVER the lane the player is in, still one safe lane and six rounds (%s)' % seen)
        pg.evaluate(sh.STEP, [1]); shot(pg, '02_lance_denied.png')
        pg.evaluate("() => { subBoss=null; subBossActive=false; eBullets.length=0; }")

        # ---- the broadside (SIEGE EMBER, stage 2 mini) ----------------------------------------------
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 2, 'pilot': 'cole'})
        for _ in range(2):
            pg.evaluate(sh.STEP, [5]); pg.wait_for_timeout(300)
        pg.evaluate("() => { player.dead=false; for(const e of enemies) e.dead=true; spawnSubBoss('siegeember'); subBoss.y=90; subBoss._entering=false; subBoss._sbPhase=null; }")
        sb = pg.evaluate("() => subBoss ? {ship: subBoss._ship, pat: SHIPBOSS[subBoss._ship].pat} : null")
        ok(sb and sb['ship'] == 'siegeember', 'the SIEGE EMBER spawned (%s)' % sb)
        pg.evaluate("() => { diffKey='insanity'; DIFF=difficultyForRun(run.mode,'insanity'); }")
        halves = []
        for step in (1, 2):
            for pl in (0, 1):
                r = volley(pg, 'siege', 2, pl, step, 2.0, 12)
                if r['pat'] != 'siege': continue
                halves.append((step, pl, r['lanes'], r['denied']))
        ok(halves and all(l[pl] == 6 and l[1 - pl] == 0 and d == 'siege' for (_, pl, l, d) in halves),
           'INSANITY: the broadside falls on the player\'s half first, both halves, both beats (%s)' % halves)
        pg.evaluate("() => { diffKey='normal'; DIFF=difficultyForRun(run.mode,'normal'); }")
        r = volley(pg, 'siege', 2, 1, 2, 2.0, 12)
        ok(r['pat'] == 'siege' and r['denied'] is None and r['lanes'][0] == 6, 'NORMAL: beat 2 fires the LEFT bank whatever half the player is in (%s)' % r)

        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]: print('    !', e)
        br.close(); stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
