"use strict";
/* Physical weapons pass: the authored barrel mouths own release and flash.
   Native HP/modules, ground traffic, locks, ordinary bullet and missile rules
   remain authoritative. Shared MG/missile emplacement fixes cover all biomes. */
const S1B={base:{spawn:spawnEnemy,naval:navalTick,tank:tankTick,draw:drawEnemy,
 tankDraw:drawModularTank,groundTick:modularGroundTurretTick,groundDraw:drawModularGroundTurret,
 shot:eShootT,truckTick:mt18Tick,projectile:drawCombatFinalProjectile,plan:buildStagePlan,load:stageLoadBegin,mod:modularTankTick,route:eb11OwnsRoute},events:[],truck:null};
for(const a of Object.values(S1B_ART)){XART._src[a.key]=a.path;XART.rdy(a.key);}
function s1bAlive(e){return !!e&&!e.dead&&e._dyingT==null;}
function s1bLand(e){return run.stage===1&&s1bAlive(e)&&/^s1tank(?:apc|light)(?:_b)?$/.test(rosterKey(e.type));}
function s1bLight(e){return /^s1tanklight(?:_b)?$/.test(rosterKey(e.type));}
function s1bRank(){return diffKey==='furious'||diffKey==='insanity'?2:diffKey==='hard'?1:0;}
// Moving ground vehicles already own terrain-relative motion and reservations.
// The generic nine-second aircraft exit push must not displace that chassis.
eb11OwnsRoute=function(e){return groundTrafficVehicle(e)||S1B.base.route.apply(this,arguments);};
function s1bLog(event,e,extra={}){S1B.events.push({event,type:e.type,at:efxClock,...extra});if(S1B.events.length>500)S1B.events.shift();}
function s1bBlit(name,f,angle,x,y,size,tint){const a=S1B_ART[name];if(!a||!XART.rdy(a.key))return false;
 const im=tint?xartTint(a.key,tint,tint==='#ffffff'?1:.55):XART.get(a.key),d=s1aDir(angle,a.dirs),s=size||a.cell;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,d*a.cell,clamp(f|0,0,a.frames-1)*a.cell,a.cell,a.cell,x-s/2,y-s/2,s,s);ctx.restore();return true;}
function s1bFlash(e,p,rocket=false,size=40){s1aFlash(e,p(),rocket?'rocket_muzzle':'muzzle',size,()=>s1bAlive(e)?p():null);}
function s1bPair(e,points,kind,speed,gray=false,rocket=false){let fired=false;
 for(let side=0;side<points.length;side++){const follow=points[side],p=follow(),b=s1aRound(e,p,speed,kind,{silent:true});if(!b||b.dead)continue;
  if(gray)b._s1bGray=true;if(rocket){b._s1bRackRocket=true;b._noArsenal=true;}
  fired=true;s1bFlash(e,follow,rocket,rocket?44:38);
 }
 if(fired){if(rocket)enemyShotSfx('s1jungleMissile');else Audio.SFX.enemyMachineGunHeavy?.();s1bLog(rocket?'missile-pair':'mg-pair',e);}
 return fired;
}
spawnEnemy=function(type,x,y,options){
 const light=/^s1tanklight(?:_b)?$/.test(rosterKey(type));if(run.stage===1&&light&&!['hard','furious'].includes(diffKey))return null;
 const e=S1B.base.spawn.apply(this,arguments);if(!e||run.stage!==1)return e;
 if(light){e._s1bGray=true;e._blk=true;e._atk='mg';}
 if(s1bLand(e)||['s1boatpatrol','s1corvette','s1jetdelta_b'].includes(e.type))e.t=0;
 return e;
};
// Core/bow turret is part of the whole patrol plate; the two existing side
// modules retain their own native damage pools and disappear from the attack
// sequence when destroyed. Source coordinates are measured on128px frames.
function s1bPatrolMuzzle(e,m,side=0){
 if(m){const p=furyBoatPoint(e,m);return{x:p.x,y:p.y+30*(99-64)/128,angle:Math.PI/2};}
 const size=Math.max(e.w,e.h)*1.10;return{x:e.x+side*3*size/128,y:e.y+(e._navBob||0)+(100-64)*size/128,angle:Math.PI/2};
}
function s1bCorvetteMuzzle(e){const k=(e._drawW||((e._bodyW||e.w)*(e._foot??ENEMY_ART_FOOT)))/145;
 return{x:e.x,y:e.y+(e._navBob||0)+(200-114)*k,angle:Math.PI/2};}
navalTick=function(e,dt){
 if(run.stage!==1||!s1bAlive(e)||!['s1boatpatrol','s1corvette'].includes(e.type))return S1B.base.naval.apply(this,arguments);
 // Run native water/steering/module owners while the new attack book owns its
 // own clocks. Prevent the old broadside/2-module MG route firing underneath.
 const saved={burst:e._burst,burstCd:e._burstCd,shot:e._shotCd,idle:e._idle};
 e._burst=0;e._burstCd=e._shotCd=e._idle=1e6;e._s1rTell=null;
 try{S1B.base.naval.call(this,e,dt);}finally{e._burst=saved.burst;e._burstCd=saved.burstCd;e._shotCd=saved.shot;e._idle=saved.idle;}
 e._s1rTell=null;e._navLean=0;e._navPulse=0;
 if(e._beached)return;for(const m of furyBoatModules(e)||[])m.aim=2;
 const A=e._s1bNavy||(e._s1bNavy={mode:'wait',cd:.6,step:0,round:0}),rank=s1bRank(),T=targetShip(e.x,e.y);
 if(A.module&&A.module.hp<=0&&A.mode!=='wait'){A.mode='wait';A.cd=.2;return;}
 A.cd-=dt;if(A.cd>0)return;
 if(A.mode==='wait'){
  if(e.y<viewTopY()+25||T.y<e.y+65)return;
  const modules=furyBoatModules(e)||[];A.module=e.type==='s1boatpatrol'&&A.step%2===0?modules[A.step%4===0?0:1]:null;
  A.step++;if(A.module&&A.module.hp<=0){A.cd=.12;return;}
  A.mode='tell';A.t=0;A.dur=.66;A.round=0;A.target={x:T.x,y:T.y};
 }
 if(A.mode==='tell'){
  A.t+=dt;A.cd=0;combatWarningTick(e,'s1b-navy',A.t,A.dur);if(A.t<A.dur)return;
  A.mode='fire';s1bLog(A.module?'side-spread':'main-burst',e,{side:A.module?.side||0});
 }
 if(A.mode==='fire'){
  if(A.module&&A.module.hp<=0){A.mode='wait';A.cd=.2;return;}
  if(A.module){const p=s1bPatrolMuzzle(e,A.module);let any=false;
   for(const off of [-.22,0,.22]){const b=s1aRound(e,{...p,angle:p.angle+off},4.4,'s1bullet',{silent:true});any=any||!!b&&!b.dead;}
   if(any){Audio.SFX.enemyMachineGunHeavy?.();s1bFlash(e,()=>s1bPatrolMuzzle(e,A.module));}A.mode='wait';A.cd=.50;
  }else{
   const corvette=e.type==='s1corvette',p=corvette?s1bCorvetteMuzzle(e):s1bPatrolMuzzle(e,null,A.round%2?-1:1),b=s1aRound(e,p,corvette?4.8:5.0,'s1bullet',{silent:true});
   if(b&&!b.dead){Audio.SFX.enemyMachineGunHeavy?.();const side=A.round%2?-1:1;s1bFlash(e,()=>corvette?s1bCorvetteMuzzle(e):s1bPatrolMuzzle(e,null,side),false,corvette?42:38);}
   A.round++;A.cd=turretInterval15(corvette?.17:.11);if(A.round>=(corvette?4:9)){A.mode='wait';A.cd=turretInterval15(corvette?1.8:.72,corvette?[1.8,1.5,1.2][rank]:.72);}
  }
 }
};
function s1bGroundHead(e){return s1aPoseAngle(e._modTurret.angle,64);}
function s1bGroundMuzzle(e,side){const T=e._modTurret,angle=s1bGroundHead(e),a=angle-Math.PI/2,c=Math.cos(a),s=Math.sin(a),k=e.w*.96/256;
 const x=(T.weapon==='mg'?(side<0?92:163):(side<0?73:182))-128,y=(T.weapon==='mg'?218:196)-128;
 return{x:e.x+(x*c-y*s)*k,y:e.y+(x*s+y*c)*k,angle};}
modularGroundTurretTick=function(e,dt){
 const T=e?._modTurret;if(!T||!['mg','missile'].includes(T.weapon)||!s1bAlive(e))return S1B.base.groundTick.apply(this,arguments);
 e._s1bTurret=true;const target=targetShip(e.x,e.y),want=Math.atan2(target.y-e.y,target.x-e.x);
 if(T.mode==='wait')T.angle+=clamp(s1aAngle(want-T.angle),-dt*turretSpeed15(2.8),dt*turretSpeed15(2.8));
 if(e.y<32||e.y>VH-44||bossActive||subBossActive)return;T.timer-=dt;
 if(T.mode==='tell'){
  if(T.weapon==='missile')return;T._s1bTell+=dt;combatWarningTick(e,'s1b-emplacement',T._s1bTell,.65);
 }
 if(T.timer>0)return;
 if(T.mode==='wait'){
  T.mode='tell';T.timer=.65;T._s1bTell=0;T.target={x:target.x,y:target.y};
  if(T.weapon==='missile'){const lock=enemyLockOn(e,.72,{fire:()=>{if(!s1bAlive(e))return;T.mode='burst';T.timer=0;T.shots=1;}});if(!lock){T.mode='wait';T.timer=.3;}}
  return;
 }
 if(T.mode==='tell'){T.mode='burst';T.shots=6;T.timer=0;}
 if(T.mode==='burst'){
  const rocket=T.weapon==='missile';s1bPair(e,[-1,1].map(side=>()=>s1bGroundMuzzle(e,side)),rocket?'s1jungleMissile':'s1bullet',rocket?3.2:4.8,false,rocket);
  T.shots--;T.timer=turretInterval15(.11);if(T.shots<=0){T.mode='wait';T.timer=turretInterval15(rocket?3:1.75);}
 }
};
drawModularGroundTurret=function(e){
 const T=e?._modTurret;if(!T||!['mg','missile'].includes(T.weapon)||!s1bAlive(e))return S1B.base.groundDraw.apply(this,arguments);
 const bk='overhaul_ground_base_'+T.stage;if(!XART.rdy(bk))return false;const size=e.w*1.27,tint=tintColor(e),im=tint?xartTint(bk,tint,tint==='#ffffff'?1:.55):XART.get(bk);
 ctx.drawImage(im,e.x-size/2,e.y-size/2,size,size);s1bBlit('head_'+T.weapon,0,s1bGroundHead(e),e.x,e.y,e.w*.96,tint);
 if(T.mode==='tell'&&T.weapon==='mg'){const m=s1bGroundMuzzle(e,0);combatWarningDraw(e,{x:m.x,y:m.y,ex:T.target.x,ey:T.target.y,progress:T._s1bTell/.65,width:27});}
 return true;
};
tankTick=function(e,dt){
 if(!s1bLand(e))return S1B.base.tank.apply(this,arguments);
 tankMotionTick(e,dt,TANK_SPD);e.shoots=false;e.fk=null;e._atk='mg';
 const A=e._s1bMG||(e._s1bMG={cd:.75,left:0}),light=s1bLight(e),rank=s1bRank(),T=targetShip(e.x,e.y);A.cd-=dt;
 if(A.cd>0||e.y<viewTopY()+35||e.y>VH-95||T.y<e.y+65||!eb11Ready(e))return;
 if(A.left<=0)A.left=light?8:5;
 s1bPair(e,[-1,1].map(side=>()=>s1aTankMuzzle(e,side)),'s1bullet',light?5.3+rank*.2:4.8,light);
 e._recoil=.08;A.left--;A.cd=A.left>0?(light?[.11,.09,.065][rank]:.16):(light?[1,.8,.6][rank]:[1.85,1.4,1.15][rank]);
};
drawModularTank=function(e){
 if(!s1bLand(e))return S1B.base.tankDraw.apply(this,arguments);
 const tint=tintColor(e),size=e.w*1.05,f=Math.floor((e._wheelT||0)*2)%8;
 if(s1bLight(e)){s1bBlit('gray_hull',f,Math.PI/2,e.x,e.y,size,tint);s1bBlit('gray_turret',0,s1aTankHead(e),e.x,e.y,size,tint);}
 else {const key=S1M_ART.hull[f].key;if(!XART.rdy(key))return false;const im=tint?xartTint(key,tint,tint==='#ffffff'?1:.55):XART.get(key);ctx.drawImage(im,e.x-size/2,e.y-size/2,size,size);s1aBlit('tank_turret',0,s1aTankHead(e),e.x,e.y,size,tint);}
 e._drawW=e._drawH=size;return true;
};
mt18Tick=function(e,dt){const old=S1B.truck;S1B.truck=e;try{return S1B.base.truckTick.apply(this,arguments);}finally{S1B.truck=old;}};
eShootT=function(x,y,angle,speed,kind,opts){const b=S1B.base.shot.apply(this,arguments);if(b&&S1B.truck&&kind==='s1jungleMissile'){
 b._s1bRackRocket=true;s1aLog('shot',S1B.truck,{kind,x,y,angle});
 }return b;};
// MT18 assigns its missile tag after eShootT returns. Its projectile owner is
// therefore identified at native draw time as well; no body/HP/launcher changes.
drawCombatFinalProjectile=function(b){
 if(b?._s1bRackRocket||b?._mt18Missile)return s1bBlit('rack_rocket',Math.floor((b.t||0)*22)%4,Math.atan2(b.vy,b.vx),b.x,b.y,64);
 if(b?._s1bGray)return s1bBlit('gray_slug',Math.floor((b.t||0)*24)%4,Math.atan2(b.vy,b.vx),b.x,b.y,64);
 return S1B.base.projectile.apply(this,arguments);
};
drawEnemy=function(e){const r=S1B.base.draw.apply(this,arguments),A=e?._s1bNavy;
 if(run.stage===1&&s1bAlive(e)&&A?.mode==='tell'){const m=e.type==='s1corvette'?s1bCorvetteMuzzle(e):s1bPatrolMuzzle(e,A.module);combatWarningDraw(e,{x:m.x,y:m.y,ex:m.x,ey:Math.max(m.y+300,A.target.y),progress:A.t/A.dur,width:A.module?58:38});}
 return r;
};
buildStagePlan=function(n){const plan=S1B.base.plan.apply(this,arguments);if(n!==1||!['hard','furious'].includes(diffKey))return plan;
 const times=s1bRank()===2?[28,35,42,49,56,63,70,77]:[32,44,56,68,77];
 times.forEach((t,i)=>{const fn=()=>{
  if(bossActive||subBossActive||stageEnding)return;
  // Match the native coast gate as well as traffic legality. A distant strip
  // of shoreline can pass a terrain mask while the live playfield is at sea.
  if(((_levelCfg(1)?.h||4212)-(mapScroll||0))>S1_COAST-60){if(waveIdx>0)waveIdx--;_waveGap=.25;return;}
  const y=viewTopY()-92,W=worldWidth(),prefer=(i%2?.72:.28)*W;let x=null;
  for(let d=0;d<230&&x==null;d+=14)for(const side of d?[-1,1]:[1]){const q=clamp(prefer+d*side,65,W-65);if(groundTrafficLegal({w:88,h:88,_drawW:93,_drawH:93},q,y)){x=q;break;}}
  if(x==null){
   // Optional reinforcements cannot enter once the dam has exhausted the
   // terrain. Retrying that impossible entry forever blocks authored waves.
   if(mapScroll>=levelScrollRange()-1){s1bLog('reinforcement-retired',{type:'s1tanklight'},{planned:t,reason:'no legal ground entry at map end'});return;}
   if(waveIdx>0)waveIdx--;_waveGap=.25;return;
  }
  spawnEnemy('s1tanklight',x,y,{_s1bReinforcement:true});
 };fn._s1Ground=true;fn._s1Pressure=1;fn._s1bCamo=true;plan.push({t,fn});});plan.sort((a,b)=>a.t-b.t);return plan;
};
stageLoadBegin=function(n,keys){return S1B.base.load.call(this,n,[...(keys||[]),...Object.values(S1B_ART).filter(a=>n===1||/head_/.test(a.key)).map(a=>a.key),...['green','yellow','red'].map(c=>'bmfx_fov_'+c+'_tall')]);};
