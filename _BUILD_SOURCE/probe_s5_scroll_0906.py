#!/usr/bin/env python3
"""probe_s5_scroll_0906.py - does stage 5's space ever STOP moving?

Mike, 0906: "its bad. DO NOT STOP SCROLLING THE level or speed, when the ship is about to become
a spaceship is when the stage tiles up to the spacebackground and we convert to it as were
scrolling in space."

Three separate things used to stop it, and a probe that only checks one would pass on a build that
still fails the other two:

  1. `_bossHold` freezes `mapScroll` for a boss or miniboss.
  2. `mapScroll = Math.min(range, ...)` CAPS at the plate end, so a LOOPING master stops for good.
  3. the launch brake eases to a standstill just before the gravity conversion.

So this drives a real stage 5 and samples the window the master was actually DRAWN at, across an
ordinary run, a forced miniboss and a forced boss.

⚠ IT READS `_masterSrcY`, NOT THE CLOCK. `_loopDraw` publishes the source row it blitted from.
Reading `_stage5SpaceScroll` back would be asking my own new variable whether it incremented -
CLAUDE.md's "a probe that recomputes the thing under test cannot find the bug", exactly. The
question is whether the PICTURE moved.

⚠ AND IT COMPARES AGAINST STAGE 6, WHICH IS KNOWN-GOOD. A number is not evidence on its own; stage
6 already satisfies this requirement (drop 0904t), so it is the control. A run where both stages
read "never stops" and a run where both read "stops" are distinguishable only because of it.
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot as sh
from playwright.sync_api import sync_playwright

WARM = """() => { const w=[]; const cfg=(typeof _levelCfg==='function')?_levelCfg():null;
  if(cfg&&cfg.master) w.push(cfg.master); if(cfg&&cfg.par) w.push(cfg.par);
  window.__w=w; for(const k of w){try{XART._touch(k);}catch(e){}} return w.length; }"""
READY = """() => { const ks=window.__w||[]; let n=0; for(const k of ks) if(XART.rdy(k)) n++;
  return ks.length?n/ks.length:1; }"""

SAMPLE = """() => ({ src:(typeof _masterSrcY!=='undefined')?_masterSrcY:null,
                     map:(typeof mapScroll!=='undefined')?mapScroll:null,
                     sb:(typeof subBossActive!=='undefined'&&subBossActive),
                     bs:(typeof bossActive!=='undefined'&&bossActive) })"""

FORCE_SUB = """() => { try{ spawnSubBoss(SUBBOSS[run.stage].kind); return !!subBoss; }catch(e){ return String(e); } }"""
FORCE_BOSS = """() => { try{ spawnBoss(); return !!boss; }catch(e){ return String(e); } }"""


def run_stage(pg, stage, label):
    r = pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': stage, 'pilot': 'cole', 'invuln': True})
    if not r.get('ok'):
        return {'err': 'setup failed: %s' % r}
    pg.evaluate(WARM)
    try:
        pg.wait_for_function('(' + READY + ')() >= 0.99', timeout=20000)
    except Exception:
        pass
    pg.evaluate(sh.TRAP_RAF)

    out = {}
    for phase, forcer in (('ordinary play', None), ('miniboss engaged', FORCE_SUB), ('boss engaged', FORCE_BOSS)):
        if forcer:
            pg.evaluate(forcer)
            pg.evaluate(sh.STEP, 30)
            pg.wait_for_timeout(25)
        seen, stalls, moved = [], 0, 0
        prev = None
        for _ in range(40):
            pg.evaluate(sh.STEP, 12)          # ~0.2s of game time per sample
            pg.wait_for_timeout(8)
            s = pg.evaluate(SAMPLE)
            v = s['src']
            if v is None:
                continue
            if prev is not None:
                # the loop wraps, so a big negative jump is a wrap, not a stall
                d = v - prev
                if abs(d) < 0.01:
                    stalls += 1
                else:
                    moved += 1
            prev = v
            seen.append(round(v, 1))
        out[phase] = {'stalls': stalls, 'moved': moved, 'first': seen[:3], 'last': seen[-3:]}
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--stages', default='5,6')
    a = ap.parse_args()
    port, stop = sh.serve(sh.GAME)
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={'width': 480, 'height': 512})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto('http://127.0.0.1:%d/index.html' % port)
            pg.wait_for_function('typeof ASSETS!=="undefined" && typeof loop==="function"', timeout=30000)
            pg.wait_for_timeout(2500)
            res = {}
            for s in [int(x) for x in a.stages.split(',')]:
                res[s] = run_stage(pg, s, 'stage %d' % s)
            b.close()
    finally:
        stop()

    bad = []
    for s in sorted(res):
        print('\n--- STAGE %d %s' % (s, '(the control - known good since 0904t)' if s == 6 else ''))
        r = res[s]
        if 'err' in r:
            print('  %s' % r['err']); bad.append('stage %d: %s' % (s, r['err'])); continue
        for phase, d in r.items():
            verdict = 'MOVING' if d['stalls'] == 0 else ('** STALLED %d/%d samples **' % (d['stalls'], d['stalls'] + d['moved']))
            print('  %-18s %-28s src %s ... %s' % (phase, verdict, d['first'], d['last']))
            if d['stalls'] > 0:
                bad.append('stage %d / %s: %d stalled samples' % (s, phase, d['stalls']))
    if errs:
        print('\n** %d page errors, first: %s' % (len(errs), errs[0][:180]))
    print('\n%s' % ('FAILED:\n  ' + '\n  '.join(bad) if bad
                    else 'stage 5 never stops scrolling, in play, at the miniboss or at the boss.'))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
