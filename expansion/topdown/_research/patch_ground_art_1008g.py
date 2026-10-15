"""1008g: Level 2 wears the Overdrive ground art.

Player: the ground pack's siege / assault / panzer tank in the chosen pilot's paint (baked by
bake_ground_tanks.py), picked on the briefing screen. Enemies: the on-foot pack's alien light and
heavy tanks. Ordnance and effects: the ground pack's shells, muzzle / impact / destruction reels
and crates. Every edit is anchored on content and refuses if its anchor is missing.
"""
import os
HERE = os.path.join(os.path.dirname(__file__), '..')
if "V = '1008f'" not in open(os.path.join(HERE, 'index.html')).read():
    raise SystemExit('already past 1008f: this patch is applied, and later drops (repath_1008h) rewrote its strings')

def patch(path, pairs):
    p = os.path.join(HERE, path); s = open(p, encoding='utf-8', newline='').read()
    crlf = '\r\n' in s                      # follow the file's own line ending (main.js is CRLF)
    for old, new in pairs:
        if crlf: old, new = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
        if new in s: continue    # already applied (a replacement may contain its own anchor)
        assert s.count(old) == 1, (path, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('patched', path, len(pairs))

# ---------------------------------------------------------------- art.js: the new loose keys
patch('js/art.js', [(
"""    // the on-foot pack's turret set""",
"""    // 1008g: the ground pack. Player tanks are baked per pilot paint; enemies are the on-foot alien tanks
    ...Object.fromEntries(['axel', 'cole', 'maverick', 'decker', 'yuri', 'freezer', 'juggernaut', 'phoenix', 'lizzie', 'falva', 'hotwire']
      .flatMap(p => ['hull', 'turret', 'damaged_hull', 'wreck'].map(k => ['pt_' + p + '_' + k, 'expansion/topdown/art/tanks/' + p + '_' + k + '.png']))),
    ...Object.fromEntries(['light', 'heavy'].flatMap(t => ['idle', 'tread', 'fire', 'damaged', 'wreck'].map(k => ['et_' + t + '_' + k, 'expansion/onfoot/enemies/' + t + '_tank_' + k + '.png']))),
    ...Object.fromEntries(['muzzle', 'impact', 'destruction'].flatMap(f => [0, 1, 2, 3, 4, 5].map(i => ['gfx_' + f + '_' + i, 'expansion/ground/fx/' + f + '_' + i + '.png']))),
    gfx_shell: 'expansion/ground/fx/shell.png', gfx_ap_shell: 'expansion/ground/fx/ap_shell.png',
    ...Object.fromEntries(['ammo', 'weapon'].flatMap(c => [['intact', 'closed'], ['damaged', 'open'], ['critical', 'broken']].map(([st, f]) => ['gp_' + c + '_crate_' + st, 'expansion/ground/pickups/' + c + '_crate_' + f + '.png']))),
    ...Object.fromEntries(['axel', 'cole', 'maverick', 'decker', 'yuri', 'freezer', 'juggernaut', 'lizzie', 'falva'].map(p => ['pav_' + p, 'assets/game/pilots_0922/portraits/' + p + '-idle.png'])),
    pav_hotwire: 'expansion/pilot_avatars/hotwire-idle.png', pav_phoenix: 'expansion/pilot_avatars/phoenix-idle.png',
    // the on-foot pack's turret set""")])

# ---------------------------------------------------------------- core.js: reels of any length, anchored
patch('js/core.js', [
("""    boom(x, y, size, kind) {
      const fam = kind || (size > 70 ? 'nxp_dense_' : 'nxp_clus_');
      this.list.push({ k: 'reel', fam, n: 8, x, y, t: 0, life: 0.5 + size / 300, s: size / 200, a: Math.random() * 6.28 });""",
"""    boom(x, y, size, kind, n) {
      const fam = kind || (size > 70 ? 'nxp_dense_' : 'nxp_clus_');
      this.list.push({ k: 'reel', fam, n: n || 8, x, y, t: 0, life: 0.5 + size / 300, s: size / 200, a: Math.random() * 6.28 });"""),
# the ground pack's muzzle reel is authored firing north with its root at the bottom
("""    flash(x, y, a, s) { this.list.push({ k: 'img', key: 'rzb_muzzle', x, y, vx: 0, vy: 0, t: 0, life: 0.07, s: s || 0.18, a: a + Math.PI, ay: 0.85 }); },""",
"""    flash(x, y, a, s) { this.list.push({ k: 'reel', fam: 'gfx_muzzle_', n: 6, x, y, t: 0, life: 0.14, s: (s || 0.18) * 1.6, a: a + Math.PI, ay: 0.8 }); },"""),
("""        if (p.k === 'reel') ART.draw(ctx, p.fam + Math.min(7, (q * p.n) | 0), p.x, p.y, { s: p.s, a: p.a });""",
"""        if (p.k === 'reel') { const key = p.fam + Math.min(p.n - 1, (q * p.n) | 0); ART.draw(ctx, key, p.x, p.y, { s: p.s, a: p.a, ay: p.ay != null ? (ART.size(key) || [0, 0])[1] * p.ay : null }); }"""),
])

# ---------------------------------------------------------------- tank.js
patch('js/tank.js', [
# the player knows its pilot; the art follows from it
("""smoke: 3, weapons: [{ id: 'vulcan', lv: 1 }], wi: 0, dead: false, hidden: false, moving: false, art: 'tk3', speed: 2.05,""",
 """smoke: 3, weapons: [{ id: 'vulcan', lv: 1 }], wi: 0, dead: false, hidden: false, moving: false, pilot: TD.pilot || 'cole', speed: 2.05,"""),
("""  TD.drawTank = drawTank;""",
"""  TD.drawTank = drawTank;

  // 1008g: the Overdrive ground tanks. 192 px north-facing canvases, hull centre (96,124) on every family;
  // the turret shares the canvas, so it sits in its socket by construction. a=0 faces south here.
  TD.PILOTS = ['cole', 'axel', 'maverick', 'decker', 'yuri', 'freezer', 'juggernaut', 'phoenix', 'lizzie', 'falva', 'hotwire'];
  TD.FAMILY = { siege: ['juggernaut', 'phoenix'], panzer: ['lizzie', 'falva', 'hotwire'] };
  TD.familyOf = pk => TD.FAMILY.siege.includes(pk) ? 'siege' : TD.FAMILY.panzer.includes(pk) ? 'panzer' : 'assault';
  const MUZZLE = { siege: 30, assault: 38, panzer: 45 };    // native muzzle distance from the hull centre, halved to draw scale
  TD.muzzleDist = p => MUZZLE[TD.familyOf(p.pilot)];
  const PS = 0.5;
  TD.drawPlayerTank = function (ctx, p, o) {
    o = o || {};
    const k = 'pt_' + p.pilot + '_', a = p.a + Math.PI, hull = k + (p.hp < p.max * 0.4 ? 'damaged_hull' : 'hull');
    const opt = { a, s: PS, ax: 96, ay: 124 };
    ART.draw(ctx, hull, p.x + 4, p.y + 6, Object.assign({}, opt, { tint: '#000000', alpha: 0.33 }));
    ART.draw(ctx, hull, p.x, p.y, Object.assign({}, opt, { flash: o.flash || 0 }));
    // recoil slides the turret back along the barrel; the hull stays put
    const [fx, fy] = M.fwd(p.a), kick = Math.min(4, (p.recoil || 0) * 0.5);
    ART.draw(ctx, k + 'turret', p.x - fx * kick, p.y - fy * kick, Object.assign({}, opt, { flash: o.flash || 0 }));
  };
  // enemy armour: the on-foot pack's alien tanks, whole plates authored facing north
  function drawAlienTank(ctx, u, T) {
    const mv = Math.hypot(u.x - (u.lx == null ? u.x : u.lx), u.y - (u.ly == null ? u.y : u.ly)) > 0.15; u.lx = u.x; u.ly = u.y;
    const st = (u.burst > 0 || u.fireWarn > 0) ? 'fire' : u.hp < u.max * 0.5 ? 'damaged' : mv && ((TD.game.t / 6) | 0) % 2 ? 'tread' : 'idle';
    const key = 'et_' + T.et + '_' + st, o = { a: u.a + Math.PI, s: T.ds };
    ART.draw(ctx, key, u.x + 4, u.y + 6, Object.assign({}, o, { tint: '#000000', alpha: 0.33 }));
    ART.draw(ctx, key, u.x, u.y, Object.assign({}, o, { flash: u.flash > 0 ? u.flash / 0.12 : 0 }));
  }"""),
("""    const mx = p.x + fx * 26, my = p.y + fy * 26;""",
 """    const md = TD.muzzleDist(p) - 4, mx = p.x + fx * md, my = p.y + fy * md;"""),
("""    const [fx, fy] = M.fwd(p.a), mx = p.x + fx * 30, my = p.y + fy * 30, big = power >= 1;""",
 """    const [fx, fy] = M.fwd(p.a), md = TD.muzzleDist(p), mx = p.x + fx * md, my = p.y + fy * md, big = power >= 1;"""),
# enemies
("""    scout: { art: 'tk0',""", """    scout: { art: 'tk0', et: 'light', ds: 0.56,"""),
("""    rifle: { art: 'tk1',""", """    rifle: { art: 'tk1', et: 'light', ds: 0.62,"""),
("""    heavy: { art: 'tk2',""", """    heavy: { art: 'tk2', et: 'heavy', ds: 0.66,"""),
("""    sniper: { art: 'tk4',""", """    sniper: { art: 'tk4', et: 'heavy', ds: 0.58,"""),
("""    } else drawTank(ctx, u, T.art);""",
 """    } else if (T.et) drawAlienTank(ctx, u, T);
    else drawTank(ctx, u, T.art);"""),
("""      FX.boom(u.x, u.y, 110, 'nxp_dense_'); FX.debris""",
 """      if (ET[u.type].et) FX.boom(u.x, u.y, 150, 'gfx_destruction_', 6); else FX.boom(u.x, u.y, 110, 'nxp_dense_'); FX.debris"""),
("""art: ET[u.type].wreck || ET[u.type].art, still: ET[u.type].still, s: ET[u.type].ds });""",
 """art: ET[u.type].et ? 'et_' + ET[u.type].et + '_wreck' : ET[u.type].wreck || ET[u.type].art, still: ET[u.type].still || !!ET[u.type].et, s: ET[u.type].ds });"""),
# crates are the ground pack's ammo / weapon crates: closed, open, broken
("""    crate: { key: 'nef_s1_ammo_crate_', hp: 4, r: 15, s: 0.17 },
    pbox: { key: 'crate6_0', hp: 2, r: 11, s: 0.42, still: true },""",
 """    crate: { key: 'gp_ammo_crate_', hp: 4, r: 15, s: 0.5 },
    pbox: { key: 'gp_weapon_crate_', hp: 2, r: 13, s: 0.44 },"""),
# the cannon round and its impact
("""    else if (s.k === 'shell') ART.draw(ctx, 'nlz_slug', s.x, s.y, { a: s.a, s: s.big ? 0.95 : 0.6 });""",
 """    else if (s.k === 'shell') ART.draw(ctx, s.big ? 'gfx_ap_shell' : 'gfx_shell', s.x, s.y, { a: s.a + Math.PI, s: s.big ? 0.75 : 0.55 });"""),
("""      FX.boom(s.x, s.y, s.big ? 140 : 70, s.big ? 'nxp_dense_' : 'nxp_clus_'); if (s.big) FX.ring(s.x, s.y, 0.6);""",
 """      FX.boom(s.x, s.y, s.big ? 140 : 70, s.big ? 'nxp_dense_' : 'nxp_clus_'); FX.boom(s.x, s.y, s.big ? 120 : 80, 'gfx_impact_', 6); if (s.big) FX.ring(s.x, s.y, 0.6);"""),
])

# ---------------------------------------------------------------- main.js
patch('js/main.js', [
("""  const WARM = ['nst4b_master', 'tk3_inta_n', 'tk3_inta_e', 'tk3_inta_s', 'tk3_inta_w', 'tk0_inta_s', 'tk1_inta_s', 'tk2_inta_s', 'tk4_inta_s',""",
 """  const WARM = ['nst4b_master', 'pt_cole_hull', 'pt_cole_turret', 'et_light_idle', 'et_light_tread', 'et_light_fire', 'et_heavy_idle', 'et_heavy_tread', 'et_heavy_fire',
    'gfx_muzzle_0', 'gfx_muzzle_2', 'gfx_impact_2', 'gfx_destruction_2', 'gfx_shell', 'gp_ammo_crate_intact', 'gp_weapon_crate_intact', 'pav_cole',"""),
("""      this.wrecks.push({ x: p.x, y: p.y, a: p.a, art: p.art, player: true });""",
 """      FX.boom(p.x, p.y, 170, 'gfx_destruction_', 6);
      this.wrecks.push({ x: p.x, y: p.y, a: p.a, art: 'pt_' + p.pilot + '_wreck', still: true, s: 0.5, player: true });"""),
("""      TD.drawTank(ctx, Object.assign({}, p, { flash: blink ? 0.12 : p.flash }), p.art);""",
 """      TD.drawPlayerTank(ctx, p, { flash: blink ? 1 : p.flash > 0 ? p.flash / 0.18 : 0 });"""),
# the briefing chooses the pilot (LEFT/RIGHT), remembered between runs
("""      Cam.follow(G.player.x, G.player.y - 60, 0.05);
      if (G.stateT > 0.6 && I.confirm()) setState('play');""",
 """      Cam.follow(G.player.x, G.player.y - 60, 0.05);
      const step = I.tap('left') ? -1 : I.tap('right') ? 1 : 0;
      if (step) {
        const L = TD.PILOTS, i = (L.indexOf(TD.pilot) + step + L.length) % L.length;
        TD.pilot = G.player.pilot = L[i]; A.play('blip');
        try { localStorage.setItem('bof_td_pilot', TD.pilot); } catch (e) {}
        ART.warm(['pt_' + TD.pilot + '_hull', 'pt_' + TD.pilot + '_turret', 'pt_' + TD.pilot + '_damaged_hull', 'pt_' + TD.pilot + '_wreck', 'pav_' + TD.pilot]);
      }
      if (G.stateT > 0.6 && I.confirm()) setState('play');"""),
("""  function drawBrief() {
    drawWorld();
    ctx.fillStyle = 'rgba(0,0,0,0.62)'; ctx.fillRect(0, 0, VW, VH);
    text(DATA.title, VW / 2, 70, 14, '#9fe0ff', 'center'); text(DATA.name, VW / 2, 96, 22, '#ffd060', 'center');""",
 """  function drawBrief() {
    drawWorld();
    ctx.fillStyle = 'rgba(0,0,0,0.62)'; ctx.fillRect(0, 0, VW, VH);
    text(DATA.title, VW / 2, 34, 12, '#9fe0ff', 'center'); text(DATA.name, VW / 2, 56, 20, '#ffd060', 'center');
    // pilot and tank: LEFT / RIGHT
    const pk = G.player.pilot, fam = TD.familyOf(pk), t = G.t / 60;
    ART.draw(ctx, 'pav_' + pk, VW / 2 - 70, 104, { s: 0.25 });
    TD.drawPlayerTank(ctx, { pilot: pk, x: VW / 2 + 60, y: 108, a: Math.PI + Math.sin(t * 1.4) * 0.35, hp: 1, max: 1 });
    text(pk.toUpperCase(), VW / 2 + 60, 146, 11, '#fff', 'center');
    text(fam.toUpperCase() + ' TANK', VW / 2 + 60, 159, 8, '#ffd060', 'center');
    if (Math.floor(t * 3) % 2) { text('<', VW / 2 - 118, 104, 14, '#ffd060', 'center'); text('>', VW / 2 + 128, 104, 14, '#ffd060', 'center'); }
    text('LEFT / RIGHT: PILOT', VW / 2, 176, 8, '#9aa89a', 'center');"""),
("""    DATA.brief.forEach((line, i) => { const s = line.slice(0, Math.max(0, typed - n)); n += line.length; text(s, VW / 2, 150 + i * 22, 11, '#e8efe8', 'center'); });""",
 """    DATA.brief.forEach((line, i) => { const s = line.slice(0, Math.max(0, typed - n)); n += line.length; text(s, VW / 2, 198 + i * 15, 10, '#e8efe8', 'center'); });"""),
# title: the Level 2 card shows the chosen tank; Level 3's art is in, the level is not built yet
("""    const cards = [['LEVEL 2', TITLE, 'FURY TANK', 'tk3_inta_n'], ['LEVEL 3', 'BOOTS ON THE GROUND', 'PILOT ON FOOT', null]];""",
 """    const cards = [['LEVEL 2', TITLE, 'FURY TANK', 'tank'], ['LEVEL 3', 'BOOTS ON THE GROUND', 'PILOT ON FOOT', null]];"""),
("""      if (c[3]) ART.draw(ctx, c[3], cx, cy + 4, { s: 0.5 });
      else { ART.draw(ctx, 'hotwire_idle', cx - 34, cy + 6, { s: 0.22, alpha: 0.55 }); ART.draw(ctx, 'phoenix_idle', cx + 34, cy + 6, { s: 0.22, alpha: 0.55 }); text('ART PENDING', cx, cy + 6, 10, '#ff6040', 'center'); }""",
 """      if (c[3]) TD.drawPlayerTank(ctx, { pilot: TD.pilot, x: cx, y: cy + 4, a: Math.PI, hp: 1, max: 1 });
      else { ART.draw(ctx, 'hotwire_idle', cx - 34, cy + 6, { s: 0.22, alpha: 0.55 }); ART.draw(ctx, 'phoenix_idle', cx + 34, cy + 6, { s: 0.22, alpha: 0.55 }); text('IN DEVELOPMENT', cx, cy + 6, 10, '#ff9a40', 'center'); }"""),
("""    if (G.lockedT > 0) text('LEVEL 3 NEEDS ITS ON-FOOT PILOT SPRITES FIRST', VW / 2, 318, 10, '#ff8060', 'center');""",
 """    if (G.lockedT > 0) text('LEVEL 3 IS BEING BUILT NEXT', VW / 2, 318, 10, '#ff8060', 'center');"""),
("""  const TITLE = 'IRON INFILTRATION';""",
 """  const TITLE = 'IRON INFILTRATION';
  TD.pilot = 'cole';
  try { const s = localStorage.getItem('bof_td_pilot'); if (s && TD.PILOTS.includes(s)) TD.pilot = s; } catch (e) {}"""),
])

p = os.path.join(HERE, 'index.html'); s = open(p, newline='').read()
if "V = '1008f'" in s: open(p, 'w', newline='').write(s.replace("V = '1008f'", "V = '1008g'")); print('stamp 1008g')
