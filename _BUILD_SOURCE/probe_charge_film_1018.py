#!/usr/bin/env python3
"""probe_charge_film_1018.py - film the charge -> release of Falva's rollerball, Maverick's helix lance and Jace's
helix nova in real Chromium, one crop every few frames, plus what each frame drew.

Mike, 1018: "now fix the animations when falva or maverick or jace charge and release their attacks"

    python _BUILD_SOURCE/probe_charge_film_1018.py [tag] [pilots]      # pilots: falva,maverick,jace
Writes _shots/charge_1018/<tag>_<pilot>.png (contact sheet, time left->right, top->bottom) and <tag>.json."""
import os, sys, json, base64, io
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
from PIL import Image, ImageDraw
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'charge_1018')

SETUP_PILOT = r"""(cfg) => {
  ASSETS.ready = true; diffKey = 'normal'; run.mode = 'arcade';
  const pi = PILOTS.findIndex(p => p.key === cfg.pilot); if (pi >= 0) pilotIndex = pi;
  startRun(4); curStage = STAGES[3]; beginStage(4); setState(GS.PLAY); player.reset(); run.pilot = cfg.pilot;
  playerHit = function(){}; stagePlan = [];
  for (const k of ['a','d','w','s','j','k','c','h']) if (Input.keys[k] === undefined) Input.keys[k] = false;
  window.__now = performance.now(); return run.pilot; }"""
SETUP_JACE = r"""() => {
  ASSETS.ready = true; diffKey = 'normal'; run.mode = 'arcade';
  startRun(6); curStage = STAGES[5]; beginStage(6); setState(GS.PLAY); player.reset();
  playerHit = function(){}; stagePlan = []; try { s6Opening = null; } catch (e) {}
  for (const k of ['a','d','w','s','j','k','c','h']) if (Input.keys[k] === undefined) Input.keys[k] = false;
  window.__now = performance.now(); spawnBoss('rebelsquad'); bossActive = true; return !!(boss && boss._rebels); }"""
STEP = r"""(n) => { for (let i = 0; i < n; i++) { window.__now += 1000/60; enemies.length = 0; player.invuln = 0; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,200); } } return state; }"""
# one filmed frame: advance, then grab the canvas and a log of what drew
FRAME = r"""(cfg) => {
  const keys = []; const g = XART.get; XART.get = function(k){ if (/fchg|florb|fllaser|nhx|helix|venom|ball|p2_jace|jace|roll|mav|hlx|lance/i.test(k)) keys.push(k); return g.apply(this, arguments); };
  for (let i = 0; i < cfg.n; i++) { if (cfg.hold != null) Input.keys.j = cfg.hold; window.__now += 1000/60; enemies.length = 0; player.invuln = 0;
    if (cfg.pin) { player.x = 340; player.y = 430; }
    try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,200); } }
  XART.get = g;
  const sp = typeof special !== 'undefined' && special ? {pilot: special.pilot, charging: !!special.charging, charge: +(special.charge || 0).toFixed(3), t: +(special.t || 0).toFixed(2)} : null;
  const pb = pBullets.filter(b => !b.dead).map(b => ({k: b.kind, x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.w || 0), t: +(b.t || 0).toFixed(2)})).slice(0, 6);
  let jace = null; if (boss && boss._rebels) { const q = boss._rebels.ships.find(s => s.key === 'jace'); if (q) { const A = q.rg4 && q.rg4.act; jace = {x: Math.round(q.x), y: Math.round(q.y), act: A && A.kind, phase: A && A.phase, t: A && +A.t.toFixed(2), ord: (boss._rebels.g || {}).ord ? null : null}; } }
  return {img: document.getElementById('screen').toDataURL('image/png'), sp, pb, jace, keys: [...new Set(keys)].slice(0, 8), cam: (worldWidth() > viewW()) ? camX : 0, err: window.__err || null}; }"""

def grab(d): return Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGBA')

def film(pg, frames, cx, cy, w=200, h=300):
    tiles, log = [], []
    for f in frames:
        r = pg.evaluate(FRAME, f)
        im = grab(r.pop('img')); k = im.width / 480
        x0 = int((cx(r) - r['cam']) * k - w / 2); y0 = int(cy(r) * k - h * .75)
        t = im.crop((x0, y0, x0 + w, y0 + h)); d = ImageDraw.Draw(t)
        lab = (r['sp'] and ('%s %.2f' % ('CHG' if r['sp']['charging'] else 'rel', r['sp']['charge']))) or (r['jace'] and ('%s %s %s' % (r['jace']['act'], r['jace']['phase'], r['jace']['t']))) or ''
        d.rectangle((0, 0, w, 11), fill=(0, 0, 0)); d.text((2, 0), lab, fill=(255, 255, 0))
        tiles.append(t); log.append(r)
    return tiles, log

def sheet(tiles, cols, path):
    w, h = tiles[0].size; rows = (len(tiles) + cols - 1) // cols
    S = Image.new('RGBA', (w * cols, h * rows), (0, 0, 0, 255))
    for i, t in enumerate(tiles): S.paste(t, ((i % cols) * w, (i // cols) * h))
    S.save(path)

def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else 'before'
    pilots = (sys.argv[2] if len(sys.argv) > 2 else 'falva,maverick,jace').split(',')
    os.makedirs(OUT, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME)
    rep = {}
    with sync_playwright() as p:
        for pk in pilots:
            errs = []
            b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
            pg = b.new_page(viewport={'width': 1000, 'height': 1100})
            pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
            pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
            pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
            pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
            if pk == 'jace':
                pg.evaluate(SETUP_JACE)
                SHOW = "() => { const S = boss && boss._rebels && boss._rebels.h3Intro && boss._rebels.h3Intro.showcase; const D = S && S.current; return D && D.q ? D.q.key + ':' + D.kind : null; }"
                for i in range(200):
                    pg.evaluate(STEP, 10);
                    if i % 6 == 0: pg.wait_for_timeout(40)
                    if pg.evaluate(SHOW) == 'jace:helix': break
                frames = [dict(n=3, hold=None) for _ in range(36)]
                t1, l1 = film(pg, frames, lambda r: (r['jace'] or {}).get('x', 340), lambda r: (r['jace'] or {}).get('y', 150) + 90, 220, 320)
                for i in range(300):
                    pg.evaluate(STEP, 10)
                    if i % 6 == 0: pg.wait_for_timeout(40)
                    j = pg.evaluate("() => { const q = boss && boss._rebels && boss._rebels.ships.find(s => s.key === 'jace'); const A = q && q.rg4 && q.rg4.act; return A ? A.kind + ':' + A.phase : null; }")
                    if j == 'helix:charge': break
                t2, l2 = film(pg, [dict(n=3, hold=None) for _ in range(60)], lambda r: (r['jace'] or {}).get('x', 340), lambda r: (r['jace'] or {}).get('y', 150) + 90, 220, 320)
                tiles, log = t1 + t2, l1 + l2
            else:
                pg.evaluate(SETUP_PILOT, {'pilot': pk})
                for i in range(4): pg.evaluate(STEP, 20); pg.wait_for_timeout(150)
                pg.evaluate("() => { startSpecial(); }")
                for i in range(3): pg.evaluate(STEP, 1); pg.wait_for_timeout(150)
                frames = [dict(n=4, hold=True, pin=True) for _ in range(24)] + [dict(n=3, hold=False, pin=True) for _ in range(24)]
                tiles, log = film(pg, frames, lambda r: 340, lambda r: 430, 220, 360)
            sheet(tiles, 12, os.path.join(OUT, '%s_%s.png' % (tag, pk)))
            rep[pk] = {'log': log, 'errs': errs}
            print(pk, 'frames', len(tiles), 'errs', len(errs), 'keys seen', sorted({k for r in log for k in r['keys']})[:14], flush=True)
            b.close()
    stop()
    json.dump(rep, open(os.path.join(OUT, '%s.json' % tag), 'w'), indent=1)

if __name__ == '__main__':
    main()
