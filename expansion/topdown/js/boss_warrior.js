/* THE WARRIOR: a separate HK-inspired encounter. Whole authored chassis,
 * helmet/torso and arms share explicit mount, hit and muzzle geometry. */
(function (root) {
  'use strict';
  const TD = root.TD, M = TD.M, FX = TD.FX, A = TD.Audio;
  const META = root.TD_GROUND_ART;
  const PARTS = {
    hull: { key: 'warrior_hull', x: 0, y: 0, hx: 0, hy: 12, r: 73, scale: 0.92 },
    helmet: { key: 'warrior_helmet', x: 0, y: -5, hx: 0, hy: -77, r: 42, scale: 0.68, mx: 0, my: -82 },
    armL: { key: 'warrior_arm_l', x: -69, y: -58, hx: -132, hy: -1, r: 34, scale: 0.5, mx: -151, my: 36 },
    armR: { key: 'warrior_arm_r', x: 71, y: -57, hx: 138, hy: 18, r: 34, scale: 0.5, mx: 158, my: 53 },
  };
  TD.WARRIOR_PARTS = PARTS;
  TD.makeWarrior = function (G, x, y) {
    const B = {
      name: 'THE WARRIOR', x, y: 150, a: 0, upper: 0, state: 'enter', t: 0, gauge: 0,
      parts: { hull: 155, helmet: 85, armL: 58, armR: 58 }, max: { hull: 155, helmet: 85, armL: 58, armR: 58 },
      flash: {}, dead: false, wrecked: false, deathT: 0, volleyT: 0, volley: 0, cycle: 0, phaseHistory: [],
      ramDir: 0, ramGoal: null, warn: null, cooldown: 0, targetX: 570, recoil: 0,
    };
    B.world = function (lx, ly, lower) {
      const a = lower ? B.a + Math.PI : B.upper, c = Math.cos(a), s = Math.sin(a);
      return { x: B.x + lx * c - ly * s, y: B.y + lx * s + ly * c };
    };
    B.position = key => B.world(PARTS[key].hx, PARTS[key].hy, key === 'hull');
    B.muzzle = key => B.world(PARTS[key].mx, PARTS[key].my);
    B.alive = () => !B.dead && B.state !== 'enter';
    B.hpFrac = () => Object.keys(B.parts).reduce((n, k) => n + Math.max(0, B.parts[k]), 0) / 356;
    B.aim = (sx, sy) => Object.keys(PARTS).filter(k => B.parts[k] > 0)
      .map(k => B.position(k)).sort((a, b) => M.dist(sx, sy, a.x, a.y) - M.dist(sx, sy, b.x, b.y))[0];
    function state(name) {
      B.state = name; B.t = 0; B.warn = null; B.volleyT = 0.15; B.volley = 0;
      B.phaseHistory.push(name);
    }
    function clearOwner(key) { G.eshots = G.eshots.filter(s => s.owner !== B || (key && s.part !== key)); }
    function detach(key, reward) {
      if (B.parts[key] <= 0) return;
      const d = PARTS[key], point = B.world(d.x, d.y);
      B.parts[key] = 0; clearOwner(key);
      // The exact mounted part becomes the fragment; no silhouette swap/fade.
      FX.fragment(d.key, point.x, point.y, B.upper, d.scale,
        key === 'armL' ? -95 : key === 'armR' ? 95 : 30, -35, META[d.key].anchor);
      FX.boom(point.x, point.y, 110, 'gfx_destruction_', 6);
      FX.boom(point.x, point.y, 70, 'nxp_dense_'); FX.concrete(point.x, point.y, 60);
      A.play('expB'); TD.Cam.kick(5); B.cooldown = 1.1;
      if (!B.dead) state('recover');
      if (reward) { G.score += 2500; G.say(key === 'helmet' ? 'HELMET DOWN - CHASSIS EXPOSED' : 'ARM DESTROYED', point); }
    }
    B.damage = function (key, amount) {
      if (!B.alive() || B.parts[key] <= 0) return;
      if (key === 'hull' && B.parts.helmet > 0) amount *= 0.18;
      B.flash[key] = 0.1; G.score += Math.round(amount * 8);
      if (key !== 'hull' && B.parts[key] <= amount) { detach(key, true); return; }
      B.parts[key] = Math.max(0, B.parts[key] - amount);
      if (key === 'hull' && B.parts.hull <= 0) {
        B.dead = true; B.warn = null; clearOwner(); state('dying'); A.stopMusic();
        for (const k of ['armL', 'armR', 'helmet']) detach(k, false);
        A.play('whiteout');
      }
    };
    B.hit = function (sx, sy, r, dmg, shot) {
      if (!B.alive()) return false;
      for (const key of ['armL', 'armR', 'helmet', 'hull']) if (B.parts[key] > 0) {
        const p = B.position(key);
        if (M.dist(sx, sy, p.x, p.y) >= PARTS[key].r + r) continue;
        if (shot) { const seen = shot.bossHits || (shot.bossHits = new Set()); if (seen.has(key)) return false; seen.add(key); }
        B.damage(key, dmg); return true;
      }
      return false;
    };
    B.blast = function (sx, sy, r, dmg) {
      if (!B.alive()) return;
      for (const key of ['armL', 'armR', 'helmet', 'hull']) if (B.parts[key] > 0) {
        const p = B.position(key); if (M.dist(sx, sy, p.x, p.y) < r + PARTS[key].r) B.damage(key, dmg * 0.6);
      }
    };
    function emit(part, kind, angle, speed, opts) {
      if (B.parts[part] <= 0 || B.dead) return;
      const p = part === 'hull' ? B.world(0, 67) : B.muzzle(part), [fx, fy] = M.fwd(angle);
      G.eshots.push(Object.assign({ k: kind, x: p.x, y: p.y, a: angle, vx: fx * speed, vy: fy * speed,
        dmg: kind === 'mg' ? 1 : 2, r: kind === 'mg' ? 4 : 5, life: 150, t: 0, owner: B, part }, opts));
      FX.flash(p.x, p.y, angle, kind === 'mg' ? 0.12 : 0.2);
      A.play(kind === 'missile' ? 'missile' : kind === 'laser' ? 'laser' : 'eshot', 0.65);
    }
    function volley(kind) {
      for (const key of ['armL', 'armR']) if (B.parts[key] > 0) {
        const p = B.muzzle(key), aim = M.angTo(p.x, p.y, G.player.x, G.player.y);
        if (kind === 'missile') emit(key, kind, aim + (key === 'armL' ? -0.18 : 0.18), 3.1, { homing: 42, turn: 0.025, accel: 0.035, max: 4.8, shootable: true });
        else for (const delta of [-0.18, 0, 0.18]) emit(key, 'mg', aim + delta, 3.4);
      }
      if (B.parts.armL <= 0 && B.parts.armR <= 0 && kind === 'mg') {
        const aim = M.angTo(B.x, B.y, G.player.x, G.player.y);
        for (const delta of [-0.24, 0.24]) emit('hull', 'mg', aim + delta, 3.2);
      }
    }
    function next() {
      const schedule = ['broadside', 'laser', 'rack', 'ram'];
      let pick = schedule[B.cycle++ % schedule.length];
      if (pick === 'laser' && B.parts.helmet <= 0) pick = 'broadside';
      if (pick === 'rack' && B.parts.armL <= 0 && B.parts.armR <= 0) pick = 'ram';
      B.targetX = B.x > 400 ? 215 : 585; state(pick);
      if (pick === 'ram') {
        B.ramGoal = { x: G.player.x, y: M.clamp(G.player.y, 200, 625) };
        B.ramDir = M.angTo(B.x, B.y, B.ramGoal.x, B.ramGoal.y);
      }
    }
    B.tick = function (dt) {
      B.t += dt; B.recoil *= 0.8;
      for (const k in B.flash) B.flash[k] = Math.max(0, B.flash[k] - dt);
      if (B.dead) {
        B.deathT += dt;
        if (B.deathT < 2.3 && Math.floor(B.deathT * 12) !== B.deathBeat) {
          B.deathBeat = Math.floor(B.deathT * 12);
          FX.boom(B.x + Math.sin(B.deathBeat * 2.4) * 60, B.y + Math.cos(B.deathBeat * 1.8) * 48, 90, 'gfx_destruction_', 6);
          A.play('expB', 0.65);
        }
        if (B.deathT >= 2.6 && !B.wrecked) {
          B.wrecked = true; FX.boom(B.x, B.y, 190, 'gfx_destruction_', 6); FX.concrete(B.x, B.y, 150);
          FX.ring(B.x, B.y, 1.1); TD.Cam.kick(9); A.play('expB'); G.bossDown();
        }
        return;
      }
      if (B.state === 'enter') {
        B.y = Math.min(y, B.y + 1.4); B.gauge = Math.min(1, B.t / 2.3);
        if (B.y >= y && B.gauge >= 1) { A.playMusic('boss2'); state('recover'); B.cooldown = 0.9; }
        return;
      }
      const toPlayer = M.angTo(B.x, B.y, G.player.x, G.player.y);
      B.upper = M.turnTo(B.upper, M.clamp(M.wrap(toPlayer), -0.45, 0.45), 0.012);
      if (B.state === 'recover') { B.cooldown -= dt; if (B.cooldown <= 0) next(); }
      else if (B.state === 'broadside') {
        const direction = B.targetX > B.x ? 1 : -1, heading = direction > 0 ? -Math.PI / 2 : Math.PI / 2;
        B.a = M.turnTo(B.a, heading, 0.06);
        if (Math.abs(M.wrap(B.a - heading)) < 0.24) B.x += direction * 1.7;
        if (B.t > 0.55 && (B.volleyT -= dt) <= 0) { B.volleyT = 0.32; volley('mg'); B.volley++; }
        if (Math.abs(B.x - B.targetX) < 10 || B.t > 3.8) { state('recover'); B.cooldown = 0.85; }
      } else if (B.state === 'laser') {
        // Committed alternating visor volleys. No charging orb or hidden beam.
        if (B.t < 0.5) B.laserAim = toPlayer;
        if (B.t >= 0.65 && (B.volleyT -= dt) <= 0 && B.volley < 6) {
          B.volleyT = 0.18; B.volley++;
          const aim = B.laserAim + (B.volley - 3.5) * 0.07;
          emit('helmet', 'laser', aim, 5.2); B.recoil = 2;
        }
        if (B.t > 2.25) { state('recover'); B.cooldown = 0.95; }
      } else if (B.state === 'rack') {
        if (B.t > 0.55 && (B.volleyT -= dt) <= 0 && B.volley < 4) {
          B.volleyT = 0.32; B.volley++; volley('missile');
        }
        if (B.t > 2.7) { state('recover'); B.cooldown = 1; }
      } else if (B.state === 'ram') {
        if (B.t < 1.15) {
          // Aim locks from the start: the player can leave the marked lane.
          B.a = M.turnTo(B.a, B.ramDir, 0.07);
          B.warn = B.t < 0.4 ? 'green' : B.t < 0.9 ? 'yellow' : 'red';
        } else {
          B.warn = null; const oldX = B.x, oldY = B.y, [fx, fy] = M.fwd(B.ramDir);
          B.x += fx * 6.4; B.y += fy * 6.4;
          TD.ramStructures(G, oldX, oldY, B.x, B.y, 79);
          FX.smoke(B.x - fx * 65, B.y - fy * 65, 0.15, 0.65);
          const edge = B.x < 165 || B.x > 635 || B.y < 230 || B.y > 565;
          if (edge || B.t > 1.95) {
            B.x = M.clamp(B.x, 165, 635); B.y = M.clamp(B.y, 230, 565);
            state('recover'); B.cooldown = 1.4; FX.concrete(B.x, B.y, 75); TD.Cam.kick(4);
          }
        }
      }
      if (B.state !== 'ram' && B.y > 335) B.y -= Math.min(1.2, B.y - 335);
      // Physical collisions always use the same mounted centers as hit tests.
      if (!G.player.dead) for (const key of ['hull', 'helmet', 'armL', 'armR']) if (B.parts[key] > 0) {
        const at = B.position(key), radius = PARTS[key].r;
        if (M.dist(at.x, at.y, G.player.x, G.player.y) < radius + G.player.r) {
          TD.hurtPlayer(G, B.state === 'ram' ? 4 : 2, G.player.x, G.player.y);
          TD.pushOut(G.player, { x: at.x, y: at.y, r: radius }); TD.World.collide(G.player, G.player.r, false);
        }
      }
    };
    B.drawUnder = function (ctx) {
      if (B.warn) {
        const [fx, fy] = M.fwd(B.ramDir);
        ART.draw(ctx, 'bmfx_fov_' + B.warn + '_tall', B.x + fx * 60, B.y + fy * 60,
          { a: B.ramDir + Math.PI, sx: 0.38, sy: 1.05, ay: 0, alpha: B.warn === 'green' ? 0.25 : 0.55 });
      }
    };
    B.draw = function (ctx) {
      if (B.wrecked) {
        ART.draw(ctx, 'warrior_wreck', B.x, B.y, { a: B.a + Math.PI, s: PARTS.hull.scale, ax: 127, ay: 128 }); return;
      }
      const hullKey = B.dead || B.parts.hull < B.max.hull * 0.5 ? 'warrior_damaged' : 'warrior_hull';
      const hullAnchor = META[hullKey].anchor;
      ART.draw(ctx, hullKey, B.x + 4, B.y + 7, { a: B.a + Math.PI, s: PARTS.hull.scale, ax: hullAnchor[0], ay: hullAnchor[1], tint: '#000000', alpha: 0.3 });
      ART.draw(ctx, hullKey, B.x, B.y, { a: B.a + Math.PI, s: PARTS.hull.scale, ax: hullAnchor[0], ay: hullAnchor[1], flash: B.flash.hull > 0 ? 1 : 0 });
      for (const key of ['armL', 'armR', 'helmet']) if (B.parts[key] > 0) {
        const d = PARTS[key], at = B.world(d.x, d.y), anchor = META[d.key].anchor;
        ART.draw(ctx, d.key, at.x, at.y, { a: B.upper, s: d.scale, ax: anchor[0], ay: anchor[1], flash: B.flash[key] > 0 ? 1 : 0 });
      }
    };
    B.drawOver = function (ctx) {
      if (B.dead || B.state === 'enter' || B.state === 'recover') return;
      const at = B.world(0, -158), color = B.state === 'ram' ? '#ffbc5b' : '#ffe0a0';
      ctx.save(); ctx.font = 'bold 9px BOFCommand, monospace'; ctx.textAlign = 'center'; ctx.fillStyle = color;
      ctx.strokeStyle = '#000'; ctx.lineWidth = 3; const label = B.state === 'broadside' ? 'BULLET VOLLEY' : B.state === 'laser' ? 'VISOR VOLLEY' : B.state === 'rack' ? 'MISSILE SALVO' : 'RAM - CLEAR THE LANE';
      ctx.strokeText(label, at.x, at.y); ctx.fillText(label, at.x, at.y); ctx.restore();
    };
    return B;
  };
})(window);
