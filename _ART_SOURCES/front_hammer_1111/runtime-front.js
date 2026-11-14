
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
