
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
