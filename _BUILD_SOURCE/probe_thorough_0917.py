#!/usr/bin/env python3
"""probe_thorough_0917.py - the THOROUGH award, measured on a real stage in real Chromium.

Mike, 0917: "earning a set amount of points thats 75% of what you could accuimalate if you were to
kill all enemies, collect as many items, powerups etc."

  THE CEILING RISES WITH THE STAGE - real waves spawning real enemies raise stageStats.scoreMax, and
  every pickup that appears adds PICKUP_SCORE. Nothing is hand-written, so a wave re-tune cannot rot it.
  THE BAR IS 75%      - a level clearing it earns the row; one just under it does not.
  IT IS THIS LEVEL'S  - the numerator is run.score minus the stage's own scoreStart, the same delta
                        the conversion uses, so a big score carried in from stage 1 cannot buy stage 2.

⚠ A CEILING OF ZERO MUST AWARD NOTHING. `got >= 0 * 0.75` is TRUE, so a stage that offered nothing -
a debug jump, an empty fixture - would hand out a free award on any score at all, including none.
That arm is driven deliberately.
"""
import os, sys, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

def main():
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof achievementStageComplete==='function' && typeof stageScoreOffer==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} achievementReload(); }")
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; run.mode='arcade'; run.lives=9; }" % sh.STEP)

        ok(pg.evaluate("() => STAGE_SCORE_SHARE===0.75"), "the bar is Mike's 75%")
        ok(pg.evaluate("() => !!ACHIEVEMENT_DEFS.stage_score_1 && ACHIEVEMENT_DEFS.stage_score_1.family==='stage_score' && ACHIEVEMENT_DEFS.stage_score_1.stage===1"),
           'and every stage has a THOROUGH row, carrying its own stage number')
        ok(pg.evaluate("() => [1,2,3,4,5,6,7,8,9].every(n=>!!ACHIEVEMENT_DEFS['stage_score_'+n])"), 'all nine of them')

        # the ceiling rises as a REAL stage runs
        pg.evaluate("() => { beginStage(1); }")
        pg.wait_for_timeout(900)
        pg.evaluate("() => { setState(GS.PLAY); for(let i=0;i<900;i++) window.__step(1); }")
        pg.wait_for_timeout(600)
        pg.evaluate("() => { for(let i=0;i<900;i++) window.__step(1); }")
        C = pg.evaluate("() => ({max:stageStats.scoreMax|0, spawned:stageStats.spawned|0, seen:stageStats.pickupsSeen|0, pick:PICKUP_SCORE})")
        print('  ceiling after ~30s of stage 1:', json.dumps(C))
        ok(C['spawned'] > 0, 'the stage spawned units (%d)' % C['spawned'])
        ok(C['max'] > 0, 'and the ceiling rose with them, measured from the stage itself (%d)' % C['max'])
        ok(C['max'] >= C['seen'] * C['pick'], 'every pickup that appeared is in it too (%d seen x %d)' % (C['seen'], C['pick']))

        # the bar itself, driven through the real grant
        R = pg.evaluate("""() => {
          const out={};
          achievementState=achievementEmpty();
          stageStats.scoreMax=10000; stageStats.scoreStart=0; run.score=7400;
          out.under=achievementStageComplete(1, stageStats, null).indexOf('stage_score_1')>=0;
          achievementState=achievementEmpty();
          run.score=7500;
          out.exact=achievementStageComplete(1, stageStats, null).indexOf('stage_score_1')>=0;
          achievementState=achievementEmpty();
          run.score=9900;
          out.over=achievementStageComplete(1, stageStats, null).indexOf('stage_score_1')>=0;
          /* THIS level's own score, not the run's: a fat score carried in must not buy the next stage */
          achievementState=achievementEmpty();
          stageStats.scoreStart=120000; run.score=120000+3000;
          out.carried=achievementStageComplete(2, stageStats, null).indexOf('stage_score_2')>=0;
          /* a stage that offered nothing awards nothing - 0 >= 0*0.75 is TRUE */
          achievementState=achievementEmpty();
          stageStats.scoreMax=0; stageStats.scoreStart=0; run.score=0;
          out.empty=achievementStageComplete(3, stageStats, null).indexOf('stage_score_3')>=0;
          achievementState=achievementEmpty();
          return out; }""")
        print('  bar:', json.dumps(R))
        ok(R['under'] is False, '74% of the ceiling does NOT earn it')
        ok(R['exact'] is True, 'exactly 75% does')
        ok(R['over'] is True, 'and 99% does')
        ok(R['carried'] is False, "a score carried in from an earlier level cannot buy this one (3,000 of a 10,000 ceiling)")
        ok(R['empty'] is False, 'a stage that offered nothing awards nothing - a zero ceiling is not a free pass')

        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} achievementReload(); }")
        print('  errors:', len(errs))
        for e in errs[:5]: print('   !', e[:180])
        ok(len(errs) == 0, 'no page or console errors (%d)' % len(errs))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
