/*
 * THE EXHIBIT - Level 5's boss: the Razorback Mk II on display in the Museum of Violence's grand hall,
 * reactivated. Original code; the Razorback's authored plates (hull 0..7, turret, guns, pods, rotors,
 * treads, sonic set, wreck) are the art.
 *
 * Contra Hard Corps boss grammar, as BOF already uses it (docs/HARDCORPS_BOSSES_1007.md, BOSS_STUDY_0918.md):
 *   CAUSE (a shape-in-the-world tell) -> COMMIT (aim locks) -> ATTACK -> CROSSING (a gap you move through)
 *   -> RECOVERY (a visible opening). Escalation reshapes the fight instead of adding HP:
 *
 *   FORM 1  ON DISPLAY  bolted to its turntable plinth. Twin guns track you; warned cannon spread;
 *                       a locked rack of shootable missiles. Break the pods to tear it off the plinth.
 *   FORM 2  BREAKOUT    the plinth shatters. It drives, and its warned ram smashes the hall's statues -
 *                       your cover - and stalls on the wall: a stalled hull takes double damage.
 *   FORM 3  OVERDRIVE   (turret gone) sonic rings with a rotating gap, sweeping sonic walls with one hole
 *                       to cross through, faster rams.
 * The hull only takes 15% until the turret falls (break it apart first). One hit still kills you on foot,
 * so every lethal move is telegraphed with the shared green/yellow/red cones.
 */
(function (root) {
  'use strict';
  const TD = root.TD, M = TD.M, A = TD.Audio, FX = TD.FX, Cam = TD.Cam;
  const S = 0.4, AR = { x0: 150, x1: 650, y0: 70, y1: 290 };

  TD.EXHIBIT_HOME = { x: 400, y: 150 };
  TD.makeExhibit = function (G, x, y) {
    const R = {
      name: 'THE EXHIBIT', x, y, a: 0, turret: 0, recoil: 0, state: 'enter', t: 0, form: 1, last: null, goal: { x, y },
      parts: { gunL: 18, gunR: 18, podL: 14, podR: 14, turret: 55, hull: 110 }, flash: {}, travel: 0, warn: null, charge: 0,
      dead: false, wrecked: false, deathT: 0, gauge: 0, ramDir: 0, novaRot: 0, rack: 0, rackT: 0, guns: { L: 0.8, R: 1.3 },
      stalled: 0, waveRow: null, log: [],
    };
    R.max = Object.assign({}, R.parts);
    const world = (lx, ly) => { const c = Math.cos(R.a), s = Math.sin(R.a); return { x: R.x + (lx * c - ly * s) * S, y: R.y + (lx * s + ly * c) * S }; };
    const fwdFrom = (p, a, d) => { const [fx, fy] = M.fwd(a); return { x: p.x + fx * d, y: p.y + fy * d }; };
    const partPos = { gunL: () => world(-57, 96), gunR: () => world(57, 96), podL: () => world(-105, 10), podR: () => world(105, 10), turret: () => ({ x: R.x, y: R.y }) };
    const partR = { gunL: 13, gunR: 13, podL: 14, podR: 14, turret: 22 };
    const hpFrac = () => { let s = 0, m = 0; for (const k in R.parts) { s += Math.max(0, R.parts[k]); m += R.max[k]; } return s / m; };
    R.hpFrac = hpFrac;
    R.alive = () => !R.dead && R.state !== 'enter';
    R.aim = () => ({ x: R.x, y: R.y });
    R.world = world; R.partPos = partPos;
    R.formName = () => ['', 'ON DISPLAY', 'BREAKOUT', 'OVERDRIVE'][R.form];
    const log = (event) => { R.log.push({ event, t: +G.time.toFixed(2), form: R.form }); };

    function damage(part, dmg) {
      if (R.parts[part] <= 0 || R.dead) return;
      if (part === 'hull' && R.parts.turret > 0) dmg *= 0.15;
      if (part === 'hull' && R.stalled > 0) dmg *= 2;
      R.parts[part] -= dmg; R.flash[part] = 0.12; G.score += Math.round(dmg * 10);
      if (R.parts[part] > 0) return;
      const p = part === 'hull' ? { x: R.x, y: R.y } : partPos[part]();
      FX.boom(p.x, p.y, 120, 'nxp_dense_'); FX.debris(p.x, p.y, 0.35); A.play('expB'); Cam.kick(7);
      if (part === 'hull') return die();
      A.play('phase'); G.score += 2000; log('break:' + part);
      G.say(part === 'turret' ? 'TURRET DOWN - HULL EXPOSED' : part.startsWith('pod') ? 'MISSILE POD DOWN' : 'GUN DOWN', p);
      reform();
    }
    // escalation is driven by what you have broken (Hard Corps), with a health floor so it always arrives
    function reform() {
      const pods = R.parts.podL <= 0 && R.parts.podR <= 0;
      const want = R.parts.turret <= 0 ? 3 : (pods || hpFrac() < 0.72) ? 2 : 1;
      if (want <= R.form) return;
      R.form = want; log('form' + want); A.play('warn', 0.7); Cam.kick(9);
      if (want === 2) {   // the plinth goes: debris ring, and the tank drops onto the floor
        for (let i = 0; i < 8; i++) { const a = i / 8 * Math.PI * 2; FX.boom(R.x + Math.cos(a) * 60, R.y + Math.sin(a) * 50, 90, 'nxp_clus_'); }
        FX.ring(R.x, R.y, 1); G.say('BREAKOUT! IT LEFT THE PLINTH', { x: R.x, y: R.y + 70 });
      } else G.say('OVERDRIVE', { x: R.x, y: R.y + 70 });
      set('recover'); R.cool = 1.1;
    }
    R.hit = function (x, y, r, dmg) {
      if (!R.alive()) return false;
      for (const k in partPos) if (R.parts[k] > 0) { const p = partPos[k](); if (M.dist(x, y, p.x, p.y) < partR[k] + r) { damage(k, dmg); return true; } }
      if (M.dist(x, y, R.x, R.y) < 54 + r) { damage('hull', dmg); return true; }
      return false;
    };
    R.blast = function (x, y, r, dmg) {
      if (!R.alive()) return;
      for (const k in partPos) if (R.parts[k] > 0) { const p = partPos[k](); if (M.dist(x, y, p.x, p.y) < partR[k] + r) damage(k, dmg * 0.6); }
      if (M.dist(x, y, R.x, R.y) < 54 + r) damage('hull', dmg * 0.6);
    };
    function die() {
      R.dead = true; R.state = 'dying'; R.deathT = 0; R.warn = null; R.waveRow = null; A.stopMusic(); A.play('whiteout'); log('die');
      for (const k in R.parts) R.parts[k] = Math.min(0, R.parts[k]);
    }
    function set(s) { R.state = s; R.t = 0; R.warn = null; R.charge = 0; }
    function pick() {
      const p = G.player, opts = [];
      if (R.form === 1) { opts.push('cannon', 'cannon'); if (R.parts.podL > 0 || R.parts.podR > 0) opts.push('rack'); }
      if (R.form === 2) { opts.push('drive', 'ram', 'ram'); if (R.parts.turret > 0) opts.push('cannon'); if (R.parts.podL > 0 || R.parts.podR > 0) opts.push('rack'); }
      if (R.form === 3) opts.push('nova', 'wave', 'ram', 'drive');
      let s = opts[(Math.random() * opts.length) | 0];
      if (s === R.last) s = opts[(Math.random() * opts.length) | 0];
      R.last = s;
      if (s === 'drive') R.goal = { x: M.rnd(AR.x0 + 30, AR.x1 - 30), y: M.rnd(AR.y0 + 10, Math.min(AR.y1 - 60, p.y - 110)) };
      set(s); log(s);
    }
    function driveTo(tx, ty, spd) {
      const want = M.angTo(R.x, R.y, tx, ty), d = Math.abs(M.wrap(want - R.a));
      R.a = M.turnTo(R.a, want, 0.05);
      if (d < 0.7) { const [fx, fy] = M.fwd(R.a); R.x += fx * spd * (1 - d); R.y += fy * spd * (1 - d); R.travel += spd; }
      return M.dist(R.x, R.y, tx, ty) < 12;
    }
    function gunsTick(dt, rate) {
      const p = G.player;
      for (const side of ['L', 'R']) {
        const part = 'gun' + side; if (R.parts[part] <= 0) continue;
        const g = partPos[part](), want = M.angTo(g.x, g.y, p.x, p.y);
        R['ga' + side] = M.turnTo(R['ga' + side] == null ? R.a : R['ga' + side], want, 0.045);
        if ((R.guns[side] -= dt) <= 0 && Math.abs(M.wrap(want - R['ga' + side])) < 0.25) { R.guns[side] = rate * M.rnd(0.9, 1.25); R['bn' + side] = 3; R['bt' + side] = 0; }
        if (R['bn' + side] > 0 && (R['bt' + side] -= dt) <= 0) {
          R['bn' + side]--; R['bt' + side] = 0.1;
          const a = R['ga' + side] + M.rnd(-0.06, 0.06), [fx, fy] = M.fwd(a);
          G.eshots.push({ k: 'mg', x: g.x + fx * 18, y: g.y + fy * 18, vx: fx * 4.2, vy: fy * 4.2, a, dmg: 1, life: 120, r: 4, t: 0 }); A.play('eshot', 0.5);
          FX.flash(g.x + fx * 18, g.y + fy * 18, a, 0.12);
        }
      }
    }
    function smashCover() {   // the ram goes through the hall's statues and vases
      for (const q of G.props) if (!q.dead && q.kind && q.kind.startsWith('mx_') && M.dist(q.x, q.y, R.x, R.y) < 58 + q.r) TD.hitProp(G, q, 99);
    }

    R.tick = function (dt) {
      const p = G.player;
      for (const k in R.flash) R.flash[k] = Math.max(0, R.flash[k] - dt);
      R.t += dt; R.stalled = Math.max(0, R.stalled - dt);
      if (R.state === 'dying') {
        R.deathT += dt;
        if (Math.random() < 0.35) { FX.boom(R.x + M.rnd(-60, 60), R.y + M.rnd(-50, 50), M.rnd(60, 140), Math.random() < 0.5 ? 'nxp_dense_' : 'nxp_clus_'); Cam.kick(4); if (Math.random() < 0.4) A.play('expB', 0.7); }
        if (R.deathT > 2.6 && !R.wrecked) { R.wrecked = true; FX.boom(R.x, R.y, 220, 'nxp_dense_'); FX.ring(R.x, R.y, 1.2); Cam.kick(12); A.play('expB'); G.bossDown(); }
        return;
      }
      if (R.state === 'enter') {   // the museum's alarms flash while the gauge fills; the exhibit turns to face you
        R.gauge = Math.min(1, R.t / 1.6); R.turret = M.turnTo(R.turret, M.angTo(R.x, R.y, p.x, p.y), 0.02);
        if (R.t % 0.4 < dt) A.play('lock', 0.5);
        if (R.t >= 1.6) { set('cannon'); A.playMusic('boss2'); log('awake'); }
        return;
      }
      R.turret = M.turnTo(R.turret, M.angTo(R.x, R.y, p.x, p.y), R.state === 'cannon' && R.charge > 0.55 ? 0.004 : 0.03);
      R.recoil *= 0.8;
      if (R.form === 1) R.a = M.turnTo(R.a, M.angTo(R.x, R.y, p.x, p.y), 0.012);   // the turntable
      if (R.state !== 'ram' && R.state !== 'recover' && R.stalled <= 0) gunsTick(dt, R.form === 1 ? 1.6 : 1.3);

      if (R.state === 'drive') {
        if (driveTo(R.goal.x, R.goal.y, 1.3) || R.t > 3.5) { set('recover'); R.cool = 0.4; }
      } else if (R.state === 'cannon') {
        if (R.parts.turret <= 0) { pick(); return; }
        // CAUSE: yellow cone while it aims, red once the aim has locked (COMMIT)
        R.charge = Math.min(1, R.t / 1.05);
        R.warn = { x: R.x, y: R.y, a: R.turret, range: 330, half: 0.24, col: R.charge < 0.55 ? 'yellow' : 'red' };
        if (R.t >= 1.05) {
          const m = fwdFrom({ x: R.x, y: R.y }, R.turret, 142 * S);
          for (const s of [-0.2, 0, 0.2]) { const a = R.turret + s, [fx, fy] = M.fwd(a); G.eshots.push({ k: 'shell', x: m.x, y: m.y, vx: fx * 5.4, vy: fy * 5.4, a, dmg: 2, life: 130, r: 7, t: 0 }); }
          R.recoil = 12; Cam.kick(5); A.play('cannon'); FX.flash(m.x, m.y, R.turret, 0.4); FX.smoke(m.x, m.y, 0.2, 0.8);
          set('recover'); R.cool = 0.85;
        }
      } else if (R.state === 'rack') {
        if (R.t < 1.0) { R.lockOn = true; if (R.t % 0.15 < dt) A.play('lock', 0.6); }
        else {
          R.lockOn = false;
          if ((R.rackT -= dt) <= 0 && R.rack < 6) {
            const pods = ['podL', 'podR'].filter(k => R.parts[k] > 0); if (!pods.length) { set('recover'); R.cool = 0.5; return; }
            const pod = pods[R.rack % pods.length], pp = partPos[pod](), a = R.a + Math.PI + (pod === 'podL' ? 0.5 : -0.5) + M.rnd(-0.2, 0.2), [fx, fy] = M.fwd(a);
            G.eshots.push({ k: 'missile', x: pp.x, y: pp.y, vx: fx * 2, vy: fy * 2, a, dmg: 2, life: 220, r: 7, t: 0, homing: 50, turn: 0.07, accel: 0.11, max: 5.8, shootable: true, over: true });
            A.play('missile', 0.6); R.rack++; R.rackT = 0.18;
          }
          if (R.rack >= 6) { R.rack = 0; set('recover'); R.cool = 1.0; }
        }
      } else if (R.state === 'nova') {
        R.charge = Math.min(1, R.t / 0.85);
        if (R.t >= 0.85) {
          const n = 18, gap = Math.floor(R.novaRot) % n;
          for (let i = 0; i < n; i++) {
            if (i === gap || (i + 1) % n === gap || (i + 2) % n === gap) continue;
            const a = (i / n) * Math.PI * 2 + R.novaRot * 0.2, [fx, fy] = M.fwd(a);
            G.eshots.push({ k: 'sonic', x: R.x, y: R.y, vx: fx * 3.0, vy: fy * 3.0, a, dmg: 2, life: 170, r: 7, t: 0, over: true });
          }
          R.novaRot += 5; FX.ring(R.x, R.y, 0.6); A.play('laser'); Cam.kick(3);
          set('recover'); R.cool = 0.95;
        }
      } else if (R.state === 'wave') {
        // CROSSING: a horizontal sonic wall with one hole, announced by its own yellow lane first
        if (!R.waveRow) { const hole = M.clamp(p.x + M.rnd(-90, 90), AR.x0 + 40, AR.x1 - 40); R.waveRow = { hole, y: R.y + 50 }; }
        R.warn = { x: R.waveRow.hole, y: R.y + 30, a: 0, range: 300, half: 0.16, col: R.t < 0.6 ? 'green' : R.t < 1.0 ? 'yellow' : 'red' };
        if (R.t >= 1.2) {
          for (let x = AR.x0 - 40; x <= AR.x1 + 40; x += 30) if (Math.abs(x - R.waveRow.hole) > 34)
            G.eshots.push({ k: 'wave', x, y: R.waveRow.y, vx: 0, vy: 2.5, a: 0, dmg: 2, life: 200, r: 9, t: 0, over: true });
          A.play('laser', 0.8); Cam.kick(4); R.waveRow = null; set('recover'); R.cool = 1.0;
        }
      } else if (R.state === 'ram') {
        // green: still tracking / yellow: locked / red: coming. Then a straight charge that stalls on the wall.
        const fast = R.form === 3 ? 1.25 : 1;
        if (R.t < 0.7 / fast) { R.ramDir = M.angTo(R.x, R.y, p.x, p.y); R.a = M.turnTo(R.a, R.ramDir, 0.08); R.warn = { x: R.x, y: R.y, a: R.ramDir, range: 380, half: 0.2, col: 'green' }; }
        else if (R.t < 1.15 / fast) { R.a = M.turnTo(R.a, R.ramDir, 0.08); R.warn.col = 'yellow'; }
        else if (R.t < 1.5 / fast) { R.warn.col = 'red'; if (R.t - dt < 1.15 / fast) A.play('warn', 0.6); }
        else {
          R.warn = null; const [fx, fy] = M.fwd(R.ramDir), v = 6.6 * fast; R.x += fx * v; R.y += fy * v; R.travel += v;
          if (R.t % 0.05 < dt) FX.smoke(R.x - fx * 50, R.y - fy * 50, 0.14, 0.7);
          smashCover();
          if (M.dist(R.x, R.y, p.x, p.y) < 54 + p.r) TD.hurtPlayer(G, 3, p.x, p.y);
          const out = R.x < AR.x0 || R.x > AR.x1 || R.y < AR.y0 || R.y > AR.y1 + 20;
          if (out) {   // RECOVERY: stalled against the wall - the hull opens up
            R.x = M.clamp(R.x, AR.x0, AR.x1); R.y = M.clamp(R.y, AR.y0, AR.y1 + 20);
            FX.boom(R.x + fx * 50, R.y + fy * 50, 120, 'nxp_dense_'); Cam.kick(10); A.play('expB');
            R.stalled = 1.7; set('recover'); R.cool = 1.7; G.say('STALLED! HULL OPEN', R); log('stall');
          }
        }
      } else if (R.state === 'recover') {
        if (R.form >= 2 && R.t > 0.2 && R.stalled <= 0) { const h = TD.EXHIBIT_HOME; if (R.form === 2 && M.dist(R.x, R.y, h.x, h.y) > 160) driveTo(h.x, h.y, 0.8); }
        if (R.t >= R.cool) pick();
      }
      R.x = M.clamp(R.x, AR.x0 - 10, AR.x1 + 10); R.y = M.clamp(R.y, AR.y0 - 10, AR.y1 + 30);
      if (M.dist(R.x, R.y, p.x, p.y) < 54 + p.r && R.state !== 'ram') TD.pushOut(p, { x: R.x, y: R.y, r: 54 });
    };

    // ------------------------------------------------------------ draw
    R.drawUnder = function (c) {
      if (R.warn) TD.Stealth.drawCone(c, { x: R.warn.x, y: R.warn.y, look: R.warn.a, vis: { range: R.warn.range, half: R.warn.half }, mode: R.warn.col === 'green' ? 'patrol' : R.warn.col === 'yellow' ? 'suspect' : 'alert' }, G.t / 60);
    };
    R.draw = function (c, t) { TD.drawExhibitTank(c, R, t, world, partPos, fwdFrom); };
    R.drawOver = function (c, t) {
      if (R.lockOn && Math.floor(t * 10) % 2) ART.draw(c, 'bmfx_alert_red_incoming_projectile', G.player.x, G.player.y - 40, { s: 0.22 });
      if (R.stalled > 0 && Math.floor(t * 8) % 2) ART.draw(c, 'bmfx_alert_yellow_danger', R.x, R.y - 62, { s: 0.2 });
    };
    return R;
  };

  // shared with the dormant exhibit drawn before it wakes
  TD.drawExhibitTank = function (c, R, t, world, partPos, fwdFrom) {
    if (R.wrecked) { ART.draw(c, 'rzb_wreck', R.x, R.y, { a: R.a, s: S }); return; }
    const i = ((Math.round(R.a / (Math.PI / 4)) % 8) + 8) % 8, resid = M.wrap(R.a - i * Math.PI / 4), hk = 'rzb_hull_' + i;
    ART.draw(c, hk, R.x + 8, R.y + 11, { a: resid, s: S, tint: '#000000', alpha: 0.34 });
    const tr = ART.get('rzb_tread');
    if (tr) for (const side of [-1, 1]) {
      c.save(); c.translate(R.x, R.y); c.rotate(R.a); c.beginPath(); c.rect((side * 81 - 19) * S, -98 * S, 38 * S, 218 * S); c.clip();
      const off = (((R.travel || 0) * 1.6) % 42 + 42) % 42;
      for (let j = -4; j < 6; j++) { const tw = tr.sw * 0.62 * S, th = tr.sh * 0.62 * S; c.drawImage(tr.im, tr.sx, tr.sy, tr.sw, tr.sh, side * 81 * S - tw / 2, (j * 65 + off) * S - th / 2, tw, th); }
      c.restore();
    }
    const fl = R.flash || {};
    ART.draw(c, hk, R.x, R.y, { a: resid, s: S, flash: fl.hull ? 1 : (R.stalled > 0 && Math.floor(t * 10) % 2 ? 0.35 : 0) });
    for (let n = 0; n < 4; n++) { const mt = [[-65, -46], [65, -46], [-70, 33], [68, 33]][n], p = world(mt[0], mt[1]); ART.draw(c, 'rzb_rotor', p.x, p.y, { a: R.a + (R.travel || 0) / 25, s: 0.43 * S }); }
    for (const k of ['podL', 'podR']) if (R.parts[k] > 0) { const p = partPos[k](); ART.draw(c, 'rzb_missile_pod', p.x, p.y, { a: R.a, s: 0.55 * S, flash: fl[k] ? 1 : 0 }); }
    for (const side of ['L', 'R']) if (R.parts['gun' + side] > 0) { const p = partPos['gun' + side](), ga = R['ga' + side] == null ? R.a : R['ga' + side]; ART.draw(c, 'rzb_machinegun', p.x, p.y, { a: ga, s: S, ax: 64, ay: 65, flash: fl['gun' + side] ? 1 : 0 }); }
    if (R.parts.turret > 0) {
      const p = fwdFrom({ x: R.x, y: R.y }, R.turret, -(R.recoil || 0) * S), tk = R.parts.turret < R.max.turret * 0.5 ? 'rzb_turret_damaged' : 'rzb_turret';
      ART.draw(c, tk, p.x, p.y, { a: R.turret, s: S, ax: 128, ay: 128, flash: fl.turret ? 1 : 0 });
    }
    if (R.charge > 0) {
      const m = R.state === 'cannon' ? fwdFrom({ x: R.x, y: R.y }, R.turret, 142 * S) : { x: R.x, y: R.y };
      ART.draw(c, 'rzb_sonic_charge', m.x, m.y, { a: t * 2, s: (0.16 + R.charge * 0.5) * S, comp: 'lighter' });
    }
  };
}(window));
