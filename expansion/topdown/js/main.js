/*
 * Bullets of Fury: Overdrive - top-down ground stages. The game: states, loop, HUD, mission flow.
 *   load -> title (stage select) -> brief -> play <-> pause -> clear / gameover
 * A fixed 60 Hz step drives everything; window.TDGAME exposes step(n) and the state for probes.
 */
(function (root) {
  'use strict';
  const TD = root.TD, M = TD.M, W = TD.World, A = TD.Audio, FX = TD.FX, Cam = TD.Cam, I = TD.Input, S = TD.Stealth;
  const VW = TD.VW, VH = TD.VH;
  const cv = document.getElementById('screen'), ctx = cv.getContext('2d');
  let SC = 2;
  function fit() {
    const k = Math.max(1, Math.floor(Math.min(root.innerWidth / VW, (root.innerHeight - 4) / VH)));
    SC = Math.max(2, k); cv.width = VW * SC; cv.height = VH * SC;
    cv.style.width = VW * k + 'px'; cv.style.height = VH * k + 'px';
  }
  root.addEventListener('resize', fit); fit();

  let MAP = TD.LEVEL2_MAP, DATA = TD.LEVEL2_DATA, MISSION = TD.MISSIONS[0];
  const WARM = [...TD.CAMPAIGN_WARM, ...(TD.MUSEUM_WARM || []), 'rzb_hull_1', 'rzb_hull_2', 'rzb_hull_3', 'rzb_hull_4', 'rzb_hull_5', 'rzb_hull_6', 'rzb_hull_7', 'rzb_tread', 'rzb_rotor', 'rzb_missile_pod', 'rzb_machinegun', 'rzb_turret_damaged', 'rzb_sonic_charge', 'rzb_sonic_bullet', 'rzb_sonic_wave', 'rzb_wreck', 'bmfx_alert_red_incoming_projectile', ...Object.keys(root.TD_GROUND_ART || {}), 'pad_a', 'pad_b', 'pad_c', 'pad_x', 'pad_y', 'pad_z', 'pad_start', 'pad_dpad',
    'target_retina', 'pt_cole_hull', 'pt_cole_turret', 'et_light_idle', 'et_light_tread', 'et_light_fire', 'et_heavy_idle', 'et_heavy_tread', 'et_heavy_fire',
    ...['muzzle', 'impact', 'destruction'].flatMap(f => [0, 1, 2, 3, 4, 5].map(i => 'gfx_' + f + '_' + i)), 'gfx_shell', 'gfx_ap_shell',
    'et_light_damaged', 'et_light_wreck', 'et_heavy_damaged', 'et_heavy_wreck', 'gp_ammo_crate_damaged', 'gp_ammo_crate_critical', 'gp_weapon_crate_damaged', 'gp_weapon_crate_critical', 'gp_ammo_crate_intact', 'gp_weapon_crate_intact', 'pav_cole',
    'oft_north', 'oft_base', 'oft_fire', 'oft_damaged', 'oft_wreck', 'bmfx_fov_green_wide', 'bmfx_fov_yellow_wide', 'bmfx_fov_red_wide',
    'bmfx_fov_green_tall', 'bmfx_fov_yellow_tall', 'bmfx_fov_red_tall', 'bmfx_alert_yellow_danger', 'bmfx_alert_red_danger',
    'nxp_dense_3', 'nxp_clus_3', 'rzb_dust', 'rzb_muzzle', 'rzb_hull_0', 'rzb_turret', 'mfx_mg_2_4', 'mfx_mg_0_4', 'nlz_slug', 'logo',
    'nef_s1_fuel_barrel_intact', 'nef_s1_ammo_crate_intact', 'crate6_0', 'micon_mg_1', 'bmbar_frame_boss', 'bmbar_fill_red', 'bmbar_tab_boss'];
  const TITLE = 'IRON INFILTRATION';
  TD.pilot = 'cole';
  try { const s = localStorage.getItem('bof_td_pilot'); if (s && TD.PILOTS.includes(s)) TD.pilot = s; } catch (e) {}

  // ------------------------------------------------------------------ the game object
  const G = TD.game = {
    state: 'load', t: 0, stateT: 0, player: null, units: [], shots: [], eshots: [], props: [], structures: [], pickups: [], wrecks: [], grenades: [],
    boss: null, msgs: [], score: 0, kills: 0, deaths: 0, lives: 3, cp: null, time: 0, extra: 0, reinfT: 0, sel: 0, paused: false,
    say(text, at) { this.msgs.push({ text, x: at ? at.x : this.player.x, y: at ? at.y - 40 : this.player.y - 40, t: 0 }); },
    playerDied() {
      const p = this.player; p.dead = true; p.deadT = 0; this.deaths++;
      if (p.onfoot) { p.reload=0; p.reloadGun=null; p.action=null; A.play('hit'); return; }
      p.deathStart=p.a;p.crashed=false;p.charge=0;FX.boom(p.x,p.y,50,'gfx_impact_',6);A.play('hit');
    },
    bossDown() { this.bossDeadT = 0; this.score += 30000; },
  };

  function start() {
    MISSION = TD.MISSIONS[G.sel] || TD.MISSIONS[0]; MAP = MISSION.map; DATA = MISSION.data;
    W.load(MAP.w, MAP.h, MAP.rects);
    S.reset(); S.alerts = 0;
    Object.assign(G, { units: [], shots: [], eshots: [], props: [], structures: [], pickups: [], wrecks: [], grenades: [], msgs: [], boss: null, bossDeadT: null,
      score: 0, kills: 0, deaths: 0, lives: 3, time: 0, extra: 0, reinfT: 0, structuresBroken: 0, ally: null, footGrenades: [], burns: [], mission: MISSION.id });
    FX.list = []; Cam.zoom = 1;
    G.player = (MISSION.mode === 'foot' ? TD.makeFootPlayer : TD.makePlayer)(DATA.start.x, DATA.start.y); G.player.a = DATA.start.a;
    G.player.aim = G.player.a;
    G.cp = { x: DATA.start.x, y: DATA.start.y };
    for (const u of DATA.units) G.units.push(TD.makeUnit(u.type, u.x, u.y, { a: u.a, wp: u.wp || null, role: u.role }));
    for (const q of DATA.props) G.props.push(TD.makeProp(q.kind, q.x, q.y, q.drop));
    for (const s of DATA.structures) G.structures.push(TD.makeStructure(s));
    for (const u of G.units) W.collide(u, u.r, false);
    for (const q of G.props) W.collide(q, q.r, false);
    if (MISSION.id === 4) G.ally = Object.assign(TD.makePlayer(DATA.start.x-65,DATA.start.y+15), { pilot: TD.companion, hp: 8, max: 8, inv: 120, fireCd: 0 });
    if (MISSION.setup) MISSION.setup(G, DATA);
    TD.Nav.build(); W.navDirty = false;
    Cam.minY = 0; Cam.maxY = 1e9; Cam.x = G.player.x - VW / 2; Cam.y = G.player.y - VH / 2; Cam.follow(G.player.x, G.player.y, 1);
  }
  function setState(s) { G.state = s; G.stateT = 0; }

  function respawn() {
    const p = G.player, cp = G.cp;
    G.lives--;
    if (G.lives < 0) { setState('gameover'); A.stopMusic(); return; }
    if(p.onfoot){const fresh=TD.makeFootPlayer(cp.x,cp.y);if(MISSION.respawn)MISSION.respawn(G,p,fresh);Object.assign(p,fresh,{pilot:TD.pilot,inv:150,aim:Math.PI});G.eshots=[];return;}
    const keep = p.weapons.filter((w, i) => i !== p.wi || w.id === 'vulcan');    // Hard Corps: you lose the gun you were holding
    if (!keep.length) keep.push({ id: 'vulcan', lv: 1 });
    Object.assign(p, { x: cp.x, y: cp.y, a: Math.PI, aim: Math.PI, vx: 0, vy: 0, manualAim: 0, hp: p.max, inv: 150, dead: false, recoil: 0, charge: 0, weapons: keep, wi: 0, smoke: Math.max(p.smoke, 2) });
    if (G.boss && G.boss.alive()) { p.x = 400; p.y = 635; G.boss.cooldown = 1.4; G.boss.state = 'recover'; G.boss.t = 0; }
    G.eshots = [];
    if (S.phase === 'ALERT' || S.phase === 'EVASION') { S.phase = 'CAUTION'; S.timer = S.T.CAUTION; }
    for (const u of G.units) if (!u.dead && (u.mode === 'alert' || u.mode === 'search')) { u.mode = 'patrol'; u.aware = 0.2; }
  }

  // ------------------------------------------------------------------ step
  function step() {
    const dt = 1 / TD.HZ;
    I.update(); G.t++; G.stateT += dt;
    if (G.state === 'help') { if (I.tap('back') || I.tap('help') || I.tap('start')) setState(G.helpReturn || 'title'); return; }
    if (I.tap('help') && G.state !== 'load') { G.helpReturn = G.state; setState('help'); return; }
    if (G.state === 'load') {
      ART.warm(WARM);
      if (ART.progress(WARM) >= 1 || G.stateT > 12) setState('title');
      return;
    }
    if (G.state === 'title') {
      if (I.tap('left') || I.tap('up')) { G.sel = (G.sel + TD.MISSIONS.length - 1) % TD.MISSIONS.length; A.play('blip'); }
      if (I.tap('right') || I.tap('down')) { G.sel = (G.sel + 1) % TD.MISSIONS.length; A.play('blip'); }
      if (I.confirm()) {
        start(); setState('brief'); A.play('intro'); A.playMusic('level2');
      }
      if (G.lockedT > 0) G.lockedT -= dt;
      return;
    }
    if (G.state === 'brief') {
      ART.warm(['rzb_hull_' + 0, 'rzb_machinegun', 'rzb_missile_pod', 'rzb_rotor', 'rzb_tread', 'rzb_razor_missile', 'rzb_sonic_bullet', 'rzb_sonic_charge', 'rzb_wreck']);
      Cam.follow(G.player.x, G.player.y - 60, 0.05);
      const step = I.tap('left') ? -1 : I.tap('right') ? 1 : 0;
      if (step) {
        const L = TD.PILOTS, i = (L.indexOf(TD.pilot) + step + L.length) % L.length;
        TD.pilot = G.player.pilot = L[i]; A.play('blip');
        try { localStorage.setItem('bof_td_pilot', TD.pilot); } catch (e) {}
        ART.warm(['pt_' + TD.pilot + '_hull', 'pt_' + TD.pilot + '_turret', 'pt_' + TD.pilot + '_damaged_hull', 'pt_' + TD.pilot + '_wreck', 'pav_' + TD.pilot]);
      }
      if(MISSION.id===4&&(I.tap('up')||I.tap('down'))){TD.companion=TD.COMPANIONS[(TD.COMPANIONS.indexOf(TD.companion)+1)%3];G.ally.pilot=TD.companion;A.play('blip');}
      if (G.stateT > 0.6 && I.confirm()) setState('play');
      return;
    }
    if (G.state === 'gameover') { if (G.stateT > 1.5 && I.confirm()) setState('title'); return; }
    if (G.state === 'clear') { if (G.stateT > 2.5 && I.confirm()) {if(G.sel<TD.MISSIONS.length-1){G.sel++;start();setState('brief');A.playMusic('level2');}else setState('title');} return; }
    if (G.state === 'pause') { if (I.tap('start')) setState('play'); return; }
    if (I.tap('start')) { setState('pause'); return; }

    // ---- play
    G.time += dt;
    if (MISSION.pre) MISSION.pre(G, dt);
    const p = G.player;
    if (!p.dead) TD.playerTick(p, G, dt);
    else {
      p.deadT+=dt;
      if(!p.onfoot){p.a=p.deathStart+Math.min(1,Math.max(0,p.deadT-.15)/1.05)*Math.PI*4;p.aim=p.a;
        if(!p.crashed&&p.deadT>=1.2){p.crashed=true;FX.ring(p.x,p.y,.8);FX.boom(p.x,p.y,160,'gfx_destruction_',6);FX.debris(p.x,p.y,.4);Cam.kick(12);A.play('expB');G.wrecks.push({x:p.x,y:p.y,a:p.a,art:'pt_'+p.pilot+'_wreck',still:true,s:.5,player:true});}
        else if(!p.crashed&&G.t%8===0){FX.boom(p.x,p.y,45,'nex_fireball_',4);FX.smoke(p.x,p.y,.15,.6);}}
      if(p.deadT>1.85)respawn();
    }
    for (const u of G.units) TD.unitTick(u, G, dt);
    if (G.boss) G.boss.tick(dt);
    S.tick(dt, G.units, p);
    TD.shotTick(G);
    TD.pickupTick(G, dt);
    TD.campaignTick(G,dt);
    if (MISSION.tick) MISSION.tick(G, dt);
    for (const s of G.structures) s.flash = Math.max(0, s.flash - dt);
    if (W.navDirty) { TD.Nav.build(); W.navDirty = false; }
    for (const q of G.props) {
      q.flash = Math.max(0, q.flash - dt);
      if (!q.dead && q.crush > 25) { TD.hitProp(G, q, 99); q.crush = 0; }
      if (!q.dead && q.crush) q.crush = Math.max(0, q.crush - 0.2);
    }
    // smoke grenades
    for (const g of G.grenades) {
      g.t += dt;
      if (g.t >= 0.45 && !g.done) {
        g.done = true; W.smokes.push({ x: g.tx, y: g.ty, r: 72, t: 0, life: 7 });
        for (let i = 0; i < 8; i++) FX.smoke(g.tx + M.rnd(-30, 30), g.ty + M.rnd(-30, 30), 0.3, 1.2);
        A.play('expS', 0.5);
      }
    }
    G.grenades = G.grenades.filter(g => !g.done);
    for (const s of W.smokes) s.t += dt;
    W.smokes = W.smokes.filter(s => s.t < s.life);
    // checkpoints
    for (const c of DATA.checkpoints) if (p.y < c[1] && G.cp.y > c[1] && !p.dead) { G.cp = { x: c[0], y: c[1] }; G.say('CHECKPOINT', p); A.play('pick', 0.6); }
    // reinforcements while the alarm is up
    if (S.phase === 'ALERT' && !G.boss && (G.reinfT -= dt) <= 0 && (!MISSION.canReinforce || MISSION.canReinforce(G))) {
      G.reinfT = 9;
      const live = G.units.filter(u => u.reinf && !u.dead).length;
      if (live < 3) {
        const gate = DATA.gates.map(g => ({ g, d: Math.abs(g[1] - p.y) })).filter(o => o.g[1] < Cam.y - 40 || o.g[1] > Cam.y + VH + 40).sort((a, b) => a.d - b.d)[0];
        if (gate) { const u = TD.makeUnit(p.onfoot?'robotScout':'scout', gate.g[0], gate.g[1], { a: 0, reinf: true }); u.mode = 'alert'; u.aware = 1; u.goal = { x: p.x, y: p.y }; G.units.push(u); G.say('REINFORCEMENTS', p); }
      }
    }
    // the boss
    if (!G.boss && p.y < DATA.bossLine && !p.dead) {
      G.boss = MISSION.boss(G, DATA.boss.x, DATA.boss.y); Cam.maxY = MISSION.id===3||MISSION.pushScroll?MAP.h:795; A.stopMusic(); A.play('warn');
      G.say('WARNING - '+G.boss.name, { x: 400, y: DATA.bossLine-70 }); G.ghost = S.alerts === 0;
    }
    if (G.boss) { p.y = Math.min(p.y, DATA.bossLine + 10); }
    if (G.bossDeadT != null && (G.bossDeadT += dt) > 3) { setState('clear'); A.playMusic('clear'); finishScore(); }
    FX.update(dt);
    for (const m of G.msgs) m.t += dt; G.msgs = G.msgs.filter(m => m.t < 1.6);
    const [fx, fy] = M.fwd(p.aim);
    const arena=G.boss&&MISSION.mode==='tank',extent=MISSION.id===2?190:110;
    const span = arena ? Math.max(420, Math.max(p.y + 50, G.boss.y + 100) - Math.min(p.y - 40, G.boss.y - extent)) : 360;
    Cam.zoom = M.lerp(Cam.zoom, arena ? M.clamp((VH - 100) / span, 0.44, 0.68) : 1, 0.08);
    if (arena && !G.boss.wrecked) {
      const top = Math.min(p.y - 40, G.boss.y - extent), bottom = Math.max(p.y + 50, G.boss.y + 100);
      Cam.follow((p.x + G.boss.x) / 2, (top + bottom) / 2 - 10 / Cam.zoom, 0.12);
    } else Cam.follow(p.x + fx * 24 + p.vx * 12, p.y + fy * 24 + p.vy * 12, 0.12);
    if (MISSION.cam) MISSION.cam(G);
    Cam.shake *= 0.86;
  }
  function finishScore() {
    const R = G.results = { time: G.time, kills: G.kills, alerts: S.alerts, deaths: G.deaths, ghost: G.ghost };
    R.timeBonus = Math.max(0, Math.round((600 - G.time) * 40));
    R.ghostBonus = G.ghost ? 25000 : 0;
    R.noDeath = G.deaths === 0 ? 10000 : 0;
    G.score += R.timeBonus + R.ghostBonus + R.noDeath;
    if (MISSION.score) MISSION.score(G, R);
    R.rank = G.deaths >= 5 ? 'l' : G.score >= 90000 ? 's' : G.score >= 70000 ? 'a' : G.score >= 52000 ? 'b' : G.score >= 38000 ? 'c' : 'd';
  }

  // ------------------------------------------------------------------ draw
  function text(s, x, y, size, col, align, outline) {
    ctx.font = 'bold ' + size + 'px BOFCommand, "Arial Black", monospace'; ctx.textAlign = align || 'left'; ctx.textBaseline = 'middle';
    ctx.lineWidth = Math.max(2, size / 5); ctx.strokeStyle = outline || '#000'; ctx.strokeText(s, x, y);
    ctx.fillStyle = col || '#fff'; ctx.fillText(s, x, y);
  }
  function drawWorld() {
    const shx = Cam.shake > 0.3 ? M.rnd(-Cam.shake, Cam.shake) : 0, shy = Cam.shake > 0.3 ? M.rnd(-Cam.shake, Cam.shake) : 0;
    ctx.save(); ctx.scale(Cam.zoom, Cam.zoom); ctx.translate(-Math.round(Cam.x + shx), -Math.round(Cam.y + shy));
    ctx.fillStyle = '#0b100c'; ctx.fillRect(Cam.x - 20, Cam.y - 20, VW / Cam.zoom + 40, VH / Cam.zoom + 40);
    const pl = ART.get(MAP.key);
    if (pl) { const sy = M.clamp(Math.floor(Cam.y) - 20, 0, MAP.h), sh = Math.min(VH / Cam.zoom + 40, MAP.h - sy); ctx.drawImage(pl.im, pl.sx, pl.sy + sy, pl.sw, sh, 0, sy, pl.sw, sh); }
    for (const w of G.wrecks) {
      if (w.fragment) ART.draw(ctx, w.art, w.x, w.y, { a: w.a, s: w.s, ax: w.ax, ay: w.ay });
      else if (w.still) ART.draw(ctx, w.art, w.x, w.y, { a: w.a + Math.PI, s: w.s || 0.42 });
      else ART.draw(ctx, w.art + '_crit_' + ['s', 'w', 'n', 'e'][((Math.round(w.a / (Math.PI / 2)) % 4) + 4) % 4], w.x, w.y, { a: 0, s: 0.5, tint: '#1b1714', alpha: 0.75 });
    }
    // the cones lie on the ground, under everything that stands on it
    for (const u of G.units) if (onScreen(u, 240)) S.drawCone(ctx, u, G.t / 60);
    if (G.boss) G.boss.drawUnder(ctx);
    FX.draw(ctx, 0);
    TD.drawStructures(ctx, G);
    for (const q of G.props) if (onScreen(q, 40)) TD.drawProp(ctx, q);
    if (MISSION.drawFloor) MISSION.drawFloor(ctx, G);
    for (const k of G.pickups) {if(G.player.onfoot)TD.drawFootPickup(ctx,k);else TD.drawPickup(ctx, k, G.t / 60);}
    for (const u of G.units) if (onScreen(u, 60)) TD.drawUnit(ctx, u);
    if (G.boss) G.boss.draw(ctx, G.t / 60);
    const p = G.player;
    if(p&&p.onfoot)TD.drawFoot(ctx,p,{flash:p.inv>0&&Math.floor(p.inv/4)%2?1:0});
    if(p&&p.dead&&!p.onfoot&&!p.crashed)TD.drawPlayerTank(ctx,p,{flash:p.deadT<.15?1:0});
    if (p && !p.dead && !p.onfoot) {
      const blink = p.inv > 0 && Math.floor(p.inv / 4) % 2;
      TD.drawPlayerTank(ctx, p, { flash: blink ? 1 : p.flash > 0 ? p.flash / 0.18 : 0 });
      if (p.charge > 0) { const [fx, fy] = M.fwd(p.aim), key = 'tank_charge_' + Math.min(3, Math.floor(p.charge / 18));
        ART.draw(ctx, key, p.x + fx * (TD.muzzleDist(p) - p.charge / 72 * 3), p.y + fy * (TD.muzzleDist(p) - p.charge / 72 * 3), { s: 0.3, a: G.t * 0.06 }); }
    }
    TD.campaignDraw(ctx,G);
    TD.drawFootCover(ctx,G);
    for (const g of G.grenades) { const q = Math.min(1, g.t / 0.45); ART.draw(ctx, 'ndk_shell_2', M.lerp(g.x, g.tx, q), M.lerp(g.y, g.ty, q) - Math.sin(q * Math.PI) * 30, { a: g.t * 14, s: 0.5 }); }
    for (const s of G.shots) TD.drawShot(ctx, s, false);
    for (const e of G.eshots) TD.drawShot(ctx, e, true);
    FX.draw(ctx, 1);
    for (const s of W.smokes) {
      const grow = Math.min(1, s.t / 0.6), fade = Math.min(1, (s.life - s.t) / 1.2);
      for (let i = 0; i < 6; i++) { const a = i * 1.05 + s.t * 0.15; ART.draw(ctx, 'rzb_dust', s.x + Math.cos(a) * s.r * 0.45 * grow, s.y + Math.sin(a) * s.r * 0.45 * grow, { s: 0.42 * grow, a: a, alpha: 0.8 * fade }); }
    }
    for (const u of G.units) if (onScreen(u, 60)) S.drawMark(ctx, u, G.t / 60);
    if (G.boss) G.boss.drawOver(ctx, G.t / 60);
    if (MISSION.drawOver) MISSION.drawOver(ctx, G);
    for (const m of G.msgs) { const a = 1 - Math.max(0, m.t - 1.1) / 0.5; ctx.globalAlpha = a; text(m.text, m.x, m.y - m.t * 22, 11, '#ffe066', 'center'); ctx.globalAlpha = 1; }
    ctx.restore();
  }
  function onScreen(o, m) { return o.x > Cam.x - m && o.x < Cam.x + VW / Cam.zoom + m && o.y > Cam.y - m && o.y < Cam.y + VH / Cam.zoom + m; }

  function drawHUD() {
    const p = G.player, t = G.t / 60;
    if (MISSION.hud && MISSION.hud(ctx, text, G)) return;
    if(p.onfoot){
      ctx.fillStyle='rgba(0,0,0,.7)';ctx.fillRect(6,6,VW-12,42);
      const w=p.weapons[p.wi],def=TD.FOOT_GUNS[w.id];
      ART.draw(ctx,'of_'+w.id+'_pickup',30,25,{s:.18});
      text(def.name,55,17,10,'#ffd060');text(p.reload>0?'RELOADING':w.ammo+' / '+w.reserve,55,35,11,w.ammo?'#fff':'#ff6440');
      text('LIVES x'+G.lives,260,17,10,'#9fe0ff');text('GRENADES '+p.smoke,260,35,9,'#fff');
      text(p.stance.toUpperCase(),VW-12,17,9,'#7dffa0','right');text('ONE HIT',VW-12,35,8,'#ffad70','right');
      text(G.boss&&G.boss.opened?'BREACH NORTH EXIT':'DISABLE FORTRESS SENTRIES',VW/2,VH-14,10,'#ffd060','center');
      text(S.phase,12,62,9,S.phase==='ALERT'?'#ff6440':'#7dffa0');return;
    }
    // armour
    ctx.fillStyle = 'rgba(0,0,0,0.55)'; ctx.fillRect(6, 6, 132, 44);
    text('ARMOR', 12, 15, 9, '#9fe0ff');
    for (let i = 0; i < p.max; i++) { ctx.fillStyle = i < p.hp ? (p.hp <= 3 ? (Math.floor(t * 6) % 2 ? '#ff4030' : '#ffb030') : '#3fe07a') : '#22302a'; ctx.fillRect(12 + i * 10, 22, 8, 7); }
    text('x' + Math.max(0, G.lives), 12, 40, 10, '#fff'); text('SMOKE ' + p.smoke, 50, 40, 9, '#c8d2c8');
    // weapons
    const w = p.weapons[p.wi];
    ART.draw(ctx, TD.iconFor(w.id, w.lv), 162, 28, { s: 0.42 });
    text(TD.WPN[w.id].name + ' LV' + w.lv, 186, 20, 10, '#ffd060');
    p.weapons.forEach((o, i) => { if (i !== p.wi) ART.draw(ctx, TD.iconFor(o.id, o.lv), 192 + i * 18, 37, { s: 0.18, alpha: 0.7 }); });
    if (p.charge > 0) { ctx.fillStyle = '#000'; ctx.fillRect(186, 44, 62, 5); ctx.fillStyle = p.charge >= 40 ? '#b6ff3a' : '#6c8f30'; ctx.fillRect(187, 45, 60 * p.charge / 72, 3); }
    // phase
    if (G.boss && !G.boss.dead) drawBossBar();
    else if (S.phase !== 'SNEAK') {
      const col = S.phase === 'ALERT' ? '#ff3828' : S.phase === 'EVASION' ? '#ffb020' : '#ffe060';
      if (S.phase !== 'ALERT' || Math.floor(t * 4) % 2) text(S.phase, VW / 2, 16, 14, col, 'center');
      text(S.timer.toFixed(2), VW / 2, 32, 11, col, 'center');
    }
    S.drawRadar(ctx, p, G.units, t, VW - 104, 6, 98);
    text(String(G.score).padStart(7, '0'), VW - 8, VH - 12, 12, '#fff', 'right');
    if (p.hidden && !p.dead) text('HIDDEN', 12, VH - 12, 10, '#7dffa0');
    if(G.ally){ART.draw(ctx,'pav_'+G.ally.pilot,25,VH-45,{s:.16});text(G.ally.pilot.toUpperCase(),52,VH-52,8,'#7deacc');text(G.ally.dead?'REGROUPING':G.ally.hp+' / '+G.ally.max,52,VH-37,8,'#fff');}
  }
  function drawBossBar() {
    const B = G.boss, w = 280, h = w * 33 / 700, sc = w / 700, x = VW / 2 - w / 2 - 30, y = VH - h - 8;   // bottom: the top row belongs to armour, weapon and radar
    ART.draw(ctx, 'bmbar_frame_boss', x, y, { ax: 0, ay: 0, s: sc });
    const f = B.state === 'enter' ? B.gauge : B.hpFrac(), fill = ART.get('bmbar_fill_red');
    if (fill) ctx.drawImage(fill.im, fill.sx, fill.sy, fill.sw * f, fill.sh, x + 61 * sc, y + 10 * sc, 578 * sc * f, 13 * sc);
    text(B.name || 'THE WARRIOR', x + w / 2, y - 7, 9, '#ffcc66', 'center');
  }
  function drawTitle() {
    const t = G.t / 60;
    ctx.fillStyle = '#05080a'; ctx.fillRect(0, 0, VW, VH);
    const pl = ART.get(MAP.key);
    if (pl) { const sy = (t * 20) % (MAP.h - VH * 2); ctx.globalAlpha = 0.45; ctx.drawImage(pl.im, pl.sx + 100, pl.sy + MAP.h - VH * 2 - sy, 600, VH * 1.25, -60, 0, VW + 120, VH * 1.5); ctx.globalAlpha = 1; }
    ART.draw(ctx, 'logo', VW / 2, 60, { s: 0.15 });
    ART.draw(ctx, 'overdrive', VW / 2, 112, { s: 0.09 });
    text('GROUND OPERATIONS', VW / 2, 146, 13, '#ffd060', 'center');
    const cards = [['LEVEL 2', TITLE, 'FURY TANK', 'tank'], ['LEVEL 3', 'BOOTS ON THE GROUND', 'RUN AND GUN', 'foot'], ['LEVEL 4', 'MACHINISTS', 'REBEL TANK SQUAD', 'squad'], ['LEVEL 5', 'MUSEUM OF VIOLENCE', 'MERCS X STEALTH', 'museum']];
    const pitch = VW / cards.length, half = Math.min(72, pitch / 2 - 6);
    cards.forEach((c, i) => {
      const cx = pitch / 2 + i * pitch, cy = 236, on = G.sel === i;
      ctx.fillStyle = on ? 'rgba(40,60,30,0.85)' : 'rgba(10,14,12,0.8)'; ctx.fillRect(cx-half,cy-66,half*2,132);
      ctx.strokeStyle = on ? (Math.floor(t*4)%2?'#ffe060':'#ff9a30'):'#3a463c';ctx.lineWidth=2;ctx.strokeRect(cx-half,cy-66,half*2,132);
      text(c[0],cx,cy-54,11,'#9fe0ff','center');text(c[1],cx,cy-40,8,'#fff','center');
      if(c[3]==='tank')TD.drawPlayerTank(ctx,{pilot:TD.pilot,x:cx,y:cy+4,a:Math.PI,hp:1,max:1});
      if(c[3]==='museum'){ART.draw(ctx,'mx_statue',cx,cy+6,{s:.42});TD.drawFoot(ctx,{pilot:TD.pilot,x:cx+18,y:cy+16,a:Math.PI,aim:Math.PI,moving:false,footTime:t,weapons:[{id:'minigun'}],wi:0,stance:'stand'});}
      if(c[3]==='foot')TD.drawFoot(ctx,{pilot:TD.pilot,x:cx,y:cy+4,a:Math.PI,aim:Math.PI,moving:true,footTime:t,weapons:[{id:'desert_eagle'}],wi:0,stance:'stand'});
      if(c[3]==='squad')TD.drawModTank(ctx,{x:cx,y:cy+10,a:Math.PI,look:Math.PI,hp:100,max:100},'wren',.55);
      text(c[2],cx,cy+54,8,'#ffd060','center');
    });
    if (G.lockedT > 0) text('LEVEL 3 IS BEING BUILT NEXT', VW / 2, 318, 10, '#ff8060', 'center');
    if (Math.floor(t * 2) % 2) ART.draw(ctx, 'pad_start', VW / 2, 333, { s: 0.16 });
    text('F1: HELP / CONTROLS', VW / 2, 352, 8, '#9aa89a', 'center');
  }
  function drawBrief() {
    drawWorld();
    ctx.fillStyle = 'rgba(0,0,0,0.62)'; ctx.fillRect(0, 0, VW, VH);
    text(DATA.title, VW / 2, 34, 12, '#9fe0ff', 'center'); text(DATA.name, VW / 2, 56, 20, '#ffd060', 'center');
    // pilot and tank: LEFT / RIGHT
    const pk = G.player.pilot, fam = TD.familyOf(pk), t = G.t / 60;
    ART.draw(ctx, 'pav_' + pk, VW / 2 - 70, 104, { s: 0.25 });
    if(G.player.onfoot)TD.drawFoot(ctx,Object.assign({},G.player,{x:VW/2+60,y:108,moving:true,footTime:t}));
    else TD.drawPlayerTank(ctx, { pilot: pk, x: VW / 2 + 60, y: 108, a: Math.PI + Math.sin(t * 1.4) * 0.35, hp: 1, max: 1 });
    text(pk.toUpperCase(), VW / 2 + 60, 146, 11, '#fff', 'center');
    text(G.player.onfoot?'INFANTRY':fam.toUpperCase()+' TANK',VW/2+60,159,8,'#ffd060','center');
    if (Math.floor(t * 3) % 2) { text('<', VW / 2 - 118, 104, 14, '#ffd060', 'center'); text('>', VW / 2 + 128, 104, 14, '#ffd060', 'center'); }
    ART.draw(ctx, 'pad_dpad', VW / 2 - 48, 176, { s: 0.09 }); text('PILOT', VW / 2 + 4, 176, 8, '#9aa89a', 'center');
    if(MISSION.id===4){ART.draw(ctx,'pad_dpad',168,248,{s:.07});text('PARTNER: '+TD.companion.toUpperCase(),VW/2+10,248,10,'#7deacc','center');}
    const typed = Math.floor(G.stateT * 40);
    let n = 0;
    DATA.brief.forEach((line, i) => { const s = line.slice(0, Math.max(0, typed - n)); n += line.length; text(s, VW / 2, 198 + i * 15, 10, '#e8efe8', 'center'); });
    const keys = MISSION.keys ? MISSION.keys : G.player.onfoot?[['a','FIRE'],['b','RELOAD'],['c','PRONE'],['x','ROLL'],['y','GRENADE'],['z','SWAP']]:[['a', 'MAIN GUN'], ['b', 'CANNON'], ['c', 'STRAFE'], ['x', 'CHARGE'], ['y', 'SMOKE'], ['z', 'SWAP']];
    keys.forEach((k, i) => { const x = 44 + (i % 3) * 148, y = 273 + Math.floor(i / 3) * 24; ART.draw(ctx, 'pad_' + k[0], x, y, { s: 0.1 }); text(k[1], x + 13, y, 9, '#c8d2c8'); });
    if (G.stateT > 0.6 && Math.floor(G.t / 30) % 2) ART.draw(ctx, 'pad_start', VW / 2, 338, { s: 0.16 });
  }
  function drawResults() {
    drawWorld();
    ctx.fillStyle = 'rgba(0,0,0,0.7)'; ctx.fillRect(0, 0, VW, VH);
    const R = G.results; if (!R) return;
    text('MISSION COMPLETE', VW / 2, 40, 20, '#ffd060', 'center');
    const rows = [['TIME', Math.floor(R.time / 60) + 'M ' + String(Math.floor(R.time % 60)).padStart(2, '0') + 'S'], ['KILLS', R.kills], ['ALERTS', R.alerts], ['DEATHS', R.deaths],
      ['TIME BONUS', R.timeBonus], ['GHOST BONUS', R.ghost ? R.ghostBonus : 'ALERTED'], ['NO DEATH', R.noDeath], ...(R.extraRows || []), ['SCORE', G.score]];
    const pitch = rows.length > 8 ? 236 / rows.length : 26;
    rows.forEach((r, i) => { if (G.stateT > 0.3 + i * 0.25) { text(r[0], 110, 82 + i * pitch, 12, '#9fe0ff'); text(String(r[1]), 300, 82 + i * pitch, 12, '#fff', 'right'); } });
    if (G.stateT > 2.4) ART.draw(ctx, 'rank_' + R.rank, 390, 180, { s: 0.42 });
    if (G.stateT > 2.5 && Math.floor(G.t / 30) % 2) ART.draw(ctx,'pad_start',VW/2,340,{s:.16});
  }
  function render() {
    ctx.setTransform(SC, 0, 0, SC, 0, 0); ctx.imageSmoothingEnabled = false;
    if (G.state === 'load') {
      ctx.fillStyle = '#000'; ctx.fillRect(0, 0, VW, VH);
      const f = ART.progress(WARM); ctx.fillStyle = '#3fe07a'; ctx.fillRect(VW / 2 - 100, VH / 2, 200 * f, 6); ctx.strokeStyle = '#fff'; ctx.strokeRect(VW / 2 - 100, VH / 2, 200, 6);
      text('LOADING BULLETS OF FURY ART', VW / 2, VH / 2 - 16, 11, '#fff', 'center');
      if (!root.BOFX) text('MANIFEST NOT FOUND - OPEN THROUGH THE BOF FOLDER', VW / 2, VH / 2 + 30, 10, '#ff6040', 'center');
      return;
    }
    if (G.state === 'title') return drawTitle();
    if (G.state === 'help') {
      ctx.fillStyle = '#080c11'; ctx.fillRect(0, 0, VW, VH); text('GROUND CONTROLS', VW / 2, 28, 18, '#ffd060', 'center');
      const rows = MISSION.help ? MISSION.help : G.player&&G.player.onfoot ? ['WASD / LEFT STICK: MOVE', 'MOUSE / RIGHT STICK / Q-E: AIM', 'J / LEFT MOUSE / A: FIRE', 'R / K / B: RELOAD', 'SHIFT / F / C: TOGGLE PRONE', 'SPACE / H / X: ROLL (VULNERABLE)', 'U / Y: THROW GRENADE', 'I / WHEEL / Z: SWAP WEAPON', 'T: WALL TAP NOISE', 'ENTER / START: PAUSE', 'ONE HIT CONSUMES A LIFE.', 'DEFEAT SENTRIES, THEN CROSS NORTH EXIT.'] : ['WASD / LEFT STICK: DRIVE', 'MOUSE / RIGHT STICK: AIM TURRET', 'SHIFT / L / C: HOLD HULL FOR SIDEWAYS STRAFE',
        'LEFT MOUSE / J / A: MAIN GUN', 'K / B: CANNON', 'RIGHT MOUSE / H / SPACE / X: HOLD CHARGE, RELEASE SHOT',
        'Q / E: ROTATE TURRET ON KEYBOARD', 'U / Y: SMOKE', 'I / WHEEL / Z: SWAP WEAPON', 'ENTER / START: PAUSE',
        'BRIEFING LEFT/RIGHT: PILOT; UP/DOWN: PARTNER IN LEVEL 4.', 'RAMS BREAK COVER; MODULE BREAKS CANCEL THEIR ATTACKS.'];
      rows.forEach((s, i) => text(s, VW / 2, 62 + i * 21, i === 5 ? 8 : 9, '#d2e3da', 'center'));
      ART.draw(ctx, 'pad_b', VW / 2 - 30, 334, { s: 0.1 }); text('BACK', VW / 2 + 5, 334, 10, '#fff'); return;
    }
    if (G.state === 'brief') return drawBrief();
    if (G.state === 'clear') return drawResults();
    drawWorld(); drawHUD();
    if (G.state === 'pause') { ctx.fillStyle = 'rgba(0,0,0,0.5)'; ctx.fillRect(0, 0, VW, VH); text('PAUSED', VW / 2, VH / 2, 22, '#fff', 'center'); }
    if (G.state === 'gameover') { ctx.fillStyle = 'rgba(40,0,0,0.6)'; ctx.fillRect(0, 0, VW, VH); text('GAME OVER', VW / 2, VH / 2, 26, '#ff4030', 'center'); }
  }

  // ------------------------------------------------------------------ loop
  let last = performance.now(), acc = 0, frozen = false;
  function frame(now) {
    if (!frozen) {
      acc += Math.min(0.1, (now - last) / 1000); last = now;
      while (acc >= 1 / TD.HZ) { step(); acc -= 1 / TD.HZ; }
      render();
    }
    root.requestAnimationFrame(frame);
  }
  root.requestAnimationFrame(frame);
  root.TDGAME = {
    G, step(n) { for (let i = 0; i < (n || 1); i++) step(); render(); }, freeze(b) { frozen = b !== false; last = performance.now(); },
    start() { start(); setState('play'); }, render,
  };
}(window));
