"use strict";
/* Mike's Stage 6/7 pass. Simulation-owned lanes, authored portals/beam reels.
   Loaded after the September 28 combat/HAMA owners. No separate cinematic screen. */
const MISSION29_BASE={opening:s6OpeningTick,openingDraw:s6OpeningDraw,strike:s6StrikeTick,
 fleet:furyFleetDraw,stage:beginStage,s7:s7mTick,portal:drawS7FinalPortalWorld,
 bg:drawBG,radar:drawCampaignRadar,radio:s7WardenRadioDraw,exit:fr27Exit,wingSay:s6WingSay};
for(const A of Object.values(MISSION29_ART))XART._src[A.key]=A.path;
function missionWarm(){for(const A of Object.values(MISSION29_ART))XART.rdy(A.key);l23FovWarm();s7mWarm();}
function missionCell(name,frame,x,y,w,h){const A=MISSION29_ART[name];if(!A||!XART.rdy(A.key))return false;
 const r=A.frames[((frame|0)%A.frames.length+A.frames.length)%A.frames.length];
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(A.key),...r,x,y,w,h);ctx.restore();return true;}
function missionBeamDraw(b){
 const A=MISSION29_ART['beam_'+b._inf];if(!A||!XART.rdy(A.key))return false;
 const top=b.top??PLAY.y,bot=b.bot??player.y-14;if(bot<=top)return true;
 const r=A.frames[Math.floor(efxClock*A.fps)%A.frames.length],ink=A.ink;
 const w=Math.max(12,b.w||18),h=bot-top;
 // One fixed origin and column; animation never widens the collision volume.
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.beginPath();ctx.rect(b.x-w/2,top,w,h);ctx.clip();
 ctx.drawImage(XART.get(A.key),r[0]+ink[0],r[1]+ink[1],ink[2],ink[3],b.x-w/2,top,w,h);ctx.restore();
 wm26Draw(ctx,wm26Family(b._inf),b.x,bot,-Math.PI/2,(efxClock*18)%1,clamp(w*1.2,20,42),INFUSIONS[b._inf]?.glow);
 return true;
}
s6WingSay=function(who,text){return MISSION29_BASE.wingSay(missionRadioWho(who),text);};

/* Opening assaults occupy the existing live-opening slot, so the normal director
   and stage timer wait while controls, missiles, maneuvers, sky and collision stay live. */
function missionAssaultStart(){
 const n=fr27Difficulty(),O=s6Opening={phase:'assault',t:0,allT:0,shots:[],jets:[],radio:null,
  lanes:[],events:[],index:0,serial:0,n,finish:0,history:[],beeps:0};
 const L=camLeftX(),R=camRightX(),T=viewTopY()+65,B=VH-62,rows=n===0?4:5;
 const ys=Array.from({length:rows},(_,i)=>lerp(T,B,(i+.5)/rows));
 let at=.65;
 // Deliberately leave one complete row safe in each crossing set.
 for(const [direction,safe]of [['west',rows-1],['east',0]]){
  for(let i=0;i<rows;i++)if(i!==safe){O.events.push({at,kind:'lane',direction,y:ys[i],x:0});at+=.50;}
  at+=4.1;
 }
 const bombSets=[2,3,4][n],concurrent=[1,2,3][n];
 for(const direction of ['east','west']){
  for(let wave=0;wave<bombSets;wave++){
   for(let j=0;j<concurrent;j++)O.events.push({at:at+j*.14,kind:'bomb',direction,y:ys[(wave+j)%rows],rack:wave,targetOffset:(j-(concurrent-1)/2)*66});
   at+=1.6;
  }
  at+=3.1;
 }
 // Descending gates always leave a full lane open; Furious sends three at once.
 const cols=5,batches=[3,4,5][n],count=[1,2,3][n];
 for(let wave=0;wave<batches;wave++){
  for(let j=0;j<count;j++){const col=(wave*2+j)%cols;
   O.events.push({at:at+j*.28,kind:'lane',direction:'south',x:lerp(L+48,R-48,(col+.5)/cols),y:0,
    attack:n===2?(wave+j)%3:null});}
  at+=2.35;
 }
 O.finish=at+4.2;missionWarm();return O;
}
function missionJetSpawn(event,O){
 const dir=event.direction,side=dir!=='south',L=camLeftX(),R=camRightX();
 const x=side?(dir==='east'?L-85:R+85):event.x,y=side?event.y:viewTopY()-85;
 const e=spawnEnemy('s1jetbomber_b',x,y,{route:'straight'});if(!e)return null;
 e.x=x;e.y=y;e.t=0;e.w=54;e.h=side?40:65;e.pattern='s6strike';e.shoots=false;e.fk=null;e._atk='none';e._esw=null;e._noSep=true;
 e._polishBomberCD=999;e._s6Strike={direction:dir,t:0,racks:0,cd:999};
 e._mission29={kind:event.kind,n:O.n,direction:dir,attack:event.attack,targetOffset:event.targetOffset||0,shot:false,bomb:false,t:0};
 // Standard hittable engine units: Retina/missiles/interception need no special path.
 e.hp=e.maxhp=[20,26,32][O.n];return e;
}
function missionLane(event,O){
 const n=O.n,q={...event,t:0,warn:[1.7,1.5,1.35][n],released:false,id:'opening-'+O.serial++};
 O.lanes.push(q);combatWarningTick(q,q.id,0,q.warn);return q;
}
function missionAssaultTick(O,dt){
 O.t+=dt;O.allT+=dt;
 while(O.index<O.events.length&&O.t>=O.events[O.index].at){const e=O.events[O.index++];O.history.push(e.kind+':'+e.direction);
  if(e.kind==='lane')missionLane(e,O);else missionJetSpawn(e,O);}
 for(const q of O.lanes){q.t+=dt;combatWarningTick(q,q.id,q.t,q.warn);
  if(!q.released&&q.t>=q.warn){q.released=true;missionJetSpawn(q,O);(Audio.SFX.tlvJetEngine||Audio.SFX.enemyShoot||function(){})();}}
 O.lanes=O.lanes.filter(q=>q.t<q.warn+.12);
 if(O.t>=O.finish&&!enemies.some(e=>e._mission29&&!e.dead)&&!groundTargetingFx.some(q=>q._mission29&&!q.dead)){
  s6Opening=null;run._mission29OpeningDone=true;Input.clearTaps();}
}
s6OpeningTick=function(dt){const O=s6Opening;if(O?.phase==='assault')return missionAssaultTick(O,dt);
 const end=O?.phase==='flyover';MISSION29_BASE.opening(dt);
 if(end&&!s6Opening&&!run._mission29OpeningDone)missionAssaultStart();};
function missionBomb(e){const n=e._mission29.n,T=targetShip(e.x,e.y);
 // Committed spots, limited pressure. No hostile FOV/zone overlay on this wave.
 const limit=[3,5,7][n];if(groundTargetingFx.filter(q=>q._mission29&&!q.dead).length>=limit)return;
 const offset=e._mission29.targetOffset;
 const q=groundTargetingSpawn({kind:'missile',x:clamp(T.x+offset,camLeftX()+42,camRightX()-42),
  y:clamp(T.y+offset*.55,viewTopY()+85,VH-48),owner:e,track:false,lane:false,warn:[1.65,1.5,1.35][n],
  radius:[25,27,29][n],size:76,active:.5,sound:'expBig',shake:5,
  onImpact:g=>{explode(g.x,g.y,90,'red');explode(g.x-19,g.y+8,38,'orange',null,null,null,null,true);}});
 q._mission29=true;q._jetBomb={x:e.x,y:e.y};
 (Audio.SFX.missile||Audio.SFX.enemyShoot||function(){})();
}
s6StrikeTick=function(e,dt){const A=e._mission29;if(!A)return MISSION29_BASE.strike(e,dt);
 A.t+=dt;e._s6Strike.t=A.t;const side=A.direction!=='south',speed=(A.kind==='bomb'?[285,355,425]:[350,455,570])[A.n];
 e.x+=(A.direction==='east'?1:A.direction==='west'?-1:0)*speed*dt;e.y+=(side?0:speed)*dt;e.spin=0;e._polishBomberCD=999;
 const inside=e.x>camLeftX()+45&&e.x<camRightX()-45&&e.y>viewTopY()+30&&e.y<VH-45;
 if(inside&&!A.shot){A.shot=true;
  if(A.kind==='bomb'||A.attack===2)missionBomb(e);
  else if(A.n===2&&A.attack===1&&e.y<player.y-65){for(const off of [-.07,.07])eMG(e.x+off*50,e.y+20,Math.PI/2+off,3.7);}}
 if(A.t>5||e.x<camLeftX()-130||e.x>camRightX()+130||e.y>VH+110)e.dead=true;
};
furyFleetDraw=function(e){const A=e._mission29;if(!A)return MISSION29_BASE.fleet(e);if(e.dead||e._dyingT!=null)return true;
 const f={east:0,west:1,south:2}[A.direction],h=72,w=72;
 if(!missionCell('bluejets',f,e.x-w/2,e.y-h/2,w,h))return MISSION29_BASE.fleet(e);
 e._drawW=w;e._drawH=h;return true;
};
s6OpeningDraw=function(){const O=s6Opening;if(O?.phase!=='assault')return MISSION29_BASE.openingDraw();
 for(const q of O.lanes){if(q.released)continue;const side=q.direction!=='south',p=clamp(q.t/q.warn,0,1);
  const L=camLeftX(),R=camRightX(),top=viewTopY(),col=l23FovPhase(p),key='bmfx_fov_'+col+'_tall';
  const x=side?L:q.x-34,y=side?q.y-29:top,w=side?viewW():68,h=side?58:viewH();
  // The authored shared field plate fills the actual swept strip, leaving visible safe lanes.
  ctx.save();ctx.globalAlpha=.18+.14*p;ctx.fillStyle=col==='green'?'#32e891':col==='yellow'?'#ffd74b':'#ff4840';ctx.fillRect(x,y,w,h);
  if(XART.rdy(key)){ctx.globalAlpha=.30;ctx.drawImage(XART.get(key),x,y,w,h);}ctx.restore();
  const alert='bmfx_alert_'+col+'_danger',ax=side?(q.direction==='west'?R-27:L+27):q.x,ay=side?q.y:top+33;
  if(XART.rdy(alert)){const im=XART.get(alert),s=32;ctx.save();ctx.globalAlpha=p<.5?1:.6+.4*Math.abs(Math.sin(q.t*(8+p*20)));ctx.drawImage(im,ax-s/2,ay-s/2,s,s);ctx.restore();}
 }};
beginStage=function(num){const r=MISSION29_BASE.stage.apply(this,arguments);run._mission29OpeningDone=false;
 if(num===6||num===7||num===8)missionWarm();return r;};

/* One upright toxic doorway everywhere; never the old ground seal or circular warp. */
function missionToxicPortal(frame,x,y,h,w){return s7mBlit('portal',clamp(frame|0,0,15),x,y,w||h*.87,h,0,1);}
fr27ToxicPortal=function(frame,x,y,size){const f=frame<4?frame:frame===4?4+Math.floor(efxClock*10)%8:12+Math.min(3,(frame-5)*2);
 return missionToxicPortal(f,x,y,size*1.8,size*1.55);};
function missionIntro(b){const M=b?._s7mod;return M&&!M.tank&&M.mode==='portal'&&!M._mission29IntroDone;}
s7mTick=function(b,dt){const M=b?._s7mod||(s7mOwns(b)?s7mInit(b):null);
 if(missionIntro(b)){
  const I=M._mission29Intro||(M._mission29Intro={t:0,fx:.3,serial:0,said:false});I.t+=dt;M.clock+=dt;M.t=0;
  const F=b._s7warden.final;F.phase='portalClose';b._s7FinalNoBar=true;b._s7warden.noHit=true;player.invuln=Math.max(player.invuln,3);
  eBullets.length=0;pBullets.length=0;storySkip();
  if(!I.said&&I.t>=1){I.said=true;F.radio={who:missionRadioWho('DECKER'),full:'RADAR RELAY IS JAMMED. I AM READING AN ANOMALY... SOMETHING IS COMING THROUGH!',t:0,typed:0,dur:6.6};Audio.SFX.lockAlert?.();}
  if(F.radio){F.radio.t+=dt;F.radio.typed+=dt*38;}
  I.fx-=dt;if(I.fx<=0&&I.t<6.8){I.fx=.42;const L=camLeftX(),R=camRightX(),i=I.serial++;
   const x=i%2?R-35:L+35,y=viewTopY()+65+(i*73)%(viewH()-115);fr27ToxicExplosion(x,y,90+i%3*22,i);s7mSound(i%4?'expSmall':'expBig');shake=Math.max(shake,2.5);}
  if(I.t>=7){M._mission29IntroDone=true;M.t=0;F.radio=null;(Audio.SFX.warpGate||Audio.SFX.teleportIn||function(){})();}
  return true;
 }
 return MISSION29_BASE.s7(b,dt);
};
const MISSION29_S7DRAW=s7mDraw;
s7mDraw=function(b){const M=b?._s7mod,E=M?.frExit;if(!E)return MISSION29_S7DRAW(b);
 if(b.y-(b.h||260)>VH+40)return true;
 // Frozen wreck pose shares the terrain's source position. No chase/recover animation.
 if(!E.pose){E.pose=s7mPose(b).map(p=>({...p}));E.x=b.x;}
 b.x=E.x;b.y=E.groundY+E.travel;M.height=0;M.drop=0;M.lean=0;
 for(const p of E.pose){const part=M.parts.find(q=>q.id===p.id);if(part&&part.hp<=0)continue;
  s7mBlit(p.id==='body'?'body':'warden',p.cell,b.x+p.x,b.y+p.y,p.w,p.h,p.a||0,1,.10+.07*Math.sin(E.t*16));}
 return true;
};
fr27Exit=function(b,dt){const r=MISSION29_BASE.exit(b,dt),E=b._s7mod.frExit;if(E){b.y=E.groundY+E.travel;b.x=E.x??b.x;
 b._s7warden.final.bossHidden=b.y-(b.h||260)>VH+40;}return r;};
drawS7FinalPortalWorld=function(){if(run.stage!==7)return;const M=boss?._s7mod;if(!M||M.tank)return;
 const E=M.frExit;if(E){if(E.t<14.1||E.t>=18.5)return;const age=E.t-14.1,close=clamp((E.t-17.3)/1.2,0,1);
  const f=close?12+Math.min(3,Math.floor(close*4)):age<.8?Math.min(3,Math.floor(age*5)):4+Math.floor(age*10)%8;
  missionToxicPortal(f,E.portalX,E.portalY,274*(1-close),240*(1-close));return;}
 if(missionIntro(boss)){const t=M._mission29Intro?.t||0;if(t>=3.3)missionToxicPortal(Math.min(7,Math.floor((t-3.3)*3)),worldWidth()/2,149,274);return;}
 if(['portal','entry','roar'].includes(M.mode)){
  const f=M.mode==='roar'?12+Math.min(3,Math.floor(M.t/.3)):4+Math.floor(M.clock*10)%8;
  if(M.mode!=='roar'||M.t<1.2)missionToxicPortal(f,worldWidth()/2,149,274);}
};
drawBG=function(dt){const r=MISSION29_BASE.bg(dt);if(run.stage===7&&missionIntro(boss)){
 const t=boss._s7mod._mission29Intro?.t||0,a=Math.min(.55,t/.65*.55)*clamp((7.6-t)/.9,0,1);
 ctx.save();ctx.fillStyle='rgba(0,2,0,'+a+')';ctx.fillRect(camLeftX()-8,viewTopY()-8,viewW()+16,viewH()+16);ctx.restore();}return r;};
drawCampaignRadar=function(){if(run.stage!==7||!missionIntro(boss))return MISSION29_BASE.radar();
 const {x,y,w,h}=bottomHudLayout().radar;MISSION29_BASE.radar();
 missionCell('radar',Math.floor((boss._s7mod._mission29Intro?.t||0)*18),x+8,y+8,w-16,h-16);
 campText('JAM',x+w/2,y+h/2,7,'#c4ffab');};
