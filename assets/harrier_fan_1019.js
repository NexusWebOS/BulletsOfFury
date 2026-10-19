"use strict";
/* Dracodia's copied Harrier keeps its authored pods/hubs. Only the actual
   turbine interiors advance through PixelLab's exact source-palette poses. */
const HF19={base:{paint:v19Paint,keys:v18Keys,warm:v18Warm},draws:{}};
for(const a of HF19_ART.frames)XART._src[a.key]=a.path;
v18Keys=function(){return [...HF19.base.keys(),...HF19_ART.frames.map(a=>a.key)];};
v18Warm=function(){let ready=HF19.base.warm();for(const a of HF19_ART.frames)if(!XART.rdy(a.key))ready=false;return ready;};
function hf19Rotor(v,b){
 const m=HF19_ART.mounts[v.p.id];if(!m||v.p.destroyed||!v19Native(b)||b._r30.v18.form!==6)return;
 const f=(Math.floor((b._r30.clock||0)*HF19_ART.fps)+(v.p.id==='fanR'?8:0))%HF19_ART.frames.length,a=HF19_ART.frames[f];
 if(!XART.rdy(a.key))return;
 const point=fmcPoint(v,m.sourceAxle[0]/m.sourceSize[0],m.sourceAxle[1]/m.sourceSize[1]),k=Math.min(v.w/m.sourceSize[0],v.h/m.sourceSize[1])/HF19_ART.referenceScale;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.shadowBlur=0;ctx.translate(point.x,point.y);ctx.rotate(v.rot||0);
 ctx.drawImage(XART.get(a.key),-32*k,-32*k,64*k,64*k);
 const flash=Math.max(v.p.flash||0,b.flash||0);if(flash>0){ctx.globalAlpha*=Math.min(.8,flash*8);ctx.drawImage(xartTint(a.key,'#ffffff',1),-32*k,-32*k,64*k,64*k);}
 ctx.restore();HF19.draws[a.key]=(HF19.draws[a.key]||0)+1;
}
v19Paint=function(v,b){const r=HF19.base.paint.apply(this,arguments);hf19Rotor(v,b);return r;};
window.BOF_HARRIER_FAN={state:HF19,rotor:hf19Rotor};
