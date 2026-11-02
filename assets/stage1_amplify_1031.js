"use strict";
/* Mike's Stage1 five-enemy pass. Actual source-frame headings, physical muzzle
   sockets and finite sorties. Native HP, damage flashes, death, ground traffic,
   missile locks/interception, ground Retina and shared mixer remain owners. */
const S1A={fx:[],events:[],draws:{},actor:null,shotSide:0,base:{spawn:spawnEnemy,
 naval:navalTick,flash:navalFlash,boatDraw:furyBoatModuleDraw,boatTick:furyBoatModuleTick,
 jet:jetTick,exhaust:s1mExhaust,draw:drawEnemy,tank:tankTick,tankDraw:drawModularTank,
 shot:eShootT,projectile:drawCombatFinalProjectile,effects:updateEffects,
 flashes:drawNavalFlashes,bomb:fb9BomberTick,ground:groundTargetingDraw,begin:beginStage,load:stageLoadBegin,aiEnd:ai27End,route:eb11OwnsRoute}};
for(const a of Object.values(S1A_ART)){XART._src[a.key]=a.path;XART.rdy(a.key);}
function s1aLog(event,e,extra={}){S1A.events.push({event,type:e?.type,at:efxClock,x:e?.x,y:e?.y,...extra});if(S1A.events.length>400)S1A.events.shift();}
function s1aLive(e){return(run.stage===1||e?._s1bTurret)&&e&&!e.dead&&e._dyingT==null;}
function s1aHeavy(e){return s1aLive(e)&&/^s1tankheavy(?:_b)?$/.test(rosterKey(e.type));}
function s1aJet(e){return s1aLive(e)&&/^s1jetdelta(?:_b)?$/.test(rosterKey(e.type));}
function s1aAngle(a){return Math.atan2(Math.sin(a),Math.cos(a));}
function s1aDir(angle,n=32){return ((Math.round(s1aAngle(angle-Math.PI/2)/TAU*n)%n)+n)%n;}
function s1aPoseAngle(angle,n=32){return Math.PI/2+s1aDir(angle,n)*TAU/n;}
function s1aBlit(name,frame,angle,x,y,size,tint){
 const a=S1A_ART[name];if(!a||!XART.rdy(a.key))return false;
 const f=clamp(frame|0,0,a.frames-1),d=s1aDir(angle,a.dirs),im=tint?xartTint(a.key,tint,tint==='#ffffff'?1:.55):XART.get(a.key),s=size||a.cell;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,d*a.cell,f*a.cell,a.cell,a.cell,x-s/2,y-s/2,s,s);ctx.restore();S1A.draws[name]=(S1A.draws[name]||0)+1;return true;
}
function s1aPlaneHead(e){return e._fb9Swoop?.head??e._s1aFlight?.head??e._s1aNativeHead??Math.PI/2;}
function s1aPlanePoint(e,x,y){
 const angle=s1aPoseAngle(s1aPlaneHead(e))-Math.PI/2,c=Math.cos(angle),s=Math.sin(angle),k=Math.max(e.w,e.h)*1.10/128;
 return{x:e.x+((x-64)*c-(y-64)*s)*k,y:e.y+((x-64)*s+(y-64)*c)*k,angle:angle+Math.PI/2};
}
function s1aPlaneMuzzle(e,side){return s1aPlanePoint(e,64+side*18,85);}
function s1aPlaneBank(e){return rosterKey(e.type)==='s1jetdelta_b'?'strike_heading':'delta_heading';}
function s1aPlanePose(e){const turn=s1aAngle(s1aPlaneHead(e)-Math.PI/2);return Math.abs(turn)<.12?0:turn<0?1:2;}
function s1aBoatMuzzle(e,m){const p=furyBoatPoint(e,m);return{x:p.x,y:p.y+(e.type==='s1boatgun'?6.6:14),angle:Math.PI/2};}
function s1aTankHead(e){return s1aPoseAngle(Number.isFinite(e._modAngle)?e._modAngle:Math.PI/2,64);}
function s1aTankMuzzle(e,side){
 const angle=s1aTankHead(e)-Math.PI/2,c=Math.cos(angle),s=Math.sin(angle),k=e.w*1.05/384;
 const x=(side<0?186:215)-192,y=365-192;
 return{x:e.x+(x*c-y*s)*k,y:e.y+(x*s+y*c)*k,angle:angle+Math.PI/2};
}
function s1aFlash(e,point,name='muzzle',size=48,follow=null){
 if(!s1aLive(e))return;S1A.fx.push({owner:e,point,follow,name,size,t:0,life:.13});if(S1A.fx.length>100)S1A.fx.shift();
}
function s1aRound(e,p,speed,kind,options={}){
 const b=S1A.base.shot(p.x,p.y,p.angle,speed,kind,{...options,noMuzzle:true,owner:e});
 if(!b||b.dead||b._ai27Held)return b;
 b._s1aOwner=e;b._s1aSlug=kind==='s1bullet';b._s1aMissile=kind==='s1jungleMissile';
 s1aLog('shot',e,{kind,x:p.x,y:p.y,angle:p.angle});return b;
}
spawnEnemy=function(){const e=S1A.base.spawn.apply(this,arguments);
 if(run.stage===1&&e&&['s1boatgun','s1corvette','s1jetdelta','s1jetbomber','s1tankheavy','s1tankheavy_b'].includes(e.type))e.t=0;
 if(run.stage===1&&e?.type==='s1boatgun'){e._naval='gun';e._atk='mg';e.fk=null;navalInit(e,'gun');}return e;
};
// Preserve each boat's existing two destructible module pools; the Gunboat now
// carries the authored small machine-gun turrets instead of rocket-rack poses.
furyBoatModuleTick=function(e,dt){const r=S1A.base.boatTick.apply(this,arguments);if(s1aLive(e)&&e.type==='s1boatgun')for(const m of furyBoatModules(e))m.aim=2;return r;};
furyBoatModuleDraw=function(e){
 if(!s1aLive(e)||e.type!=='s1boatgun')return S1A.base.boatDraw.apply(this,arguments);
 for(const m of furyBoatModules(e)){const p=furyBoatPoint(e,m),key='furyboat_turret_'+(m.hp>0?0:1)+'_2';if(!XART.rdy(key))continue;
  const tint=tintColor(e),im=tint?xartTint(key,tint,tint==='#ffffff'?1:.55):XART.get(key);ctx.drawImage(im,p.x-9,p.y-9,18,18);}
};
navalTick=function(e,dt){const old=S1A.actor;if(s1aLive(e)&&['s1boatgun','s1boatpatrol','s1corvette'].includes(e.type))S1A.actor=e;
 try{const r=S1A.base.naval.apply(this,arguments);if(e.type==='s1boatgun'&&e._s1rTell){e._s1rTell.x=e.x;e._s1rTell.y=targetShip(e.x,e.y).y;}return r;}finally{S1A.actor=old;}
};
eShootT=function(x,y,angle,speed,kind,opts){
 const e=S1A.actor;if(!s1aLive(e))return S1A.base.shot.apply(this,arguments);
 if(kind!=='s1bullet')return S1A.base.shot.apply(this,arguments);
 let p={x,y,angle};
 if(s1aJet(e)){const side=S1A.shotSide++%2?-1:1;p=s1aPlaneMuzzle(e,side);const b=s1aRound(e,p,speed,kind,opts);if(b&&!b.dead)s1aFlash(e,p,'muzzle',40,()=>s1aLive(e)?s1aPlaneMuzzle(e,side):null);return b;}
 if(e.type==='s1boatgun'){
  const m=furyBoatModules(e).filter(m=>m.hp>0).sort((a,b)=>Math.hypot(furyBoatPoint(e,a).x-x,furyBoatPoint(e,a).y-y)-Math.hypot(furyBoatPoint(e,b).x-x,furyBoatPoint(e,b).y-y))[0];
  if(m)p=s1aBoatMuzzle(e,m);
 }
 return s1aRound(e,p,speed,kind,opts);
};
navalFlash=function(e,mz,scale,fam,opts={}){
 if(!e&&s1aJet(S1A.actor))return; // eShootT already emitted this barrel's attached frame reel.
 if(!s1aLive(e)||!['s1boatgun','s1boatpatrol','s1corvette'].includes(e.type))return S1A.base.flash.apply(this,arguments);
 if(e.type==='s1corvette'){
  const point=()=>s1aLive(e)?{...navalHardpoint(e,opts.ox,opts.oy),angle:Math.PI/2}:null;
  return s1aFlash(e,point(),'muzzle',48,point);
 }
 const m=furyBoatModules(e).filter(m=>m.hp>0).sort((a,b)=>Math.hypot(furyBoatPoint(e,a).x-mz.x,furyBoatPoint(e,a).y-mz.y)-Math.hypot(furyBoatPoint(e,b).x-mz.x,furyBoatPoint(e,b).y-mz.y))[0];
 if(!m)return;const point=()=>s1aLive(e)&&m.hp>0?s1aBoatMuzzle(e,m):null;return s1aFlash(e,point(),'muzzle',e.type==='s1boatgun'?42:48,point);
};
function s1aFlight(e,dt){
 let A=e._s1aFlight;
 if(!A){if(e._jet==null){const C=S1_JET_ELITE[diffKey];if(C){e.hp=Math.ceil(e.hp*C.hp);e.maxhp=e.hp;e._jspd*=C.speed;e._fmul=(e._fmul||1)*C.fire;}e._s1aEliteApplied=true;}const T=targetShip(e.x,e.y),mid=(camLeftX()+camRightX())/2,side=e.x<mid?-1:1;
  A=e._s1aFlight={head:Math.PI/2,phase:'approach',side,aimX:clamp(T.x+side*70,camLeftX()+55,camRightX()-55),aimY:PLAY.y+190,cd:.50,rounds:0,speed:e._jspd||96};
  if(e._route&&e._route!=='straight'){A.phase='route';A.side=/R$/.test(e._route)?1:-1;}
  e._jet=1;e._s1Elite=null;e._noSep=true;e.fk=null;e.shoots=false;e._atk='none';
 }
 const oldX=e.x,oldY=e.y;
 if(A.phase==='approach'&&(e.y>PLAY.y+55||Math.hypot(e.x-A.aimX,e.y-A.aimY)<45))A.phase='attack';
 if(A.phase==='attack'&&(e.y>PLAY.y+225||Math.hypot(e.x-A.aimX,e.y-A.aimY)<45)){A.phase='peel';A.exitX=A.side<0?camLeftX()-140:camRightX()+140;A.exitY=Math.max(e.y+90,PLAY.y+335);}
 if(A.phase==='route'&&e.y>VH*.70){A.phase='peel';A.exitX=A.side<0?camLeftX()-140:camRightX()+140;A.exitY=VH+130;}
 const tx=A.phase==='approach'?e.x:A.phase==='attack'?A.aimX:A.exitX,ty=A.phase==='approach'?e.y+100:A.phase==='attack'?A.aimY:A.exitY;
 const wx=A.phase==='route'?clamp(jetRouteX(e,dt),-A.speed*.92,A.speed*.92):0;
 const want=A.phase==='route'?Math.atan2(Math.sqrt(A.speed*A.speed-wx*wx),wx):Math.atan2(ty-e.y,tx-e.x);A.head+=clamp(s1aAngle(want-A.head),-dt*1.65,dt*1.65);
 e.x+=Math.cos(A.head)*A.speed*dt;e.y+=Math.sin(A.head)*A.speed*dt;e.vx=(e.x-oldX)/Math.max(dt,.001)/60;e.vy=(e.y-oldY)/Math.max(dt,.001)/60;e.spin=0;
 const T=targetShip(e.x,e.y);A.cd-=dt;
 if(A.cd<=0&&e.y>PLAY.y+15&&e.y<T.y-85&&e.x>camLeftX()+22&&e.x<camRightX()-22&&Math.abs(s1aAngle(A.head-Math.PI/2))<1.10&&(typeof eb11Ready!=='function'||eb11Ready(e))){
  let fired=false;for(const side of [-1,1]){const p=s1aPlaneMuzzle(e,side),b=s1aRound(e,p,4.6,'s1bullet',{silent:true});if(b&&!b.dead){fired=true;s1aFlash(e,p,'muzzle',40,()=>s1aLive(e)?s1aPlaneMuzzle(e,side):null);}}
  if(fired)Audio.SFX.enemyMachineGunLight?.();A.rounds++;A.cd=(A.rounds%4?.14:.72)*(e._fmul||1);
 }
 const pad=Math.max(e.w,e.h)*.7;if(e.x<camLeftX()-pad||e.x>camRightX()+pad||e.y>VH+pad)e.dead=true;
}
jetTick=function(e,dt){
 const old=S1A.actor,x=e?.x,y=e?.y,wasLocked=e?._kmLocked;if(s1aJet(e)){S1A.actor=e;S1A.shotSide=0;}
 try{if(s1aJet(e)&&!e._fb9Swoop&&!e._s1Kamikaze&&!e._s1Rush){if((e._s1DelayFrames||0)>0){e._s1DelayFrames--;return;}if(e._stagger>0){e._stagger=Math.max(0,e._stagger-dt);return;}return s1aFlight(e,dt);}const r=S1A.base.jet.apply(this,arguments);if(s1aJet(e)&&Math.hypot(e.x-x,e.y-y)>.01)e._s1aNativeHead=Math.atan2(e.y-y,e.x-x);if(s1aJet(e)&&e._s1Kamikaze&&!wasLocked&&e._kmLocked)Audio.SFX.jetDash?.();return r;}finally{S1A.actor=old;}
};
// The shared AI may decide a lateral dodge; turn that decision into a flown
// heading on the next frame instead of adding a sideways displacement.
ai27End=function(e,previous){if(s1aJet(e)&&e._s1aFlight&&e._ai27?.dx){e._s1aFlight.aimX=clamp(e._s1aFlight.aimX+e._ai27.dx,camLeftX()+45,camRightX()-45);e._ai27.dx=0;}return S1A.base.aiEnd.apply(this,arguments);};
s1mExhaust=function(e){if(s1aJet(e))return;return S1A.base.exhaust.apply(this,arguments);};
function s1aJetDraw(e){
 const head=s1aPlaneHead(e),size=Math.max(e.w,e.h)*1.10,pose=s1aPlanePose(e),bank=s1aPlaneBank(e);
 ctx.save();ctx.globalAlpha=.24;s1aBlit(bank,pose,head,e.x+10,e.y+18,size,'#000000');ctx.restore();
 for(const [x,y]of S1A_ART[bank].tailSockets[pose]){const m=s1aPlanePoint(e,x,y);s1aBlit('thruster',Math.floor((e.t||0)*22)%8,m.angle,m.x,m.y,58);}
 s1aBlit(bank,pose,head,e.x,e.y,size,tintColor(e));e._air13RenderedKey=S1A_ART[bank].key;e._air13Frame=s1aDir(head);e._s1aPose=pose;e._drawW=e._drawH=size;
}
drawEnemy=function(e){if(s1aJet(e))return s1aJetDraw(e);return S1A.base.draw.apply(this,arguments);};
eb11OwnsRoute=function(e){return s1aHeavy(e)||s1aJet(e)||s1aLive(e)&&e.type==='s1jetbomber'||S1A.base.route.apply(this,arguments);};
fb9BomberTick=function(e,dt){
 if(!s1aLive(e)||e.type!=='s1jetbomber')return S1A.base.bomb.apply(this,arguments);
 const B=e._fb9Bomber;if(!B)return;B.cd-=dt;
 if(e.y>viewTopY()+12&&e.y<VH+e.h*.2&&e.x>camLeftX()+18&&e.x<camRightX()-18&&B.cd<=0){
  B.cd=diffKey==='easy'?.68:diffKey==='normal'?.58:.46;B.n++;
  const side=B.n%2?1:-1,x=e.x+side*e.w*.16,y=e.y+e.h*.14,warn=diffKey==='easy'?1.1:diffKey==='normal'?.98:.88;
  const q=groundTargetingSpawn({kind:'missile',x,y:Math.min(VH-24,y+105),owner:e,track:false,lane:false,warn,active:.42,radius:25,size:46,sound:'expBig',shake:3,onImpact:g=>{explode(g.x,g.y,46,'red');}});
  q._s1aBomb={x,y};q._fb9Bomb=true;s1aLog('bomb-drop',e,{x,y,landX:q.x,landY:q.y,index:B.n});Audio.SFX.bombDrop?.();
 }
};
groundTargetingDraw=function(){const r=S1A.base.ground.apply(this,arguments);for(const q of groundTargetingFx)if(q._s1aBomb&&!q.dead&&!q.impact&&q.delay<=0){const u=clamp(q.t/q.warn,0,1),p=q._s1aBomb,x=lerp(p.x,q.x,u),y=lerp(p.y,q.y,u*u);s1aBlit('bomb',0,Math.PI/2,x,y,46);}return r;};
tankTick=function(e,dt){
 if(!s1aHeavy(e))return S1A.base.tank.apply(this,arguments);
 const A=e._s1aTank||(e._s1aTank={cd:.8,pending:false});e._atk='dualMissile';e.fk=null;e.shoots=false;
 if(A.pending)e._phase='brake';tankMotionTick(e,dt,TANK_SPD);A.cd-=dt;
 if(A.pending)return;
 const T=targetShip(e.x,e.y),ready=e.y>viewTopY()+e.h*.45&&e.y<VH-110&&T.y>e.y+70&&e.x>camLeftX()+12&&e.x<camRightX()-12&&(typeof eb11Ready!=='function'||eb11Ready(e));
 if(A.cd>0||!ready)return;
 if(e._spd>1.8){e._phase='brake';e._phT=.7;return;}
 A.pending=true;A.cd=diffKey==='furious'?1.05:diffKey==='hard'?1.85:3.3;
 const L=enemyLockOn(e,diffKey==='easy'?.95:.72,{fire:()=>{
  A.pending=false;if(!s1aHeavy(e))return;let fired=false;
  for(const side of [-1,1]){const p=s1aTankMuzzle(e,side),b=s1aRound(e,p,3.05,'s1jungleMissile',{szMul:1.15,silent:true,w:8,h:24});
   if(b&&!b.dead){b.homing=true;b.turn=.025;fired=true;s1aFlash(e,p,'rocket_muzzle',55,()=>s1aHeavy(e)?s1aTankMuzzle(e,side):null);}}
  if(fired){enemyShotSfx('s1jungleMissile');e._recoil=.18;s1aLog('tank-dual',e);}
 }});
 if(!L)A.pending=false;
};
drawModularTank=function(e){
 if(!s1aHeavy(e))return S1A.base.tankDraw.apply(this,arguments);
 const tint=tintColor(e),a=S1M_ART.hull[Math.floor((e._wheelT||0)*2)%8],size=e.w*1.05;
 if(!XART.rdy(a.key)||!XART.rdy(S1A_ART.tank_turret.key))return false;
 const im=tint?xartTint(a.key,tint,tint==='#ffffff'?1:.55):XART.get(a.key);ctx.drawImage(im,e.x-size/2,e.y-size/2,size,size);
 s1aBlit('tank_turret',0,s1aTankHead(e),e.x,e.y,size,tint);e._drawW=e.w;e._drawH=e.h;return true;
};
drawCombatFinalProjectile=function(b){
 if(b?._s1aSlug)return s1aBlit('slug',Math.floor((b.t||0)*24)%4,Math.atan2(b.vy,b.vx),b.x,b.y,64);
 if(b?._s1aMissile)return s1aBlit('missile',Math.min(5,Math.floor((b.t||0)*13)),Math.atan2(b.vy,b.vx),b.x,b.y,54);
 return S1A.base.projectile.apply(this,arguments);
};
updateEffects=function(dt){const r=S1A.base.effects.apply(this,arguments);for(const f of S1A.fx)f.t+=dt;S1A.fx=S1A.fx.filter(f=>s1aLive(f.owner)&&f.t<f.life);return r;};
drawNavalFlashes=function(){const r=S1A.base.flashes.apply(this,arguments);for(const f of S1A.fx){const p=f.follow?f.follow():f.point;if(p)s1aBlit(f.name,Math.min(3,Math.floor(f.t/f.life*4)),p.angle,p.x,p.y,f.size);}return r;};
stageLoadBegin=function(n,keys){return S1A.base.load.call(this,n,n===1?[...(keys||[]),...Object.values(S1A_ART).map(a=>a.key),'furyboat_turret_1_2',...Array.from({length:5},(_,i)=>'furyboat_turret_0_'+i)]:keys);};
beginStage=function(){S1A.fx=[];S1A.events=[];S1A.draws={};S1A.actor=null;return S1A.base.begin.apply(this,arguments);};
