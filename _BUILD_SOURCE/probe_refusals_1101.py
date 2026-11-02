#!/usr/bin/env python3
"""probe_refusals_1101.py - are enemy rounds silently refused? (the Stage-7 twin-gun bug, generalised)
Each type is spawned alone on its stage with the plan's own spawnEnemy call (stage clock held, plan empty) and the
OUTERMOST eShootT/eShoot is wrapped: every request is logged with its owner, the frame, and whether the returned round
is dead (refused by some layer). Reports per type: requests, refused, frames with 2+ requests (volleys), largest volley,
refused-in-volley. Also checks the owner's own event log for beam/laser releases (not eBullets).
  python _BUILD_SOURCE/probe_refusals_1101.py --stage 5|6|8 [--diff furious] [--secs 12]
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
A = sys.argv
STAGE = int(A[A.index('--stage') + 1]); CASTKEY = STAGE; STAGE = 6 if STAGE in (66, 67) else 5 if STAGE == 55 else STAGE; DIFF = A[A.index('--diff') + 1] if '--diff' in A else 'furious'
SECS = int(A[A.index('--secs') + 1]) if '--secs' in A else 12
CAST = {
 5: [('s5frigate', .30, -90, {}), ('s5interceptor', .70, -80, {}), ('s5rammer', .50, -90, {}), ('s5skimmer', 'L', .18, {'_side': 1}),
     ('s5gravity', .50, -100, {}), ('s5minelayer', .28, -100, {}), ('s5satellite', .72, -90, {}), ('s5portalmine', .32, -80, {}),
     ('s5repair', .50, -88, {}), ('s5station', .50, -110, {}), ('s5leech', .26, -85, {})],
 55: [('s5skimmer', 'L', .18, {'_side': 1})],
 67: [('s6dart', .22, -64, {'_jetManeuver': 'dash'}), ('l6v_r1', .30, -90, {}), ('s6thunder', .30, -76, {})],
 66: [('xelite_solarwarden', .70, -70, {}), ('s1jetbomber_b', .5, -80, {})],
 6: [('s6dart', .22, -64, {'_jetManeuver': 'dash'}), ('s6mine', .50, -74, {}), ('s6lancer', .28, -74, {}), ('s6skimmer', 'L', .25, {'_side': 1, '_jetManeuver': 'bomb'}),
     ('s6thunder', .30, -76, {}), ('s6probe', .50, -76, {}), ('s6cyclone', .27, -78, {'_side': 1}), ('s6bomber', 'L', .22, {'_side': 1, '_jetManeuver': 'bomb'}),
     ('s6turbine', .50, -96, {}), ('l6v_s0', .18, -70, {}), ('l6v_s1', .34, -84, {}), ('l6v_s2', .50, -80, {}), ('l6v_r0', .24, -72, {}), ('l6v_r1', .30, -90, {}),
     ('l6v_r2', .50, -86, {}), ('l6v_b0', .20, -76, {}), ('l6v_b1', .28, -96, {}), ('l6v_b2', .50, -92, {}),
     ('xelite_glacierlance', .50, -72, {}), ('xelite_tempest', .30, -70, {}), ('xelite_solarwarden', .70, -70, {}), ('s1jetbomber_b', .5, -80, {})],
 8: [('s8interceptor', .27, -100, {}), ('s8needlejet', .50, -105, {}), ('s8scout', .32, -96, {}), ('s8manta', .50, -130, {}),
     ('s8deathorb', .50, -135, {}), ('s8parasite', .30, -105, {}), ('s8crescent', .50, -118, {}), ('s8hunter', .28, -105, {}),
     ('s8skull', .32, -95, {}), ('s8tentacle', .50, -145, {}), ('s8symbiote', .22, -100, {}), ('s8carrier', .50, -180, {}),
     ('s8gunship', .50, -165, {}), ('s8bomber', .28, -150, {}), ('s8voidjet', .50, -170, {}), ('s8laserharrier', .5, -110, {}), ('s8hellwing', .5, -110, {})],
}
SETUP = r"""(c) => { ASSETS.ready = true; diffKey = c.d; DIFF = DIFFS[c.d]; run.mode = 'arcade'; coopOn = false;
  startRun(c.s); curStage = STAGES[c.s - 1]; beginStage(c.s); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {} for (const k of ['story','fb2Talk','fb2Intro','s6Opening']) { try { window.eval(k + '=null'); } catch (e) {} }
  playerHit = function(){}; stagePlan = []; window.__now = performance.now(); window.__F = 0;
  const own = (o) => { o = o || ai27Context; return o && o.type ? o : null; };
  const T = eShootT; eShootT = function (x, y, a, s, k, opt) { const o = own(opt && opt.owner), b = T.apply(this, arguments);
    if (window.__R && o && window.__U.has(o)) window.__R.push({f: window.__F, kind: k, dead: !b || !!b.dead, held: !!(b && b._ai27Held), literal: !!(b && b.dead && b.kind === undefined), air17: !!(typeof AIR17 !== 'undefined' && AIR17.owner), j3: !!(typeof J3 !== 'undefined' && J3.dialogueLive), keys: b ? Object.keys(b).slice(0, 12).join(',') : 'null', stack: b && b.dead ? (new Error().stack || '').split(String.fromCharCode(10)).slice(2, 6).map(l => l.trim().slice(0, 90)).join(' | ') : ''}); return b; };
  const P = eShoot; eShoot = function () { const o = own(null), n = eBullets.length, r = P.apply(this, arguments);
    if (window.__R && o && window.__U.has(o)) window.__R.push({f: window.__F, kind: 'eShoot', dead: eBullets.length === n, plain: true}); return r; };
  return true; }"""
SPAWN = r"""(c) => { for (const e of enemies) e.dead = true; enemies.length = 0; eBullets.length = 0; stagePlan = []; stageTimer = 2;
  try { boss = null; bossActive = false; subBoss = null; subBossActive = false; } catch (e) {}
  for (const k of ['S511','S611','S811','CC111','CA111']) { try { const o = window.eval(k); if (o && Array.isArray(o.events)) o.events.length = 0; } catch (e) {} }
  player.x = (worldWidth() > viewW() ? camX : 0) + VW / 2; player.y = VH - 90; window.__R = [];
  const ww = worldWidth(), x = c.x === 'L' ? -90 : ww * c.x, y = c.x === 'L' ? VH * c.y : c.y, n = enemies.length;
  try { spawnEnemy(c.type, x, y, c.opts || {}); } catch (e) { return {err: String(e).slice(0, 160)}; }
  const mine = enemies.slice(n); window.__U = new Set(mine);
  return {types: mine.map(e => e.type), hp: mine.map(e => Math.round(e.hp))}; }"""
STEP = r"""(n) => { for (let i = 0; i < n; i++) { stageTimer = 2; window.__F++; window.__now += 1000/60;
    for (const e of enemies) if (window.__U && !window.__U.has(e) && e._parentOf === undefined && window.__U.size < 12 && [...window.__U].some(u => e._owner === u || e._parent === u || e._carrier === u)) window.__U.add(e);
    try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0, 160); } } return window.__err || null; }"""
EV = r"""() => { const out = {}; for (const k of ['S511','S611','S811','CC111','CA111']) { let o; try { o = window.eval(k); } catch (e) { continue; }
  if (o && Array.isArray(o.events)) for (const x of o.events) { const n = k + ':' + x.event; out[n] = (out[n] || 0) + 1; } } return out; }"""

def main():
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME); out = {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio']); pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60); pg.evaluate(SETUP, {'s': STAGE, 'd': DIFF})
        for i in range(200):
            if pg.evaluate("(s) => { try { stageLoadTick(); return stageLoadReady(s); } catch (e) { return true; } }", STAGE): break
            pg.wait_for_timeout(100)
        for typ, x, y, o in CAST[CASTKEY]:
            s = pg.evaluate(SPAWN, {'type': typ, 'x': x, 'y': y, 'opts': o})
            for k in range(SECS): pg.evaluate(STEP, 60); pg.wait_for_timeout(12)
            R = pg.evaluate("() => window.__R"); ev = pg.evaluate(EV)
            fr = {}
            for r in R: fr.setdefault(r['f'], []).append(r)
            vol = [v for v in fr.values() if len(v) >= 2]
            refused = sum(r['dead'] for r in R); rv = sum(r['dead'] for v in vol for r in v[1:])
            kinds = sorted(set(r['kind'] for r in R))
            beams = {k: v for k, v in ev.items() if any(w in k for w in ('beam', 'laser', 'release', 'fire', 'shot', 'strike'))}
            flag = ('  <-- REFUSED: placeholder %d, during AIR17-owned AI %d, dialogue %d' % (sum(r['dead'] and r['literal'] for r in R), sum(r['dead'] and r['air17'] for r in R), sum(r['dead'] and r['j3'] for r in R))) if refused else ''
            print('%-20s %-24s req %4d refused %3d | volleys %3d (max %d, refused-in-volley %d) | %s | ev %s%s' % (
                typ, ','.join(s.get('types', [])) if s else '-', len(R), refused, len(vol), max([len(v) for v in vol] or [0]), rv, kinds, beams, flag), flush=True)
            if refused: print('     refused samples', [r for r in R if r['dead']][:3])
            out[typ] = {'spawn': s, 'req': len(R), 'refused': refused, 'volleys': len(vol), 'events': ev, 'kinds': kinds}
        print('page errors', errs[:3]); b.close()
    stop()
    json.dump(out, open(os.path.join(os.path.dirname(HERE), '_shots', 'audit_1101', 'refusals_s%d_%s.json' % (STAGE, DIFF)), 'w'), indent=1)

if __name__ == '__main__':
    main()
