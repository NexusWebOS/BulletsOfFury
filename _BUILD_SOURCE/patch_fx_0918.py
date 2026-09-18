#!/usr/bin/env python3
"""patch_fx_0918.py - wire the 0918 generated effects (bursts, burning, geysers). Anchors asserted."""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
P = os.path.join(ROOT, 'assets', 'game.js')
s = open(P, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old); assert n == count, 'anchor %d (want %d): %r' % (n, count, old[:90]); s = s.replace(old, new)

# ---- art
rep("""  for(const _v of [100,250,500,1000]) X._src['score_bullet_'+_v]='assets/game/ui/pickups_0917b/score_'+_v+'.png';
""", """  for(const _v of [100,250,500,1000]) X._src['score_bullet_'+_v]='assets/game/ui/pickups_0917b/score_'+_v+'.png';
  /* 0918: the generated effect animations - 8-frame horizontal strips (fx_install_0918.py) */
  for(const _e of ['fire','ice','lightning','prism','toxic','kinetic','water','chrome','dark']) X._src['efx_burst_'+_e]='assets/game/fx_0918/efx_burst_'+_e+'.png';
  X._src['efx_burn']='assets/game/fx_0918/efx_burn.png';
  for(const _g of ['fire','water','lightning']) X._src['efx_geyser_'+_g]='assets/game/fx_0918/efx_geyser_'+_g+'.png';
""")

# ---- the geyser becomes a real column that takes up a section of the screen
rep("""function geyserSpawn(x,y,kind){ geysers.push({x,y,kind:kind||'water',t:0,life:1.1,h:0}); }
function geyserTick(dt){
  if(!geysers.length) return;
  for(const g of geysers){ g.t+=dt; g.h=Math.min(150, g.h+520*dt);
    if(g.t<g.life){ for(const e of enemies){ if(e.dead||e._dyingT!=null) continue;
      if(Math.abs(e.x-g.x)<18 && e.y<g.y && e.y>g.y-g.h){""",
"""/* ⚠ 0918: A GEYSER IS A COLUMN THAT TAKES UP A SECTION OF THE SCREEN (Mike: "flaming laser beam geysers that take
   up sections of the screen"). It was a 150px sprinkle of particles over an 18px-wide damage lane; it now erupts to
   GEYSER_H with the generated column drawn over it (efxDraw), and the lane is the column's own drawn width. */
const GEYSER_H=360, GEYSER_GROW=1150, GEYSER_LIFE=1.5, GEYSER_CAP=4;
function geyserSpawn(x,y,kind){
  if(geysers.length>=GEYSER_CAP) geysers.shift();
  geysers.push({x,y,kind:kind||'water',t:0,life:GEYSER_LIFE,h:0});
  try{ XART.rdy('efx_geyser_'+(kind||'water')); }catch(_g){ }
  if(typeof shake!=='undefined') shake=Math.max(shake,3);
}
function geyserLane(g){
  let w=40;
  try{ const k='efx_geyser_'+g.kind; if(XART.rdy(k)){ const im=XART.get(k), fw=(im.naturalWidth||im.width)/8, fh=(im.naturalHeight||im.height); w=GEYSER_H*(fw/fh); } }catch(_l){ }
  return w*0.34;
}
function geyserTick(dt){
  if(!geysers.length) return;
  for(const g of geysers){ g.t+=dt; g.h=Math.min(GEYSER_H, g.h+GEYSER_GROW*dt);
    if(g.t<g.life){ const lane=geyserLane(g); for(const e of enemies){ if(e.dead||e._dyingT!=null) continue;
      if(Math.abs(e.x-g.x)<lane+(e.w||20)*0.3 && e.y<g.y && e.y>g.y-g.h){""")

# ---- the bursts, and the fire geyser off a high-level fire kill
rep("""  const lv=(run.infusion&&run.infusion.elem===b._inf)?(run.infusion.lv|0):1;
  _infBusy=true;
  try{""",
"""  const lv=(run.infusion&&run.infusion.elem===b._inf)?(run.infusion.lv|0):1;
  _infBusy=true;
  try{
    /* the element's generated BURST where the round lands (0918), throttled per target so a beam's 20 hits a
       second read as a rhythm of bursts rather than a smear */
    if(typeof efxBurst==='function' && efxClock-(e._efxAt==null?-9:e._efxAt)>0.12){ e._efxAt=efxClock;
      efxBurst(b._inf, e.x+rnd(-(e.w||20)*0.2,(e.w||20)*0.2), e.y+rnd(-(e.h||20)*0.2,(e.h||20)*0.2), 30+lv*9); }""")
rep("""    if(b._inf==='fire'){
      e._burn=Math.max(e._burn||0, DK_BURN_TIME*(0.7+0.3*lv));""",
"""    if(b._inf==='fire'){
      e._burn=Math.max(e._burn||0, DK_BURN_TIME*(0.7+0.3*lv));
      /* the FLAMING GEYSER off a high-level fire kill (0918) - more often the higher the forge */
      if(e.hp<=0 && lv>=3 && !e._geyDone && Math.random()<[0,0,0,0.22,0.36,0.52][Math.min(5,lv)]){ e._geyDone=1; geyserSpawn(e.x,e.y,'fire'); }""")
rep("""    } else if(b._inf==='lightning'){
      e._zapFlash=0.2;""",
"""    } else if(b._inf==='lightning'){
      e._zapFlash=0.2;
      if(e.hp<=0 && lv>=3 && !e._geyDone && Math.random()<0.18){ e._geyDone=1; geyserSpawn(e.x,e.y,'lightning'); }""")

# ---- tick, draw, reset
rep("""    if(typeof geyserTick==='function') geyserTick(dt);""",
    """    if(typeof geyserTick==='function') geyserTick(dt);
    if(typeof efxTick==='function') efxTick(dt);   /* 0918 generated effects */""")
rep("""function _drawEffectsInner(){
  try{ updateShockRings(1/60); }catch(_ue){}""",
"""function _drawEffectsInner(){
  try{ updateShockRings(1/60); }catch(_ue){}
  try{ if(typeof efxDraw==='function') efxDraw(); }catch(_ef){}   /* 0918: bursts, burning, geysers */""")
rep("""  if(typeof bombReset==='function') bombReset();   /* a fuse never carries into the next stage (0917c) */""",
    """  if(typeof bombReset==='function') bombReset();   /* a fuse never carries into the next stage (0917c) */
  efxBursts=[]; geysers=[];                         /* nor a burst or a geyser (0918) */""")

NEW = '''
/* ============================================================
   0918 - THE GENERATED EFFECTS (Mike)
   "fire effects in game like burst fire decals for our new upgrades, same with the other elements. We also
    need actual fire effects that animate and we need flaming laser beam geysers that take up sections of
    the screen. These should all be generated effects."
   SpriteCook still -> animate_game_art, 8-frame strips in assets/game/fx_0918 (fx_install_0918.py):
     efx_burst_<elem>   one-shot, where a forged round lands        (infusionOnHit -> efxBurst)
     efx_burn           loop, on every unit that is burning          (e._burn)
     efx_geyser_<kind>  loop, the column a geyser raises             (geysers[])
   All drawn in WORLD space from drawEffects, so they ride the camera with the units they belong to.
   ============================================================ */
const EFX_N=8, EFX_BURST_T=0.42, EFX_BURST_CAP=28;
let efxBursts=[], efxClock=0;
function efxFrame(key,i,x,y,w,h,alpha){
  if(typeof XART==='undefined' || !XART.rdy(key)) return false;
  const im=XART.get(key), fw=(im.naturalWidth||im.width)/EFX_N, fh=(im.naturalHeight||im.height);
  ctx.save(); if(alpha!=null) ctx.globalAlpha*=alpha; ctx.imageSmoothingEnabled=false;
  ctx.drawImage(im,(i%EFX_N)*fw,0,fw,fh,x,y,w,h); ctx.restore(); return true;
}
function efxBurst(elem,x,y,size){
  if(!INFUSIONS[elem]) return null;
  if(efxBursts.length>=EFX_BURST_CAP) efxBursts.shift();
  const b={elem:elem,x:x,y:y,t:0,s:size||48}; efxBursts.push(b);
  try{ XART.rdy('efx_burst_'+elem); }catch(_b){ }
  return b;
}
function efxTick(dt){
  efxClock+=dt;
  for(const b of efxBursts) b.t+=dt;
  efxBursts=efxBursts.filter(function(b){ return b.t<EFX_BURST_T; });
}
function efxDraw(){
  /* burning units: the generated fire, standing on the unit, flickering on its own phase */
  const tt=efxClock;
  for(const e of enemies){
    if(!e || e.dead || !(e._burn>0)) continue;
    const s=Math.max(22,Math.min(58,(e.w||30)*0.8)), f=Math.floor(tt*13+((e.x|0)%7))%EFX_N;
    efxFrame('efx_burn',f,e.x-s/2,e.y-s*0.78,s,s,Math.min(1,e._burn*2.5));
  }
  /* geysers: the column erupts UP out of its vent - the source is revealed from the bottom as it grows */
  for(const g of geysers){
    const k='efx_geyser_'+g.kind; if(!XART.rdy(k)) continue;
    const im=XART.get(k), fw=(im.naturalWidth||im.width)/EFX_N, fh=(im.naturalHeight||im.height);
    const W=GEYSER_H*(fw/fh), frac=Math.max(0.02,Math.min(1,g.h/GEYSER_H)), sh=fh*frac;
    const f=Math.floor(g.t*14)%EFX_N, a=Math.min(1,(g.life+0.2-g.t)/0.35);
    ctx.save(); ctx.globalAlpha*=Math.max(0,a); ctx.imageSmoothingEnabled=false;
    ctx.drawImage(im,f*fw,fh-sh,fw,sh,g.x-W/2,g.y-g.h,W,g.h); ctx.restore();
  }
  /* bursts */
  for(const b of efxBursts){
    const f=Math.min(EFX_N-1,Math.floor(b.t/EFX_BURST_T*EFX_N));
    efxFrame('efx_burst_'+b.elem,f,b.x-b.s/2,b.y-b.s/2,b.s,b.s,1);
  }
}
'''
rep("""
function drawGameOver(dt){""", NEW + "\nfunction drawGameOver(dt){")
open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('patched OK')
