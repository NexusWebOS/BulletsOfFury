#!/usr/bin/env python3
"""probe_stage8_plan_1101.py - why did 30 s of Stage 8 show no regular enemies? Dumps stagePlan after beginStage(8),
then steps the real loop and logs every spawnEnemy call (type, x, y) and what each produced (type, dead?, culled?)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
STAGE = int(sys.argv[1]) if len(sys.argv) > 1 else 8

JS = r"""(st) => { ASSETS.ready = true; diffKey = 'hard'; DIFF = DIFFS.hard; run.mode = 'arcade'; coopOn = false;
  startRun(st); curStage = STAGES[st - 1]; beginStage(st); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {}
  for (const k of ['story','fb2Talk','fb2Intro','s6Opening']) { try { window.eval(k + '=null'); } catch (e) {} }
  playerHit = function(){};
  const W = window; W.__log = [];
  const plan = (stagePlan || []).map(p => ({t: p.t != null ? p.t : p.time, done: !!p.done, fn: String(p.fn || p.f || p.cb || '').slice(0, 90)}));
  const S = spawnEnemy; spawnEnemy = function (type, x, y) { const n = enemies.length; let r; try { r = S.apply(this, arguments); } finally {
      const made = enemies.slice(n).map(e => ({type: e.type, dead: !!e.dead, x: Math.round(e.x), y: Math.round(e.y)}));
      W.__log.push({t: +(stageTimer || 0).toFixed(2), type, x: Math.round(x), y: Math.round(y), made, ret: r ? (r.type || typeof r) : null}); } return r; };
  return {planLen: plan.length, plan: plan.slice(0, 40), keys: stagePlan[0] ? Object.keys(stagePlan[0]) : [], lenS: curStage.length}; }"""

STEP = r"""(n) => { window.__now = window.__now || performance.now(); for (let i = 0; i < n; i++) { window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e); } }
  return {t: +(stageTimer || 0).toFixed(1), n: enemies.length, live: enemies.filter(e => !e.dead).map(e => e.type + '@' + Math.round(e.x) + ',' + Math.round(e.y)).slice(0, 30),
    plan: (stagePlan || []).filter(p => !p.done && !p.fired).length, state, sub: !!subBossActive, err: window.__err || null,
    flags: {story: typeof story !== 'undefined' && !!story, paused: typeof paused !== 'undefined' && paused, wave: typeof waveHold !== 'undefined' ? waveHold : 'n/a'}}; }"""

def main():
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        info = pg.evaluate(JS, STAGE)
        print('plan', info['planLen'], 'entry keys', info['keys'], 'stage length', info['lenS'])
        for x in info['plan'][:12]: print('  ', x)
        for s in range(19):
            r = pg.evaluate(STEP, 120); pg.wait_for_timeout(40)
            print('t=%s n=%s plan-left=%s sub=%s %s live=%s err=%s' % (r['t'], r['n'], r['plan'], r['sub'], r['flags'], r['live'], r['err']))
        L = pg.evaluate("() => window.__log")
        print('spawnEnemy calls:', len(L))
        for x in L[:40]: print('  ', x)
        print('page errors', errs[:5])
        b.close()
    stop()

if __name__ == '__main__':
    main()
