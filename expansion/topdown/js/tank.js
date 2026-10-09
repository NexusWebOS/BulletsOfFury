/*
 * Tanks, turrets, cameras, props, pickups and every projectile.
 *
 * PLAYER: immediate smooth movement, independent turret aim, and C hull lock for sideways strafe.
 * Separate calibrated hull and turret layers share the authored socket. VULCAN / CRASH / LASER /
 * HOMING) on A, the main cannon on B with recoil, a charged piercing round on X, smoke on Y, Z swaps.
 *
 * ENEMIES see through the stealth module's cones and hunt with the flow field. A shot that lands on
 * a unit that has not noticed you (green cone) deals double damage - the sneak strike.
 * Art: tk0..tk4 (tan/olive/black/blue/green) N/E/S/W plates, intact/damaged/critical; turret cores,
 * the radar-dish emplacement as a camera, s1 fuel barrels / ammo crates, BOF's own ordnance.
 */
(function (root) {
  'use strict';
  const TD = root.TD, M = TD.M, W = TD.World, A = TD.Audio, FX = TD.FX, Cam = TD.Cam;
  const TS = 0.5;                                     // tank plates are 124 px cells; drawn at half
  const DIRK = ['s', 'w', 'n', 'e'];                  // heading 0 faces south; +PI/2 per step (clockwise on screen)

  // ------------------------------------------------------------------ drawing a tank
  function tankKey(art, u) {
    const st = u.hp > u.max * 0.66 ? 'inta' : u.hp > u.max * 0.33 ? 'dama' : 'crit';
    const k = ((Math.round(u.a / (Math.PI / 2)) % 4) + 4) % 4;
    return { key: art + '_' + st + '_' + DIRK[k], resid: M.wrap(u.a - k * Math.PI / 2) };
  }
  function drawTank(ctx, u, art, s) {
    const { key, resid } = tankKey(art, u), sc = (s || TS);
    ART.draw(ctx, key, u.x + 4, u.y + 6, { a: resid, s: sc, tint: '#000000', alpha: 0.33 });
    ART.draw(ctx, key, u.x, u.y, { a: resid, s: sc, flash: u.flash > 0 ? u.flash / 0.12 : 0 });
  }
  TD.drawTank = drawTank;

  // 1008g: the Overdrive ground tanks. 192 px north-facing canvases, hull centre (96,124) on every family;
  // the turret shares the canvas, so it sits in its socket by construction. a=0 faces south here.
  TD.PILOTS = ['cole', 'axel', 'maverick', 'decker', 'yuri', 'freezer', 'juggernaut', 'phoenix', 'lizzie', 'falva', 'hotwire'];
  TD.FAMILY = { siege: ['juggernaut', 'phoenix'], panzer: ['lizzie', 'falva', 'hotwire'] };
  TD.familyOf = pk => TD.FAMILY.siege.includes(pk) ? 'siege' : TD.FAMILY.panzer.includes(pk) ? 'panzer' : 'assault';
  const MUZZLE = { siege: 30, assault: 38, panzer: 45 };    // native muzzle distance from the hull centre, halved to draw scale
  TD.muzzleDist = p => MUZZLE[TD.familyOf(p.pilot)];
  const PS = 0.5;
  TD.drawPlayerTank = function (ctx, p, o) {
    o = o || {};
    const k = 'pt_' + p.pilot + '_', a = p.a + Math.PI, hull = k + (p.hp < p.max * 0.4 ? 'damaged_hull' : 'hull');
    const opt = { a, s: PS, ax: 96, ay: 124 };
    ART.draw(ctx, hull, p.x + 4, p.y + 6, Object.assign({}, opt, { tint: '#000000', alpha: 0.33 }));
    ART.draw(ctx, hull, p.x, p.y, Object.assign({}, opt, { flash: o.flash || 0 }));
    // recoil slides the turret back along the barrel; the hull stays put
    const aim = p.aim == null ? p.a : p.aim, [fx, fy] = M.fwd(aim);
    const kick = Math.min(6, (p.recoil || 0) * 0.7) + (p.charge || 0) / 72 * 3;
    ART.draw(ctx, k + 'turret', p.x - fx * kick, p.y - fy * kick, Object.assign({}, opt, { a: aim + Math.PI, flash: o.flash || 0 }));
  };
  // enemy armour: the on-foot pack's alien tanks, whole plates authored facing north
  function drawAlienTank(ctx, u, T) {
    const mv = Math.hypot(u.x - (u.lx == null ? u.x : u.lx), u.y - (u.ly == null ? u.y : u.ly)) > 0.15; u.lx = u.x; u.ly = u.y;
    const st = (u.burst > 0 || u.fireWarn > 0) ? 'fire' : u.hp < u.max * 0.5 ? 'damaged' : mv && ((TD.game.t / 6) | 0) % 2 ? 'tread' : 'idle';
    const key = 'et_' + T.et + '_' + st, o = { a: u.a + Math.PI, s: T.ds };
    ART.draw(ctx, key, u.x + 4, u.y + 6, Object.assign({}, o, { tint: '#000000', alpha: 0.33 }));
    ART.draw(ctx, key, u.x, u.y, Object.assign({}, o, { flash: u.flash > 0 ? u.flash / 0.12 : 0 }));
  }

  // ------------------------------------------------------------------ weapons
  const WPN = TD.WPN = {
    vulcan: { name: 'VULCAN', icon: 'micon_mg_', cd: [6, 5, 5], noise: 140 },
    crash: { name: 'CRASH', icon: 'micon_fireorb_', cd: [24, 20, 16], noise: 230 },
    laser: { name: 'LASER', icon: 'micon_laser_', cd: [11, 9, 8], noise: 170 },
    homing: { name: 'HOMING', icon: 'micon_missile_', cd: [22, 18, 15], noise: 190 },
  };
  const ICON_LV = [1, 3, 5];
  TD.iconFor = (id, lv) => WPN[id].icon + ICON_LV[M.clamp(lv, 1, 3) - 1];

  function shot(list, o) { o.t = 0; list.push(o); return o; }
  function firePrimary(p, G) {
    const w = p.weapons[p.wi], lv = w.lv, def = WPN[w.id], aim = p.aim, [fx, fy] = M.fwd(aim);
    const md = TD.muzzleDist(p) - 4, mx = p.x + fx * md, my = p.y + fy * md;
    if (w.id === 'vulcan') {
      const spread = lv === 1 ? [0] : lv === 2 ? [-1, 1] : [-0.12, 0, 0.12];
      for (const s of spread) {
        const a = lv === 2 ? aim : aim + s + M.rnd(-0.03, 0.03), off = lv === 2 ? s * 6 : 0, [px, py] = M.fwd(aim + Math.PI / 2), [vx, vy] = M.fwd(a);
        shot(G.shots, { k: 'vulcan', x: mx + px * off, y: my + py * off, vx: vx * 7.5, vy: vy * 7.5, a, dmg: 1, life: 55, r: 4 });
      }
      A.play('mg'); FX.flash(mx, my, aim, 0.14);
    } else if (w.id === 'crash') {
      shot(G.shots, { k: 'crash', x: mx, y: my, vx: fx * 5, vy: fy * 5, a: aim, dmg: 2 + lv, life: 48, r: 7, splash: 26 + lv * 12, sdmg: 1 + lv });
      A.play('cannon', 0.55); FX.flash(mx, my, aim, 0.18);
    } else if (w.id === 'laser') {
      shot(G.shots, { k: 'laser', x: mx, y: my, vx: fx * 11, vy: fy * 11, a: aim, dmg: 2, life: 40, r: 4, pierce: lv + 1, lv });
      A.play('laser');
    } else if (w.id === 'homing') {
      for (let i = 0; i < lv; i++) {
        const a = aim + (i - (lv - 1) / 2) * 0.28, [vx, vy] = M.fwd(a), [sx, sy] = M.fwd(aim + Math.PI / 2);
        const offset = (i - (lv - 1) / 2) * 10;
        shot(G.shots, { k: 'homing', x: mx + sx * offset, y: my + sy * offset, vx: vx * 2.8, vy: vy * 2.8, a,
          dmg: 3, life: 130, r: 5, homing: true, splash: 27, sdmg: 2 });
      }
      A.play('missile');
    }
    TD.Stealth.noise(p.x, p.y, def.noise, 0.4, G.units);
    p.fireCd = def.cd[lv - 1];
  }
  function fireCannon(p, G, power) {
    const aim = p.aim, [fx, fy] = M.fwd(aim), md = TD.muzzleDist(p), mx = p.x + fx * md, my = p.y + fy * md, big = power >= 1;
    shot(G.shots, { k: 'shell', x: mx, y: my, vx: fx * 15.6, vy: fy * 15.6, a: aim, dmg: big ? 14 : 6, life: 30, r: big ? 9 : 5, splash: big ? 56 : 34, sdmg: big ? 6 : 3, pierce: big ? 3 : 0, big });
    p.recoil = big ? 10 : 6; p.kickAim = aim; p.vx -= fx * (big ? 4.2 : 2.3); p.vy -= fy * (big ? 4.2 : 2.3); Cam.kick(big ? 5 : 2);
    FX.flash(mx, my, aim, big ? 0.34 : 0.24); FX.smoke(mx, my, big ? 0.22 : 0.14, 0.6, fx * 0.6, fy * 0.6); FX.casing(p.x, p.y, aim);
    A.play('cannon', big ? 1 : 0.8);
    TD.Stealth.noise(p.x, p.y, big ? 520 : 420, big ? 0.9 : 0.75, G.units);
    p.canCd = 45;
  }

  // ------------------------------------------------------------------ the player tank
  TD.makePlayer = (x, y) => ({
    x, y, vx: 0, vy: 0, r: 20, a: Math.PI, aim: Math.PI, manualAim: 0, hp: 12, max: 12, inv: 90, flash: 0, recoil: 0, fireCd: 0, canCd: 0, charge: 0,
    smoke: 3, weapons: [{ id: 'vulcan', lv: 1 }], wi: 0, dead: false, hidden: false, moving: false, pilot: TD.pilot || 'cole', speed: 2.7,
  });
  TD.playerTick = function (p, G, dt) {
    if (p.onfoot) return TD.footTick(p, G, dt);
    const I = TD.Input;
    if (p.dead) return;
    p.flash = Math.max(0, p.flash - dt); if (p.inv > 0) p.inv--;
    p.recoil *= 0.74; if (p.recoil < 0.05) p.recoil = 0;
    const [dx, dy] = I.dir(), lock = I.down('C');
    const inHedge = !!W.inType(p.x, p.y, 'h');
    const spd = p.speed * (inHedge ? 0.55 : 1);
    const len = Math.hypot(dx, dy) || 1, slowdown = I.down('X') ? 0.68 : 1;
    const tx = dx / len * spd * slowdown, ty = dy / len * spd * slowdown;
    p.vx = M.lerp(p.vx, tx, dx || dy ? 0.24 : 0.34); p.vy = M.lerp(p.vy, ty, dx || dy ? 0.24 : 0.34);
    if ((dx || dy) && !lock) {
      const want = M.angTo(0, 0, dx, dy), diff = Math.abs(M.wrap(want - p.a));
      if (diff < 2.65) p.a = M.turnTo(p.a, want, 0.12);
    }
    const aim = I.aim(p);
    if (aim != null) { p.aim = M.turnTo(p.aim, aim, 0.18); p.manualAim = 30; }
    else if (I.down('aimLeft') || I.down('aimRight')) {
      p.aim += (I.down('aimRight') ? 1 : -1) * 0.07; p.manualAim = 120;
    } else if (p.manualAim > 0) p.manualAim--;
    else if (!lock) p.aim = M.turnTo(p.aim, p.a, 0.12);
    p.moving = Math.hypot(p.vx, p.vy) > 0.15;
    p.x += p.vx; p.y += p.vy;
    // Charge tension gently seats the whole tank behind the bore, while firing
    // adds a larger physical impulse. The collision pass constrains both.
    if (I.down('X') && p.charge < 40) { const [fx, fy] = M.fwd(p.aim); p.x -= fx * 0.09; p.y -= fy * 0.09; }
    if (p.moving && G.t % 10 === 0) { const [fx, fy] = M.fwd(p.a); FX.smoke(p.x - fx * 24, p.y - fy * 24, 0.07, 0.5); }
    for (const q of G.props) if (!q.dead) pushOut(p, q);
    W.collide(p, p.r, false);
    p.hidden = !!W.inType(p.x, p.y, 'h');
    // weapons
    if (I.state.wheel || I.tap('Z')) { if (p.weapons.length > 1) { p.wi = (p.wi + (I.state.wheel < 0 ? -1 : 1) + p.weapons.length) % p.weapons.length; A.play('blip'); } }
    if (p.fireCd > 0) p.fireCd--; if (p.canCd > 0) p.canCd--;
    if (I.down('A') && p.fireCd <= 0) firePrimary(p, G);
    if (I.tap('B') && p.canCd <= 0 && !I.down('X')) fireCannon(p, G, 0);
    if (I.down('X') && p.canCd <= 0) { if (p.charge === 0) A.play('charge'); p.charge = Math.min(72, p.charge + 1); }
    else if (p.charge > 0) { if (p.canCd <= 0) fireCannon(p, G, p.charge >= 40 ? 1 : 0); p.charge = 0; }
    if (I.tap('Y') && p.smoke > 0) {
      p.smoke--; const [fx, fy] = M.fwd(p.aim);
      G.grenades.push({ x: p.x, y: p.y, tx: p.x + fx * 90, ty: p.y + fy * 90, t: 0 }); A.play('blip', 0.8);
    }
  };
  function pushOut(o, q) {
    const dx = o.x - q.x, dy = o.y - q.y, d = Math.hypot(dx, dy), m = o.r + q.r;
    if (d < m && d > 0.01) {
      o.x = q.x + dx / d * m; o.y = q.y + dy / d * m;
      if (o === TD.game.player && q.kind === 'crate') q.crush = (q.crush || 0) + 1;   // a tank shoving a crate breaks it
    }
  }
  TD.pushOut = pushOut;
  TD.hurtPlayer = function (G, dmg, x, y) {
    const p = G.player; if (p.dead || p.inv > 0 || G.state !== 'play') return;
    p.hp -= p.onfoot ? p.hp : dmg; p.inv = 50; p.flash = 0.18; Cam.kick(5); A.play('hit');
    if (x != null) FX.boom(x, y, 40, 'nxp_clus_');
    if (p.hp <= 0) TD.game.playerDied();
  };

  // ------------------------------------------------------------------ enemy types
  const ET = TD.ET = {
    scout: { art: 'tk0', et: 'light', ds: 0.56, hp: 4, speed: 1.55, r: 19, vis: { range: 190, half: 0.62 }, gun: 'burst', cd: 1.6, prefer: [110, 190], score: 300 },
    rifle: { art: 'tk1', et: 'light', ds: 0.62, hp: 7, speed: 1.1, r: 20, vis: { range: 210, half: 0.6 }, gun: 'shell', cd: 2.3, prefer: [150, 230], score: 500 },
    heavy: { art: 'tk2', et: 'heavy', ds: 0.66, hp: 15, speed: 0.78, r: 22, vis: { range: 200, half: 0.55 }, gun: 'twin', cd: 2.8, warn: 0.4, prefer: [130, 220], score: 900 },
    sniper: { art: 'tk4', et: 'heavy', ds: 0.58, hp: 6, speed: 0.85, r: 20, vis: { range: 320, half: 0.26, rate: 0.75 }, gun: 'snipe', cd: 3.4, warn: 0.75, prefer: [230, 310], score: 700 },
    turret: { art: 'oft_north', hurt: 'oft_damaged', fire: 'oft_fire', wreck: 'oft_wreck', hp: 10, r: 18, vis: { range: 240, half: 0.7 }, gun: 'burst', cd: 1.3, still: true, score: 600 },
    camera: { art: 'oft_base', wreck: 'oft_wreck', ds: 0.34, hp: 3, r: 14, vis: { range: 220, half: 0.28, rate: 1.6 }, still: true, camera: true, radio: 1200, score: 400 },
  };
  TD.makeUnit = function (type, x, y, o) {
    const T = ET[type];
    const u = Object.assign({
      type, x, y, r: T.r, a: 0, look: 0, hp: T.hp, max: T.hp, vis: Object.assign({}, T.vis), mode: 'patrol', aware: 0, goal: null,
      wp: null, wi: 0, pause: 0, scan: 0, fireCd: M.rnd(0.5, T.cd || 1), fireWarn: 0, flash: 0, dead: false, radio: T.radio, stunned: 0,
    }, o || {});
    u.look = u.a; u.base = u.a;
    return u;
  };

  function drive(u, tx, ty, spd, G, reverse) {
    let ax = tx - u.x, ay = ty - u.y;
    if (W.rayBlock(u.x, u.y, tx, ty)) { const s = TD.Nav.step(TD.Nav.field(tx, ty, G.t / 60), u.x, u.y); if (s) { ax = s[0]; ay = s[1]; } }
    if (Math.hypot(ax, ay) < 2) return true;
    const want = M.angTo(0, 0, ax, ay);
    if (reverse) { const back = M.wrap(want + Math.PI); u.a = M.turnTo(u.a, back, 0.05); const [fx, fy] = M.fwd(u.a); u.x -= fx * spd * 0.7; u.y -= fy * spd * 0.7; }
    else {
      u.a = M.turnTo(u.a, want, 0.06);
      const d = Math.abs(M.wrap(want - u.a));
      if (d < 0.6) { const [fx, fy] = M.fwd(u.a); u.x += fx * spd * (1 - d); u.y += fy * spd * (1 - d); }
    }
    return false;
  }
  function enemyFire(u, G) {
    const T = ET[u.type], gun = T.gun, [fx, fy] = M.fwd(u.look), mx = u.x + fx * 24, my = u.y + fy * 24;
    const E = (o) => { o.t = 0; G.eshots.push(o); };
    if (gun === 'burst') { u.burst = 3 + (u.type === 'turret' ? 2 : 0); u.burstT = 0; return; }
    if (gun === 'shell') { E({ k: 'shell', x: mx, y: my, vx: fx * 5.6, vy: fy * 5.6, a: u.look, dmg: 2, life: 80, r: 5 }); A.play('eshot'); }
    if (gun === 'twin') for (const s of [-1, 1]) { const [px, py] = M.fwd(u.look + Math.PI / 2); E({ k: 'shell', x: mx + px * s * 9, y: my + py * s * 9, vx: fx * 5.2, vy: fy * 5.2, a: u.look, dmg: 2, life: 85, r: 6 }); A.play('eshot'); }
    if (gun === 'snipe') { E({ k: 'snipe', x: mx, y: my, vx: fx * 9.5, vy: fy * 9.5, a: u.look, dmg: 3, life: 45, r: 4 }); A.play('laser', 0.7); }
    if (gun === 'rocket') for (const d of [-0.22, 0, 0.22]) { const a = u.look + d, f = M.fwd(a); E({ k: 'missile', x: mx, y: my, vx: f[0] * 3.2, vy: f[1] * 3.2, a, dmg: 2, life: 120, r: 5, homing: 35, turn: 0.025, shootable: true }); }
    FX.flash(mx, my, u.look, 0.18);
    TD.Stealth.noise(u.x, u.y, 160, 0.2, G.units.filter(o => o !== u));
  }
  TD.unitTick = function (u, G, dt) {
    if (u.dead) return;
    const T = ET[u.type], p = G.player;
    u.flash = Math.max(0, u.flash - dt);
    if (u.stunned > 0) { u.stunned -= dt; return; }
    const d = M.dist(u.x, u.y, p.x, p.y), toP = M.angTo(u.x, u.y, p.x, p.y);
    // burst fire in progress
    if (u.burst > 0 && (u.burstT -= dt) <= 0) {
      u.burst--; u.burstT = 0.09; const a = u.look + M.rnd(-0.06, 0.06), [fx, fy] = M.fwd(a);
      G.eshots.push({ k: 'mg', x: u.x + fx * 22, y: u.y + fy * 22, vx: fx * 4.6, vy: fy * 4.6, a, dmg: 1, life: 80, r: 4, t: 0 }); A.play('eshot', 0.6);
    }
    if (T.camera) {   // a camera only ever sweeps; spotting you is its whole job
      u.scan += dt * 0.55; u.look = u.base + Math.sin(u.scan) * 0.85;
      if (u.mode === 'alert' && !u.sees) { u.mode = 'search'; }
      if (TD.Stealth.phase === 'SNEAK') u.mode = 'patrol';
      return;
    }
    if (T.still) {   // a turret: sweep while calm, track and shoot when it knows
      if (u.mode === 'alert' && u.sees) { u.look = M.turnTo(u.look, toP, 0.045); }
      else if (u.mode === 'suspect' && u.goal) u.look = M.turnTo(u.look, M.angTo(u.x, u.y, u.goal.x, u.goal.y), 0.03);
      else { u.scan += dt * 0.5; u.look = M.turnTo(u.look, u.base + Math.sin(u.scan) * 0.6, 0.03); }
      u.a = u.look;
      if (u.mode === 'alert' && u.sees && (u.fireCd -= dt) <= 0 && Math.abs(M.wrap(toP - u.look)) < 0.15) { enemyFire(u, G); u.fireCd = T.cd; }
      return;
    }
    const spd = T.speed * (TD.Stealth.phase === 'CAUTION' ? 1.15 : 1);
    if (u.mode === 'patrol') {
      if (u.wp && u.wp.length) {
        if (u.pause > 0) { u.pause -= dt; u.scan += dt * 1.6; u.look = u.a + Math.sin(u.scan) * 0.7; }
        else {
          const w = u.wp[u.wi];
          if (drive(u, w[0], w[1], spd * 0.75, G) || M.dist(u.x, u.y, w[0], w[1]) < 14) { u.wi = (u.wi + 1) % u.wp.length; u.pause = M.rnd(0.8, 2.0); }
          u.look = M.turnTo(u.look, u.a, 0.08);
        }
      } else { u.scan += dt * 0.6; u.look = u.base + Math.sin(u.scan) * 0.7; u.a = M.turnTo(u.a, u.look, 0.04); }
    } else if (u.mode === 'suspect') {
      u.suspectT -= dt;
      if (u.goal) {
        const gd = M.dist(u.x, u.y, u.goal.x, u.goal.y), ga = M.angTo(u.x, u.y, u.goal.x, u.goal.y);
        if (gd > 70) { drive(u, u.goal.x, u.goal.y, spd * 0.7, G); u.look = M.turnTo(u.look, ga, 0.06); }
        else { u.scan += dt * 2; u.look = ga + Math.sin(u.scan) * 0.8; }
      }
      if (u.suspectT <= 0 && !u.sees) { u.mode = 'patrol'; u.aware = Math.min(u.aware, 0.2); }
    } else if (u.mode === 'alert') {
      const tgt = u.goal || TD.Stealth.lastKnown;
      if (u.sees) {
        const [lo, hi] = T.prefer;
        if (d > hi) drive(u, p.x, p.y, spd, G);
        else if (d < lo) drive(u, p.x, p.y, spd, G, true);
        u.a = M.turnTo(u.a, toP, 0.05); u.look = u.a;
        if (u.fireWarn > 0) { if ((u.fireWarn -= dt) <= 0) { enemyFire(u, G); u.fireCd = T.cd * M.rnd(0.85, 1.15); } }
        else if ((u.fireCd -= dt) <= 0 && Math.abs(M.wrap(toP - u.look)) < 0.14 && !W.rayBlock(u.x, u.y, p.x, p.y)) {
          if (T.warn) u.fireWarn = T.warn; else { enemyFire(u, G); u.fireCd = T.cd * M.rnd(0.85, 1.15); }
        }
      } else if (tgt) { drive(u, tgt.x, tgt.y, spd, G); u.look = M.turnTo(u.look, u.a, 0.08); }
    } else if (u.mode === 'search') {
      u.searchT = (u.searchT || 0) + dt;
      if (u.goal && (drive(u, u.goal.x, u.goal.y, spd * 0.85, G) || M.dist(u.x, u.y, u.goal.x, u.goal.y) < 30 || u.searchT > 4)) {
        const L = TD.Stealth.lastKnown; u.goal = { x: L.x + M.rnd(-150, 150), y: L.y + M.rnd(-150, 150) }; u.searchT = 0;
      }
      u.scan += dt * 1.8; u.look = u.a + Math.sin(u.scan) * 0.9;
    }
    for (const q of G.props) if (!q.dead) pushOut(u, q);
    for (const o of G.units) if (o !== u && !o.dead) { const dx = u.x - o.x, dy = u.y - o.y, dd = Math.hypot(dx, dy), m = u.r + o.r; if (dd < m && dd > 0.1) { u.x += dx / dd * (m - dd) * 0.5; u.y += dy / dd * (m - dd) * 0.5; } }
    W.collide(u, u.r, false);
    // contact with the player tank
    if (M.dist(u.x, u.y, p.x, p.y) < u.r + p.r) TD.pushOut(p, u);
  };
  TD.drawUnit = function (ctx, u) {
    if (u.dead) return;
    const T = ET[u.type];
    if (T.foot) { TD.drawRobot(ctx, u, T.foot); return; }
    if (T.mod) { TD.drawModTank(ctx, u, T.mod, T.ds); return; }
    if (T.still) {
      // the plates are authored facing north, the fire frame facing east; a=0 faces south here
      const firing = T.fire && u.burst > 0, key = firing ? T.fire : T.hurt && u.hp < u.max * 0.5 ? T.hurt : T.art;
      const a = u.look + (firing ? Math.PI / 2 : Math.PI), s = T.ds || 0.42;
      ART.draw(ctx, key, u.x + 3, u.y + 5, { a, s, tint: '#000000', alpha: 0.3 });
      ART.draw(ctx, key, u.x, u.y, { a, s, flash: u.flash > 0 ? 1 : 0 });
    } else if (T.et) drawAlienTank(ctx, u, T);
    else drawTank(ctx, u, T.art);
    if (u.fireWarn > 0) { const [fx, fy] = M.fwd(u.look); ART.draw(ctx, 'tank_charge_' + Math.min(3, Math.floor((1 - u.fireWarn) * 4)), u.x + fx * 26, u.y + fy * 26, { s: 0.2 }); }
  };

  // ------------------------------------------------------------------ damage
  TD.hitUnit = function (G, u, dmg, x, y, silent) {
    if (u.dead) return;
    let sneak = false;
    if (u.mode === 'patrol' && !silent) { dmg *= 2; sneak = true; }
    u.hp -= dmg; u.flash = 0.12;
    if (!silent && u.mode !== 'alert') { u.mode = 'suspect'; u.aware = Math.max(u.aware, 0.75); u.goal = { x: G.player.x, y: G.player.y }; u.suspectT = 5; }
    if (u.hp <= 0) {
      u.dead = true; G.kills++; G.score += ET[u.type].score * (sneak ? 2 : 1);
      if (ET[u.type].et) FX.boom(u.x, u.y, 150, 'gfx_destruction_', 6); else FX.boom(u.x, u.y, 110, 'nxp_dense_'); FX.debris(u.x, u.y, 0.35); FX.ring(u.x, u.y, 0.5, 'rzb_sonic_ring'); FX.smoke(u.x, u.y, 0.3, 1.6);
      Cam.kick(5); A.play('expB');
      const T = ET[u.type];
      G.wrecks.push({ x: u.x, y: u.y, a: T.foot ? -Math.PI : u.a, art: T.mod ? 'wm_tank_' + T.mod + '_wreck' : T.et ? 'et_' + T.et + '_wreck' : T.wreck || T.art, still: T.still || !!T.et || !!T.mod || !!T.foot, s: T.mod ? T.ds * 256 / 192 : T.ds });
      TD.Stealth.noise(u.x, u.y, 300, 0.5, G.units);
      if (sneak) G.say('SNEAK KILL x2', u);
      if (Math.random() < 0.22) TD.dropPickup(G, u.x, u.y);
    } else if (sneak) G.say('SNEAK STRIKE', u);
  };

  // ------------------------------------------------------------------ props
  const PROP = TD.PROP = {   // 1009: a mission may register its own kinds (draw / onBreak / broken)
    barrel: { key: 'nef_s1_fuel_barrel_', hp: 3, r: 13, s: 0.16 },
    crate: { key: 'gp_ammo_crate_', hp: 4, r: 15, s: 0.5 },
    pbox: { key: 'gp_weapon_crate_', hp: 2, r: 13, s: 0.44 },
  };
  TD.makeProp = (kind, x, y, drop) => ({ kind, x, y, r: PROP[kind].r, hp: PROP[kind].hp, max: PROP[kind].hp, drop, dead: false, flash: 0 });
  TD.hitProp = function (G, q, dmg) {
    if (q.dead) return;
    q.hp -= dmg; q.flash = 0.1;
    if (q.hp > 0) return;
    q.dead = true;
    if (PROP[q.kind].onBreak) { PROP[q.kind].onBreak(G, q); return; }
    if (q.kind === 'barrel') {
      FX.boom(q.x, q.y, 120, 'nxp_dense_'); FX.ring(q.x, q.y, 0.6); A.play('expB'); Cam.kick(6);
      TD.blast(G, q.x, q.y, 64, 5, true);
    } else { FX.boom(q.x, q.y, 50, 'nxp_clus_'); FX.debris(q.x, q.y, 0.22); A.play('expS'); TD.dropPickup(G, q.x, q.y, q.drop); }
  };
  TD.drawProp = function (ctx, q) {
    const P = PROP[q.kind];
    if (P.draw) { P.draw(ctx, q); return; }
    if (q.dead) return;
    const st = q.hp > q.max * 0.66 ? 'intact' : q.hp > q.max * 0.33 ? 'damaged' : 'critical';
    const key = P.still ? P.key : P.key + st;
    ART.draw(ctx, key, q.x + 3, q.y + 4, { s: P.s, tint: '#000000', alpha: 0.3 });
    ART.draw(ctx, key, q.x, q.y, { s: P.s, flash: q.flash > 0 ? 1 : 0 });
  };
  // area damage (shell splash, barrels, the boss): hurts units, props, and - if hurtsPlayer - you
  TD.blast = function (G, x, y, r, dmg, hurtsPlayer) {
    for (const u of G.units) if (!u.dead && M.dist(x, y, u.x, u.y) < r + u.r) TD.hitUnit(G, u, dmg * (1 - 0.5 * M.dist(x, y, u.x, u.y) / (r + u.r)), x, y);
    for (const q of G.props) if (!q.dead && M.dist(x, y, q.x, q.y) < r + q.r) TD.hitProp(G, q, dmg);
    if (G.boss) G.boss.blast(x, y, r, dmg);
    TD.blastStructures(G, x, y, r, dmg);
    if (hurtsPlayer && M.dist(x, y, G.player.x, G.player.y) < r + G.player.r) TD.hurtPlayer(G, Math.ceil(dmg / 2), x, y);
  };

  // ------------------------------------------------------------------ pickups
  TD.dropPickup = function (G, x, y, kind) {
    if (G.player.onfoot) return TD.footDrop(G, x, y, kind);
    if (!kind) { const r = Math.random(); kind = r < 0.38 ? 'repair' : r < 0.55 ? 'smoke' : r < 0.9 ? ['vulcan', 'crash', 'laser', 'homing'][(Math.random() * 4) | 0] : 'score'; }
    G.pickups.push({ kind, x, y, t: 0 });
  };
  TD.pickupTick = function (G, dt) {
    if (G.player.onfoot) return TD.footPickups(G, dt);
    const p = G.player;
    for (const k of G.pickups) {
      k.t += dt;
      if (!p.dead && M.dist(k.x, k.y, p.x, p.y) < p.r + 14) {
        k.dead = true; A.play('pick');
        if (WPN[k.kind]) {
          const have = p.weapons.find(w => w.id === k.kind);
          if (have) { have.lv = Math.min(3, have.lv + 1); p.wi = p.weapons.indexOf(have); }
          else if (p.weapons.length < 4) { p.weapons.push({ id: k.kind, lv: 1 }); p.wi = p.weapons.length - 1; }
          else { p.weapons[p.wi] = { id: k.kind, lv: 1 }; }
          G.say(WPN[k.kind].name + ' LV' + p.weapons[p.wi].lv, p);
        } else if (k.kind === 'repair') { p.hp = Math.min(p.max, p.hp + 4); G.say('ARMOR +4', p); }
        else if (k.kind === 'smoke') { p.smoke = Math.min(5, p.smoke + 2); G.say('SMOKE +2', p); }
        else if (k.kind === 'life') { G.lives++; G.say('1UP', p); }
        else { G.score += 1000; G.say('+1000', p); }
      }
    }
    G.pickups = G.pickups.filter(k => !k.dead && k.t < 14);
  };
  TD.drawPickup = function (ctx, k, t) {
    const bob = Math.sin(t * 4 + k.x) * 2, blink = k.t > 11 && Math.floor(k.t * 8) % 2;
    if (blink) return;
    if (WPN[k.kind]) ART.draw(ctx, TD.iconFor(k.kind, 1), k.x, k.y + bob, { s: 0.36 });
    else if (k.kind === 'repair') ART.draw(ctx, 'crate6_0', k.x, k.y + bob, { s: 0.42 });
    else if (k.kind === 'smoke') ART.draw(ctx, 'missilecrate', k.x, k.y + bob, { s: 0.3 });
    else if (k.kind === 'life') ART.draw(ctx, 'life_up', k.x, k.y + bob, { s: 0.3 });
    else ART.draw(ctx, 'score_1000', k.x, k.y + bob, { s: 0.3 });
  };

  // ------------------------------------------------------------------ projectiles
  const PELLET = (fam, age) => 'mfx_mg_' + fam + '_' + Math.min(4, (age / 3) | 0);
  TD.shotTick = function (G) {
    const p = G.player;
    for (const s of G.shots) {
      s.t++;
      if (s.homing) {
        let best = null, bd = 360;
        const consider = u => { const d = M.dist(s.x, s.y, u.x, u.y);
          if (d < bd && Math.abs(M.wrap(M.angTo(s.x, s.y, u.x, u.y) - s.a)) < 1.35 && !W.rayBlock(s.x, s.y, u.x, u.y)) { bd = d; best = u; } };
        for (const u of G.units) if (!u.dead && u.vis) consider(u);
        if (G.boss && G.boss.alive()) { const b = G.boss.aim(s.x, s.y); if (b) consider(b); }
        if (best && s.t > 8) { s.a = M.turnTo(s.a, M.angTo(s.x, s.y, best.x, best.y), 0.09); }
        const sp = Math.min(7.5, Math.hypot(s.vx, s.vy) + 0.18), [fx, fy] = M.fwd(s.a); s.vx = fx * sp; s.vy = fy * sp;
        if (s.t % 3 === 0) FX.smoke(s.x - fx * 10, s.y - fy * 10, 0.05, 0.35);
      }
      const sx = s.x, sy = s.y; s.x += s.vx; s.y += s.vy;
      if (TD.structureImpact(G, s, sx, sy, s.x, s.y)) { endShot(G, s); continue; }
      if (--s.life <= 0 || W.solidAt(s.x, s.y)) { endShot(G, s); continue; }
      for (const u of G.units) {
        if (u.dead || (s.hit && s.hit.has(u))) continue;
        if (M.dist(s.x, s.y, u.x, u.y) < u.r + s.r) {
          TD.hitUnit(G, u, s.dmg, s.x, s.y); A.play('hit', 0.6); FX.boom(s.x, s.y, 26, 'nxp_clus_');
          if (s.pierce > 0) { s.pierce--; (s.hit = s.hit || new Set()).add(u); } else { endShot(G, s); break; }
        }
      }
      if (s.dead) continue;
      for (const q of G.props) if (!q.dead && M.dist(s.x, s.y, q.x, q.y) < q.r + s.r) { TD.hitProp(G, q, s.dmg); endShot(G, s); break; }
      if (s.dead) continue;
      if (G.boss && G.boss.alive()) { const hit = G.boss.hit(s.x, s.y, s.r, s.dmg, s); if (hit) { FX.boom(s.x, s.y, 30, 'nxp_clus_'); A.play('hit', 0.6); if (s.pierce > 0) s.pierce--; else endShot(G, s); } }
      // a player round can shoot down a boss missile
      if (!s.dead) for (const e of G.eshots) if (e.shootable && !e.dead && M.dist(s.x, s.y, e.x, e.y) < e.r + s.r + 2) { e.dead = true; FX.boom(e.x, e.y, 50, 'nxp_clus_'); A.play('expS'); G.score += 100; endShot(G, s); break; }
    }
    G.shots = G.shots.filter(s => !s.dead);
    for (const e of G.eshots) {
      e.t++;
      if (e.homing && e.t < e.homing) { const target=e.target&&!e.target.dead?e.target:p;e.a = M.turnTo(e.a, M.angTo(e.x, e.y, target.x, target.y), e.turn || 0.05); const sp = Math.hypot(e.vx, e.vy), [fx, fy] = M.fwd(e.a); e.vx = fx * sp; e.vy = fy * sp; }
      if (e.accel) { const sp = Math.min(e.max || 8, Math.hypot(e.vx, e.vy) + e.accel), [fx, fy] = M.fwd(e.a); e.vx = fx * sp; e.vy = fy * sp; if (e.t % 3 === 0) FX.smoke(e.x - fx * 12, e.y - fy * 12, 0.06, 0.4); }
      const ex = e.x, ey = e.y; e.x += e.vx; e.y += e.vy;
      if (TD.structureImpact(G, e, ex, ey, e.x, e.y)) { e.dead = true; continue; }
      if (--e.life <= 0 || (!e.over && W.solidAt(e.x, e.y))) { e.dead = true; if (e.r > 5) FX.boom(e.x, e.y, 40, 'nxp_clus_'); continue; }
      if (!p.dead && M.dist(e.x, e.y, p.x, p.y) < p.r * 0.75 + e.r) { e.dead = true; TD.hurtPlayer(G, e.dmg, e.x, e.y); continue; }
      if (G.ally && !G.ally.dead && M.dist(e.x, e.y, G.ally.x, G.ally.y) < G.ally.r + e.r) { e.dead = true; TD.hurtAlly(G, e.dmg); continue; }
      for (const q of G.props) if (!q.dead && M.dist(e.x, e.y, q.x, q.y) < q.r + e.r) { e.dead = true; TD.hitProp(G, q, e.dmg); break; }
    }
    G.eshots = G.eshots.filter(e => !e.dead);
  };
  function endShot(G, s) {
    s.dead = true;
    if(s.napalm){(G.burns=G.burns||[]).push({x:s.x,y:s.y,t:0,next:.4});}
    if (s.splash) {
      FX.boom(s.x, s.y, s.big ? 140 : 70, s.big ? 'nxp_dense_' : 'nxp_clus_'); FX.boom(s.x, s.y, s.big ? 120 : 80, 'gfx_impact_', 6); if (s.big) FX.ring(s.x, s.y, 0.6);
      A.play(s.big ? 'expB' : 'expS'); TD.blast(G, s.x, s.y, s.splash, s.sdmg || 2, false);
    }
  }
  const EGL = [1, 3, 4, 5, 6, 7];   // eglaser_2 is not registered
  TD.drawShot = function (ctx, s, enemy) {
    if (enemy) {
      if (s.k === 'missile') { ART.draw(ctx, 'tank_missile_' + ((s.t / 3 | 0) % 4), s.x, s.y, { a: s.a + Math.PI, s: 0.22 }); return; }
      if (s.k === 'laser' || s.k === 'snipe') { ART.draw(ctx, 'tank_laser_crimson', s.x, s.y, { a: s.a + Math.PI, s: 0.28 }); return; }
      if (s.k === 'sonic') { ART.draw(ctx, 'rzb_sonic_bullet', s.x, s.y, { a: s.a, s: 0.16, comp: 'lighter' }); return; }
      if (s.k === 'wave') { ART.draw(ctx, 'rzb_sonic_wave', s.x, s.y, { a: s.a, s: 0.3, alpha: 0.9, comp: 'lighter' }); return; }
      const fam = s.k === 'snipe' ? 4 : 0, sc = s.k === 'shell' ? 0.42 : s.k === 'snipe' ? 0.4 : 0.32;
      ART.draw(ctx, PELLET(fam, s.t), s.x, s.y, { a: s.a, s: sc }); return;
    }
    if (s.k === 'vulcan') ART.draw(ctx, PELLET(2, s.t), s.x, s.y, { a: s.a, s: 0.34 });
    else if (s.k === 'shell') ART.draw(ctx, s.big ? 'tank_ap' : 'gfx_shell', s.x, s.y, { a: s.a + Math.PI, s: s.big ? 0.26 : 0.55 });
    else if (s.k === 'crash') ART.draw(ctx, 'nex_fireball_' + ((s.t / 3 | 0) % 4), s.x, s.y, { a: s.t * 0.3, s: 0.32 });
    else if (s.k === 'laser') ART.draw(ctx, 'tank_laser_' + ['gold', 'silver', 'crimson'][(s.lv || 1) - 1], s.x, s.y, { a: s.a + Math.PI, s: 0.3 });
    else if (s.k === 'homing') ART.draw(ctx, 'tank_missile_' + ((s.t / 3 | 0) % 4), s.x, s.y, { a: s.a + Math.PI, s: 0.21 });
  };
}(window));
