"use strict";
/* Stage8 only. Every held/thrown/rage weapon below was baked offline from
   ONE prop at ONE physical unit. Native action clocks and combat stay owned. */
const HC23={base:{pose:hb20Pose,pickup:hb20Pickup,clip:v18Clip,start:hb20Start,effect:b20SizedEffect},draws:{}};
hb20Pose=function(b){
 if(!hb20Own(b))return HC23.base.pose.apply(this,arguments);
 const Q=hb20State(b),A=Q?.action;if(!A)return HC23.base.pose.apply(this,arguments);
 const t=A.t||0,u=t-(A.tell||0);let bank=null,f=0;
 if(A.type==='ball'){
  // The old ball tell carried another hammer for its first seven keys.
  // Keep the canonical armed/crouched plates, then select only the fully
  // transformed ball keys from that existing transform owner.
  if(u<0&&t/A.tell<.82){bank='corrupt_jump';f=t/A.tell<.55?0:6;}
  else {const q=HC23.base.pose.apply(this,arguments),a=H22_ART.banks.corrupt_ball[t/A.tell<.94?7:8];return hf22Swap({...q,a},b);}
 }else if(A.type==='side'){
  const right=A.target.x>=A.origin.x,start=right?8:0,n=right?7:8;
  bank='corrupt_sides';f=start+(u<0?clamp(t/A.tell,0,1)*2:2+clamp(u/.8,0,1)*(n-3));
 }else if(A.type==='spin'){bank='corrupt_spin_fixed';f=u<0?0:Math.floor(u/.7*15)%15;}
 else if(['charge','shield'].includes(A.type)){bank='corrupt_hold';}
 else if(A.type==='dance'){bank='corrupt_sides';const seq=[0,1,2,4,5,6,8,9,10,12,13,14];f=seq[Math.floor(Math.max(0,u)*8)%seq.length];}
 else if(A.type==='pickup'){bank='corrupt_jump';f=t<.8?0:t<1.3?lerp(0,4,(t-.8)/.5):t<1.78?lerp(4,7,(t-1.3)/.48):lerp(7,10,clamp((t-1.78)/1.07,0,1));}
 else if(A.type==='break'){bank='corrupt_break_fixed';f=t<1.35?clamp(t/1.35,0,.999)*3:3+Math.floor((t-1.35)*12)%6;}
 else if(A.type==='luminaire'){bank='corrupt_throw';f=t<.15?5:t<.35?6:7;}
 if(bank){const q=hf22Pose(b,bank,f);if(q){HC23.draws[bank]=(HC23.draws[bank]||0)+1;return q;}}
 return HC23.base.pose.apply(this,arguments);
};
hb20Pickup=function(b,corrupt=false){const C=HC23.base.pickup.apply(this,arguments);if(corrupt){const a=hf22Row('corrupt_jump',HF22_ART.phases.corrupt.strikeEnd);C.box=hb20World(a,a.tip,C.station,1,0);}return C;};
hb20Start=function(b,type){let source=null;const Q=hb20Own(b)&&hb20State(b);if(Q&&type==='luminaire'){const C=Q._hc23Break,f=C?3+Math.floor((C.t-1.35)*12)%6:3,q=hf22Pose(b,'corrupt_break_fixed',f);if(q?.a)source=hb20World(q.a,q.a.glow,b,1,0);}const A=HC23.base.start.apply(this,arguments);if(Q&&A?.type==='break')Q._hc23Break=A;if(A?.type==='luminaire'&&source)A.coreFrom=source;return A;};
b20SizedEffect=function(bank,t,x,y,size,rot){const b=boss,A=hb20Own(b)&&hb20State(b)?.action;if(A?.type==='break'&&bank===DR21_ART.banks.ball&&size===42){const q=hb20Pose(b);if(q?.a?._hc23){const at=hb20World(q.a,q.a.glow,b,1,0);HC23.lastCoreAt=at;return HC23.base.effect.call(this,bank,t,at.x,at.y,size,0);}}return HC23.base.effect.apply(this,arguments);};
v18Clip=function(name,t,d,x,y,size,reverse){if(name==='morph_hammer'){const a=hf22Row('corrupt_hold',0);if(a&&XART.rdy(a.key))return hf22Cell(a,x,y);}return HC23.base.clip.apply(this,arguments);};
window.BOF_HAMMER_CONSISTENCY=HC23;
