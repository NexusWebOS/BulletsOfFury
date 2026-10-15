/* THE WARRIOR: a separate HK-inspired encounter. Whole authored chassis,
 * helmet/torso and arms share explicit mount, hit and muzzle geometry. */
(function (root) {
  'use strict';
  const TD = root.TD, M = TD.M, FX = TD.FX, A = TD.Audio;
  const META = root.TD_WARRIOR_ART.assets, PARTS = root.TD_WARRIOR_ART.rig;
  TD.WARRIOR_PARTS = PARTS;
  TD.makeWarrior = function (G, x, y) {
    y+=root.TD_WARRIOR_ART.spawnYOffset||0;
    const lowerAngle=PARTS.hull.baseAngle??Math.PI;
    const B = {
      name: 'THE WARRIOR', x, y: y - 64, homeY: y, a: 0, upper: 0, state: 'enter', t: 0, gauge: 0,
      parts: { hull: 220, helmet: 120, armL: 85, armR: 85 }, max: { hull: 220, helmet: 120, armL: 85, armR: 85 },
      armorFactor: .18, scale: .85,
      flash: {}, dead: false, wrecked: false, deathT: 0, volleyT: 0, volley: 0, cycle: 0, phaseHistory: [],
      ramDir: 0, ramGoal: null, warn: null, cooldown: 0, targetX: 570, recoil: 0,
    };
    B.world = function (lx, ly, lower) {
      const a = lower ? B.a + lowerAngle : B.upper, c = Math.cos(a), s = Math.sin(a);
      return { x: B.x + (lx * c - ly * s) * B.scale, y: B.y + (lx * s + ly * c) * B.scale };
    };
    B.position = key => B.world(PARTS[key].hx, PARTS[key].hy, key === 'hull');
    B.radiusFor = key => PARTS[key].r * B.scale;
    B.muzzle = key => B.world(PARTS[key].mx, PARTS[key].my);
    B.alive = () => !B.dead && B.state !== 'enter';
    B.retinaTargets=()=>Object.keys(PARTS).filter(k=>B.parts[k]>0).map(k=>({id:'warrior:'+k,point:()=>B.position(k),valid:()=>B.alive()&&B.parts[k]>0}));
    B.hpFrac = () => Object.keys(B.parts).reduce((n, k) => n + Math.max(0, B.parts[k]), 0) /
      Object.values(B.max).reduce((n, hp) => n + hp, 0);
    B.bounds = function () {
      const box = { left: Infinity, top: Infinity, right: -Infinity, bottom: -Infinity };
      for (const key of Object.keys(PARTS)) if (B.parts[key] > 0 || key === 'hull') {
        const d = PARTS[key], meta = META[d.key], at = key === 'hull' ? B : B.world(d.x, d.y);
        const angle = key === 'hull' ? B.a + lowerAngle : B.upper, c = Math.cos(angle), s = Math.sin(angle);
        for (const px of [meta.bounds[0], meta.bounds[2]]) for (const py of [meta.bounds[1], meta.bounds[3]]) {
          const lx = (px - meta.anchor[0]) * d.scale * B.scale, ly = (py - meta.anchor[1]) * d.scale * B.scale;
          const wx = at.x + lx * c - ly * s, wy = at.y + lx * s + ly * c;
          box.left = Math.min(box.left, wx); box.right = Math.max(box.right, wx);
          box.top = Math.min(box.top, wy); box.bottom = Math.max(box.bottom, wy);
        }
      }
      return box;
    };
    // Respect the authored module extents, including torso aim and sideways
    // chassis rotation. Collision circles alone do not contain the long arms.
    B.limitX = function (target) {
      const b = B.bounds(), gutter = 18;
      return M.clamp(target, B.x + gutter - b.left, B.x + TD.World.w - gutter - b.right);
    };
    B.followCamera = function (p, smoothing) {
      // Preserve 1:1 pixels. Frame the duel's visible parts and the player; when
      // they exceed the viewport, the player's escape route takes priority.
      const b = B.bounds(), vw = TD.VW / TD.Cam.zoom, vh = TD.VH / TD.Cam.zoom;
      const left = Math.min(b.left, p.x - 32), right = Math.max(b.right, p.x + 32);
      const top = Math.min(b.top, p.y - 32), bottom = Math.max(b.bottom, p.y + 32);
      const cx = M.clamp((left + right - vw) / 2, p.x - vw + 48, p.x - 48);
      const cy = M.clamp((top + bottom) / 2 - vh / 2, p.y - vh + 70, p.y - 82);
      TD.Cam.follow(cx + vw / 2, cy + vh / 2, smoothing ?? .12);
    };
    B.introProfile = () => ({ name: B.name,
      cardKey: 'od_warrior_card', views: root.TD_BOSS_INTRO_ART.turntable,
      classLabel: 'CLASS: SUPERHEAVY / FURY TANK HUNTER',
      total: Object.values(B.max).reduce((sum, hp) => sum + hp, 0),
      armor: Math.round((1 - B.armorFactor) * 100),
      targets: [
        { key: 'armL', name: 'LEFT TURRET', hp: B.max.armL, marker: [-155,255,90], detail: 'TWIN GUNS + HOMING MISSILE RACK' },
        { key: 'armR', name: 'RIGHT TURRET', hp: B.max.armR, marker: [155,255,90], detail: 'TWIN GUNS + HOMING MISSILE RACK' },
        { key: 'helmet', name: 'HEAD / HELMET', hp: B.max.helmet, marker: [0,270,0], detail: 'BREAK THE HEAD TO STRIP HULL GUARD' },
        { key: 'hull', name: 'BODY / HULL', hp: B.max.hull, marker: [0,150,40], detail: 'ARMORED DRIVE CHASSIS / RAM ENGINE' },
      ],
      attacks: ['MACHINE-GUN BROADSIDES', 'VISOR LASER VOLLEYS', 'HOMING MISSILE SALVOS', 'CONCRETE-SMASHING RAM'],
    });
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
      FX.fragment(d.key, point.x, point.y, B.upper, d.scale * B.scale,
        key === 'armL' ? -95 : key === 'armR' ? 95 : 30, -35, META[d.key].anchor);
      FX.boom(point.x, point.y, 110, 'gfx_destruction_', 6);
      FX.boom(point.x, point.y, 70, 'nxp_dense_'); FX.concrete(point.x, point.y, 60);
      A.play('expB'); TD.Cam.kick(5); B.cooldown = 1.1;
      if (!B.dead) state('recover');
      if (reward) { G.score += 2500; G.say(key === 'helmet' ? 'HELMET DOWN - CHASSIS EXPOSED' : 'ARM DESTROYED', point); }
    }
    B.damage = function (key, amount) {
      if (!B.alive() || B.parts[key] <= 0) return;
      if (key === 'hull' && B.parts.helmet > 0) amount *= B.armorFactor;
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
        if (M.dist(sx, sy, p.x, p.y) >= B.radiusFor(key) + r) continue;
        if (shot) { const seen = shot.bossHits || (shot.bossHits = new Set()); if (seen.has(key)) return false; seen.add(key); }
        B.damage(key, dmg); return true;
      }
      return false;
    };
    B.blast = function (sx, sy, r, dmg) {
      if (!B.alive()) return;
      for (const key of ['armL', 'armR', 'helmet', 'hull']) if (B.parts[key] > 0) {
        const p = B.position(key); if (M.dist(sx, sy, p.x, p.y) < r + B.radiusFor(key)) B.damage(key, dmg * 0.6);
      }
    };
    function emit(part, kind, angle, speed, opts) {
      if (B.parts[part] <= 0 || B.dead) return;
      const p = part === 'hull' ? B.world(0, -112, true) : B.muzzle(part), [fx, fy] = M.fwd(angle);
      G.eshots.push(Object.assign({ k: kind, x: p.x, y: p.y, a: angle, vx: fx * speed, vy: fy * speed,
        dmg: kind === 'mg' ? 1 : 2, r: kind === 'mg' ? 4 : 5, life: 150, t: 0, owner: B, part }, opts));
      FX.flash(p.x, p.y, angle, kind === 'mg' ? 0.12 : 0.2);
      A.play(kind === 'missile' ? 'missileLaunch' : kind === 'laser' ? 'enemyHeavyLaser' : 'quadFire', 0.8);
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
      B.targetX = B.limitX(B.x > 400 ? 215 : 585); state(pick);
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
        B.y = Math.min(y, B.y + 0.8); B.gauge = Math.min(1, B.t / 2.3);
        if (B.y >= y && B.gauge >= 1) { A.playMusic('warrior'); state('recover'); B.cooldown = 0.9; }
        return;
      }
      const toPlayer = M.angTo(B.x, B.y, G.player.x, G.player.y);
      B.upper = M.turnTo(B.upper, M.clamp(M.wrap(toPlayer), -0.45, 0.45), 0.012);
      if (B.state === 'recover') { B.cooldown -= dt; if (B.cooldown <= 0) next(); }
      else if (B.state === 'broadside') {
        const target = B.limitX(B.targetX);
        const direction = target > B.x ? 1 : -1, heading = direction > 0 ? -Math.PI / 2 : Math.PI / 2;
        B.a = M.turnTo(B.a, heading, 0.06);
        if (Math.abs(M.wrap(B.a - heading)) < 0.24) B.x += direction * 1.7;
        if (B.t > 0.55 && (B.volleyT -= dt) <= 0) { B.volleyT = 0.32; volley('mg'); B.volley++; }
        if (Math.abs(B.x - target) < 10 || B.t > 3.8) { state('recover'); B.cooldown = 0.85; }
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
          TD.ramStructures(G, oldX, oldY, B.x, B.y, B.radiusFor('hull'));
          FX.smoke(B.x - fx * 65, B.y - fy * 65, 0.15, 0.65);
          const edge = B.x < 195 || B.x > 605 || B.y < 300 || B.y > 565;
          if (edge || B.t > 1.95) {
            B.x = M.clamp(B.x, 195, 605); B.y = M.clamp(B.y, 300, 565);
            state('recover'); B.cooldown = 1.4; FX.concrete(B.x, B.y, 75); TD.Cam.kick(4);
          }
        }
      }
      if (B.state !== 'ram') B.y += M.clamp(B.homeY - B.y, -1.2, 1.2);
      B.x = B.limitX(B.x);
      // Physical collisions always use the same mounted centers as hit tests.
      if (!G.player.dead) for (const key of ['hull', 'helmet', 'armL', 'armR']) if (B.parts[key] > 0) {
        const at = B.position(key), radius = B.radiusFor(key);
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
          { a: B.ramDir + Math.PI, sx: 0.55, sy: 1.05, ay: 0, alpha: B.warn === 'green' ? 0.25 : 0.55 });
      }
    };
    B.draw = function (ctx) {
      if (B.wrecked) {
        const anchor = META.warrior_wreck.anchor;
        ART.draw(ctx, 'warrior_wreck', B.x, B.y, { a: B.a + lowerAngle, s: PARTS.hull.scale * B.scale, ax: anchor[0], ay: anchor[1] }); return;
      }
      const hullKey = B.dead || B.parts.hull < B.max.hull * 0.5 ? 'warrior_damaged' : 'warrior_hull';
      const hullAnchor = META[hullKey].anchor;
      ART.draw(ctx, hullKey, B.x + 4, B.y + 7, { a: B.a + lowerAngle, s: PARTS.hull.scale * B.scale, ax: hullAnchor[0], ay: hullAnchor[1], tint: '#000000', alpha: 0.3 });
      ART.draw(ctx, hullKey, B.x, B.y, { a: B.a + lowerAngle, s: PARTS.hull.scale * B.scale, ax: hullAnchor[0], ay: hullAnchor[1], flash: B.flash.hull > 0 ? 1 : 0 });
      for (const key of ['armL', 'armR', 'helmet']) if (B.parts[key] > 0) {
        const d = PARTS[key], at = B.world(d.x, d.y), anchor = META[d.key].anchor;
        ART.draw(ctx, d.key, at.x, at.y, { a: B.upper, s: d.scale * B.scale, ax: anchor[0], ay: anchor[1], flash: B.flash[key] > 0 ? 1 : 0 });
      }
    };
    B.drawOver = function (ctx) {
      if (B.dead || B.state === 'enter' || B.state === 'recover') return;
      const at = { x: TD.Cam.x + TD.VW - 10, y: TD.Cam.y + 20 }, color = B.state === 'ram' ? '#ffbc5b' : '#ffe0a0';
      ctx.save(); ctx.font = 'bold 9px BOFCommand, monospace'; ctx.textAlign = 'right'; ctx.fillStyle = color;
      ctx.strokeStyle = '#000'; ctx.lineWidth = 3; const label = B.state === 'broadside' ? 'BULLET VOLLEY' : B.state === 'laser' ? 'VISOR VOLLEY' : B.state === 'rack' ? 'MISSILE SALVO' : 'RAM - MOVE!';
      ctx.strokeText(label, at.x, at.y); ctx.fillText(label, at.x, at.y); ctx.restore();
    };
    return B;
  };
})(window);
