/* Overdrive encounter dossiers: authored turntable art, live combat data,
 * deterministic camera choreography and a combat-free inspection window. */
(function (root) {
  'use strict';
  const TD = root.TD, M = TD.M, I = TD.Input, A = TD.Audio, Cam = TD.Cam;
  const ART_KEYS = root.TD_BOSS_INTRO_ART;
  const ease = t => { t = M.clamp(t, 0, 1); return t * t * (3 - 2 * t); };
  const INTRO = TD.BossIntro = {
    warm: Object.keys(ART_KEYS.assets),
    warning: 'Stings like a butterfly, Tramples you like a giant ass tank that it is!',
    durations: { arrival: 4.2, card: 11.6, slide: .65, restore: 1.1 },
    active(G) { return !!G.bossIntro && !G.bossIntro.done; },
    canContinue(G) { const s = G.bossIntro; return !!s && s.phase === 'card' && s.t >= 3.85 && s.turns >= 1; },
    start(G, profile) {
      const B = G.boss, p = G.player;
      G.bossIntro = { phase: 'arrival', t: 0, elapsed: 0, done: false,
        profile, selected: 0, inspect: false, yaw: 0, turns: 0, idle: 0,
        reveal: 0, filled: 0, history: ['arrival'], fromY: -154,
        cameraStart: { x: Cam.x, y: Cam.y, zoom: Cam.zoom } };
      B.introducing = true; B.state = 'enter'; B.t = 0; B.y = -154;
      B.a = B.upper = 0; B.gauge = 0;
      p.vx = p.vy = 0; p.boosting = p.moving = p.cruising = false;
      p.charge = 0; p.retina = null;
      G.shots = []; G.eshots = []; G.grenades = [];
      G.msgs = [];
      A.stopEffects(); A.stopMusic(); A.play('warn');
      ART.warm(this.warm);
    },
    phase(G, next) {
      const s = G.bossIntro;
      s.phase = next; s.t = 0; s.idle = 0; s.history.push(next);
      if (next === 'card') { A.stopLoops(); A.play('intro', .65); }
      if (next === 'slide') A.play('loadoutLaunch', .5);
      if (next === 'restore') {
        const before = { x: Cam.x, y: Cam.y, zoom: Cam.zoom };
        Cam.zoom = 1; G.boss.followCamera(G.player, 1);
        s.cameraEnd = { x: Cam.x, y: Cam.y, zoom: 1 };
        s.cameraStart = before;
        Object.assign(Cam, before);
      }
    },
    continue(G) {
      const s = G.bossIntro;
      if (s.phase !== 'card') return false;
      // The first full turn and all stats appear before Continue is enabled.
      if (this.canContinue(G)) this.phase(G, 'slide');
      else A.play('blip', .4);
      return true;
    },
    pick(G, index) {
      const s = G.bossIntro;
      s.selected = (index + s.profile.targets.length) % s.profile.targets.length;
      s.inspect = true; s.idle = 0; A.play('lockon', .5);
    },
    update(G, dt) {
      const s = G.bossIntro, B = G.boss;
      s.t += dt; s.elapsed += dt;
      if (s.phase === 'arrival') {
        const progress = M.clamp(s.t / this.durations.arrival, 0, 1);
        const before = B.y;
        B.y = M.lerp(s.fromY, B.homeY, ease(progress));
        B.t = s.t; B.gauge = progress; B.vy = (B.y - before) * 60;
        // Start close to the arriving chassis, pull back and follow it south.
        Cam.zoom = M.lerp(1.65, 1.12, ease(progress));
        const vw = TD.VW / Cam.zoom, vh = TD.VH / Cam.zoom;
        const target = { x: M.clamp(B.x - vw / 2, 0, TD.World.w - vw),
          y: Math.max(0, B.y - 6 - vh / 2) };
        const capture = ease(s.t / .65);
        Cam.x = M.lerp(s.cameraStart.x, target.x, capture);
        Cam.y = M.lerp(s.cameraStart.y, target.y, capture);
        Cam.shake = 0;
        if (progress > .12 && progress < .96 && G.t % 8 === 0) {
          for (const x of [-100, 100]) TD.FX.smoke(B.x + x, B.y - 90, .3, .6);
        }
        A.scene(G, dt);
        if (progress === 1) {
          B.y = B.homeY; B.vy = 0; B.gauge = 1;
          if (ART.progress(this.warm) >= 1) this.phase(G, 'card');
        }
      } else if (s.phase === 'card') {
        s.idle += dt;
        const previousYaw = s.yaw;
        const manual = (I.down('right') ? 1 : 0) - (I.down('left') ? 1 : 0);
        if (manual) { s.yaw += manual * dt * Math.PI; s.idle = 0; }
        else if (!s.inspect) {
          s.yaw += dt * Math.PI * 2 / 3.2;
        }
        s.rotationDistance = (s.rotationDistance || 0) + Math.abs(s.yaw - previousYaw);
        s.turns = Math.floor(s.rotationDistance / (Math.PI * 2));
        if (I.tap('down')) this.pick(G, s.selected + 1);
        if (I.tap('up')) this.pick(G, s.selected - 1);
        if (I.tap('back') || I.tap('B')) { s.inspect = false; s.idle = 0; A.play('blip', .4); }
        if (I.state.click && !I.last.click) {
          const p = I.pointer;
          const n = Math.floor((p.y - 183) / 22);
          if (p.x >= 374 && p.x <= 585 && n >= 0 && n < 4) this.pick(G, n);
          else if (p.x >= 56 && p.x <= 355 && p.y >= 138 && p.y <= 331) {
            s.inspect = !s.inspect; s.idle = 0; A.play('loadoutSelect', .4);
          } else if (p.y > 447 && p.x > 470) this.continue(G);
        }
        s.reveal = ease((s.t - .6) / 1.6);
        const groups = Math.min(4, Math.max(0, Math.floor((s.t - .6) / .35)));
        if (groups > s.filled) { s.filled = groups; A.play(groups === 4 ? 'forgeComplete' : 'blip', .35); }
        if (s.t >= this.durations.card && s.idle > 4 && s.turns >= 1) this.phase(G, 'slide');
      } else if (s.phase === 'slide') {
        if (s.t >= this.durations.slide) this.phase(G, 'restore');
      } else if (s.phase === 'restore') {
        const t = ease(s.t / this.durations.restore);
        for (const key of ['x', 'y', 'zoom']) Cam[key] = M.lerp(s.cameraStart[key], s.cameraEnd[key], t);
        if (t === 1) {
          s.done = true; s.phase = 'combat'; s.history.push('combat');
          Cam.zoom = 1; B.introducing = false; B.introCompleted = true;
          B.state = 'recover'; B.t = 0; B.cooldown = .9; B.vy = 0;
          G.introFireLatch = I.holdCombat(); A.playMusic('warrior'); A.play('alert', .45);
        }
      }
      TD.FX.update(dt);
    },
    draw(ctx, text, G) {
      const s = G.bossIntro;
      if (!this.active(G)) return;
      s.textLayouts=[];
      const fit=(value,box,size,col)=>{const layout=TD.Text.fit(ctx,text,value,box,size,col);s.textLayouts.push(layout);return layout;};
      if (s.phase === 'arrival') {
        ctx.fillStyle = 'rgba(0,0,0,.75)'; ctx.fillRect(0, 0, TD.VW, 30);
        fit('OVERDRIVE / INCOMING HEAVY ARMOR',[8,4,TD.VW-16,22],11,'#ffc15c');
        const w = 220; ctx.fillStyle = '#152b37'; ctx.fillRect(TD.VW / 2 - w / 2, TD.VH - 23, w, 5);
        ctx.fillStyle = '#ff8b30'; ctx.fillRect(TD.VW / 2 - w / 2, TD.VH - 23, w * G.boss.gauge, 5);
        fit(G.boss.gauge === 1 ? 'DECODING THREAT FILE' : 'THE WARRIOR / APPROACHING',[100,TD.VH-44,TD.VW-200,16],9,'#a8eeff');
        return;
      }
      if (s.phase === 'restore') return;
      ctx.fillStyle = 'rgba(0,4,10,.78)'; ctx.fillRect(0, 0, TD.VW, TD.VH);
      const slide = s.phase === 'slide' ? -700 * ease(s.t / this.durations.slide) : 700 * (1 - ease(s.t / this.durations.slide));
      ctx.save(); ctx.translate(slide, 0);
      ART.draw(ctx, s.profile.cardKey || 'od_warrior_card', 320, 240, { s: .5 });
      const F = TD.Frontend, oldCtx = F.ctx, oldText = F.text;
      F.ctx = ctx; F.text = text;
      s.textLayouts.push(F.fitTx(s.profile.name,[146,74,348,26],22,'#ffcf66'));
      F.ctx = oldCtx; F.text = oldText;
      fit('OVERDRIVE / ENEMY DOSSIER',[146,57,348,16],8,'#a8edff');
      fit(s.profile.classLabel || 'CLASS: SUPERHEAVY',[146,101,348,16],7,'#d4dce2');
      const p = s.profile, target = p.targets[s.selected];
      fit('HP '+p.total,[374,138,208,18],11,'#ffe090');
      fit('HULL GUARD '+p.armor+'% / HELMET ACTIVE',[374,155,208,14],7,'#9beaff');
      fit('TARGETABLE PARTS',[374,169,208,14],8,'#e7f4ff');
      p.targets.forEach((part, i) => {
        const y = 193 + i * 22, fill = ease((s.t - .75 - i * .3) / .65);
        if (i === s.selected) {
          ctx.fillStyle = 'rgba(255,154,46,.16)'; ctx.fillRect(374, y - 10, 208, 20);
          ctx.strokeStyle = '#ffb84a'; ctx.strokeRect(374, y - 10, 208, 20);
        }
        fit(part.name+' / '+Math.round(part.hp*fill)+' HP',[379,y-9,196,16],8,i===s.selected?'#ffe07a':'#b4e9fa');
        ctx.fillStyle = '#153846'; ctx.fillRect(379, y + 6, 196, 2);
        ctx.fillStyle = i === s.selected ? '#ffad35' : '#39bdd5'; ctx.fillRect(379, y + 6, 196 * fill, 2);
      });
      fit('ATTACK PROFILE',[374,270,208,16],8,'#ffbf63');
      p.attacks.forEach((name,i)=>fit(name,[378,286+i*11,200,11],7,'#eef4ff'));
      // The showcase is sixteen authored yaw views, including side and rear.
      const angle = ((s.yaw % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
      const views = p.views || ART_KEYS.turntable;
      const frame = Math.round(angle / (Math.PI * 2) * views.length) % views.length;
      s.frame = frame;
      ctx.save(); ctx.beginPath(); ctx.rect(56, 137, 301, 194); ctx.clip();
      ART.draw(ctx, views[frame], 206, 318, { s: .43, ax: 256, ay: 454 });
      fit('360 VIEW / '+String(Math.round(angle*180/Math.PI)).padStart(3,'0')+' DEG',[61,139,291,18],8,'#89efff');
      if (s.inspect) {
        // Project dossier annotation points around the grounded vertical axis.
        // This is a UI callout; combat still uses the authored module mounts.
        if (target.marker) {
          const [side,height,depth] = target.marker;
          const mx = 206 + (side * Math.cos(angle) - depth * Math.sin(angle)) * .43;
          const my = 318 + (-height + .35 * (side * Math.sin(angle) + depth * Math.cos(angle))) * .43;
          const retinaKey=ART.has('nbret_'+TD.pilot)?'nbret_'+TD.pilot:'retmb_0',g=ART.get(retinaKey);
          if(g)ART.draw(ctx,retinaKey,mx,my,{s:30/g.sw,alpha:.9,palette:retinaKey==='retmb_0'?TD.Retina.colors[TD.pilot]:null});
          ctx.strokeStyle = '#ffe37b'; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(mx + 8, my); ctx.lineTo(347, my); ctx.stroke();
        }
        ctx.fillStyle = 'rgba(3,10,17,.9)'; ctx.fillRect(61, 294, 291, 34);
        fit(target.name+' / '+target.hp+' HP',[63,296,287,15],9,'#ffc66b');
        fit(target.detail,[63,311,287,15],7,'#c4edff');
      } else fit('ROTATING ARMOR SCAN',[61,315,291,14],7,'#c4edff');
      ctx.restore();
      fit('WARNING -',[72,361,496,20],11,'#ffbc54');
      const lines = p.warningLines || ['"Stings like a butterfly,', 'Tramples you like a giant ass tank that it is!"'];
      lines.forEach((line,i)=>fit(line,[72,379+i*15,496,15],9,'#fff1dc'));
      const ready=this.canContinue(G),hints=[['pad_dpad','ROTATE / PARTS'],['pad_a',ready?'CONTINUE':'SCANNING'],['pad_b','OVERVIEW'],['pad_start',ready?'CONTINUE':'SCANNING']];
      ctx.fillStyle='rgba(3,10,17,.9)';ctx.fillRect(55,421,530,22);
      for(let i=0;i<hints.length;i++){const [key,label]=hints[i],x=55+i*132.5;ART.draw(ctx,key,x+13,432,{s:.08});fit(label,[x+28,423,102,18],7,'#d5edff');}
      ctx.restore();
    },
  };
})(window);
