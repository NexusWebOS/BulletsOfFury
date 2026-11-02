#!/usr/bin/env python3
"""probe_s7_dualfire_1101.py - does every Stage-7 refit gun actually release its rounds?
Spawns each S711 model alone on Stage 7 (Furious, like the review films), wraps s711Shot to see every REQUEST
(gun index, returned bullet or null) and records the x of every created round, for 12 s.
Prints per model: requests per gun index, refused (null) per gun index, distinct firing x columns.
  python _BUILD_SOURCE/probe_s7_dualfire_1101.py [--diff furious] [--layer]   (--layer: expect the 1101 fix layer)
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
DIFF = sys.argv[sys.argv.index('--diff') + 1] if '--diff' in sys.argv else 'furious'
CAST = [('s7tank', .5, -92, {}), ('s7pipe', .06, -76, {}), ('cp22relay', .3, -84, {}), ('cp22slime', .5, -90, {}),
        ('s7missilejet', .6, -155, {}), ('s7barge', .5, -130, {}), ('s8crescent', .5, -130, {}), ('ll18brood', .5, -120, {})]

SETUP = r"""(d) => { ASSETS.ready = true; diffKey = d; DIFF = DIFFS[d]; run.mode = 'arcade'; coopOn = false;
  startRun(7); curStage = STAGES[6]; beginStage(7); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {} for (const k of ['story','fb2Talk','fb2Intro','s6Opening']) { try { window.eval(k + '=null'); } catch (e) {} }
  playerHit = function(){}; stagePlan = []; window.__now = performance.now();
  const S = s711Shot; s711Shot = function (e, p, kind, speed, silent, index) { const b = S.apply(this, arguments);
    if (window.__R) window.__R.push({own: e && e.type, i: index | 0, kind, ok: !!b, x: Math.round(p.x), y: Math.round(p.y), t: +efxClock.toFixed(3), held: b ? !!b._ai27Held : null}); return b; };
  return true; }"""
SPAWN = r"""(c) => { for (const e of enemies) e.dead = true; enemies.length = 0; eBullets.length = 0; stagePlan = []; stageTimer = 2;
  player.x = (worldWidth() > viewW() ? camX : 0) + VW / 2; player.y = VH - 90; window.__R = [];
  const ww = worldWidth(); spawnEnemy(c.type, ww * c.x, c.y, c.opts || {}); const e = enemies[enemies.length - 1];
  return e ? {type: e.type, model: e._s711 && e._s711.model} : null; }"""
STEP = r"""(n) => { for (let i = 0; i < n; i++) { stageTimer = 2; window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0, 160); } } return window.__err || null; }"""

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
            if pg.evaluate("() => { try { stageLoadTick(); return stageLoadReady(7); } catch (e) { return true; } }"): break
            pg.wait_for_timeout(100)
        for typ, x, y, o in CAST:
            s = pg.evaluate(SPAWN, {'type': typ, 'x': x, 'y': y, 'opts': o})
            for k in range(12): pg.evaluate(STEP, 60); pg.wait_for_timeout(15)
            R = [q for q in pg.evaluate("() => window.__R") if q['own'] == (s and s['type'])]; out[typ] = R
            by = {}
            for r in R:
                d = by.setdefault(r['i'], [0, 0]); d[0] += 1; d[1] += (not r['ok'])
            beats = {}
            for r in R: beats.setdefault(r['t'], []).append(r['i'])
            pairs = sum(1 for v in beats.values() if len(set(v)) >= 2)
            kinds = sorted(set(r['kind'] for r in R))
            print('%-13s %-12s requests/refused by gun %s | beats %d, beats with 2+ guns %d | kinds %s' % (typ, s and s['model'], {k: tuple(v) for k, v in sorted(by.items())}, len(beats), pairs, kinds))
        print('page errors', errs[:3]); b.close()
    stop()
    json.dump(out, open(os.path.join(os.path.dirname(HERE), '_shots', 'audit_1101', 's7_dualfire_%s.json' % DIFF), 'w'))

if __name__ == '__main__':
    main()
