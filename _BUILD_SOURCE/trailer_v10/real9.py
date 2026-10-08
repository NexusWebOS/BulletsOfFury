"""real9.py - REAL GAMEPLAY for the v9 trailer takes (Mike, 0930: "you shouldnt be invisible taking bullets. real
gameplay my friend").

capture3's LIB stubs `playerHit` to nothing and its autopilot zeroes `player.invuln` and clears `player.dead` every
frame, so every v7/v8/v9 take flew an invincible ship straight through enemy fire. LIB_REAL is evaluated AFTER
capture3.LIB and capture9.LIB9 and undoes both:

  hits      the game's own `playerHit` is back - shields pop, i-frames blink, a lethal hit runs the real spin-out
            death (header rule) and the respawn. Only the GAME OVER is kept off the table: `run.lives` is held at
            >= 3 every frame, which is what keeps a take recording; the HUD's life counter is the one tell.
  dodge     the autopilot no longer flies a sine through the fire. Every frame it predicts each enemy round
            (`b.x += b.vx` per frame, the engine's own motion) and every enemy hull 2..26 frames ahead, scores the
            nine moves the input map can make at the ship's real speed (`playerBaseSpeed() * 1.35`, diagonals
            normalised - updatePlay's own maths) against those, adds the pull toward the take's mode target and a
            small cost for changing direction, and holds the cheapest. When every move is a hit inside 6 frames it
            barrel-rolls (a real double tap, so the 5 s roll cooldown applies).
  rearm     a death strips the gun to the default, exactly as in play; the take's loadout is re-applied when the
            pilot respawns so a boss take keeps showing the weapon it was set up to show.
  metrics   'hits' (cumulative), 'dd' (dead / spinning out), 'iv' (i-frames up) - edit9 penalises dead frames.
"""

LIB_REAL = r"""() => {
  if (window.__realHit) playerHit = window.__realHit;
  const R = window.__real = {hits: 0, deaths: 0, rolls: 0, dir: 4, armSpec: null, wasDead: false, rollAt: -999, plan: null};
  const _hit = playerHit;
  playerHit = function(){
    const dead0 = !!player.dead, iv0 = player.invuln | 0, sh0 = run.shield | 0;
    const r = _hit.apply(this, arguments);
    if (!dead0 && (player.dead || (player.invuln | 0) > iv0 || (run.shield | 0) < sh0)) R.hits++;
    if (!dead0 && player.dead) { R.deaths++; try { const st = String(new Error().stack).split('\n').slice(2, 5).map(x => x.trim().replace(/\(?https?:\/\/[^)]*\/([^/:]+):(\d+):\d+\)?/, '$1:$2')).join(' < '); (R.killers = R.killers || []).push(st.slice(0, 220)); } catch (e) {} }
    return r;
  };
  window.__armSpecSet = function(a){ R.armSpec = a; };

  const DIRS = [[-1,-1],[0,-1],[1,-1],[-1,0],[0,0],[1,0],[-1,1],[0,1],[1,1]];
  const KS = [2, 4, 6, 8, 11, 14, 18, 22, 26];
  const MOVE = ['a', 'd', 'w', 's'];
  function target(m, i){
    const t = i / 60, ww = worldWidth();
    let tx = player.x, ty = player.y;
    if (m === 'weave') {
      tx = ww / 2 + Math.sin(t * 0.9) * Math.min(150, ww * 0.24);
      ty = PLAY.y + PLAY.h * 0.76 + Math.sin(t * 1.7) * 28;
    } else if (m === 'boss') {
      const T = window.__tgt();
      tx = (T && isFinite(T.x)) ? T.x + Math.sin(t * 1.1) * 46 : ww / 2 + Math.sin(t * 0.8) * 90;
      ty = PLAY.y + PLAY.h * 0.80 + Math.sin(t * 1.5) * 16;
    } else if (m === 'hold') {
      tx = (window.__hx == null) ? player.x : window.__hx;
      ty = (window.__hy == null) ? player.y : window.__hy;
    } else if (m === 'gates') {
      let g = null;
      if (typeof s5run !== 'undefined' && s5run && !s5run.done && s5run.gates)
        for (const q of s5run.gates) { if (!q.passed && !q.missed) { g = q; break; } }
      tx = g ? g.x : ww / 2;
      ty = PLAY.y + PLAY.h * 0.72;
    }
    return [tx, ty];
  }
  function threats(){
    const L = [];
    const px = player.x, py = player.y, reach = 26 * 9;
    for (const b of eBullets) {
      if (!b || b.dead || b.reflected || b._friendly) continue;
      const vx = +b.vx || 0, vy = +b.vy || 0;
      const ax = (b._rpvx != null) ? Math.max(-0.6, Math.min(0.6, vx - b._rpvx)) : 0, ay = (b._rpvy != null) ? Math.max(-0.6, Math.min(0.6, vy - b._rpvy)) : 0;
      b._rpvx = vx; b._rpvy = vy;
      if (Math.abs(b.x - px) > reach + Math.abs(vx) * 26 + 40 || Math.abs(b.y - py) > reach + Math.abs(vy) * 26 + 40) continue;
      L.push([b.x, b.y, vx, vy, (b.w || 6) * 0.15 + 5, (b.h || 6) * 0.15 + 5, ax, ay]);
    }
    // stage-2 vent debris: thrown up and falling under DEBRIS_G (per-frame units), radius d.r + 8
    try { if (typeof fireDebris !== 'undefined') for (const d of fireDebris) {
      if (d.dead || d.delay > 0) continue;
      const g = (typeof DEBRIS_G !== 'undefined') ? DEBRIS_G : 0.25;
      L.push([d.x, d.y, d.vx, d.vy + g * 0.5, (d.r || 9) + 6, (d.r || 9) + 6, 0, g]);
    } } catch (e) {}
    for (const e of enemies) {
      if (!e || e.dead || e._dyingT != null || e.ground || e.prop) continue;
      const vx = (e._apx != null) ? e.x - e._apx : 0, vy = (e._apy != null) ? e.y - e._apy : 0;
      e._apx = e.x; e._apy = e.y;
      if (Math.abs(e.x - px) > 300 || Math.abs(e.y - py) > 300) continue;
      L.push([e.x, e.y, vx, vy, (e.w || 24) * 0.42 + 4, (e.h || 24) * 0.42 + 4, 0, 0]);
    }
    return L;
  }
  /* the hazards that are not rounds: the l23 boss beams (warned lanes, live after B.warm - avoided from 0.5 s before
     they open) and the boss / miniboss HULLS, tested through the game's own bossHitTest at the boss's predicted spot */
  function hazards(){
    const H = {beams: [], boss: null, sub: null};
    for (const o of [typeof boss !== 'undefined' ? boss : null, typeof subBoss !== 'undefined' ? subBoss : null]) {
      const B = o && !o.dead && o._l23Beam;
      if (!B || !B.slots || B.t < B.warm - 0.5 || B.t >= B.warm + B.active) continue;
      const half = B.width * 0.32 + 14, len = Math.max(VW, VH) * 1.25;
      for (let i = 0; i < B.slots.length; i++) {
        try { const p = shipBossMount(o, B.slots[i]), a = B.angles[i]; H.beams.push([p.x, p.y, Math.cos(a), Math.sin(a), half, len]); } catch (e) {}
      }
    }
    H.cols = [];        // vertical columns: [x, half, yTop, yBot] - hostile stage-2 vents and lane strikes
    H.circ = [];        // circles: [x, y, r] - targeted missile strikes
    try { if (typeof geysers !== 'undefined') for (const g of geysers) if (g.hostile && g.t < g.life)
      H.cols.push([g.x, geyserLane(g) * 0.75 + 12, g.y - GEYSER_H, g.y]); } catch (e) {}
    try { if (typeof groundTargetingFx !== 'undefined') for (const q of groundTargetingFx) {
      if (q.dead || q._fztEye) continue;
      if (q.kind === 'missile') H.circ.push([q.x, q.y, (q.radius || 30) + 12]);
      else H.cols.push([q.x, (q.radius || 30) + 12, q.lane ? -999 : q.y - (q.radius || 30) - 12, q.lane ? 9999 : q.y + (q.radius || 30) + 12]);
    } } catch (e) {}
    if (typeof boss !== 'undefined' && boss && bossActive && !boss.dead && typeof bossHitTest === 'function') {
      const vx = (boss._apx != null) ? boss.x - boss._apx : 0, vy = (boss._apy != null) ? boss.y - boss._apy : 0;
      boss._apx = boss.x; boss._apy = boss.y; H.boss = [vx, vy];
    }
    if (typeof subBoss !== 'undefined' && subBoss && subBossActive && !subBoss.dead && !subBoss.enter) {
      const sy = subBoss._drawY || subBoss.y;
      const vx = (subBoss._apx != null) ? subBoss.x - subBoss._apx : 0, vy = (subBoss._apy != null) ? sy - subBoss._apy : 0;
      subBoss._apx = subBoss.x; subBoss._apy = sy; H.sub = [subBoss.x, sy, vx, vy, subBoss.w / 2 + 16, subBoss.h / 2 + 16];
    }
    return H;
  }
  function cost(dx, dy, sp, L, tx, ty, H){
    const ww = worldWidth(), y0 = PLAY.y + 12, y1 = PLAY.y + PLAY.h - 6;
    const hx = (player._hx != null ? player._hx : 9), hy = (player._hy != null ? player._hy : 10);
    const l = Math.hypot(dx, dy) || 1, ux = dx / l * sp, uy = dy / l * sp;
    let c = 0, hit = 99;
    for (const k of KS) {
      const qx = Math.min(ww - 10, Math.max(10, player.x + ux * k)), qy = Math.min(y1, Math.max(y0, player.y + uy * k));
      const w = 1 / (1 + k * 0.07);
      for (const T of L) {
        const hk = 0.5 * k * k, ax = Math.abs(T[0] + T[2] * k + T[6] * hk - qx) / (hx + T[4]), ay = Math.abs(T[1] + T[3] * k + T[7] * hk - qy) / (hy + T[5]);
        const d = Math.max(ax, ay);
        if (d < 1) { c += 900 * w; if (k < hit) hit = k; }
        else if (d < 2.4) c += (2.4 - d) * 26 * w;
      }
      if (H) {
        for (const Bm of H.beams) {
          const px = qx - Bm[0], py = qy - Bm[1], al = px * Bm[2] + py * Bm[3], ac = Math.abs(px * Bm[3] - py * Bm[2]);
          if (al >= -10 && al <= Bm[5] && ac < Bm[4]) { c += 700 * w; if (k < hit) hit = k; }
        }
        if (H.boss && k <= 14) {
          let inHull = false; try { inHull = !!bossHitTest(qx - H.boss[0] * k, qy - 6 - H.boss[1] * k); } catch (e) {}
          if (inHull) { c += 800 * w; if (k < hit) hit = k; }
          else if (k <= 6) { try { if (bossHitTest(qx - H.boss[0] * k, qy - 34 - H.boss[1] * k)) c += 60 * w; } catch (e) {} }
        }
        for (const C of H.cols) if (Math.abs(qx - C[0]) < C[1] && qy > C[2] && qy < C[3]) { c += 500 * w; if (k < hit) hit = k; }
        for (const C of H.circ) if ((qx - C[0]) * (qx - C[0]) + (qy - C[1]) * (qy - C[1]) < C[2] * C[2]) { c += 500 * w; if (k < hit) hit = k; }
        if (H.sub) {
          const S = H.sub, ax = Math.abs(S[0] + S[2] * k - qx) / S[4], ay = Math.abs(S[1] + S[3] * k - qy) / S[5];
          if (Math.max(ax, ay) < 1) { c += 800 * w; if (k < hit) hit = k; }
        }
      }
    }
    const ex = player.x + ux * 14, ey = player.y + uy * 14;
    c += Math.hypot(ex - tx, ey - ty) * 0.09;
    if (player.x + ux * 8 < 30 || player.x + ux * 8 > ww - 30) c += 14;
    return [c, hit];
  }
  window.__auto = function(i){
    const K = Input.keys, m = window.__mode;
    const play = (typeof player !== 'undefined') && state === GS.PLAY;
    try { if (typeof run !== 'undefined' && run && (run.lives | 0) < 3) run.lives = 3; } catch (e) {}
    if (window.__burst) { const b = window.__burst; window.__fire = (i % (b[0] + b[1])) < b[0]; }
    if (!play || m === 'none') { for (const k of MOVE) K[k] = false; K.j = play && !!window.__fire; return; }
    // the respawn: put the take's loadout back once, the frame the pilot is flying again
    if (R.wasDead && !player.dead && R.armSpec) {
      try { const a = R.armSpec; for (let k = 0; k < a[1]; k++) applyPowerup({kind: 'weapon', wtype: a[0], wvar: a[2] || null, x: player.x, y: player.y}); floaters.length = 0; } catch (e) {}
    }
    R.wasDead = !!player.dead;
    K.j = !!window.__fire;
    if (player.dead) { for (const k of MOVE) K[k] = false; return; }
    if (m === 'hold' && window.__hy === -9999) {      // the charge wind-up: the take is steering, not dodging
      const dy = -9999 - player.y; K.a = K.d = false; K.w = dy < -5; K.s = false; return;
    }
    const tg = target(m, i), sp = ((typeof playerBaseSpeed === 'function') ? playerBaseSpeed() : 2.6) * 1.35;
    const L = threats(), HZ = hazards();
    if (window.__noDodge) {                      // the CONTROL arm: the old straight-to-target autopilot, real hits on
      const dx = tg[0] - player.x, dy = tg[1] - player.y;
      K.a = dx < -5; K.d = dx > 5; K.w = dy < -5; K.s = dy > 5; return;
    }
    let best = 4, bc = Infinity, allHit = true;
    for (let d = 0; d < 9; d++) {
      const r = cost(DIRS[d][0], DIRS[d][1], sp, L, tg[0], tg[1], HZ);
      let c = r[0] + (d === R.dir ? 0 : 4);
      if (r[1] > 6) allHit = false;
      if (c < bc) { bc = c; best = d; }
    }
    // the gates run is a line to hold, not a fight: dodge only what would actually land
    if (m === 'gates') {
      const dx = tg[0] - player.x, dy = tg[1] - player.y;
      if (bc < 600) { K.a = dx < -3; K.d = dx > 3; K.w = dy < -3; K.s = dy > 3; R.dir = 4; return; }
    }
    R.dir = best;
    const D = DIRS[best];
    K.a = D[0] < 0; K.d = D[0] > 0; K.w = D[1] < 0; K.s = D[1] > 0;
    // nothing escapes it in time: a real barrel roll (double tap toward the safer side; the game's cooldown applies)
    if (R.plan) {
      if (i >= R.plan[1]) { Input.injectTap(R.plan[0]); R.plan = null; }
    } else if (allHit && (L.length || HZ.beams.length || HZ.cols.length || HZ.circ.length || HZ.boss || HZ.sub) && i - R.rollAt > 40 && !player.roll && !player.somer) {
      const key = (D[0] < 0) ? 'a' : (D[0] > 0) ? 'd' : (player.x > worldWidth() / 2 ? 'a' : 'd');
      Input.injectTap(key); R.plan = [key, i + 3]; R.rollAt = i; R.rolls++;
    }
  };
  const _m = window.__metrics;
  window.__metrics = function(){
    const o = _m();
    o.killers = R.killers || [];
    o.hits = R.hits; o.deaths = R.deaths; o.rolls = R.rolls;
    o.dd = (player.dead || player._spin) ? 1 : 0;
    o.iv = (player.invuln | 0) > 0 ? 1 : 0;
    return o;
  };
  return true;
}"""
