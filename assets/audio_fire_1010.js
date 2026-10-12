"use strict";
/* Authored formation, moving flame loop and discrete shatter; no fading ring. */
const AP10_FIRE={draw:magmaWardBarrierDraw,chain:fztChain,tick:magmaWardBarrierTick,load:stageLoadBegin,draws:{}};
for(const bank of Object.values(AP10_FIRE_ART))for(const a of bank)XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){return AP10_FIRE.load.call(this,n,[...(keys||[]),...(n===2?Object.values(AP10_FIRE_ART).flat().map(a=>a.key):[])]);};
function ap10FireCell(name,f,x,y,size,rot=0,flash=0){const bank=AP10_FIRE_ART[name],a=bank[clamp(f|0,0,bank.length-1)];
 if(!XART.rdy(a.key))return false;const k=size/a.h,im=flash>0?xartTint(a.key,'#ffffff',1):XART.get(a.key);
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(x,y);ctx.rotate(rot);
 ctx.drawImage(im,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
 AP10_FIRE.draws[name]=(AP10_FIRE.draws[name]||0)+1;return true;
}
magmaWardBarrierTick=function(b,dt){const H=b?._mwBarrier;if(H){
 if(H.active&&!H._ap10WasActive)H._ap10Age=0;
 H._ap10Age=(H._ap10Age||0)+dt;H._ap10WasActive=H.active;
 }return AP10_FIRE.tick.apply(this,arguments);};
magmaWardBarrierDraw=function(b){const H=b?._mwBarrier;if(!H||!b._fz)return AP10_FIRE.draw.apply(this,arguments);
 if(b._fz.phase==='intro')return;
 if(!H.active&&!(H.breakT>0))return;
 const age=H._ap10Age||0,f=H.active?(age<.32?Math.min(3,Math.floor(age/.08)):4+Math.floor(age*24)%20):24+Math.min(7,Math.floor((.72-H.breakT)/.72*8));
 if(!ap10FireCell('fire_shield',f,b.x,b._drawY??b.y,288,0,H.hit))return AP10_FIRE.draw.apply(this,arguments);
};
fztChain=function(a,b,alpha=1){const dx=b.x-a.x,dy=b.y-a.y,len=Math.hypot(dx,dy),rot=Math.atan2(-dx,dy),n=Math.ceil(len/(18*FZT_S));
 const bank=AP10_FIRE_ART.chain;if(!bank.every(q=>XART.rdy(q.key)))return AP10_FIRE.chain.apply(this,arguments);
 for(let i=0;i<=n;i++){const u=i/Math.max(1,n),f=(Math.floor(efxClock*20)+i*2)%16;
  ctx.save();ctx.globalAlpha*=alpha;ap10FireCell('chain',f,lerp(a.x,b.x,u),lerp(a.y,b.y,u),40*FZT_S,rot);ctx.restore();}
};
