/*
 * Bullets of Fury: Overdrive - top-down ground stages.
 * ART: every sprite here is Bullets of Fury's own art, resolved through the game's own manifest
 * (../../assets/manifest.js -> window.BOFX). Nothing is drawn procedurally in place of a sprite.
 *
 *   ART.get(key)   -> {im,sx,sy,sw,sh} once the sheet has decoded, else null (and starts the load)
 *   ART.draw(ctx,key,x,y,o)   o = {a (rad, canvas clockwise), s (scale), ax/ay (anchor px in the cell,
 *                               default centre), alpha, flash (0..1 white), tint ('#rrggbb' silhouette)}
 *
 * Pixel reads are never used (getImageData throws on a file:// page and this must run from disk);
 * the white hit-flash and the black shadow are built by compositing, which works on any image.
 */
(function (root) {
  'use strict';
  const BASE = '../../';
  const LOOSE = {};
  for (const [key, meta] of Object.entries((root.TD_CAMPAIGN_ART || {}).frames || {})) LOOSE[key] = meta.file;
  LOOSE.pav_niel = 'expansion/windstorm_machinists/identity/niel_avatar_v2.png';
  for (const [key, meta] of Object.entries(root.TD_GROUND_ART || {})) LOOSE[key] = 'expansion/topdown/art/ground_1008/' + meta.file;
  for (const [key, meta] of Object.entries(root.TD_MUSEUM_ART || {})) LOOSE[key] = meta.file;   // 1009 Level 5 museum
  for (const k of ['debris', 'dust', 'hull_0', 'hull_1', 'hull_2', 'hull_3', 'hull_4', 'hull_5', 'hull_6', 'hull_7', 'hull_base',
    'machinegun', 'missile_pod', 'muzzle', 'razor_missile', 'rotor', 'sonic_bullet', 'sonic_charge', 'sonic_impact', 'sonic_ring',
    'sonic_wave', 'tread', 'turret', 'turret_damaged', 'wreck']) LOOSE['rzb_' + k] = 'assets/game/levels/stage_01/miniboss/bosses/razorback/rzb_' + k + '.png';
  for (const r of ['a', 'b', 'c', 'd', 'f', 'l', 's']) LOOSE['rank_' + r] = 'assets/game/shared/ui/ui/debrief_0916/rankplate_' + r + '.png';
  Object.assign(LOOSE, {
    life_up: 'assets/game/shared/ui/ui/pickups_0915/life_up_wings.png',
    score_100: 'assets/game/shared/ui/ui/pickups_0917b/score_100.png', score_250: 'assets/game/shared/ui/ui/pickups_0917b/score_250.png',
    score_500: 'assets/game/shared/ui/ui/pickups_0917b/score_500.png', score_1000: 'assets/game/shared/ui/ui/pickups_0917b/score_1000.png',
    fury_bomb: 'assets/game/shared/ui/ui/pickups_0917b/fury_bomb.png', pow_badge: 'assets/game/shared/ui/ui/infusion_0917/inf_kinetic.png', logo: 'assets/game/shared/ui/ui/logo_0916/bof_logo.png',
    overdrive: 'expansion/concept/overdrive_word_overlay.png',
    target_retina: 'assets/game/levels/stage_03/boss/bosses/stage3_thermo/nuclear_retina.png',
    // 1008g: the ground pack. Player tanks are baked per pilot paint; enemies are the on-foot alien tanks
    ...Object.fromEntries(['axel', 'cole', 'maverick', 'decker', 'yuri', 'freezer', 'juggernaut', 'phoenix', 'lizzie', 'falva', 'hotwire']
      .flatMap(p => ['hull', 'turret', 'damaged_hull', 'wreck'].map(k => ['pt_' + p + '_' + k, 'expansion/topdown/art/tanks/' + p + '_' + k + '.png']))),
    ...Object.fromEntries(['light', 'heavy'].flatMap(t => ['idle', 'tread', 'fire', 'damaged', 'wreck'].map(k => ['et_' + t + '_' + k, 'expansion/onfoot/enemies/' + t + '_tank_' + k + '.png']))),
    ...Object.fromEntries(['muzzle', 'impact', 'destruction'].flatMap(f => [0, 1, 2, 3, 4, 5].map(i => ['gfx_' + f + '_' + i, 'expansion/ground/fx/' + f + '_' + i + '.png']))),
    gfx_shell: 'expansion/ground/fx/shell.png', gfx_ap_shell: 'expansion/ground/fx/ap_shell.png',
    ...Object.fromEntries(['ammo', 'weapon'].flatMap(c => [['intact', 'closed'], ['damaged', 'open'], ['critical', 'broken']].map(([st, f]) => ['gp_' + c + '_crate_' + st, 'expansion/ground/pickups/' + c + '_crate_' + f + '.png']))),
    ...Object.fromEntries(['axel', 'cole', 'maverick', 'decker', 'yuri', 'freezer', 'juggernaut', 'lizzie', 'falva'].map(p => ['pav_' + p, 'assets/game/pilots/' + p + '/portraits/pilots_0922/portraits/' + p + '-idle.png'])),
    pav_hotwire: 'expansion/pilot_avatars/hotwire-idle.png', pav_phoenix: 'expansion/pilot_avatars/phoenix-idle.png',
    // the on-foot pack's turret set: turrets and cameras (the old nlgt_/nmrv_ cores went to the archive in the 1006 cleanup)
    ...Object.fromEntries(['base', 'north', 'fire', 'damaged', 'wreck'].map(k => ['oft_' + k, 'expansion/onfoot/enemies/turret_' + k + '.png'])),
    hotwire_idle: 'expansion/pilot_avatars/hotwire-idle.png', phoenix_idle: 'expansion/pilot_avatars/phoenix-idle.png',
  });
  const images = {};
  function image(path) {
    let im = images[path];
    if (!im) { im = new Image(); im.decoding = 'async'; im.src = BASE + path; images[path] = im; }
    return im;
  }
  const ok = im => im.complete && im.naturalWidth > 0;

  function resolve(key) {
    const X = root.BOFX; if (!X) return null;
    const c = X.cells[key];
    if (c) return { path: X.img['nca_' + c[0]] || X.img[c[0]], sx: c[1], sy: c[2], sw: c[3], sh: c[4] };
    const pc = X.playercells && X.playercells[key];
    if (pc) return { path: X.img[pc[0]] || X.img['nca_' + pc[0]], sx: pc[1], sy: pc[2], sw: pc[3], sh: pc[4] };
    const ic = X.icons && X.icons[key];
    if (ic) return { path: X.img[ic[4] || 'nia_icons'], sx: ic[0], sy: ic[1], sw: ic[2], sh: ic[3] };
    const p = LOOSE[key] || X.img[key];
    return p ? { path: p, sx: 0, sy: 0, sw: 0, sh: 0 } : null;
  }
  const rcache = {};
  function get(key) {
    let r = rcache[key];
    if (r === undefined) { r = rcache[key] = resolve(key); }
    if (!r) return null;
    const im = image(r.path);
    if (!ok(im)) return null;
    return { im, sx: r.sx, sy: r.sy, sw: r.sw || im.naturalWidth, sh: r.sh || im.naturalHeight };
  }
  function has(key) { if (rcache[key] === undefined) rcache[key] = resolve(key); return !!rcache[key]; }
  function warm(keys) { for (const k of keys) get(k); }
  function progress(keys) { let n = 0; for (const k of keys) if (get(k)) n++; return keys.length ? n / keys.length : 1; }

  // silhouettes (white flash / black shadow) - one small canvas per key+colour, built by compositing
  const sil = {};
  function silhouette(key, col) {
    const id = key + col; if (sil[id]) return sil[id];
    const g = get(key); if (!g) return null;
    const cv = document.createElement('canvas'); cv.width = g.sw; cv.height = g.sh;
    const c = cv.getContext('2d'); c.drawImage(g.im, g.sx, g.sy, g.sw, g.sh, 0, 0, g.sw, g.sh);
    c.globalCompositeOperation = 'source-in'; c.fillStyle = col; c.fillRect(0, 0, g.sw, g.sh);
    return (sil[id] = cv);
  }
  function draw(ctx, key, x, y, o) {
    o = o || {};
    const g = get(key); if (!g) return false;
    const s = o.s == null ? 1 : o.s, sx = o.sx == null ? s : o.sx, sy = o.sy == null ? s : o.sy;
    const ax = o.ax == null ? g.sw / 2 : o.ax, ay = o.ay == null ? g.sh / 2 : o.ay;
    ctx.save(); ctx.translate(x, y); if (o.a) ctx.rotate(o.a);
    if (o.alpha != null) ctx.globalAlpha *= o.alpha;
    if (o.comp) ctx.globalCompositeOperation = o.comp;
    if (o.tint) { const t = silhouette(key, o.tint); if (t) ctx.drawImage(t, -ax * sx, -ay * sy, g.sw * sx, g.sh * sy); }
    else ctx.drawImage(g.im, g.sx, g.sy, g.sw, g.sh, -ax * sx, -ay * sy, g.sw * sx, g.sh * sy);
    if (o.flash > 0) { const w = silhouette(key, '#ffffff'); if (w) { ctx.globalAlpha *= Math.min(1, o.flash); ctx.drawImage(w, -ax * sx, -ay * sy, g.sw * sx, g.sh * sy); } }
    ctx.restore(); return true;
  }
  function size(key) { const g = get(key); return g ? [g.sw, g.sh] : null; }
  root.ART = { get, has, warm, progress, draw, size, silhouette, image, ok, BASE };
}(window));
