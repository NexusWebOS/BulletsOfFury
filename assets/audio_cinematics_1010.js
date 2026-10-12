"use strict";
/* Registered portal animation; collision and scene clocks stay with the engine. */
const AP10_C={cell:aa5Cell,toxic:missionToxicPortal,drCell:dr5Cell,
 load:stageLoadBegin,hit:playerHit,intro:on5IntroDraw,draws:{}};
for(const bank of Object.values(AP10_CIN_ART))for(const a of bank)XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){return AP10_C.load.call(this,n,[...(keys||[]),
 ...(n>=5?Object.values(AP10_CIN_ART).flat().map(a=>a.key):[])]);};
function ap10VoidWarm(){for(const a of AP10_CIN_ART.void)XART.rdy(a.key);}
function ap10VoidFrame(open,t){return open==='open'?Math.min(7,Math.floor(t*12)):
 open==='close'?24+Math.min(7,Math.floor(t*16)):8+Math.floor(t*20)%16;}
function ap10VoidCell(f,x,y,w,h=w,rot=0,alpha=1){
 const a=AP10_CIN_ART.void[clamp(f|0,0,31)];if(!XART.rdy(a.key))return false;
 ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),-w/2,-h/2,w,h);ctx.restore();AP10_C.draws.void=(AP10_C.draws.void||0)+1;return true;
}
aa5Cell=function(name,f,x,y,w,h=w,rot=0,alpha=1){
 if(name!=='void')return AP10_C.cell.apply(this,arguments);
 const t=j3State(boss)?.aa5Clock??efxClock,index=f<8?Math.min(7,f):ap10VoidFrame('loop',t);
 if(ap10VoidCell(index,x,y,w,h,rot,alpha))return true;return AP10_C.cell.apply(this,arguments);
};
missionToxicPortal=function(f,x,y,w,h){
 const index=f<4?Math.min(7,f*2):f<12?ap10VoidFrame('loop',efxClock):24+(f-12)*2;
 if(ap10VoidCell(index,x,y,w,h||w))return true;return AP10_C.toxic.apply(this,arguments);
};
dr5Cell=function(name,f,x,y,w,h=w,rot=0,alpha=1){
 if(name==='portal'){
  const index=f<4?f*2:f<8?ap10VoidFrame('loop',boss?._r30?.t||efxClock):24+(f-8)*2;
  if(ap10VoidCell(index,x,y,w,h,rot,alpha))return true;
 }return AP10_C.drCell.apply(this,arguments);
};
// A scripted flight cannot die to a surviving collision owner while its ship
// is being carried into the next stage. The world continues to advance.
playerHit=function(){const E=run.stage===7&&boss?._s7mod?.frExit;
 if(E?.k1001&&!E.done)return;return AP10_C.hit.apply(this,arguments);};
on5IntroDraw=function(b){
 const S=b._r30;if(S.mode!=='takeover')return AP10_C.intro.apply(this,arguments);
 const f=Math.min(15,Math.floor(S.t/4.5*16)),a=AP10_CIN_ART.consumption[f];
 if(!XART.rdy(a.key))return AP10_C.intro.apply(this,arguments);
 // This is a cinematic plate. Combat still uses its separate, targetable rig.
 const k=360/a.w;ctx.save();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),b.x-a.pivot[0]*k,b.y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
 AP10_C.draws.consumption=(AP10_C.draws.consumption||0)+1;
};
