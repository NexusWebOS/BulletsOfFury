#!/usr/bin/env python3
"""probe_easy_finale_1101.py - Easy ends at Stage 5 like Normal (normal_finale_1031.js, 1101 change).
Real Chromium. Checks:
  EASY  : beginStage(6/7/8) opens the finale instead of the stage; the Stage-5 clear opens the EASY COMPLETE flight/menu
          and saves diff 'easy'; the menu offers NORMAL / HARD / FURIOUS; NORMAL's text names normal health/fire and
          Stages 1-5; choosing NORMAL starts Stage 1 on real Normal tuning (DIFF eHp/eFire/ebSpeed == DIFFS.normal and a
          spawned enemy gets the same HP as a fresh Normal run), and that Normal run is still blocked at Stage 6.
  NORMAL: still blocked at 6-8, menu offers HARD / FURIOUS only.
  HARD  : Stage 6 starts normally (not blocked).
  --bust: nf100Ends reverted to Normal-only at runtime -> the Easy checks must fail.
Screenshots: _shots/easy_finale_1101/.
"""
import os, sys, base64, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'easy_finale_1101')

PREP = r"""(cfg) => { ASSETS.ready = true; window.__now = performance.now();
  if (cfg.bust) nf100Ends = function (k) { return (k === undefined ? diffKey : k) === 'normal'; };
  try { localStorage.removeItem(NF100.key); } catch (e) {}
  return typeof nf100Ends === 'function'; }"""

# start a campaign run on a difficulty and try to enter a stage
ENTER = r"""(c) => { diffKey = c.diff; DIFF = difficultyForRun('campaign', c.diff); run.mode = 'campaign'; coopOn = false;
  startRun(c.stage); curStage = STAGES[c.stage - 1]; NF100.current = null;
  let err = null; try { beginStage(c.stage); } catch (e) { err = String(e).slice(0, 160); }
  const A = NF100.current;
  return {state: String(state), finale: state === NF100.state, from: A && A.from, opts: A ? nf100Options(A).map(o => o.key) : null,
          stageTimer, err}; }"""

STEP = r"""(n) => { for (let i = 0; i < n; i++) { window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0, 160); } } return {state: String(state), phase: NF100.current && NF100.current.phase, err: window.__err || null}; }"""

# the real Stage-5 clear: scLeaveStage on stage 5 for this difficulty
CLEAR5 = r"""(c) => { diffKey = c.diff; DIFF = difficultyForRun('campaign', c.diff); run.mode = 'campaign'; coopOn = false;
  startRun(5); curStage = STAGES[4]; run.stage = 5; NF100.current = null;
  let err = null; try { scLeaveStage({bonus: 1000, rank: 'A'}); } catch (e) { err = String(e).slice(0, 160); }
  let saved = null; try { saved = JSON.parse(localStorage.getItem(NF100.key) || 'null'); } catch (e) {}
  const A = NF100.current;
  return {state: String(state), finale: state === NF100.state, phase: A && A.phase, from: A && A.from, err,
          savedDiff: saved && saved.diff, savedStage: saved && saved.stage, metaDiff: saved && saved.normalComplete100 && saved.normalComplete100.diff,
          label: campAutoLabel()}; }"""

MENU = r"""(sel) => { const A = NF100.current; A.phase = 'menu'; A.t = 1; A.sel = sel; const O = nf100Options(A);
  return {opts: O.map(o => o.key), labels: O.map(o => o.label), detail: O[sel].detail}; }"""

CHOOSE = r"""(i) => { const ok = nf100Choose(i); return {ok, chosen: NF100.current && NF100.current.chosen}; }"""

AFTER = r"""() => { const N = DIFFS.normal;
  return {state: String(state), pilot: state === GS.PILOT, diffKey, stage: run.stage, ngplus: !!run.ngplus,
          eHp: DIFF.eHp, eFire: DIFF.eFire, ebSpeed: DIFF.ebSpeed, nHp: N.eHp, nFire: N.eFire, nSpeed: N.ebSpeed}; }"""

# HP of the same regular enemy spawned in Stage 1 under the current difficulty
HP = r"""(diff) => { if (diff) { diffKey = diff; DIFF = difficultyForRun('campaign', diff); }
  run.mode = 'campaign'; startRun(1); curStage = STAGES[0]; beginStage(1); setState(GS.PLAY); stagePlan = [];
  enemies.length = 0; spawnEnemy('drone', 200, 100, {}); const e = enemies[enemies.length - 1];
  return {diffKey, hp: e ? e.hp : null, type: e ? e.type : null}; }"""

def shot(pg, name):
    d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
    open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

def main():
    bust = '--bust' in sys.argv
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    res, errs = [], []
    def check(name, ok, info=''):
        res.append(ok); print(('ok   ' if ok else 'FAIL ') + name + ('   ' + str(info) if info else ''), flush=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        pg.evaluate(PREP, {'bust': bust})

        for st in (6, 7, 8):
            r = pg.evaluate(ENTER, {'diff': 'easy', 'stage': st})
            check('EASY stage %d is blocked and opens the finale' % st, r['finale'] and r['from'] == 'easy', r)
        r = pg.evaluate(ENTER, {'diff': 'easy', 'stage': 6})
        check('EASY finale offers NORMAL / HARD / FURIOUS', r['opts'] == ['normal', 'hard', 'furious'], r['opts'])
        r = pg.evaluate(ENTER, {'diff': 'easy', 'stage': 9})
        check('EASY Stage 9 bonus detour is still allowed', not r['finale'], r['state'])
        for st in (6, 8):
            r = pg.evaluate(ENTER, {'diff': 'normal', 'stage': st})
            check('NORMAL stage %d is still blocked' % st, r['finale'] and r['from'] == 'normal', r['state'])
        check('NORMAL finale offers HARD / FURIOUS only', r['opts'] == ['hard', 'furious'], r['opts'])
        r = pg.evaluate(ENTER, {'diff': 'hard', 'stage': 6})
        check('HARD stage 6 starts (not blocked)', not r['finale'] and not r['err'], r)

        # the real Stage-5 clear on Easy
        r = pg.evaluate(CLEAR5, {'diff': 'easy'})
        check('EASY Stage-5 clear opens the return flight', r['finale'] and r['phase'] == 'flight' and r['from'] == 'easy', r)
        check('EASY clear is saved as an Easy completion at Stage 5', r['savedDiff'] == 'easy' and r['savedStage'] == 5 and r['metaDiff'] == 'easy', r)
        check('auto-save label reads EASY COMPLETE', r['label'] == 'AUTO  EASY COMPLETE', r['label'])
        pg.evaluate(STEP, 100); shot(pg, 'easy-flight.png')
        for i, nm in enumerate(['normal', 'hard', 'furious']):
            m = pg.evaluate(MENU, i); pg.evaluate(STEP, 2); shot(pg, 'easy-menu-%s.png' % nm)
        m = pg.evaluate(MENU, 0)
        d = m['detail']
        check('NORMAL option text names normal health and firing speed', 'NORMAL HEALTH AND FIRING SPEED' in d, d)
        check('NORMAL option text says Stages 1-5 only', 'STAGES 1-5 ONLY' in d, d)
        c = pg.evaluate(CHOOSE, 0)
        check('choosing NORMAL commits normal', c['ok'] and c['chosen'] == 'normal', c)
        pg.evaluate(STEP, 60)
        a = pg.evaluate(AFTER)
        check('fade lands on pilot select for a fresh Stage 1 Normal run', a['pilot'] and a['diffKey'] == 'normal' and a['stage'] == 1 and not a['ngplus'], a)
        check('that run uses Normal enemy health / fire / bullet speed', a['eHp'] == a['nHp'] and a['eFire'] == a['nFire'] and a['ebSpeed'] == a['nSpeed'], a)
        hpN = pg.evaluate(HP, None)
        hpRef = pg.evaluate(HP, 'normal'); hpE = pg.evaluate(HP, 'easy')
        check('a Stage-1 enemy has the same HP as a fresh Normal run (and more than Easy)', hpN['hp'] == hpRef['hp'] and hpRef['hp'] > hpE['hp'], (hpN, hpRef, hpE))
        r = pg.evaluate(ENTER, {'diff': 'normal', 'stage': 6})
        check('the Normal run chosen from Easy is still blocked at Stage 6', r['finale'], r['state'])
        pg.evaluate(MENU, 0); pg.evaluate(STEP, 2); shot(pg, 'normal-menu.png')
        check('no page/console errors', not errs, errs[:4])
        b.close()
    stop()
    passed = sum(res); print('%d/%d passed%s' % (passed, len(res), ' (BUST arm)' if bust else ''))
    sys.exit(0 if passed == len(res) else 1)

if __name__ == '__main__':
    main()
