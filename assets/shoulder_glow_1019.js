"use strict";
/* Rime's permanent shoulder apertures: light inside the measured cavity,
   authored frost motion and a fixed brightness ladder. Real hit flashes remain. */
const SG19={draws:[],base:{load:stageLoadBegin,blit:mr27Blit}};
for(const bank of Object.values(SG19_ART.banks))for(const a of bank)XART._src[a.key]=a.path;
function sg19Keys(){return Object.values(SG19_ART.banks).flat().map(a=>a.key);}
function sg19Ready(){let ok=true;for(const key of sg19Keys())if(!XART.rdy(key))ok=false;return ok;}
stageLoadBegin=function(n,keys){return SG19.base.load.call(this,n,[...(keys||[]),...(n===3?sg19Keys():[])]);};
mr27Blit=function(skin,cell,p,flash,form,owner){
 // SA14's alternating whole-hull charge wash hid the authored icy steel. Its
 // saved native blitter still draws the real owner/part hit flash and expiry.
 if(rd19Owns(owner))return SA14.base.blit.apply(this,arguments);
 return SG19.base.blit.apply(this,arguments);
};
function sg19Shoulders(b,k){
 const C=rd19State(b),scale=Math.min(b.w/MR27_ART.rime.cells[0][2],b.h/MR27_ART.rime.cells[0][3]);
 const intensity=PXG_STEPS[Math.max(2,Math.min(5,Math.round(clamp(k,0,1)*5)))];
 for(const side of [-1,1]){const bank=side<0?'L':'R',i=Math.floor(C.age*SG19_ART.fps)%32,a=SG19_ART.banks[bank][i];
  if(!XART.rdy(a.key))continue;const p=rd19Port(b,side);
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=intensity;
  ctx.drawImage(XART.get(a.key),p.x-40*scale,p.y-40*scale,80*scale,80*scale);ctx.restore();
  SG19.draws.push({key:a.key,x:p.x,y:p.y,scale,intensity});if(SG19.draws.length>128)SG19.draws.shift();
 }
}
window.BOF_SHOULDER_GLOW={state:SG19,ready:sg19Ready};
