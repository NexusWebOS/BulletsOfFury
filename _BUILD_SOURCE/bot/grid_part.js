  /* ---- the space-time planner ------------------------------------------------------------------------
     A grid of positions around the ship (cell = one diagonal frame-step, so every move the DP allows is one the
     ship can make), and for each of the next H frames which cells are lethal (rasterised with the engine's own
     hit boxes) and which are merely close. A min-cost DP over (cell, frame) finds the cheapest path that is still
     alive at the horizon; its first step is the move. When no path lives long, the planner reports how long the
     best one lives, and the caller rolls. */
  const GR = {R: 0, N: 0, W: 0, occ: [], near: [], cost: null, nxt: null, par: [], soft: null, mask: null};
  function gridAlloc(R){
    if (GR.R === R) return;
    GR.R = R; GR.W = 2 * R + 1; GR.N = GR.W * GR.W;
    GR.occ = []; GR.near = []; GR.par = [];
    for (let k = 0; k <= H; k++) { GR.occ.push(new Uint8Array(GR.N)); GR.near.push(new Uint8Array(GR.N)); GR.par.push(new Int32Array(GR.N)); }
    GR.cost = new Float32Array(GR.N); GR.nxt = new Float32Array(GR.N); GR.soft = new Float32Array(GR.N); GR.mask = new Uint8Array(GR.N);
  }
  function gridPlan(L, Z, tx, ty, sp){
    const g = Math.max(2.2, sp / Math.SQRT2), R = Math.min(48, Math.ceil(H * sp / g) + 2);
    gridAlloc(R);
    const W = GR.W, N = GR.N, ox = player.x - R * g, oy = player.y - R * g;
    const ww = worldWidth(), y0 = PLAY.y + 12, y1 = PLAY.y + PLAY.h - 6, iv = (player.invuln | 0) - 1;
    for (let k = 1; k <= H; k++) { GR.occ[k].fill(0); GR.near[k].fill(0); }
    // the static soft field: edges, the top of the field, warned lanes, firewall lanes, keep-away rings
    const soft = GR.soft; soft.fill(0);
    const top = PLAY.y + PLAY.h * 0.38;
    for (let r = 0, c = 0; r < W; r++) {
      const y = oy + r * g;
      for (let q = 0; q < W; q++, c++) {
        const x = ox + q * g;
        if (x < 10 || x > ww - 10 || y < y0 || y > y1) { soft[c] = -1; continue; }   // off the field
        let s = 0;
        const sd = Math.min(x, ww - x); if (sd < 70) s += (70 - sd) * 0.45;
        const bd = y1 - y; if (bd < 30) s += (30 - bd) * 0.4;
        if (y < top) s += (top - y) * 3;
        for (const C of FB.cones) if (inCone(x, y, C, 10)) { s += (C.k > 0.3 || C.seen < FB.i) ? 60 : 14; break; }
        for (const lx of Z.lanes) { const d = Math.abs(x - lx); if (d < 120) s += (120 - d) * 0.05; }
        for (const A of Z.rzb) { const d = Math.hypot(x - A.x, y - A.y), R0 = A.r + 140; if (d < R0) s += (R0 - d) * 0.09; }
        if (Z.sub && !Z.rzb.length) {
          const S = Z.sub, ex = Math.max(0, Math.abs(x - S[0]) - S[4]), ey = Math.max(0, Math.abs(y - S[1]) - S[5]), gap = Math.hypot(ex, ey);
          if (gap < 90) s += (90 - gap) * 0.25;
        }
        soft[c] = s;
      }
    }
    // rasterise a box (centre, half extents) into frame k: lethal into occ, a margin into near
    function box(k, cx, cy, hx, hy, pad){
      const qa = Math.ceil((cx - hx - pad - ox) / g), qb = Math.floor((cx + hx + pad - ox) / g);
      const ra = Math.ceil((cy - hy - pad - oy) / g), rb = Math.floor((cy + hy + pad - oy) / g);
      if (qb < 0 || rb < 0 || qa >= W || ra >= W) return;
      const O = GR.occ[k], NE = GR.near[k];
      for (let r = Math.max(0, ra); r <= Math.min(W - 1, rb); r++) {
        const y = oy + r * g, inY = Math.abs(y - cy) < hy;
        for (let q = Math.max(0, qa); q <= Math.min(W - 1, qb); q++) {
          const c = r * W + q;
          if (inY && Math.abs(ox + q * g - cx) < hx) O[c] = 1; else if (NE[c] < 250) NE[c] += 1;
        }
      }
    }
    function cellTest(k0, k1, fn){              // a hazard that has no simple box: test every cell centre
      for (let r = 0, c = 0; r < W; r++) { const y = oy + r * g; for (let q = 0; q < W; q++, c++) { if (soft[c] < 0) continue; if (fn(ox + q * g, y)) for (let k = k0; k <= k1; k++) GR.occ[k][c] = 1; } }
    }
    // rounds, hulls, debris
    for (const T of L) {
      if (T.steer) {
        const S = T.steer; let x = T.x, y = T.y, ang = S.ang, spd = S.spd, t = S.t, committed = false;
        for (let k = 1; k <= H; k++) {
          t += 1 / 60;
          if (S.homing && !committed) { let tr = S.tr; if (S.swerve != null) tr = t < S.swerve ? S.trA : S.trB; const ta = Math.atan2(player.y - y, player.x - x); const da = ((ta - ang + Math.PI * 3) % (Math.PI * 2)) - Math.PI; ang += Math.max(-tr, Math.min(tr, da)); }
          if (S.lock && !committed) { const dxl = player.x - x, dyl = player.y - y; if (dxl * dxl + dyl * dyl < LOCK_COMMIT_PX * LOCK_COMMIT_PX) committed = true; else if (!S.homing) { const ta = Math.atan2(dyl, dxl); const da = ((ta - ang + Math.PI * 3) % (Math.PI * 2)) - Math.PI; ang += Math.max(-S.lockTurn, Math.min(S.lockTurn, da)); } }
          if (S.acc) spd = Math.min(S.max, spd + S.acc);
          const v = spd * S.eb, nx = x + Math.cos(ang) * v, ny = y + Math.sin(ang) * v;
          const infl = (S.homing || S.lock) && !committed ? Math.min(26, k * 0.9) : 0;
          if (k >= T.t0 && k <= T.t1) { box(k, nx, ny, T.wx + infl, T.wy + infl, 7); box(k, (x + nx) / 2, (y + ny) / 2, T.wx + infl, T.wy + infl, 0); }
          x = nx; y = ny;
        }
        continue;
      }
      for (let k = 1; k <= H; k++) {
        if (k < T.t0 || k > T.t1) continue;
        let px_, py_, px0, py0;
        if (T.sw) {
          const Wv = T.sw, f = (tt) => Math.sin(tt * SWIRL_HZ + Wv.ph);
          const d = (f(Wv.t + k / 60) - f(Wv.t)) * Wv.amp, d0 = (f(Wv.t + (k - 1) / 60) - f(Wv.t)) * Wv.amp;
          px_ = T.x + T.vx * k + Wv.px * d; py_ = T.y + T.vy * k + Wv.py * d; px0 = T.x + T.vx * (k - 1) + Wv.px * d0; py0 = T.y + T.vy * (k - 1) + Wv.py * d0;
        } else {
          const hk = 0.5 * k * k, h0 = 0.5 * (k - 1) * (k - 1);
          px_ = T.x + T.vx * k + T.ax * hk; py_ = T.y + T.vy * k + T.ay * hk; px0 = T.x + T.vx * (k - 1) + T.ax * h0; py0 = T.y + T.vy * (k - 1) + T.ay * h0;
        }
        if (T.ell) {
          const cx = px_, cy = py_, E = T.ell;
          const qa = Math.max(0, Math.ceil((cx - T.wx - ox) / g)), qb = Math.min(W - 1, Math.floor((cx + T.wx - ox) / g));
          const ra = Math.max(0, Math.ceil((cy - T.wy - oy) / g)), rb = Math.min(W - 1, Math.floor((cy + T.wy - oy) / g));
          for (let r = ra; r <= rb; r++) for (let q = qa; q <= qb; q++) {
            const ux = ox + q * g - cx, uy = oy + r * g - cy, ex = ux * E.c + uy * E.s, ey = -ux * E.s + uy * E.c, e = (ex / E.rw) ** 2 + (ey / E.rh) ** 2;
            if (e < 1) GR.occ[k][r * W + q] = 1; else if (e < 2) GR.near[k][r * W + q] += 1;
          }
          continue;
        }
        box(k, px_, py_, T.wx, T.wy, T.kind === 'e' ? 4 : 8);
        if (T.kind === 'b') {                       // the engine's swept step: a fast round fills its whole step
          const st = Math.max(Math.abs(px_ - px0) / T.wx, Math.abs(py_ - py0) / T.wy);
          if (st > 0.9) { const n = Math.ceil(st); for (let j = 1; j < n; j++) box(k, px0 + (px_ - px0) * j / n, py0 + (py_ - py0) * j / n, T.wx, T.wy, 0); }
        }
      }
    }
    // field hazards
    for (const Bm of Z.beams) cellTest(1, H, function(x, y){ const px = x - Bm[0], py = y - Bm[1], al = px * Bm[2] + py * Bm[3], ac = Math.abs(px * Bm[3] - py * Bm[2]); return al >= -10 && al <= Bm[5] && ac < Bm[4]; });
    for (const C of Z.cols) cellTest(1, H, function(x, y){ return Math.abs(x - C[0]) < C[1] && y > C[2] && y < C[3]; });
    for (const C of Z.circ) cellTest(1, H, function(x, y){ return (x - C[0]) * (x - C[0]) + (y - C[1]) * (y - C[1]) < C[2] * C[2]; });
    for (const Rr of Z.rects) { const k0 = Math.max(1, Rr[4]), k1 = Math.min(H, Rr[5]); if (k0 <= k1) cellTest(k0, k1, function(x, y){ return x > Rr[0] && x < Rr[1] && y > Rr[2] && y < Rr[3]; }); }
    for (const Lb of FB.beams) { const k1 = Math.min(H, Lb.k1 == null ? 8 : Lb.k1); cellTest(1, k1, function(x, y){ return segDist(x, y, Lb) < Lb.half; }); }
    for (const Wl of Z.walls) for (let k = 1; k <= H; k++) { const yk = Wl.y + Wl.vy * k, half = 51 * (0.9 + Math.min(1, Math.max(0, (Wl.t + k / 60) / FIRE_CROSS)) * 1.25) + 3; box(k, Wl.x, yk, half, half, 6); }
    if (Z.sub) { const S = Z.sub; for (let k = 1; k <= Math.min(H, 24); k++) box(k, S[0] + S[2] * k, S[1] + S[3] * k, S[4], S[5], 8); }
    for (const A of Z.rzb) {
      for (let k = 1; k <= H; k++) {
        const hx = A.x + A.vx * Math.min(k, 20), hy = A.y + A.vy * Math.min(k, 20), r2 = A.r * A.r;
        const qa = Math.max(0, Math.ceil((hx - A.r - ox) / g)), qb = Math.min(W - 1, Math.floor((hx + A.r - ox) / g));
        const ra = Math.max(0, Math.ceil((hy - A.r - oy) / g)), rb = Math.min(W - 1, Math.floor((hy + A.r - oy) / g));
        for (let r = ra; r <= rb; r++) for (let q = qa; q <= qb; q++) { const dx = ox + q * g - hx, dy = oy + r * g - hy; if (dx * dx + dy * dy < r2) GR.occ[k][r * W + q] = 1; }
      }
      for (const Wv of A.waves) for (let k = 1; k <= H; k++) {
        const rr = Wv.r + Wv.sp * k; if (rr > Wv.maxR) break;
        for (let r = 0, c = 0; r < W; r++) { const y = oy + r * g; for (let q = 0; q < W; q++, c++) {
          const x = ox + q * g, dd = Math.hypot(x - Wv.x, y - Wv.y);
          if (Math.abs(dd - rr) < Wv.half) { let hitw = true; try { hitw = rzbWaveAngleHit(Wv.w, rzbWrap(rzbAim(Wv.w, {x: x, y: y}) - Wv.w.a)); } catch (e) {} if (hitw) GR.occ[k][c] = 1; }
        } }
      }
    }
    // the boss hull: its own shape (bossHitTest), sampled once on a 2-cell lattice and carried along its velocity
    if (Z.boss) {
      const mask = GR.mask; mask.fill(0); let any = false;
      for (let r = 0; r < W; r += 2) { const y = oy + r * g; for (let q = 0; q < W; q += 2) { let h = false; try { h = !!bossHitTest(ox + q * g, y - 6); } catch (e) {}
        if (h) { any = true; for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) { const rr = r + a, qq = q + b; if (rr >= 0 && rr < W && qq >= 0 && qq < W) mask[rr * W + qq] = 1; } } } }
      if (any) for (let k = 1; k <= Math.min(H, 18); k++) {
        const sx = Math.round(Z.boss[0] * k / g), sy = Math.round(Z.boss[1] * k / g), O = GR.occ[k];
        for (let r = 0; r < W; r++) { const r2 = r - sy; if (r2 < 0 || r2 >= W) continue; for (let q = 0; q < W; q++) { const q2 = q - sx; if (q2 < 0 || q2 >= W) continue; if (mask[r2 * W + q2]) O[r * W + q] = 1; } }
      }
    }
    // the DP: min cost over (cell, frame), dead cells excluded once i-frames have run out
    const cost = GR.cost, nxt = GR.nxt;
    cost.fill(Infinity); const start = R * W + R; cost[start] = 0;
    let lastK = 0;
    for (let k = 1; k <= H; k++) {
      nxt.fill(Infinity);
      const O = GR.occ[k], NE = GR.near[k], P = GR.par[k], wk = 1 / (1 + k * 0.05), lethal = k > iv;
      let alive = false;
      for (let r = 0; r < W; r++) {
        const ra = r > 0 ? r - 1 : 0, rb = r < W - 1 ? r + 1 : W - 1;
        for (let q = 0; q < W; q++) {
          const c = r * W + q;
          if (soft[c] < 0) continue;
          if (lethal && O[c]) continue;
          const qa = q > 0 ? q - 1 : 0, qb = q < W - 1 ? q + 1 : W - 1;
          let bv = Infinity, bp = -1;
          for (let rr = ra; rr <= rb; rr++) for (let qq = qa; qq <= qb; qq++) { const n = rr * W + qq, v = cost[n]; if (v < bv) { bv = v; bp = n; } }
          if (bp < 0 || bv === Infinity) continue;
          nxt[c] = bv + (soft[c] + NE[c] * 26 + (O[c] ? 60 : 0)) * wk; P[c] = bp; alive = true;
        }
      }
      if (!alive) break;
      cost.set(nxt); lastK = k;
    }
    // the endpoint: the cheapest living cell at the deepest frame reached, plus the pull of the attack spot
    let bestC = -1, bestV = Infinity;
    for (let c = 0; c < N; c++) {
      if (cost[c] === Infinity) continue;
      const x = ox + (c % W) * g, y = oy + Math.floor(c / W) * g;
      const v = cost[c] + Math.hypot(x - tx, y - ty) * 0.9;
      if (v < bestV) { bestV = v; bestC = c; }
    }
    if (bestC < 0 || lastK < 1) return {dir: [0, 0], live: 0, cost: Infinity, end: null};
    let c = bestC;
    for (let k = lastK; k > 1; k--) c = GR.par[k][c];
    const dq = (c % W) - R, dr = Math.floor(c / W) - R;
    return {dir: [Math.sign(dq), Math.sign(dr)], live: lastK, cost: bestV, end: [ox + (bestC % W) * g, oy + Math.floor(bestC / W) * g]};
  }
