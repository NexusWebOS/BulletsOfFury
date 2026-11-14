'use strict';
/* Held weapons belong to complete generated drawings. Only a released thrown
   hammer owns a separate rendered/interceptable weapon entity. */
const WH1110={base:{pose:ha21Blue,dracPose:hb20Pose,rig:v19HammerRig,tick:v19NativeTick,sample:rd74Sample,head:hammerHeadPoint,weaponTarget:hammerWeaponTargetable,shootable:c26Shootable,hit:bossHitTest,catch:c35Catch,toolAt:rd74ToolAt},draws:0};
ha21Blue=function(b){if(ba119Blue(b)&&!b._hammer.c25Knock&&!b._hammer.hb20Pickup){const h=b._hammer;if(h.throw&&h.state==='throw'){const T=h.throw,d=Math.hypot(T.x-c35Catch(b).at.x,T.y-c35Catch(b).at.y),f=T.phase==='return'&&d<160?12:h.t<.10?0:h.t<.24?4:8;return ba119Pose('blue-empty',f,c27Material(b));}if(!h.throw&&['spin','revenge_charge'].includes(h.state))return ba119Pose('blue-overhead',Math.min(8,h.t/HAMMER_SPIN_TIME*9),c27Material(b));if(!h.throw&&!h.hammerDestroyed&&!h._hf22Charge&&!h.c30&&['hammer','storm_idle','idle','back','leap_reset','hammer_catch'].includes(h.state))return ba119Pose('blue-overhead',0,c27Material(b));}return WH1110.base.pose.apply(this,arguments);};
hb20Pose=function(b){if(rd74Own(b)){const Q=hb20State(b),A=Q.action;if(!A&&!Q.rf1110&&!Q.hammerDestroyed)return ba119Corrupt(Q,0);if(A&&!Q.rf1110){const u=A.t-A.tell;if(A.type==='throw'&&u>=0){const returning=u>4.6,f=returning?12:u<.10?0:u<.24?4:8;return ba119Corrupt(Q,f,'corrupt-empty');}if(A.type==='side'){const right=u>=.7,age=right?u-.7:Math.max(0,u),f=age<.35?age/.35*5:5+(age-.35)/.35*10;return ba119Corrupt(Q,u<0?0:f,right?'corrupt-right':'corrupt-sides');}if((A.type==='throw'&&u<0)||(A.type==='arsenal'&&A.t<.95))return ba119Corrupt(Q,Math.min(8,A.t/(A.type==='throw'?A.tell:.95)*9));}}return WH1110.base.dracPose.apply(this,arguments);};
v19HammerRig=function(b){const out=WH1110.base.rig.apply(this,arguments);if(!rd74Own(b))return out;const A=hb20State(b).action,detached=A?.type==='throw'&&A.launch&&A.t>=A.tell;return out.filter(v=>v.p?.id!=='hammer'||detached);};
v19NativeTick=function(b,dt){const A=rd74Own(b)&&hb20State(b).action,r=WH1110.base.tick.apply(this,arguments);if(A&&hb20State(b).action===A&&A.type==='throw'&&A.launch&&!A.wh1110Released){A.wh1110Released=true;A.launch=rf1110HammerCentre(b,ba119Row('corrupt-overhead',8,rd74Mat(hb20State(b))));A.theta0=Math.atan2((A.launch.y-(viewTopY()+viewH()*.5))/(viewH()*.5-80),(A.launch.x-(camLeftX()+camRightX())/2)/(viewW()*.5-65));}return r;};
// Preserve the copied throw's native orbit and timing; return to the head in
// the new complete ready drawing instead of the retired retract plate.
rd74ToolAt=function(b,A){if(!rd74Own(b)||A?.type!=='throw')return WH1110.base.toolAt.apply(this,arguments);const Q=hb20State(b),u=A.t-A.tell,home=rf1110HammerCentre(b,ba119Row('corrupt-overhead',0,rd74Mat(Q)));if(u<0)return rf1110HammerCentre(b,hb20Pose(b).a);if(!A.launch)return home;const cx=(camLeftX()+camRightX())/2,cy=viewTopY()+viewH()*.5,rx=viewW()*.5-65,ry=viewH()*.5-80,theta=A.theta0+A.orbit,edge={x:cx+Math.cos(theta)*rx,y:cy+Math.sin(theta)*ry};if(u<.3)return{x:lerp(A.launch.x,edge.x,u/.3),y:lerp(A.launch.y,edge.y,u/.3)};if(u>4.6){const v=clamp((u-4.6)/.8,0,1);return{x:lerp(edge.x,home.x,v),y:lerp(edge.y,home.y,v)};}return edge;};
// The native return solver consumes c35Catch(). Its destination must be the
// head in the new complete ready drawing, not the retired left-hand plate.
c35Catch=function(b){if(c25Own(b)){const a=ba119Row('blue-overhead',0,c27Material(b));return{at:hb20World(a,a.headCenter,b,1,0),angle:Math.PI,scale:1};}return WH1110.base.catch.apply(this,arguments);};
// The native charging weakpoint remains a counter aperture within the whole
// actor. Ordinary held weapons do not have their own Retina/deflection entity.
hammerWeaponTargetable=function(b){if(c25Own(b)&&!b._hammer.throw&&!c25Counter(b))return false;return WH1110.base.weaponTarget.apply(this,arguments);};
c26Shootable=function(b){if(c25Own(b)&&!b._hammer.throw)return false;return WH1110.base.shootable.apply(this,arguments);};
hammerHeadPoint=function(b){if(c25Own(b)&&!b._hammer.throw&&['spin','revenge_charge'].includes(b._hammer.state)){const q=ha21Blue(b);if(q?.a.wholeGenerated)return hb20World(q.a,q.a.headCenter,b,q.k,0);}return WH1110.base.head.apply(this,arguments);};
bossHitTest=function(x,y){const b=boss;if(ba119Blue(b)){const q=ha21Blue(b);if(q?.a.wholeGenerated){if(b._noHit||hammerDepthScale(b)<.95)return false;const a=q.a,k=q.k||1,px=(x-b.x)/k+a.pivot[0],py=(y-b.y)/k+a.pivot[1];b._hammerModuleHit=null;return ba119Contains(a.spans,px,py);}}return WH1110.base.hit.apply(this,arguments);};
globalThis.BOF_WHOLE_HAMMER_1110=WH1110;


// HA1111: reference-led whole drawings for the existing native whirlwind.
const HA1111={base:{blue:ha21Blue,drac:hb20Pose,head:hammerHeadPoint,state:hammerState,glow:cgActive,target:hammerTarget}};
function ha1111Aim(b){if(!ba119Blue(b))return;const h=b._hammer,s=h.state;if(!['warn','storm_warn','giant_warn'].includes(s))return;
 const k=s==='giant_warn'?1.25:1,a=ba119Row('blue-overhead',11,c27Material(b)),r=ba119Clearance('blue',k),tip=(a.tip[0]-a.pivot[0])*k;
 const aim=x=>clamp(x-tip,camLeftX()+r.left,camRightX()-r.right)+tip;
 if(Number.isFinite(h.tx))h.tx=aim(h.tx);if(s==='storm_warn'&&h.stormTarget)h.stormTarget.x=aim(h.stormTarget.x);
}
hammerTarget=function(b){const out=HA1111.base.target.apply(this,arguments);ha1111Aim(b);return out;};
cgActive=function(b){if(ba119Blue(b)){const h=b._hammer;if(['whirl_warn','whirl_turn','whirlwind','fr_twirl'].includes(h.state)||h.ha1111Exit?.state===h.state&&h.t<.35)return false;}return HA1111.base.glow.apply(this,arguments);};
hammerState=function(b,s){const h=b?._hammer,from=h?.state;
 if(h)delete h.ha1111Exit;
 if(h&&s==='whirlwind'&&from==='whirl_warn')h.ha1111SpinStart=h.c26SpinClock||0;
 if(h&&['whirlwind','whirl_turn','fr_twirl'].includes(from)&&!['whirlwind','whirl_turn','fr_twirl'].includes(s))
  h.ha1111Exit={phase:((((h.c26SpinClock||0)-(h.ha1111SpinStart||0))*2)%16+16)%16,state:s};
 const out=HA1111.base.state.apply(this,arguments);ha1111Aim(b);return out;
};
ha21Blue=function(b){if(ba119Blue(b)&&!b._hammer.c25Knock&&!b._hammer.hb20Pickup&&!b._hammer.throw){
 const h=b._hammer,s=h.state,mat=c27Material(b);
 if(s==='whirl_warn')return ba119Pose('blue-overhead',clamp(h.t/(h.whirl?.warm||1.1),0,.999)*3.5,mat);
 if(['whirl_turn','whirlwind','fr_twirl'].includes(s))return ba119Pose('blue-whirl',((((h.c26SpinClock||0)-(h.ha1111SpinStart||0))*2)%16+16)%16,mat);
 const e=h.ha1111Exit;if(e&&e.state===s&&h.t<.35){const u=clamp(h.t/.35,0,1),f=e.phase+(16-e.phase)*(1-(1-u)*(1-u));return ba119Pose('blue-whirl',f%16,mat);}
 }return HA1111.base.blue.apply(this,arguments);
};
hammerHeadPoint=function(b){if(ba119Blue(b)&&!b._hammer.throw){const q=ha21Blue(b);if(q?.a.bank==='blue-whirl')return hb20World(q.a,q.a.headCenter,b,q.k,0);}return HA1111.base.head.apply(this,arguments);};
hb20Pose=function(b){if(rd74Own(b)){const Q=hb20State(b),A=Q.action;
 if(A?.type==='spin'&&!Q.rf1110){const u=A.t-A.tell;
  if(u<0)return ba119Corrupt(Q,clamp(A.t/A.tell,0,.999)*3.5);
  const end=A.duration-A.tell;
  // Three authored revolutions fit the existing active interval; the final
  // revolution decelerates into frame0 and the native ready/recovery owner.
  const elapsed=clamp(u/end,0,.999999),turns=3*(1-(1-elapsed)*(1-elapsed));
  return ba119Corrupt(Q,(turns*16)%16,'corrupt-whirl');
 }}return HA1111.base.drac.apply(this,arguments);
};
globalThis.BOF_HEAVY_HAMMER_1111=HA1111;


// FH1111 keeps all live held-hammer attack variants on the same frontal banks.
const FH1111={base:{blue:ha21Blue},states:[]};
for(const n of ['blue-overhead','blue-sides','blue-right','blue-whirl']){const key='nca_ba119_'+n+'_red';if(!BA119.keys[5].includes(key))BA119.keys[5].push(key);}
ha21Blue=function(b){if(b?._hammerTime&&b._hammerTime.mode!=='attack')return null;
 if(ba119Blue(b)&&!b._hammer.c25Knock&&!b._hammer.hb20Pickup&&!b._hammer.throw){
 const h=b._hammer,s=h.state,t=h.t||0,mat=c27Material(b),k=s.startsWith('giant_')?hammerDepthScale(b):1;
 if(!h.hammerDestroyed&&['giant_idle','giant_windup','giant_rise','giant_warn'].includes(s)){
  const f=s==='giant_idle'?0:s==='giant_windup'?clamp(t/.48,0,1)*8:8;
  return ba119Pose('blue-overhead',f,mat,k);
 }
 if(s==='storm_split'&&!h._hf22StormPair&&!h.c27Combo)return ba119Pose('blue-overhead',11+clamp(t/.75,0,.999)*4.99,mat);
 }return FH1111.base.blue.apply(this,arguments);
};
globalThis.BOF_FRONT_HAMMER_1111=FH1111;
