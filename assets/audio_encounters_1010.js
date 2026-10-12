"use strict";
/* Timestamped encounter fixes from the October 10 Normal playthrough. */
const AP10_E={base:{book:er26Book,set:er26Set,war:er26WarTick,core:er26CoreTick,
 draw:er26Draw,beam:l23BossBeamStart,begin:beginStage,leave:scLeaveStage,
 quick:gp4QuickEncounter,play:updatePlay,world:drawWorld},history:[]};
function ap10EncounterLog(event,data={}){AP10_E.history.push({event,...data});if(AP10_E.history.length>160)AP10_E.history.shift();}
er26Book=function(b){let book=AP10_E.base.book.apply(this,arguments);
 if(b._ship==='stormsovereign')book=book.map(m=>['hc-cross1007','storm-lance1002'].includes(m)?'ap10-stormburst':m);
 if(av3Reaver(b)&&b.hp>b.maxhp*.35)book=book.map(m=>/mortar|bombard/.test(m)?'furnace-lance':m);
 return book;
};
l23BossBeamStart=function(b,family,slots,angles,warm,active,retract,width,opts){
 if(av3Reaver(b)&&family==='inferno'){
  width=Math.max(width||0,diffKey==='furious'?40:diffKey==='hard'?36:32);
  active=Math.max(active||0,1.7);opts={...(opts||{}),sweepArc:slots.map((s,i)=>(i&1?-1:1)*.12),sweepRate:1.1};
 }
 return AP10_E.base.beam.call(this,b,family,slots,angles,warm,active,retract,width,opts);
};
er26Set=function(b,mode){const r=AP10_E.base.set.apply(this,arguments);
 if(b._ship!=='stormsovereign')return r;
 if(mode!=='ap10-stormburst'){if(b._ap10Storm&&!b._ap10Storm.shot)b._ap10Storm=null;return r;}
 const R=b._er26,rank=diffKey==='furious'?2:diffKey==='hard'?1:0;
 b._l23Beam=null;if(b._hc1007)b._hc1007.cross=null;
 b._ap10Storm={age:0,warm:diffKey==='easy'?2.4:2.0,rank,released:false,burst:false,shot:null};
 R.warm=b._ap10Storm.warm;R.dur=R.warm+2.1;
 Audio.SFX.warshipCoreCharge?.();ap10EncounterLog('sovereign-fusion-charge',{rank});return r;
};
er26WarTick=function(b,dt){
 const Q=b._ap10Storm,R=b._er26,S=b._s4war;
 if(b._ship!=='stormsovereign'||R.mode!=='ap10-stormburst'||!Q)return AP10_E.base.war.apply(this,arguments);
 Q.age+=dt;R.warnings=[];S.poseRot=0;S.scale=1;b._drawY=b.y;
 stage4ShieldTick(b,dt);stage4ShieldSyncNodes(b);er26CoreTick(b,dt);
 if(b.dead||S.shield?.rearming){b._ap10Storm=null;er26Set(b,'recover');return true;}
 const C=shipBossMount(b,'C');
 if(!Q.released){
  if(!mr27CanFire(b,'C')){b._ap10Storm=null;er26Set(b,'recover');return true;}
  const p=clamp(Q.age/Q.warm,0,1);
  R.warnings.push({slot:'C',angle:Math.PI/2,width:52,progress:p});
  combatWarningTick(b,'ap10-stormburst',Q.age,Q.warm);
  b.x+=(er26Station(b,0)-b.x)*Math.min(1,dt*3);b.y+=(R.home-b.y)*Math.min(1,dt*3);
  if(Q.age>=Q.warm){const muzzle=shipBossMount(b,'C');Q.released=true;Q.shot={x:muzzle.x,y:muzzle.y,fromY:muzzle.y,vy:[280,360,450][Q.rank],end:Math.max(muzzle.y+60,PLAY.y+PLAY.h*.51)};
   stage4WarfareMuzzle(b,'C','lightning',1.4,.24);Audio.SFX.fusionBeam?.();shake=Math.max(shake,5);
   ap10EncounterLog('sovereign-fusion-release',{x:C.x,y:C.y});}
 }
 if(Q.shot){const q=Q.shot;q.y+=q.vy*dt;
  for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.abs(player.x-q.x)<18+(player._hx||8)&&Math.abs(player.y-q.y)<36)playerHit('Lightning fusion shot');});
  if(q.y>=q.end){
   q.y=q.end;const aim=aimPlayer(q.x,q.y),count=diffKey==='easy'?3:[5,7,9][Q.rank],speed=[3.0,4.05,5.0][Q.rank];
   for(let i=0;i<count;i++){const a=aim+(i-(count-1)/2)*.15,shot=stage4WarfareShot(b,{x:q.x,y:q.y},a,speed,'orb',{shootable:true,hp:2,szMul:.7,lift:0});
    shot.vx=Math.cos(a)*speed;shot.vy=Math.sin(a)*speed;shot._ap10Lightning=true;shot._weaponProof=false;shot._er26Source=b._ship;}
   efxBurst('lightning',q.x,q.y,110);Audio.SFX.enemyElectricBolt?.();shake=Math.max(shake,7);
   Q.shot=null;Q.burst=true;Q.recoverAt=Q.age;ap10EncounterLog('sovereign-fusion-midburst',{count,speed,y:q.y});
  }
 }
 if(Q.burst&&Q.age-Q.recoverAt>1.05){b._ap10Storm=null;er26Set(b,'recover');}
 return true;
};
er26Draw=function(b){const r=AP10_E.base.draw.apply(this,arguments),Q=b._ap10Storm;if(!Q||b.dead)return r;
 if(!Q.released){const C=shipBossMount(b,'C'),k=clamp(Q.age/Q.warm,0,1);
  ctx.save();ctx.fillStyle='rgba(1,3,12,'+(.12+.25*k)+')';ctx.fillRect(camLeftX(),viewTopY(),viewW(),viewH());ctx.restore();
  av3Muzzle(ctx,C.x,C.y,30+k*64,'fusion',Q.age);}
 if(Q.shot){const q=Q.shot;av3Beam(ctx,q.x,q.y-70,Math.PI/2,105,26,'fusion',Q.age);}
 return r;
};
// Helpers advance their own alternating windup/fire/overheat cycle, rather
// than remaining disabled through every renamed boss attack in the book.
er26CoreTick=function(b,dt){
 const S=b._s4war,R=b._er26;if(!S?.coreUnlocked)return;
 if(S.coreEnrage)stage4CoreEnrageEnd(b);stage4CoreFormationTick(b,dt);
 S._ap10HelperClock=(S._ap10HelperClock||0)+dt;
 const rank=diffKey==='furious'?2:diffKey==='hard'?1:0,warm=diffKey==='easy'?1.15:.90;
 for(const d of S.coreTurrets){
  if(d.dead||b._mr27&&mr27HelperState(d).dead)continue;
  if(b._mr27)d._mrOwner=b;const dest=stage4CoreTurretTarget(b,d.side);
  d.spawnT+=dt;d.materialize=clamp(d.spawnT/.8,0,1);d.flash=Math.max(0,d.flash-dt);
  d.deflectFlash=Math.max(0,(d.deflectFlash||0)-dt);d.deflectSfx=Math.max(0,(d.deflectSfx||0)-dt);
  d.x+=(dest.x-d.x)*Math.min(1,dt*5);d.y+=(dest.y-d.y)*Math.min(1,dt*5);
  const local=(S._ap10HelperClock+(d.side>0?3:0))%6;
  const paused=!!(b._ap10Storm&&!b._ap10Storm.burst)||S.shield?.rearming;
  const state=!paused&&local<warm?'windup':!paused&&local<warm+1.2?'fire':'overheat';
  if(d.state!==state){d.state=state;d.stateT=0;d.fireShot=0;
   if(state==='windup'){const T=targetShip(d.x,d.y);d._erAim=Math.atan2(T.y-d.y,T.x-d.x);Audio.SFX.warshipCoreCharge?.();}
   if(state==='fire')Audio.SFX.enemyMachineGunHeavy?.();}
  d.stateT+=dt;d.vulnerable=state==='overheat';S.coreCycleSeen[state]=true;
  d.heat=state==='overheat'?.75:state==='fire'?.48:.15;d.reelSpeed=state==='fire'?38:state==='windup'?22:6;d.spin=(d.spin+dt*d.reelSpeed)%8;
  const a=clamp(d._erAim??Math.PI/2,Math.PI*.22,Math.PI*.78);
  d.ang+=stage4AngleDelta(d.ang,a)*Math.min(1,dt*5);
  if(d.materialize<1)continue;
  if(state==='windup')for(const side of [-1,1]){const p=stage4CoreTurretTip(d,side);R.warnings.push({slot:null,x:p.x,y:p.y,angle:a,width:24,progress:local/warm});combatWarningTick(d,'ap10-helper-'+side,local,warm);}
  if(state!=='fire')continue;d.fireShot-=dt;if(d.fireShot>0)continue;d.fireShot=[.135,.11,.09][rank];
  const side=d.barrelNext||-1;d.barrelNext=-side;const p=stage4CoreTurretTip(d,side);
  const shot=stage4WarfareShot(b,p,a,[4.6,5.0,5.4][rank],'lightningmg',{szMul:1.22});
  shot._s4CoreSide=d.side;shot._s4CoreBarrel=side;shot._er26Source='core';shot._shootable=false;shot._weaponProof=true;
  S.coreShots++;S.coreBarrelShots[side]++;R.helperShots++;stage4CoreTurretMuzzle(b,d,side);
 }
};
// The central Furious finisher uses the same committed projectile/mid-burst
// language. It never silently changes into a screen-wide instant kill.
stage4GiantStrikeStart=function(b){if(!b?._s4war||b._s4war.mini)return false;er26Set(b,'ap10-stormburst');b._s4war.giantStrike=null;return true;};

/* The detour restores the original timeline after all begin-stage wrappers
   have added their scheduled events, so no early miniboss/wave replays. */
beginStage=function(n){const suspended=n===5&&run._s5ResumeArm&&run._s5Resume?{...run._s5Resume}:null;
 const r=AP10_E.base.begin.apply(this,arguments);
 if(suspended){stageTimer=suspended.t;spawnClock=suspended.clock;waveIdx=suspended.wave;
  stagePlan=stagePlan.filter(q=>q.t>stageTimer+.001);
  if(suspended.map!=null)mapScroll=suspended.map;
  if(typeof scroll==='number')scroll=suspended.scroll;
  if(suspended.sky!=null)_stage5SpaceScroll=suspended.sky;
  subBossDone=suspended.miniDone!==false;subBossTriggered=subBossDone||!!suspended.miniTriggered;_sbMusicResumed=subBossDone;
  run._s5Resume=null;run._s5ResumeArm=0;storySkip();BOFCinematicDirector.cancel();setState(GS.PLAY);
  ap10EncounterLog('stage5-detour-resume',{t:stageTimer,miniDone:subBossDone});}
 return r;
};
scLeaveStage=function(R){
 if(run.stage===9&&run._s5Resume){
  run.score+=(R.bonus||0);if(R.seats)run2.score+=R.seats[1]?.bonus||0;
  if(run.mode==='campaign')campAutoAfterClear(9,campaign.unlockedMax,R.rank);
  drawStageClear._init=false;drawStageClear._res=null;run._s9taken=1;run._s5ResumeArm=1;run._s5GateOut=1;
  Audio.stopMusic();beginStage(5);return;
 }
 return AP10_E.base.leave.apply(this,arguments);
};
