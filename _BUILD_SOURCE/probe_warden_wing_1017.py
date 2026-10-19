#!/usr/bin/env python3
"""probe_warden_wing_1017.py - the Olive Warden's orbit wing, sounds, flash and no-lightning rule, real Chromium.

Mike, 1017: "my bullets are still just making his entire frame flash white ... on hard, 4 jets should appear, 2 from
the south, 2 from the north, and they shouldnt fly off, they should kinda orbit and circle around the boss until we
destroy them. Then when theyre destroyed, they respawn about 5 seconds later. On Insanity, 6. 2 south, 2 north, 1
east, 1 west ... Get sounds for all his attacks too ... but no lightning."
"""
import os, sys, json, base64
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'modular_1017')

SETUP = r"""(cfg) => {
  ASSETS.ready = true; diffKey = cfg.diff; run.mode = 'arcade';
  startRun(4); curStage = STAGES[3]; beginStage(4); setState(GS.PLAY); player.reset();
  window.__ph = 0; playerHit = function(){ window.__ph++; }; stagePlan = [];
  for (const k of ['a','d','w','s','j','k','c']) if (Input.keys[k] === undefined) Input.keys[k] = false;
  window.__now = performance.now(); window.__err = null; spawnSubBoss('olivewarden');
  window.__SND = {}; for (const k of ['wardenGun','wardenRocket','wardenRackCharge','bossWeaponCharge','razorbackCharge','razorbackRam','tlvJetThrust','tlvJetBrake','enemyMachineGunLight','enemyMachineGunBurst']) {
    const f = Audio.SFX[k]; if (typeof f === 'function') Audio.SFX[k] = function(){ window.__SND[k] = (window.__SND[k] || 0) + 1; return f.apply(this, arguments); }; }
  window.__LIGHT = 0; const g = XART.get; XART.get = function(k){ if (/chain_lightning|lightning_ball|lightning_lance|lightning_mg/.test(k) && subBoss && subBoss._ship === 'olivewarden') window.__LIGHT++; return g.apply(this, arguments); };
  return state; }"""
STEP = r"""(n) => { for (let i = 0; i < n; i++) { window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,200); } } return state; }"""
WATCH = r"""(cfg) => { const b = subBoss, out = {spawns: [], maxJets: 0, offscreenFrames: 0, orbitFrames: 0, shots: 0, warnFrames: 0, angle: {}, minR: 1e9, maxR: 0};
  const seen = new Set(); const S = new Set(eBullets);
  for (let i = 0; i < cfg.frames; i++) { player.x = 340 + Math.sin(i / 40) * 120; player.y = 440;
    window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,200); }
    const J = enemies.filter(e => e._wing17 && !e.dead && e._dyingT == null);
    out.maxJets = Math.max(out.maxJets, J.length);
    for (const e of J) { const A = e._wing17;
      if (!seen.has(e)) { seen.add(e); out.spawns.push({edge: A.slot.edge, x: Math.round(A.from.x), y: Math.round(A.from.y), frame: i}); }
      if (A.t >= 1.3) { out.orbitFrames++; const L = camLeftX(), R = camRightX();
        if (e.x < L || e.x > R || e.y < 0 || e.y > VH) out.offscreenFrames++;
        const d = Math.hypot(e.x - b.x, e.y - (b._drawY ?? b.y)); out.minR = Math.min(out.minR, d); out.maxR = Math.max(out.maxR, d);
        const a = Math.atan2(e.y - b.y, e.x - b.x); const k = A.serial; (out.angle[k] = out.angle[k] || []).push(a); }
      if (A.phase === 'warn') out.warnFrames++; }
    for (const q of eBullets) if (!S.has(q)) { S.add(q); if (q._wing17Shot) out.shots++; } }
  // total angle swept by each jet: proves it circles rather than parks
  out.swept = Object.values(out.angle).map(L => { let s = 0; for (let i = 1; i < L.length; i++) { let d = L[i] - L[i-1]; while (d > Math.PI) d -= 2*Math.PI; while (d < -Math.PI) d += 2*Math.PI; s += d; } return +Math.abs(s).toFixed(2); });
  delete out.angle; out.err = window.__err; return out; }"""
KILLONE = r"""() => { const J = enemies.filter(e => e._wing17 && !e.dead && e._dyingT == null); if (!J.length) return null;
  const e = J[0], edge = e._wing17.slot.edge, slot = e._wing17.slot.i; e.hp = 1; _dmgBullet = null; hitEnemy(e, 9999); if (!e.dead && e._dyingT == null) hitEnemy(e, 9999);
  let f = 0; for (; f < 600; f++) { window.__now += 1000/60; try { loop(window.__now); } catch (e) {}
    const n = enemies.find(q => q._wing17 && q !== e && !q.dead && q._wing17.slot.i === slot && q._wing17.t < .05); if (n) return {edge, slot, respawnS: +(f / 60).toFixed(2), sameEdge: n._wing17.slot.edge === edge, fromY: Math.round(n._wing17.from.y), fromX: Math.round(n._wing17.from.x)}; }
  return {edge, slot, respawnS: null}; }"""
FLASH = r"""() => { const b = subBoss; const g = mr27Shape(b, 'gunR'); b.flash = 0; for (const p of b._mr27.parts) p.flash = 0;
  _lastHitX = g.x; _lastHitY = g.y; hitSubBoss(3, g.x, g.y); const piece = {hull: b.flash, gun: b._mr27.parts.find(p => p.id === 'gunR').flash};
  b.flash = 0; let c = null; for (let y = b.y - b.h * .3; y < b.y + b.h * .3 && !c; y += 3) if (mr27At(b, b.x, y) === 'core') c = y;
  _lastHitX = b.x; _lastHitY = c; hitSubBoss(3, b.x, c); return {piece, hull: b.flash}; }"""
KILLMODS = r"""() => { const b = subBoss; for (const p of b._mr27.parts) { const q = mr27Shape(b, p.id); _lastHitX = q.x; _lastHitY = q.y; mr27Damage(b, 99999, q.x, q.y); } return b._mr27.parts.every(p => p.dead); }"""

def main():
    os.makedirs(OUT, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME)
    ok = fail = 0; rep = {}
    def check(name, cond, info=''):
        nonlocal ok, fail
        ok += 1 if cond else 0; fail += 0 if cond else 1
        print(('ok   ' if cond else 'FAIL ') + name + ('  ' + str(info)[:300] if info != '' else ''), flush=True)
    with sync_playwright() as p:
        for diff, want in (('normal', None), ('hard', {'S': 2, 'N': 2}), ('furious', {'S': 2, 'N': 2, 'E': 1, 'W': 1}), ('insanity', {'S': 2, 'N': 2, 'E': 1, 'W': 1})):
            errs = []
            b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
            pg = b.new_page(viewport={'width': 1000, 'height': 1100})
            pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
            pg.on('console', lambda m: errs.append(m.text[:200]) if m.type == 'error' else None)
            pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
            pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
            pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
            pg.evaluate(SETUP, {'diff': diff})
            for i in range(6): pg.evaluate(STEP, 40); pg.wait_for_timeout(120)
            w = pg.evaluate(WATCH, {'frames': 1200}); rep[diff + '_watch'] = w
            if want is None:
                check('%s: no orbit wing (fly-in escort turns as before)' % diff, w['maxJets'] == 0, w['maxJets'])
            else:
                edges = {}
                for s in w['spawns'][:len(sum(([k] * v for k, v in want.items()), []))]: edges[s['edge']] = edges.get(s['edge'], 0) + 1
                check('%s: %d jets fly at once' % (diff, sum(want.values())), w['maxJets'] == sum(want.values()), w['maxJets'])
                check('%s: they enter from %s' % (diff, want), edges == want, w['spawns'])
                check('%s: south jets come from below the screen, north from above' % diff,
                      all((s['y'] > 512 if s['edge'] == 'S' else s['y'] < 0 if s['edge'] == 'N' else True) for s in w['spawns']), w['spawns'])
                check('%s: they orbit him and never fly off (%d orbit frames, %d off screen, radius %d..%d)' % (diff, w['orbitFrames'], w['offscreenFrames'], w['minR'], w['maxR']),
                      w['orbitFrames'] > 600 and w['offscreenFrames'] == 0 and w['maxR'] < 300)
                check('%s: each jet circles (swept %s rad over 20 s)' % (diff, w['swept']), w['swept'] and min(w['swept']) > 3.0)
                check('%s: they fire warned bursts (%d rounds, %d warn frames)' % (diff, w['shots'], w['warnFrames']), w['shots'] >= 10 and w['warnFrames'] > 0)
                k = pg.evaluate(KILLONE); rep[diff + '_respawn'] = k
                check('%s: a destroyed jet is replaced ~5 s later from the same edge (%s s)' % (diff, k and k['respawnS']), bool(k) and k['respawnS'] is not None and 4.7 <= k['respawnS'] <= 5.6 and k['sameEdge'], k)
            fl = pg.evaluate(FLASH); rep[diff + '_flash'] = fl
            check('%s: a module hit flashes the module only (module %.2f, hull %.2f); a hull hit flashes the hull (%.2f)' % (diff, fl['piece']['gun'], fl['piece']['hull'], fl['hull']),
                  fl['piece']['gun'] > 0 and fl['piece']['hull'] == 0 and fl['hull'] > 0)
            pg.evaluate(KILLMODS)
            w2 = pg.evaluate(WATCH, {'frames': 1200}); rep[diff + '_laststand_watch'] = w2
            if want is not None:
                check('%s: through the last stand (rams included) the wing keeps circling on screen (%d orbit frames, %d off)' % (diff, w2['orbitFrames'], w2['offscreenFrames']),
                      w2['orbitFrames'] > 600 and w2['offscreenFrames'] == 0)
            snd = pg.evaluate('window.__SND'); light = pg.evaluate('window.__LIGHT'); rep[diff + '_sound'] = snd
            need = ['wardenGun', 'wardenRocket', 'wardenRackCharge', 'bossWeaponCharge', 'razorbackCharge', 'razorbackRam', 'tlvJetBrake'] + (['tlvJetThrust', 'enemyMachineGunLight'] if want else [])
            check('%s: every attack has its sound %s' % (diff, snd), all(snd.get(k, 0) > 0 for k in need), [k for k in need if not snd.get(k)])
            check('%s: no lightning art is drawn on the Warden (%d asks)' % (diff, light), light == 0)
            if diff != 'normal':
                d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
                open(os.path.join(OUT, 'wing_%s.png' % diff), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
            check('%s: 0 page/console errors' % diff, not errs, errs[:3])
            b.close()
    stop()
    json.dump(rep, open(os.path.join(OUT, 'wing.json'), 'w'), indent=1)
    print('%d ok / %d fail' % (ok, fail)); sys.exit(1 if fail else 0)

if __name__ == '__main__':
    main()
