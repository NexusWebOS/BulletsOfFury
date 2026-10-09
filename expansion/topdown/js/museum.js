/*
 * LEVEL 5 - MUSEUM OF VIOLENCE. One on-foot mission built from four studied games plus the MGS layer:
 *
 *   MERCS            push-scroll that never scrolls back (the branch you take is committed), MEGA CRASH bombs
 *                    (A+B together, or G) with a limited stock, POW raises the gun in hand, and a vehicle
 *                    you climb into: the exhibit Fury tank has its own armour and ejects you when it dies.
 *   DEMOLITION MAN   (stage 2, the museum) an overhead Smash-TV room that locks until its waves are dead,
 *                    exhibits you shoot open for power-ups, and hostages you must not shoot.
 *   CONTRA HARD CORPS four carried guns (A-D), death costs only the gun in your hand, a branching route,
 *                    and a boss that is broken apart part by part (boss_exhibit.js).
 *   METAL GEAR       cones, CAUTION/ALERT/EVASION, cameras, laser tripwires you crawl under, alarm panels
 *                    that are the only source of reinforcements, a crawl duct, CQC from behind, and bodies
 *                    that other guards find.
 *
 * Nothing here is cartridge code: these are original systems written for this engine from the games'
 * published behaviour (docs/MUSEUM_STUDY_1009.md lists what came from where).
 */
(function (root) {
  'use strict';
  const TD = root.TD, M = TD.M, W = TD.World, FX = TD.FX, I = TD.Input, A = TD.Audio, S = TD.Stealth, Cam = TD.Cam;
  const L5 = root.TD_LEVEL5, P5 = root.TD_LEVEL5_PLACE, MART = root.TD_MUSEUM_ART || {};
  const CA = root.TD_CAMPAIGN_ART, FR = CA.frames, SEQ = CA.sequences;
  const VW = TD.VW, VH = TD.VH, PI = Math.PI, MID = 5;
  const MX = TD.MUSEUM = { log: [] };

  // ------------------------------------------------------------------ helpers
  function anim(key, time, loop) {
    const q = SEQ[key]; if (!q) return null;
    const f = Math.floor(time * (q.fps || 9));
    return q.frames[loop === false ? Math.min(f, q.frames.length - 1) : f % q.frames.length];
  }
  function frame(ctx, key, x, y, o) {
    if (!key) return; const m = FR[key];
    ART.draw(ctx, key, x, y, Object.assign({ ax: m ? m.anchor[0] : 48, ay: m ? m.anchor[1] : 48 }, o));
  }
  function label(ctx, s, x, y, size, col) {
    ctx.font = 'bold ' + size + 'px BOFCommand, "Arial Black", monospace'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.lineWidth = Math.max(2, size / 5); ctx.strokeStyle = '#000'; ctx.strokeText(s, x, y); ctx.fillStyle = col || '#fff'; ctx.fillText(s, x, y);
  }
  function segCirc(ax, ay, bx, by, cx, cy, r) {
    const dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy || 1, t = M.clamp(((cx - ax) * dx + (cy - ay) * dy) / l2, 0, 1);
    return Math.hypot(ax + dx * t - cx, ay + dy * t - cy) < r;
  }
  const inView = (o, m) => o.x > Cam.x - m && o.x < Cam.x + VW / Cam.zoom + m && o.y > Cam.y - m && o.y < Cam.y + VH / Cam.zoom + m;
  const footType = u => !!(TD.ET[u.type] && TD.ET[u.type].foot);
  function ringRects() {
    const R = L5.ring, out = [];
    for (let i = 0; i < 64; i++) {
      const a = i / 64 * PI * 2; if (R.doors.some(([c, w]) => Math.abs(M.wrap(a - c)) < w)) continue;
      const x = R.x + Math.cos(a) * R.r, y = R.y + Math.sin(a) * R.r, h = R.t / 2; out.push([x - h, y - h, x + h, y + h, 'b']);
    }
    return out;
  }
  // a beam drawn from authored laser art: the bolt is authored vertical, so it is turned onto the segment
  // and drawn in short pieces so a long curtain is not one smeared bolt
  function beam(ctx, ax, ay, bx, by, t, alpha) {
    const len = Math.hypot(bx - ax, by - ay), n = Math.max(1, Math.ceil(len / 52)), a = M.angTo(ax, ay, bx, by);
    const flick = (alpha || 1) * (0.7 + 0.3 * Math.sin(t * 31 + ax));
    for (let i = 0; i < n; i++) {
      const q = (i + 0.5) / n;
      ART.draw(ctx, 'tank_laser_crimson', M.lerp(ax, bx, q), M.lerp(ay, by, q), { a, sx: 0.32, sy: len / n / 104, alpha: flick, comp: 'lighter' });
    }
  }

  // ------------------------------------------------------------------ exhibits (Demolition Man: shoot the art)
  const EX = {
    statue: { hp: 6, r: 17, s: 0.42, noise: 220 }, vase: { hp: 2, r: 12, s: 0.36, noise: 150 }, painting: { hp: 3, r: 15, s: 0.36, noise: 120 },
    rifle_case: { hp: 3, r: 17, s: 0.40, noise: 260 }, plasma_case: { hp: 4, r: 17, s: 0.40, noise: 260 },
    alarm: { hp: 3, r: 10, s: 0.32, noise: 200 }, laser_post: { hp: 2, r: 6, s: 0.36, noise: 90 }, rope: { hp: 1, r: 12, s: 0.32, noise: 40 },
  };
  const LENS = [43, 36];                    // measured: the post's lens centre in mx_laser_post
  function drawExhibit(ctx, q) {
    const E = EX[q.kind.slice(3)], key = q.kind + (q.dead ? '_broken' : ''), m = MART[key];
    const o = { s: E.s, ax: m ? m.anchor[0] : null, ay: m ? m.anchor[1] : null };
    ART.draw(ctx, key, q.x + 3, q.y + 3, Object.assign({}, o, { tint: '#000000', alpha: 0.28 }));
    ART.draw(ctx, key, q.x, q.y, Object.assign({}, o, { flash: q.flash > 0 && !q.dead ? 1 : 0 }));
  }
  function breakExhibit(G, q) {
    const kind = q.kind.slice(3), E = EX[kind];
    FX.boom(q.x, q.y - 10, kind === 'statue' ? 90 : 55, kind.includes('case') ? 'gfx_impact_' : 'nxp_clus_', kind.includes('case') ? 6 : 8);
    FX.debris(q.x, q.y - 6, 0.22); A.play(kind === 'statue' ? 'expB' : 'expS', 0.7);
    S.noise(q.x, q.y, E.noise, 0.45, G.units);
    G.exhibits = (G.exhibits || 0) + 1; G.score += 250;
    if (q.drop) TD.dropPickup(G, q.x, q.y + 10, q.drop);
    if (kind === 'alarm') G.say('ALARM PANEL DOWN', q);
    if (kind === 'laser_post') G.say('LASER OFF', q);
  }
  for (const k in EX) TD.PROP['mx_' + k] = { key: 'mx_' + k, hp: EX[k].hp, r: EX[k].r, s: EX[k].s, draw: drawExhibit, onBreak: breakExhibit };

  // ------------------------------------------------------------------ setup
  function setup(G, DATA) {
    Object.assign(G, {
      crash: 3, crashT: 0, rescued: 0, hostagesLost: 0, exhibits: 0, bodies: [], lasers: [], tripCd: 0, routeT: 0,
      pushY: 1e9, inVehicle: false, footSave: null, boardCd: 0, cqc: null,
      arena: { state: 'idle', wave: 0, next: 0, rects: [] },
      hostages: P5.hostages.map(h => Object.assign({ state: 'bound', t: 0 }, h)),
      vehicle: Object.assign({ max: P5.vehicle.hp, parked: true, dead: false }, P5.vehicle),
    });
    G.player.slots4 = true; W.navR = 9;   // infantry clearance, so the gallery's lanes exist for the guards' pathing
    // radio range per guard (MGS: a guard calls the guards near him, not the whole building)
    DATA.units.forEach((pl, i) => { const u = G.units[i]; if (u) u.radio = u.type === 'camera' ? 520 : pl.radio; });
    for (const L of P5.lasers) {
      const a = TD.makeProp('mx_laser_post', L.x, L.y), b = TD.makeProp('mx_laser_post', L.x2, L.y2);
      G.props.push(a, b); G.lasers.push({ a, b });
    }
    if (!G._museumHooks) {   // the tank ejects you instead of costing a life (Mercs); installed once, gated on the mission
      G._museumHooks = true;
      const died = G.playerDied;
      G.playerDied = function () { if (this.mission === MID && this.inVehicle) { eject(this, true); return; } return died.apply(this, arguments); };
    }
    MX.log.length = 0;
  }

  // ------------------------------------------------------------------ the vehicle (Mercs)
  function board(G) {
    const f = G.player, v = G.vehicle, t = TD.makePlayer(v.x, v.y);
    Object.assign(t, { pilot: v.pilot, a: v.a, aim: v.a, hp: v.hp, max: v.max, inv: 30, smoke: 2, vehicle: true,
      weapons: [{ id: 'vulcan', lv: 2 }, { id: 'homing', lv: 1 }], wi: 0 });
    G.footSave = f; G.player = t; G.inVehicle = true; v.parked = false;
    A.play('intro', 0.6); Cam.kick(4); G.say('FURY TANK MOUNTED', t); MX.log.push({ event: 'board', t: G.time });
  }
  function eject(G, destroyed) {
    const t = G.player, f = G.footSave, v = G.vehicle;
    const [sx, sy] = M.fwd(t.a + PI / 2);
    Object.assign(f, { x: t.x + sx * 30, y: t.y + sy * 30, dead: false, inv: destroyed ? 120 : 40, stance: 'stand', roll: 0, action: null, reload: 0, reloadGun: null });
    W.collide(f, f.r, false);
    G.player = f; G.inVehicle = false; G.footSave = null; G.boardCd = 1.4;
    if (destroyed) {
      v.dead = true; v.parked = false;
      FX.boom(t.x, t.y, 170, 'gfx_destruction_', 6); FX.ring(t.x, t.y, 0.9); FX.debris(t.x, t.y, 0.4); FX.smoke(t.x, t.y, 0.3, 1.8);
      Cam.kick(12); A.play('expB');
      G.wrecks.push({ x: t.x, y: t.y, a: t.a, art: 'pt_' + v.pilot + '_wreck', still: true, s: 0.5 });
      G.say('TANK DESTROYED - EJECT!', f);
    } else { Object.assign(v, { x: t.x, y: t.y, a: t.a, hp: t.hp, parked: true }); G.say('DISMOUNTED', f); }
    MX.log.push({ event: destroyed ? 'eject' : 'dismount', t: G.time });
  }

  // ------------------------------------------------------------------ MEGA CRASH (Mercs)
  function megaCrash(G) {
    if (!(G.crash > 0)) return false;
    G.crash--; G.crashT = 0.9; const p = G.player; p.inv = Math.max(p.inv || 0, 75);
    for (const u of G.units) if (!u.dead && inView(u, 10)) TD.hitUnit(G, u, 10, u.x, u.y);
    for (const q of G.props) if (!q.dead && inView(q, 0)) TD.hitProp(G, q, 3);
    for (const e of G.eshots) if (inView(e, 20)) { e.dead = true; FX.boom(e.x, e.y, 30, 'nxp_clus_'); }
    G.eshots = G.eshots.filter(e => !e.dead);
    if (G.boss && G.boss.alive()) G.boss.blast(G.boss.x, G.boss.y, 260, 14);
    for (let i = 0; i < 9; i++) FX.boom(Cam.x + M.rnd(40, VW - 40), Cam.y + M.rnd(40, VH - 40), M.rnd(90, 170), i % 2 ? 'nxp_dense_' : 'gfx_destruction_', i % 2 ? 8 : 6);
    FX.ring(p.x, p.y, 1.4); Cam.kick(14); A.play('whiteout');
    S.noise(p.x, p.y, 700, 1, G.units);
    G.say('MEGA CRASH!', p); MX.log.push({ event: 'crash', t: G.time, left: G.crash });
    return true;
  }

  // ------------------------------------------------------------------ CQC (MGS): a silent takedown from behind
  function cqcTarget(G) {
    const p = G.player; if (!p.onfoot || p.dead || p.action || p.roll > 0 || p.stance === 'prone') return null;
    let best = null, bd = 26;
    for (const u of G.units) {
      if (u.dead || !footType(u) || u.mode === 'alert') continue;
      const d = M.dist(u.x, u.y, p.x, p.y); if (d >= bd) continue;
      const behind = Math.abs(M.wrap(M.angTo(u.x, u.y, p.x, p.y) - u.look)) > 1.75;
      if (behind || u.stunned > 0) { best = u; bd = d; }
    }
    return best;
  }
  function cqcKill(G, u) {
    const T = TD.ET[u.type];
    u.dead = true; u.hp = 0; G.kills++; G.score += T.score * 2; G.cqcKills = (G.cqcKills || 0) + 1;
    FX.boom(u.x, u.y, 40, 'gfx_impact_', 6); A.play('hit', 0.8);
    G.wrecks.push({ x: u.x, y: u.y, a: -PI, art: T.wreck || T.art, still: true, s: T.ds });
    G.say('CQC TAKEDOWN', u); MX.log.push({ event: 'cqc', t: G.time, type: u.type });
  }

  // ------------------------------------------------------------------ the Smash-TV room
  function arenaTick(G, dt) {
    const R = G.arena, p = G.player;
    if (R.state === 'idle') {
      if (p.y < 1112 && p.y > 884) {
        R.state = 'locked'; R.next = 0.9; R.alertsBefore = S.alerts;
        R.rects = L5.curtains.map(c => W.add({ x0: Math.min(c[0], c[2]) - 2, y0: c[1] - 6, x1: Math.max(c[0], c[2]) + 2, y1: c[1] + 6, t: 'b' }));
        A.play('alert'); Cam.kick(5); G.say('HALL OF ARMS - ROOM LOCKED', { x: 400, y: 1010 }); MX.log.push({ event: 'lock', t: G.time });
      }
      return;
    }
    if (R.state !== 'locked') return;
    if (R.next > 0) {
      if ((R.next -= dt) <= 0) {
        for (const [type, x, y] of P5.waves[R.wave]) {
          const u = TD.makeUnit(type, x, y, { a: 0, arena: true, radio: 700 }); u.mode = 'alert'; u.aware = 1; u.goal = { x: p.x, y: p.y };
          G.units.push(u); FX.boom(x, y, 60, 'gfx_impact_', 6);
        }
        R.wave++; A.play('warn', 0.5); G.say('WAVE ' + R.wave + ' / ' + P5.waves.length, { x: 400, y: 960 });
      }
      return;
    }
    if (G.units.some(u => u.arena && !u.dead)) return;
    if (R.wave < P5.waves.length) { R.next = 1.1; return; }
    // cleared: the curtains drop, the room's alarm does not count against GHOST, the wings calm down
    R.state = 'clear'; for (const q of R.rects) W.remove(q); R.rects = [];
    S.alerts = R.alertsBefore; S.phase = 'CAUTION'; S.timer = 8;
    for (const u of G.units) if (!u.dead && !u.arena && u.mode !== 'patrol') { u.mode = 'patrol'; u.aware = 0.15; u.goal = null; u.heard = null; }   // the fight's noise does not linger
    G.score += 5000; G.routeT = 8; A.play('phase'); G.say('ROOM CLEAR +5000', { x: 400, y: 1000 }); MX.log.push({ event: 'clear', t: G.time });
  }

  // ------------------------------------------------------------------ per-frame
  function pre(G, dt) {
    const p = G.player;
    G.boardCd = Math.max(0, G.boardCd - dt); G.crashT = Math.max(0, G.crashT - dt); G.tripCd = Math.max(0, G.tripCd - dt);
    if (p.dead) return;
    // Mercs push-scroll: the screen never goes back, and neither do you
    const bottom = Cam.y + VH / Cam.zoom - 12; if (p.y > bottom) p.y = bottom;
    // MEGA CRASH: A+B together (Mercs' both-buttons bomb) or G. Swallow the buttons so B does not also reload.
    if (I.tap('crash') || (I.down('A') && I.tap('B')) || (I.tap('A') && I.down('B'))) {
      if (megaCrash(G)) { I.state.A = false; I.state.B = false; p.fireCd = Math.max(p.fireCd || 0, 12); }
    }
    if (p.onfoot) {
      G.cqc = cqcTarget(G);
      if (G.cqc && I.tap('A')) { cqcKill(G, G.cqc); G.cqc = null; I.state.A = false; p.fireCd = 18; }
      const v = G.vehicle;
      if (v.parked && !v.dead && G.boardCd <= 0 && p.stance !== 'prone' && M.dist(p.x, p.y, v.x, v.y) < 30) board(G);
    } else if (I.tap('exitVehicle')) eject(G, false);
    // a player round that reaches a hostage kills the hostage (Demolition Man)
    for (const s of G.shots) for (const h of G.hostages) if (h.state === 'bound' && M.dist(s.x, s.y, h.x, h.y) < 10) { s.life = 0; killHostage(G, h); }
  }
  function killHostage(G, h) {
    h.state = 'dead'; h.t = 0; G.hostagesLost++; G.score = Math.max(0, G.score - 5000);
    A.play('hit'); G.say('HOSTAGE DOWN -5000', h); MX.log.push({ event: 'hostageDown', t: G.time });
  }
  function tick(G, dt) {
    const p = G.player;
    if (p.onfoot && G.footSave) G.footSave = null;
    if (!p.onfoot && G.footSave) { G.footSave.x = p.x; G.footSave.y = p.y; }
    arenaTick(G, dt);
    G.routeT = Math.max(0, G.routeT - dt);
    // hostages: walk to them to free them; each hands over its reward
    for (const h of G.hostages) {
      h.t += dt;
      if (h.state === 'bound' && p.onfoot && !p.dead && M.dist(p.x, p.y, h.x, h.y) < 20) {
        h.state = 'freed'; h.t = 0; G.rescued++; G.score += 3000; A.play('pick');
        TD.footDrop(G, h.x + 14, h.y + 6, h.reward); G.say('RESCUED +3000', h); MX.log.push({ event: 'rescue', t: G.time });
      }
      if (h.state === 'freed' && h.t > 1.4) h.y += 1.1;
    }
    // laser tripwires: standing in a live beam raises the alarm; prone crawls under it
    for (const L of G.lasers) {
      L.on = !L.a.dead && !L.b.dead;
      if (!L.on || p.dead || G.tripCd > 0 || (p.onfoot && p.stance === 'prone')) continue;
      if (segCirc(L.a.x, L.a.y, L.b.x, L.b.y, p.x, p.y, p.r * 0.8)) {
        G.tripCd = 3; G.trips = (G.trips || 0) + 1; A.play('alert'); G.say('LASER TRIPPED!', p);
        S.raise({ x: (L.a.x + L.b.x) / 2, y: (L.a.y + L.b.y) / 2 }, p, G.units); MX.log.push({ event: 'trip', t: G.time });
      }
    }
    // bodies: a guard who sees a fallen guard investigates, and the museum goes to CAUTION
    for (const u of G.units) if (u.dead && !u.bodyMarked && footType(u)) { u.bodyMarked = true; G.bodies.push({ x: u.x, y: u.y, found: false }); }
    if (G.t % 6 === 0) for (const b of G.bodies) {
      if (b.found) continue;
      for (const u of G.units) {
        if (u.dead || !u.vis || u.type === 'camera' || u.mode === 'alert') continue;
        const d = M.dist(u.x, u.y, b.x, b.y);
        if (d > u.vis.range * 0.8 || d < 4 || Math.abs(M.wrap(M.angTo(u.x, u.y, b.x, b.y) - u.look)) > u.vis.half || !W.los(u.x, u.y, b.x, b.y)) continue;
        b.found = true; u.mode = 'suspect'; u.goal = { x: b.x, y: b.y }; u.suspectT = 6; u.aware = Math.max(u.aware, 0.6);
        if (S.phase === 'SNEAK') { S.phase = 'CAUTION'; S.timer = S.T.CAUTION; }
        A.play('blip'); G.say('BODY FOUND', u); MX.log.push({ event: 'body', t: G.time }); break;
      }
    }
  }
  function cam(G) {
    G.pushY = Math.min(G.pushY, Cam.y);
    Cam.maxY = Math.min(L5.h, G.pushY + VH / Cam.zoom);
  }
  function canReinforce(G) {
    if (G.arena.state === 'locked') return false;
    // MGS: reinforcements are called by an alarm panel. Break the panels and nobody answers.
    return G.props.some(q => q.kind === 'mx_alarm' && !q.dead && Math.abs(q.y - G.player.y) < 520);
  }
  function respawn(G, p, fresh) {
    // Contra Hard Corps: you lose only the gun in your hand. Mercs: you come back where you fell.
    const held = p.weapons[p.wi];
    let keep = p.weapons.filter(w => w !== held || w.id === 'desert_eagle');
    if (!keep.some(w => w.id === 'desert_eagle')) keep.unshift({ id: 'desert_eagle', lv: 1, ammo: 12, reserve: 60 });
    keep = keep.slice(0, 4);
    if (held && held.id !== 'desert_eagle') G.say('LOST ' + TD.FOOT_GUNS[held.id].name, p);
    Object.assign(fresh, { x: p.x, y: p.y, weapons: keep, wi: 0, slots4: true, smoke: Math.max(3, p.smoke) });
    if (W.inType(fresh.x, fresh.y, 'd')) fresh.stance = 'prone'; else W.collide(fresh, fresh.r, false);
    G.crash = Math.max(G.crash, 2);
  }

  // ------------------------------------------------------------------ drawing
  // before it wakes, the exhibit stands on the grand hall's mosaic like any other piece in the museum
  const DORMANT = { x: 400, y: 150, a: 0, turret: 0, recoil: 0, charge: 0, travel: 0, flash: {}, parts: { gunL: 1, gunR: 1, podL: 1, podR: 1, turret: 1 }, max: { turret: 1 } };
  function dormantWorld(lx, ly) { return { x: DORMANT.x + lx * 0.4, y: DORMANT.y + ly * 0.4 }; }
  const DORMANT_PARTS = { gunL: () => dormantWorld(-57, 96), gunR: () => dormantWorld(57, 96), podL: () => dormantWorld(-105, 10), podR: () => dormantWorld(105, 10) };
  function drawFloor(ctx, G) {
    const t = G.t / 60, v = G.vehicle;
    if (!G.boss) TD.drawExhibitTank(ctx, DORMANT, t, dormantWorld, DORMANT_PARTS, (p, a, d) => { const [fx, fy] = M.fwd(a); return { x: p.x + fx * d, y: p.y + fy * d }; });
    if (v.parked && !v.dead) TD.drawPlayerTank(ctx, { pilot: v.pilot, x: v.x, y: v.y, a: v.a, aim: v.a, hp: v.hp, max: v.max });
    for (const h of G.hostages) {
      if (h.state === 'freed' && h.t > 2.6) continue;
      let key;
      if (h.state === 'bound') key = anim('of_' + h.body + '_stun', t + h.x, true);
      else if (h.state === 'freed') key = h.t < 0.5 ? anim('of_' + h.body + '_recovery', h.t, false) : anim('of_' + h.body + '_powerup', h.t - 0.5, true);
      else key = anim('of_' + h.body + '_death', 9, false);
      const alpha = h.state === 'freed' ? M.clamp((2.6 - h.t) / 0.8, 0, 1) : 1;
      frame(ctx, key, h.x + 2, h.y + 3, { s: 0.7, tint: '#000', alpha: 0.3 * alpha });
      frame(ctx, key, h.x, h.y, { s: 0.7, alpha });
    }
    // live beams sit at the emitters' lens height
    for (const L of G.lasers) if (!L.a.dead && !L.b.dead) {
      const m = MART.mx_laser_post, s = EX.laser_post.s, ox = (LENS[0] - m.anchor[0]) * s, oy = (LENS[1] - m.anchor[1]) * s;
      beam(ctx, L.a.x + ox, L.a.y + oy, L.b.x + ox, L.b.y + oy, t, 0.95);
    }
    if (G.arena.state === 'locked') for (const c of L5.curtains) beam(ctx, c[0], c[1] - 10, c[2], c[3] - 10, t, 1);
  }
  function drawOver(ctx, G) {
    const t = G.t / 60, p = G.player;
    for (const h of G.hostages) if (h.state === 'bound' && Math.floor(t * 2 + h.x) % 2) label(ctx, 'HELP!', h.x, h.y - 30, 8, '#ffe066');
    if (G.cqc && Math.floor(t * 6) % 2) { ART.draw(ctx, 'pad_a', G.cqc.x - 12, G.cqc.y - 44, { s: 0.07 }); label(ctx, 'CQC', G.cqc.x + 8, G.cqc.y - 44, 8, '#7dffa0'); }
    const v = G.vehicle;
    if (p.onfoot && v.parked && !v.dead && M.dist(p.x, p.y, v.x, v.y) < 110) label(ctx, 'WALK IN TO BOARD', v.x, v.y - 42, 8, '#7deacc');
    if (G.routeT > 0 && Math.floor(t * 3) % 2) {
      label(ctx, 'WEST: GALLERY - STEALTH', 269, 820, 8, '#7dffa0');
      label(ctx, 'EAST: TANK HALL - ARMOR', 527, 805, 8, '#ff9a60');
      label(ctx, 'DUCT: PRONE ONLY', 400, 836, 8, '#9fe0ff');
    }
    if (G.crashT > 0) { ctx.save(); ctx.globalAlpha = Math.min(1, G.crashT / 0.5) * 0.85; ctx.fillStyle = '#fff6e0'; ctx.fillRect(Cam.x - 20, Cam.y - 20, VW / Cam.zoom + 40, VH / Cam.zoom + 40); ctx.restore(); }
  }
  function objective(G) {
    const R = G.arena, p = G.player;
    if (G.boss && G.boss.alive()) return G.boss.name;
    if (R.state === 'idle') return 'ENTER THE HALL OF ARMS';
    if (R.state === 'locked') return 'ROOM LOCKED - WAVE ' + Math.max(1, R.wave) + ' / ' + P5.waves.length;
    if (p.y > 830) return 'CHOOSE A WING: GALLERY / DUCT / TANK HALL';
    if (p.y > 300) return 'REACH THE ROTUNDA - THE GRAND HALL IS NORTH';
    return 'THE EXHIBIT IS AWAKE';
  }
  function hud(ctx, text, G) {
    const p = G.player, t = G.t / 60;
    if (!p.onfoot) { text('FURY TANK  O / SELECT: DISMOUNT', 12, VH - 30, 8, '#7deacc'); return false; }
    ctx.fillStyle = 'rgba(0,0,0,0.72)'; ctx.fillRect(6, 6, VW - 12, 44);
    for (let i = 0; i < 4; i++) {                        // Hard Corps: four slots, the one in hand lit
      const x = 10 + i * 38, w = p.weapons[i], on = i === p.wi;
      ctx.fillStyle = on ? 'rgba(60,70,30,0.9)' : 'rgba(20,24,22,0.9)'; ctx.fillRect(x, 9, 34, 38);
      ctx.strokeStyle = on ? (Math.floor(t * 4) % 2 ? '#ffe060' : '#ff9a30') : '#3a463c'; ctx.lineWidth = on ? 2 : 1; ctx.strokeRect(x, 9, 34, 38);
      text('ABCD'[i], x + 3, 15, 7, on ? '#ffe060' : '#8a988a');
      if (w) { ART.draw(ctx, 'of_' + w.id + '_pickup', x + 17, 30, { s: 0.24 }); if ((w.lv || 1) > 1) text('L' + w.lv, x + 31, 41, 7, '#7dffa0', 'right'); }
    }
    const w = p.weapons[p.wi], def = TD.FOOT_GUNS[w.id];
    text(def.name, 166, 17, 9, '#ffd060');
    text(p.reload > 0 ? 'RELOADING' : w.ammo + ' / ' + w.reserve, 166, 34, 10, w.ammo ? '#fff' : '#ff6440');
    text('MEGA CRASH', 278, 15, 7, '#ffad70');
    for (let i = 0; i < (G.crash || 0); i++) ART.draw(ctx, 'fury_bomb', 287 + i * 19, 32, { s: 0.115 });
    text('LIVES x' + Math.max(0, G.lives), 360, 15, 8, '#9fe0ff'); text('GRENADES ' + p.smoke, 360, 28, 7, '#fff');
    text('HOSTAGES ' + G.rescued + '/' + G.hostages.length, 360, 41, 7, '#ffe066');
    S.drawRadar(ctx, p, G.units, t, VW - 50, 8, 40);
    const col = S.phase === 'ALERT' ? '#ff3828' : S.phase === 'EVASION' ? '#ffb020' : S.phase === 'CAUTION' ? '#ffe060' : '#7dffa0';
    if (S.phase !== 'ALERT' || Math.floor(t * 4) % 2) text(S.phase + (S.phase === 'SNEAK' ? '' : ' ' + S.timer.toFixed(1)), 12, 62, 9, col);
    text(p.stance === 'prone' ? (W.inType(p.x, p.y, 'd') ? 'PRONE - IN DUCT' : 'PRONE') : p.hidden ? 'HIDDEN' : 'STAND', VW - 12, 62, 8, '#7dffa0', 'right');
    if (G.boss && G.boss.alive()) drawBossBar(ctx, text, G.boss);
    else text(objective(G), VW / 2, VH - 14, 10, '#ffd060', 'center');
    return true;
  }
  function drawBossBar(ctx, text, B) {
    const w = 280, h = w * 33 / 700, sc = w / 700, x = VW / 2 - w / 2, y = VH - h - 8;
    ART.draw(ctx, 'bmbar_frame_boss', x, y, { ax: 0, ay: 0, s: sc });
    const f = B.state === 'enter' ? B.gauge : B.hpFrac(), fill = ART.get('bmbar_fill_red');
    if (fill) ctx.drawImage(fill.im, fill.sx, fill.sy, fill.sw * f, fill.sh, x + 61 * sc, y + 10 * sc, 578 * sc * f, 13 * sc);
    text(B.name + (B.formName ? ' - ' + B.formName() : ''), x + w / 2, y - 7, 9, '#ffcc66', 'center');
  }
  function score(G, R) {
    const bonus = G.rescued * 3000 + (G.rescued === G.hostages.length ? 10000 : 0);
    G.score += bonus;
    R.extraRows = [['HOSTAGES', G.rescued + ' / ' + G.hostages.length + (G.hostagesLost ? '  LOST ' + G.hostagesLost : '')], ['RESCUE BONUS', bonus], ['EXHIBITS', G.exhibits]];
  }

  // ------------------------------------------------------------------ outside the mission: wrappers gated on it
  const baseDrop = TD.dropPickup, basePickups = TD.pickupTick, baseBlast = TD.blast;
  TD.dropPickup = function (G, x, y, kind) {
    if (G.mission === MID) return TD.footDrop(G, x, y, kind || (Math.random() < 0.1 ? 'pow' : 'ammo'));
    return baseDrop.apply(this, arguments);
  };
  TD.pickupTick = function (G, dt) {
    if (G.mission === MID && !G.player.onfoot) return;    // the pickups wait for you to climb out
    return basePickups.apply(this, arguments);
  };
  TD.blast = function (G, x, y, r) {
    baseBlast.apply(this, arguments);
    if (G.mission === MID) for (const h of G.hostages) if (h.state === 'bound' && M.dist(x, y, h.x, h.y) < r + 6) killHostage(G, h);
  };

  // ------------------------------------------------------------------ the mission
  const DATA = {
    title: 'LEVEL 5', name: 'MUSEUM OF VIOLENCE',
    brief: ['THE MUSEUM OF VIOLENCE IS SEIZED. FURY CREW ARE HELD INSIDE.', 'SHOOT THE EXHIBITS FOR GUNS. A+B OR G: MEGA CRASH.',
      'THE HALL OF ARMS LOCKS. THEN CHOOSE STEALTH OR ARMOR.', 'FREE THE HOSTAGES. STOP THE EXHIBIT IN THE GRAND HALL.'],
    start: L5.start, checkpoints: P5.checkpoints, gates: P5.gates, bossLine: P5.bossLine, boss: P5.boss, structures: [],
    units: P5.units, props: P5.props,
  };
  TD.MISSIONS.push({
    id: MID, mode: 'foot', pushScroll: true, data: DATA,
    map: { key: 'museum_ground', w: L5.w, h: L5.h, rects: [...L5.rects, ...ringRects()] },
    boss: (G, x, y) => TD.makeExhibit(G, x, y),
    setup, pre, tick, cam, canReinforce, respawn, drawFloor, drawOver, hud, score,
    keys: [['a', 'FIRE / CQC'], ['b', 'RELOAD'], ['c', 'PRONE'], ['x', 'ROLL'], ['y', 'GRENADE'], ['z', 'SWAP A-D']],
    help: ['WASD / LEFT STICK: MOVE    MOUSE / RIGHT STICK / Q-E: AIM', 'J / LEFT MOUSE / A: FIRE - BEHIND AN UNAWARE GUARD: CQC',
      'A+B TOGETHER OR G: MEGA CRASH (LIMITED STOCK)', 'R / K / B: RELOAD     SHIFT / F / C: PRONE (CRAWL UNDER LASERS, DUCT)',
      'SPACE / H / X: ROLL     U / Y: GRENADE     I / WHEEL / Z: SWAP A-D', 'WALK INTO THE EXHIBIT TANK TO BOARD.  O / SELECT: DISMOUNT',
      'T: WALL TAP NOISE      ENTER / START: PAUSE', 'FOUR GUNS (A-D). DYING LOSES THE GUN IN YOUR HAND.',
      'THE SCREEN NEVER SCROLLS BACK: YOUR ROUTE IS COMMITTED.', 'ALARM PANELS CALL REINFORCEMENTS. BREAK THEM.',
      'DO NOT SHOOT THE HOSTAGES.  BODIES LEFT IN VIEW ARE FOUND.', 'ONE HIT CONSUMES A LIFE ON FOOT.'],
  });
  TD.MUSEUM_WARM = ['museum_ground', ...Object.keys(MART), 'tank_laser_crimson', 'pow_badge', 'fury_bomb', 'life_up', 'score_1000', 'pt_niel_hull', 'pt_niel_turret', 'pt_niel_damaged_hull', 'pt_niel_wreck',
    ...['regular', 'female', 'athletic', 'heavy'].flatMap(b => ['stun', 'recovery', 'powerup', 'death'].flatMap(a => (SEQ['of_' + b + '_' + a] || { frames: [] }).frames))];
}(window));
