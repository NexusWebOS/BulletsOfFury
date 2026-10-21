"use strict";
/* Stage1 release feedback, southern return and post-helicopter air raid.
   Existing authored plates, native shots, deaths and campaign callbacks remain. */
const S1R21={base:{naval:navalTick,flash:navalFlash,draw:drawEnemy,ov:updateOverlordX,
 ready:damAssaultReady1002,raid:damAssaultTick1002,die:bossDie,play:updatePlay},events:[]};
function s1r21Boat(e){return run.stage===1&&e&&!e.dead&&e._dyingT==null&&/^(s1boatgun|s1boatpatrol|s1corvette)$/.test(e.type);}
navalTick=function(e,dt){
 if(!s1r21Boat(e))return S1R21.base.naval.apply(this,arguments);
 let A=e._s1rTell;
 const readyMissile=e._naval==='missile'&&!e._beached&&e._idle<=dt&&e._shotCd<=dt&&navalInSix(e);
 if(!A&&readyMissile&&!e._s1rPrimed)A=e._s1rTell={t:0,dur:.75,x:player.x,y:player.y,missile:true};
 if(A){
  A.t+=dt;if(A.t<A.dur*.55){A.x=player.x;A.y=player.y;}
  const saved={burst:e._burst,cd:e._burstCd,shot:e._shotCd,idle:e._idle};
  e._burst=0;e._burstCd=e._shotCd=e._idle=999;
  try{S1R21.base.naval.call(this,e,dt);}finally{e._burst=saved.burst;e._burstCd=saved.cd;e._shotCd=saved.shot;e._idle=saved.idle;}
  combatWarningTick(e,'s1r-boat',A.t,A.dur);
  if(A.t>=A.dur||e._beached){e._s1rTell=null;e._s1rPrimed=!e._beached;}
  return;
 }
 const before=e._burst||0,r=S1R21.base.naval.apply(this,arguments);e._s1rPrimed=false;
 if(!e._beached&&before<=0&&e._burst>0)e._s1rTell={t:0,dur:.65,x:player.x,y:player.y};
 return r;
};
navalFlash=function(e,mz,scale,fam,opts){
 if(!s1r21Boat(e))return S1R21.base.flash.apply(this,arguments);
 const missile=e.type==='s1boatgun',mods=furyBoatModules(e)||[],module=mods.filter(m=>m.hp>0).sort((a,b)=>{
  const p=furyBoatPoint(e,a),q=furyBoatPoint(e,b);return Math.hypot(p.x-mz.x,p.y-mz.y)-Math.hypot(q.x-mz.x,q.y-mz.y);
 })[0];
 const p=module?furyBoatPoint(e,module):{x:e.x,y:e.y},dx=mz.x-p.x,dy=mz.y-p.y;
 const follow=()=>{if(e.dead||module&&module.hp<=0)return null;const q=module?furyBoatPoint(e,module):{x:e.x,y:e.y};return{x:q.x+dx,y:q.y+dy};};
 S1R21.events.push({kind:'boat-release',type:e.type,x:mz.x,y:mz.y,t:e.t});if(S1R21.events.length>160)S1R21.events.shift();
 return S1R21.base.flash.call(this,e,mz,1,fam,{...(opts||{}),hpx:missile?84:76,life:missile?.22:.19,follow});
};
drawEnemy=function(e){
 const r=S1R21.base.draw.apply(this,arguments),A=e._s1rTell;
 if(s1r21Boat(e)&&A)combatWarningDraw(e,{x:e.x,y:e.y+e.h*.12,ex:A.x,ey:A.y,progress:A.t/A.dur,width:A.missile?38:52});
 return r;
};
updateOverlordX=function(b,dt){
 if(run.stage===1&&b&&!b.dead&&b._ovInit&&!b.enter&&(!b._ovIntro||b._ovIntro.done)&&b.hp>0&&b.hp/b.maxhp<=.5&&!b._s1rSouth){
  b._s1rSouth=true;
  if(!b._ovPassSeq){
   b._ovPassUsed=true;b._ovPassSeq={pass:0,used:[],lastLane:null};b._ovFurySingleRam=false;b._enraged=true;
   if(!['chargeTell','chargeOff'].includes(b._ovState)){
    b._ovSweep=b._ovVolley=b._ovSonic=b._ovRush=null;ovStartChargeTell(b);
   }
   S1R21.events.push({kind:'south-return-committed',hp:b.hp});
  }
 }
 return S1R21.base.ov.apply(this,arguments);
};
// The former pre-boss bomber gate is now the attack after his destruction.
damAssaultReady1002=function(){return run.stage===1?true:S1R21.base.ready.apply(this,arguments);};
bossDie=function(){
 const b=boss,after=run.stage===1&&b&&b.kind==='damkeeper'&&!b.dead;
 const r=S1R21.base.die.apply(this,arguments);
 if(after&&b.dead){run._damAssault1002={t:0,next:0,waves:0,done:false,afterHelicopter:true};S1R21.events.push({kind:'post-helicopter-raid-pending'});}
 return r;
};
damAssaultTick1002=function(dt){
 if(run.stage!==1)return S1R21.base.raid.apply(this,arguments);
 const A=run._damAssault1002;
 if(!A?.afterHelicopter||!boss?.dead||boss.dying<8.6)return;
 if(!A.started){A.started=true;Audio.startMusic(curStage.music||'stage');}
 return S1R21.base.raid.apply(this,arguments);
};
updatePlay=function(dt){
 const A=run.stage===1?run._damAssault1002:null,hold=A?.afterHelicopter&&!A.done,wasDone=A?.done;
 if(hold)stageEnding=0;
 const r=S1R21.base.play.apply(this,arguments);
 if(hold&&!wasDone&&A.done){stageEnding=5.79;S1R21.events.push({kind:'post-helicopter-raid-clear'});}
 return r;
};
window.BOF_STAGE1_REPAIR=S1R21;
