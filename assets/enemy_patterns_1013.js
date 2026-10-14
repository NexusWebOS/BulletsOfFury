"use strict";
/* Late-stage attack vocabulary. One field unit owns the complex pattern; its
   original controller resumes after a visible recovery. No additional actors. */
const EP13={clock:0,next:0,serial:0,owner:null,events:[],stage:0,
 profiles:{
  easy:{tell:1.30,recover:1.25,space:2.2,width:16,sweep:45,live:1.45,pellets:12,rings:1,gap:1.52,shot:1.75,missiles:3,volleys:1,rifleRounds:6,rifleBeat:.18,rifleSpeed:4.5,cap:68},
  normal:{tell:1.12,recover:1.10,space:1.9,width:18,sweep:55,live:1.60,pellets:16,rings:2,gap:1.38,shot:2.05,missiles:3,volleys:2,rifleRounds:8,rifleBeat:.16,rifleSpeed:4.7,cap:82},
  hard:{tell:1.00,recover:1.00,space:1.7,width:20,sweep:65,live:1.75,pellets:20,rings:2,gap:1.24,shot:2.30,missiles:5,volleys:2,rifleRounds:10,rifleBeat:.15,rifleSpeed:4.9,cap:98},
  furious:{tell:.90,recover:.90,space:1.5,width:22,sweep:74,live:1.90,pellets:24,rings:3,gap:1.12,shot:2.50,missiles:5,volleys:3,rifleRounds:12,rifleBeat:.14,rifleSpeed:5.1,cap:112}
 },
 families:{
  5:{s5frigate:['sweep','charge'],s5station:['charge','sweep'],s5gravity:['ring'],s5satellite:['missile']},
  7:{s7skimmer:['sweep'],mm1003_hexpyre:['ring'],mm1003_impharrow:['missile'],mm1003_riflelocust:['rifle']},
  8:{s8solar:['sweep','charge'],s8deathorb:['ring'],s8hunter:['missile'],mm1003_hexpyre:['ring'],mm1003_furnacemaw:['missile']},
  9:{s9gunship:['sweep','charge'],s9prism:['charge','ring'],s9ring:['ring'],s9beacon:['shards'],horizon:['sweep'],dreadv:['ring','charge']}
 }};
function ep13Profile(){return EP13.profiles[diffKey==='insanity'?'furious':diffKey]||EP13.profiles.normal;}
function ep13Log(event,e,data={}){EP13.events.push({event,stage:run.stage,type:e?.type,time:EP13.clock,...data});if(EP13.events.length>160)EP13.events.shift();}
function ep13Blocked(){return state!==GS.PLAY||bossActive||subBossActive||warnT>0||!!story||!!debugFight||!seatList().some(s=>{const p=seatShip(s);return p&&!p.dead&&!p.out;})||!!wfx?.fseq;}
function ep13Alive(e){return !!e&&!e.dead&&e._dyingT==null&&e.hp>0;}
function ep13Suppressed(e){return !!(e&&(e._eshStun||e._shieldStun>0||e._frozen||e._mercuryLock>0));}
function ep13Disarmed(e){return e._mm1003&&((e._ep13?.kind!=='rifle'&&e._ep13?.partId&&e._mm1003.parts.find(p=>p.id===e._ep13.partId)?.dead)||(typeof mm1003Disarmed==='function'&&mm1003Disarmed(e)));}
function ep13Muzzle(e){
 if(e._s9void==='s9beacon')return s9vHardpoint(e,0,.28);
 if(e._mm1003){const p=e._mm1003.parts.find(p=>!p.dead&&(e._ep13?.partId?p.id===e._ep13.partId:p.kind==='gun'||p.kind==='arm'));if(p){const m=mm1003Pose(e,p);return {x:m.mx,y:m.my};}}
 return typeof combatHardpoint==='function'?combatHardpoint(e,0,.34):{x:e.x,y:e.y+(e.h||50)*.34};
}
function ep13Cancel(e,reason){if(!e?._ep13)return;ep13Log('end',e,{reason});e._noSep=e._ep13.oldNoSep;e.shoots=e._ep13.oldShoots;e._ep13=null;e._ep13Next=EP13.clock+8;EP13.next=EP13.clock+ep13Profile().space;if(EP13.owner===e)EP13.owner=null;
 e._fcd=Math.max(e._fcd||0,.9);e._s9fire=Math.max(e._s9fire||0,.9);if(e._mm1003){e._mm1003.cd=Math.max(e._mm1003.cd||0,.9);e._mm1003.cycles++;}}
function ep13Warm(){for(let i=0;i<5;i++)XART.rdy('laserbeam_'+i);for(let i=0;i<8;i++){XART.rdy('nchg_orb_'+i);XART.rdy('warpprismshard_'+i);XART.rdy('warpcrystalimpact_'+i);}for(let i=0;i<4;i++)XART.rdy('weapon_muzzle_rotary_'+i);}
function ep13ReadyArt(){return XART.rdy('laserbeam_0')&&XART.rdy('nchg_orb_0');}
function ep13Start(e,kind){
 // Weapon identity is also enforced for the live encyclopedia/direct preview API.
 if(e._mutator1003==='riflelocust')kind='rifle';else if(e._s9void==='s9beacon')kind='shards';
 const P=ep13Profile(),m=ep13Muzzle(e),T=targetShip(e.x,e.y),L=camLeftX(),R=camRightX(),margin=Math.max(72,(e.w||50)*.60),x=clamp(e.x,L+margin,R-margin);
 const dir=x>(L+R)/2?-1:1,end=clamp(x+dir*P.sweep*P.live,L+margin,R-margin),angle=clamp(Math.atan2(T.y-m.y,T.x-m.x),.55,Math.PI-.55);
 e._ep13={id:++EP13.serial,kind,t:0,phase:'tell',beat:0,x,y:e.y,end,angle,gap:angle,muzzleOffset:m.x-e.x,profile:P,stage:run.stage,oldNoSep:e._noSep,oldShoots:e.shoots,partId:e._mm1003?.parts.find(p=>!p.dead&&(p.kind==='gun'||p.kind==='arm'))?.id};
 if(e._mm1003)e._mm1003.target={x:T.x,y:T.y};
 if(kind==='rifle')e._ep13.guns=e._mm1003.parts.filter(p=>p.kind==='gun'&&!p.dead).map(p=>{const m=mm1003Pose(e,p);return {id:p.id,angle:Math.atan2(T.y-m.my,T.x-m.mx)};});
 e._ep13Cycles=(e._ep13Cycles||0)+1;e.x=x;e.shoots=false;e._noSep=true;EP13.owner=e;
 ep13Log('start',e,{kind,warning:P.tell,gapRadians:P.gap});if(kind!=='rifle'&&kind!=='shards')(Audio.SFX.bossWeaponCharge||Audio.SFX.furnaceLaserCharge||Audio.SFX.laserCharge)?.();
}
function ep13CanStart(e){
 const types=EP13.families[run.stage];if(!types?.[e.type]||EP13.owner||EP13.clock<EP13.next||EP13.clock<(e._ep13Next||0)||e._ep13Cycles>=2)return false;
 if(!ep13Alive(e)||ep13Blocked()||ep13Suppressed(e)||ep13Disarmed(e)||e._vp12||e._cp12||e._mini||e._amini||e.boss||e._boss||e.ground||e._environmentBody)return false;
 if(e._mm1003&&!['rest'].includes(e._mm1003.phase))return false;
 if(e._s8Act||e._s8Roll||e._barrelT>0||e._beamT>0||(typeof eb11Queue==='function'&&eb11Queue(e)))return false;
 const P=ep13Profile(),T=targetShip(e.x,e.y);if(eBullets.length>P.cap-30||!T||T.dead||T.y-e.y<140||e.y<PLAY.y+30||e.y>PLAY.y+PLAY.h*.44)return false;
 if(e.x<camLeftX()+Math.max(62,e.w*.55)||e.x>camRightX()-Math.max(62,e.w*.55))return false;
 if(typeof eb11Ready==='function'&&!eb11Ready(e))return false;
 return ep13ReadyArt()&&(e._s9void!=='s9beacon'||XART.rdy('warpprismshard_0')&&XART.rdy('warpcrystalimpact_0'));
}
function ep13Shot(e,a,kind,speed,ordinal){const m=ep13Muzzle(e),b=eShootT(m.x,m.y,a,speed,kind,{w:kind==='emissile'?10:8,h:kind==='emissile'?18:8,szMul:kind==='emissile'?1:.5,owner:e,silent:ordinal>0});if(b&&!b.dead){b._ep13=true;b._ep13Owner=e._ep13.id;b._ep13Angle=a;}return b;}
function ep13RingAngles(q){const P=q.profile,angles=[];for(let i=0;i<P.pellets;i++){const a=TAU*i/P.pellets+(q.beat%2)*Math.PI/P.pellets,d=Math.atan2(Math.sin(a-q.gap),Math.cos(a-q.gap));if(Math.abs(d)>P.gap*.5)angles.push(a);}return angles;}
function ep13Emit(e){const q=e._ep13,P=q.profile;if(eBullets.length>=P.cap)return;
 if(q.kind==='ring'||q.kind==='shards'){const kind=q.kind==='shards'?'warpshard':run.stage===5?'s5split':run.stage===7?'blob':run.stage===8?'s8pair':'photon';const angles=ep13RingAngles(q);if(eBullets.length+angles.length>P.cap)return;angles.forEach((a,i)=>ep13Shot(e,a,kind,P.shot*(1-q.beat*.08),i));ep13Log(q.kind,e,{count:angles.length,gap:q.gap,gapRadians:P.gap});}
 else if(q.kind==='missile'){if(eBullets.length+P.missiles>P.cap)return;for(let i=0;i<P.missiles;i++)ep13Shot(e,q.angle+(i-(P.missiles-1)/2)*.22,'emissile',P.shot+1,i);ep13Log('missile',e,{count:P.missiles,angle:q.angle});}
 else if(q.kind==='rifle'){
  const guns=q.guns.filter(g=>!e._mm1003.parts.find(p=>p.id===g.id)?.dead),g=guns[q.beat%Math.max(1,guns.length)];if(!g)return;
  const p=e._mm1003.parts.find(p=>p.id===g.id),m=mm1003Pose(e,p),first=eBullets.length;
  if(mm1003Shot(e,m.mx,m.my,g.angle,P.rifleSpeed,'rifle')){p.recoil=3;r30Sound('enemyMG');for(let i=first;i<eBullets.length;i++)Object.assign(eBullets[i],{_ep13:true,_ep13Owner:q.id,_ep13Angle:g.angle,_ep13Gun:p.id});ep13Log('rifle',e,{gun:p.id,angle:g.angle});}
 }
}
function ep13Beam(e){const q=e?._ep13;if(!q||q.phase!=='fire'||!['sweep','charge'].includes(q.kind)||!ep13Alive(e)||ep13Suppressed(e)||ep13Disarmed(e))return null;
 const P=q.profile,u=clamp((q.t-P.tell)/P.live,0,1),m=ep13Muzzle(e),edge=Math.min(1,u/.10,(1-u)/.16);
 return {x:m.x,y:m.y,a:q.kind==='sweep'?Math.PI/2:q.angle,width:P.width*Math.max(0,edge),len:PLAY.h+160,active:u>.10&&u<.84};
}
function ep13BeamTouches(b,p){const dx=p.x-b.x,dy=p.y-b.y,along=dx*Math.cos(b.a)+dy*Math.sin(b.a),across=Math.abs(-dx*Math.sin(b.a)+dy*Math.cos(b.a));return b.active&&along>=20&&along<=b.len&&across<b.width*.5+Math.min(8,p._hx||8);}
function ep13Tick(e,dt){
 if(!e._ep13&&ep13CanStart(e)){const kinds=EP13.families[run.stage][e.type];ep13Start(e,kinds[(e._ep13Cycles||0)%kinds.length]);}
 const q=e._ep13;if(!q)return false;
 if(!ep13Alive(e)||ep13Blocked()||q.stage!==run.stage||ep13Disarmed(e)||ep13Suppressed(e)){ep13Cancel(e,'interrupted');return false;}
 const P=q.profile;q.t+=dt;e.shoots=false;e.vx=e.vy=0;e.spin=e._bank=0;if(e._ai27)e._ai27.dx=0;
 if(e._mm1003){e._mm1003.t+=dt;for(const p of e._mm1003.parts){p.recoil=Math.max(0,p.recoil-dt*26);p.flash=Math.max(0,(p.flash||0)-dt);}}
 if(q.kind==='sweep')e.x=lerp(q.x,q.end,clamp((q.t-P.tell)/P.live,0,1));else e.x=q.x;e.y=q.y;
 if(q.t<P.tell){q.phase='tell';combatWarningTick(e,'ep13-'+q.id,q.t,P.tell);return true;}
 if(q.phase==='tell'){q.phase='fire';ep13Log('release',e,{kind:q.kind,angle:q.angle});if(['sweep','charge'].includes(q.kind))(Audio.SFX.enemyHeavyLaser||Audio.SFX.laserBeamStart)?.();}
 const shots=q.kind==='rifle'?P.rifleRounds:['ring','shards'].includes(q.kind)?P.rings:P.volleys,interval=q.kind==='rifle'?P.rifleBeat:.38,fireTime=['sweep','charge'].includes(q.kind)?P.live:(shots-1)*interval+.24;
 if(q.t<P.tell+fireTime){q.phase='fire';if(['ring','missile','shards','rifle'].includes(q.kind)&&q.beat<shots&&q.t>=P.tell+q.beat*interval){ep13Emit(e);q.beat++;}return true;}
 q.phase='recover';if(q.t>=P.tell+fireTime+P.recover)ep13Cancel(e,'recovered');return true;
}
let ep13NativeOwner=null;
// Reuse the actual violet crystal reel, with its authored base at the emitter.
WM26_REELS.crystal={key:'warpcrystalimpact_',n:8,size:30,pivot:.88,up:true};
function ep13CrystalMuzzle(e,angle){const m=ep13Muzzle(e);return wm26Emit(e,m.x,m.y,angle,'crystal',null,{size:30,life:.18,follow:()=>ep13Alive(e)&&!ep13Suppressed(e)?{...ep13Muzzle(e),angle}:null});}
const EP13_SHOT=eShootT;eShootT=function(x,y,a,speed,kind,options){
 const owner=options?.owner||ep13NativeOwner;
 if(owner?._s9void!=='s9beacon')return EP13_SHOT.apply(this,arguments);
 // Native queued Beacon rings use the same physical shards as its new pulses.
 const b=EP13_SHOT.call(this,x,y,a,speed,'warpshard',{...options,w:8,h:24,szMul:1,noMuzzle:true,silent:true,owner});
 if(b&&!b.dead){b._s9a='warpshard';b._noArsenal=true;b._ep13Crystal=true;ep13CrystalMuzzle(owner,owner._ep13?.gap??Math.PI/2);if(!options?.silent)enemyShotSfx('s9warp');}
 return b;
};
const EP13_S9_MUZZLE=s9vMuzzle;s9vMuzzle=function(e){if(e?._s9void==='s9beacon')return ep13CrystalMuzzle(e,Math.PI/2);return EP13_S9_MUZZLE.apply(this,arguments);};
const EP13_MM_SHOT=mm1003Shot;mm1003Shot=function(e,x,y,a,speed,kind){
 const first=eBullets.length,result=EP13_MM_SHOT.apply(this,arguments);if(!result||kind!=='rifle'||e?._mutator1003!=='riflelocust')return result;
 let gun=null,dist=Infinity;for(const p of e._mm1003.parts){if(p.dead||p.kind!=='gun')continue;const m=mm1003Pose(e,p),d=Math.hypot(x-m.mx,y-m.my);if(d<dist){dist=d;gun=p;}}
 if(gun){for(let i=first;i<eBullets.length;i++)eBullets[i]._ep13Gun=gun.id;
  wm26Emit(e,x,y,a,'mg',null,{size:26,life:.12,follow:()=>{if(!ep13Alive(e)||ep13Suppressed(e)||gun.dead)return null;const m=mm1003Pose(e,gun);return {x:m.mx,y:m.my,angle:a};}});
 }return result;
};
function ep13Controller(base){return function(e,dt){if(ep13Tick(e,dt))return;const previous=ep13NativeOwner;ep13NativeOwner=e;try{return base.apply(this,arguments);}finally{ep13NativeOwner=previous;}};}
s5SpaceTick=ep13Controller(s5SpaceTick);s7ToxicTick=ep13Controller(s7ToxicTick);s8MegaTick=ep13Controller(s8MegaTick);
s9VoidTick=ep13Controller(s9VoidTick);s9ChaosTick=ep13Controller(s9ChaosTick);mm1003Tick=ep13Controller(mm1003Tick);
const EP13_END=ai27End;ai27End=function(e,previous){if(e?._ep13&&e._ai27)e._ai27.dx=0;return EP13_END.apply(this,arguments);};
const EP13_BEGIN=beginStage;beginStage=function(n){if(EP13.owner)ep13Cancel(EP13.owner,'stage');EP13.clock=0;EP13.next=1;EP13.stage=n;EP13.owner=null;const r=EP13_BEGIN.apply(this,arguments);if(EP13.families[n])ep13Warm();return r;};
const EP13_PLAY=updatePlay;updatePlay=function(dt){if(!ep13Blocked())EP13.clock+=dt;const r=EP13_PLAY.apply(this,arguments),e=EP13.owner;
 if(e&&(!ep13Alive(e)||ep13Blocked()||ep13Suppressed(e)||!enemies.includes(e)))ep13Cancel(e,'owner-left');
 ep13HitSeats();return r;
};
function ep13HitSeats(){const beam=ep13Beam(EP13.owner);if(beam){for(const s of seatList())withSeat(s,()=>{if(!player.dead&&player.invuln<=0&&ep13BeamTouches(beam,player))playerHit();});}}
function ep13Draw(e){const q=e._ep13;if(!q||!ep13Alive(e))return;const P=q.profile,m=ep13Muzzle(e);
 if(q.phase==='tell'){
  const progress=clamp(q.t/P.tell,0,1),args={x:m.x,y:m.y,progress,width:P.width+10};
  if(q.kind==='sweep'){
   // This is the whole traversed corridor, including the moving muzzle offset.
   const mid=(q.x+q.end)/2+q.muzzleOffset,w=Math.abs(q.end-q.x)+P.width*2.8;
   combatWarningDraw(e,{...args,x:mid,ex:mid,ey:PLAY.y+PLAY.h+30,width:w,fieldOnly:true});
   combatWarningDraw(e,{...args,ex:m.x,ey:PLAY.y+PLAY.h,alertOnly:true});
  }else if(q.kind==='ring'||q.kind==='shards'){
   for(const a of ep13RingAngles(q))combatWarningDraw(e,{...args,ex:m.x+Math.cos(a)*620,ey:m.y+Math.sin(a)*620,width:9,fieldOnly:true,alpha:.32});
   combatWarningDraw(e,{...args,ex:m.x,ey:m.y+620,alertOnly:true});
  }else if(q.kind==='rifle'){
   q.guns.forEach((g,i)=>{const p=e._mm1003.parts.find(p=>p.id===g.id);if(!p||p.dead)return;const m=mm1003Pose(e,p);combatWarningDraw(e,{...args,x:m.mx,y:m.my,ex:m.mx+Math.cos(g.angle)*620,ey:m.my+Math.sin(g.angle)*620,width:10,fieldOnly:i>0});});
  }else{const angles=q.kind==='missile'?Array.from({length:P.missiles},(_,i)=>q.angle+(i-(P.missiles-1)/2)*.22):[q.angle];angles.forEach((a,i)=>combatWarningDraw(e,{...args,ex:m.x+Math.cos(a)*620,ey:m.y+Math.sin(a)*620,fieldOnly:i>0,width:q.kind==='missile'?14:P.width+10}));}
  if(q.kind==='shards'){ctx.save();ctx.globalAlpha=.40+progress*.5;wm26Draw(ctx,'crystal',m.x,m.y,q.gap,(q.t*5)%1,12+progress*14,null);ctx.restore();}
  else if(q.kind!=='rifle'){const key='nchg_orb_'+Math.floor(q.t*16)%8;if(XART.rdy(key)){const im=XART.get(key),size=18+progress*24;ctx.save();ctx.globalCompositeOperation='lighter';ctx.drawImage(im,m.x-size/2,m.y-size/2,size,size);ctx.restore();}}
 }
 const b=ep13Beam(e);if(b&&b.width>0){let key='laserbeam_'+Math.floor(q.t*22)%5;if(!XART.rdy(key))key='laserbeam_0';if(XART.rdy(key)){const visualWidth=b.width*2.8;ctx.save();ctx.translate(b.x,b.y);ctx.rotate(b.a-Math.PI/2);ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.95;ctx.drawImage(XART.get(key),-visualWidth/2,0,visualWidth,b.len);ctx.restore();}}
}
const EP13_DRAW=drawEnemy;drawEnemy=function(e){const r=EP13_DRAW.apply(this,arguments);ep13Draw(e);return r;};
window.BOF_ENEMY_PATTERNS={director:EP13,start:ep13Start,tick:ep13Tick,beam:ep13Beam,touches:ep13BeamTouches,angles:ep13RingAngles};
