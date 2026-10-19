#!/usr/bin/env python3
"""probe_spread_rounds_1017.py - spread fire flies the machine gun's own rounds, and its stream no longer races.

Mike, 1017: "spread fire, should no longer be the large slugs. should be our actual bullet graphics, but spread
style. and the speed is too fast by level 2/3."

Real Chromium, the real trigger (Input.keys.j held through loop()):
  - every plain spread pellet's draw asks for an mgcf_<level>_ plate (the gun's round), never spr1001_*
  - the plate is rotated along the pellet's own line (pellet heading vs the drawn rotation)
  - level 1's volley rate is unchanged; the stream grows gently with level instead of racing
  - an infused spread pellet still wears the element's round (element_arsenal), not a slug
  - BUSTED ARM: the old slug draw restored -> the slug keys come back, so the key check can fail
Frames: _shots/spread_1017/spread_lv<N>.png
"""
import os, sys, json, base64
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'spread_1017')

SETUP = r"""() => {
  ASSETS.ready = true; diffKey = 'normal'; run.mode = 'arcade';
  startRun(1); curStage = STAGES[0]; beginStage(1); setState(GS.PLAY); player.reset();
  playerHit = function(){}; stagePlan = []; enemies.length = 0;
  for (const k of ['a','d','w','s','j','k','c']) if (Input.keys[k] === undefined) Input.keys[k] = false;
  window.__now = performance.now(); window.__err = null;
  for (let lv = 1; lv <= 5; lv++) for (let f = 0; f < 6; f++) XART.rdy('mgcf_' + lv + '_' + f);
  for (const a of Object.values(SPREAD1001_ART)) XART.rdy(a.key);
  return state; }"""
READY = r"""() => { for (let lv = 1; lv <= 5; lv++) for (let f = 0; f < 6; f++) if (!XART.rdy('mgcf_' + lv + '_' + f)) return false; return true; }"""
RUN = r"""(cfg) => {
  pBullets.length = 0; enemies.length = 0; run.weapon = 1; run.wlevels[1] = cfg.lv; run.wlevel = cfg.lv; run.wvars[1] = null;
  run.infusion = cfg.inf ? {elem: cfg.inf, lv: 3} : null; player.fireCd = 0; player.x = 340; player.y = 440;
  const keys = {}, rots = []; const g = XART.get; let cur = null;
  XART.get = function(k) { if (cur) keys[k] = (keys[k] || 0) + 1; return g.apply(this, arguments); };
  const dm = drawMfx; drawMfx = function(key, x, y, ang) { if (cur && /^mgcf_/.test(key)) rots.push([+(ang || 0).toFixed(3), +(Math.atan2(cur.vy || -1, cur.vx || 0) + Math.PI / 2).toFixed(3)]); return dm.apply(this, arguments); };
  const sd = spreadDraw1001; spreadDraw1001 = function(b) { cur = b; try { return sd.apply(this, arguments); } finally { cur = null; } };
  const seen = new Set(); let pellets = 0;
  for (let i = 0; i < 120; i++) { Input.keys.j = true; enemies.length = 0;
    window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,200); }
    for (const b of pBullets) if ((b.kind === 'spread') && !seen.has(b)) { seen.add(b); pellets++; } }
  Input.keys.j = false; XART.get = g; drawMfx = dm; spreadDraw1001 = sd;
  const slug = Object.keys(keys).filter(k => /^spr1001|spread_?1001/i.test(k) || Object.values(SPREAD1001_ART).some(a => a.key === k));
  const mgcf = Object.keys(keys).filter(k => /^mgcf_/.test(k));
  const badRot = rots.filter(r => Math.abs(r[0] - r[1]) > 0.01).length;
  return {pellets, perSec: +(pellets / 2).toFixed(1), cadence: +_weaponCadence().toFixed(4), mgcf, slug, rots: rots.length, badRot,
          lvOk: mgcf.every(k => k.startsWith('mgcf_' + cfg.lv + '_')), err: window.__err}; }"""
SNAP = r"""() => document.getElementById('screen').toDataURL('image/png')"""

def main():
    os.makedirs(OUT, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME)
    ok = fail = 0; rep = {}
    def check(name, cond, info=''):
        nonlocal ok, fail
        ok += 1 if cond else 0; fail += 0 if cond else 1
        print(('ok   ' if cond else 'FAIL ') + name + ('  ' + str(info) if info != '' else ''), flush=True)
    with sync_playwright() as p:
        errs = []
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.on('console', lambda m: errs.append(m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        pg.evaluate(SETUP)
        pg.wait_for_function(READY, timeout=60000)
        per = {}
        for lv in (1, 2, 3, 4, 5):
            r = pg.evaluate(RUN, {'lv': lv}); rep['lv%d' % lv] = r; per[lv] = r['perSec']
            check('level %d: every pellet draws the gun round (%s), no slug' % (lv, ','.join(sorted(r['mgcf']))[:60]), r['mgcf'] and not r['slug'] and r['lvOk'], r)
            check('level %d: each round is turned along its own line (%d draws, %d off)' % (lv, r['rots'], r['badRot']), r['rots'] > 0 and r['badRot'] == 0)
            d = pg.evaluate(SNAP); open(os.path.join(OUT, 'spread_lv%d.png' % lv), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        check('level 1 keeps its volley rate (cadence %.4f = WEAPON_CADENCE[1])' % rep['lv1']['cadence'], abs(rep['lv1']['cadence'] - pg.evaluate('WEAPON_CADENCE[1]')) < 1e-6)
        check('the stream grows gently with level, pellets/s %s' % per, per[3] <= per[1] * 1.45 and per[5] <= per[1] * 1.7 and per[5] > per[1])
        check('volleys slow as the fan widens (cadence %s)' % [rep['lv%d' % l]['cadence'] for l in range(1, 6)],
              all(rep['lv%d' % (l + 1)]['cadence'] > rep['lv%d' % l]['cadence'] for l in range(1, 5)))
        r = pg.evaluate(RUN, {'lv': 3, 'inf': 'ice'}); rep['ice'] = r
        check('an infused pellet is the element round, not a slug and not drawn by spreadDraw1001', not r['slug'] and not r['mgcf'], r)
        # busted arm: put the old slug draw back
        pg.evaluate("""() => { window.__new = spreadDraw1001; spreadDraw1001 = function(b){ const a=SPREAD1001_ART[b._inf]||SPREAD1001_ART.base;if(!XART.rdy(a.key))return false;
          const r=a.frames[0],h=30+(b.lv||1)*1.5,w=h*r[2]/r[3];ctx.save();ctx.translate(b.x,b.y);ctx.drawImage(XART.get(a.key),...r,-w/2,-h/2,w,h);ctx.restore();return true; }; }""")
        r = pg.evaluate(RUN, {'lv': 3}); rep['busted'] = r
        check('busted arm: the old draw brings the slug back (%s), so the key check can fail' % r['slug'], bool(r['slug']) and not r['mgcf'])
        check('0 page/console errors', not errs, errs[:3])
        b.close()
    stop()
    json.dump(rep, open(os.path.join(OUT, 'report.json'), 'w'), indent=1)
    print('%d ok / %d fail' % (ok, fail)); sys.exit(1 if fail else 0)

if __name__ == '__main__':
    main()
