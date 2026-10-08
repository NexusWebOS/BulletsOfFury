/*
 * RAZORBACK MK II - the Level 2 boss, on the Razorback's own authored plates (hull 0..7, turret,
 * machine guns, missile pods, rotors, treads, sonic set, wreck). Original code for this engine.
 *
 * Hard Corps-style: break the parts to open the machine. The two side guns and two missile pods are
 * targets of their own; the turret soaks the main cannon and must fall before the hull takes full
 * damage (until then the hull takes 15%). Every committed attack is telegraphed with the game's FOV
 * cones - green while it is still deciding, yellow when it locks, red when it is coming (Mike's rule).
 *
 *   drive   - repositions across the plaza, both guns tracking you independently
 *   cannon  - turret charge (sonic_charge at the muzzle) -> a three-shell spread
 *   rack    - a lock warning over you, then six shootable razor missiles from alternating pods
 *   nova    - (turret gone) a ring of sonic rounds with a gap that rotates each wave
 *   ram     - (under 40%) green -> yellow -> red cone, then a straight charge to the wall; it stalls
 *             on impact for a moment, which is your window
 */
(function (root) {
  'use strict';
  const TD = root.TD, M = TD.M, A = TD.Audio, FX = TD.FX, Cam = TD.Cam;
  const S = 0.4;                                     // plate scale (the main game draws it at 0.46 on a 680 field)
  const ARENA = { x0: 175, x1: 625, y0: 120, y1: 640 };

  TD.makeRazorback = function (G, x, y) {
    const R = {
      x, y: -120, a: 0, turret: 0, recoil: 0, state: 'enter', t: 0, next: 'drive', goal: { x, y },
      parts: { gunL: 22, gunR: 22, podL: 16, podR: 16, turret: 60, hull: 110 }, flash: {}, travel: 0,
      warn: null, charge: 0, dead: false, deathT: 0, gauge: 0, ramDir: 0, stall: 0, novaRot: 0, rack: 0, rackT: 0, guns: { L: 0, R: 0 },
    };
    R.max = Object.assign({}, R.parts);
    const world = (lx, ly) => { const c = Math.cos(R.a), s = Math.sin(R.a); return { x: R.x + (lx * c - ly * s) * S, y: R.y + (lx * s + ly * c) * S }; };
    const fwdFrom = (p, a, d) => { const [fx, fy] = M.fwd(a); return { x: p.x + fx * d, y: p.y + fy * d }; };
    const partPos = {
      gunL: () => world(-57, 96), gunR: () => world(57, 96), podL: () => world(-105, 10), podR: () => world(105, 10), turret: () => ({ x: R.x, y: R.y }),
    };
    const partR = { gunL: 14, gunR: 14, podL: 15, podR: 15, turret: 24 };
    const hpFrac = () => { let s = 0, m = 0; for (const k in R.parts) { s += Math.max(0, R.parts[k]); m += R.max[k]; } return s / m; };
    R.hpFrac = hpFrac;
    R.alive = () => !R.dead && R.state !== 'enter';
    R.aim = () => ({ x: R.x, y: R.y });
    R.world = world;

    function damage(part, dmg) {
      if (R.parts[part] <= 0) return;
      if (part === 'hull' && R.parts.turret > 0) dmg *= 0.15;
      R.parts[part] -= dmg; R.flash[part] = 0.12; G.score += Math.round(dmg * 10);
      if (R.parts[part] <= 0) {
        const p = part === 'hull' ? { x: R.x, y: R.y } : partPos[part]();
        FX.boom(p.x, p.y, 120, 'nxp_dense_'); FX.debris(p.x, p.y, 0.35); A.play('expB'); Cam.kick(7);
        if (part !== 'hull') { A.play('phase'); G.say(part === 'turret' ? 'TURRET DOWN - HULL EXPOSED' : 'PART DESTROYED', p); G.score += 2000; }
        if (part === 'hull') die();
      }
    }
    R.hit = function (x, y, r, dmg) {
      if (!R.alive()) return false;
      for (const k in partPos) if (R.parts[k] > 0) { const p = partPos[k](); if (M.dist(x, y, p.x, p.y) < partR[k] + r) { damage(k, dmg); return true; } }
      if (M.dist(x, y, R.x, R.y) < 56 + r) { damage('hull', dmg); R.flash.hull = 0.12; return true; }
      return false;
    };
    R.blast = function (x, y, r, dmg) {
      if (!R.alive()) return;
      for (const k in partPos) if (R.parts[k] > 0) { const p = partPos[k](); if (M.dist(x, y, p.x, p.y) < partR[k] + r) damage(k, dmg * 0.6); }
      if (M.dist(x, y, R.x, R.y) < 56 + r) damage('hull', dmg * 0.6);
    };
    function die() {
      R.dead = true; R.state = 'dying'; R.deathT = 0; R.warn = null; A.stopMusic(); A.play('whiteout');
      for (const k in R.parts) R.parts[k] = Math.min(0, R.parts[k]);
    }

    function setState(s) { R.state = s; R.t = 0; R.warn = null; R.charge = 0; }
    function pick() {
      const p = G.player, f = hpFrac(), opts = ['drive', 'cannon'];
      if (R.parts.podL > 0 || R.parts.podR > 0) opts.push('rack');
      if (R.parts.turret <= 0) opts.push('nova', 'nova');
      if (f < 0.4) opts.push('ram', 'ram');
      if (R.parts.turret <= 0) { const i = opts.indexOf('cannon'); if (i >= 0) opts.splice(i, 1); }
      let s = opts[(Math.random() * opts.length) | 0];
      if (s === R.last && Math.random() < 0.7) s = opts[(Math.random() * opts.length) | 0];
      R.last = s;
      if (s === 'drive') {   // never further than one screen from you, so the camera can always frame the fight
        const lo = Math.max(ARENA.y0, p.y - 300), hi = Math.max(lo + 20, Math.min(ARENA.y1, p.y - 130));
        R.goal = { x: M.rnd(ARENA.x0, ARENA.x1), y: M.rnd(lo, hi) };
      }
      setState(s);
    }
    function driveTo(tx, ty, spd) {
      const want = M.angTo(R.x, R.y, tx, ty), d = Math.abs(M.wrap(want - R.a));
      R.a = M.turnTo(R.a, want, 0.045);
      if (d < 0.7) { const [fx, fy] = M.fwd(R.a); R.x += fx * spd * (1 - d); R.y += fy * spd * (1 - d); R.travel += spd; }
      return M.dist(R.x, R.y, tx, ty) < 12;
    }
    function gunsTick(dt, rate) {
      const p = G.player;
      for (const side of ['L', 'R']) {
        const part = 'gun' + side; if (R.parts[part] <= 0) continue;
        const g = partPos[part](), want = M.angTo(g.x, g.y, p.x, p.y);
        R['ga' + side] = M.turnTo(R['ga' + side] == null ? R.a : R['ga' + side], want, 0.05);
        if ((R.guns[side] -= dt) <= 0 && Math.abs(M.wrap(want - R['ga' + side])) < 0.25) {
          R.guns[side] = rate * M.rnd(0.85, 1.2); R['bn' + side] = 3; R['bt' + side] = 0;
        }
        // the burst runs on the game clock, so pausing the game pauses the gun
        if (R['bn' + side] > 0 && (R['bt' + side] -= dt) <= 0) {
          R['bn' + side]--; R['bt' + side] = 0.09;
          const a = R['ga' + side] + M.rnd(-0.07, 0.07), [fx, fy] = M.fwd(a);
          G.eshots.push({ k: 'mg', x: g.x + fx * 20, y: g.y + fy * 20, vx: fx * 4.8, vy: fy * 4.8, a, dmg: 1, life: 110, r: 4, t: 0 }); A.play('eshot', 0.5);
          FX.flash(g.x + fx * 20, g.y + fy * 20, a, 0.12);
        }
      }
    }
    R.tick = function (dt) {
      const p = G.player;
      for (const k in R.flash) R.flash[k] = Math.max(0, R.flash[k] - dt);
      R.t += dt;
      if (R.state === 'dying') {
        R.deathT += dt;
        if (Math.random() < 0.35) { FX.boom(R.x + M.rnd(-60, 60), R.y + M.rnd(-60, 60), M.rnd(60, 140), Math.random() < 0.5 ? 'nxp_dense_' : 'nxp_clus_'); Cam.kick(4); if (Math.random() < 0.4) A.play('expB', 0.7); }
        if (R.deathT > 2.6 && !R.wrecked) { R.wrecked = true; FX.boom(R.x, R.y, 220, 'nxp_dense_'); FX.ring(R.x, R.y, 1.2); Cam.kick(12); A.play('expB'); G.bossDown(); }
        return;
      }
      if (R.state === 'enter') {
        R.y += 2.2; R.a = 0; R.travel += 2.2; R.gauge = M.clamp((R.y + 120) / (y + 120), 0, 1);
        if (R.t % 0.12 < dt) FX.smoke(R.x + M.rnd(-40, 40), R.y - 50, 0.12, 0.8);
        if (R.y >= y) { R.y = y; setState('cannon'); A.playMusic('boss2'); }
        return;
      }
      // the turret tracks you whatever else is happening
      R.turret = M.turnTo(R.turret, M.angTo(R.x, R.y, p.x, p.y), R.state === 'cannon' && R.charge > 0.55 ? 0.004 : 0.03);
      R.recoil *= 0.8;
      const f = hpFrac(), rage = f < 0.4 ? 1.35 : 1;
      if (R.state !== 'ram') gunsTick(dt, 1.4 / rage);

      if (R.state === 'drive') {
        if (driveTo(R.goal.x, R.goal.y, 1.25 * rage) || R.t > 4) pick();
      } else if (R.state === 'cannon') {
        if (R.parts.turret <= 0) { pick(); return; }
        R.charge = Math.min(1, R.t / 1.0);
        R.warn = { x: R.x, y: R.y, a: R.turret, range: 330, half: 0.22, col: R.charge < 0.55 ? 'yellow' : 'red' };
        if (R.t >= 1.0) {
          const m = fwdFrom({ x: R.x, y: R.y }, R.turret, 142 * S);
          for (const s of [-0.16, 0, 0.16]) { const a = R.turret + s, [fx, fy] = M.fwd(a); G.eshots.push({ k: 'shell', x: m.x, y: m.y, vx: fx * 6.2, vy: fy * 6.2, a, dmg: 2, life: 120, r: 7, t: 0 }); }
          R.recoil = 12; Cam.kick(5); A.play('cannon'); FX.flash(m.x, m.y, R.turret, 0.4); FX.smoke(m.x, m.y, 0.2, 0.8);
          R.charge = 0; R.warn = null; R.t = 0; R.state = 'cooldown'; R.cool = 0.7;
        }
      } else if (R.state === 'rack') {
        if (R.t < 0.9) { R.lockOn = true; if (R.t % 0.15 < dt) A.play('lock', 0.6); }
        else {
          R.lockOn = false;
          if ((R.rackT -= dt) <= 0 && R.rack < 6) {
            const pods = ['podL', 'podR'].filter(k => R.parts[k] > 0); if (!pods.length) { pick(); return; }
            const pod = pods[R.rack % pods.length], pp = partPos[pod](), a = R.a + Math.PI + (pod === 'podL' ? 0.5 : -0.5) + M.rnd(-0.2, 0.2), [fx, fy] = M.fwd(a);
            G.eshots.push({ k: 'missile', x: pp.x, y: pp.y, vx: fx * 2, vy: fy * 2, a, dmg: 2, life: 220, r: 7, t: 0, homing: 55, turn: 0.075, accel: 0.12, max: 6.5, shootable: true, over: true });
            A.play('missile', 0.6); R.rack++; R.rackT = 0.16;
          }
          if (R.rack >= 6) { R.rack = 0; R.state = 'cooldown'; R.cool = 1.0; R.t = 0; }
        }
      } else if (R.state === 'nova') {
        R.charge = Math.min(1, R.t / 0.8);
        if (R.t >= 0.8) {
          const n = 18, gap = R.novaRot;
          for (let i = 0; i < n; i++) {
            const a = (i / n) * Math.PI * 2 + gap * 0.2; if (i % n === Math.floor(gap) % n || (i + 1) % n === Math.floor(gap) % n || (i + 2) % n === Math.floor(gap) % n) continue;
            const [fx, fy] = M.fwd(a); G.eshots.push({ k: 'sonic', x: R.x, y: R.y, vx: fx * 3.4, vy: fy * 3.4, a, dmg: 2, life: 160, r: 7, t: 0, over: true });
          }
          R.novaRot += 5; FX.ring(R.x, R.y, 0.6); A.play('laser'); Cam.kick(3);
          R.charge = 0; R.state = 'cooldown'; R.cool = 0.9; R.t = 0;
        }
      } else if (R.state === 'ram') {
        // green: track you / yellow: locked / red: coming
        if (R.t < 0.7) { R.ramDir = M.angTo(R.x, R.y, p.x, p.y); R.a = M.turnTo(R.a, R.ramDir, 0.08); R.warn = { x: R.x, y: R.y, a: R.ramDir, range: 380, half: 0.2, col: 'green' }; }
        else if (R.t < 1.15) { R.a = M.turnTo(R.a, R.ramDir, 0.08); R.warn.col = 'yellow'; }
        else if (R.t < 1.5) { R.warn.col = 'red'; if (R.t - dt < 1.15) A.play('warn', 0.6); }
        else {
          R.warn = null; const [fx, fy] = M.fwd(R.ramDir); R.x += fx * 7.2; R.y += fy * 7.2; R.travel += 7.2;
          if (R.t % 0.05 < dt) FX.smoke(R.x - fx * 50, R.y - fy * 50, 0.14, 0.7);
          if (M.dist(R.x, R.y, p.x, p.y) < 56 + p.r) TD.hurtPlayer(G, 3, p.x, p.y);
          if (R.x < ARENA.x0 - 20 || R.x > ARENA.x1 + 20 || R.y < ARENA.y0 - 20 || R.y > ARENA.y1 + 60) {
            R.x = M.clamp(R.x, ARENA.x0 - 20, ARENA.x1 + 20); R.y = M.clamp(R.y, ARENA.y0 - 20, ARENA.y1 + 60);
            FX.boom(R.x + fx * 50, R.y + fy * 50, 120, 'nxp_dense_'); Cam.kick(10); A.play('expB'); R.state = 'cooldown'; R.cool = 1.6; R.t = 0; G.say('STALLED!', R);
          }
        }
      } else if (R.state === 'cooldown') {
        if (R.t >= R.cool) pick();
      }
      // keep inside the plaza, never on top of the player
      R.x = M.clamp(R.x, ARENA.x0 - 20, ARENA.x1 + 20); R.y = M.clamp(R.y, ARENA.y0 - 20, ARENA.y1 + 60);
      const dp = M.dist(R.x, R.y, p.x, p.y);
      if (dp < 56 + p.r && R.state !== 'ram') TD.pushOut(p, { x: R.x, y: R.y, r: 56 });
    };

    // ------------------------------------------------------------ draw
    const img = k => ART.get(k);
    R.drawUnder = function (c) {
      if (R.warn) TD.Stealth.drawCone(c, { x: R.warn.x, y: R.warn.y, look: R.warn.a, vis: { range: R.warn.range, half: R.warn.half }, mode: R.warn.col === 'green' ? 'patrol' : R.warn.col === 'yellow' ? 'suspect' : 'alert' }, G.t / 60);
    };
    R.draw = function (c, t) {
      if (R.wrecked) { ART.draw(c, 'rzb_wreck', R.x, R.y, { a: R.a, s: S }); return; }
      const i = ((Math.round(R.a / (Math.PI / 4)) % 8) + 8) % 8, resid = M.wrap(R.a - i * Math.PI / 4), hk = 'rzb_hull_' + i;
      ART.draw(c, hk, R.x + 8, R.y + 11, { a: resid, s: S, tint: '#000000', alpha: 0.34 });
      // treads scroll with distance travelled, under the hull
      const tr = img('rzb_tread');
      if (tr) for (const side of [-1, 1]) {
        c.save(); c.translate(R.x, R.y); c.rotate(R.a); c.beginPath(); c.rect((side * 81 - 19) * S, -98 * S, 38 * S, 218 * S); c.clip();
        const off = ((R.travel * 1.6) % 42 + 42) % 42;
        for (let j = -4; j < 6; j++) { const tw = tr.sw * 0.62 * S, th = tr.sh * 0.62 * S; c.drawImage(tr.im, tr.sx, tr.sy, tr.sw, tr.sh, side * 81 * S - tw / 2, (j * 65 + off) * S - th / 2, tw, th); }
        c.restore();
      }
      ART.draw(c, hk, R.x, R.y, { a: resid, s: S, flash: R.flash.hull ? 1 : 0 });
      for (let n = 0; n < 4; n++) { const mt = [[-65, -46], [65, -46], [-70, 33], [68, 33]][n], p = world(mt[0], mt[1]); ART.draw(c, 'rzb_rotor', p.x, p.y, { a: R.a + R.travel / 25, s: 0.43 * S }); }
      for (const [k, sx] of [['podL', -1], ['podR', 1]]) if (R.parts[k] > 0) { const p = partPos[k](); ART.draw(c, 'rzb_missile_pod', p.x, p.y, { a: R.a, s: 0.55 * S, flash: R.flash[k] ? 1 : 0 }); }
      for (const side of ['L', 'R']) if (R.parts['gun' + side] > 0) { const p = partPos['gun' + side](), ga = R['ga' + side] == null ? R.a : R['ga' + side]; ART.draw(c, 'rzb_machinegun', p.x, p.y, { a: ga, s: S, ax: 64, ay: 65, flash: R.flash['gun' + side] ? 1 : 0 }); }
      if (R.parts.turret > 0) {
        const p = fwdFrom({ x: R.x, y: R.y }, R.turret, -R.recoil * S), tk = R.parts.turret < R.max.turret * 0.5 ? 'rzb_turret_damaged' : 'rzb_turret';
        ART.draw(c, tk, p.x, p.y, { a: R.turret, s: S, ax: 128, ay: 128, flash: R.flash.turret ? 1 : 0 });
      }
      if (R.charge > 0) {
        const m = R.state === 'cannon' ? fwdFrom({ x: R.x, y: R.y }, R.turret, 142 * S) : { x: R.x, y: R.y };
        ART.draw(c, 'rzb_sonic_charge', m.x, m.y, { a: t * 2, s: (0.16 + R.charge * 0.5) * S, comp: 'lighter' });
      }
    };
    R.drawOver = function (c, t) {
      if (R.lockOn) { const p = G.player, on = Math.floor(t * 10) % 2; if (on) ART.draw(c, 'bmfx_alert_red_incoming_projectile', p.x, p.y - 40, { s: 0.22 }); }
    };
    return R;
  };
}(window));
