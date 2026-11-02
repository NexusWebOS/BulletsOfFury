#!/usr/bin/env python3
"""probe_current_breaker_guard_1102.py - CBG (assets/current_breaker_guard_1102.js) checks in real Chromium, N/H/F.
Current Breaker spawned alone on Stage 9 (stage clock held, plan empty, protected pilot), TRAP_RAF stepping.
 - HP is CBG_HP x the CB112/native value (window.CBG_OFF=1 spawn gives the baseline)
 - liquid phases (orb entry, transformation) absorb the real fire key: HP unchanged, no damage flash, splashes drawn
 - humanoid phases take damage and flash
 - depth phases leave spaceTargets/_lockTargets and take no damage from held fire; a missile-reflected roller still
   lands its native counter damage
 - every tidal shove and every depth roller is preceded by a lane (combatWarningDraw from this owner within 1.6 s)
 - a kill in a humanoid phase runs the native death (_dyingT) and removes him; no page errors
  python _BUILD_SOURCE/probe_current_breaker_guard_1102.py [--diffs normal,hard,furious]
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
A = sys.argv
DIFFS = (A[A.index('--diffs') + 1] if '--diffs' in A else 'normal,hard,furious').split(',')
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'cb_inspect_1102')
SETUP = r"""(d) => { ASSETS.ready = true; diffKey = d; DIFF = DIFFS[d]; run.mode = 'arcade'; coopOn = false;
  startRun(9); curStage = STAGES[8]; beginStage(9); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {} for (const k of ['story','fb2Talk','fb2Intro','s6Opening']) { try { window.eval(k + '=null'); } catch (e) {} }
  playerHit = function(){}; stagePlan = []; window.__now = performance.now(); window.__F = 0;
  if (!window.__hooked) { window.__hooked = true; const W = window;
    const CW = combatWarningDraw; combatWarningDraw = function (e, o) { if (W.__cb && e === W.__cb && o && Number.isFinite(o.ex)) W.__W.push({f: W.__F, ph: e._cb112 && e._cb112.phase}); return CW.apply(this, arguments); };
    const T = eShootT; eShootT = function (x, y, a, s, k, opt) { const b = T.apply(this, arguments); const o = (opt && opt.owner) || ai27Context;
      if (W.__cb && (o === W.__cb || (b && b._s911Owner === W.__cb)) && b && !b.dead) W.__R.push({f: W.__F, ph: W.__cb._cb112 && W.__cb._cb112.phase, roller: !!b._cb112Roller, wave: !!b._cb112Wave}); return b; }; }
  return true; }"""
SPAWN = r"""(off) => { window.CBG_OFF = off ? 1 : 0; for (const e of enemies) e.dead = true; enemies.length = 0; eBullets.length = 0; stagePlan = []; stageTimer = 2;
  player.x = (worldWidth() > viewW() ? camX : 0) + VW / 2; player.y = VH - 90; const n = enemies.length; window.__W = []; window.__R = []; window.__F = 0;
  spawnEnemy('cbreak', worldWidth() * .72, -124, {}); const e = window.__cb = enemies.slice(n).find(e => e.type === 'cbreak');
  BOF_CURRENT_BREAKER_GUARD_1102.state.absorbed = 0; return {hp: e.hp, maxhp: e.maxhp}; }"""
STEP = r"""(c) => { const W = window, e = W.__cb; let maxFlash = 0, hp0 = e.hp, fx = 0;
  for (let i = 0; i < c.n; i++) { stageTimer = 2; W.__F++; W.__now += 1000/60;
    Input.keys.j = !!c.fire; if (c.fire && !e.dead) player.x += (e.x - player.x) * .08;
    try { loop(W.__now); } catch (er) { W.__err = String(er).slice(0, 160); }
    maxFlash = Math.max(maxFlash, e.flash || 0); fx = Math.max(fx, BOF_CURRENT_BREAKER_1102.state.fx.length);
    if (c.until && e._cb112 && e._cb112.phase === c.until) break; if (e.dead) break; }
  Input.keys.j = false; const q = e._cb112;
  return {phase: q ? q.phase : null, hp: e.hp, hp0, maxFlash, fx, dead: !!e.dead, dying: e._dyingT ?? null, absorbed: BOF_CURRENT_BREAKER_GUARD_1102.state.absorbed,
    inTargets: spaceTargets().includes(e), inLocks: _lockTargets().includes(e), err: W.__err || null}; }"""

checks = []
def check(name, ok, info=''):
    checks.append({'name': name, 'ok': bool(ok), 'info': str(info)[:200]}); print('%s %s  %s' % ('PASS' if ok else 'FAIL', name, info), flush=True)

def main():
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME); errs = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio']); pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        for D in DIFFS:
            pg.evaluate(SETUP, D)
            for i in range(200):
                if pg.evaluate("() => { try { stageLoadTick(); return stageLoadReady(9); } catch (e) { return true; } }"): break
                pg.wait_for_timeout(100)
            base = pg.evaluate(SPAWN, True); g = pg.evaluate(SPAWN, False)
            check('%s HP x4 of the CB112 value' % D, abs(g['hp'] - 4 * base['hp']) <= 4 and g['maxhp'] == g['hp'], (base['hp'], g['hp'], g['maxhp']))
            # liquid: fire through entry + transformation
            r = pg.evaluate(STEP, {'n': 600, 'fire': True, 'until': 'grenade-charge'})
            check('%s liquid entry/transform absorbs held fire' % D, r['phase'] == 'grenade-charge' and r['hp'] == g['hp'] and r['absorbed'] > 20, r)
            check('%s absorbed hits show water splashes, no damage flash' % D, r['fx'] > 0 and r['maxFlash'] == 0, (r['fx'], r['maxFlash']))
            r = pg.evaluate(STEP, {'n': 90, 'fire': True})
            check('%s humanoid takes damage and flashes' % D, r['hp'] < r['hp0'] and r['maxFlash'] > 0.05, (r['phase'], r['hp0'], r['hp'], r['maxFlash']))
            # passive through to depth-spin, keep him alive
            pg.evaluate("() => { window.__cb.hp = window.__cb.maxhp; }")
            r = pg.evaluate(STEP, {'n': 3000, 'fire': False, 'until': 'depth-spin'})
            pg.evaluate(STEP, {'n': 20, 'fire': False})
            r = pg.evaluate(STEP, {'n': 1, 'fire': False})
            check('%s depth: out of collision and lock lists' % D, r['phase'] == 'depth-spin' and not r['inTargets'] and not r['inLocks'], r)
            r = pg.evaluate(STEP, {'n': 120, 'fire': True})
            check('%s depth: held fire does no damage' % D, r['phase'] in ('depth-spin', 'depth-linger') and r['hp'] == r['hp0'], (r['phase'], r['hp0'], r['hp']))
            for k in range(40):
                if pg.evaluate("() => BOF_CURRENT_BREAKER_1102.state.balls.some(F => !F.done && !F.returning && F.q && !F.q.dead && F.e === window.__cb)"): break
                pg.evaluate(STEP, {'n': 3, 'fire': False})
            c = pg.evaluate("""() => { const S = BOF_CURRENT_BREAKER_1102.state, F = S.balls.find(F => !F.done && !F.returning && F.q && !F.q.dead && F.e === window.__cb);
              if (!F) return {ok: false}; const hp = window.__cb.hp; BOF_CURRENT_BREAKER_1102.weapon(F, {kind: 'gmiss', seat: 1, x: F.q.x, y: F.q.y}); return {ok: true, hp}; }""")
            r = pg.evaluate(STEP, {'n': 60, 'fire': False})
            check('%s depth: reflected roller still lands its counter damage' % D, c.get('ok') and c['hp'] - r['hp'] >= 20, (c, r['hp']))
            # warnings: run the rest of the cycle passively, then judge every tidal / roller round
            r = pg.evaluate(STEP, {'n': 1500, 'fire': False, 'until': 'retreat'})
            W = pg.evaluate("() => window.__W"); R = pg.evaluate("() => window.__R")
            for kind, sel in (('tidal shove', lambda x: x['ph'] == 'tidal'), ('depth roller', lambda x: x['ph'] == 'depth-spin')):
                rs = [x for x in R if sel(x)]; warned = [x for x in rs if any(x['f'] - 96 <= w['f'] <= x['f'] for w in W)]
                check('%s every %s preceded by a lane' % (D, kind), rs and len(warned) == len(rs), '%d/%d' % (len(warned), len(rs)))
            # death in a humanoid phase
            pg.evaluate(SPAWN, False); pg.evaluate(STEP, {'n': 900, 'fire': False, 'until': 'grenades'})
            pg.evaluate("() => { const e = window.__cb; e.hp = 3; }")
            r = pg.evaluate(STEP, {'n': 240, 'fire': True})
            check('%s kill runs native death and removes him' % D, r['dead'], (r['phase'], r['hp'], r['dying']))
            pg.screenshot(path=os.path.join(OUT, 'guard_%s_end.png' % D))
        check('no page errors', not errs and not pg.evaluate("() => window.__err || null"), errs[:3])
        b.close()
    stop()
    os.makedirs(OUT, exist_ok=True); json.dump(checks, open(os.path.join(OUT, 'guard_checks.json'), 'w'), indent=1)
    print('%d/%d' % (sum(c['ok'] for c in checks), len(checks)))

if __name__ == '__main__':
    main()
