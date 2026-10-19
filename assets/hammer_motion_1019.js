"use strict";
/* Real changing views share the native Stage-5 Hammer clock and collision rig.
   Counter swings, throwing, broken-hammer and giant states keep their owners. */
const HM19={base:{rig:v19HammerRig,keys:v18Keys,warm:v18Warm,at:v19AtRect},draws:{}};
const hm19Art=()=>Object.values(HM19_ART.banks).flat();
for(const a of hm19Art()){
 XART._src[a.key]=a.path;
 FMC_ART[a.key]={key:a.key,path:a.path,rects:{pose:[0,0,a.w,a.h]}};
}
v18Keys=function(){return [...HM19.base.keys(),...hm19Art().map(a=>a.key)];};
v18Warm=function(){let ready=HM19.base.warm();for(const a of hm19Art())if(!XART.rdy(a.key))ready=false;return ready;};
function hm19Frame(h){
 if(!h||h.hc11Counter||h.hammerDestroyed||h.throw)return null;
 if(h.state==='ball'){
  const a=((h.angle||0)%(Math.PI*2)+Math.PI*2)%(Math.PI*2);
  return HM19_ART.banks.ball[Math.floor(a/(Math.PI*2)*HM19_ART.banks.ball.length)];
 }
 if(['whirl_warn','whirl_turn','whirlwind','spin','fr_twirl'].includes(h.state)){
  const t=h.t||0,clock=h.state==='whirlwind'&&h.whirl?h.whirl.reel:
   ['spin','fr_twirl'].includes(h.state)?(t*9+Math.min(t,1.6)*t*7)*2:0;
  return HM19_ART.banks.twirl[((Math.floor(clock)%8)+8)%8];
 }
 return null;
}
v19HammerRig=function(b){
 const p=gd4Create(b,8).p,h=p._hammer,a=hm19Frame(h);
 if(!a||!XART.rdy(a.key))return HM19.base.rig.apply(this,arguments);
 // Undo only the common reference export scale. One proportional world scale
 // keeps the occupied body the same size as its original native motion pose.
 const k=.76/a.referenceScale,core=b.parts.find(p=>p.id==='core');
 const v={p:core,key:a.key,a,ax:b.x,ay:b.y,x:b.x,y:b.y,w:a.w*k,h:a.h*k,
  rot:0,alpha:1,k,z:1,_hm19:true,spec:{px:.5,py:.5,art:'pose',sheet:a.key,role:'core'}};
 const out=[v],hammer=b.parts.find(p=>p.id==='hammer');
 if(a.head&&hammer&&!hammer.destroyed){const x=b.x+(a.head[0]-128)*k,y=b.y+(a.head[1]-128)*k;
  out.push({p:hammer,key:a.key,ax:x,ay:y,x,y,w:64,h:55,rot:0,alpha:1,z:5,
   spec:{px:.5,py:.5,role:'hammerHead',hidden:true}});
 }
 HM19.draws[a.key]=(HM19.draws[a.key]||0)+1;return out;
};
v19AtRect=function(v,x,y){
 if(!v._hm19)return HM19.base.at.apply(this,arguments);
 const px=Math.floor((x-v.ax)/v.k+128),py=Math.floor((y-v.ay)/v.k+128),m=v18Mask(v.a);
 return !!(m&&px>=0&&py>=0&&px<v.a.w&&py<v.a.h&&m[py*v.a.w+px]>48);
};
window.BOF_HAMMER_MOTION={state:HM19,frame:hm19Frame};
