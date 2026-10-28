"use strict";
/* Stage 6 carrier: red authored laser palette; passive fan objectives.
   Native HP, Retina targets, collision, breakup and Nightwing handoff remain. */
const CR31={drawing:0,smoke:[],base:{get:XART.get,draw:roster17Draw,weapon:roster17Weapon,fanDraw:s6r18FanDraw,load:stageLoadBegin}};
for(const a of Object.values(CR31_ART.banks))XART._src[a.key]=a.path;
function cr31Own(b){return run.stage===6&&!run._gp4StageX&&!!(b?._carrier17||b?._s6CarrierFall);}
stageLoadBegin=function(n,keys){return CR31.base.load.call(this,n,n===6?[...(keys||[]),...Object.values(CR31_ART.banks).map(a=>a.key)]:keys);};
// Palette substitution is scoped to the carrier's own draw. The exact existing
// beam and focused muzzle renderers retain their animation, widths and sockets.
XART.get=function(key){const name=CR31.drawing&&CR31_ART.aliases[key];return CR31.base.get.call(this,name?CR31_ART.banks[name].key:key);};
roster17Draw=function(b){if(!cr31Own(b))return CR31.base.draw.apply(this,arguments);CR31.drawing++;
 try{return CR31.base.draw.apply(this,arguments);}finally{CR31.drawing--;}};
roster17Weapon=function(b,p,dt){if(cr31Own(b)&&p?.kind==='fan'){
 // Never enter targeting, warning, fire or audio owners. These parts still
 // participate in the original native health budget and player Retina list.
 p.phase=p.dead?'dead':'rest';p.t=0;p.cool=1;delete p.aim;delete p.angle;delete p.lanes;delete p.er28Bearing;return;
 }return CR31.base.weapon.apply(this,arguments);};
s6r18FanDraw=function(b,C){const result=CR31.base.fanDraw.apply(this,arguments);CR31.smoke=[];
 if(!cr31Own(b))return result;const a=CR31_ART.banks.fan_smoke;if(!XART.rdy(a.key))return result;
 const W=b._whv,S=s6r18State(b);
 for(const p of C.parts){if(p.kind!=='fan'||!p.dead)continue;
  const x=W.cx+p.dx*WHV_S,y=W.cy+(W.dy||0)+p.dy*WHV_S,F=S.fanFx.get(p.id),f=Math.floor((F?.t||0)*a.fps+(p.id==='R'?4:0))%a.frames;
  // The existing overlay supplies the same carrier translation/depth transform
  // as the fan sockets. One fixed authored column per broken fan, including fall.
  ctx.drawImage(XART.get(a.key),f*a.cw,0,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);
  CR31.smoke.push({id:p.id,x,y,frame:f});
 }return result;
};
globalThis.BOF_CARRIER_REVISION_1028=CR31;
