#!/usr/bin/env python3
"""probe_s9_fov_1101.py - Stage 9 FOV warnings vs real firing direction, facing, and balance. Real Chromium.
Each Stage-9 type is spawned alone with its plan call (incl. _s9Role), stage clock held, plan empty, passive pilot.
Hooks: combatWarningDraw (every FOV lane drawn: owner, origin, angle), the outermost eShootT/eShoot (every round:
owner, origin, velocity angle), S911/owner beam events. For each round it finds that owner's FOV lanes drawn in the
previous 1.6 s and reports the smallest angular miss between round direction and any lane, plus whether a lane was
shown at all. Facing: round angle vs the owner's displayed heading (S911 head, or spin+90deg).
Per type: HP, visible s, rounds, rounds/s while visible, first shot (s after visible), warned share, median/max FOV
miss, median facing miss, beams. Writes _shots/audit_1101/s9_fov_<diff>.json.
  python _BUILD_SOURCE/probe_s9_fov_1101.py [--diff furious] [--secs 14] [--types a,b]
"""
import os, sys, json, statistics
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
A = sys.argv
DIFF = A[A.index('--diff') + 1] if '--diff' in A else 'furious'
SECS = int(A[A.index('--secs') + 1]) if '--secs' in A else 14
ONLY = A[A.index('--types') + 1].split(',') if '--types' in A else None
CAST = [('s9comet', 'L', .17, {'_side': 1, '_s9Role': 'slider'}), ('s9beacon', .50, -108, {'_s9Role': 'orb'}), ('s9interceptor', .50, -112, {'_s9Role': 'jumper'}),
        ('s9ring', .38, -104, {'_s9Role': 'spinner'}), ('s9gunship', .50, -126, {'_s9Role': 'beam'}), ('wskim', .44, -104, {}),
        ('s9gateturret', .50, -110, {'_s9Role': 'spinner'}), ('s9interceptor', .50, -122, {'_s9Role': 'kamikaze'}), ('gleech', .14, -100, {}),
        ('s9prism', .50, -130, {'_s9Role': 'beam'}), ('echof', .56, -108, {}), ('s9singularity', .50, -120, {'_s9Role': 'orb'}),
        ('s9prism', .72, -142, {'_s9Role': 'orb'}), ('pmine', .50, -104, {}), ('s9gunship', .50, -134, {'_s9Role': 'laser'}),
        ('vmanta', .76, -132, {}), ('tsplit', .50, -118, {}), ('cbreak', .72, -124, {})]
SETUP = r"""(d) => { ASSETS.ready = true; diffKey = d; DIFF = DIFFS[d]; run.mode = 'arcade'; coopOn = false;
  startRun(9); curStage = STAGES[8]; beginStage(9); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {} for (const k of ['story','fb2Talk','fb2Intro','s6Opening']) { try { window.eval(k + '=null'); } catch (e) {} }
  playerHit = function(){}; stagePlan = []; window.__now = performance.now(); window.__F = 0;
  const W = window, own = (o) => { o = o || ai27Context; return o && o.type ? o : null; };
  const head = (e) => { const S = e._s911 || e._s9 || e._s711; if (S && Number.isFinite(S.head)) return S.head; if (Number.isFinite(e.spin)) return e.spin + Math.PI / 2; return Math.PI / 2; };
  W.__head = head;
  const CW = combatWarningDraw; combatWarningDraw = function (e, opt) { try { if (W.__U && e && W.__U.has(e) && opt && Number.isFinite(opt.ex)) W.__W.push({f: W.__F, x: opt.x, y: opt.y, a: Math.atan2(opt.ey - opt.y, opt.ex - opt.x), w: opt.width || 0, ph: e._s911 && e._s911.phase, atk: e._s911 && e._s911.attack}); } catch (_) {} return CW.apply(this, arguments); };
  const T = eShootT; eShootT = function (x, y, a, s, k, opt) { const o = own(opt && opt.owner), b = T.apply(this, arguments);
    if (W.__U && o && W.__U.has(o) && b && !b.dead) W.__R.push({f: W.__F, x, y, a: Math.atan2(b.vy || Math.sin(a), b.vx || Math.cos(a)), kind: k, head: head(o), ph: o._s911 && o._s911.phase, atk: o._s911 && o._s911.attack}); return b; };
  const P = eShoot; eShoot = function () { const o = own(null), n = eBullets.length, r = P.apply(this, arguments);
    if (W.__U && o && W.__U.has(o)) for (const b of eBullets.slice(n)) W.__R.push({f: W.__F, x: b.x, y: b.y, a: Math.atan2(b.vy, b.vx), kind: b.kind || 'eShoot', head: head(o)}); return r; };
  return true; }"""
SPAWN = r"""(c) => { for (const e of enemies) e.dead = true; enemies.length = 0; eBullets.length = 0; stagePlan = []; stageTimer = 2;
  try { boss = null; bossActive = false; subBoss = null; subBossActive = false; } catch (e) {}
  for (const k of ['S911']) { try { const o = window.eval(k); if (o && Array.isArray(o.events)) o.events.length = 0; } catch (e) {} }
  player.x = (worldWidth() > viewW() ? camX : 0) + VW / 2; player.y = VH - 90; window.__R = []; window.__W = []; window.__F = 0;
  const ww = worldWidth(), x = c.x === 'L' ? -86 : ww * c.x, y = c.x === 'L' ? VH * c.y : c.y, n = enemies.length;
  try { spawnEnemy(c.type, x, y, c.opts || {}); } catch (e) { return {err: String(e).slice(0, 160)}; }
  const mine = enemies.slice(n); window.__U = new Set(mine); window.__vis = 0; window.__firstVis = null;
  return {types: mine.map(e => e.type), hp: mine.map(e => Math.round(e.hp)), role: mine[0] && (mine[0]._s9Role || '')}; }"""
STEP = r"""(n) => { const W = window; for (let i = 0; i < n; i++) { stageTimer = 2; W.__F++; W.__now += 1000/60;
    try { loop(W.__now); } catch (e) { W.__err = String(e).slice(0, 160); }
    const e = [...(W.__U || [])].find(u => !u.dead); if (e) { const co = (worldWidth() > viewW()) ? camX : 0, sx = e.x - co, y = e._drawY ?? e.y;
      if (sx > 0 && sx < VW && y > 0 && y < VH) { W.__vis++; if (W.__firstVis == null) W.__firstVis = W.__F; } } }
  return W.__err || null; }"""
EV = r"""() => { const out = {}; for (const k of ['S911']) { let o; try { o = window.eval(k); } catch (e) { continue; }
  if (o && Array.isArray(o.events)) for (const x of o.events) { const n = x.event; out[n] = (out[n] || 0) + 1; } } return out; }"""

def ang(d):
    import math
    d = (d + math.pi) % (2 * math.pi) - math.pi
    return abs(d) * 180 / math.pi

def main():
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME); out = {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio']); pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60); pg.evaluate(SETUP, DIFF)
        for i in range(200):
            if pg.evaluate("() => { try { stageLoadTick(); return stageLoadReady(9); } catch (e) { return true; } }"): break
            pg.wait_for_timeout(100)
        print('%-22s %5s %5s %6s %6s %6s %7s %8s %8s %8s  %s' % ('type/role', 'hp', 'vis', 'rounds', 'r/s', 'first', 'warned', 'fovMed', 'fovMax', 'faceMed', 'events'))
        for typ, x, y, o in CAST:
            key = typ + ('/' + o['_s9Role'] if '_s9Role' in o else '')
            if ONLY and typ not in ONLY and key not in ONLY: continue
            s = pg.evaluate(SPAWN, {'type': typ, 'x': x, 'y': y, 'opts': o})
            for k in range(SECS): pg.evaluate(STEP, 60); pg.wait_for_timeout(10)
            R = pg.evaluate("() => window.__R"); Wn = pg.evaluate("() => window.__W"); ev = pg.evaluate(EV)
            vis = pg.evaluate("() => window.__vis") / 60; fv = pg.evaluate("() => window.__firstVis")
            misses, warned, face = [], 0, []
            for r in R:
                lanes = [w for w in Wn if r['f'] - 96 <= w['f'] <= r['f']]
                if lanes: warned += 1; misses.append(min(ang(r['a'] - w['a']) for w in lanes))
                face.append(ang(r['a'] - r['head']))
            first = round((R[0]['f'] - fv) / 60, 2) if R and fv is not None else None
            row = {'spawn': s, 'vis': round(vis, 1), 'rounds': len(R), 'rps': round(len(R) / vis, 2) if vis else 0, 'first': first,
                   'warned': round(warned / len(R), 2) if R else None, 'fovMed': round(statistics.median(misses)) if misses else None,
                   'fovMax': round(max(misses)) if misses else None, 'faceMed': round(statistics.median(face)) if face else None,
                   'kinds': sorted(set(r['kind'] for r in R)), 'events': ev, 'lanes': len(Wn)}
            out[key] = row
            if os.environ.get('DUMP'):
                for r in R[:40]:
                    ln = [w for w in Wn if r['f'] - 96 <= w['f'] <= r['f']]
                    print('    round f%d %s/%s kind %s a%.0f  lanes %s' % (r['f'], r.get('atk'), r.get('ph'), r['kind'], r['a']*57.3, sorted(set((w.get('atk'), w.get('ph'), round(w['a']*57.3)) for w in ln))[:4]))
            if os.environ.get('GROUP'):
                grp = {}
                for r in R:
                    g = grp.setdefault('%s/%s' % (r.get('atk'), r['kind']), [0, 0]); g[0] += 1
                    if any(r['f'] - 96 <= w['f'] <= r['f'] for w in Wn): g[1] += 1
                for k2, (n2, w2) in sorted(grp.items()): print('    %-28s rounds %3d  lane-warned %3d' % (k2, n2, w2))
            evs = {k: v for k, v in ev.items() if k not in ('spawn',)}
            print('%-22s %5s %5.1f %6d %6.2f %6s %7s %8s %8s %8s  %s %s' % (key[:22], (s.get('hp') or ['-'])[0] if s else '-', row['vis'], row['rounds'], row['rps'], row['first'], row['warned'], row['fovMed'], row['fovMax'], row['faceMed'], row['kinds'], dict(list(evs.items())[:6])), flush=True)
        print('page errors', errs[:3]); b.close()
    stop()
    json.dump(out, open(os.path.join(os.path.dirname(HERE), '_shots', 'audit_1101', 's9_fov_%s.json' % DIFF), 'w'), indent=1)

if __name__ == '__main__':
    main()
