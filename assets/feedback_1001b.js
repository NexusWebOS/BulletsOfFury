"use strict";
/* ============================================================================================
   1001b - Mike's notes from the trailer v9 redo.
   Loaded after every other gameplay layer (before the widescreen HUD) so each override here is the
   outermost wrapper of the function it changes. Each section names what was wrong, measured in
   real Chromium (_BUILD_SOURCE/scene1001.py), before the change.
   ============================================================================================ */

/* ---------------------------------------------------------------------------------------------
   A. BOMBER SQUADS FLASH WHITE
   "we have new bomber squad units. ensure they flash white when hit."
   Measured: the Stage 6 squadron (s1jetbomber_b carrying _mission29, drawn by the bluejets cells,
   red/green palettes since 1001) DID take e.flash, but the flash was a 74% white flood blitted at
   55-85% alpha over the plate - the paint, outlines and both palettes read straight through it, so in
   play a hit looked like a faint haze. The 116x124 storm bombers (enc30PartFlash) peaked at 70%.
   Now every bomber hit is a SOLID silhouette in the hit colour (white, or the elemental red/blue
   crit), the same read every other enemy gives, fading out with e.flash.
   --------------------------------------------------------------------------------------------- */
function fb1001FlashAlpha(e){return Math.min(1,.78+(e.flash||0)*3);}
s67CellFlash=function(name,frame,x,y,w,h,e){
  const A=MISSION29_ART[name];if(!A||!XART.rdy(A.key))return false;
  const c=xartTint(A.key,hitFlashColor(e,'#ffffff'),1);if(!c)return false;
  const r=A.frames[((frame|0)%A.frames.length+A.frames.length)%A.frames.length];
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=fb1001FlashAlpha(e);ctx.drawImage(c,...r,x,y,w,h);ctx.restore();return true;
};
if(typeof enc30PartFlash==='function'){
  enc30PartFlash=function(e,name,f,x,y,w,h,pal){
    const r=enc30Cell(name,f,x,y,w,h,pal);
    if(r&&e.flash>0){ctx.save();ctx.globalAlpha=fb1001FlashAlpha(e);enc30Cell(name,f,x,y,w,h,hitFlashColor(e));ctx.restore();}
    return r;
  };
}

/* ---------------------------------------------------------------------------------------------
   B. STAGE 6 - THE SPLIT ACTUALLY TURNS
   "if you choose left, make us scroll 340 units to the left, or 340 units to the right if we chose
   right to make it appear like we are really going left or right."
   The world is 680 wide against a 480 view, so the camera itself only has 200px of travel - it
   cannot move 340. The SKY moves instead: after the choice the whole stage-6 backdrop (sky, the city
   rising through it, the clouds) slides 340px toward the far side over 2.6s, as the wing banks onto
   its new heading. The plate is laid out three times across, the outer copies mirrored, so the slide
   never reveals an edge. Combat geometry, enemies and the camera are untouched - this is the view
   of the ground, the same contract the stage-6 sky clock already keeps.
   --------------------------------------------------------------------------------------------- */
const S6_TURN_PX=340,S6_TURN_T=2.6;
function s6TurnOffset(){
  if(run.stage!==6||typeof s6Wing==='undefined'||!s6Wing||!s6Wing.route)return 0;
  if(typeof Rival24!=='undefined'&&Rival24.active)return 0;
  const k=clamp((s6Wing.routeFightT||0)/S6_TURN_T,0,1),e=k*k*(3-2*k);
  return (s6Wing.route==='left'?1:-1)*S6_TURN_PX*e;   // flying LEFT carries the ground to the RIGHT
}
const FB1001_BG6_LOOP=bg6LoopDraw;
bg6LoopDraw=function(img,key,scroll,drawW,winH,dstY){
  const off=s6TurnOffset();
  if(!off)return FB1001_BG6_LOOP.apply(this,arguments);
  const W=drawW||worldWidth();let r;
  for(const k of [-1,0,1]){
    ctx.save();ctx.translate(off+k*W,0);
    if(k!==0){ctx.translate(W,0);ctx.scale(-1,1);}
    try{r=FB1001_BG6_LOOP.call(this,img,key,scroll,drawW,winH,dstY);}finally{ctx.restore();}
  }
  return r;
};

/* ---------------------------------------------------------------------------------------------
   C. STAGE X - A WATER PLATEAU WITH A GIANT MOUNTAIN
   "Stage X, should be a water plateau with a giant mountain as the level, not what we have now. use
   spritecook to generate our new stage. its a boss arena or dogfight arena stage really."
   The duel borrowed Stage 6's sky (Rival24.arenaStage() -> 6). It now flies over its own SpriteCook
   plate (_BUILD_SOURCE/stagex_1001/, 1536x2752 source, 680x1218 in game): a flooded tableland ringed
   by cliffs with one snow-capped mountain in the middle. An arena, not a corridor - so it does not
   run out: the camera flies in from the plateau's southern cliffs and then circles the mountain,
   drifting slowly up and down the plate so the peak never leaves the fight.
   --------------------------------------------------------------------------------------------- */
// Generated terrain-only coastal city. Native alpha exposes the authored water reel.
XART._src.sx1001_arena='assets/game/levels/stage_x/stage/stagex_coast_1004j/terrain.png';
const SX4J_WATER_KEYS=['nwl_water_0','nwl_water_1','nwl_water_2','nwl_water_3'];
let sx1001T=0;
function stageXArenaReady(){
  const terrain=XART.rdy('sx1001_arena');
  let water=true;
  for(const k of SX4J_WATER_KEYS)if(!XART.rdy(k))water=false;
  return terrain&&water;
}
function stageXArenaWaterDraw(sy,top,h,W){
  const key=SX4J_WATER_KEYS[Math.floor(sx1001T*6)%SX4J_WATER_KEYS.length];
  const fr=XART.get(key),tw=fr.naturalWidth||fr.width,th=fr.naturalHeight||fr.height;
  // The bed moves independently of the terrain camera, in world coordinates.
  const phase=((sy-sx1001T*4)%th+th)%th;
  for(let y=top-phase;y<top+h;y+=th){
    for(let x=0;x<W;x+=tw)ctx.drawImage(fr,x,y,tw,th);
  }
}
function stageXArenaSrcY(img){
  const H=img.naturalHeight||img.height,span=Math.max(0,H-viewH()),mid=span*.46,swing=span*.22;
  const intro=clamp(sx1001T/4.5,0,1),ie=intro*intro*(3-2*intro);
  const orbit=mid+swing*Math.sin(Math.max(0,sx1001T-4.5)*TAU/52);
  return lerp(span,orbit,ie);                   // starts on the southern cliffs, settles onto the peak
}
function stageXArenaDraw(dt){
  if(!stageXArenaReady())return false;
  sx1001T+=Math.max(0,dt||0);
  const img=XART.get('sx1001_arena'),W=worldWidth(),sy=stageXArenaSrcY(img),top=viewTopY(),h=viewH();
  ctx.save();ctx.imageSmoothingEnabled=false;
  stageXArenaWaterDraw(sy,top,h,W);
  ctx.drawImage(img,0,sy,img.naturalWidth||img.width,h,0,top,W,h);
  ctx.restore();
  _masterSrcY=sy-top;
  return true;
}
const FB1001_DRAWBG=drawBG;
function stageXArenaActive(){
  return !!(typeof Rival24!=='undefined'&&Rival24.active)||run.stage===6&&!!run._gp4StageX;
}
drawBG=function(dt){
  if(stageXArenaActive()&&stageXArenaDraw(dt))return;
  return FB1001_DRAWBG.apply(this,arguments);
};
/* the duel's launch (a Stage-6 launch underneath) flies in over the same plate */
const FB1001_S6TRANS=stage6TransitionBackgroundDraw;
stage6TransitionBackgroundDraw=function(scroll){
  if(stageXArenaActive()&&stageXArenaReady()){
    sx1001T=0;ctx.save();if(worldWidth()>VW)ctx.translate(-camX,0);stageXArenaDraw(0);ctx.restore();return;
  }
  return FB1001_S6TRANS.apply(this,arguments);
};
const FB1001_BEGIN=beginStage;
beginStage=function(num){sx1001T=0;const r=FB1001_BEGIN.apply(this,arguments);stageXArenaReady();return r;};

/* ---------------------------------------------------------------------------------------------
   D. STAGE 9 - SMALLER, CLEANER ASTEROIDS, AND WATERY ONES
   "Stage 9, remove the giant asteroids. generate cleaner, smaller ones please. And generate watery
   asteroids as the theme of the level is indeed water in space."
   The giants were spawnS9Meteor: the small purple crystal comet (ns9c_sm) blown up 300-500%, i.e.
   132-220px bodies drawn ~225-375px wide - a third of the screen each, three to a shower. Six new
   SpriteCook plates (_BUILD_SOURCE/s9_asteroids_1001/): three clean grey rocks and three wrapped in
   seawater. Showers keep their corridors, their gravity and their collision bounce; the bodies are
   46-74px now. Watery ones burst through the existing tidal-geyser death (s9WaterBurst) instead of a
   fireball; the rift water-rock units wear the watery plates too.
   --------------------------------------------------------------------------------------------- */
const S9AST_ROCK=['s9ast_rock_0','s9ast_rock_1','s9ast_rock_2'],S9AST_WET=['s9ast_wet_0','s9ast_wet_1','s9ast_wet_2'];
for(const k of [...S9AST_ROCK,...S9AST_WET]){XART._src[k+'_idle']='assets/game/levels/stage_09/enemies/s9_asteroids_1001/'+k+'.png';ENEMY_ART[k]=k;}
function s9AstWarm(){for(const k of [...S9AST_ROCK,...S9AST_WET])XART.rdy(k+'_idle');}
let s9AstSerial=0;
spawnS9Meteor=function(x,y,scale,vx,vy){
  if(typeof spawnEnemy!=='function')return null;
  const n=s9AstSerial++,wet=n%2===1,list=wet?S9AST_WET:S9AST_ROCK,art=list[n%3];
  /* the old 3..5 scale band becomes a 46..74px body */
  const size=Math.round(46+clamp(((scale||3)-3)/2,0,1)*28);
  const e=spawnEnemy('cometsm',x,y,{pattern:'s9meteor',_s9Meteor:true,_route:'meteor'});
  if(!e)return null;
  e._meteorId=++_s9MeteorId;e._meteorScale=size/44;e.art=art;e.w=e.h=size;e._foot=1;
  e.hp=e.maxhp=EHP(6+Math.round(size/9));e._mvx=vx==null?rnd(-28,28):vx;e._mvy=vy==null?rnd(82,126):vy;
  e._mspin=rnd(-.9,.9);e.shoots=false;e.dropOk=false;e.impact=true;
  if(wet){e._waterRock=1;}
  return e;
};
if(typeof S9_UNITS!=='undefined'){
  if(S9_UNITS.riftrocksm)S9_UNITS.riftrocksm.art='s9ast_wet_2',S9_UNITS.riftrocksm.foot=1;
  if(S9_UNITS.riftrock)S9_UNITS.riftrock.art='s9ast_wet_0',S9_UNITS.riftrock.foot=1;
}
const FB1001_BEGIN_S9=beginStage;
beginStage=function(num){const r=FB1001_BEGIN_S9.apply(this,arguments);if(num===9){s9AstSerial=0;s9AstWarm();}return r;};

/* ---------------------------------------------------------------------------------------------
   E. THE STAGE 7 PORTAL - NO PAUSE, NO HESITATION
   "Why are you pausing and hesitating? The pilot flies, the portal appears as the pilot is flying and
   he flys through it while going 'What is this?! What is happening to me?!' and the portal literally
   swallows them and animates to close and then the flames engulf the screen and the dialogue with
   the other pilots and such."
   What made it hesitate (0929/0930 escape, measured): a 2.2s stand-still self-destruct before the
   ship moved, a 1.9s DECELERATION onto a portal fixed to the ground, a 0.4s HOLD in front of it, and
   only then the entry - the run braked to a stop twice.
   Now, one continuous run:
     0.0  the wreck goes critical behind you (0.9s) - Decker calls the self-destruct
     0.9  full thrust; the sewer races underneath at 880px/s and never slows
     2.8  a rift tears open in the AIR ahead, mid-flight - the pilot: "WHAT IS THIS?!..."
     3.2  the rift pulls the ship in, spinning and shrinking, still at full speed
     4.5  swallowed: the rift snaps shut through its closing frames
     4.7  the flames roll up the screen and engulf it
     5.2  Decker, then Cole, over the fire - then fade and the stage clears
   --------------------------------------------------------------------------------------------- */
const S7P={SD:.9,ACC:.7,VMAX:880,OPEN:2.8,PULL:3.2,ENTRY:1.3,CLOSE:.9,FLAME_IN:1.1,PORTAL_H:236};
function s7pSpeed(t){const tau=t-S7P.SD;if(tau<=0)return 0;const k=clamp(tau/S7P.ACC,0,1);return S7P.VMAX*k*k*(3-2*k);}
function s7pSay(who,text,dur){const F=boss&&boss._s7warden&&boss._s7warden.final;if(!F)return;F.radio={who,full:text,t:0,typed:0,dur:dur||3};}
function s7pFlameBoom(x,y,size,serial){
  if(serial%3===0)explode(x,y,size*.7,'red','fireball');
  else s67ToxicBoom(x,y,size,serial);
}
fr27Exit=function(b,dt){
  const M=b._s7mod,F=b._s7warden.final;let E=M.frExit;
  if(!E||!E.k1001){
    E=M.frExit={s67:true,k1001:true,t:0,beat:0,serial:0,fx:0,S:0,travel:0,v:0,groundY:b.y,x:b.x,sourceY:_masterSrcY,
      startX:player.x,startY:player.y,portalX:clamp((camLeftX()+camRightX())/2,170,worldWidth()-170),portalYNow:viewTopY()+VH*.40,
      zoom:1,blown:false,portalOn:false,portalT:0,entry:null,closeT:null,flame:null,done:false,fade:0};
    for(const k of ['s7m_portal','s7m_explosion','s7m_spew','efx_burst_toxic'])try{XART.rdy(k);}catch(_w){}
  }
  E.t+=dt;M.t=E.t;M.clock+=dt;const C=S7P,t=E.t;
  F.phase='escape';b._s7FinalNoBar=true;b._s7warden.noHit=true;bossDefeated=true;eBullets.length=0;
  for(const s of seatList())withSeat(s,()=>{player.invuln=Math.max(player.invuln,3);});
  /* the terrain never brakes; once the flames own the screen it is no longer seen, and it stops at
     the end of the connector strip the stage-7 backdrop extends north */
  E.v=E.flame&&E.flame.k>=1?0:s7pSpeed(t);
  const dS=Math.min(3900-E.S,E.v*dt);if(dS>0){E.S+=dS;s67ShiftAnchored(dS);}
  E.travel=E.S;b.x=E.x;b.y=E.groundY+E.S;F.bossHidden=b.y-(b.h||260)>VH+60;
  const name=(PILOTS.find(q=>q.key===run.pilot)?.name||run.pilot).toUpperCase();
  /* radio */
  if(E.beat===0&&t>=.1){E.beat=1;s7pSay(missionRadioWho('DECKER'),'SELF-DESTRUCT SEQUENCE IN THAT THING! GO!',1.7);s7WardenMechSound('scream');}
  if(E.beat===1&&t>=1.7){E.beat=2;s7pSay(missionRadioWho('COLE'),"IT'S GONNA BLOW! PUNCH IT!",1.1);}
  if(E.beat===2&&t>=C.OPEN){E.beat=3;s7pSay(String(run.pilot||'').toUpperCase(),'WHAT IS THIS?! WHAT IS HAPPENING TO ME?!',2.1);}
  if(E.beat===3&&E.entry&&E.entry.gone&&t>=E.entry.goneAt+.7){E.beat=4;s7pSay(missionRadioWho('DECKER'),name+', NOOOOOOOOOOOOOOO!',2.4);}
  if(E.beat===4&&E.entry&&t>=E.entry.goneAt+3.2){E.beat=5;s7pSay(missionRadioWho('COLE'),'WHERE DID THEY GO? ARE THEY ALL RIGHT? CHECK THE RADAR, NOW!',3.0);}
  if(F.radio){F.radio.t+=dt;F.radio.typed+=dt*46;if(F.radio.t>F.radio.dur)F.radio=null;}
  /* 1. critical: a short cook-off on the wreck while the ship spools up */
  if(t<C.SD){
    E.fx-=dt;if(E.fx<=0){E.fx=.12;const i=E.serial++;s67ToxicBoom(b.x+Math.sin(i*2.4)*92,b.y+Math.cos(i*1.7)*70-10,70+(i%3)*24,i);if(i%2)s7mSound('expSmall');}
    shake=Math.max(shake,2+t*3);
  }
  /* 2. the run */
  if(t>=C.SD&&!E.go){E.go=true;(Audio.SFX.dash||Audio.SFX.launch||function(){})();(Audio.SFX.boost||function(){})();
    for(const p of powerups)if(!p.dead&&p.kind!=='forgecombo'){try{applyPowerup(p);}catch(_ap){}p.dead=true;}}
  if(E.go&&!E.entry){
    const k=clamp((t-C.SD)/1.1,0,1),e=k*k*(3-2*k);
    player.x=lerp(E.startX,E.portalX,e);player.y=lerp(E.startY,VH*.74,e);player._thrustPower=1;
    shake=Math.max(shake,1.5+3.5*(E.v/C.VMAX));
  }
  if(!E.blown&&b.y>VH+40){E.blown=true;const bx=b.x,by=b.y;
    s67Anchor(()=>{for(let i=0;i<7;i++)fr27ToxicExplosion(bx+(i-3)*58,by-20+Math.abs(i-3)*14,190+(i%3)*40,E.serial++);
      if(typeof spawnShockRing==='function')for(const r of [200,320])spawnShockRing(bx,by,r,'fire');});
    shake=Math.max(shake,14);E.greenFlash=.35;(Audio.SFX.atomicDetonate||Audio.SFX.expBig||function(){})();}
  if(E.blown&&!E.flame){E.fx-=dt;if(E.fx<=0){E.fx=.12;s67ToxicBoom(camLeftX()+Math.random()*viewW(),VH-10+Math.random()*40,150+Math.random()*70,E.serial++);}}
  /* 3. the rift opens ahead of the ship, in the air, while it is still flying */
  if(!E.portalOn&&t>=C.OPEN){E.portalOn=true;E.portalT=0;(Audio.SFX.warpGate||Audio.SFX.teleportIn||function(){})();}
  if(E.portalOn)E.portalT+=dt;
  if(E.portalOn&&!E.entry&&t>=C.PULL)E.entry={t0:t,x0:player.x,y0:player.y,gone:false,scale:1,spin:0};
  if(E.entry){
    const P=E.entry,u=clamp((t-P.t0)/C.ENTRY,0,1),e=u*u*u*.35+u*u*.65;
    for(const p of powerups)if(!p.dead&&p.kind!=='forgecombo')p.dead=true;
    if(!P.gone){
      player.x=lerp(P.x0,E.portalX,e);player.y=lerp(P.y0,E.portalYNow,e);player._thrustPower=1;
      P.scale=1-.9*clamp((u-.3)/.7,0,1);P.spin=u*u*TAU*1.6;E.zoom=1+.16*(u*(2-u));F.shipHidden=true;
      if(u>=1){P.gone=true;P.goneAt=t;E.closeT=t;E.whiteFlash=.6;
        s67Anchor(()=>{if(typeof efxBurst==='function')efxBurst('toxic',E.portalX,E.portalYNow,140);if(typeof spawnShockRing==='function')spawnShockRing(E.portalX,E.portalYNow,170,'fire');});
        (Audio.SFX.teleportIn||Audio.SFX.warpGate||function(){})();}
    }else E.zoom=Math.max(1,E.zoom-dt*.4);
  }
  /* 4. the flames roll up and engulf the screen */
  if(E.entry&&E.entry.gone&&!E.flame&&t>=E.entry.goneAt+.2){E.flame={t0:t,k:0,fx:0};(Audio.SFX.atomicDetonate||Audio.SFX.expBig||function(){})();}
  if(E.flame){
    const Fl=E.flame;Fl.k=clamp((t-Fl.t0)/C.FLAME_IN,0,1);Fl.fx-=dt;
    if(Fl.fx<=0){Fl.fx=.06;const front=lerp(VH+60,viewTopY()-40,Fl.k);
      for(let i=0;i<3;i++)s7pFlameBoom(camLeftX()+Math.random()*viewW(),front+Math.random()*(VH-front+60),160+Math.random()*120,E.serial++);
      if(E.serial%4===0)s7mSound('expBig');}
    shake=Math.max(shake,Fl.k<1?9:4);
  }
  E.greenFlash=Math.max(0,(E.greenFlash||0)-dt*1.4);E.whiteFlash=Math.max(0,(E.whiteFlash||0)-dt*1.8);
  /* 5. done: after the last line, fade and clear */
  const end=E.entry&&E.entry.goneAt!=null?E.entry.goneAt+7.6:1e9;
  if(t>=end-1.3)E.fade=clamp((t-(end-1.3))/1.1,0,1);
  if(t>=end&&!E.done){E.done=true;
    if(!b._forgeRewardDropped){b._forgeRewardDropped=true;forgeBossDrop(player.x,player.y);run.score+=35000;}
    for(const p of powerups)if(p.kind==='forgecombo'&&!p.dead){applyPowerup(p);p.dead=true;}
    F.finished=true;F.phase='done';F.radio=null;F.shipHidden=false;b.dead=true;bossActive=false;bossDefeated=true;whiteBlast=0;run._l78Entry=1;
    if(run.mode==='campaign')campaign._l78Pending=1;drawStageClear._init=false;drawStageClear._res=null;Audio.stopMusic();setState(GS.STAGECLEAR);}
  return true;
};
const FB1001_S7PORTAL=drawS7FinalPortalWorld;
drawS7FinalPortalWorld=function(){
  if(run.stage!==7)return;const E=boss?._s7mod?.frExit;
  if(!E||!E.k1001)return FB1001_S7PORTAL();
  s67StreaksDraw(E);
  const C=S7P;
  if(E.portalOn&&!(E.closeT&&E.t>E.closeT+C.CLOSE)){
    let f,size=C.PORTAL_H;const age=E.portalT;
    if(E.closeT){const c=clamp((E.t-E.closeT)/C.CLOSE,0,1);f=12+Math.min(3,Math.floor(c*4));size*=1-.75*c*c;}
    else{f=age<.6?Math.min(3,Math.floor(age*6.5)):4+Math.floor(age*10)%8;size*=.35+.65*clamp(age/.5,0,1);
      if(E.entry&&!E.entry.gone)size*=1+.12*clamp((E.t-E.entry.t0)/C.ENTRY,0,1);}  // it widens to take the ship
    missionToxicPortal(f,E.portalX,E.portalYNow,size,size*.87);
    if(E.whiteFlash>0){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=E.whiteFlash;missionToxicPortal(f,E.portalX,E.portalYNow,size,size*.87);ctx.restore();}
  }
  const P=E.entry;
  if(P&&!P.gone&&typeof _drawPlayerCore==='function'){
    const s=P.scale==null?1:P.scale;ctx.save();ctx.translate(player.x,player.y);ctx.rotate(P.spin||0);ctx.scale(s,s);ctx.translate(-player.x,-player.y);
    ctx.globalAlpha=clamp(.3+s,0,1);try{_drawPlayerCore();}catch(_pc){}ctx.restore();
  }
};
/* the fire wall is drawn in screen space under the radio, so the dialogue reads over the flames */
const FB1001_S7RADIO=s7WardenRadioDraw;
s7WardenRadioDraw=function(){
  const E=boss?._s7mod?.frExit;if(!E||!E.k1001)return FB1001_S7RADIO();
  if(E.greenFlash>0){ctx.save();ctx.fillStyle='rgba(120,255,70,'+Math.min(.45,E.greenFlash)+')';ctx.fillRect(0,0,VW,VH);ctx.restore();}
  if(E.whiteFlash>0){ctx.save();ctx.fillStyle='rgba(235,255,225,'+Math.min(.6,E.whiteFlash)+')';ctx.fillRect(0,0,VW,VH);ctx.restore();}
  if(E.flame){
    const k=E.flame.k,front=lerp(VH,-60,k),fl=.9+.1*Math.sin(E.t*23);
    ctx.save();
    const g=ctx.createLinearGradient(0,front-90,0,VH);
    g.addColorStop(0,'rgba(255,170,40,0)');g.addColorStop(.25,'rgba(255,120,30,'+(.55*fl)+')');
    g.addColorStop(.6,'rgba(150,230,40,'+(.62*fl)+')');g.addColorStop(1,'rgba(40,70,10,'+(.78*fl)+')');
    ctx.fillStyle=g;ctx.fillRect(0,front-90,VW,VH-front+90);ctx.restore();
  }
  /* the radio is pinned to the top: the in-play box rides above the player, which during the swallow
     put it straight over the rift and the ship going into it */
  const F=boss&&boss._s7warden&&boss._s7warden.final,R=F&&F.radio;
  if(R&&typeof dlgBox==='function'){
    const full=(typeof subst==='function')?subst(R.full):R.full,who=R.who||'FURY WING';
    dlgBox({who,full,shown:full.slice(0,Math.max(0,R.typed|0)),y:12,portrait:String(who).toLowerCase(),
      emo:String(who).toLowerCase()===String(run.pilot||'').toLowerCase()?'crash':'anger',
      tint:(typeof dialogueNameColor==='function'?dialogueNameColor(who,'#54dcff'):'#54dcff')});
  }
  if(E.fade>0){ctx.save();ctx.fillStyle='rgba(0,0,0,'+E.fade+')';ctx.fillRect(0,0,VW,VH);ctx.restore();}
};
