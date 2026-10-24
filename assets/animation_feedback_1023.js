"use strict";
/* Native fleet controllers keep warnings, hitboxes, shields, attacks and deaths.
   Shared retired atlas aliases cannot be sampled as their former 4x4 layout.
   Correct type-specific authored cells and white variants are prebaked at
   native units; this renderer uses integer blits and no runtime recoloring. */
const AQ23_FIX={base:{realm:drawS8Mega,load:stageLoadBegin},draws:0};
for(const s of Object.values(AQ23_ART.sheets))XART._src[s.key]=s.path;
stageLoadBegin=function(n,keys){return AQ23_FIX.base.load.call(this,n,[...(keys||[]),...(n===8?Object.keys(AQ23_ART.sheets):[])]);};
drawS8Mega=function(e){const m=AQ23_ART.models[e.type];if(!m)return AQ23_FIX.base.realm.apply(this,arguments);
 const A=e._frRealmAI,size=Math.max(e.w,e.h)*1.28;e._drawW=size*.82;e._drawH=size;
 const turn=Math.abs(e._frBank||0)>10?(e._frBank<0?1:7):0,key=e.flash>0?m.white:m.key;
 if(!XART.rdy(key))return false;const im=XART.get(key),s=m.cell;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,turn%4*s,Math.floor(turn/4)*s,s,s,Math.round(e.x-m.pivot[0]),Math.round(e.y-m.pivot[1]),s,s);AQ23_FIX.draws++;
 if(A?.tell)combatWarningDraw(e,{x:e.x,y:e.y+e.h*.35,ex:A.tell.x,ey:A.tell.y,progress:A.tell.t/.8,width:fr27RealmRow(e)===0?85:fr27RealmRow(e)===2?30:100,alpha:.32});
 return true;
};
window.BOF_ANIMATION_FEEDBACK=AQ23_FIX;
