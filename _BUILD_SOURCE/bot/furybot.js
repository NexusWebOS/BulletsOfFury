/* furybot.js - a Furious-difficulty autopilot that plays by the rules (Mike, 1014: "a strong BOT capable of
   playing on Furious Difficulty and able to live and win without cheating").

   WHAT IT MAY DO: press keys. Everything the bot does goes through Input.keys (held) and Input.injectTap (edges),
   the same two doors a keyboard uses. It READS game state freely - bullets, enemies, the boss - the way a player
   reads the screen - but it never WRITES a life, an i-frame, a weapon, a shield or a state.

   THE BRAIN, per PLAY frame:
     1. threats    every enemy round, debris chunk and enemy hull, with the engine's own hit rule:
                   |dx| < hx + b.w*0.15 and |dy| < hy + b.h*0.15 for rounds (the swept segment box is covered by
                   stepping every frame), |dx| < e.w/2 + hx-1 for hulls. Rounds move b.vx per frame at 60 Hz;
                   acceleration is estimated from the last frame (homing, gravity, easing).
     2. hazards    boss / miniboss hulls through the game's own bossHitTest, l23 warned beams, hostile geyser
                   columns, ground strikes, the Stage-2 vent debris.
     3. plans      9 directions x 9 directions x 2 switch points + "hold": two-leg plans flown frame by frame over
                   a 30-frame horizon at the ship's real speed (playerBaseSpeed()*1.35, diagonals normalised, the
                   field clamp - updatePlay's own maths). A plan is scored by its first predicted hit (earlier is
                   far worse), a near-miss margin, distance to the attack position, edges, and churn.
     4. escape     when every plan is hit inside ~8 frames: barrel roll (double tap, i-frames for the whole roll,
                   5 s cooldown) toward the safer side, else somersault (double tap UP, 7 s cooldown).
     5. offence    the trigger is held. The attack position sits under the boss's hittable mass (probed with
                   bossHitTest), else under the miniboss, else under the nearest live air target, low in the field.
                   Pickups within reach pull the position over. Against a boss or miniboss the Retina is tapped
                   to lock it and manual missiles are tapped while the stock lasts.
   Non-PLAY screens are advanced with Enter / J taps, never by setting state. */
(function(){
  if (window.FB && window.FB.__v === 3) return;
  const FB = window.FB = {__v: 3, hits: 0, deaths: 0, rolls: 0, somers: 0, missiles: 0, killers: [], plan: null, dir: [0, 0],
    rollAt: -9999, tapAt: -9999, ring: [], lockAt: -9999, mslAt: -9999, lastState: '', stateT: 0, log: [], i: 0, cont: 0, pauses: 0};
  const K = Input.keys;
  for (const k of ['a', 'd', 'w', 's', 'j', 'k', 'c', 'enter', 'h', 'y']) if (K[k] === undefined) K[k] = false;
  const MOVE = ['a', 'd', 'w', 's'];
  const DIRS = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [1, -1], [-1, 1], [1, 1]];
  const H = 30;                          // horizon, frames
  const SW = [5, 12];                    // where a two-leg plan changes direction

  /* ---- the real playerHit, counted ------------------------------------------------------------ */
  const _hit = playerHit;
  playerHit = function(){
    const dead0 = !!player.dead, sh0 = run.shield | 0, iv0 = player.invuln | 0;
    const r = _hit.apply(this, arguments);
    if (!dead0 && (player.dead || (run.shield | 0) < sh0 || (player.invuln | 0) > iv0)) FB.hits++;
    if (!dead0 && player.dead) {
      FB.deaths++;
      try {
        const st = String(new Error().stack).split('\n').slice(2, 6).map(x => x.trim().replace(/\(?https?:\/\/[^)]*\/([^/:]+):(\d+):\d+\)?/, '$1:$2')).join(' < ');
        const near = [];
        for (const b of eBullets) { if (!b || b.dead) continue; const dx = b.x - player.x, dy = b.y - player.y;
          const q = Math.max(Math.abs(dx) / (9 + (b.w || 6) * 0.15), Math.abs(dy) / (10 + (b.h || 6) * 0.15));
          if (q < 3) near.push([+q.toFixed(2), b.kind, Math.round(dx), Math.round(dy), +(b.vx || 0).toFixed(1), +(b.vy || 0).toFixed(1), b.w, b.h, b.homing ? 'H' : '', b._lockId != null ? 'L' : '', b._committed ? 'C' : '', +(b.t || 0).toFixed(2)]); }
        near.sort((a, b) => a[0] - b[0]);
        // forensic: did last frame's threat list, stepped one frame, overlap where the ship actually is now?
        let fx = null;
        try { if (FB.lastL) { let bq = 9; for (const T of FB.lastL) { if (T.kind !== 'b') continue;
          const x1 = T.x + T.vx + T.ax * 0.5, y1 = T.y + T.vy + T.ay * 0.5, q = Math.max(Math.abs(x1 - player.x) / T.wx, Math.abs(y1 - player.y) / T.wy);
          const sw = sweep(T.x, T.y, x1, y1, player.x, player.y, T.wx, T.wy); if (q < bq) { bq = q; fx = [+q.toFixed(2), sw ? 1 : 0, Math.round(T.x - player.x), Math.round(T.y - player.y), +T.vx.toFixed(1), +T.vy.toFixed(1), +T.wx.toFixed(1), +T.wy.toFixed(1), T.steer ? 1 : 0]; } } } } catch (e) { fx = String(e).slice(0, 60); }
        // the killer, by identity: was it in last frame's list, and where did we expect it?
        try { let kb = null, kq = 9; for (const b of eBullets) { if (!b || b.dead) continue; const q = Math.max(Math.abs(b.x - player.x) / (9 + (b.w || 6) * 0.15), Math.abs(b.y - player.y) / (10 + (b.h || 6) * 0.15)); if (q < kq) { kq = q; kb = b; } }
          if (kb) { const T = FB.lastL ? FB.lastL.find(t => t.b === kb) : null;
            FB.kid = {kind: kb.kind, q: +kq.toFixed(2), inL: !!T, exp: T ? [Math.round(T.x + T.vx + T.ax / 2 - player.x), Math.round(T.y + T.vy + T.ay / 2 - player.y), +T.wx.toFixed(1), +T.wy.toFixed(1), T.steer ? 'S' : ''] : null, now: [Math.round(kb.x - player.x), Math.round(kb.y - player.y)], v: [+(kb.vx || 0).toFixed(2), +(kb.vy || 0).toFixed(2)], keys: Object.keys(kb).filter(k => k[0] === '_' && !/^_fb/.test(k)).slice(0, 16)}; } } catch (e) { FB.kid = String(e).slice(0, 80); }
        FB.fx = fx; FB.fxL = FB.lastL ? FB.lastL.length : -1; FB.fxPlay = FB.lastPlayI; FB.fxI = FB.i;
        FB.killers.push({st: st.slice(0, 260), stage: run.stage, t: +(stageTimer || 0).toFixed(1), boss: !!(bossActive && boss), sub: !!(subBossActive && subBoss), x: Math.round(player.x), y: Math.round(player.y), near: near.slice(0, 6), sb: (subBossActive && subBoss) ? {k: subBoss.kind, x: Math.round(subBoss.x), y: Math.round(subBoss.y), dy: subBoss._drawY != null ? Math.round(subBoss._drawY) : null, w: subBoss.w, h: subBoss.h, en: !!subBoss.enter, f: Object.keys(subBoss).filter(k => /^_[a-z0-9]{2,6}$/i.test(k) && subBoss[k] === true).slice(0, 12)} : null,
          ring: FB.ring.slice(-24), bs: (bossActive && boss) ? {k: boss.kind, x: Math.round(boss.x), y: Math.round(boss.y), w: boss.w, h: boss.h} : null, zsub: FB.zsub, dir: FB.dir, lastFirst: FB.lastFirst, roll: FB.i - FB.rollAt, kid: FB.kid, gt: (typeof groundTargetingFx !== 'undefined') ? groundTargetingFx.slice(0, 6).map(q => [q.kind, Math.round(q.x), Math.round(q.y), +q.t.toFixed(2), q.warn, q.active, +(q.delay || 0).toFixed(2), q.lane ? 1 : 0, q.radius, q.track ? 1 : 0, q.trackFor, q.impact ? 1 : 0]) : null, bh: (bossActive && boss) ? {now: (() => { try { return !!bossHitTest(player.x, player.y - 6); } catch (e) { return 'x'; } })(), c: FB.lastBossC, v: FB.lastBossV, n: boss._fbcn, bx: Math.round(boss.x), by: Math.round(boss.y), dyb: boss._drawY != null ? Math.round(boss._drawY) : null, hm: !!boss._hammer, st: boss._hammer ? boss._hammer.state : (boss._ovState || boss.mode || null)} : null, fx: FB.fx, fxL: FB.fxL, fxPlay: FB.fxPlay, fxI: FB.fxI, pp: FB.pp ? FB.pp.map(Math.round) : null});
      } catch (e) {}
    }
    return r;
  };

  /* ---- the warnings on screen: every shared green/yellow/red FOV the game draws ------------------------- */
  FB.cones = [];
  if (!window.__fbFovWrapped) {
    window.__fbFovWrapped = true;
    const _fov = l23FovDraw;
    l23FovDraw = function(b, B, i, p, k, lane){
      try {
        const a = B.angles[i], dn = Math.sin(a), F = (typeof L23_FOV !== 'undefined' && L23_FOV[B.family]) || {minFar: 60, far: 2.2};
        const L = (Number.isFinite(B.len) && B.len > 0) ? Math.max(36, B.len) : Math.max(120, dn > 0.25 ? (VH - p.y) / dn : Math.max(VW, VH) * 1.25);
        const far = Math.max(F.minFar || 60, lane * (F.far || 2.2));
        if (isFinite(p.x) && isFinite(p.y) && isFinite(a)) FB.coneIn.push({x: p.x, y: p.y, dx: Math.cos(a), dy: Math.sin(a), L, lane: lane || 20, far, k: +k || 0, o: b, id: i});
      } catch (e) {}
      return _fov.apply(this, arguments);
    };
  }
  FB.coneIn = [];
  /* ---- the beams on screen: every authored boss beam goes through av3Beam. Its draw transform is mapped back to
     the world through the matrix drawBullets runs under (a world-space draw), so a beam drawn inside a local
     translate still lands where it really is. */
  FB.beamIn = []; FB.beams = [];
  if (!window.__fbBeamWrapped && typeof av3Beam === 'function') {
    window.__fbBeamWrapped = true;
    const _db = drawBullets;
    drawBullets = function(){ try { FB.wm = ctx.getTransform(); } catch (e) {} return _db.apply(this, arguments); };
    const _av = av3Beam;
    av3Beam = function(g, x, y, angle, length, width, color, t, alpha){
      try {
        if (FB.wm && length > 0 && width > 0 && (alpha == null || alpha > (FB.alphaMin == null ? 0.45 : FB.alphaMin))) {
          const M = g.getTransform(), inv = FB.wm.inverse();
          const P = (px, py) => { const cx = M.a * px + M.c * py + M.e, cy = M.b * px + M.d * py + M.f; return [inv.a * cx + inv.c * cy + inv.e, inv.b * cx + inv.d * cy + inv.f]; };
          const a = P(x, y), b = P(x + Math.cos(angle) * length, y + Math.sin(angle) * length);
          const sc = Math.hypot(M.a, M.b) / Math.max(1e-6, Math.hypot(FB.wm.a, FB.wm.b));
          if (isFinite(a[0]) && isFinite(b[1]) && Math.hypot(a[0] - player.x, a[1] - player.y) > 34)
            FB.beamIn.push({x: a[0], y: a[1], ex: b[0], ey: b[1], half: width * sc * 0.5 + 6});
        }
      } catch (e) {}
      return _av.apply(this, arguments);
    };
  }
  function sweep(x0, y0, x1, y1, cx, cy, hx, hy){
    let lo = 0, hi = 1;
    const dx = x1 - x0, dy = y1 - y0;
    if (Math.abs(dx) < 1e-9) { if (Math.abs(x0 - cx) > hx) return false; }
    else { let a = (cx - hx - x0) / dx, z = (cx + hx - x0) / dx; if (a > z) { const t = a; a = z; z = t; } lo = Math.max(lo, a); hi = Math.min(hi, z); if (lo > hi) return false; }
    if (Math.abs(dy) < 1e-9) { if (Math.abs(y0 - cy) > hy) return false; }
    else { let a = (cy - hy - y0) / dy, z = (cy + hy - y0) / dy; if (a > z) { const t = a; a = z; z = t; } lo = Math.max(lo, a); hi = Math.min(hi, z); if (lo > hi) return false; }
    return true;
  }
  function segDist(x, y, L){ const dx = L.ex - L.x, dy = L.ey - L.y, d = dx * dx + dy * dy, u = d ? Math.max(0, Math.min(1, ((x - L.x) * dx + (y - L.y) * dy) / d)) : 0; return Math.hypot(x - L.x - dx * u, y - L.y - dy * u); }
  // the Hammer donor's chromium rift on the final boss (hardcorps_finale_1007): a pull, a lethal core, forked lanes
  function finalRift(){
    try { const C = boss && bossActive && !boss.dead && boss._r30 && boss._r30.hc7Rift; return C && (C.phase === 'raise' || C.phase === 'active') ? C : null; } catch (e) { return null; }
  }
  // every Warhive shot list alive: the boss's own, and any copy the final boss is wearing as a donor form
  function warhiveShots(){
    const out = [];
    try { if (boss && boss._whv && boss._whv.shots) out.push(boss._whv.shots); } catch (e) {}
    try { const J = typeof j3State === 'function' ? j3State(boss) : null, D = J && J.gp4Donors;
      if (D) for (const k in D) { const p = D[k] && D[k].p; if (p && p._whv && p._whv.shots && out.indexOf(p._whv.shots) < 0) out.push(p._whv.shots); } } catch (e) {}
    return out;
  }
  function ingestBeams(){
    FB.beams = FB.beamIn; FB.beamIn = [];
    try { if (typeof S81003 !== 'undefined') for (const q of S81003.beams) if (q.t < q.dur) FB.beams.push({x: q.x, y: q.y, ex: q.ex, ey: q.ey, half: q.width * 0.5 + 6, k1: Math.ceil((q.dur - q.t) * 60) + 1}); } catch (e) {}
    // the final boss's chromium rift: its forked lightning lanes (tell .90 s, live to 1.07 s), drawn from core to rim
    try { const C = finalRift(); if (C && C.lanes) for (const L of C.lanes) if (L.age < 1.07) FB.beams.push({x: L.x, y: L.y, ex: L.ex, ey: L.ey, half: L.width * 0.5 + 3 + 10, k1: Math.ceil((1.07 - L.age) * 60) + 2}); } catch (e) {}
  }
  function ingestCones(){
    // a warned lane stays dangerous for ~1.1 s after its last warning frame: the release follows the warning
    const keep = [];
    for (const C of FB.cones) if (C.until > FB.i && !FB.coneIn.some(N => N.o === C.o && N.id === C.id)) keep.push(C);
    for (const N of FB.coneIn) { N.until = FB.i + 66; N.seen = FB.i; keep.push(N); }
    FB.cones = keep.slice(-24); FB.coneIn = [];
  }
  function inLane(qx, qy, C){
    const rx = qx - C.x, ry = qy - C.y, al = rx * C.dx + ry * C.dy;
    if (al < -14 || al > C.L + 24) return false;
    return Math.abs(rx * C.dy - ry * C.dx) < C.lane * 0.5 + 11;
  }
  function inCone(qx, qy, C, pad){
    const rx = qx - C.x, ry = qy - C.y, al = rx * C.dx + ry * C.dy;
    if (al < -14 || al > C.L + 24) return false;
    const ac = Math.abs(rx * C.dy - ry * C.dx), f = Math.max(0, Math.min(1, al / Math.max(1, C.L)));
    return ac < (C.lane * 0.5 + (C.far * 0.5 - C.lane * 0.5) * f) * 0.85 + pad;
  }
  /* ---- threat collection ------------------------------------------------------------------------ */
  // the bank narrows the hitbox (player._hx = 9*wf), but the bank follows the move the bot is about to choose:
  // plan with the widest box the ship can have
  function hxy(){ return [Math.max(9, player._hx || 0), Math.max(10, player._hy || 0)]; }
  function threats(){
    const L = [], px = player.x, py = player.y, R = 420;
    const [hx, hy] = hxy();
    for (const b of eBullets) {
      if (!b || b.dead || b.reflected || b._friendly) continue;
      const vx = +b.vx || 0, vy = +b.vy || 0;
      let ax = 0, ay = 0, om = 0, ds = 0;
      if (b._fbvx != null) {
        ax = Math.max(-0.8, Math.min(0.8, vx - b._fbvx)); ay = Math.max(-0.8, Math.min(0.8, vy - b._fbvy));
        const pv = Math.hypot(b._fbvx, b._fbvy), cv = Math.hypot(vx, vy);
        if (pv > 0.05 && cv > 0.05) { om = Math.max(-0.12, Math.min(0.12, Math.atan2(b._fbvx * vy - b._fbvy * vx, b._fbvx * vx + b._fbvy * vy))); ds = Math.max(-0.4, Math.min(0.4, cv - pv)); }
      }
      b._fbvx = vx; b._fbvy = vy;
      if (!isFinite(b.x) || !isFinite(b.y)) continue;
      if (Math.abs(b.x - px) > R + Math.abs(vx) * H || Math.abs(b.y - py) > R + Math.abs(vy) * H) continue;
      let wx = hx + (b.w || 6) * 0.15, wy = hy + (b.h || 6) * 0.15;
      if (b.kind === 'mechmortar') { // lands on (tx,ty) and hurts within 30
        const left = Math.max(1, Math.round(((b.life || 1.25) - (b.t || 0)) * 60));
        L.push({x: b.tx, y: b.ty, vx: 0, vy: 0, ax: 0, ay: 0, wx: 30, wy: 30, t0: left - 1, t1: left + 1, kind: 'mortar'});
        continue;
      }
      if (b._hammerLaser || b._frostNoseLaser || b._pt11Wave) { wx += 10; wy += 10; }
      const T = {x: b.x, y: b.y, vx, vy, ax, ay, wx, wy, t0: 0, t1: 999, kind: 'b', b: b};
      if (b._pt11Wave) { T.wave = {ang: b.ang, sc: b._pt11Scale}; T.wx = 100 * (b._pt11Scale || 0.64) + 20; T.wy = T.wx; }
      if (b._ovSonicWave) {
        const a = b._south ? 0 : b.ang - Math.PI / 2;
        T.ell = {c: Math.cos(a), s: Math.sin(a), rw: (b._waveW || b.w) * 0.42 + hx + 4, rh: (b._waveH || b.h) * 0.32 + hy + 4};
        T.wx = T.ell.rw + T.ell.rh; T.wy = T.wx;      // the bounding box, for the quick reject
      }
      // the game's own missile motion (updatePlay's steering block): heading + speed, steering toward the ship
      const missile = (b._shootable || b.kind === 'emissile' || b.kind === 's1jungleMissile') && (!b._energyOrdnance || b.homing) &&
        !(typeof enemyOrdnanceCanIntercept === 'function' && !enemyOrdnanceCanIntercept(b));
      if (missile) {
        const eb = (typeof DIFF !== 'undefined' && DIFF) ? DIFF.ebSpeed : 1;
        const S = {ang: Math.atan2(vy, vx), spd: b.spd || 2.7, acc: b._accel || 0, max: b._maxspd || 4.0, eb, tr: 0, homing: false, lock: false, lockTurn: b._lockTurn || LOCK_TURN, t: b.t || 0};
        if (b.homing && !b._committed && (run.stage === 1 || b._frostHoming)) {
          S.homing = true; S.tr = b.turn || 0.05;
          if (b._swerve != null) { S.swerve = b._swerve; S.trA = b.turn || 0.012; S.trB = b._turnLock || 0.085; }
        }
        if (b._lockId && !b._committed) { const Lk = lockById(b._lockId); if (Lk && Lk.state === 'locked') S.lock = true; }
        if (S.homing || S.lock || S.acc) { T.steer = S; T.ax = T.ay = 0; }
      } else if ((b.kind === 'fireorb' || b._reaverOrb) && !b._committed) {
        // the Reaver / fire orb: homes far, commits for good inside FIREORB_COMMIT (updatePlay's own rule)
        T.steer = {ang: Math.atan2(vy, vx), spd: b.spd || 2.6, acc: 0, max: 99, eb: (typeof DIFF !== 'undefined' && DIFF) ? DIFF.ebSpeed : 1, tr: FIREORB_TURN, homing: true, lock: false, lockTurn: 0, t: b.t || 0, commitR: FIREORB_COMMIT};
        T.ax = T.ay = 0;
      } else if (b.kind === 'groundup' && !b.mg) {
        T.steer = {ang: Math.atan2(vy, vx), spd: Math.hypot(vx, vy), acc: 0, max: 99, eb: 1, tr: 0.03, homing: true, lock: false, lockTurn: 0, t: b.t || 0};
        T.ax = T.ay = 0;
      } else if (b._swirl) {
        const a = Math.atan2(vy, vx);
        T.sw = {px: Math.cos(a - Math.PI / 2), py: Math.sin(a - Math.PI / 2), ph: b._swPh || 0, amp: (b._swAmp || 1) * SWIRL_AMP, t: b.t || 0};
        T.ax = T.ay = 0;
      }
      // the path, flown frame by frame: a round turning at its measured rate and changing speed at its measured rate
      // (curving, homing-ish and accelerating rounds), capped so a short-lived change is not extrapolated forever
      if (!T.steer && !T.sw && (Math.abs(om) > 0.002 || Math.abs(ds) > 0.01)) {
        const P = new Float32Array(2 * (H + 1)); let x = b.x, y = b.y, a = Math.atan2(vy, vx), sp = Math.hypot(vx, vy);
        const cap = Math.min(14, Math.max(sp * 2.5, sp + Math.max(0, ds) * 40)), lo = Math.max(0.3, sp * 0.3);
        P[0] = x; P[1] = y;
        for (let k = 1; k <= H; k++) { a += om; sp = Math.max(lo, Math.min(cap, sp + ds)); x += Math.cos(a) * sp; y += Math.sin(a) * sp; P[2 * k] = x; P[2 * k + 1] = y; }
        T.path = P; T.ax = T.ay = 0;
      }
      L.push(T);
    }
    try { if (typeof fireDebris !== 'undefined') for (const d of fireDebris) {
      if (d.dead || d.delay > 0) continue;
      const g = (typeof DEBRIS_G !== 'undefined') ? DEBRIS_G : 0.25;
      L.push({x: d.x, y: d.y, vx: d.vx, vy: d.vy, ax: 0, ay: g, wx: (d.r || 9) + 8, wy: (d.r || 9) + 8, t0: 0, t1: 999, kind: 'd'});
    } } catch (e) {}
    for (const e of enemies) {
      if (!e || e.dead || e._dyingT != null || e._noHit) continue;
      if (!isFinite(e.x) || !isFinite(e.y)) continue;
      const vx = (e._fbpx != null) ? e.x - e._fbpx : 0, vy = (e._fbpy != null) ? e.y - e._fbpy : 0;
      e._fbpx = e.x; e._fbpy = e.y;
      if (Math.abs(e.x - px) > 360 || Math.abs(e.y - py) > 360) continue;
      L.push({x: e.x, y: e.y, vx: Math.max(-12, Math.min(12, vx)), vy: Math.max(-12, Math.min(12, vy)), ax: 0, ay: 0,
              wx: (e.w || 20) / 2 + hx - 1, wy: (e.h || 20) / 2 + hy - 2, t0: 0, t1: 999, kind: 'e'});
    }
    return L;
  }
  function hazards(){
    const Z = {beams: [], cols: [], circ: [], rects: [], mcirc: [], boss: null, sub: null};
    for (const o of [typeof boss !== 'undefined' ? boss : null, typeof subBoss !== 'undefined' ? subBoss : null]) {
      const B = o && !o.dead && o._l23Beam;
      if (!B || !B.slots || B.t < B.warm - 0.6 || B.t >= B.warm + B.active) continue;
      const half = B.width * 0.32 + 14, len = Math.max(VW, VH) * 1.3;
      for (let i = 0; i < B.slots.length; i++) {
        try { const p = shipBossMount(o, B.slots[i]), a = B.angles[i]; Z.beams.push([p.x, p.y, Math.cos(a), Math.sin(a), half, len]); } catch (e) {}
      }
    }
    try { if (typeof geysers !== 'undefined') for (const g of geysers) if (g.hostile && g.t < g.life)
      Z.cols.push([g.x, geyserLane(g) * 0.75 + 12, g.y - GEYSER_H, g.y]); } catch (e) {}
    try { if (typeof zoneCols !== 'undefined') for (const c of zoneCols) if (c && c.hostile && c.t < c.warn + c.life) {
      const k0 = Math.max(1, Math.round((c.warn - c.t) * 60) - 4), k1 = Math.round((c.warn + c.life - c.t) * 60) + 2;
      Z.rects.push([c.x0 + 2, c.x0 + c.w - 2, -999, 9999, k0, k1]);
    } } catch (e) {}
    try { if (typeof groundTargetingFx !== 'undefined') for (const q of groundTargetingFx) {
      if (q.dead || q._fztEye || q.t > (q.delay || 0) + q.warn + (q.active || 0.2) + 0.05) continue;
      // lethal only while it strikes ([warn, warn+active]); while it still tracks the ship it is not a place to avoid
      const k0 = Math.max(1, Math.ceil(((q.delay || 0) + q.warn - q.t) * 60) - 2), k1 = k0 + Math.ceil((q.active || 0.2) * 60) + 4;
      if (q.track && q.t < q.warn * (q.trackFor == null ? 0.56 : q.trackFor) && k0 > 12) continue;
      const r = (q.radius || 30) + 8;
      if (q.kind === 'missile') Z.circ.push([q.x, q.y, r, k0, k1]);
      else { const ry = Math.max(32, q.radius || 30) + 8; Z.rects.push([q.x - r, q.x + r, q.lane ? -999 : q.y - ry, q.lane ? 9999 : q.y + ry, k0, k1]); }
    } } catch (e) {}
    if (typeof boss !== 'undefined' && boss && bossActive && !boss.dead && typeof bossHitTest === 'function') {
      // where the hull really is: the centroid of the boss's own hit shape on a 16 px lattice over the view
      let sx = 0, sy = 0, n = 0;
      const L0 = camLeftX(), R0 = camRightX();
      for (let y = PLAY.y; y < PLAY.y + PLAY.h; y += 16) for (let x = L0; x < R0; x += 16) { let h = false; try { h = !!bossHitTest(x, y); } catch (e) {} if (h) { sx += x; sy += y; n++; } }
      // fallback: the boss's own position fields (a hull entering or leaving the view changes the centroid's sample)
      const byy = boss._drawY != null ? boss._drawY : boss.y;
      let vx = boss._fbpx != null ? boss.x - boss._fbpx : 0, vy = boss._fbpy != null ? byy - boss._fbpy : 0;
      boss._fbpx = boss.x; boss._fbpy = byy;
      if (Math.hypot(vx, vy) > 40) { vx = 0; vy = 0; }
      if (n) { const cx = sx / n, cy = sy / n; if (boss._fbcx != null && boss._fbcn && Math.abs(n - boss._fbcn) < Math.max(4, n * 0.3)) { vx = cx - boss._fbcx; vy = cy - boss._fbcy; } boss._fbcx = cx; boss._fbcy = cy; boss._fbcn = n; Z.bossC = [cx, cy]; }
      Z.boss = [Math.max(-14, Math.min(14, vx)), Math.max(-14, Math.min(14, vy))];
    }
    if (typeof subBoss !== 'undefined' && subBoss && subBossActive && !subBoss.dead && !subBoss.enter && !subBoss._jcGhost && !subBoss._s4MiniSafe) {
      const sy = subBoss._drawY || subBoss.y;
      const vx = (subBoss._fbpx != null) ? subBoss.x - subBoss._fbpx : 0, vy = (subBoss._fbpy != null) ? sy - subBoss._fbpy : 0;
      subBoss._fbpx = subBoss.x; subBoss._fbpy = sy;
      Z.sub = [subBoss.x, sy, Math.max(-10, Math.min(10, vx)), Math.max(-10, Math.min(10, vy)), subBoss.w / 2 + 12, subBoss.h / 2 + 12];
    }
    // timed rectangles [x0,x1,y0,y1,k0,k1]: the stage-2 mountain geysers (horizontal) and the vents about to become them
    try { if (typeof geysers !== 'undefined') for (const g of geysers) if (g.hostile && g.horizontal && g.t < g.life) {
      const end = g.x - g.side * GEYSER_H, ln = geyserLane(g) * 0.75 + 4;
      Z.rects.push([Math.min(g.x, end), Math.max(g.x, end), g.y - ln, g.y + ln, 0, Math.ceil((g.life - g.t) * 60) + 3]);
    } } catch (e) {}
    try { if (typeof s2Vents !== 'undefined') for (const v of s2Vents) if (!v.done && v._ac10Side) {
      const end = v.x - v.side * GEYSER_H, ln = geyserLane({kind: 'fire'}) * 0.75 + 8, k0 = Math.max(0, Math.floor((S2VENT.warn - v.t) * 60) - 6);
      Z.rects.push([Math.min(v.x, end), Math.max(v.x, end), v.y - ln, v.y + ln, k0, k0 + 100]);
    } } catch (e) {}
    // the stage-2 firewall: a big square of fire falling down its lane, growing as it falls
    Z.walls = []; Z.lanes = [];
    try { if (typeof wfx !== 'undefined' && wfx && wfx.fseq) {
      const F = wfx.fseq;
      if (F.wave) Z.walls.push({x: F.wave.x, y: F.wave.y, t: F.wave.t, vy: (VH + 300) / FIRE_CROSS / 60});
      if (F.lanes) for (let j = (F.wave ? F.fired : F.fired); j < F.lanes.length; j++) Z.lanes.push(F.lanes[j]);
    } } catch (e) {}
    // the Chrome Hammer's thrown hammer: hits within 30 + the hitbox of its centre
    try { if (boss && boss._hammer && boss._hammer.throw && !boss._hammer.throw.reflected) { const T = boss._hammer.throw;
      const vx = T._fbx != null ? T.x - T._fbx : 0, vy = T._fby != null ? T.y - T._fby : 0; T._fbx = T.x; T._fby = T.y;
      Z.mcirc.push([T.x, T.y, Math.max(-14, Math.min(14, vx)), Math.max(-14, Math.min(14, vy)), 30 + 10 + 6]); } } catch (e) {}
    // the Chrome Hammer Archmage's columns: the eradication beam under him and the spell pillars
    try { if (boss && boss._hammer && bossActive) { const h = boss._hammer, yT = boss.y - 20, yB = PLAY.y + PLAY.h + 20;
      if (h.state === 'mega_charge' || h.state === 'mega_beam') {
        const half = hammerEradWidth() * 0.5 + 8, k0 = h.state === 'mega_charge' ? Math.max(1, Math.round((1.65 - h.t) * 60) - 4) : 1, k1 = h.state === 'mega_beam' ? Math.round((hammerEradDuration() - h.t) * 60) + 2 : 999;
        Z.rects.push([boss.x - half, boss.x + half, yT, yB, k0, k1]);
      }
      if (h.state === 'spell' && h.spellTargets) for (const q of h.spellTargets) { const k0 = Math.max(1, Math.round((2.35 - h.t) * 60) - 4); Z.rects.push([q.x - 30, q.x + 30, -999, 9999, k0, k0 + 70]); }
      if (h.state === 'spell_blast' && h.pillars) for (const q of h.pillars) Z.rects.push([q.x - 30, q.x + 30, -999, 9999, 1, Math.max(1, Math.round((1.05 - h.t) * 60) + 2)]);
    } } catch (e) {}
    // the Chrome Hammer's body attacks: whirlwind (r 102 round y+36), the spiked ball (bouncing), the giant dive + sweep box
    try { if (boss && boss._hammer && bossActive && !boss.dead) { const h = boss._hammer, Bv = Z.boss || [0, 0];
      if (h.state === 'whirlwind' && h.whirl) { const w = h.whirl, sp = (w.speed || 300) / 60 * (w.dir || 1); Z.mcirc.push([boss.x, boss.y + 36, sp, 0, 102 + 12, 1]); }
      if (h.state === 'ball') Z.mcirc.push([boss.x, boss.y, Bv[0], Bv[1], 54 + 12 + 6, 1]);
      if (h.state === 'giant_dive') { const k0 = Math.max(1, Math.round((0.52 - h.t) * 60) - 2); Z.rects.push([h.tx - 162, h.tx + 162, h.ty - 90, h.ty + 90, k0, k0 + 24]); }
      if (h.state === 'giant_sweep' && h.t <= 0.34) Z.rects.push([boss.x - 162, boss.x + 162, boss.y - 90, boss.y + 90, 1, Math.round((0.34 - h.t) * 60) + 2]);
    } } catch (e) {}
    // Warhive rounds (whvShotsTick): straight per-frame flight; a bolt hits inside |dx|<6,|dy|<16, a ball inside r+5
    try { for (const L of warhiveShots()) for (const sh of L) {
      if (Math.abs(sh.x - player.x) > 300 || Math.abs(sh.y - player.y) > 300) continue;
      Z.mcirc.push([sh.x, sh.y, sh.vx, sh.vy, sh.kind === 'bolt' ? 16 + 4 : (sh.r || 6) + 5 + 4, 0, 1]);
    } } catch (e) {}
    // the chromium rift: the core kills, and inside half its radius the pull is stronger than a clean escape
    try { const C = finalRift(); if (C) {
      const k0 = C.phase === 'raise' ? Math.max(1, Math.round((C.tell - C.t) * 60) - 6) : 1;
      Z.circ.push([C.x, C.y, C.core + 4 + 12, k0, 9999]);
      Z.circ.push([C.x, C.y, C.radius * 0.5, k0, 9999]);
    } } catch (e) {}
    // stage-5 rocks: vacuum drift, lethal inside rad*0.78+8 of their centre
    try { if (typeof l5Rocks !== 'undefined') for (const r of l5Rocks) if (r && !r.dead && Math.abs(r.x - player.x) < 400 && Math.abs(r.y - player.y) < 400)
      Z.mcirc.push([r.x, r.y, r.vx, r.vy, r.rad * 0.78 + 8 + 4, 0, 1]); } catch (e) {}
    // lobbed targeted balls (tb28): they land on (tx,ty) after warm+flight and splash
    try { if (typeof tb28List !== 'undefined') for (const q of tb28List) {
      if (q.dead || q.arrived || !(q.splash > 0 || (q.burst && q.shot))) continue;
      const left = q.phase === 'warn' ? (q.warm - q.t) + q.flight : q.flight - (q.ft || 0), kA = Math.round(left * 60);
      if (q.phase === 'warn' && q.t < q.warm * (q.track || 0) && kA > 14) continue;     // still following the ship
      // the splash, and the landing burst that fans out of the landing point (it was aimed at the ship)
      const r = Math.max((q.splash || 0) + 16, q.burst ? 46 : 0);
      Z.circ.push([q.tx, q.ty, r, Math.max(1, kA - 3), kA + (q.burst ? 12 : 3)]);
    } } catch (e) {}
    // the 1013 enemy pattern beams (ep13Beam): a live beam from the owner's muzzle
    try { if (typeof ep13Beam === 'function' && typeof EP13 !== 'undefined' && EP13.owner) { const b = ep13Beam(EP13.owner); if (b && b.width > 0) { const len = b.len, x2 = b.x + Math.cos(b.a) * len, y2 = b.y + Math.sin(b.a) * len; FB.beams.push({x: b.x + Math.cos(b.a) * 20, y: b.y + Math.sin(b.a) * 20, ex: x2, ey: y2, half: b.width * 0.5 + 12, k1: 30}); } } } catch (e) {}
    // the Razorback (stage 1 miniboss): its hull runs you over inside 105*S, its pressure waves are expanding arcs
    Z.rzb = [];
    try {
      const actors = [];
      if (typeof subBoss !== 'undefined' && subBoss && subBossActive && !subBoss.dead && subBoss._rzb) actors.push(subBoss);
      if (subBoss && subBoss._rzbPair && subBoss._rzbPair.actors) for (const a of subBoss._rzbPair.actors) if (a && a !== subBoss && a._rzb && !a.dead) actors.push(a);
      for (const b of actors) {
        const R = b._rzb, S = rzbScale(b);
        const vx = (b._fbrx != null) ? b.x - b._fbrx : 0, vy = (b._fbry != null) ? b.y - b._fbry : 0; b._fbrx = b.x; b._fbry = b.y;
        Z.rzb.push({x: b.x, y: b.y, vx: Math.max(-8, Math.min(8, vx)), vy: Math.max(-8, Math.min(8, vy)), r: 105 * S + 8,
          waves: (R.waves || []).map(w => ({w, x: w.x, y: w.y, r: w.r, sp: w.speed / 60, half: w.width + 7 * S + 7, maxR: (w.maxR || 300) * 0.916}))});
      }
    } catch (e) {}
    return Z;
  }
  function rzbHit(qx, qy, k, Z){
    for (const A of Z.rzb) {
      const hx = A.x + A.vx * k, hy = A.y + A.vy * k;
      if (k <= 20 && (qx - hx) * (qx - hx) + (qy - hy) * (qy - hy) < A.r * A.r) return true;
      for (const W of A.waves) {
        const r = W.r + W.sp * k; if (r > W.maxR) continue;
        const dd = Math.hypot(qx - W.x, qy - W.y);
        if (Math.abs(dd - r) < W.half) {
          try { if (rzbWaveAngleHit(W.w, rzbWrap(rzbAim(W.w, {x: qx, y: qy}) - W.w.a))) return true; } catch (e) { return true; }
        }
      }
    }
    return false;
  }
  // a moving circle at frame k; [5] = bounces off the view's edges (fold the straight path back into the box)
  function mcircAt(M, k){
    if (!M[5]) { const kk = M[6] ? k : Math.min(k, 14); return [M[0] + M[2] * kk, M[1] + M[3] * kk]; }
    const fold = (v, a, b) => { const w = b - a; if (w <= 0) return v; let t = (v - a) % (2 * w); if (t < 0) t += 2 * w; return a + (t <= w ? t : 2 * w - t); };
    return [fold(M[0] + M[2] * k, camLeftX() + 40, camRightX() - 40), fold(M[1] + M[3] * k, PLAY.y + 40, PLAY.y + PLAY.h - 40)];
  }
  function inBoss(qx, qy, k, Z){
    if (!Z.boss) return false;
    try { if (k <= 3 && bossHitTest(qx, qy - 6)) return true; } catch (e) {}      // where the hull is NOW (a form can appear on you)
    try { return !!bossHitTest(qx - Z.boss[0] * k, qy - 6 - Z.boss[1] * k); } catch (e) { return false; }
  }

  /* ---- plan scoring --------------------------------------------------------------------------- */
  function scorePlan(d1, d2, sw, sp, L, Z, tx, ty){
    const ww = worldWidth(), y0 = PLAY.y + 12, y1 = PLAY.y + PLAY.h - 6;
    let qx = player.x, qy = player.y, c = 0, first = 999, near = 0;
    const SS = [], iv = (player.invuln | 0) - 1; let why = '', coneC = 0;
    for (let n = 0; n < L.length; n++) { const T = L[n]; if (T.steer) SS.push([n, T.x, T.y, T.steer.ang, T.steer.spd, T.steer.t, T.steer.lock ? 0 : 1]); }
    const l1 = Math.hypot(d1[0], d1[1]) || 1, l2 = Math.hypot(d2[0], d2[1]) || 1;
    for (let k = 1; k <= H; k++) {
      const d = k <= sw ? d1 : d2, l = k <= sw ? l1 : l2;
      qx = Math.min(ww - 10, Math.max(10, qx + d[0] / l * sp));
      qy = Math.min(y1, Math.max(y0, qy + d[1] / l * sp));
      const w = 1 / (1 + k * 0.06);
      let hitNow = false;
      // advance the steering rounds one frame, aimed at where THIS plan puts the ship this frame
      for (const M of SS) {
        const S = L[M[0]].steer;
        let ang = M[3];
        M[5] += 1 / 60;
        if (S.commitR && !M[9] && Math.hypot(qx - M[1], qy - M[2]) <= S.commitR) M[9] = 1;
        if (S.homing && !M[9]) {
          let tr = S.tr; if (S.swerve != null) tr = M[5] < S.swerve ? S.trA : S.trB;
          const ta = Math.atan2(qy - M[2], qx - M[1]); const da = ((ta - ang + Math.PI * 3) % (Math.PI * 2)) - Math.PI; ang += Math.max(-tr, Math.min(tr, da));
        }
        if (S.lock && !M[6]) {
          const dxl = qx - M[1], dyl = qy - M[2];
          if (dxl * dxl + dyl * dyl < LOCK_COMMIT_PX * LOCK_COMMIT_PX) M[6] = 1;
          else if (!S.homing) { const ta = Math.atan2(dyl, dxl); const da = ((ta - ang + Math.PI * 3) % (Math.PI * 2)) - Math.PI; ang += Math.max(-S.lockTurn, Math.min(S.lockTurn, da)); }
        }
        if (S.acc) M[4] = Math.min(S.max, M[4] + S.acc);
        const v = M[4] * S.eb; M[7] = M[1]; M[8] = M[2]; M[1] += Math.cos(ang) * v; M[2] += Math.sin(ang) * v; M[3] = ang;
      }
      for (let n = 0, si = 0; n < L.length; n++) {
        const T = L[n];
        if (k < T.t0 || k > T.t1) continue;
        let px_, py_, px0, py0;
        if (T.steer) { const M = SS[si++]; px_ = M[1]; py_ = M[2]; px0 = M[7]; py0 = M[8]; }
        else if (T.sw) { const W = T.sw, f = (tt) => Math.sin(tt * SWIRL_HZ + W.ph); const d = (f(W.t + k / 60) - f(W.t)) * W.amp, d0 = (f(W.t + (k - 1) / 60) - f(W.t)) * W.amp;
          px_ = T.x + T.vx * k + W.px * d; py_ = T.y + T.vy * k + W.py * d; px0 = T.x + T.vx * (k - 1) + W.px * d0; py0 = T.y + T.vy * (k - 1) + W.py * d0; }
        else if (T.path) { px_ = T.path[2 * k]; py_ = T.path[2 * k + 1]; px0 = T.path[2 * k - 2]; py0 = T.path[2 * k - 1]; }
        else { const hk = 0.5 * k * k, h0 = 0.5 * (k - 1) * (k - 1); px_ = T.x + T.vx * k + T.ax * hk; py_ = T.y + T.vy * k + T.ay * hk; px0 = T.x + T.vx * (k - 1) + T.ax * h0; py0 = T.y + T.vy * (k - 1) + T.ay * h0; }
        const dx = Math.abs(px_ - qx), dy = Math.abs(py_ - qy);
        if (T.wave) {
          if (dx < T.wx && dy < T.wy) { let h = false; try { h = pt11FireWaveHit({x: px_, y: py_, ang: T.wave.ang, _pt11Scale: T.wave.sc}, {x: qx, y: qy}, 9, 10, px0, py0); } catch (e) {} if (h) { hitNow = 'wave'; break; } }
          continue;
        }
        if (T.ell && dx < T.wx && dy < T.wy) {
          const ux = qx - px_, uy = qy - py_, ex = ux * T.ell.c + uy * T.ell.s, ey = -ux * T.ell.s + uy * T.ell.c;
          const e = (ex / T.ell.rw) ** 2 + (ey / T.ell.rh) ** 2;
          if (e < 1) { hitNow = 'ell'; break; }
          if (e < 2.2) near += (2.2 - e) * 6 * w;
          continue;
        }
        if (dx < T.wx && dy < T.wy) { hitNow = T.kind + (T.steer ? 'S' : ''); break; }
        // the engine sweeps a round's whole step against the box (ec7SegmentBox), so a fast round cannot skip it
        if (T.kind === 'b' && px0 != null && sweep(px0, py0, px_, py_, qx, qy, T.wx, T.wy)) { hitNow = 'bS'; break; }
        const mx = dx - T.wx, my = dy - T.wy, m = Math.max(mx, my);   // clearance
        if (m < 14) near += (14 - m) * (T.kind === 'e' ? 0.5 : 1) * w;
      }
      if (!hitNow) {
        for (const B of Z.beams) {
          const px = qx - B[0], py = qy - B[1], al = px * B[2] + py * B[3], ac = Math.abs(px * B[3] - py * B[2]);
          if (al >= -10 && al <= B[5] && ac < B[4]) { hitNow = 'beam'; break; }
        }
      }
      if (!hitNow) for (const C of Z.cols) if (Math.abs(qx - C[0]) < C[1] && qy > C[2] && qy < C[3]) { hitNow = 'col'; break; }
      if (!hitNow) for (const C of Z.circ) if ((C[3] == null || (k >= C[3] && k <= C[4])) && (qx - C[0]) * (qx - C[0]) + (qy - C[1]) * (qy - C[1]) < C[2] * C[2]) { hitNow = 'circ'; break; }
      if (!hitNow && k <= 16 && inBoss(qx, qy, k, Z)) hitNow = 'boss';
      if (!hitNow && Z.rzb.length && rzbHit(qx, qy, k, Z)) hitNow = 'rzb';
      if (!hitNow && Z.mcirc) for (const M of Z.mcirc) { const P = mcircAt(M, k); if (Math.hypot(qx - P[0], qy - P[1]) < M[4]) { hitNow = 'mcirc'; break; } }
      if (!hitNow) for (const L of FB.beams) if ((L.k1 == null ? k <= 8 : k <= L.k1) && segDist(qx, qy, L) < L.half) { hitNow = 'av3'; break; }
      // a warned lane is not a hit yet: it is a strong push out of the lane, weighted toward its release
      for (const C of FB.cones) if (inCone(qx, qy, C, 10)) { coneC += (C.k > 0.3 || C.seen < FB.i ? 700 : 160) * (0.4 + 0.6 * Math.min(1, k / 12)); break; }
      if (!hitNow) for (const R of Z.rects) if (k >= R[4] && k <= R[5] && qx > R[0] && qx < R[1] && qy > R[2] && qy < R[3]) { hitNow = 'rect'; break; }
      if (!hitNow) for (const W of Z.walls) {
        const yk = W.y + W.vy * k, half = 51 * (0.9 + Math.min(1, Math.max(0, (W.t + k / 60) / FIRE_CROSS)) * 1.25) + 3;
        if (Math.abs(qx - W.x) < half && Math.abs(qy - yk) < half) { hitNow = 'wall'; break; }
      }
      if (!hitNow && Z.sub && k <= 20) {
        const S = Z.sub;
        if (Math.abs(S[0] + S[2] * k - qx) < S[4] && Math.abs(S[1] + S[3] * k - qy) < S[5]) hitNow = 'sub';
      }
      if (hitNow) {
        if (k < iv) c += 260 * w;                         // i-frames still cover this frame: no damage, but get out
        else { if (k < first) { first = k; why = hitNow; } c += 900 * w; }
      }
    }
    // end position: the attack spot, edges, the boss's hull just above
    c += Math.hypot(qx - tx, qy - ty) * 0.06;
    { const sd = Math.min(qx, ww - qx); if (sd < 70) c += (70 - sd) * 0.45; const bd = y1 - qy; if (bd < 30) c += (30 - bd) * 0.4; }
    if (Z.boss && inBoss(qx, qy - 30, 0, Z)) c += 40;
    c += Math.min(near * 1.4, 900);
    c += coneC;
    { const top = PLAY.y + PLAY.h * 0.38; if (qy < top) c += (top - qy) * 3; }
    for (const lx of Z.lanes) { const d = Math.abs(qx - lx); if (d < 120) c += (120 - d) * 0.5; }
    for (const A of Z.rzb) { const d = Math.hypot(qx - A.x, qy - A.y), R0 = A.r + 140; if (d < R0) c += (R0 - d) * 0.9; }
    if (Z.sub && !Z.rzb.length) {
      const S = Z.sub, ex = Math.max(0, Math.abs(qx - S[0]) - S[4]), ey = Math.max(0, Math.abs(qy - S[1]) - S[5]), gap = Math.hypot(ex, ey);
      if (gap < 90) c += (90 - gap) * 2.5;
    }
    if (first <= H) c += 60000 + (H + 1 - first) * 8000;
    return [c, first, qx, qy, why];
  }

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
    GR.V = []; GR.D = []; for (let k = 0; k <= H; k++) { GR.V.push(new Float32Array(GR.N)); GR.D.push(new Uint8Array(GR.N)); }
  }
  function gridPlan(L, Z, tx, ty, sp){
    const g = Math.max(2.2, sp / Math.SQRT2), R = Math.min(48, Math.ceil(H * sp / g) + 2);
    gridAlloc(R);
    const W = GR.W, N = GR.N, ox = player.x - R * g, oy = player.y - R * g;
    const ww = worldWidth(), y0 = PLAY.y + 12, y1 = PLAY.y + PLAY.h - 6, y1c = y1, iv = (player.roll || player.somer || player._chgDash) ? (player.invuln | 0) - 1 : (player.invuln | 0) - 45;   // respawn i-frames: plan as if they end early, so the ship leaves the danger while it still can
    for (let k = 1; k <= H; k++) { GR.occ[k].fill(0); GR.near[k].fill(0); }
    // the static soft field: edges, the top of the field, warned lanes, firewall lanes, keep-away rings
    const soft = GR.soft; soft.fill(0);
    // a berth around the boss body; the Stage-4 Sovereign's shield bubble (w*0.67) can switch on in one frame
    let BB = null;
    if (typeof boss !== 'undefined' && boss && bossActive && !boss.dead) {
      const by = boss._drawY != null ? boss._drawY : boss.y, rB = Math.max(boss.w || 60, boss.h || 60) * 0.5 + 50;
      let sh = 0; try { if (boss._ship === 'stormsovereign' && boss._s4war && boss._s4war.shield) sh = boss.w * 0.67 + 16; } catch (e) {}
      BB = [boss.x, by, rB, sh];
    }
    FB.hulls = [];
    for (const T of L) if (T.kind === 'e' && Math.abs(T.x - player.x) < 260 && Math.abs(T.y - player.y) < 260) FB.hulls.push([T.x, T.y, T.wx, T.wy]);
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
        for (const C of FB.cones) { if (inLane(x, y, C)) { s += (C.k > 0.5 || C.seen < FB.i) ? 400 : 40; break; } if (inCone(x, y, C, 6)) { s += (C.k > 0.5 || C.seen < FB.i) ? 25 : 8; break; } }
        for (const lx of Z.lanes) { const d = Math.abs(x - lx); if (d < 120) s += (120 - d) * 0.05; }
        for (const A of Z.rzb) { const d = Math.hypot(x - A.x, y - A.y), R0 = A.r + 140; if (d < R0) s += (R0 - d) * 0.09; }
        if (Z.sub && !Z.rzb.length) {
          const S = Z.sub, ex = Math.max(0, Math.abs(x - S[0]) - S[4]), ey = Math.max(0, Math.abs(y - S[1]) - S[5]), gap = Math.hypot(ex, ey);
          if (gap < 90) s += (90 - gap) * 0.25;
        }
        if (BB) { const d = Math.hypot(x - BB[0], y - BB[1]); if (d < BB[2]) s += (BB[2] - d) * 0.7; if (BB[3] && d < BB[3]) s += 120; }
        for (const E of FB.hulls) { const ex = Math.max(0, Math.abs(x - E[0]) - E[2]), ey = Math.max(0, Math.abs(y - E[1]) - E[3]), gap = Math.hypot(ex, ey); if (gap < 70) s += (70 - gap) * 0.12; }
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
        const y = oy + r * g, inY = Math.abs(y - cy) < hy + 1.5;
        for (let q = Math.max(0, qa); q <= Math.min(W - 1, qb); q++) {
          const c = r * W + q;
          if (inY && Math.abs(ox + q * g - cx) < hx + 1.5) O[c] = 1; else if (NE[c] < 250) NE[c] += 1;
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
          if (S.commitR && !committed && Math.hypot(player.x - x, player.y - y) <= S.commitR) committed = true;
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
        } else if (T.path) {
          px_ = T.path[2 * k]; py_ = T.path[2 * k + 1]; px0 = T.path[2 * k - 2]; py0 = T.path[2 * k - 1];
        } else {
          const hk = 0.5 * k * k, h0 = 0.5 * (k - 1) * (k - 1);
          px_ = T.x + T.vx * k + T.ax * hk; py_ = T.y + T.vy * k + T.ay * hk; px0 = T.x + T.vx * (k - 1) + T.ax * h0; py0 = T.y + T.vy * (k - 1) + T.ay * h0;
        }
        if (T.wave) {
          const qa = Math.max(0, Math.ceil((px_ - T.wx - ox) / g)), qb = Math.min(W - 1, Math.floor((px_ + T.wx - ox) / g));
          const ra = Math.max(0, Math.ceil((py_ - T.wy - oy) / g)), rb = Math.min(W - 1, Math.floor((py_ + T.wy - oy) / g));
          const sh = {x: px_, y: py_, ang: T.wave.ang, _pt11Scale: T.wave.sc};
          for (let r = ra; r <= rb; r++) for (let q = qa; q <= qb; q++) { let h = false; try { h = pt11FireWaveHit(sh, {x: ox + q * g, y: oy + r * g}, 11, 12, px0, py0); } catch (e) {} if (h) GR.occ[k][r * W + q] = 1; }
          continue;
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
        // an accelerating round may hit its speed cap at any time: its linear path is lethal too
        if ((T.ax || T.ay || T.path) && k > 2) box(k, T.x + T.vx * k, T.y + T.vy * k, T.wx, T.wy, 0);
        if (T.kind === 'b') {                       // the engine's swept step: a fast round fills its whole step
          const st = Math.max(Math.abs(px_ - px0) / T.wx, Math.abs(py_ - py0) / T.wy);
          if (st > 0.9) { const n = Math.ceil(st); for (let j = 1; j < n; j++) box(k, px0 + (px_ - px0) * j / n, py0 + (py_ - py0) * j / n, T.wx, T.wy, 0); }
        }
      }
    }
    // field hazards
    for (const Bm of Z.beams) cellTest(1, H, function(x, y){ const px = x - Bm[0], py = y - Bm[1], al = px * Bm[2] + py * Bm[3], ac = Math.abs(px * Bm[3] - py * Bm[2]); return al >= -10 && al <= Bm[5] && ac < Bm[4]; });
    for (const C of Z.cols) cellTest(1, H, function(x, y){ return Math.abs(x - C[0]) < C[1] && y > C[2] && y < C[3]; });
    for (const C of Z.circ) cellTest(C[3] == null ? 1 : Math.min(H, C[3]), C[4] == null ? H : Math.min(H, C[4]), function(x, y){ return (x - C[0]) * (x - C[0]) + (y - C[1]) * (y - C[1]) < C[2] * C[2]; });
    for (const Rr of Z.rects) { const k0 = Math.max(1, Rr[4]), k1 = Math.min(H, Rr[5]); if (k0 <= k1) cellTest(k0, k1, function(x, y){ return x > Rr[0] && x < Rr[1] && y > Rr[2] && y < Rr[3]; }); }
    for (const C of FB.cones) {
      const big = C.o && ((typeof boss !== 'undefined' && C.o === boss) || (typeof subBoss !== 'undefined' && C.o === subBoss));
      if (!FB.bigLanes || !big || !(C.k > 0.75 || C.seen < FB.i)) continue;
      const half = Math.max(C.lane * 0.5, (C.o.w || 60) * 0.42) + 10;
      cellTest(1, H, function(x, y){ const rx = x - C.x, ry = y - C.y, al = rx * C.dx + ry * C.dy; return al > -30 && al < C.L + 40 && Math.abs(rx * C.dy - ry * C.dx) < half; });
    }
    for (const Lb of FB.beams) { const k1 = Math.min(H, Lb.k1 == null ? 8 : Lb.k1); cellTest(1, k1, function(x, y){ return segDist(x, y, Lb) < Lb.half; }); }
    for (const Wl of Z.walls) for (let k = 1; k <= H; k++) { const yk = Wl.y + Wl.vy * k, half = 51 * (0.9 + Math.min(1, Math.max(0, (Wl.t + k / 60) / FIRE_CROSS)) * 1.25) + 3; box(k, Wl.x, yk, half, half, 6); }
    for (const M of Z.mcirc) for (let k = 1; k <= H; k++) { const P = mcircAt(M, k); cellTest(k, k, function(x, y){ return Math.hypot(x - P[0], y - P[1]) < M[4]; }); }
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
        if (h) { any = true; for (let a = -3; a <= 3; a++) for (let b = -3; b <= 3; b++) { const rr = r + a, qq = q + b; if (rr >= 0 && rr < W && qq >= 0 && qq < W) { const v = (Math.abs(a) <= 1 && Math.abs(b) <= 1) ? 2 : 1; if (mask[rr * W + qq] < v) mask[rr * W + qq] = v; } } } } }
      if (any) for (let k = 1; k <= H; k++) {
        const kk = Math.min(k, 18), sx = Math.round(Z.boss[0] * kk / g), sy = Math.round(Z.boss[1] * kk / g), O = GR.occ[k];
        const NE = GR.near[k];
        for (let r = 0; r < W; r++) { const r2 = r - sy; if (r2 < 0 || r2 >= W) continue; for (let q = 0; q < W; q++) { const q2 = q - sx; if (q2 < 0 || q2 >= W) continue; const m = mask[r2 * W + q2]; if (m === 2 || (m === 1 && k >= 3)) O[r * W + q] = 1; else if (m === 1 && NE[r * W + q] < 250) NE[r * W + q] += 2; } }
      }
    }
    // the DP, run BACKWARD: V[k][c] is the cheapest cost of flying on from cell c at frame k to the horizon, D[k][c]
    // the deepest frame that is survivable from there. Lethal cells are excluded once i-frames have run out.
    const V = GR.V, D = GR.D;
    for (let c = 0; c < N; c++) {
      const x = ox + (c % W) * g, y = oy + Math.floor(c / W) * g;
      if (soft[c] < 0 || (H > iv && GR.occ[H][c])) { V[H][c] = Infinity; D[H][c] = H - 1; continue; }
      V[H][c] = soft[c] + GR.near[H][c] * 26 + Math.hypot(x - tx, y - ty) * 0.9; D[H][c] = H;
    }
    for (let k = H - 1; k >= 1; k--) {
      const O = GR.occ[k], NE = GR.near[k], Vk = V[k], Vn = V[k + 1], Dk = D[k], Dn = D[k + 1], wk = 1 / (1 + k * 0.05), lethal = k > iv;
      for (let r = 0; r < W; r++) {
        const ra = r > 0 ? r - 1 : 0, rb = r < W - 1 ? r + 1 : W - 1;
        for (let q = 0; q < W; q++) {
          const c = r * W + q;
          if (soft[c] < 0 || (lethal && O[c])) { Vk[c] = Infinity; Dk[c] = k - 1; continue; }
          const qa = q > 0 ? q - 1 : 0, qb = q < W - 1 ? q + 1 : W - 1;
          let bv = Infinity, bd = k;
          for (let rr = ra; rr <= rb; rr++) for (let qq = qa; qq <= qb; qq++) { const n = rr * W + qq; if (Vn[n] < bv) bv = Vn[n]; if (Dn[n] > bd) bd = Dn[n]; }
          Dk[c] = bd;
          Vk[c] = bv === Infinity ? Infinity : bv + (soft[c] + NE[c] * 26 + (O[c] ? 60 : 0)) * wk;
        }
      }
    }
    // the first move is checked EXACTLY: the real ship moves sp per frame (sp/sqrt2 per axis on a diagonal), which the
    // grid only approximates, so each of the nine real moves is flown through the exact hit tests (scorePlan) and then
    // scored by the worse of the grid cells either side of where it really lands.
    let best = null, bestDepth = -1, bestV = Infinity;
    const cellsAt = (x, y) => {
      const fq = (x - ox) / g, fr = (y - oy) / g, out = [];
      for (const q of [Math.floor(fq), Math.ceil(fq)]) for (const r of [Math.floor(fr), Math.ceil(fr)]) if (q >= 0 && q < W && r >= 0 && r < W) out.push(r * W + q);
      return out;
    };
    for (const d of DIRS) {
      const l = Math.hypot(d[0], d[1]) || 1;
      const x1 = Math.min(ww - 10, Math.max(10, player.x + d[0] / l * sp)), y1 = Math.min(y1c, Math.max(y0, player.y + d[1] / l * sp));
      const ex = scorePlan(d, [0, 0], 1, sp, L, Z, tx, ty);       // exact: hit frame of "this move, then hold"
      if (ex[1] === 1 && 1 > iv) continue;                         // dies on the very next frame
      const cs = cellsAt(x1, y1); if (!cs.length) continue;
      let dep = H, v = 0;
      for (const c of cs) { dep = Math.min(dep, D[1][c]); v = Math.max(v, V[1][c]); }
      if (ex[1] <= H && ex[1] > iv) dep = Math.max(dep, 0);
      v += (d[0] !== FB.dir[0] || d[1] !== FB.dir[1]) ? 3 : 0;
      if (dep > bestDepth || (dep === bestDepth && v < bestV)) { bestDepth = dep; bestV = v; best = d; }
    }
    if (!best || bestV === Infinity) {
      // no path survives to the horizon: get out of the biggest body we are in or next to
      let hx = null, hy = null;
      if (Z.sub) { hx = Z.sub[0]; hy = Z.sub[1]; } else if (Z.bossC) { hx = Z.bossC[0]; hy = Z.bossC[1]; } else if (Z.rzb.length) { hx = Z.rzb[0].x; hy = Z.rzb[0].y; }
      else { // the nearest live round
        let bd2 = 1e9; for (const T of L) { const d = Math.hypot(T.x - player.x, T.y - player.y); if (d < bd2) { bd2 = d; hx = T.x; hy = T.y; } }
      }
      if (hx != null) {
        let bd = -1;
        for (const d of DIRS) {
          if (d[0] === 0 && d[1] === 0) continue;
          const l = Math.hypot(d[0], d[1]), x1 = player.x + d[0] / l * sp * 8, yy = player.y + d[1] / l * sp * 8;
          if (x1 < 14 || x1 > ww - 14 || yy < y0 || yy > y1c) continue;
          const sc = Math.hypot(x1 - hx, yy - hy);
          if (sc > bd) { bd = sc; best = d; }
        }
      }
    }
    if (!best) return {dir: [0, 0], live: 0, cost: Infinity, end: null};
    return {dir: best, live: bestDepth, cost: bestV, end: null};
  }

  const PV = {weapon: 130, crate: 130, life: 320, lifeup: 320, oneup: 320, continueup: 260, shield: 100, capsule: 100, speed: 70,
    special: 90, specialicon: 90, sonicbox: 80, lzmgbox: 80, dkshotbox: 80, missilepack: 45, missilepack2: 45, missileup_super: 80,
    missileup_ultra: 80, missileup_uber: 80, missileupbox_super: 70, missileupbox_ultra: 70, missileupbox_uber: 70, furybomb: 70,
    timebomb: 25, scorechip: 8, mcrate: 60, scrate: 60, retinascan: 40};
  function pickupValue(k){ if (PV[k] != null) return PV[k]; if (/life|1up/i.test(k || '')) return 300; if (/infus|elem|forge/i.test(k || '')) return 90; return 35; }
  /* ---- the attack position -------------------------------------------------------------------- */
  function attackSpot(Z){
    const ww = worldWidth(), t = FB.i / 60;
    const lowY = PLAY.y + PLAY.h * 0.80;
    let tx = null, ty = lowY;
    let T = null;
    if (typeof boss !== 'undefined' && boss && bossActive && !boss.dead) T = boss;
    else if (typeof subBoss !== 'undefined' && subBoss && subBossActive && !subBoss.dead) T = subBoss;
    if (T) {
      // the column with the most hittable boss under it (bossHitTest is the boss's own shape)
      let bx = T.x;
      if (T === boss && typeof bossHitTest === 'function') {
        let best = -1, bestX = T.x;
        for (let ox = -120; ox <= 120; ox += 20) {
          let n = 0; const x = T.x + ox;
          for (let y = Math.max(PLAY.y + 10, (T.y || 100) - 140); y < Math.min(lowY - 40, (T.y || 100) + 160); y += 16) { try { if (bossHitTest(x, y)) n++; } catch (e) {} }
          const s = n - Math.abs(ox) * 0.01;
          if (n > 0 && s > best) { best = s; bestX = x; }
        }
        bx = bestX;
        // stand off below the hull's lowest point: the body's own attacks (dives, sweeps) start from it
        let low = null; for (let y = PLAY.y + PLAY.h - 12; y > PLAY.y && low == null; y -= 12) { for (let ox = -100; ox <= 100; ox += 25) { let hh = false; try { hh = !!bossHitTest(T.x + ox, y); } catch (e) {} if (hh) { low = y; break; } } }
        FB.bossLow = low;
      }
      tx = bx + Math.sin(t * 1.3) * 22;
      // the Storm Sovereign: while its shield is up only the shield's nodes take hits; once the core opens, its turrets
      try { const S = T === boss && T._s4war; if (S) {
        let pick = null;
        if (S.shield && S.shield.active && S.shield.nodes) { for (const n of S.shield.nodes) if (!n.dead && (!pick || Math.abs(n.x - player.x) < Math.abs(pick.x - player.x))) pick = n; }
        else if (S.coreUnlocked && S.coreTurrets) { for (const q of S.coreTurrets) if (!q.dead && q.materialize >= 0.92 && (!pick || Math.abs(q.x - player.x) < Math.abs(pick.x - player.x))) pick = q; }
        if (pick) tx = pick.x;
      } } catch (e) {}
      // the Chrome Hammer heals by raising his hammer: rounds in the hammer's own column (and missiles) break it
      try { if (T === boss && T._hammer && T._hammer.recovery && T._hammer.recovery.status === 'charging' && hammerWeaponTargetable(T)) { tx = hammerHeadPoint(T).x; FB.healBreak = true; } else FB.healBreak = false; } catch (e) { FB.healBreak = false; }
      ty = lowY + Math.sin(t * 0.9) * 10;
      if (T === boss && FB.bossLow != null) ty = Math.max(ty, Math.min(PLAY.y + PLAY.h - 24, FB.bossLow + 130));
    } else {
      // the nearest live air target ahead
      let bd = 1e9, bt = null;
      for (const e of enemies) {
        if (!e || e.dead || e._dyingT != null || e.prop || e.y > player.y - 30 || e.y < PLAY.y - 20) continue;
        const d = Math.abs(e.x - player.x) + (player.y - e.y) * 0.25;
        if (d < bd) { bd = d; bt = e; }
      }
      tx = bt ? bt.x : ww / 2 + Math.sin(t * 0.6) * Math.min(140, ww * 0.25);
    }
    // pickups pull the position over: value over distance, anywhere on the screen
    let pk = null, ps = 0;
    for (const p of powerups) {
      if (!p || p.dead || p._wingSupply) continue;
      if (typeof spaceShootableContainer === 'function' && spaceShootableContainer(p)) continue;
      if (p.y < PLAY.y + 20 || p.y > PLAY.y + PLAY.h + 10) continue;
      const v = pickupValue(p.kind);
      const d = Math.hypot(p.x - player.x, p.y - player.y);
      const sc = v / (d + 80);
      if (sc > ps) { ps = sc; pk = p; }
    }
    if (pk && ps > 0.12) { tx = pk.x; ty = Math.max(PLAY.y + 60, Math.min(PLAY.y + PLAY.h - 20, pk.y + (pk.vy || 0) * 12)); FB.pk = pk.kind; } else FB.pk = null;
    return [Math.max(20, Math.min(ww - 20, tx)), ty];
  }

  /* ---- the frame ---------------------------------------------------------------------------- */
  function release(){ for (const k of MOVE) K[k] = false; }
  function tapKey(k){ if (K[k] === undefined) K[k] = false; Input.injectTap(k); }
  FB.play = function(){
    const i = FB.i;
    K.j = true;                                   // the trigger is held, as a player would
    // the Fusion: damage grows only 0.6x per full charge while time grows 1:1, so the quickest legal release
    // (SPACE_SHADOW_MIN_CHARGE) is the most damage per second - and it never comes near the overload
    if (run._spaceShadowHeld && (run._spaceShadowCharge || 0) >= (typeof SPACE_SHADOW_MIN_CHARGE !== 'undefined' ? SPACE_SHADOW_MIN_CHARGE : 0.42) + 0.03) K.j = false;
    if (player.dead || player.out) { release(); return; }
    if (typeof s6OpeningControlsLocked === 'function' && s6OpeningControlsLocked()) { release(); return; }
    // a planned second tap (the double-tap of a roll or a flip)
    if (FB.plan) { if (i >= FB.plan[1]) { tapKey(FB.plan[0]); FB.plan = null; } }
    const sp = ((typeof playerBaseSpeed === 'function') ? playerBaseSpeed() : 2.6) * 1.35;
    ingestCones(); ingestBeams();
    // self-check: how well did last frame's one-step prediction match where things actually are?
    if (FB.audit) {
      const A = FB.aud || (FB.aud = {});
      if (FB.pp) { const e = Math.hypot(player.x - FB.pp[0], player.y - FB.pp[1]); const r = A.__ship || (A.__ship = [0, 0, 0]); r[0]++; r[1] += e; r[2] = Math.max(r[2], e); }
      for (const b of eBullets) {
        if (b && b.__fbp && b.__fbp[2] === FB.i - 1) {
          const e = Math.hypot(b.x - b.__fbp[0], b.y - b.__fbp[1]); const r = A[b.kind] || (A[b.kind] = [0, 0, 0]); r[0]++; r[1] += e; r[2] = Math.max(r[2], e);
        }
        if (b) b.__fbp = [b.x + (b.vx || 0), b.y + (b.vy || 0), FB.i];
      }
    }
    const L = threats(), Z = hazards(); FB.lastBossC = Z.bossC ? Z.bossC.map(Math.round) : null; FB.lastBossV = Z.boss ? Z.boss.map(v => +v.toFixed(1)) : null; FB.lastL = L; FB.lastPlayI = FB.i; FB.zsub = Z.sub ? Z.sub.map(v => Math.round(v)) : null;
    let [tx, ty] = attackSpot(Z);
    if (FB.targetOverride) { try { const o = FB.targetOverride(); if (o) { tx = o[0]; ty = o[1]; } } catch (e) {} }
    let best, bestFirst, anySafe, bestWhy = '', bc;
    if (FB.mode !== 'plans') {
      const G = gridPlan(L, Z, tx, ty, sp);
      best = G.dir; bestFirst = G.live >= H ? 999 : G.live; anySafe = G.live > 10; bc = G.cost; FB.gend = G.end;
    } else {
      best = null; bc = Infinity; bestFirst = 0; anySafe = false;
      for (let a = 0; a < 9; a++) for (let s = 0; s < SW.length; s++) for (let b2 = 0; b2 < 9; b2++) {
        if (s === 1 && b2 !== a && b2 !== 0) continue;
        const r = scorePlan(DIRS[a], DIRS[b2], SW[s], sp, L, Z, tx, ty);
        let c = r[0];
        if (DIRS[a][0] !== FB.dir[0] || DIRS[a][1] !== FB.dir[1]) c += 3;
        if (r[1] > 10) anySafe = true;
        if (c < bc) { bc = c; best = DIRS[a]; bestFirst = r[1]; bestWhy = r[4]; }
      }
    }
    FB.dir = best; FB.lastFirst = bestFirst;
    FB.ring.push([i, Math.round(player.x), Math.round(player.y), best[0], best[1], bestFirst, anySafe ? 1 : 0, Math.round(bc), Z.sub ? 1 : 0, (subBoss && subBossActive) ? [Math.round(subBoss.x), Math.round(subBoss._drawY || subBoss.y), subBoss.enter ? 1 : 0] : 0, player.invuln | 0, bestWhy, FB.cones.length, (bossActive && boss) ? (() => { try { return bossHitTest(player.x, player.y - 6) ? 1 : 0; } catch (e) { return 'x'; } })() : '-', GR.W ? GR.occ[1][GR.R * GR.W + GR.R] : '-', GR.W ? GR.mask[GR.R * GR.W + GR.R] : '-']);
    if (FB.ring.length > 60) FB.ring.shift();
    K.a = best[0] < 0; K.d = best[0] > 0; K.w = best[1] < 0; K.s = best[1] > 0;
    if (FB.audit) { const l = Math.hypot(best[0], best[1]) || 1; FB.pp = [Math.min(worldWidth() - 10, Math.max(10, player.x + best[0] / l * sp)), Math.min(PLAY.y + PLAY.h - 6, Math.max(PLAY.y + 12, player.y + best[1] / l * sp))]; }
    const rolling = !!player.roll || !!player.somer;
    // nothing escapes: a barrel roll, else a somersault (both are real double taps; the game's cooldowns apply)
    if (!anySafe && bestFirst <= 9 && !rolling && !FB.plan && i - FB.rollAt > 12 && (player.invuln | 0) <= 2) {
      if ((player._rollCool || 0) <= 0 && !(typeof lzMountActive === 'function' && lzMountActive())) {
        const key = best[0] < 0 ? 'a' : best[0] > 0 ? 'd' : (player.x > worldWidth() / 2 ? 'a' : 'd');
        tapKey(key); FB.plan = [key, i + 2]; FB.rollAt = i; FB.rolls++;
      } else if ((player._somerCool || 0) <= 0) {
        tapKey('w'); FB.plan = ['w', i + 2]; FB.rollAt = i; FB.somers++;
      }
    }
    if (typeof s6Wing !== 'undefined' && s6Wing && s6Wing.choice && !s6Wing.route) {
      if (i % 40 === 0) tapKey(FB.route === 'right' ? 'd' : 'a');
      else if (i % 40 === 20) tapKey('j');                       // CHOOSE YOUR PURSUIT: A / fire confirms
    }
    // missiles at a boss / miniboss: lock it with the Retina, then fire from the stock
    const big = (typeof boss !== 'undefined' && boss && bossActive && !boss.dead) || (typeof subBoss !== 'undefined' && subBoss && subBossActive && !subBoss.dead);
    if (big && !FB.plan && (run.bombs | 0) > 0) {
      const locked = (typeof retina !== 'undefined' && retina && retina.target && retinaTargetValid(retina.target));
      if (!locked && i - FB.lockAt > 45) { tapKey('c'); FB.lockAt = i; }
      else if (locked && i - FB.mslAt > (FB.healBreak ? 16 : 50)) { tapKey('k'); FB.mslAt = i; FB.missiles++; }
    }
  };
  /* non-PLAY screens: Enter / J taps on a cadence, so cinematics, debriefs, the Forge and the loadout move on */
  FB.menu = function(s){
    const i = FB.i;
    release(); K.j = false;
    if (s === 'continue' || s === 'gameover') return;
    if (s === 'paused') { if (i - FB.tapAt > 30) { tapKey('enter'); FB.tapAt = i; FB.pauses++; } return; }
    if (i - FB.tapAt <= 28) return;
    FB.tapAt = i;
    if (s === 'forge') { const F = (typeof forge !== 'undefined') ? forge : null; tapKey(F && F.row !== 0 ? 'escape' : 'enter'); return; }
    if (s === 'armory') { tapKey('escape'); return; }
    if (s === 'stagesel') { tapKey((typeof campPause !== 'undefined' && campPause) ? 'escape' : 'j'); return; }
    tapKey((Math.floor(i / 28) % 2) ? 'enter' : 'j');
  };
  /* bossHitTest leaves transient hit-routing notes on the boss (which part, core, shield node, bay was last hit).
     The bot queries it many times a frame, so those notes are restored afterwards: looking must not change anything. */
  const BOSS_NOTES = ['_s4CoreHit', '_s4ShieldHit', '_hammerModuleHit', '_carrierBayHit', '_lastPart'];
  FB.playSafe = function(){
    const B = (typeof boss !== 'undefined' && boss) ? boss : null, saved = B ? BOSS_NOTES.map(k => [k, Object.prototype.hasOwnProperty.call(B, k), B[k]]) : null;
    try { FB.play(); } finally { if (B) for (const [k, had, v] of saved) { if (had) B[k] = v; else delete B[k]; } }
  };
  FB.snaps = []; FB._d0 = 0;
  FB.tick = function(){
    FB.i++;
    // a picture of every death, taken on the frame after it (the wreck is still where the ship was)
    if (FB.deaths !== FB._d0) { FB._d0 = FB.deaths; if (FB.snapDeaths && FB.snaps.length < 8) { try { FB.snaps.push([FB.deaths, document.getElementById('screen').toDataURL('image/jpeg', 0.75)]); } catch (e) {} } }
    if (FB.hook) { try { FB.hook(); } catch (e) {} }          // diagnostics only (never set in a real run)
    const s = state;
    if (s !== FB.lastState) { FB.log.push([FB.i, s, run.stage]); FB.lastState = s; FB.stateT = 0; }
    FB.stateT++;
    try {
      if (s === GS.PLAY) FB.playSafe(); else FB.menu(s);
    } catch (e) { FB.err = String(e && e.stack || e).slice(0, 300); release(); }
  };
  FB.metrics = function(){
    return {i: FB.i, state, stage: run.stage, lives: run.lives, cont: run.contUsed | 0, score: run.score | 0, hits: FB.hits,
      deaths: FB.deaths, rolls: FB.rolls, somers: FB.somers, msl: FB.missiles, bombs: run.bombs | 0, wl: run.wlevel, w: run.weapon,
      boss: (typeof boss !== 'undefined' && boss && bossActive) ? [boss.kind || boss.name, Math.round(boss.hp), Math.round(boss.maxhp || 0)] : null,
      sub: (typeof subBoss !== 'undefined' && subBoss && subBossActive) ? [subBoss.kind, Math.round(subBoss.hp), Math.round(subBoss.maxhp || 0)] : null,
      st: +(typeof stageTimer !== 'undefined' ? stageTimer : 0).toFixed(1), err: FB.err || null};
  };
})();
