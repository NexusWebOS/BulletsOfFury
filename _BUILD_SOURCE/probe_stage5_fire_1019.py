#!/usr/bin/env python3
"""probe_stage5_fire_1019.py - Mike (overnight 1019): "Level 5, enemies dont shoot and have the same problem before
we adjusted enemy AI."

Real Chromium, the real Stage 5 wave plan, invulnerable test pilot (playerHit stubbed), no shooting by the player.
For --seconds of game time it records, per enemy TYPE: units spawned, frames alive on screen, units that fired at
least once, and rounds fired (each new eBullet is attributed to the nearest live unit within 70 px).
  --stage N  (default 5) - run the same audit on another stage as a control.
Writes _shots/claude_assist_1019/stage<N>_fire.json.
"""
import os, sys, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'claude_assist_1019')

SETUP = r"""(cfg) => { window.CA19_OFF = cfg.bust ? 1 : 0; ASSETS.ready = true; diffKey = cfg.diff; run.mode = 'arcade';
  const pi = PILOTS.findIndex(p => p.key === 'cole'); if (pi >= 0) pilotIndex = pi;
  startRun(cfg.stage); curStage = STAGES[cfg.stage - 1]; beginStage(cfg.stage); setState(GS.PLAY); player.reset();
  playerHit = function(){}; try { s6Opening = null; } catch (e) {}
  for (const k of ['a','d','w','s','j','k','c']) if (Input.keys[k] === undefined) Input.keys[k] = false;
  window.__now = performance.now(); window.__T = {}; window.__seenE = new WeakSet(); window.__seenB = new WeakSet(); window.__fired = new WeakSet();
  for (const b of eBullets) window.__seenB.add(b);
  const KE = killEnemy; killEnemy = function (e) { try { if (e && !e.__kc) { e.__kc = 1; const t = e.type || '?'; const T = window.__T; T[t] = T[t] || {spawned: 0, frames: 0, fired: 0, rounds: 0, shoots: 0, atk: {}}; T[t].kills = (T[t].kills || 0) + 1; if (!(e.__on > 0)) { T[t].killsOffscreen = (T[t].killsOffscreen || 0) + 1; const kb = (typeof _dmgBullet !== 'undefined' && _dmgBullet) ? (_dmgBullet.kind || '?') : ('src:' + (typeof _dmgSrc !== 'undefined' ? _dmgSrc : '-')); T[t].by = T[t].by || {}; T[t].by[kb + '@y' + Math.round(e._drawY ?? e.y)] = 1; } } } catch (_) {} return KE.apply(this, arguments); };
  return {stage: run.stage, space: typeof spaceWeaponsActive === 'function' && spaceWeaponsActive()}; }"""

STEP = r"""(n) => { const T = window.__T;
  for (let i = 0; i < n; i++) { window.__now += 1000/60; player.invuln = 0;
    try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0, 160); }
    if (state !== GS.PLAY) continue;
    if (window.__fire) Input.keys.j = true;
    for (const e of enemies) if (e && (e.dead || e._dyingT != null) && window.__seenE.has(e) && !e.__dc) { e.__dc = 1; const t = e.type || '?'; if (T[t]) { T[t].died = (T[t].died || 0) + 1; if (!window.__fired.has(e)) T[t].diedSilent = (T[t].diedSilent || 0) + 1; } }
    const L = enemies.filter(e => e && !e.dead && e._dyingT == null);
    for (const e of L) { const t = e.type || '?'; T[t] = T[t] || {spawned: 0, frames: 0, fired: 0, rounds: 0, shoots: 0, atk: {}};
      if (!window.__seenE.has(e)) { window.__seenE.add(e); T[t].spawned++; if (e.shoots) T[t].shoots++; const a = String(e._atk || e.fk || e.atk || '-'); T[t].atk[a] = (T[t].atk[a] || 0) + 1; }
      const sx = e.x - ((worldWidth() > viewW()) ? camX : 0); if (sx > -10 && sx < VW + 10 && e.y > 0 && e.y < VH) { T[t].frames++; e.__on = (e.__on || 0) + 1; } }
    for (const b of eBullets) { if (!b || window.__seenB.has(b)) continue; window.__seenB.add(b);
      let best = null, bd = 70; for (const e of L) { const d = Math.hypot(b.x - e.x, b.y - e.y); if (d < bd) { bd = d; best = e; } }
      if (best) { const t = best.type || '?'; T[t].rounds++; if (!window.__fired.has(best)) { window.__fired.add(best); T[t].fired++; (T[t].lat = T[t].lat || []).push(best.__on || 0); } }
      else { T['(unattributed)'] = T['(unattributed)'] || {spawned: 0, frames: 0, fired: 0, rounds: 0, shoots: 0, atk: {}}; T['(unattributed)'].rounds++; } } }
  return {state, enemies: enemies.length, t: +(stageTimer || 0).toFixed(1), err: window.__err || null}; }"""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--stage', type=int, default=5); ap.add_argument('--seconds', type=int, default=90)
    ap.add_argument('--diff', default='normal'); ap.add_argument('--bust', action='store_true'); ap.add_argument('--fire', action='store_true'); a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as p:
        errs = []
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        print(pg.evaluate(SETUP, {'stage': a.stage, 'diff': a.diff, 'bust': a.bust}), flush=True)
        if a.fire: pg.evaluate("() => { Input.keys.j = true; window.__fire = 1; }")
        for i in range(a.seconds):
            r = pg.evaluate(STEP, 60); pg.wait_for_timeout(30)
            if i % 15 == 0: print(i, r, flush=True)
        T = pg.evaluate("() => window.__T")
        hp = pg.evaluate("() => { const o = {}; for (const t of ['s5station','s5minelayer','s5frigate','s5repair']) { const n = enemies.length; spawnEnemy(t, 240, -80); const e = enemies[enemies.length - 1]; o[t] = e && e.type === t ? e.maxhp : null; if (enemies.length > n) enemies.length = n; } return o; }")
        b.close()
    stop()
    print('\n%-22s %7s %7s %6s %6s %6s  %s' % ('type', 'spawned', 'shoots', 'fired', 'rounds', 'frames', 'atk'))
    for t, v in sorted(T.items(), key=lambda kv: -kv[1]['spawned']):
        lat = v.get('lat') or []
        print('%-22s %7d %7d %6d %6d %6d  died %s silent %s KILLED %s offscreen-kills %s first-shot s %s %s' % (t, v['spawned'], v['shoots'], v['fired'], v['rounds'], v['frames'], v.get('died',0), v.get('diedSilent',0), v.get('kills',0), v.get('killsOffscreen',0), [round(x/60,1) for x in lat], list((v.get('by') or {}).keys())))
    print('page errors', errs[:3])
    off = sum(v.get('killsOffscreen', 0) for v in T.values())
    print('heavy hull max hp', hp)
    if a.fire:
        good = off == 0 and (hp.get('s5station') or 0) >= 100 and (hp.get('s5repair') or 0) > 12
        print(('ok   ' if good else 'FAIL ') + 'Stage %d: %d off-screen kills, station %s hp, repair %s hp' % (a.stage, off, hp.get('s5station'), hp.get('s5repair')))
        if not good: sys.exit(1)
    json.dump(T, open(os.path.join(OUT, 'stage%d_fire%s.json' % (a.stage, '_bust' if a.bust else '')), 'w'), indent=1)

if __name__ == '__main__':
    main()
