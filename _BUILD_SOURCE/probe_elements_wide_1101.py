#!/usr/bin/env python3
"""probe_elements_wide_1101.py - Forge elements on every Forge weapon and on bosses, real Chromium.
A) Stage 7, three held Slime Jets (test-only: AI paused, 600 HP). For each of the 9 weapons at level 3 and each element
   (toxic / lightning / wind / chrome) the real trigger fires for 1.5 s, then stops for 2 s. Records element hits that
   reached infusionOnHit (and the round kinds), flash colours, swirl blits, chain damage to neighbours, wind kicks,
   chromium metal hits, damage after firing (toxic).
B) Bosses: Stage 1 / 2 / 5 boss and the Stage 4 miniboss through debugJump (the Boss Mode entry). MG level 3 with each
   element fires at the live encounter: element hits on the boss, flash colours, swirl, metal, no wind displacement.
  python _BUILD_SOURCE/probe_elements_wide_1101.py [--part weapons|bosses|both]
"""
import os, sys, base64, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'elements_wide_1101')
PART = sys.argv[sys.argv.index('--part') + 1] if '--part' in sys.argv else 'both'
ELEMS = ['toxic', 'lightning', 'wind', 'chrome']
COL = {'toxic': ['#5dff4a'], 'lightning': ['#ffe03a', '#7fb4ff'], 'wind': ['#47e6d2'], 'chrome': ['#a9b4c2']}
WEAPONS = ['MACHINE GUN', 'SPREAD FIRE', 'MISSILES', 'LASER', 'FLAMETHROWER', 'ICE ORB', 'LASER MIST', 'CHAINGUN', 'LIGHTNING ORB']

HOOK = r"""() => { const W = window; if (W.__hooked) return true; W.__hooked = 1; W.__now = performance.now(); playerHit = function(){};
  const tag = new WeakMap(), g = XART.get; XART.get = function (k) { const r = g.apply(this, arguments); try { if (r && typeof r === 'object') tag.set(r, k); } catch (e) {} return r; };
  W.__sw = 0; const dI = ctx.drawImage; ctx.drawImage = function (im) { const k = tag.get(im); if (k && /^l21_wrap_/.test(k)) W.__sw++; return dI.apply(this, arguments); };
  const IO = infusionOnHit; infusionOnHit = function (e, b, d) { if (!EL11.busy && !_infBusy && e && b && b._inf) { const t = e === boss ? 'boss' : e === subBoss ? 'sub' : 'enemy'; W.__ih[t] = (W.__ih[t] || 0) + 1; W.__kinds[b.kind] = 1; } return IO.apply(this, arguments); };
  W.__ih = {}; W.__kinds = {}; W.__cols = {}; return true; }"""
STAGE = r"""(c) => { ASSETS.ready = true; diffKey = 'hard'; DIFF = DIFFS.hard; run.mode = 'arcade'; coopOn = false;
  const pi = PILOTS.findIndex(p => p.key === (c.pilot || 'cole')); if (pi >= 0) pilotIndex = pi;
  startRun(c.s); curStage = STAGES[c.s - 1]; beginStage(c.s); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {} for (const k of ['story','fb2Talk','fb2Intro','s6Opening']) { try { window.eval(k + '=null'); } catch (e) {} }
  stagePlan = []; for (const k of ['l21_wrap_back_00','l21_wrap_front_00']) try { XART.rdy(k); } catch (e) {} return true; }"""
WEAP = r"""(c) => { if (!run.wlevels) run.wlevels = WEAPONS.map(() => 0); run.weapon = c.w; run.wlevels[c.w] = 3; run.wlevel = 3; run._chainHeat = 0;
  run.infusion = c.el ? {elem: c.el, lv: 3} : null; try { if (typeof forgeApply === 'function') forgeApply(); } catch (e) {} return {weapon: run.weapon, lv: run.wlevel, inf: infusionActive()}; }"""
ARM = r"""() => { for (const e of enemies) e.dead = true; enemies.length = 0; eBullets.length = 0; pBullets.length = 0; stagePlan = []; stageTimer = 2;
  window.__sw = 0; window.__ih = {}; window.__kinds = {}; window.__cols = {}; EL11.events.length = 0;
  const cx = (worldWidth() > viewW() ? camX : 0) + VW / 2, T = [];
  for (const x of [cx - 70, cx, cx + 70]) { spawnEnemy('cp22slime', x, 150, {}); const e = enemies[enemies.length - 1]; e.x = x; e.y = 150; e.hp = e.maxhp = e._maxhp = 600; e._esh = null; T.push(e); }
  window.__T = T; window.__home = T.map(e => e.y); player.x = cx; player.y = VH - 90; return true; }"""
STEP = r"""(c) => { const W = window, T = W.__T || [];
  for (let i = 0; i < c.n; i++) { if (c.hold) stageTimer = 2; W.__now += 1000/60;
    for (const e of T) if (!e.dead) { e._stagger = 99; e.vx = 0; e.vy = 0; }
    Input.keys.j = !!c.fire; if (c.track) { const t = c.track === 'boss' ? (subBoss && subBossActive ? subBoss : boss) : T[1]; if (t) player.x += (t.x - player.x) * .2; } player.y = c.py || (VH - 90);
    try { loop(W.__now); } catch (err) { W.__err = String(err).slice(0, 160); }
    for (const e of [...T, boss, subBoss]) if (e && e.flash > 0 && !e.dead) { const k = hitFlashColor(e); W.__cols[k] = (W.__cols[k] || 0) + 1; } }
  Input.keys.j = false;
  return {hp: T.map(e => +e.hp.toFixed(1)), y: T.map(e => Math.round(e.y)), err: W.__err || null}; }"""
COLLECT = r"""() => ({ih: window.__ih, kinds: Object.keys(window.__kinds), cols: window.__cols, sw: window.__sw, ev: EL11.events.map(e => e.event)})"""

def page(p, port, errs):
    pg = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio']).new_page(viewport={'width': 1000, 'height': 1100})
    pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:200]))
    pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
    pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
    pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60); return pg

def shot(pg, name):
    d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')"); open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME); res = []; errs = []; out = {}
    def check(name, ok, info=''):
        res.append(bool(ok)); print(('ok   ' if ok else 'FAIL ') + name + ('   ' + str(info)[:260] if (info and not ok) else ''), flush=True)
    with sync_playwright() as p:
        if PART in ('weapons', 'both'):
            pg = page(p, port, errs); pg.evaluate(STAGE, {'s': 7}); pg.evaluate(HOOK)
            for i in range(200):
                if pg.evaluate("() => { try { stageLoadTick(); return stageLoadReady(7) && XART.rdy('l21_wrap_front_00'); } catch (e) { return true; } }"): break
                pg.wait_for_timeout(100)
            for w in [int(x) for x in os.environ.get('WEAPONS', '0,1,2,3,4,5,6,7,8').split(',')]:
                row = {}
                if w == 8:  # Lightning Orb is Yuri's; test-only unlock so the weapon can fire here
                    pg.evaluate(STAGE, {'s': 7, 'pilot': 'yuri'}); pg.evaluate("() => { yuriLightningOrbIsUnlocked = () => true; return true; }")
                PY = 300 if w == 4 else None
                for el in [None] + ELEMS:
                    info = pg.evaluate(WEAP, {'w': w, 'el': el}); pg.evaluate(ARM); pg.evaluate(STEP, {'n': 20, 'hold': True, 'track': 'mid', 'py': PY})
                    s1 = None
                    for k in range(9):
                        s1 = pg.evaluate(STEP, {'n': 10, 'fire': True, 'hold': True, 'track': 'mid', 'py': PY}); pg.wait_for_timeout(5)
                        if k == 6 and el in ('lightning', 'chrome') and w in (2, 3, 4, 5): shot(pg, 'w%d-%s.png' % (w, el))
                    s2 = pg.evaluate(STEP, {'n': 120, 'hold': True, 'track': 'mid', 'py': PY})
                    c = pg.evaluate(COLLECT); home = pg.evaluate("() => window.__home")
                    row[el or 'none'] = {'inf': info['inf'], 'hits': c['ih'].get('enemy', 0), 'kinds': c['kinds'], 'cols': c['cols'], 'sw': c['sw'],
                        'tgt': 600 - s1['hp'][1], 'nb': (600 - s1['hp'][0]) + (600 - s1['hp'][2]), 'after': s1['hp'][1] - s2['hp'][1],
                        'dy': home[1] - s1['y'][1], 'metal': c['ev'].count('metal'), 'kick': c['ev'].count('kick')}
                out[WEAPONS[w]] = row; base = row['none']
                print('%-14s base dmg %5.1f | ' % (WEAPONS[w], base['tgt']) + ' | '.join('%s hits %d kinds %s' % (e[:4], row[e]['hits'], ','.join(row[e]['kinds'])) for e in ELEMS), flush=True)
                for el in ELEMS:
                    r = row[el]; got = r['hits'] > 0
                    check('%s + %s: element reaches the enemy' % (WEAPONS[w], el), got, r)
                    if not got: continue
                    check('%s + %s: flashes its colour' % (WEAPONS[w], el), any(k in r['cols'] for k in COL[el]), r['cols'])
                    if el == 'toxic': check('%s + toxic: keeps damaging after firing' % WEAPONS[w], r['after'] > base['after'] + 3, (r['after'], base['after']))
                    if el == 'lightning': check('%s + electric: chain hurts neighbours + swirl' % WEAPONS[w], r['nb'] > base['nb'] + 5 and r['sw'] > 0, (r['nb'], base['nb'], r['sw']))
                    if el == 'wind': check('%s + wind: target kicked back' % WEAPONS[w], r['kick'] > 0 and r['dy'] > base['dy'] + 15, (r['kick'], r['dy'], base['dy']))
                    if el == 'chrome': check('%s + chromium: metallic bonus hits' % WEAPONS[w], r['metal'] > 0, r['metal'])
            pg.context.browser.close()
        if PART in ('bosses', 'both'):
            for st, role in [x for x in ((1, 'boss'), (2, 'boss'), (4, 'mini'), (5, 'boss')) if str(x[0]) in os.environ.get('BOSSES', '1,2,4,5').split(',')]:
                pg = page(p, port, errs); pg.evaluate(STAGE, {'s': st}); pg.evaluate(HOOK)
                for i in range(200):
                    if pg.evaluate("(s) => { try { stageLoadTick(); return stageLoadReady(s); } catch (e) { return true; } }", st): break
                    pg.wait_for_timeout(100)
                pg.evaluate("(c) => { window.__T = []; debugJump({stage: c.s, role: c.r}); return true; }", {'s': st, 'r': role})
                # wait (firing, no element) until the encounter actually loses HP: entrances/dialogue are protected
                pg.evaluate(WEAP, {'w': 0, 'el': None}); live = False
                for k in range(90):
                    hp0 = pg.evaluate("(r) => { const b = r === 'mini' ? subBoss : boss; return b && !b.dead ? b.hp : null; }", role)
                    pg.evaluate(STEP, {'n': 30, 'fire': k > 4, 'track': 'boss', 'py': 470})
                    hp1 = pg.evaluate("(r) => { const b = r === 'mini' ? subBoss : boss; return b && !b.dead ? b.hp : null; }", role)
                    fl = pg.evaluate("(r) => { const b = r === 'mini' ? subBoss : boss; return !!(b && b.flash > 0); }", role)
                    if hp0 is not None and hp1 is not None and (hp1 < hp0 or (fl and k > 6)): live = True; break
                tag = 'Stage %d %s' % (st, 'miniboss' if role == 'mini' else 'boss')
                check('%s: encounter live and taking damage' % tag, live)
                if not live: pg.context.browser.close(); continue
                rows = {}
                order = os.environ.get('ORDER', ','.join(ELEMS)).split(',')
                for el in order:
                    pg.evaluate(WEAP, {'w': 0, 'el': el})
                    pg.evaluate("() => { window.__sw = 0; window.__ih = {}; window.__kinds = {}; window.__cols = {}; EL11.events.length = 0; for (const b of [boss, subBoss]) if (b) { b._el11 = null; b._el11Poison = 0; b._el11Swirl = 0; } pBullets.length = 0; }")  # test-only: clear the previous element
                    pos0 = pg.evaluate("(r) => { const b = r === 'mini' ? subBoss : boss; return b ? [Math.round(b.x), Math.round(b.y)] : null; }", role)
                    for k in range(8):
                        pg.evaluate(STEP, {'n': 15, 'fire': True, 'track': 'boss', 'py': 470}); pg.wait_for_timeout(5)
                        if k == 5: shot(pg, 'boss-s%d-%s.png' % (st, el))
                    c = pg.evaluate(COLLECT); key = 'sub' if role == 'mini' else 'boss'
                    rows[el] = {'hits': sum(1 for x in pg.evaluate("() => EL11.events.filter(e => e.event === 'boss-hit').map(e => e.el)") if x == el), 'cols': c['cols'], 'sw': c['sw'], 'metal': c['ev'].count('metal'), 'kick': c['ev'].count('kick')}
                    pg.evaluate(STEP, {'n': 40, 'track': 'boss', 'py': 470})
                out[tag] = rows
                print('%-18s ' % tag + ' | '.join('%s hits %d cols %s sw %d metal %d kick %d' % (e[:4], rows[e]['hits'], list(rows[e]['cols'])[:3], rows[e]['sw'], rows[e]['metal'], rows[e]['kick']) for e in ELEMS), flush=True)
                for el in order:
                    r = rows[el]; check('%s + %s: element reaches the boss' % (tag, el), r['hits'] > 0, r)
                    if r['hits'] > 0:
                        check('%s + %s: boss flashes the element colour' % (tag, el), any(k in r['cols'] for k in COL[el]), r['cols'])
                        if el == 'lightning': check('%s + electric: swirl drawn on the boss' % tag, r['sw'] > 0, r['sw'])
                        if el == 'chrome': check('%s + chromium: metallic bonus on the boss' % tag, r['metal'] > 0, r['metal'])
                        if el == 'wind': check('%s + wind: boss is not knocked around' % tag, r['kick'] == 0, r['kick'])
                pg.context.browser.close()
    check('no page/console errors', not errs, errs[:5])
    stop()
    json.dump(out, open(os.path.join(OUT, 'report.json'), 'w'), indent=1)
    print('%d/%d passed' % (sum(res), len(res)))
    sys.exit(0 if all(res) else 1)

if __name__ == '__main__':
    main()
