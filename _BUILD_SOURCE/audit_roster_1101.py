#!/usr/bin/env python3
"""audit_roster_1101.py - independent front-end audit of the November 1 regular-enemy refits (Stages 4-8).

Not the owning agent's probes: this plays each stage's REAL wave plan in real Chromium (TRAP_RAF, game clock stepped in
chunks with real pauses so lazy art decodes), with an invulnerable test pilot (playerHit stubbed, never invuln-pinned),
and records per enemy TYPE:
  spawned / on-screen frames / never-entered (died or culled with 0 visible frames)
  fired units, rounds (each new eBullet attributed to the nearest live unit within 80 px), first-shot latency (s on screen)
  kills / off-screen kills (killEnemy while the unit had 0 visible frames)
  teleports: largest single-frame world displacement (> 60 px flagged)
  stuck: units visible > 20 s that moved < 8 px in total
Two arms per stage: passive (pilot does not fire) and firing (pilot holds fire and weaves).
Also: every console error / page error (DBG.verbose on, so swallowed draw errors are reported every time), and a
contact sheet of full frames every 6 s.
  python _BUILD_SOURCE/audit_roster_1101.py [--stages 4,5,6,7,8] [--seconds 80] [--diff normal]
Writes _shots/audit_1101/stage<N>_<arm>.json and stage<N>_sheet.jpg.
"""
import os, sys, json, base64, io, argparse, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
from PIL import Image, ImageDraw
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'audit_1101')

SETUP = r"""(cfg) => { try { DBG.verbose = true; } catch (e) {}
  ASSETS.ready = true; diffKey = cfg.diff; DIFF = DIFFS[cfg.diff]; run.mode = 'arcade'; coopOn = false;
  const pi = PILOTS.findIndex(p => p.key === 'cole'); if (pi >= 0) pilotIndex = pi;
  startRun(cfg.stage); curStage = STAGES[cfg.stage - 1]; beginStage(cfg.stage); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {}
  for (const k of ['story','fb2Talk','fb2Intro','s6Opening']) { try { window.eval(k + '=null'); } catch (e) {} }
  playerHit = function(){};
  for (const k of ['a','d','w','s','j','k','c']) if (Input.keys[k] === undefined) Input.keys[k] = false;
  window.__now = performance.now(); window.__f = 0;
  const W = window; W.__T = {}; W.__seen = new WeakSet(); W.__seenB = new WeakSet(); W.__fired = new WeakSet();
  for (const b of eBullets) W.__seenB.add(b);
  const KE = killEnemy; killEnemy = function (e) { try { if (e && !e.__kc) { e.__kc = 1; const R = W.__T[e.type]; if (R) { R.kills++; if (!(e.__on > 0)) R.offKills++; } } } catch (_) {} return KE.apply(this, arguments); };
  return {stage: run.stage, state, space: typeof spaceWeaponsActive === 'function' && spaceWeaponsActive()}; }"""

READY = r"""(n) => { try { if (typeof stageLoadTick === 'function') stageLoadTick(); return typeof stageLoadReady !== 'function' || !!stageLoadReady(n); } catch (e) { return true; } }"""

STEP = r"""(cfg) => { const W = window, T = W.__T;
  const camOff = () => (worldWidth() > viewW()) ? camX : 0;
  for (let i = 0; i < cfg.n; i++) { W.__now += 1000/60; W.__f++;
    if (cfg.fire) { Input.keys.j = true; const ph = W.__f / 60; Input.keys.a = Math.sin(ph * 0.9) < -0.3; Input.keys.d = Math.sin(ph * 0.9) > 0.3; }
    try { loop(W.__now); } catch (e) { W.__err = String(e).slice(0, 160); }
    if (state !== GS.PLAY) continue;
    const L = enemies.filter(e => e && !e.dead && e._dyingT == null), co = camOff();
    for (const e of L) { const t = e.type || '?';
      const R = T[t] = T[t] || {spawned: 0, frames: 0, fired: 0, rounds: 0, lat: [], kills: 0, offKills: 0, maxJump: 0, jumps: 0, stuck: 0, neverEntered: 0};
      const x = e.x, y = (e._drawY != null ? e._drawY : e.y);
      if (!W.__seen.has(e)) { W.__seen.add(e); R.spawned++; e.__lx = x; e.__ly = y; e.__path = 0; }
      else { const d = Math.hypot(x - e.__lx, y - e.__ly); e.__path += d; if (d > R.maxJump) R.maxJump = Math.round(d); if (d > 60) R.jumps++; e.__lx = x; e.__ly = y; }
      const sx = x - co; if (sx > 0 && sx < VW && y > 0 && y < VH) { R.frames++; e.__on = (e.__on || 0) + 1; }
    }
    for (const b of eBullets) { if (!b || W.__seenB.has(b)) continue; W.__seenB.add(b);
      let best = null, bd = 80; for (const e of L) { const d = Math.hypot(b.x - e.x, b.y - (e._drawY != null ? e._drawY : e.y)); if (d < bd) { bd = d; best = e; } }
      if (best) { const R = T[best.type]; if (R) { R.rounds++; if (!W.__fired.has(best)) { W.__fired.add(best); R.fired++; R.lat.push(+((best.__on || 0) / 60).toFixed(1)); } } }
    }
    for (const e of enemies) if (e && (e.dead || e._dyingT != null) && W.__seen.has(e) && !e.__done) { e.__done = 1; const R = T[e.type];
      if (R) { if (!(e.__on > 0)) R.neverEntered++; if ((e.__on || 0) > 1200 && e.__path < 8) R.stuck++; } }
  }
  if (cfg.fire) { Input.keys.j = false; Input.keys.a = false; Input.keys.d = false; }
  return {state, n: enemies.length, t: +(stageTimer || 0).toFixed(1), boss: !!(bossActive && boss), sub: !!(subBossActive && subBoss), err: W.__err || null}; }"""

FINAL = r"""() => { const T = window.__T;
  for (const e of enemies) if (e && window.__seen.has(e) && !e.__done) { const R = T[e.type]; if (R && (e.__on || 0) > 1200 && e.__path < 8) R.stuck++; }
  return T; }"""

def run_arm(p, port, stage, arm, secs, diff, shots):
    errs = []
    b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 1000, 'height': 1100})
    pg.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
    pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:220]))
    pg.on('console', lambda m: errs.append('console: ' + m.text[:220]) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
    pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
    pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
    info = pg.evaluate(SETUP, {'stage': stage, 'diff': diff})
    for i in range(300):
        if pg.evaluate(READY, stage): break
        pg.wait_for_timeout(100)
    log = []
    for s in range(secs):
        r = pg.evaluate(STEP, {'n': 60, 'fire': arm == 'firing'}); pg.wait_for_timeout(25)
        if s % 10 == 0: log.append((s, r)); print('  s%d %s %3ds %s' % (stage, arm, s, r), flush=True)
        if shots is not None and s % 6 == 3:
            d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/jpeg', .72)")
            im = Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGB'); im.thumbnail((300, 330)); shots.append(('%s %ds' % (arm, s), im))
    T = pg.evaluate(FINAL)
    b.close()
    return {'info': info, 'types': T, 'log': log, 'errors': errs}

def report(stage, arm, R):
    T = R['types']
    print('\n=== Stage %d  %s  (%d console/page errors)' % (stage, arm, len(R['errors'])))
    print('%-22s %4s %6s %5s %5s %6s %5s %5s %5s %5s %5s  %s' % ('type', 'spwn', 'frames', 'never', 'fired', 'rounds', 'kills', 'offK', 'maxJ', 'jumps', 'stuck', 'first-shot s'))
    for t, v in sorted(T.items(), key=lambda kv: -kv[1]['spawned']):
        print('%-22s %4d %6d %5d %5d %6d %5d %5d %5d %5d %5d  %s' % (t[:22], v['spawned'], v['frames'], v['neverEntered'], v['fired'], v['rounds'], v['kills'], v['offKills'], v['maxJump'], v['jumps'], v['stuck'], v['lat'][:6]))
    seen = set()
    for e in R['errors']:
        k = e[:120]
        if k in seen: continue
        seen.add(k); print('   ERR', e)
        if len(seen) > 8: break

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--stages', default='4,5,6,7,8'); ap.add_argument('--seconds', type=int, default=80)
    ap.add_argument('--diff', default='normal'); ap.add_argument('--arms', default='passive,firing'); a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as p:
        for stage in [int(x) for x in a.stages.split(',')]:
            shots = []
            for arm in a.arms.split(','):
                R = run_arm(p, port, stage, arm, a.seconds, a.diff, shots)
                json.dump(R, open(os.path.join(OUT, 'stage%d_%s_%s.json' % (stage, arm, a.diff)), 'w'), indent=1)
                report(stage, arm, R)
            if shots:
                cols = 7; w, h = shots[0][1].size; rows = (len(shots) + cols - 1) // cols
                S = Image.new('RGB', (w * cols, h * rows))
                for i, (lab, im) in enumerate(shots):
                    S.paste(im, ((i % cols) * w, (i // cols) * h)); ImageDraw.Draw(S).text(((i % cols) * w + 4, (i // cols) * h + 4), lab, fill=(255, 255, 0))
                S.save(os.path.join(OUT, 'stage%d_sheet_%s.jpg' % (stage, a.diff)))
    stop()

if __name__ == '__main__':
    main()
