#!/usr/bin/env python3
"""patch_fx_0918b.py - Mike's 0918b effects pass. Anchors asserted.

  "this fire geyser is awesome, we can use these on stage 2 like geysers that animate and erupt on the sides
   of the mountains and launch fire debris up in the air, then come flying down and can damage us. Another
   thing, remove the geyser bottom effect and just use the fire animation, you can use that flipped for the
   stage boss's flamethrower and other cool effects like scaling it up 200% to be like a screen fill 1/4th
   section imagining the screen has 4 horizontal zones ... Same with the other effects too."

  1. STAGE-2 MOUNTAIN VENTS - hostile fire geysers at the screen's sides, a warning first, then fire debris.
  2. THE FURNACE TYRANT'S FLAMETHROWER is the fire geyser flipped (narrow end at the muzzle).
  3. ZONE COLUMNS - the screen as four horizontal zones; a geyser scaled up to fill one. The Furnace pours a
     fire column DOWN into the player's zone (hostile); a level IV+ fire / water / lightning kill raises that
     element's column UP through the zone it died in (friendly).
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
P = os.path.join(ROOT, 'assets', 'game.js')
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old); assert n == count, 'anchor %d (want %d): %r' % (n, count, old[:90]); s = s.replace(old, new)

# ---- art
rep("""  for(const _g of ['fire','water','lightning']) X._src['efx_geyser_'+_g]='assets/game/fx_0918/efx_geyser_'+_g+'.png';
""", """  for(const _g of ['fire','water','lightning']) X._src['efx_geyser_'+_g]='assets/game/fx_0918/efx_geyser_'+_g+'.png';
  X._src['efx_debris_0']='assets/game/fx_0918/efx_debris_0.png'; X._src['efx_debris_1']='assets/game/fx_0918/efx_debris_1.png';
""")

# ---- geyserSpawn returns the column; a HOSTILE column burns the player instead of enemies
rep("""  geysers.push({x,y,kind:kind||'water',t:0,life:GEYSER_LIFE,h:0});
  try{ XART.rdy('efx_geyser_'+(kind||'water')); }catch(_g){ }
  if(typeof shake!=='undefined') shake=Math.max(shake,3);
}""", """  const g={x,y,kind:kind||'water',t:0,life:GEYSER_LIFE,h:0}; geysers.push(g);
  try{ XART.rdy('efx_geyser_'+(kind||'water')); }catch(_g){ }
  if(typeof shake!=='undefined') shake=Math.max(shake,3);
  return g;
}""")
rep("""    if(g.t<g.life){ const lane=geyserLane(g); for(const e of enemies){ if(e.dead||e._dyingT!=null) continue;""",
"""    if(g.t<g.life){ const lane=geyserLane(g);
      /* 0918b: a stage-2 mountain vent is HOSTILE - its column burns the player, never the enemies */
      if(g.hostile){ if(!player.dead && typeof playerHit==='function' && Math.abs(player.x-g.x)<lane*0.75 && player.y<g.y && player.y>g.y-g.h) playerHit(); }
      else for(const e of enemies){ if(e.dead||e._dyingT!=null) continue;""")

# ---- the friendly zone column off a level IV+ elemental kill
rep("""      efxBurst(b._inf, e.x+rnd(-(e.w||20)*0.2,(e.w||20)*0.2), e.y+rnd(-(e.h||20)*0.2,(e.h||20)*0.2), 30+lv*9); }""",
"""      efxBurst(b._inf, e.x+rnd(-(e.w||20)*0.2,(e.w||20)*0.2), e.y+rnd(-(e.h||20)*0.2,(e.h||20)*0.2), 30+lv*9); }
    /* 0918b: a level IV+ fire / water / lightning KILL may raise that element's ZONE COLUMN - the geyser scaled
       to fill a quarter of the screen - up through the zone the target died in. One at a time, 4 s apart. */
    if(e.hp<=0 && lv>=4 && (b._inf==='fire'||b._inf==='water'||b._inf==='lightning') && typeof zoneColumnSpawn==='function'
       && efxClock-zoneFriendlyAt>ZONE_FRIENDLY_GAP && !zoneCols.some(function(c){ return !c.hostile; }) && Math.random()<(lv>=5?0.16:0.10)){
      zoneFriendlyAt=efxClock; zoneColumnSpawn(zoneOf(e.x),b._inf,false); }""")

# ---- ticks and reset
rep("""    if(typeof efxTick==='function') efxTick(dt);   /* 0918 generated effects */""",
"""    if(typeof efxTick==='function') efxTick(dt);   /* 0918 generated effects */
    if(typeof s2VentTick==='function') s2VentTick(dt);   /* 0918b stage-2 vents + fire debris */
    if(typeof zoneTick==='function') zoneTick(dt);       /* 0918b quarter-screen zone columns */""")
rep("""  efxBursts=[]; geysers=[];                         /* nor a burst or a geyser (0918) */""",
"""  efxBursts=[]; geysers=[];                         /* nor a burst or a geyser (0918) */
  s2Vents=[]; fireDebris=[]; zoneCols=[]; s2VentT=S2VENT.first;   /* nor a vent, debris or zone column (0918b) */""")

# ---- the Furnace pours a zone column
rep("""    F.at+=dt; furnaceCombat(b,dt);
  }""", """    F.at+=dt; furnaceCombat(b,dt);
    if(typeof furnaceZoneTick==='function') furnaceZoneTick(b,dt);   /* 0918b */
  }""")

# ---- the flamethrower is the fire geyser, flipped
rep("""  if(q.kind==='flame'){
    const im=fztImg('fzt_flame_jet_'+(Math.floor(n/77)%2));
    if(im){ const w=q.width*2.8*1.25; ctx.drawImage(im,70,0,116,240,-w/2,-8*FZT_S,w,q.len+8*FZT_S); }
  } else {""", """  if(q.kind==='flame'){
    /* 0918b (Mike): the fire geyser, FLIPPED - its narrow base sits in the muzzle and the column flares out
       along the beam. The pack's jet stays as the fallback while the strip decodes. */
    const gk='efx_geyser_fire';
    if(XART.rdy(gk)){ const g=XART.get(gk), fw=(g.naturalWidth||g.width)/EFX_N, fh=(g.naturalHeight||g.height);
      const w=q.width*4.2, L=q.len+10*FZT_S, f=Math.floor(n/70)%EFX_N;
      ctx.scale(1,-1); ctx.drawImage(g,f*fw,0,fw,fh,-w/2,-L+2*FZT_S,w,L); }
    else { const im=fztImg('fzt_flame_jet_'+(Math.floor(n/77)%2));
      if(im){ const w=q.width*2.8*1.25; ctx.drawImage(im,70,0,116,240,-w/2,-8*FZT_S,w,q.len+8*FZT_S); } }
  } else {""")

# ---- draws inside efxDraw
rep("""  /* geysers: the column erupts UP out of its vent - the source is revealed from the bottom as it grows */
  for(const g of geysers){""", """  s2VentDraw();
  /* geysers: the column erupts UP out of its vent - the source is revealed from the bottom as it grows */
  for(const g of geysers){""")
rep("""  /* bursts */
  for(const b of efxBursts){
    const f=Math.min(EFX_N-1,Math.floor(b.t/EFX_BURST_T*EFX_N));
    efxFrame('efx_burst_'+b.elem,f,b.x-b.s/2,b.y-b.s/2,b.s,b.s,1);
  }
}""", """  zoneDraw();
  debrisDraw();
  /* bursts */
  for(const b of efxBursts){
    const f=Math.min(EFX_N-1,Math.floor(b.t/EFX_BURST_T*EFX_N));
    efxFrame('efx_burst_'+b.elem,f,b.x-b.s/2,b.y-b.s/2,b.s,b.s,1);
  }
}""")

NEW = r'''
/* ============================================================
   0918b - STAGE-2 MOUNTAIN VENTS, FIRE DEBRIS, ZONE COLUMNS (Mike)
   ============================================================ */
/* The vents: on stage 2 a fire geyser erupts on the SIDE of the screen every few seconds (the mountainsides),
   0.95 s of warning first - the vent glows and the generated fire starts in it - then a HOSTILE column and
   five chunks of burning rock thrown up out of it, which arc over and come down on the field. The column and
   every chunk hurt the player (playerHit, so a roll's or a respawn's i-frames still protect). Off while a
   boss is up - the Furnace has its own zone column. */
const S2VENT={warn:0.95, gap:[6.2,10.4], first:4.5, debris:5};
let s2Vents=[], s2VentT=4.5, fireDebris=[];
function s2VentDiff(){ const k=(typeof diffKey!=='undefined')?diffKey:'normal'; return k==='easy'?1.4:(k==='hard'||k==='furious'||k==='insanity')?0.8:1; }
function s2VentTick(dt){
  debrisTick(dt);
  for(const v of s2Vents){ v.t+=dt;
    if(!v.done && v.t>=S2VENT.warn){ v.done=true;
      const g=geyserSpawn(v.x,v.y,'fire'); if(g) g.hostile=true;
      for(let i=0;i<S2VENT.debris;i++) debrisLaunch(v.x+rnd(-12,12), v.y-rnd(4,24), -v.side, i*0.07+rnd(0,0.05));
      try{ if(Audio.SFX.furnaceFlameRelease) Audio.SFX.furnaceFlameRelease(); }catch(_s){ }
      if(typeof shake!=='undefined') shake=Math.max(shake,6); } }
  s2Vents=s2Vents.filter(function(v){ return v.t<S2VENT.warn+0.05; });
  const on=run && run.stage===2 && !(typeof bossActive!=='undefined'&&bossActive) && player && !player.dead
           && !(typeof spaceWeaponsActive==='function'&&spaceWeaponsActive());
  if(!on) return;
  s2VentT-=dt; if(s2VentT>0) return;
  s2VentT=rnd(S2VENT.gap[0],S2VENT.gap[1])*s2VentDiff();
  s2VentSpawn(chance(0.5)?-1:1);
}
function s2VentSpawn(side,y){
  const L=camLeftX(), R=camRightX();
  const v={side:side, x:side<0?L+rnd(24,64):R-rnd(24,64), y:(y!=null?y:rnd(VH*0.62,VH+4)), t:0, done:false};
  s2Vents.push(v);
  try{ XART.rdy('efx_geyser_fire'); XART.rdy('efx_burn'); XART.rdy('efx_debris_0'); XART.rdy('efx_debris_1'); }catch(_r){ }
  try{ if(Audio.SFX.furnaceFlameIgnite) Audio.SFX.furnaceFlameIgnite(); }catch(_s){ }
  return v;
}
function s2VentDraw(){
  for(const v of s2Vents){ if(v.done) continue;
    const k=clamp(v.t/S2VENT.warn,0,1), pulse=0.5+0.5*Math.sin(v.t*30);
    ctx.save(); ctx.globalCompositeOperation='lighter';
    const r=14+22*k, gr=ctx.createRadialGradient(v.x,v.y,1,v.x,v.y,r);
    gr.addColorStop(0,'rgba(255,220,120,'+(0.55+0.35*pulse)+')'); gr.addColorStop(0.5,'rgba(255,90,20,'+(0.35+0.2*pulse)+')'); gr.addColorStop(1,'rgba(255,40,0,0)');
    ctx.fillStyle=gr; ctx.beginPath(); ctx.ellipse(v.x,v.y,r,r*0.55,0,0,Math.PI*2); ctx.fill(); ctx.restore();
    const s=12+40*k; efxFrame('efx_burn',Math.floor(v.t*14)%EFX_N,v.x-s/2,v.y-s*0.85,s,s,0.6+0.4*k);
    if(chance(0.6)) particles.push({x:v.x+rnd(-8,8),y:v.y-rnd(0,6),vx:rnd(-0.4,0.4),vy:rnd(-2.6,-1),life:rnd(0.25,0.5),t:0,r:rnd(1.2,2.4),color:chance(0.4)?'#ffd27a':'#ff6a1e'});
  }
}
/* fire debris: its own list, because enemy rounds have no gravity. Per-frame units like every other round. */
const DEBRIS_G=0.25, DEBRIS_CAP=24;
function debrisLaunch(x,y,dir,delay){
  if(fireDebris.length>=DEBRIS_CAP) fireDebris.shift();
  const d={x:x,y:y,vx:dir*rnd(0.5,2.9),vy:-rnd(8.6,12.2),rot:0,spin:rnd(-0.2,0.2),v:chance(0.5)?1:0,s:rnd(20,30),r:9,delay:delay||0,t:0,dead:false};
  fireDebris.push(d); return d;
}
function debrisTick(dt){
  if(!fireDebris.length) return;
  const k=dt*60;
  for(const d of fireDebris){ if(d.dead) continue;
    if(d.delay>0){ d.delay-=dt; continue; }
    d.t+=dt; d.vy+=DEBRIS_G*k; d.x+=d.vx*k; d.y+=d.vy*k; d.rot+=d.spin*k;
    if(chance(0.7)) particles.push({x:d.x+rnd(-3,3),y:d.y+rnd(-3,3),vx:rnd(-0.3,0.3),vy:rnd(-0.6,0.2),life:rnd(0.18,0.34),t:0,r:rnd(1.2,2.6),color:chance(0.5)?'#ff7a1e':'#ffd070'});
    if(!player.dead && typeof playerHit==='function' && Math.hypot(player.x-d.x,player.y-d.y)<d.r+8){
      playerHit(); d.dead=true; if(typeof explode==='function') explode(d.x,d.y,14,'orange'); }
    if(d.y>VH+60) d.dead=true;
  }
  fireDebris=fireDebris.filter(function(d){ return !d.dead; });
}
function debrisDraw(){
  for(const d of fireDebris){ if(d.dead||d.delay>0) continue;
    const key='efx_debris_'+d.v;
    if(!XART.rdy(key)){ ctx.save(); ctx.fillStyle='#ff6a1e'; ctx.beginPath(); ctx.arc(d.x,d.y,5,0,Math.PI*2); ctx.fill(); ctx.restore(); continue; }
    const im=XART.get(key);
    ctx.save(); ctx.translate(d.x,d.y); ctx.rotate(Math.atan2(d.vy,d.vx)-Math.PI*0.75); ctx.imageSmoothingEnabled=false;
    ctx.drawImage(im,-d.s/2,-d.s/2,d.s,d.s); ctx.restore();
  }
}

/* ZONE COLUMNS: the screen as four horizontal zones (Mike: "imagining the screen has 4 horizontal zones"),
   and a geyser scaled up to fill one of them, top to bottom. The zones are the CAMERA's quarters, measured at
   the moment the column is called, and the column stays at that world x. A hostile column warns for ZONE_WARN
   (the zone lit and its edges flashing), then POURS DOWN from the top; a friendly one rises from the bottom
   after a short beat. */
const ZONE_N=4, ZONE_WARN=1.05, ZONE_LIFE=1.15, ZONE_GROW=0.24, ZONE_FRIENDLY_GAP=4;
const ZONE_COL={fire:'#ff5a1e', water:'#5fd0ff', lightning:'#ffe23a'};
let zoneCols=[], zoneFriendlyAt=-9;
function zoneBounds(i){ const L=camLeftX(), R=camRightX(), w=(R-L)/ZONE_N; return {x0:L+i*w, w:w}; }
function zoneOf(x){ const L=camLeftX(), R=camRightX(); return clamp(Math.floor((x-L)/((R-L)/ZONE_N)),0,ZONE_N-1); }
function zoneColumnSpawn(i,kind,hostile){
  const z=zoneBounds(i), c={i:i, x0:z.x0, w:z.w, kind:kind, hostile:!!hostile, t:0, warn:hostile?ZONE_WARN:0.3, life:ZONE_LIFE, boom:false};
  zoneCols.push(c);
  try{ XART.rdy('efx_geyser_'+kind); }catch(_r){ }
  if(hostile){ try{ if(Audio.SFX.alertDanger) Audio.SFX.alertDanger(); else if(Audio.SFX.furnaceFlameIgnite) Audio.SFX.furnaceFlameIgnite(); }catch(_s){ } }
  return c;
}
function zoneReach(c){ return clamp((c.t-c.warn)/ZONE_GROW,0,1)*(VH+20); }
function zoneTick(dt){
  if(!zoneCols.length) return;
  for(const c of zoneCols){ c.t+=dt;
    const live=c.t>=c.warn && c.t<c.warn+c.life; if(!live) continue;
    if(!c.boom){ c.boom=true; if(typeof shake!=='undefined') shake=Math.max(shake,c.hostile?9:6);
      try{ const f=c.kind==='lightning'?Audio.SFX.enemyElectricBolt:Audio.SFX.furnaceFlameRelease; if(f) f(); }catch(_s){ } }
    const reach=zoneReach(c), x1=c.x0+c.w;
    if(c.hostile){
      if(!player.dead && typeof playerHit==='function' && player.x>c.x0+4 && player.x<x1-4 && player.y<reach) playerHit();
    } else {
      for(const e of enemies){ if(!e||e.dead||e._dyingT!=null) continue;
        if(e.x<c.x0||e.x>x1||e.y<VH+20-reach) continue;
        e._zoneT=(e._zoneT||0)-dt; if(e._zoneT>0) continue; e._zoneT=0.18;
        if(c.kind==='fire') e._burn=Math.max(e._burn||0,DK_BURN_TIME*0.7);
        if(c.kind==='water') e._soaked=Math.max(e._soaked||0,2.5);
        hitEnemy(e, c.kind==='lightning'?6:5); }
    }
    if(chance(0.8)) particles.push({x:rnd(c.x0+8,x1-8),y:c.hostile?rnd(0,reach):rnd(VH-reach,VH),vx:rnd(-0.6,0.6),vy:c.hostile?rnd(1,3):rnd(-3,-1),life:rnd(0.2,0.45),t:0,r:rnd(1.5,3),color:chance(0.4)?'#ffffff':ZONE_COL[c.kind]});
  }
  zoneCols=zoneCols.filter(function(c){ return c.t<c.warn+c.life+0.25; });
}
function zoneDraw(){
  for(const c of zoneCols){
    const col=ZONE_COL[c.kind]||'#ffffff', x1=c.x0+c.w;
    if(c.t<c.warn){
      /* the telegraph: the zone lit and its edges flashing, faster as it closes */
      const k=c.t/c.warn, on=Math.floor(c.t*(6+14*k))%2===0;
      ctx.save(); ctx.globalAlpha*=(c.hostile?0.10:0.06)+0.10*k; ctx.fillStyle=col; ctx.fillRect(c.x0,0,c.w,VH+20);
      ctx.globalAlpha=on?0.85:0.35; ctx.fillStyle=col; ctx.fillRect(c.x0,0,2,VH+20); ctx.fillRect(x1-2,0,2,VH+20); ctx.restore();
      continue;
    }
    const k='efx_geyser_'+c.kind; if(!XART.rdy(k)) continue;
    const im=XART.get(k), fw=(im.naturalWidth||im.width)/EFX_N, fh=(im.naturalHeight||im.height);
    const H=VH+40, W=c.w*1.5, cx=c.x0+c.w/2, reach=zoneReach(c), u=c.t-c.warn;
    const a=Math.max(0,Math.min(1,(c.life+0.25-u)/0.35)), f=Math.floor(u*14)%EFX_N;
    ctx.save(); ctx.globalAlpha*=a; ctx.imageSmoothingEnabled=false;
    ctx.beginPath();
    if(c.hostile) ctx.rect(c.x0-W,0,c.w+W*2,reach); else ctx.rect(c.x0-W,VH+20-reach,c.w+W*2,reach);
    ctx.clip();
    if(c.hostile){ ctx.translate(cx,-10); ctx.scale(1,-1); ctx.drawImage(im,f*fw,0,fw,fh,-W/2,-H,W,H); }
    else ctx.drawImage(im,f*fw,0,fw,fh,cx-W/2,VH+20-H,W,H);
    ctx.restore();
  }
}
/* the Furnace Tyrant pours a fire column down the zone the player is in, every 8-11 s once it is fighting */
function furnaceZoneTick(b,dt){
  const F=b._fz; if(!F||b.dead||F.phase==='intro') return;
  if(F.zoneT==null) F.zoneT=6;
  F.zoneT-=dt; if(F.zoneT>0) return;
  if(zoneCols.some(function(c){ return c.hostile; })) return;
  F.zoneT=rnd(8,11)*s2VentDiff();
  zoneColumnSpawn(zoneOf(player.x),'fire',true);
}
'''
rep("""
function drawGameOver(dt){""", NEW + "\nfunction drawGameOver(dt){")
open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('patched OK')
