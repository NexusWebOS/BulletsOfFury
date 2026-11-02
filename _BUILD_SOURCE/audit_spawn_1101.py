#!/usr/bin/env python3
"""audit_spawn_1101.py - per-type front-end audit of the November 1 refits, one unit type at a time.

The real wave plans gate their later casts behind each stage's miniboss, so a timed playthrough never reaches them.
Here the stage is started for real (beginStage, real art/loader), the plan is emptied, and each type is spawned with the
SAME spawnEnemy call its wave plan uses. Real Chromium, TRAP_RAF stepping with real pauses (lazy art decodes),
invulnerable passive pilot parked at the bottom centre. Per type it records:
  path: entry/exit, mean speed px/s, total |dx|, max single-frame jump, time visible
  rounds: every new eBullet within 90 px of the unit: time, kind, angle vs straight-down, angle vs bearing to pilot
  shot gaps (s), first shot (s after first visible frame)
  art keys drawn while it lives (XART.get tags seen by ctx.drawImage), console/page errors during its window
  a crop of the frame around the unit at 3 moments (contact sheet)
  python _BUILD_SOURCE/audit_spawn_1101.py --stage 4 [--secs 14] [--diff normal] [--types s4tanker,s4sam]
"""
import os, sys, json, base64, io, argparse, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
from PIL import Image, ImageDraw
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'audit_1101')

# the plan's own calls (x as a fraction of worldWidth or an edge, y, opts)
CAST = {
 4: [('s4command', .50, -82, {}), ('s4heavyjet', .25, -92, {}), ('s4missile', .30, -90, {}), ('s4tanker', .35, -102, {}),
     ('s4tractor', .67, -116, {}), ('s4sam', .50, -100, {}), ('s4minitank', .30, -62, {}), ('s4airfield', .50, -86, {}),
     ('s4rocket', .27, -72, {'_side': 1}), ('s4interceptor', 'L', .18, {'_side': 1}), ('s4bomber', 'L', .22, {'_side': 1}), ('s4barrel', .38, -54, {})],
 5: [('s5frigate', .30, -90, {}), ('s5interceptor', .70, -80, {}), ('s5rammer', .50, -90, {}), ('s5skimmer', 'L', .18, {'_side': 1}),
     ('s5gravity', .50, -100, {}), ('s5minelayer', .28, -100, {}), ('s5satellite', .72, -90, {}), ('s5portalmine', .32, -80, {}),
     ('s5repair', .50, -88, {}), ('s5station', .50, -110, {}), ('s5leech', .26, -85, {})],
 66: [('l6v_s0', .18, -70, {}), ('l6v_s1', .34, -84, {}), ('l6v_s2', .50, -80, {}), ('l6v_r0', .24, -72, {}), ('l6v_r1', .30, -90, {}), ('l6v_r2', .50, -86, {}), ('l6v_b0', .20, -76, {}), ('l6v_b1', .28, -96, {}), ('l6v_b2', .50, -92, {})],
 6: [('s6dart', .22, -64, {'_jetManeuver': 'dash'}), ('s6mine', .50, -74, {}), ('s6lancer', .28, -74, {}), ('s6skimmer', 'L', .25, {'_side': 1, '_jetManeuver': 'bomb'}),
     ('s6thunder', .30, -76, {}), ('s6probe', .50, -76, {}), ('s6cyclone', .27, -78, {'_side': 1}), ('s6bomber', 'L', .22, {'_side': 1, '_jetManeuver': 'bomb'}),
     ('s6turbine', .50, -96, {})],
 7: [('s7sampler', .28, -72, {}), ('s7pipe', .06, -76, {}), ('s7tank', .50, -92, {}), ('s7skimmer', 'L', .22, {'_side': 1}),
     ('s7lamprey', .27, -84, {'_side': 1}), ('s7mine', .50, -84, {}), ('s7canister', .25, -76, {}), ('s7barge', .50, -130, {}),
     ('s7serpent', .50, -108, {'_side': 1}), ('s7missilejet', .50, -90, {}), ('s7bio', .40, -90, {}), ('s7laser', .60, -90, {}), ('s7toxic', .50, -90, {}), ('s8crescent', .50, -110, {})],
 8: [('s8interceptor', .27, -100, {}), ('s8needlejet', .50, -105, {}), ('s8leech', .50, -120, {}), ('s8scout', .32, -96, {}),
     ('s8razor', .25, -90, {}), ('s8manta', .50, -130, {}), ('s8spread', 'L', .18, {'_side': 1}), ('s8deathorb', .50, -135, {}),
     ('s8parasite', .30, -105, {}), ('s8crescent', .50, -118, {}), ('s8hunter', .28, -105, {}), ('s8skull', .32, -95, {}),
     ('s8solar', .50, -155, {}), ('s8tentacle', .50, -145, {}), ('s8symbiote', .22, -100, {}), ('s8carrier', .50, -180, {}),
     ('s8gunship', .50, -165, {}), ('s8bomber', .28, -150, {})],
}

SETUP = r"""(cfg) => { try { DBG.verbose = true; } catch (e) {}
  ASSETS.ready = true; diffKey = cfg.diff; DIFF = DIFFS[cfg.diff]; run.mode = 'arcade'; coopOn = false;
  const pi = PILOTS.findIndex(p => p.key === 'cole'); if (pi >= 0) pilotIndex = pi;
  startRun(cfg.stage); curStage = STAGES[cfg.stage - 1]; beginStage(cfg.stage); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {}
  for (const k of ['story','fb2Talk','fb2Intro','s6Opening']) { try { window.eval(k + '=null'); } catch (e) {} }
  playerHit = function(){}; stagePlan = [];
  const W = window; W.__now = performance.now();
  const tag = new WeakMap(); W.__tag = tag; const g = XART.get; XART.get = function (k) { const r = g.apply(this, arguments); try { if (r && typeof r === 'object') tag.set(r, k); } catch (e) {} return r; };
  W.__keys = null; const dI = ctx.drawImage; ctx.drawImage = function (im) { if (W.__keys) { const k = tag.get(im); if (k) W.__keys[k] = (W.__keys[k] || 0) + 1; } return dI.apply(this, arguments); };
  return {stage: run.stage, state}; }"""

READY = r"""(n) => { try { if (typeof stageLoadTick === 'function') stageLoadTick(); return typeof stageLoadReady !== 'function' || !!stageLoadReady(n); } catch (e) { return true; } }"""

SPAWN = r"""(c) => { const W = window;
  for (const e of enemies) { e.dead = true; } enemies.length = 0; eBullets.length = 0; stagePlan = [];
  for (const k of ['S411','S511','S611','S711','S811','CC111','CA111']) { try { const o = window.eval(k); if (o && Array.isArray(o.events)) o.events.length = 0; } catch (e) {} }
  stageTimer = 2; warnT = 0; warnKind = null; try { boss = null; bossActive = false; } catch (e) {}
  try { if (subBossActive) { subBossActive = false; subBoss = null; } } catch (e) {}
  player.x = (worldWidth() > viewW() ? camX : 0) + VW / 2; player.y = VH - 90;
  const ww = worldWidth(); const x = c.x === 'L' ? -90 : c.x === 'R' ? ww + 90 : ww * c.x; const y = c.x === 'L' || c.x === 'R' ? VH * c.y : c.y;
  const n = enemies.length; let err = null; try { spawnEnemy(c.type, x, y, c.opts || {}); } catch (e) { err = String(e).slice(0, 200); }
  const mine = enemies.slice(n); W.__U = mine; W.__seenB = new WeakSet(); for (const b of eBullets) W.__seenB.add(b);
  W.__keys = {}; W.__tr = {f: 0, on: 0, first: null, path: [], rounds: [], maxJump: 0, dx: 0, lastx: null, lasty: null, gone: null, hpStart: mine[0] ? mine[0].hp : null, types: mine.map(e => e.type)};
  return {n: mine.length, err, types: mine.map(e => e.type), hp: mine.map(e => e.hp)}; }"""

STEP = r"""(n) => { const W = window, T = W.__tr; const co = () => (worldWidth() > viewW()) ? camX : 0;
  for (let i = 0; i < n; i++) { W.__now += 1000/60; T.f++;
    try { loop(W.__now); } catch (e) { T.err = String(e).slice(0, 160); }
    if (state !== GS.PLAY) continue;
    const e = W.__U[0]; if (!e) break;
    const live = !e.dead && e._dyingT == null;
    if (!live) { if (T.gone == null) T.gone = {f: T.f, killed: !!e.__killed, x: Math.round(e.x), y: Math.round(e.y)}; continue; }
    const x = e.x, y = (e._drawY != null ? e._drawY : e.y), sx = x - co();
    if (T.lastx != null) { const d = Math.hypot(x - T.lastx, y - T.lasty); if (d > T.maxJump) T.maxJump = d; T.dx += Math.abs(x - T.lastx); }
    T.lastx = x; T.lasty = y;
    const vis = sx > 0 && sx < VW && y > 0 && y < VH; if (vis) { T.on++; if (T.first == null) T.first = T.f; }
    if (T.f % 15 === 0) T.path.push([T.f, Math.round(sx), Math.round(y)]);
    for (const b of eBullets) { if (!b || W.__seenB.has(b)) continue; W.__seenB.add(b);
      let near = null, bd = 90; for (const u of W.__U) { if (u.dead) continue; const d = Math.hypot(b.x - u.x, b.y - (u._drawY != null ? u._drawY : u.y)); if (d < bd) { bd = d; near = u; } }
      if (!near) continue;
      const a = Math.atan2(b.vy || 0, b.vx || 0), down = Math.PI / 2, toP = Math.atan2(player.y - b.y, player.x - b.x);
      const dd = (p, q) => { let r = p - q; while (r > Math.PI) r -= 2 * Math.PI; while (r < -Math.PI) r += 2 * Math.PI; return Math.round(Math.abs(r) * 180 / Math.PI); };
      T.rounds.push({f: T.f, kind: b.kind || b.type || '?', vDown: dd(a, down), vPlayer: dd(a, toP), sp: +Math.hypot(b.vx || 0, b.vy || 0).toFixed(2), shoot: !!b._shootable, hm: !!b.homing, ux: Math.round(near.x - co()), uy: Math.round(near._drawY != null ? near._drawY : near.y), vis: (near.x - co()) > 0 && (near.x - co()) < VW && (near._drawY != null ? near._drawY : near.y) > 0});
    }
  }
  const e = W.__U[0];
  return {f: T.f, live: !!(e && !e.dead && e._dyingT == null), x: e ? Math.round(e.x - co()) : null, y: e ? Math.round(e._drawY != null ? e._drawY : e.y) : null, hp: e ? e.hp : null, err: T.err || null}; }"""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--stage', type=int, required=True); ap.add_argument('--secs', type=int, default=14)
    ap.add_argument('--diff', default='normal'); ap.add_argument('--types', default=''); a = ap.parse_args()
    cast = CAST[a.stage]; stage = 6 if a.stage == 66 else a.stage
    if a.types: want = a.types.split(','); cast = [c for c in cast if c[0] in want]
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    results, crops, errs = {}, [], []
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
        pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:220]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:220]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        print(pg.evaluate(SETUP, {'stage': stage, 'diff': a.diff}))
        for i in range(300):
            if pg.evaluate(READY, stage): break
            pg.wait_for_timeout(100)
        pg.evaluate("() => { window.__tr = {f:0}; window.__U = []; for (let i = 0; i < 60; i++) { window.__now += 1000/60; try { loop(window.__now); } catch (e) {} } }")
        for (typ, fx, y, opts) in cast:
            e0 = len(errs)
            s = pg.evaluate(SPAWN, {'type': typ, 'x': fx, 'y': y, 'opts': opts})
            snaps = []
            for sec in range(a.secs * 4):
                r = pg.evaluate(STEP, 15); pg.wait_for_timeout(15)
                if sec in (6, 14, 26) and r['live'] and r['x'] is not None:
                    d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
                    im = Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGB')
                    cw = pg.evaluate("() => [document.getElementById('screen').width, VW, VH]")
                    k = cw[0] / cw[1]; cx, cy = r['x'] * k, r['y'] * k; R = 150 * k
                    box = (int(max(0, cx - R)), int(max(0, cy - R)), int(min(im.width, cx + R)), int(min(im.height, cy + R)))
                    if box[2] > box[0] + 10 and box[3] > box[1] + 10:
                        c = im.crop(box); c.thumbnail((220, 220)); snaps.append(('%s %.1fs' % (typ, (sec + 1) / 4), c))
                if not r['live'] and sec > 4: break
            T = pg.evaluate("() => { const T = window.__tr; const ev = []; for (const k of ['S411','S511','S611','S711','S811','CC111','CA111']) { let o; try { o = window.eval(k); } catch (e) { continue; } if (o && Array.isArray(o.events)) for (const x of o.events) if (x && x.event !== 'spawn') ev.push(k + ':' + x.event + '@' + (x.t != null ? (+x.t).toFixed(2) : '?')); } return {...T, keys: window.__keys, ev: ev.slice(-40)}; }")
            T['spawn'] = s; T['errors'] = errs[e0:]
            results[typ] = T; crops += snaps
            on = T['on'] / 60; R = T['rounds']
            first = (R[0]['f'] - T['first']) / 60 if R and T['first'] is not None else None
            gaps = [round((y2['f'] - y1['f']) / 60, 2) for y1, y2 in zip(R, R[1:])]
            pth = T['path']; spd = None
            if len(pth) > 2: spd = sum(math.hypot(q[1] - p_[1], q[2] - p_[2]) for p_, q in zip(pth, pth[1:])) / ((pth[-1][0] - pth[0][0]) / 60)
            kinds = sorted(set(x['kind'] for x in R))
            print('%-15s spawned %s hp %s | visible %.1fs | speed %s px/s | sum|dx| %d | maxJump %d | rounds %d first %s | kinds %s | vDown %s | vPlayer %s | gone %s | keys %d | errs %d' % (
                typ, s['types'], s['hp'], on, None if spd is None else round(spd), T['dx'], T['maxJump'], len(R), None if first is None else round(first, 2), kinds,
                sorted(set(x['vDown'] // 15 * 15 for x in R))[:8], sorted(set(x['vPlayer'] // 15 * 15 for x in R))[:8], T['gone'], len(T['keys'] or {}), len(T['errors'])))
            if gaps: print('                gaps %s' % gaps[:14])
            off = [(x['ux'], x['uy']) for x in R if not x['vis']]
            if off: print('                FIRED WHILE OFF-SCREEN x%d, at %s' % (len(off), off[:6]))
            if T.get('ev'): print('                events %s' % T['ev'][-14:])
            for e in T['errors'][:3]: print('                ERR', e)
        b.close()
    stop()
    json.dump(results, open(os.path.join(OUT, 'spawn_stage%d_%s.json' % (a.stage, a.diff)), 'w'), indent=1)
    if crops:
        cols = 6; w, h = 220, 220; rows = (len(crops) + cols - 1) // cols
        S = Image.new('RGB', (w * cols, h * rows), (20, 20, 20))
        for i, (lab, im) in enumerate(crops):
            S.paste(im, ((i % cols) * w, (i // cols) * h)); ImageDraw.Draw(S).text(((i % cols) * w + 3, (i // cols) * h + 3), lab, fill=(255, 255, 0))
        S.save(os.path.join(OUT, 'spawn_stage%d_%s.png' % (a.stage, a.diff)))

if __name__ == '__main__':
    main()
