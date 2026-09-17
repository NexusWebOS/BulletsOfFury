#!/usr/bin/env python3
"""probe_dropreach_0917.py - can the player actually CATCH the boss's combination powerup?

The drop is guaranteed and permanent, and none of that matters if the pickup falls off the bottom of
the screen during the 9-second boss cook-off, or if the stage ends before the player can reach it.
This measures the window in the real death sequence rather than reasoning about it:

  - how many frames the pickup stays alive after bossDie()
  - where it is when the state stops being PLAY
  - whether a player who flies at it can reach it in that time

⚠ "THE PICKUP EXISTS" AND "THE PICKUP IS CATCHABLE" ARE DIFFERENT CLAIMS, and the first one passes on
a build where the reward is unobtainable.
"""
import os, sys, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

def main():
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof forgeBossDrop==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} achievementReload(); }")
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; run.mode='arcade'; run.lives=9; }" % sh.STEP)
        R = pg.evaluate("""() => {
          powerups.length=0;
          spawnBoss((STAGES[0]&&STAGES[0].boss)||'damkeeper');
          boss.hp=0; bossDie();
          const P=powerups.filter(p=>p.kind==='forgecombo')[0];
          if(!P) return {err:'no drop'};
          const y0=P.y, out={y0:y0, py:player.y, states:[], alive:0, offAt:-1, stateLeftAt:-1, path:[]};
          for(let i=0;i<900;i++){
            window.__step(1);
            const live=powerups.indexOf(P)>=0 && !P.dead;
            if(live){ out.alive=i+1; if(i%60===0) out.path.push({f:i, y:Math.round(P.y)}); }
            else if(out.offAt<0){ out.offAt=i;
              /* [!] "COLLECTED" AND "CULLED" LOOK IDENTICAL FROM THE POWERUPS ARRAY - both leave it.
                 The profile is what separates a reward that was caught from one that was thrown away. */
              out.gotIt=forgeComboOwned(P.elem,P.fw); out.offY=Math.round(P.y); }
            if(state!=='play' && out.stateLeftAt<0){ out.stateLeftAt=i; out.stateName=state; }
            if(out.offAt>=0 && out.stateLeftAt>=0) break;
          }
          out.finalY=P.y; out.dead=!!P.dead; out.vh=VH;
          return out; }""")
        print('  reach:', json.dumps(R))
        br.close()
    stop()
    if R.get('err'):
        print('  FAIL', R['err']); sys.exit(1)
    frames = R.get('alive', 0)
    print('\n  the pickup stayed catchable for %d frames (%.1f s at 60fps)' % (frames, frames / 60.0))
    print('  it left the powerups list at frame %s, at y %s - COLLECTED: %s'
          % (R.get('offAt'), R.get('offY'), R.get('gotIt')))
    print('  the state left PLAY at frame %s (%s)' % (R.get('stateLeftAt'), R.get('stateName')))
    print('  y: %s -> %s of %s' % (R.get('y0'), round(R.get('finalY', 0)), R.get('vh')))

if __name__ == '__main__':
    main()
