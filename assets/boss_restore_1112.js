'use strict';
/* Mike requested the earlier full sideways sweeps and the original Stage5 rage
   formation / Kamehameha. Restore their existing owners; retain new overheads,
   ships and modular guns. No new generated character drawing is introduced. */
const BR1112={base:{blue:ha21Blue,draw:hammerBossDraw,tick:hammerBossTick,hit:bossHitTest,
 glow:cgActive,trace:c27TraceAura,pose:hb20Pose,jump:rd74JumpPose,sample:rd74Sample,
 load:stageLoadBegin},sideSource:'boss_strike_1109b',events:[]};
function br1112Rage(b){return c25Own(b)&&!b.dead&&!!(b._hammer._hf22Charge||c30Own(b));}
// These saved functions predate the RF1110 replacement and retain the original
// C45/C46/C47/CF48/CF49/CF50 choreography, aura, sound and wave owners.
c45ReelDraw=rf1110Reel;c45ReelHead=rf1110ReelHead;c45StopDraw=rf1110StopDraw;
c32Pose=RF1110.base.palm;c30Hand=RF1110.base.hand;
ha21Blue=function(b){return br1112Rage(b)?RF1110.base.pose.apply(this,arguments):BR1112.base.blue.apply(this,arguments);};
hammerBossDraw=function(b){return br1112Rage(b)?RF1110.base.draw.apply(this,arguments):BR1112.base.draw.apply(this,arguments);};
hammerBossTick=function(b,dt){return c25Own(b)?RF1110.base.tick.apply(this,arguments):BR1112.base.tick.apply(this,arguments);};
bossHitTest=function(){return br1112Rage(boss)?RF1110.base.hit.apply(this,arguments):BR1112.base.hit.apply(this,arguments);};
cgActive=function(b){return br1112Rage(b)?RF1110.base.active.apply(this,arguments):BR1112.base.glow.apply(this,arguments);};
c27TraceAura=function(b,q){return br1112Rage(b)?rf1110OldTrace.apply(this,arguments):BR1112.base.trace.apply(this,arguments);};
stageLoadBegin=function(n,keys){return BR1112.base.load.call(this,n,[...(keys||[]),...(n===5?[C45_REEL_KEY,C45_STOP_KEY]:[])]);};
// Native contact clocks stay fixed. Put the recovered full sweep at contact,
// then show its authored follow-through and return instead of holding a guard.
function br1112SideFrame(age,contact=.5,end=1.06){
 age=Math.max(0,age)+1e-9;if(age<contact)return age/contact*8;
 const follow=contact+(end-contact)*.42;
 return age<follow?8+(age-contact)/(follow-contact)*3:Math.min(15.999,11+(age-follow)/(end-follow)*4.999);
}
ba119SideFrame=function(age){return br1112SideFrame(age);};
rd74JumpPose=function(Q,A){const u=A.t-A.tell;
 if(A.strikes===4&&u>=2.7&&u<4.1){const right=u>=3.4,start=right?3.4:2.7,contact=right?.35:.4375;
  return ba119Corrupt(Q,br1112SideFrame(u-start,contact,.7),right?'corrupt-right':'corrupt-sides');}
 return BR1112.base.jump.apply(this,arguments);
};
hb20Pose=function(b){if(rd74Own(b)){const Q=hb20State(b),A=Q.action;
 if(A?.type==='side'&&!Q.rf1110&&!Q.rage){const u=A.t-A.tell,right=u>=.7,age=right?u-.7:Math.max(0,u);
  return ba119Corrupt(Q,u<0?0:br1112SideFrame(age,.35,.7),right?'corrupt-right':'corrupt-sides');}}
 return BR1112.base.pose.apply(this,arguments);
};
rd74Sample=function(bank,f=0){const Q=rd74Own(boss)&&hb20State(boss);
 if(Q?.action?.type==='skystrike'&&f===16){if(bank.startsWith('left_'))return ba119Corrupt(Q,8,'corrupt-sides');if(bank.startsWith('right_'))return ba119Corrupt(Q,8,'corrupt-right');}
 return BR1112.base.sample.apply(this,arguments);
};
globalThis.BOF_BOSS_RESTORE_1112=BR1112;
