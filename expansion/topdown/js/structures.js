/* Authored destructible scenery. The same rectangles own drawing, cover, hits
 * and movement. A collapse retires its rectangle before the burst begins. */
(function (root) {
  'use strict';
  const TD = root.TD, M = TD.M, W = TD.World, FX = TD.FX;
  const TYPES = {
    warehouse: { hw: 65, hh: 57, hp: 26, sx: 0.62, sy: 0.57, fragment: 'roof_fragment' },
    relay: { hw: 56, hh: 52, hp: 19, sx: 0.57, sy: 0.55, fragment: 'wall_fragment' },
    barrier: { hw: 63, hh: 18, hp: 12, sx: 0.54, sy: 0.25, fragment: 'concrete_fragment' },
  };
  TD.makeStructure = function (spec) {
    const type = TYPES[spec.kind], s = Object.assign({ dead: false, flash: 0, hp: type.hp, max: type.hp }, spec);
    s.type = type;
    s.rect = W.add({ x0: s.x - type.hw, y0: s.y - type.hh, x1: s.x + type.hw, y1: s.y + type.hh, t: 'b', structure: s });
    return s;
  };
  TD.hitStructure = function (G, s, dmg, ram) {
    if (s.dead) return false;
    s.hp -= dmg; s.flash = 0.1;
    if (s.hp > 0) { if (ram) FX.concrete(s.x, s.y, 48); return true; }
    s.dead = true; W.remove(s.rect); G.structuresBroken = (G.structuresBroken || 0) + 1;
    const wall = s.kind === 'barrier';
    FX.concrete(s.x, s.y, wall ? 105 : 160);
    if (!wall) FX.boom(s.x, s.y, 95, 'gfx_destruction_', 6);
    for (let i = 0; i < (wall ? 4 : 5); i++) {
      const a = i * Math.PI * 2 / (wall ? 4 : 5) + 0.2, speed = wall ? 65 : 85;
      FX.fragment(s.type.fragment, s.x + Math.cos(a) * 14, s.y + Math.sin(a) * 10, a,
        wall ? 0.12 : 0.13, Math.cos(a) * speed, Math.sin(a) * speed);
    }
    TD.Audio.play(wall ? 'expS' : 'expB', wall ? 0.65 : 0.85); TD.Cam.kick(wall ? 3 : 5);
    TD.Stealth.noise(s.x, s.y, 320, 0.6, G.units);
    G.score += wall ? 150 : 650;
    if (s.drop) TD.dropPickup(G, s.x, s.y, s.drop);
    return true;
  };
  // Slab intersection returns the first impact, including an expanded projectile
  // radius. This also catches a cannon crossing a thin wall in one tick.
  function intersection(ax, ay, bx, by, rect, radius) {
    let t0 = 0, t1 = 1;
    for (const [start, end, lo, hi] of [[ax, bx, rect.x0 - radius, rect.x1 + radius], [ay, by, rect.y0 - radius, rect.y1 + radius]]) {
      const d = end - start;
      if (Math.abs(d) < 1e-8) { if (start < lo || start > hi) return null; continue; }
      let a = (lo - start) / d, b = (hi - start) / d;
      if (a > b) [a, b] = [b, a];
      t0 = Math.max(t0, a); t1 = Math.min(t1, b);
      if (t0 > t1) return null;
    }
    return t0;
  }
  TD.structureImpact = function (G, s, ax, ay, bx, by) {
    let nearest = null, best = 2;
    for (const q of G.structures) if (!q.dead) {
      const t = intersection(ax, ay, bx, by, q.rect, s.r || 0);
      if (t != null && t < best) { nearest = q; best = t; }
    }
    if (!nearest) return false;
    s.x = M.lerp(ax, bx, best); s.y = M.lerp(ay, by, best);
    TD.hitStructure(G, nearest, s.dmg);
    FX.concrete(s.x, s.y, 30);
    return true;
  };
  TD.ramStructures = function (G, ax, ay, bx, by, radius) {
    let count = 0;
    for (const s of G.structures) if (!s.dead && intersection(ax, ay, bx, by, s.rect, radius) != null) {
      TD.hitStructure(G, s, s.max + 1, true); count++;
    }
    return count;
  };
  TD.blastStructures = function (G, x, y, radius, damage) {
    for (const s of G.structures) if (!s.dead) {
      const q = s.rect, distance = Math.hypot(x - M.clamp(x, q.x0, q.x1), y - M.clamp(y, q.y0, q.y1));
      if (distance < radius) TD.hitStructure(G, s, damage * (1 - distance / radius * 0.4));
    }
  };
  TD.drawStructures = function (ctx, G) {
    for (const s of G.structures) {
      const state = s.dead ? 'rubble' : s.hp < s.max * 0.6 ? 'damaged' : 'intact';
      ART.draw(ctx, s.kind + '_' + state, s.x, s.y, { sx: s.type.sx, sy: s.type.sy, flash: s.flash > 0 ? s.flash / 0.1 : 0 });
    }
  };
})(window);
