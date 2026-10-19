#!/usr/bin/env python3
"""probe_lizzie_space_mg_1019.py - Mike (overnight 1019): "lizzie's machine gun is slow in space for some reason
when she gets the special."

Real Chromium, real index.html. Lizzie, held fire for 4 s of game time, docked heavy-MG mount granted, on the
ground (stage 1) and in space (stage 5). Counts what actually lands in pBullets per second, by kind.
  --bust   runs without the 1019 fix layer's cadence correction (window.CA19_OFF=1) so the check can fail.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh

RUN = r"""async (cfg) => {
  if (cfg.bust) window.CA19_OFF = 1; else window.CA19_OFF = 0;
  ASSETS.ready = true; diffKey = 'normal'; run.mode = 'arcade';
  const pi = PILOTS.findIndex(p => p.key === 'lizzie'); if (pi >= 0) pilotIndex = pi;
  startRun(cfg.stage); curStage = STAGES[cfg.stage - 1]; beginStage(cfg.stage); setState(GS.PLAY); player.reset();
  run.pilot = 'lizzie'; playerHit = function(){}; stagePlan = []; enemies.length = 0;
  try { s6Opening = null; } catch (e) {}
  for (const k of ['a','d','w','s','j','k','c']) if (Input.keys[k] === undefined) Input.keys[k] = false;
  let now = performance.now();
  const step = n => { for (let i = 0; i < n; i++) { now += 1000/60; enemies.length = 0; player.invuln = 0; try { loop(now); } catch (e) { window.__err = String(e).slice(0,160); } } };
  step(30);
  if (cfg.mount) { lzMountGrant(); lzMount.docked = true; lzMount.life = 99; }
  const space = typeof spaceWeaponsActive === 'function' && spaceWeaponsActive();
  const seen = new Set(pBullets), kinds = {};
  Input.keys.j = true;
  for (let i = 0; i < 240; i++) { step(1); for (const b of pBullets) if (!seen.has(b)) { seen.add(b); kinds[b.kind || '?'] = (kinds[b.kind || '?'] || 0) + 1; } }
  Input.keys.j = false;
  return {stage: cfg.stage, mount: !!cfg.mount, space, mountActive: lzMountActive(), kinds, cad: _weaponCadence(), err: window.__err || null};
}"""

def main():
    bust = '--bust' in sys.argv
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME)
    ok = fail = 0; rep = []
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
        res = {}
        for stage in (1, 5):
            for mount in (False, True):
                r = pg.evaluate(RUN, {'stage': stage, 'mount': mount, 'bust': bust}); rep.append(r)
                res[(stage, mount)] = r
                print(r, flush=True)
        g, s = res[(1, True)], res[(5, True)]
        gs, ss = g['kinds'].get('lzslug', 0) / 4, s['kinds'].get('lzslug', 0) / 4
        check('ground: the docked heavy MG fires lzslug rounds (%.1f/s)' % gs, gs > 15)
        check('space: stage 5 really is a space-weapon stage', s['space'])
        check('space: the docked heavy MG fires at its ground rate (%.1f/s vs %.1f/s)' % (ss, gs), ss >= 0.9 * gs, s)
        check('0 page errors', not errs and not any(r.get('err') for r in rep), errs[:3])
        b.close()
    stop()
    out = os.path.join(os.path.dirname(HERE), '_shots', 'claude_assist_1019'); os.makedirs(out, exist_ok=True)
    json.dump(rep, open(os.path.join(out, 'lizzie_space_mg%s.json' % ('_bust' if bust else '')), 'w'), indent=1)
    print('%d ok / %d fail' % (ok, fail)); sys.exit(1 if fail else 0)

if __name__ == '__main__':
    main()
