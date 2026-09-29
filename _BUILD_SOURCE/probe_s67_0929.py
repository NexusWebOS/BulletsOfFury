#!/usr/bin/env python3
"""probe_s67_0929.py - Mike's Stage 6/7 list (0929), measured in real Chromium.

    python _BUILD_SOURCE/probe_s67_0929.py [--only NAME[,NAME]] [--json]

Sections: triangles, bombers, supply, warhive. Each asserts on what the game DREW or CALLED
(ctx.drawImage wrapped on the instance, XART.get wrapped for keys), never on a flag the same code sets.
Frames land in _shots/probe_s67_0929/.
"""
import os, sys, json, base64, argparse, http.server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a, **k: None
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(sh.GAME, '_shots', 'probe_s67_0929')
RESULTS = []

def ok(cond, name, detail=''):
    RESULTS.append({'ok': bool(cond), 'name': name, 'detail': detail})
    print(('  ok   ' if cond else '  FAIL ') + name + ('  -- ' + str(detail) if detail != '' else ''))

HOOKS = r"""
() => {
  if (typeof ht27Stop === 'function') ht27Stop();
  window.__keys = {}; window.__sfx = {};
  if (!window.__xg) { window.__xg = XART.get.bind(XART);
    XART.get = function(k){ window.__keys[k] = (window.__keys[k]||0) + 1; return window.__xg(k); }; }
  for (const k of Object.keys(Audio.SFX)) { const f = Audio.SFX[k]; if (typeof f !== 'function' || f.__w) continue;
    const w = function(){ window.__sfx[k] = (window.__sfx[k]||0) + 1; return f.apply(this, arguments); }; w.__w = 1; Audio.SFX[k] = w; }
  window.__hits = 0; playerHit = function(){ window.__hits++; };
  return true;
}
"""
SETUP_STAGE = r"""
(c) => { debugFight = null; coopOn = false; diffKey = c.diff; DIFF = DIFFS[c.diff]; bossDefeated = false; run.mode = 'campaign';
  run.pilot = 'cole'; pilotIndex = PILOTS.findIndex(p => p.key === 'cole');
  beginStage(c.stage); setState(GS.PLAY); story = null; special = null; player.reset();
  stagePlan = []; waveIdx = 999; spawnClock = 9999; enemies = []; eBullets = []; pBullets = []; powerups = [];
  if (typeof groundTargetingReset === 'function') groundTargetingReset();
  window.__keys = {}; window.__sfx = {}; return true; }
"""

def step(pg, frames, chunk=20, pause=20):
    t = 0
    while t < frames:
        n = min(chunk, frames - t)
        e = pg.evaluate(sh.STEP, n)
        if e: RESULTS.append({'ok': False, 'name': 'STEP threw', 'detail': e}); print('  STEP threw', e)
        t += n; pg.wait_for_timeout(pause)

def grab(pg, name):
    os.makedirs(OUT, exist_ok=True)
    d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
    fn = os.path.join(OUT, name + '.png'); open(fn, 'wb').write(base64.b64decode(d.split(',', 1)[1])); return fn

# ---------------------------------------------------------------------------
def sec_triangles(pg):
    print('[triangles]')
    r = pg.evaluate(r"""() => ({s4: drawS4DamageOverlay.toString().replace(/\s/g,''), s6: drawS6DamageOverlay.toString().replace(/\s/g,''), s7: drawS7DamageOverlay.toString().replace(/\s/g,'')})""")
    ok(all(v == 'function(){}' for v in r.values()), 'the three procedural damage overlays draw nothing', r)
    pg.evaluate(SETUP_STAGE, {'diff': 'normal', 'stage': 7})
    step(pg, 30)
    # a damaged stage-7 unit: count lineTo+fill triangles drawn while its draw runs, and the authored damage keys asked for
    r = pg.evaluate(r"""() => {
      const e = spawnEnemy('s7tank', camLeftX()+200, 200, {}); if (!e) return {err:'no spawn'};
      e.hp = e.maxhp * 0.2; e.shoots = false; e._fcd = 99;
      const c = ctx; let lines = 0; const lt = c.lineTo; c.lineTo = function(){ lines++; return lt.apply(this, arguments); };
      window.__keys = {};
      try { for (let i=0;i<8;i++) { drawEnemy(e); drawEnemyDamage(e, 1/60); } } finally { c.lineTo = lt; }
      const dmgKeys = Object.keys(window.__keys).filter(k => /^(nsd_|nxp_upward)/.test(k));
      return {lines, dmgKeys: dmgKeys.slice(0,6), hp: e.hp, max: e.maxhp};
    }""")
    ok(r.get('lines', 1) == 0, 'a critically damaged stage-7 enemy draws no lineTo triangle', r)
    pg.wait_for_timeout(1500)
    r = pg.evaluate(r"""() => { const e = enemies.find(q => q._s7toxic && q.hp < q.maxhp*.5); if (!e) return {err:'gone'};
      window.__keys = {}; for (let i=0;i<8;i++) drawEnemyDamage(e, 1/60);
      return Object.keys(window.__keys).filter(k => /^(nsd_|nxp_upward)/.test(k)).slice(0,6); }""")
    ok(isinstance(r, list) and len(r) > 0, 'the authored damage reels still vent on it', r)
    # an ordinary-enemy warning lane (the stage 3+ bomber lanes): no FOV cone, a band instead
    r = pg.evaluate(r"""() => {
      const e = spawnEnemy('s7tank', camLeftX()+240, 160, {}); if (!e) return {err:'no spawn'};
      let cones = 0; const f = l23FovDraw; l23FovDraw = function(){ cones++; return f.apply(this, arguments); };
      let bands = 0; const b = s67LaneBand; s67LaneBand = function(){ bands++; return b.apply(this, arguments); };
      try { for (const k of [0.1, 0.5, 0.9]) combatWarningDraw(e, {x:e.x, y:e.y+20, ex:e.x, ey:VH, progress:k, width:34}); }
      finally { l23FovDraw = f; s67LaneBand = b; }
      // and a BOSS keeps its cone
      let bossCones = 0; const g = l23FovDraw; l23FovDraw = function(){ bossCones++; return g.apply(this, arguments); };
      const fake = {x:300, y:120, t:1, h:100, w:100};
      try { combatWarningDraw(fake, {x:300, y:120, ex:300, ey:VH, progress:0.5, width:34}); } finally { l23FovDraw = g; }
      return {cones, bands, bossCones};
    }""")
    ok(r.get('cones') == 0 and r.get('bands') == 3, 'an ordinary enemy lane draws a band, never the FOV cone', r)
    ok(r.get('bossCones') == 1, 'a boss warning still draws its FOV cone', r)

def sec_bombers(pg):
    print('[bombers]')
    pg.evaluate(SETUP_STAGE, {'diff': 'normal', 'stage': 6})
    pg.evaluate("() => { s6Opening = null; if (s6Wing) { s6Wing.choice=false; } const O = missionAssaultStart(); window.__O = O; s67AssaultWarm(); return O.events.length; }")
    pg.wait_for_timeout(1200)
    # run straight to the first bomb set
    at = pg.evaluate("() => window.__O.events.find(e => e.kind==='bomb').at")
    step(pg, int(at * 60) + 30)
    r = pg.evaluate(r"""() => { const js = enemies.filter(e => e._mission29 && !e.dead);
      return js.map(e => ({k:e._mission29.kind, s:e._s67Draw, w:e.w, h:e.h, hp:e.hp, dw:e._drawW})); }""")
    bomb = [j for j in r if j['k'] == 'bomb']
    ok(bomb and all(j['s'] == 128 for j in bomb), 'the bomb-run jets draw at 128 (native), was 72', bomb[:2])
    # shoot the bomber: it must flash (the tinted sheet is asked for and blitted)
    r = pg.evaluate(r"""() => { const e = enemies.find(q => q._mission29 && q._mission29.kind==='bomb' && !q.dead); if (!e) return {err:'none'};
      let tints = 0; const t = xartTint; xartTint = function(k){ if (k==='mission29_bluejets') tints++; return t.apply(this, arguments); };
      e.flash = 0; hitEnemy(e, 1); const fl = e.flash;
      try { furyFleetDraw(e); } finally { xartTint = t; }
      return {flash: fl, tints}; }""")
    ok((r.get('flash') or 0) > 0 and r.get('tints', 0) >= 1, 'a shot bomber flashes (tinted cell drawn)', r)
    grab(pg, 'bombers_flash')
    step(pg, 40)
    sfx = pg.evaluate("() => window.__sfx")
    ok(sfx.get('atomicLaunch', 0) >= 1, "the bomb release plays Lizzie's atomicLaunch", {k: v for k, v in sfx.items() if 'atom' in k.lower() or 'missile' in k.lower()})
    grab(pg, 'bombers_falling')
    # step until an impact
    for _ in range(12):
        step(pg, 20)
        n = pg.evaluate("() => s67Nukes.length")
        if n: break
    grab(pg, 'bombers_impact')
    sfx = pg.evaluate("() => window.__sfx")
    ok(pg.evaluate("() => s67Nukes.length") >= 1, 'an impact raises the atomic mushroom', pg.evaluate("() => s67Nukes.map(b=>({x:Math.round(b.x),y:Math.round(b.y),t:+b.t.toFixed(2)}))"))
    ok(sfx.get('atomicDetonate', 0) >= 1, "the impact plays Lizzie's atomicDetonate", {k: v for k, v in sfx.items() if 'atom' in k.lower() or 'exp' in k.lower()})
    step(pg, 12)
    keys = pg.evaluate("() => Object.keys(window.__keys).filter(k => /^lz_(nuke|bomb)/.test(k))")
    ok(any(k.startswith('lz_nuke') for k in keys) and 'lz_bomb' in keys, 'her lz_bomb and lz_nuke art are what draws', keys)
    grab(pg, 'bombers_mushroom')

def sec_supply(pg):
    print('[supply]')
    pg.evaluate(SETUP_STAGE, {'diff': 'normal', 'stage': 6})
    r = pg.evaluate(r"""() => { s6Opening = null; s6WingInit(); const W = s6Wing; s6WingLaunch(3, false);
      for (const q of W.ships) { q.phase = 'fight'; q.y = VH - 140; }
      W.boxes = W.boxes || [];
      W.boxes.push({key:W.ships[0].key, x:200, y:120, w:38, h:38, hp:6, t:0, open:false});
      W.boxes.push({key:_pilotKey(), x:260, y:120, w:38, h:38, hp:6, t:0, open:false});
      let drawn = 0; const g = window.__xg; window.__keys = {};
      s6SupplyTick(W, 1/60); s6SupplyDraw(W);
      const boxes = W.boxes.length, pending = W.s67Grants.length;
      const boost0 = W.ships[0].boostT || 0;
      for (let i = 0; i < 60*7; i++) s6SupplyTick(W, 1/60);
      return {boxes, pending, boost0, boostAfter: W.ships[0].boostT||0, specialKeys: Object.keys(window.__keys).filter(k=>k.startsWith('special_')), left: W.s67Grants.length}; }""")
    ok(r['boxes'] == 0 and r['specialKeys'] == [], 'no supply box exists or draws', r)
    ok(r['pending'] == 2 and r['left'] == 0 and r['boostAfter'] > 0, 'each due box becomes a random grant that lands', r)

def sec_warhive(pg):
    print('[warhive]')
    for d, want in (('normal', 4), ('hard', 5), ('furious', 5)):
        pg.evaluate(SETUP_STAGE, {'diff': d, 'stage': 6})
        n = pg.evaluate("() => { s6Opening=null; spawnBoss('warhive'); bossActive=true; return boss._whv.jetN; }")
        ok(n == want, 'Warhive launches %d escorts on %s' % (want, d), n)

def sec_escape(pg):
    print('[escape]')
    pg.evaluate(SETUP_STAGE, {'diff': 'normal', 'stage': 7})
    pg.evaluate(r"""() => { spawnBoss('sludgeemperor'); bossActive = true; const M = s7mInit(boss); M._mission29IntroDone = true;
      M.mode='recover'; boss.y = boss.ty; mapScroll = s7mEndScroll() - 300; return true; }""")
    pg.wait_for_timeout(1500)
    step(pg, 30)
    pg.evaluate(r"""() => { const b = boss, M = b._s7mod; for (const p of M.parts) p.hp = 0; M.shield = 0; M.core = 0; s7mSet(b, 'dead'); return true; }""")
    track = []
    shots = {1.0: 'escape_selfdestruct', 3.4: 'escape_run', 5.2: 'escape_fire_behind', 7.6: 'escape_portal_arrive',
             8.9: 'escape_entry', 9.4: 'escape_entry_late', 10.6: 'escape_sealed', 11.8: 'escape_wave'}
    t = 0.0; last = None
    while t < 17.5:
        e = pg.evaluate(sh.STEP, 6); t += 0.1
        if e: ok(False, 'STEP threw', e); break
        s = pg.evaluate(r"""() => { const E = boss && boss._s7mod && boss._s7mod.frExit; if (!E) return {st: state};
          const anc = explosions.filter(q => q._s67a); return {st: state, t: +E.t.toFixed(2), S: Math.round(E.S), by: Math.round(boss.y),
            sy: Math.round(_masterSrcY), py: Math.round(player.y), px: Math.round(player.x), pY: Math.round(E.portalYNow),
            exMin: anc.length ? Math.round(Math.min(...anc.map(q => q.y))) : null, free: explosions.filter(q => !q._s67a).length,
            entry: !!E.entry, gone: !!(E.entry && E.entry.gone), scale: E.entry ? +E.entry.scale.toFixed(2) : 1, v: Math.round(E.v)}; }""")
        track.append(s)
        for k, nm in list(shots.items()):
            if s.get('t') is not None and s['t'] >= k:
                grab(pg, nm); del shots[k]
        pg.wait_for_timeout(15)
        if s.get('st') != pg.evaluate("() => GS.PLAY"): break
    json.dump(track, open(os.path.join(OUT, 'escape_track.json'), 'w'), indent=0)
    run = [s for s in track if s.get('t') is not None]
    vmax = max(s['v'] for s in run) if run else 0
    ok(vmax >= 800, 'the escape scrolls fast (peak px/s)', vmax)
    # anchoring: the wreck and the terrain move by the same amount each sample
    bad = [(a['t'], (b['by'] - a['by']), (a['sy'] - b['sy'])) for a, b in zip(run, run[1:]) if abs((b['by'] - a['by']) - (a['sy'] - b['sy'])) > 2 and b['by'] < 900]
    ok(not bad, 'the wreck moves exactly with the terrain', bad[:4])
    # the fire stays behind: after the reactor blows, no anchored explosion climbs above the ship during the run
    runphase = [s for s in run if 3.6 < s['t'] < 7.0 and s['exMin'] is not None]
    close = [s for s in runphase if s['exMin'] < s['py'] - 20]
    ok(runphase and not close, 'the fire stays behind the ship while it flies', [(s['t'], s['exMin'], s['py']) for s in close[:4]])
    ent = [s for s in run if s['entry'] and not s['gone']]
    ok(ent and min(s['scale'] for s in ent) < .4 and abs(ent[-1]['py'] - ent[-1]['pY']) < 40, 'the ship flies into the portal and shrinks', ent[-1] if ent else None)
    ok(any(s.get('st') != pg.evaluate("() => GS.PLAY") for s in track) or track[-1].get('st') == pg.evaluate("() => GS.STAGECLEAR"),
       'the escape ends on the stage clear', track[-1])

WARDEN_SETUP = r"""(d) => { spawnBoss('sludgeemperor'); bossActive = true; const M = s7mInit(boss); M._mission29IntroDone = true;
  boss.y = boss.ty; s7mSet(boss, 'recover'); M.t = 0; window.__B = boss; return M.n; }"""

def sec_warden(pg):
    print('[warden]')
    # rotation: Furious weaves the three modes in; Normal never picks them
    for d, want in (('furious', True), ('normal', False)):
        pg.evaluate(SETUP_STAGE, {'diff': d, 'stage': 7}); pg.evaluate(WARDEN_SETUP, d)
        picks = pg.evaluate(r"""() => { const b = boss, out = []; for (let i = 0; i < 12; i++) { s7mNext(b); out.push(b._s7mod.mode); } return out; }""")
        got = any(m in ('chaingun', 'stomp', 'toxic-mortar') for m in picks)
        ok(got == want, ('Furious weaves in' if want else 'Normal never picks') + ' the new modes', picks)
    pg.evaluate(SETUP_STAGE, {'diff': 'furious', 'stage': 7}); pg.evaluate(WARDEN_SETUP, 'furious')
    pg.wait_for_timeout(1500); step(pg, 20)
    # CHAINGUN
    pg.evaluate("() => { eBullets = []; s7mSet(boss, 'chaingun'); window.__cg = []; return true; }")
    step(pg, 50); grab(pg, 'warden_chaingun_warn')
    angs = []
    for i in range(10):
        step(pg, 12)
        r = pg.evaluate(r"""() => { const M = boss._s7mod; const mg = eBullets.filter(q => q.kind === 'mg' && q._s7modOwner === boss);
          return {mode: M.mode, n: mg.length, angs: mg.map(q => +Math.atan2(q.vy, q.vx).toFixed(2)), gun: M.cgAng ? [ +M.cgAng.gunL.toFixed(2), +M.cgAng.gunR.toFixed(2)] : null}; }""")
        angs += r['angs']
        if i == 4: grab(pg, 'warden_chaingun_fire')
    spread = (max(angs) - min(angs)) if angs else 0
    ok(len(set(angs)) > 20 and spread > 1.0, 'the chaingun sprays real mg bullets in a wide sweep', {'rounds': len(angs), 'spread': round(spread, 2)})
    pose = pg.evaluate(r"""() => { boss._s7mod.mode='chaingun'; boss._s7mod.t=1.4; boss._s7mod.cgAng={gunL:Math.PI/2+.6,gunR:Math.PI/2-.6};
      return s7mPose(boss).filter(p => p.id.startsWith('gun')).map(p => +p.a.toFixed(2)); }""")
    ok(len(pose) == 2 and abs(pose[0] - pose[1]) > .9, 'the barrels themselves angle with the sweep', pose)
    # STOMP then SWAT
    pg.evaluate("() => { eBullets = []; s7mSet(boss, 'stomp'); boss.y = 175; return true; }")
    hs, modes, reticles = [], [], 0
    for i in range(30):
        step(pg, 6)
        r = pg.evaluate("() => ({h: boss._s7mod.height, m: boss._s7mod.mode, w: boss._s7mod.warn, g: groundTargetingFx.filter(q => q.owner === boss && !q.impact).length})")
        hs.append(r['h']); modes.append(r['m']); reticles = max(reticles, r['g'])
        if i == 3: grab(pg, 'warden_stomp_air')
        if r['m'] == 'swipeL' and 'swat' not in [m for m in modes[:-1]]: grab(pg, 'warden_swat')
    ok(max(hs) > 60 and reticles >= 1, 'he hops onto committed landing reticles', {'maxH': round(max(hs)), 'reticles': reticles})
    ok('swipeL' in modes, 'the stomps end in claw swats', sorted(set(modes)))
    # TOXIC MORTAR -> CLOUDS
    pg.evaluate("() => { s67Clouds = []; s7mSet(boss, 'toxic-mortar'); return true; }")
    step(pg, 70); grab(pg, 'warden_mortar_charge')
    for i in range(20):
        step(pg, 12)
        if pg.evaluate("() => s67Clouds.length") >= 4: break
    n = pg.evaluate("() => s67Clouds.length")
    ok(n >= 4, 'the core mortar rounds land as gas clouds', n)
    step(pg, 30)
    keys = pg.evaluate("() => { const got = []; const f = xartPalette; xartPalette = function(k, m){ if (String(k).startsWith('nl6c_low_rolling_bank_')) got.push(k + '|' + m); return f.apply(this, arguments); }; try { drawWorld(0); } finally { xartPalette = f; } return got; }")
    ok(len(keys) >= 1, 'the clouds draw over the field', keys)
    grab(pg, 'warden_clouds')

def sec_carrier(pg):
    print('[carrier]')
    pg.evaluate(SETUP_STAGE, {'diff': 'hard', 'stage': 6})
    pg.evaluate("() => { s6Opening = null; if (s6Wing) { s6Wing.choice=false; s6Wing.route='left'; } spawnBoss('warhive'); bossActive = true; whvWarm(); return true; }")
    pg.wait_for_timeout(1800)
    step(pg, 60 * 4)
    keys = pg.evaluate("() => { window.__keys = {}; drawWorld(0); return Object.keys(window.__keys).filter(k => k.startsWith('whv_')); }")
    ok(all(k in keys for k in ('whv_closed_w', 'whv_well', 'whv_fan', 'whv_cannon')) or all(k in keys for k in ('whv_open_w', 'whv_well', 'whv_fan', 'whv_cannon')),
       'the carrier draws from modules: open-well hull, well floor, fans, cannons', keys)
    r = pg.evaluate(r"""() => { const W = boss._whv; const hub = whvPartPos(boss,'L'), m = s67WhvMuzzle(boss,'L'); return {dep: +W.dep.L.toFixed(2), hubY: Math.round(hub.y), muzY: Math.round(m.y), st: W.st, spin: +W.spin.L.toFixed(1)}; }""")
    ok(r['dep'] > .9 and r['muzY'] - r['hubY'] > 50, 'on Hard the cannon has deployed out under its nacelle', r)
    grab(pg, 'carrier_deployed')
    # force a beam on the left and watch where it comes from
    pg.evaluate("() => { const W = boss._whv; W.can.seq = null; W.beam = {side:'L', t:0, warn:1.55, fire:1.25, w:VW/3}; return true; }")
    step(pg, 60); grab(pg, 'carrier_beam_charge')
    step(pg, 50)
    r = pg.evaluate(r"""() => { const W = boss._whv; if (!W.beam) return {err:'no beam', st: W.st}; const got = []; const d = ctx.drawImage;
      ctx.drawImage = function(im, ...a) { if (im && im.width === 240 && im.height === 617) got.push(a.length >= 8 ? Math.round(a[5]) : Math.round(a[1])); return d.call(this, im, ...a); };
      try { drawWorld(0); } finally { ctx.drawImage = d; }
      return {t: +W.beam.t.toFixed(2), beamY: got, muzY: Math.round(s67WhvMuzzle(boss,'L').y), hubY: Math.round(whvPartPos(boss,'L').y), spin: +W.spin.L.toFixed(1), fanV: +W.fanV.toFixed(1)}; }""")
    ok(r.get('beamY') and abs(r['beamY'][0] - r['muzY']) <= 2 and r['muzY'] > r['hubY'] + 40, 'the beam (Tempest blue) leaves the cannon muzzle, not the fan hub', r)
    ok(r.get('spin', 0) > r.get('fanV', 99) * 1.5, 'the fan spins up as its cannon charges', r)
    grab(pg, 'carrier_beam_fire')
    # a hull hit flashes the hull
    r = pg.evaluate(r"""() => { const W = boss._whv; W.hullFl = 0; _lastHitX = W.cx; _lastHitY = W.cy - 60; boss._whvHit = 'hull';
      hitBoss(4); const fl = W.hullFl; let tints = 0; const t = xartTint; xartTint = function(k){ if (/^whv_(closed|open|broken)_w$/.test(k)) tints++; return t.apply(this, arguments); };
      try { drawWorld(0); } finally { xartTint = t; } return {fl, tints}; }""")
    ok(r['fl'] > 0 and r['tints'] >= 1, 'a hull hit flashes the whole hull (it never did)', r)
    grab(pg, 'carrier_hull_flash')

def sec_ace(pg):
    print('[ace]')
    pg.evaluate(SETUP_STAGE, {'diff': 'hard', 'stage': 6})
    pg.evaluate("() => { s6Opening = null; spawnBoss('warhive'); bossActive = true; whvWarm(); return true; }")
    pg.wait_for_timeout(1500); step(pg, 60 * 3)
    pg.evaluate("() => { const W = boss._whv; W.st='hold'; W.t=0; W.cy=WHV_HOME_Y; W.core=0; return true; }")
    step(pg, 60 * 7)
    r = pg.evaluate("() => ({mode: boss._whv.mode, w: boss.w, h: boss.h})")
    ok(r['mode'] == 'ace' and r['w'] >= 125, 'the ace is 1.5x larger (lock box too)', r)
    pg.wait_for_timeout(1200)
    r = pg.evaluate(r"""() => { const A = boss._whv.ace; A.roll = null; A.somer = null; A.vx = 60; window.__keys = {}; drawWorld(0);
      return Object.keys(window.__keys).filter(k => k.startsWith('whv_acem_')); }""")
    ok(len(r) >= 3, 'the ace draws as modules (fuselage + two wings)', r)
    r = pg.evaluate(r"""() => { const A = boss._whv.ace; A.roll = null; A.somer = null; A.desp = null; A.dash = null; A.st = 'fight';
      const hit = warhiveHitTest(boss, A.x - 30*S67_ACE_K, A.y); if (hit) hitBoss(1); return {hit, fl: A.fl}; }""")
    ok(r['hit'] and r['fl']['wingL'] > 0 and r['fl']['body'] == 0, 'a wing hit flashes that wing only', r)
    grab(pg, 'ace_modular')
    r = pg.evaluate("() => whvAceDecide.toString().includes('.45') && whvAceDecide.toString().includes('rnd(7,9.5)')")
    ok(r, 'the ace keeps its moves on longer cooldowns', r)

SECTIONS = {'carrier': sec_carrier, 'ace': sec_ace, 'escape': sec_escape, 'warden': sec_warden, 'triangles': sec_triangles, 'bombers': sec_bombers, 'supply': sec_supply, 'warhive': sec_warhive}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--only', default=''); ap.add_argument('--json', action='store_true'); a = ap.parse_args()
    names = [s for s in a.only.split(',') if s] or list(SECTIONS)
    port, stop = sh.serve(sh.GAME)
    errs = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:240]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF); pg.evaluate(HOOKS)
        for n in names:
            try: SECTIONS[n](pg)
            except Exception as ex: ok(False, n + ' raised', str(ex)[:300])
        br.close()
    stop()
    ok(not errs, 'no page or console errors', errs[:6])
    fails = [r for r in RESULTS if not r['ok']]
    print('\n%d ok / %d fail' % (len(RESULTS) - len(fails), len(fails)))
    os.makedirs(OUT, exist_ok=True)
    json.dump(RESULTS, open(os.path.join(OUT, 'results.json'), 'w'), indent=1)
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
