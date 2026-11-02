#!/usr/bin/env python3
"""probe_elemental_status_1101.py - Forge elements on real enemies (assets/elemental_status_1101.js), real Chromium.
Stage 7, three Slime Jets in a row (test-only: AI paused via _stagger, 600 HP so they survive). The REAL starter gun
fires up into the middle jet for 1.5 s with run.infusion = {elem, lv:3} (the native Forge stamp), then stops for 3 s.
Per element: damage to the target while firing, damage to the neighbours (chain), damage after the gun stops (DoT),
target displacement, flash colours actually returned by hitFlashColor while flashing, swirl draws, and a screenshot.
  checks: toxic DoT > 0 after firing and green flashes; lightning chain damages neighbours, swirl drawn, flashes
  cycle yellow/blue/white; wind pushes the target back (up) far more than the no-element baseline, teal flashes;
  chromium deals more damage than baseline (metal bonus) with gray flashes; no page/console errors.
"""
import os, sys, base64, io
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'elemental_status_1101')
ELEMS = ['none', 'toxic', 'lightning', 'wind', 'chrome', 'fire', 'ice']

SETUP = r"""() => { ASSETS.ready = true; diffKey = 'hard'; DIFF = DIFFS.hard; run.mode = 'arcade'; coopOn = false;
  startRun(7); curStage = STAGES[6]; beginStage(7); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {} for (const k of ['story','fb2Talk','fb2Intro','s6Opening']) { try { window.eval(k + '=null'); } catch (e) {} }
  playerHit = function(){}; stagePlan = []; window.__now = performance.now();
  for (const k of ['l21_wrap_back_00','l21_wrap_front_00']) try { XART.rdy(k); } catch (e) {}
  const tag = new WeakMap(), g = XART.get; XART.get = function (k) { const r = g.apply(this, arguments); try { if (r && typeof r === 'object') tag.set(r, k); } catch (e) {} return r; };
  window.__sw = 0; const dI = ctx.drawImage; ctx.drawImage = function (im) { const k = tag.get(im); if (k && /^l21_wrap_/.test(k)) window.__sw++; return dI.apply(this, arguments); };
  return true; }"""
ARM = r"""(el) => { for (const e of enemies) e.dead = true; enemies.length = 0; eBullets.length = 0; pBullets.length = 0; stagePlan = []; stageTimer = 2;
  run.infusion = el === 'none' ? null : {elem: el, lv: 3}; window.__sw = 0; EL11.events.length = 0;
  const cx = (worldWidth() > viewW() ? camX : 0) + VW / 2, xs = [cx - 70, cx, cx + 70], T = [];
  for (const x of xs) { spawnEnemy('cp22slime', x, 150, {}); const e = enemies[enemies.length - 1]; e.x = x; e.y = 150; e.hp = e.maxhp = e._maxhp = 600; if (e._esh) e._esh = null; T.push(e); }
  window.__T = T; window.__home = T.map(e => ({x: e.x, y: e.y})); window.__cols = {}; window.__hp0 = T.map(e => e.hp);
  player.x = cx; player.y = VH - 90; return {n: T.length, types: T.map(e => e.type), inf: !!infusionActive()}; }"""
STEP = r"""(c) => { const W = window, T = W.__T;
  for (let i = 0; i < c.n; i++) { stageTimer = 2; W.__now += 1000/60;
    for (const e of T) { if (!e.dead) { e._stagger = 99; e.vx = 0; e.vy = 0; } }
    Input.keys.j = !!c.fire; player.x = T[1].x; player.y = VH - 90;
    try { loop(W.__now); } catch (err) { W.__err = String(err).slice(0, 160); }
    for (const e of T) if (e.flash > 0 && !e.dead) { const k = hitFlashColor(e); W.__cols[k] = (W.__cols[k] || 0) + 1; } }
  Input.keys.j = false;
  return {hp: T.map(e => +e.hp.toFixed(1)), pos: T.map(e => [Math.round(e.x), Math.round(e.y)]), err: W.__err || null}; }"""

def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME); res = []; errs = []; R = {}
    def check(name, ok, info=''):
        res.append(bool(ok)); print(('ok   ' if ok else 'FAIL ') + name + ('   ' + str(info)[:300] if info else ''), flush=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio']); pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60); pg.evaluate(SETUP)
        for i in range(200):
            if pg.evaluate("() => { try { stageLoadTick(); return stageLoadReady(7) && XART.rdy('l21_wrap_front_00'); } catch (e) { return true; } }"): break
            pg.wait_for_timeout(100)
        for el in ELEMS:
            a = pg.evaluate(ARM, el); hp0 = [600, 600, 600]
            pg.evaluate(STEP, {'n': 30, 'fire': False})
            s1 = None
            for k in range(9):
                s1 = pg.evaluate(STEP, {'n': 10, 'fire': True}); pg.wait_for_timeout(10)
                if k == 6:
                    d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')"); open(os.path.join(OUT, '%s.png' % el), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
            s2 = pg.evaluate(STEP, {'n': 180, 'fire': False})
            cols = pg.evaluate("() => window.__cols"); sw = pg.evaluate("() => window.__sw"); ev = pg.evaluate("() => EL11.events.map(e => e.event)")
            home = pg.evaluate("() => window.__home")
            R[el] = {'fireT': hp0[1] - s1['hp'][1], 'fireN': (hp0[0] - s1['hp'][0]) + (hp0[2] - s1['hp'][2]), 'after': s1['hp'][1] - s2['hp'][1],
                     'dy': home[1]['y'] - s1['pos'][1][1], 'cols': cols, 'swirl': sw, 'metal': ev.count('metal'), 'kick': ev.count('kick'), 'inf': a['inf'], 'err': s2['err']}
            print('%-9s target %-6.1f neighbours %-6.1f after-fire %-6.1f pushed-up %-4d swirl-blits %-4d metal %-3d kicks %-3d colours %s' % (
                el, R[el]['fireT'], R[el]['fireN'], R[el]['after'], R[el]['dy'], sw, R[el]['metal'], R[el]['kick'], sorted(cols.items(), key=lambda kv: -kv[1])[:4]), flush=True)
        b.close()
    stop()
    B = R['none']
    def has(el, cs): return any(c.lower() in cs for c in R[el]['cols'])
    check('baseline: no element, white flashes only', set(B['cols']) <= {'#ffffff'} and B['fireT'] > 0, B['cols'])
    check('TOXIC: slow damage keeps ticking after the gun stops', R['toxic']['after'] > B['after'] + 5, (R['toxic']['after'], B['after']))
    check('TOXIC: target flashes green', has('toxic', ['#5dff4a']), R['toxic']['cols'])
    check('ELECTRIC: static chain damages the neighbours', R['lightning']['fireN'] > 0 and B['fireN'] == 0, (R['lightning']['fireN'], B['fireN']))
    check('ELECTRIC: lightning swirl drawn around the targets', R['lightning']['swirl'] > 0 and B['swirl'] == 0, R['lightning']['swirl'])
    check('ELECTRIC: flashes cycle yellow / blue / white', all(c in R['lightning']['cols'] for c in ['#ffe03a', '#7fb4ff', '#ffffff']), R['lightning']['cols'])
    check('WIND: target is kicked back up the screen', R['wind']['dy'] >= 25 and R['wind']['dy'] > B['dy'] + 20, (R['wind']['dy'], B['dy']))
    check('WIND: target flashes teal', has('wind', ['#47e6d2']), R['wind']['cols'])
    check('CHROMIUM: metallic bonus damage over the same fire', R['chrome']['metal'] > 0 and R['chrome']['fireT'] > B['fireT'] * 1.15, (R['chrome']['fireT'], B['fireT'], R['chrome']['metal']))
    check('CHROMIUM: target flashes gray', has('chrome', ['#a9b4c2']), R['chrome']['cols'])
    check('FIRE / ICE flash their own colours', has('fire', ['#ff6a1e']) and has('ice', ['#9fdcff']), (R['fire']['cols'], R['ice']['cols']))
    check('every element run had the Forge element active', all(R[e]['inf'] for e in ELEMS if e != 'none'), [R[e]['inf'] for e in ELEMS])
    check('no page/console errors', not errs, errs[:4])
    print('%d/%d passed' % (sum(res), len(res)))
    sys.exit(0 if all(res) else 1)

if __name__ == '__main__':
    main()
