/*
 * Stealth: vision cones, the detection meter, the alert phases and the radar.
 *
 *   SNEAK    nobody knows you are here. Cones are green at the game's 25% (the plate is authored at
 *            alpha 128, so opacity 0.5 = 25%).
 *   ALERT    someone saw you. Every unit within radio range hunts you; the radar jams; the phase
 *            timer refills every frame anyone can still see you and counts down when nobody can.
 *   EVASION  they lost you. They search the last known position with yellow cones; the radar stays jammed.
 *   CAUTION  they gave up but stay sharp: detection fills 1.5x faster until the timer runs out.
 *
 * A cone that is DRAWN is the cone that is TESTED: both come from u.vis {range, half}, and the plate
 * (bmfx_fov_*) is scaled per axis so its edges land on that half-angle. Hedges and smoke block sight
 * (a unit inside a hedge is hidden past 70 px); buildings block it; pits do not.
 * Noise is heard through walls: the cannon carries 420 px, the machine gun 140.
 */
(function (root) {
  'use strict';
  const TD = root.TD, M = TD.M, W = TD.World;
  // plate geometry, measured off the cells (apex, depth to the arc, half-width at the widest row and its depth)
  const PLATE = {
    wide: { ax: 159, ay: 11, len: 213, hw: 125, hd: 167 },
    tall: { ax: 159.5, ay: 11, len: 267, hw: 62.5, hd: 240 },
  };
  const COL = { patrol: 'green', suspect: 'yellow', search: 'yellow', alert: 'red' };
  const S = TD.Stealth = {
    phase: 'SNEAK', timer: 0, alerts: 0, lastKnown: { x: 0, y: 0 }, seen: false, spottedBy: null,
    T: { ALERT: 10, EVASION: 12, CAUTION: 15 },
    reset() { this.phase = 'SNEAK'; this.timer = 0; this.seen = false; },
    canSee(u, p) {
      const v = u.vis; if (!v || u.dead || u.stunned > 0) return false;
      const dx = p.x - u.x, dy = p.y - u.y, d = Math.hypot(dx, dy);
      if (d > v.range + p.r) return false;
      if (d > p.r && Math.abs(M.wrap(M.angTo(u.x, u.y, p.x, p.y) - u.look)) > v.half + Math.atan2(p.r, Math.max(d, 1))) return false;
      if (p.hidden && d > 70) return false;
      return W.los(u.x, u.y, p.x, p.y);
    },
    noise(x, y, r, str, units) {
      for (const u of units) {
        if (u.dead || !u.vis) continue;
        const d = M.dist(x, y, u.x, u.y); if (d > r) continue;
        if (u.mode === 'alert') { u.goal = { x, y }; continue; }
        // a guard REACTS to a sound a beat after hearing it - so a cannon shell lands on a target that
        // has not turned yet, which is what makes the sneak strike possible with a loud gun
        const lvl = Math.min(0.95, 0.35 + str * (1 - d / r));
        if (!u.heard || lvl > u.heard.lvl) u.heard = { x, y, lvl, t: 0.35 };
      }
    },
    hearTick(u, dt) {
      const h = u.heard; if (!h || u.dead) return;
      if ((h.t -= dt) > 0) return;
      u.heard = null;
      if (u.mode === 'alert') return;
      u.aware = Math.max(u.aware, h.lvl);
      if (u.aware >= 0.3) { u.mode = 'suspect'; u.goal = { x: h.x, y: h.y }; u.suspectT = 4; }
    },
    raise(u, p, units) {
      if (this.phase !== 'ALERT') { this.alerts++; TD.Audio.play('alert'); TD.game && TD.game.say('!', u); }
      this.phase = 'ALERT'; this.timer = this.T.ALERT; this.lastKnown = { x: p.x, y: p.y };
      for (const o of units) if (!o.dead && o.vis && M.dist(o.x, o.y, p.x, p.y) < (o.radio || 700)) { o.mode = 'alert'; o.aware = 1; o.goal = { x: p.x, y: p.y }; }
    },
    tick(dt, units, p) {
      const mul = this.phase === 'CAUTION' ? 1.5 : 1;
      this.seen = false;
      for (const u of units) {
        if (u.dead || !u.vis) continue;
        this.hearTick(u, dt);
        const sees = !p.dead && this.canSee(u, p);
        u.sees = sees;
        if (sees) {
          this.seen = true;
          if (this.phase === 'ALERT' || this.phase === 'EVASION' || u.mode === 'alert') { u.aware = 1; if (u.mode !== 'alert') u.mode = 'alert'; this.raise(u, p, units); continue; }
          const d = M.dist(u.x, u.y, p.x, p.y);
          u.aware += dt * (u.vis.rate || 1.15) * mul * (1.3 - d / u.vis.range) * (p.moving ? 1.25 : 0.8) * (p.hidden ? 0.35 : 1);
          u.goal = { x: p.x, y: p.y };
          if (u.aware >= 1) { this.raise(u, p, units); continue; }
          if (u.aware >= 0.3 && u.mode === 'patrol') { u.mode = 'suspect'; u.suspectT = 4; TD.Audio.play('blip', 0.7); }
        } else if (u.mode !== 'alert') {
          u.aware = Math.max(0, u.aware - dt * 0.12);
        }
      }
      if (this.phase === 'ALERT') {
        if (this.seen) { this.timer = this.T.ALERT; this.lastKnown = { x: p.x, y: p.y }; for (const u of units) if (u.mode === 'alert') u.goal = { x: p.x, y: p.y }; }
        else if ((this.timer -= dt) <= 0) {
          this.phase = 'EVASION'; this.timer = this.T.EVASION;
          for (const u of units) if (!u.dead && u.mode === 'alert') { u.mode = 'search'; u.goal = { x: this.lastKnown.x + M.rnd(-120, 120), y: this.lastKnown.y + M.rnd(-120, 120) }; u.searchT = 0; }
        }
      } else if (this.phase === 'EVASION') {
        if ((this.timer -= dt) <= 0) { this.phase = 'CAUTION'; this.timer = this.T.CAUTION; for (const u of units) if (!u.dead && u.mode === 'search') { u.mode = 'patrol'; u.aware = 0.15; } }
      } else if (this.phase === 'CAUTION') {
        if ((this.timer -= dt) <= 0) { this.phase = 'SNEAK'; this.timer = 0; }
      }
    },
    jammed() { return this.phase === 'ALERT' || this.phase === 'EVASION'; },

    // -------------------------------------------------------------- drawing
    drawCone(ctx, u, t) {
      const v = u.vis; if (!v || u.dead) return;
      const mode = u.mode || 'patrol', col = COL[mode] || 'green', shape = v.half < 0.42 ? 'tall' : 'wide', P = PLATE[shape];
      const sy = v.range / P.len, sx = sy * Math.tan(v.half) / (P.hw / P.hd);
      const alpha = mode === 'patrol' ? 0.5 : mode === 'alert' ? 0.85 : 0.75;
      ART.draw(ctx, 'bmfx_fov_' + col + '_' + shape, u.x, u.y, { a: u.look, sx, sy, ax: P.ax, ay: P.ay, alpha });
    },
    drawMark(ctx, u, t) {
      if (u.dead || !u.vis) return;
      const y = u.y - (u.markY || 34);
      if (u.mode === 'suspect' || u.mode === 'search') {
        const on = u.mode === 'search' || Math.floor(t * (3 + u.aware * 9)) % 2 === 0;
        if (on) ART.draw(ctx, 'bmfx_alert_yellow_danger', u.x, y, { s: 0.2 });
      } else if (u.mode === 'alert' && (u.sees || u.fireWarn > 0)) {
        if (u.fireWarn <= 0 || Math.floor(t * 14) % 2 === 0) ART.draw(ctx, 'bmfx_alert_red_danger', u.x, y, { s: 0.22 });
      }
    },
    // Soliton-style radar, top-right. Jammed in ALERT and EVASION.
    drawRadar(ctx, p, units, t, rx, ry, size) {
      const sc = 0.16, half = size / 2;
      ctx.save(); ctx.translate(rx, ry);
      ctx.fillStyle = 'rgba(4,24,12,0.82)'; ctx.fillRect(0, 0, size, size);
      ctx.beginPath(); ctx.rect(0, 0, size, size); ctx.clip();
      if (this.jammed()) {
        for (let i = 0; i < 160; i++) { const g = (Math.random() * 120) | 0; ctx.fillStyle = 'rgb(' + g + ',' + (g + 40) + ',' + g + ')'; ctx.fillRect(Math.random() * size, Math.random() * size, 2, 2); }
        ctx.fillStyle = Math.floor(t * 3) % 2 ? '#ff5040' : '#ffd040'; ctx.font = '10px BOFCommand, monospace'; ctx.textAlign = 'center';
        ctx.fillText('JAMMING', half, half + 4);
      } else {
        ctx.strokeStyle = 'rgba(80,200,120,0.18)'; ctx.lineWidth = 1;
        for (let g = 0; g <= size; g += 12) { ctx.beginPath(); ctx.moveTo(g, 0); ctx.lineTo(g, size); ctx.moveTo(0, g); ctx.lineTo(size, g); ctx.stroke(); }
        const ox = p.x - half / sc, oy = p.y - half / sc;
        for (const q of W.near(oy, oy + size / sc)) {
          ctx.fillStyle = q.t === 'b' ? 'rgba(150,200,160,0.55)' : q.t === 'h' ? 'rgba(40,120,50,0.6)' : 'rgba(0,0,0,0.7)';
          ctx.fillRect((q.x0 - ox) * sc, (q.y0 - oy) * sc, (q.x1 - q.x0) * sc, (q.y1 - q.y0) * sc);
        }
        for (const u of units) {
          if (u.dead || !u.vis) continue;
          const x = (u.x - ox) * sc, y = (u.y - oy) * sc; if (x < -20 || y < -20 || x > size + 20 || y > size + 20) continue;
          const c = u.mode === 'alert' ? '255,60,40' : (u.mode === 'patrol' ? '90,230,110' : '255,210,60');
          ctx.fillStyle = 'rgba(' + c + ',0.35)'; ctx.beginPath(); ctx.moveTo(x, y);
          ctx.arc(x, y, u.vis.range * sc, u.look + Math.PI / 2 - u.vis.half, u.look + Math.PI / 2 + u.vis.half); ctx.closePath(); ctx.fill();
          ctx.fillStyle = 'rgb(' + c + ')'; ctx.fillRect(x - 2, y - 2, 4, 4);
        }
        ctx.fillStyle = '#ffffff'; ctx.save(); ctx.translate(half, half); ctx.rotate(p.a); ctx.beginPath(); ctx.moveTo(0, 5); ctx.lineTo(-3.5, -3.5); ctx.lineTo(3.5, -3.5); ctx.closePath(); ctx.fill(); ctx.restore();
      }
      ctx.restore();
      ctx.strokeStyle = this.jammed() ? '#c0302a' : '#3c9a58'; ctx.lineWidth = 2; ctx.strokeRect(rx, ry, size, size);
    },
  };
}(window));
