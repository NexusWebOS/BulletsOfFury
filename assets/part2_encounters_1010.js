"use strict";
/* Part-two footage: physical emitters, committed warnings and recovery. Keep
   the authored modular plates, HP pools, shield nodes and target geometry. */
const P2E={base:{book:er26Book,set:er26Set,combat:er26Combat,war:er26WarTick,core:er26CoreTick,
 draw:er26Draw,space:s5SpaceTick,enemy:drawEnemy,partDraw:av3PartDraw,partTick:er26Tick},events:[]};
function p2eLog(event,data={}){P2E.events.push({event,...data});if(P2E.events.length>160)P2E.events.shift();}
function p2eLive(b,slots){return slots.filter(s=>mr27CanFire(b,s));}
function p2eFrostBare(b){return b?._ship==='frostcruiser'&&b._mr27&&!p2eLive(b,['L','R']).length;}
er26Book=function(b){
 if(p2eFrostBare(b))return ['p2-core-balls','p2-core-laser','p2-core-charge'];
 if(b._ship==='olivewarden')return p2eLive(b,['L','R']).length?
  ['p2-battery','p2-rockets','p2-core-laser','p2-charge']:['p2-core-laser','p2-rockets','p2-charge'];
 if(b._ship==='stormsovereign')return ['p2-battery','p2-rockets','ap10-stormburst','p2-core-balls'];
 return P2E.base.book.apply(this,arguments);
};
er26Set=function(b,mode){
 const r=P2E.base.set.apply(this,arguments),R=b._er26;if(!R)return r;
 if((b._ship==='stormsovereign'||b._ship==='olivewarden')&&mode==='recover'){
  R.dur=diffKey==='easy'?1.6:diffKey==='furious'?1.0:1.2;R.to={x:er26Station(b,0),y:R.home};}
 if(!mode.startsWith('p2-'))return r;
 R._p2={from:{x:b.x,y:b.y},aim:{x:player.x,y:player.y},locked:false,shot:0,wave:0};
 R.warm=diffKey==='easy'?1.55:diffKey==='furious'?1.05:1.25;
 R.live=mode.includes('laser')?1.10:mode.includes('charge')?2.0:1.7;R.dur=R.warm+R.live;
 R.beamStarted=false;R.warnings=[];b._ap10Storm=null;b._l23Beam=null;
 b._noHit=false;
 if(b._mr27)b._mr27.ram1002=null;
 p2eLog('attack',{ship:b._ship,mode,warm:R.warm});return r;
};
function p2eSlots(b,mode){
 if(mode==='p2-rockets')return p2eLive(b,['ROCKET_L','ROCKET_R']);
 if(mode==='p2-battery')return p2eLive(b,['L','R']);
 return mr27CanFire(b,'C')?['C']:[];
}
function p2eAttack(b,dt){
 const R=b._er26,A=R._p2,mode=R.mode;if(!A)return false;
 const n=R.level,core=shipBossMount(b,'C'),slots=p2eSlots(b,mode);R.warnings=[];
 // Sample during the tell, then lock for the final 0.45 seconds. A player can
 // leave that committed lane without a laser/bullet snapping back onto them.
 if(R.t<R.warm-.45)A.aim={x:player.x,y:player.y};else A.locked=true;
 if(mode.includes('charge')){
  if(R.t<R.warm){const a=Math.atan2(A.aim.y-b.y,A.aim.x-b.x);
   R.warnings.push({x:b.x,y:b.y,angle:a,width:b.w*.40,progress:R.t/R.warm,laneShape:'line'});
   combatWarningTick(b,'p2-ram-'+R.serial,R.t,R.warm);return true;}
  if(!A.drive){const tx=clamp(A.aim.x,camLeftX()+b.w*.38,camRightX()-b.w*.38),ty=Math.min(A.aim.y-36,VH*.70);
   A.drive={x:b.x,y:b.y,tx,ty};Audio.SFX.chargeDash?.();weaponFeedbackBurst('ram',b.x,b.y,88,.24,Math.atan2(ty-b.y,tx-b.x));}
  const D=A.drive,t=R.t-R.warm,u=clamp(t/.65,0,1),v=u*u*(3-2*u);
  if(t<.65){b.x=lerp(D.x,D.tx,v);b.y=lerp(D.y,D.ty,v);
   for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&player.invuln<=0&&Math.abs(player.x-b.x)<b.w*.28&&Math.abs(player.y-b.y)<b.h*.30)playerHit('Committed cruiser charge');});}
  else {const u=clamp((t-.65)/1.25,0,1),v=u*u*(3-2*u);b.x=lerp(D.tx,er26Station(b,0),v);b.y=lerp(D.ty,R.home,v);}
  b._drawY=b.y;return true;
 }
 b.x+=(er26Station(b,0)-b.x)*Math.min(1,dt*1.35);b.y+=(R.home-b.y)*Math.min(1,dt*2);b._drawY=b.y;
 if(!slots.length){er26Set(b,'p2-charge');return true;}
 if(mode==='p2-core-laser'){
  if(!R.beamStarted){const C=shipBossMount(b,'C'),a=Math.atan2(A.aim.y-C.y,A.aim.x-C.x);
   l23BossBeamStart(b,b._s3Nuclear&&R.form==='fire'?'inferno':'rime',['C'],[a],Math.max(1.3,R.warm),R.live,.25,b._ship==='stormsovereign'?29:24);
   R.beamStarted=true;R.warm=b._l23Beam.warm;R.dur=R.warm+R.live+.3;}
  l23BossBeamTick(b,dt);return true;
 }
 for(const slot of slots){const p=shipBossMount(b,slot),a=Math.atan2(A.aim.y-p.y,A.aim.x-p.x);
  if(R.t<R.warm)R.warnings.push({slot,angle:a,width:mode==='p2-rockets'?30:24,progress:R.t/R.warm});}
 if(R.t<R.warm){combatWarningTick(b,'p2-attack-'+R.serial,R.t,R.warm);return true;}
 A.shot-=dt;if(A.shot>0)return true;
 const slot=slots[A.wave%slots.length],p=shipBossMount(b,slot),a=Math.atan2(A.aim.y-p.y,A.aim.x-p.x);A.wave++;
 if(mode==='p2-battery'){
  if(A.wave>12)return true;const angle=a+(A.wave%5-2)*.025;
  mr27Fire(b,slot,angle);const tip=shipBossMount(b,slot),q=b._s4war?stage4WarfareShot(b,tip,angle,4.7+n*.25,'mg',{szMul:1.15}):eShootT(tip.x,tip.y,angle,5.0,'mg',{w:7,h:17});
  q._p2Emitter={ship:b._ship,slot,x:tip.x,y:tip.y};q.mg=true;q._shootable=false;q._weaponProof=true;
  shipBossMuzzleStart(b,[slot],{fam:'mg',life:.1,hpx:30});Audio.SFX.machineGun?.();A.shot=diffKey==='easy'?.19:.115;
 }else if(mode==='p2-rockets'){
  if(A.wave>3+n)return true;mr27Fire(b,slot,a);const tip=shipBossMount(b,slot),q=eShootT(tip.x,tip.y,a,5.2+n*.65,'emissile',{w:12,h:24,silent:true});
  Object.assign(q,{_p2Emitter:{ship:b._ship,slot,x:tip.x,y:tip.y},_shootable:true,_weaponProof:false,hp:2,homing:false,_boss:true,_noArsenal:true});
  shipBossMuzzleStart(b,[slot],{fam:'missile',life:.16,hpx:34});Audio.SFX.enemyMissile?.();A.shot=.43;
 }else{
  if(A.wave>3)return true;const fire=b._s3Nuclear&&R.form==='fire',storm=b._ship==='stormsovereign';
  for(const off of (n>0?[-.15,0,.15]:[0])){const q=er26Shot(b,'C',a+off,3.8+n*.35,{large:true});
   if(!q.dead){q._p2Emitter={ship:b._ship,slot:'C',x:core.x,y:core.y};q._er26Art=storm?'lightning':fire?'fire':'ice';q._ap10Lightning=storm;q._shootable=true;q._weaponProof=false;}}
  av3Sound('laser_release',.8);shipBossMuzzleStart(b,['C'],{fam:storm?'lightning':fire?'magma':'cryo',life:.18,hpx:48});A.shot=.48;
 }
 R.shots++;p2eLog('release',{ship:b._ship,mode,slot,x:p.x,y:p.y});return true;
}
er26Combat=function(b,dt){
 if(p2eFrostBare(b)&&!b._er26.mode.startsWith('p2-')&&b._er26.mode!=='overdrive')er26Set(b,'p2-core-balls');
 if(b._er26.mode.startsWith('p2-'))return p2eAttack(b,dt);
 return P2E.base.combat.apply(this,arguments);
};
er26WarTick=function(b,dt){
 if(!['olivewarden','stormsovereign'].includes(b._ship))return P2E.base.war.apply(this,arguments);
 if(b._ship==='stormsovereign'&&b._er26?.mode==='ap10-stormburst')return P2E.base.war.apply(this,arguments);
 const R=b._er26,S=b._s4war;S.poseRot=0;S.scale=1;if(b._mr27)b._mr27.ram1002=null;
 if(!S.mini){stage4ShieldTick(b,dt);stage4ShieldSyncNodes(b);
  if(S.shield.rearming){b.x+=(er26Station(b,0)-b.x)*Math.min(1,dt*2);b.y+=(R.home-b.y)*Math.min(1,dt*2);b._drawY=b.y;R.wasRearming=true;return true;}
  if(R.wasRearming){R.wasRearming=false;er26Set(b,'recover');}
  er26CoreTick(b,dt);
 }else er26EscortTick(b,dt);
 if(R.mode==='recover'){R.warnings=[];er26Move(b,R,R.t/R.dur);if(R.t>=R.dur)er26Next(b);}
 else if(R.mode==='overdrive'){er28Combat(b,dt);if(R.t>=R.dur){b._noHit=false;er26Set(b,'recover');}}
 else {if(!R.mode.startsWith('p2-'))er26Set(b,'p2-battery');p2eAttack(b,dt);if(R.t>=R.dur&&!b._l23Beam)er26Set(b,'recover');}
 if(!S.mini)stage4ShieldSyncNodes(b);return true;
};
// Helpers attack in their own recovery slot, never under a reactor laser/ram.
er26CoreTick=function(b,dt){const S=b._s4war,R=b._er26;if(!S?.coreUnlocked)return;
 if(!R.mode.startsWith('p2-'))return P2E.base.core.apply(this,arguments);
 stage4CoreFormationTick(b,dt);for(const d of S.coreTurrets){if(d.dead)continue;const dest=stage4CoreTurretTarget(b,d.side);
 d.spawnT+=dt;d.materialize=clamp(d.spawnT/.8,0,1);d.x+=(dest.x-d.x)*Math.min(1,dt*4);d.y+=(dest.y-d.y)*Math.min(1,dt*4);
 d.state='overheat';d.vulnerable=true;d.spin=(d.spin+dt*9)%8;d.flash=Math.max(0,d.flash-dt);}
};
er26Draw=function(b){const r=P2E.base.draw.apply(this,arguments),R=b._er26;if(b.dead||!R?.mode.startsWith('p2-'))return r;
 const p=b._mr27?mr27Shape(b,'core'):shipBossMount(b,'C'),q=clamp(R.t/Math.max(1,R.warm),0,1);
 if(R.t<R.warm&&mr27CanFire(b,'C'))av3Muzzle(ctx,p.x,p.y,28+q*35,b._ship==='stormsovereign'?'lightning':b._s3Nuclear&&R.form==='fire'?'fire':'ice',R.t);
 return r;
};
// Space formations keep their native distinct weapons and hardpoints. Every
// queued salvo now has a visible FOV, a full 0.65 s tell and a shorter recovery.
s5SpaceTick=function(e,dt){const old=e._s5Act,r=P2E.base.space.apply(this,arguments),A=e._s5Act;
 if(!old&&A){A.at=Math.max(A.at,.65);A.dur=Math.max(A.dur,A.at+.24);A._p2Aim={x:player.x,y:player.y};e._fcd=Math.max(1.0,(e._fcd||1)*.78);
  const fire=A.fn;A.fn=function(){const aim=aimPlayer,before=new Set(eBullets);aimPlayer=(x,y)=>Math.atan2(A._p2Aim.y-y,A._p2Aim.x-x);
   try{fire();}finally{aimPlayer=aim;}
   const k=diffKey==='furious'?1.30:diffKey==='hard'?1.18:1.08;
   for(const b of eBullets)if(!before.has(b)){b.vx*=k;b.vy*=k;if(b._spaceMax)b._spaceMax*=k;
    b._p2Emitter={ship:e._s5space,x:b.x,y:b.y};}
   p2eLog('space-salvo',{ship:e._s5space,shots:eBullets.filter(b=>!before.has(b)).length});
  };
 }
 if(A&&!A.fired&&A.t<A.at-.25)A._p2Aim={x:player.x,y:player.y};
 if(A&&!A.fired&&e._dyingT==null&&!e.dead)combatWarningTick(e,'p2-space',A.t,A.at);
 return r;
};
drawEnemy=function(e){const r=P2E.base.enemy.apply(this,arguments),A=e._s5Act;
 if(run.stage===5&&A&&!A.fired&&A._p2Aim&&!e.dead&&e._dyingT==null){const p=s5Hardpoint(e,0,.34),T=A._p2Aim;
 combatWarningDraw(e,{x:p.x,y:p.y,ex:T.x,ey:T.y,progress:A.t/A.at,width:24});}return r;
};
// Reaver debris remains solid through its burning flight; the last frame is
// covered by a rupture rather than a transparent disappearing module.
av3PartDraw=function(b,p,pose,alpha){return P2E.base.partDraw.call(this,b,p,pose,1);};
er26Tick=function(b,dt){const before=[...(b._av3Reaver?.debris||[])],r=P2E.base.partTick.apply(this,arguments);
 for(const d of before)if(d.t>=1.12&&!d._p2Burst){d._p2Burst=true;explode(d.pose.x,d.pose.y,56,'red');Audio.SFX.expSmall?.();}return r;};

// The first fully raised authored shaft reaches the top of the visible arena.
// Use one common scale for both the sprite and its existing height collider.
const P2_STORM_IMPACT=hammerStormImpact;
hammerStormImpact=function(b){const r=P2_STORM_IMPACT.apply(this,arguments),max=Math.max(...HM10_ART.spike.map(a=>a.height)),crest=HM10_ART.spike[7].height;
 for(const q of b._hammer.stormWaves||[])q.height=Math.max(q.height,(q.y-viewTopY())*max/crest);
 p2eLog('hammer-full-height-spikes',{lanes:b._hammer.stormWaves.length});return r;
};
