#!/usr/bin/env python3
"""
probe_infusion_rate_0917.py - WHY THE SECOND PLAYTEST SWEEP DREW ZERO INFUSIONS.

The sweep's `drops > 0` gate is a coin flip, not a proof: at INFUSION_DROP_P 0.14 behind the 18%
kill-drop gate on HARD (dropMul 0.95) an eligible kill pays a pickup about once in 44, and the
sweep's eligible stages scored 129 kills - expected 2.9. Zero is a 5% night, not a bug.

This probe replaces the coin flip with a measurement: per stage it reads what `infusionEligible()`
actually decides and then drives 4,000 real `dropPowerup` calls and counts the pickups.
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
    rows = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof infusionEligible==='function' && typeof dropPowerup==='function'", timeout=60000)
        # ⚠ READ THE CONSTANT, NEVER HARDCODE IT (0917): a hardcoded 0.14 here failed every eligible
        # stage the moment the roll moved to killDrop and the constant became a per-eligible-kill rate.
        P_LIVE = pg.evaluate("() => (typeof INFUSION_DROP_P!=='undefined') ? INFUSION_DROP_P : 0.14")
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        for stage in range(1, 10):
            pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': stage, 'pilot': 'cole'})
            pg.evaluate("() => { diffKey='hard'; DIFF=difficultyForRun(run.mode,'hard'); }")
            pg.evaluate(sh.STEP, [8])
            rows[stage] = pg.evaluate("""() => {
              const n0 = powerups.length;
              for (let i=0;i<4000;i++) dropPowerup(100, 100);
              const inf = powerups.slice(n0).filter(p=>p.kind==='infuse').length;
              powerups.length = n0;
              return { bg: curStage?curStage.bg:null, space: !!spaceWeaponsActive(),
                       elig: !!infusionEligible(), dropMul: DIFF.dropMul, inf: inf,
                       bias: (typeof INFUSION_STAGE_BIAS!=='undefined') ? (INFUSION_STAGE_BIAS[run.stage]||null) : null };
            }""")
        br.close()
    stop()
    print(json.dumps(rows, indent=2))
    qa = {
        'drop': '0917 infusion drop rate, per stage',
        'request': 'the playtest sweep drew 0 infusions; is the roll wrong, the gate wrong, or the night unlucky?',
        'method': '4,000 real dropPowerup calls per stage in Chromium, HARD, after SETUP entered the stage',
        'expected_per_4000': P_LIVE * 0.95 * 4000,
        'stages': rows,
    }
    qp = os.path.join(ROOT, 'docs', 'qa', 'infusion_rate_0917.json')
    json.dump(qa, open(qp, 'w'), indent=2)
    print('wrote ' + qp)
    exp = P_LIVE * 0.95 * 4000    # ⚠ the LIVE constant - a hardcoded 0.14 failed all seven eligible
                                  # stages the moment killDrop took the roll and the rate became per-kill
    for st, r in rows.items():
        if st in (5, 9):
            ok(not r['elig'] and r['inf'] == 0, 'stage %d (space weapons): CONTROL - ineligible, %d/4000 pickups' % (st, r['inf']))
        else:
            ok(r['elig'], 'stage %d (bg %s): infusions are ELIGIBLE' % (st, r['bg']))
            ok(abs(r['inf'] - exp) < exp * 0.25, 'stage %d: %d/4000 pickups, expected ~%d (INFUSION_DROP_P x dropMul)' % (st, r['inf'], exp))
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL ' + f)
    return 1 if FAILS else 0
if __name__ == '__main__':
    sys.exit(main())
