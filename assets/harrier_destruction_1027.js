'use strict';
/* Opaque carrier -> hull-sized detonation -> spreading fire and smoke.
   Reuses the approved engine explosion/smoke owners, never fades the ship. */
const HD29={base:{tick:whvDeathTick,draw:whvDrawCarrier,load:stageLoadBegin},events:[],last:null};
function hd29Own(b){return run.stage===6&&!run._gp4StageX&&!!b?._s6CarrierFall;}
stageLoadBegin=function(n,keys){const art=['nxp_dense','nxp_barrage','nxp_ring','nsd_ring'].flatMap(f=>Array.from({length:8},(_,i)=>f+'_'+i));return HD29.base.load.call(this,n,n===6?[...(keys||[]),...art]:keys);};
function hd29Log(b,event,data={}){HD29.events.push({event,t:b._whv.t,...data});if(HD29.events.length>100)HD29.events.shift();}
whvDeathTick=function(b,dt){const r=HD29.base.tick.apply(this,arguments);if(!hd29Own(b))return r;const W=b._whv,S=b._hd29||(b._hd29={next:.12,n:0,covered:false,ring:0}),unit=roster17HullScale(b),w=WHV_PLATE.w*WHV_S*unit,h=WHV_PLATE.h*WHV_S*unit,x=W.cx,y=W.cy+(W.dy||0),T=W.t;
 // A finite outward sweep reaches both wings and the nose, rather than
 // clustering small explosions over a transparent whole-carrier image.
 if(T<5.15&&T>=S.next){S.next+=.17;const i=S.n++,a=i*2.39996323,spread=T<3.6?.43:.63,px=x+Math.cos(a)*w*spread,py=y+Math.sin(a)*h*spread;
  explode(px,py,w*(T<3.6?.19:.27),'red',null,i%2?'nxp_dense':'nxp_barrage',null,.65,true);hd29Log(b,'spread-blast',{x:px,y:py,size:w*(T<3.6?.19:.27)});
 }
 if(T>=3.6&&!S.covered){S.covered=true;
  explode(x,y,w*1.12,'red',null,'nxp_dense',null,1.15,true);
  for(const side of[-1,1])for(const row of[-1,0,1])explode(x+side*w*.33,y+row*h*.30,w*.52,'red',null,'nxp_dense',null,.9,true);
  hd29Log(b,'hull-detonation',{x,y,width:w,height:h,size:w*1.12});
 }
 if(S.covered&&S.ring<3&&T>=3.6+S.ring*.38){
  // Stage6's shared smoke owner applies .65 crowded scaling. Compensate the
  // requested size so these rings actually match this carrier's visible hull.
  spawnSmokeRing(x+(S.ring-1)*w*.1,y,w*(.75+S.ring*.14)/.65);S.ring++;hd29Log(b,'smoke-ring',{size:w*(.75+(S.ring-1)*.14)});
 }
 return r;
};
whvDrawCarrier=function(b){if(!hd29Own(b))return HD29.base.draw.apply(this,arguments);const S=b._hd29;
 if(S?.covered&&b._whv.t>=3.9){HD29.last={t:b._whv.t,hull:false,reason:'hull-sized detonation'};return;}
 // Full authored wreck stays opaque until the covering detonation begins.
 roster17Draw(b,b._s6CarrierFall);s6r18CarrierOverlay(b,b._s6CarrierFall);HD29.last={t:b._whv.t,hull:true,alpha:ctx.globalAlpha};
};
globalThis.BOF_HARRIER_DESTRUCTION_1027=HD29;
