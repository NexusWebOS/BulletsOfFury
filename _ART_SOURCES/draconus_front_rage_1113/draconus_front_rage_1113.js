'use strict';
/* Mike: Draconus's strikes must keep his face/chest toward the player, and
   his actual rage formation and full attack book must be visible in combat. */
const DFR13={base:{pose:hb20Pose,jump:rd74JumpPose,sample:rd74Sample,finish:rd74Finish,
 melee:rd74Melee,draw:v19DonorDraw,tick:v19NativeTick},events:[]};
function dfr13Log(type,data={}){DFR13.events.push({type,time:efxClock,...data});if(DFR13.events.length>600)DFR13.events.shift();}
function dfr13Stroke(age,contact,end=.7){
 age=Math.max(0,age)+1e-9;const lift=contact*.6;
 if(age<lift)return age/lift*8;
 if(age<contact)return 8+(age-lift)/(contact-lift)*3;
 return Math.min(15.999,11+(age-contact)/(end-contact)*4.999);
}
function dfr13Pose(Q,right,age,contact=.35){return ba119Corrupt(Q,dfr13Stroke(age,contact),right?'corrupt-overhead-right':'corrupt-overhead-left');}
rd74JumpPose=function(Q,A){const u=A.t-A.tell;
 if(A.strikes===4&&u>=2.7&&u<4.1){const right=u>=3.4;return dfr13Pose(Q,right,u-(right?3.4:2.7),right?.35:.4375);}
 return DFR13.base.jump.apply(this,arguments);
};
hb20Pose=function(b){if(rd74Own(b)){const Q=hb20State(b),A=Q.action;
 if(A?.type==='side'&&!Q.rf1110&&!Q.rage){const u=A.t-A.tell,right=u>=.7;
  return dfr13Pose(Q,right,u<0?0:u-(right?.7:0));}}
 return DFR13.base.pose.apply(this,arguments);
};
rd74Sample=function(bank,f=0){const Q=rd74Own(boss)&&hb20State(boss),A=Q?.action;
 if(f===16&&(A?.type==='skystrike'||A?.type==='side')){
  if(bank.startsWith('left_'))return ba119Corrupt(Q,11,'corrupt-overhead-left');
  if(bank.startsWith('right_'))return ba119Corrupt(Q,11,'corrupt-overhead-right');
 }
 return DFR13.base.sample.apply(this,arguments);
};
// Keep native per-stroke hit sets; windups and recovery no longer hurt ships.
rd74Melee=function(b,A,part,head){if(rd74Own(b)&&A.type==='side'){
 const u=A.t-A.tell,right=u>=.7,age=u-(right?.7:0);
 if(age<.25||age>.49){A.last=null;return;}
 if(age>=.35){const id=right?4:3;if(!A['impact'+id])rd74Impact(b,A,id);}
 }return DFR13.base.melee.apply(this,arguments);};
v19DonorDraw=function(b){const out=DFR13.base.draw.apply(this,arguments);if(!rd74Own(b))return out;
 const Q=hb20State(b),A=Q.action;if(A?.type==='side'&&!Q.rf1110&&!Q.rage){const u=A.t-A.tell;
  for(const right of [false,true]){const start=right?.7:-A.tell,hit=right?1.05:.35;if(u<start||u>=hit)continue;
   const at=rd74Point(b,dfr13Pose(Q,right,.35));b20Reticle(at.x,at.y,48,clamp((u-start)/(hit-start),0,1));}
 }return out;
};
// Commit the existing native rage immediately at the low-HP action boundary.
// Otherwise the52s copied-form return can win during its idle cooldown.
rd74Finish=function(b,A){const out=DFR13.base.finish.apply(this,arguments);if(rd74Own(b)&&!b.dead&&b.hp>0){const Q=hb20State(b);
 if(!Q.action&&!Q.rage&&!Q.rf1110&&Q.chrome&&Q.opening&&b.hp<=b.maxhp*.29){
  Q.cool=0;hb20Start(b,'rage');dfr13Log('native-rage-committed',{hp:b.hp,maxhp:b.maxhp,donorAge:b._r30.v18.donorAge});
 }}return out;
};
v19NativeTick=function(b,dt){const Q=rd74Own(b)&&hb20State(b),R=Q?.rf1110,phase=R?.phase,cycle=R?.cycle;
 const out=DFR13.base.tick.apply(this,arguments),next=Q?.rf1110;
 if(Q&&next&&(next.phase!==phase||next.cycle!==cycle))dfr13Log('rage-phase',{phase:next.phase,cycle:next.cycle,depth:next.volley?.depth,hp:b.hp});
 if(R&&!next)dfr13Log('rage-book-complete',{cycles:R.cycle,hp:b.hp,donorAge:b._r30.v18.donorAge});
 return out;
};
globalThis.BOF_DRACONUS_FRONT_RAGE_1113=DFR13;
