#!/usr/bin/env python3
"""probe_spread_muzzle_1019.py - Mike (overnight 1019): "Spread fire, fix and center the muzzle flash on all ships,
needs slow down on lizzie it was going so fast."

Real Chromium. Each pilot fires Spread (level 3) on stage 1, held still at x=240. Every wm26Draw call for the spread
muzzle is recorded (its x,y and frame). The flash's visible INK centre is measured by drawing the exact same call
onto an offscreen canvas and reading its alpha; the ship's nose is measured the same way from the hull frame the
game drew (ship ink in the top rows). Reported: ink-centre offset of the flash from the nose, per pilot.
  pass:  |offset| <= 1.0 px on every pilot.
  --bust runs with window.CA19_OFF=1 (the original placement) so the check can fail.
Also records pellet speed / volleys per second per pilot (the "slow down on lizzie" half).
"""
import os, sys, json, base64, io
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
from PIL import Image
PILOTS = ['cole', 'maverick', 'lizzie', 'juggernaut', 'yuri', 'freezer', 'falva', 'decker', 'axel']
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'claude_assist_1019')

SETUP = r"""(bust) => { window.CA19_OFF = bust ? 1 : 0; ASSETS.ready = true; diffKey = 'normal'; run.mode = 'arcade';
  startRun(1); curStage = STAGES[0]; beginStage(1); setState(GS.PLAY); player.reset();
  playerHit = function(){}; stagePlan = []; enemies.length = 0;
  for (const k of ['a','d','w','s','j','k','c']) if (Input.keys[k] === undefined) Input.keys[k] = false;
  window.__now = performance.now(); return true; }"""

MEASURE = r"""async (cfg) => {
  const pk = cfg.pilot, out = {pk};
  run.pilot = pk; const pi = PILOTS.findIndex(p => p.key === pk); if (pi >= 0) pilotIndex = pi;
  { const _P = PILOTS[pi]; PILOTMOD = {spd: _P.spd || 0, fire: _P.fire || 0, range: _P.range || 0, tint: _P.tint}; }   // as startRun applies it
  player.dead = false; player.invuln = 0; player.roll = null; player.somer = null; player._bank = 0; player._spawnClearT = 0;
  chaingunUnlocked = false; run._earnedUnlocks = {...(run._earnedUnlocks || {}), chaingun: false};
  run.forge = {}; run.forgeForms = {}; run.infusion = null; run.loadout = [1]; powerups = []; run.shield = 0;
  run.weapon = 1; run.wlevels[1] = 3; run.wlevel = 3; player.fireCd = 0;
  XART.rdy('ship_' + pk); for (let i = 0; i < 4; i++) XART.rdy('ndk_muz_' + i);
  for (let i = 0; i < 80 && !(XART.rdy('ship_' + pk) && XART.rdy('ndk_muz_3')); i++) await new Promise(r => setTimeout(r, 50));
  const step = n => { for (let i = 0; i < n; i++) { window.__now += 1000/60; enemies.length = 0; player.invuln = 0; player.x = 240; player.y = 400; player._lx = 240; try { loop(window.__now); } catch (e) { out.err = String(e).slice(0, 160); } } };
  step(4);
  const calls = [], base = wm26Draw;
  wm26Draw = function (g, family, x, y, angle, progress, size, color) { if (family === 'spread' && g === ctx) calls.push({x, y, angle, progress, size, m: ctx.getTransform()}); return base.apply(this, arguments); };
  const seen = new Set(pBullets), pel = []; let volleys = 0;
  Input.keys.j = true;
  for (let f = 0; f < 120; f++) { step(1); let n = 0; for (const b of pBullets) if (!seen.has(b)) { seen.add(b); n++; pel.push(Math.hypot(b.vx || 0, b.vy || 0)); } if (n) volleys++; }
  Input.keys.j = false; wm26Draw = base;
  out.speed = pel.length ? +(pel.reduce((a, b) => a + b, 0) / pel.length).toFixed(2) : null; out.volleysPerSec = volleys / 2;
  if (!calls.length) { out.noCalls = true; return out; }
  // ink centre of the flash as drawn: replay one recorded call onto an offscreen canvas at identity
  const c = calls[Math.floor(calls.length / 2)];
  const off = document.createElement('canvas'); off.width = 400; off.height = 400; const og = off.getContext('2d');
  base.call(null, og, 'spread', 200, 300, c.angle, c.progress, c.size, null);
  const d = og.getImageData(0, 0, 400, 400).data; let sx = 0, sw = 0, ymax = -1;
  for (let y = 0; y < 400; y++) for (let x = 0; x < 400; x++) { const a = d[(y * 400 + x) * 4 + 3]; if (a > 60) { sx += (x + .5) * a; sw += a; ymax = Math.max(ymax, y); } }
  const flashInkDx = sw ? sx / sw - 200 : null;
  // the nose: the ship frame the game draws, at its drawn size, ink centre of its top 4 rows
  const frame = shipGlowKey('ship_' + pk), im = XART.get(frame), H = SHIP_DRAW_H, W = H * (im.width || im.naturalWidth) / (im.height || im.naturalHeight);
  const s2 = document.createElement('canvas'); s2.width = Math.ceil(W) + 4; s2.height = H + 4; const sg = s2.getContext('2d'); sg.imageSmoothingEnabled = false;
  sg.drawImage(im, 2 + (240 - W / 2) % 1, 2, W, H);
  const sd = sg.getImageData(0, 0, s2.width, s2.height).data; let top = -1;
  for (let y = 0; y < s2.height && top < 0; y++) for (let x = 0; x < s2.width; x++) if (sd[(y * s2.width + x) * 4 + 3] > 100) { top = y; break; }
  let nx = 0, nw = 0; for (let y = top; y < top + 4; y++) for (let x = 0; x < s2.width; x++) { const a = sd[(y * s2.width + x) * 4 + 3]; if (a > 100) { nx += (x + .5) * a; nw += a; } }
  const noseX = 240 - W / 2 + (nx / nw - 2 - (240 - W / 2) % 1);   // world x of the nose ink centre
  out.noseX = +(noseX - 240).toFixed(2); out.flashX = +(c.x - 240).toFixed(2); out.flashInk = +(c.x + flashInkDx - 240).toFixed(2);
  out.offset = +(c.x + flashInkDx - noseX).toFixed(2); out.calls = calls.length;
  return out; }"""

def main():
    bust = '--bust' in sys.argv
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    rep = []; ok = fail = 0
    def check(name, cond, info=''):
        nonlocal ok, fail
        ok += cond; fail += (not cond)
        print(('ok   ' if cond else 'FAIL ') + name + ('  ' + str(info)[:300] if info != '' else ''), flush=True)
    with sync_playwright() as p:
        errs = []
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        pg.evaluate(SETUP, bust)
        for pk in PILOTS:
            r = pg.evaluate(MEASURE, {'pilot': pk}); rep.append(r); print(r, flush=True)
            check('%s: the spread flash ink is centred on the nose (offset %s px)' % (pk, r.get('offset')), r.get('offset') is not None and abs(r['offset']) <= 1.0)
        check('0 page errors', not errs and not any(r.get('err') for r in rep), errs[:3])
        b.close()
    stop()
    json.dump(rep, open(os.path.join(OUT, 'spread_muzzle%s.json' % ('_bust' if bust else '')), 'w'), indent=1)
    print('%d ok / %d fail' % (ok, fail)); sys.exit(1 if fail else 0)

if __name__ == '__main__':
    main()
