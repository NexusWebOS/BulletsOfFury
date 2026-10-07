"use strict";
/* The ship visibly restores generators on the existing three HP thresholds.
   Authored charge -> hull/socket conduits -> local reconstruction. Cosmetic only. */
XART._src[S4REV1006_ART.key]=S4REV1006_ART.path;
const S4REV1006_BASE={init:stage4WarfareInit,rearm:stage4ShieldBeginRearm,tick:stage4ShieldTick,over:mr27Over};
function s4RevivalClip1006(name,u,x,y,sx,sy,alpha){
 if(alpha<=0||!XART.rdy(S4REV1006_ART.key))return false;
 const clip=S4REV1006_ART.clips[name],frame=clip.frames[clamp(Math.floor(u*4),0,3)],r=frame.rect;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=clamp(alpha,0,1);
 ctx.drawImage(XART.get(S4REV1006_ART.key),...r,x+frame.offset[0]*sx,y+frame.offset[1]*sy,r[2]*sx,r[3]*sy);ctx.restore();return true;
}
stage4WarfareInit=function(b){
 const result=S4REV1006_BASE.init.apply(this,arguments);
 if(b?._ship==='stormsovereign'&&!b._s4war?.mini)XART.rdy(S4REV1006_ART.key);
 return result;
};
stage4ShieldBeginRearm=function(b,threshold){
 const result=S4REV1006_BASE.rearm.apply(this,arguments);
 if(result&&b?._ship==='stormsovereign'&&!b._s4war.mini){
  b._s4war.shield.revival1006={t:0,threshold,cycle:b._s4war.shield.cycle};
  XART.rdy(S4REV1006_ART.key);stage4WarfareSound('warshipCoreCharge','bossWeaponCharge');
 }
 return result;
};
stage4ShieldTick=function(b,dt){
 const result=S4REV1006_BASE.tick.apply(this,arguments),H=b?._s4war?.shield,V=H?.revival1006;
 if(V){V.t+=dt;if(b.dead||(!H.rearming&&!H.active)||V.t>=1.48)H.revival1006=null;}
 return result;
};
function s4RevivalDraw1006(b){
 const H=b?._s4war?.shield,V=H?.revival1006;
 if(!V||b.dead||(!H.rearming&&!H.active)||b._ship!=='stormsovereign')return;
 const t=V.t,cy=b._drawY??b.y,charge=clamp(t/.20,0,1)*clamp((1.08-t)/.26,0,1);
 // Hollow corona surrounds the hull's reactor; it remains separate from damage flash.
 s4RevivalClip1006('charge',clamp(t/1.08,0,1),b.x,cy+b.h*.02,.60,.60,charge*.88);
 for(let i=0;i<H.nodes.length;i++){
  const n=H.nodes[i];if(n.dead)continue;
  const start=.16+i*.055,age=t-start,u=clamp(age/.92,0,1);
  if(age<0)continue;
  const pulse=clamp(age/.16,0,1)*clamp((1.42-t)/.28,0,1);
  const a={x:b.x+n.side*b.w*.19,y:cy+b.h*.07},dx=n.x-a.x,dy=n.y-a.y,len=Math.hypot(dx,dy);
  if(t<1.10&&len>1){
   ctx.save();ctx.translate(a.x,a.y);ctx.rotate(Math.atan2(dy,dx));
   s4RevivalClip1006('conduit',u,0,0,len/S4REV1006_ART.conduitEndpointSpan,.18,pulse*.92);ctx.restore();
  }
  s4RevivalClip1006('socket',u,n.x,n.y,.31,.31,pulse*.94);
 }
}
mr27Over=function(b){const result=S4REV1006_BASE.over.apply(this,arguments);s4RevivalDraw1006(b);return result;};
