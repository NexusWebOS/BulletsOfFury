#!/usr/bin/env python3
"""probe_warden_laststand_1017.py - the Olive Warden's last stand, in real Chromium.

Mike, 1017: "Stage 4 miniboss, he does nothing when all his modular pieces are destroyed."

Kills the four modules through the game's own damage route (mr27Damage), then watches the hull:
  - its book becomes the last stand (core fan, hull ram) and it FIRES - counted per round, by owner tag
  - the core fan's rounds leave on exactly the lanes its warning showed (committed gap)
  - the ram tracks the player during green, locks for yellow/red (late movement cannot move it),
    dives off the bottom and returns to station from the top
  - the ram hurts a player standing in its lane and spares one beside it
  - contact is the hull's silhouette now: a player under the turrets' old broad box is not "touching" him
  - escorts come round sooner
  - BUSTED ARM: with the last stand's hooks removed the exposed Warden fires nothing - so the count can fail
Frames: _shots/modular_1017/laststand_*.png
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
  if (cfg.busted) { er26Book = WLS17.base.book; er26Set = WLS17.base.set; sa14MiniAttack = WLS17.base.mini; sa14Escorts = WLS17.base.escorts; }
  return state; }"""
STEP = r"""(n) => { for (let i = 0; i < n; i++) { window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,200); } } return state; }"""
KILL = r"""() => { const b = subBoss; for (const p of b._mr27.parts) { const q = mr27Shape(b, p.id); _lastHitX = q.x; _lastHitY = q.y; mr27Damage(b, 99999, q.x, q.y); }
  return {dead: b._mr27.parts.map(p => p.dead), exposed: typeof wls17Exposed === 'function' ? wls17Exposed(b) : null, book: er26Book(b)}; }"""
# advance until a given mode starts; return frames taken
UNTIL = r"""(cfg) => { for (let i = 0; i < cfg.max; i++) { if (subBoss && subBoss._er26 && subBoss._er26.mode === cfg.mode && subBoss._er26.t < 0.05) return i;
  window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,200); } } return -1; }"""
FAN = r"""() => { const b = subBoss, R = b._er26, T = R._sa14; const warned = new Set(); let warnFrames = 0, warmFrames = 0;
  const seen = new Set(eBullets); const angles = []; let shots = 0;
  while (R.mode === 'sa14-corefan') {
    window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,200); }
    if (R.mode !== 'sa14-corefan') break;
    if (R.t < R.warm) { warmFrames++; if (R.warnings.length) { warnFrames++; for (const w of R.warnings) warned.add(w.angle.toFixed(3)); } }
    for (const q of eBullets) if (!seen.has(q)) { seen.add(q); if (q._wls17) { shots++; angles.push(Math.atan2(q.vy, q.vx).toFixed(3)); } }
  }
  const off = angles.filter(a => !warned.has(a));
  return {warmFrames, warnFrames, lanes: warned.size, shots, offLane: off.length, distinctAngles: new Set(angles).size}; }"""
RAM = r"""(cfg) => { const b = subBoss, R = b._er26, T = R._sa14; const out = {track: [], lockMoves: 0, minY: 1e9, maxY: -1e9, phases: [], ph0: window.__ph};
  const c = wls17Cfg(); let lockedX = null, n = 0;
  player.x = cfg.px0; player.y = PLAY.y + PLAY.h - 60;
  while (R.mode === 'sa14-ram' && n++ < 900) {
    const k = R.t / R.warm;
    if (k > c.ramTrack + 0.05 && R.t < R.warm) { if (lockedX === null) lockedX = b.x; player.x = cfg.px1; }   // dodge AFTER the lock
    if (R.t >= R.warm && cfg.stay) player.x = T.lane;   // stand in the committed lane for the contact check
    eBullets.length = 0; enemies.length = 0;   // only the hull itself may touch the player here - escort rounds are not the ram
    window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,200); }
    if (R.mode !== 'sa14-ram') break;
    if (lockedX !== null && R.t < R.warm && Math.abs(b.x - lockedX) > 0.5) out.lockMoves++;
    if (out.phases[out.phases.length - 1] !== T.phase) out.phases.push(T.phase);
    out.minY = Math.min(out.minY, b.y); out.maxY = Math.max(out.maxY, b.y);
  }
  out.lane = T.lane; out.lockedX = lockedX; out.homeX = T.home.x; out.homeY = T.home.y; out.endX = b.x; out.endY = b.y; out.mode = R.mode;
  out.hits = window.__ph - out.ph0; out.frames = n; return out; }"""
WATCH = r"""(n) => { const seen = new Set(eBullets); let hull = 0, escort = 0; const b = subBoss;
  for (let i = 0; i < n; i++) { window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,200); }
    for (const q of eBullets) if (!seen.has(q)) { seen.add(q); if (q._sa14EscortShot || q._wing17Shot) escort++; else if (q._wls17 || q._sa14Slug || q._sa14Missile) hull++; } }
  return {hull, escort, err: window.__err}; }"""
CONTACT = r"""() => { const b = subBoss, g = mr27Shape(b, 'gunL'); const p0 = window.__ph;
  // a point inside the old broad contact box (w/2+10, h/2+10) but outside the hull silhouette and every piece
  let spot = null;
  for (let dy = b.h * .5; dy > 0 && !spot; dy -= 4) for (let dx = -b.w * .5; dx < b.w * .5; dx += 4) {
    const x = b.x + dx, y = (b._drawY ?? b.y) + dy; if (mr27At(b, x, y) === null) { spot = {x, y}; break; } }
  if (!spot) return {spot: null};
  const R = b._er26; R.mode = 'recover'; R.t = 0; R.dur = 99;
  for (let i = 0; i < 20; i++) { player.x = spot.x; player.y = spot.y; player.invuln = 0; window.__now += 1000/60; try { loop(window.__now); } catch (e) {} }
  const outside = window.__ph - p0;
  const p1 = window.__ph; const hx = b.x, hy = (b._drawY ?? b.y);
  for (let i = 0; i < 20; i++) { player.x = hx; player.y = hy; player.invuln = 0; window.__now += 1000/60; try { loop(window.__now); } catch (e) {} }
  return {spot, outside, inside: window.__ph - p1}; }"""
SNAP = r"""() => document.getElementById('screen').toDataURL('image/png')"""

def boot(p, port, errs):
    b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 1000, 'height': 1100})
    pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:200]))
    pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
    pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
    pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
    return b, pg

def save(pg, name):
    d = pg.evaluate(SNAP); open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

def main():
    os.makedirs(OUT, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME)
    ok = fail = 0; report = {}
    def check(name, cond, info=''):
        nonlocal ok, fail
        if cond: ok += 1
        else: fail += 1
        print(('ok   ' if cond else 'FAIL ') + name + ('  ' + str(info) if info != '' else ''), flush=True)
    with sync_playwright() as p:
        for diff in ('normal', 'hard'):
            errs = []
            b, pg = boot(p, port, errs)
            pg.evaluate(SETUP, {'diff': diff, 'busted': False})
            for i in range(10): pg.evaluate(STEP, 40); pg.wait_for_timeout(80)
            k = pg.evaluate(KILL)
            check('%s: all four modules die through mr27Damage' % diff, all(k['dead']), k)
            check('%s: the Warden reports itself exposed and switches book' % diff, k['exposed'] and 'sa14-corefan' in k['book'], k['book'])
            n = pg.evaluate(UNTIL, {'mode': 'sa14-corefan', 'max': 600}); pg.wait_for_timeout(150)
            check('%s: a core fan starts' % diff, n >= 0, n)
            pg.evaluate(STEP, 30); pg.wait_for_timeout(200); pg.evaluate(STEP, 1)
            if diff == 'normal': save(pg, 'laststand_fan_warn.png')
            f = pg.evaluate(FAN)
            report[diff + '_fan'] = f
            check('%s: the fan is warned on every warm frame' % diff, f['warnFrames'] > 0 and f['warnFrames'] >= f['warmFrames'] - 31, f)
            check('%s: the fan fires (%d rounds over %d lanes)' % (diff, f['shots'], f['lanes']), f['shots'] >= f['lanes'] * 2 and f['lanes'] >= 7)
            check('%s: every round leaves on a lane the warning showed' % diff, f['offLane'] == 0 and f['distinctAngles'] <= f['lanes'], f)
            n = pg.evaluate(UNTIL, {'mode': 'sa14-ram', 'max': 900})
            check('%s: a hull ram starts' % diff, n >= 0, n)
            r = pg.evaluate(RAM, {'px0': 200, 'px1': 470, 'stay': False})
            report[diff + '_ram_dodge'] = r
            check('%s: the ram tracked the player during green' % diff, r['lockedX'] is not None and abs(r['lockedX'] - 340) > 20, r)
            check('%s: the lane does not move after it locks' % diff, r['lockMoves'] == 0, r['lockMoves'])
            check('%s: it dives off the bottom and comes back from the top' % diff, r['maxY'] > 512 and r['minY'] < 0 and r['phases'][:3] == ['track', 'dive', 'drop'], r['phases'])
            check('%s: it ends back on station' % diff, abs(r['endY'] - r['homeY']) < 1 and abs(r['endX'] - r['homeX']) < 1, r)
            check('%s: a player who left the lane after the lock is not hit' % diff, r['hits'] == 0, r['hits'])
            n = pg.evaluate(UNTIL, {'mode': 'sa14-ram', 'max': 1500})
            pg.evaluate(STEP, 20); pg.wait_for_timeout(200); pg.evaluate(STEP, 1)
            if diff == 'normal': save(pg, 'laststand_ram_warn.png')
            r2 = pg.evaluate(RAM, {'px0': 340, 'px1': 340, 'stay': True})
            report[diff + '_ram_stay'] = r2
            check('%s: a player standing in the committed lane is rammed' % diff, n >= 0 and r2['hits'] > 0, r2['hits'])
            w = pg.evaluate(WATCH, 900)
            report[diff + '_watch'] = w
            check('%s: over 15 s the hull fires and the escorts fly' % diff, w['hull'] > 20 and w['escort'] > 0, w)
            c = pg.evaluate(CONTACT)
            report[diff + '_contact'] = c
            check('%s: contact is the silhouette (old box: hit, now: %d) and the hull still hurts (%d)' % (diff, c.get('outside', -1), c.get('inside', -1)), c['spot'] is not None and c['outside'] == 0 and c['inside'] > 0, c)
            check('%s: 0 page/console errors' % diff, not errs, errs[:3])
            b.close()
        # busted arm: the hooks removed, the exposed Warden is the old one
        errs = []
        b, pg = boot(p, port, errs)
        pg.evaluate(SETUP, {'diff': 'normal', 'busted': True})
        for i in range(10): pg.evaluate(STEP, 40); pg.wait_for_timeout(80)
        pg.evaluate(KILL)
        w = pg.evaluate(WATCH, 900)
        report['busted_watch'] = w
        check('busted arm: without the last stand the exposed hull fires nothing (%d)' % w['hull'], w['hull'] == 0, w)
        b.close()
    stop()
    json.dump(report, open(os.path.join(OUT, 'laststand.json'), 'w'), indent=1)
    print('%d ok / %d fail' % (ok, fail))
    sys.exit(1 if fail else 0)

if __name__ == '__main__':
    main()
