"use strict";
/* Projectile animation only: spread count, damage, hit boxes and muzzle stay owned
   by the weapon. Forge uses this same draw path, so preview matches flight. */
for(const a of Object.values(SPREAD1001_ART))XART._src[a.key]=a.path;
function spreadDraw1001(b){
 const a=SPREAD1001_ART[b._inf]||SPREAD1001_ART.base;if(!XART.rdy(a.key))return false;
 const f=Math.floor((b.t||0)*a.fps)%a.frames.length,r=a.frames[f];
 const h=30+clamp(b._infLv||b.lv||1,1,8)*1.5,w=h*r[2]/r[3];
 const im=!b._inf&&b.lv>1?xartPalette(a.key,wlvGlow(b.lv)):XART.get(a.key);if(!im)return false;
 ctx.save();ctx.translate(b.x,b.y);ctx.rotate(Math.atan2(b.vy||-1,b.vx||0)+Math.PI/2);
 ctx.imageSmoothingEnabled=false;ctx.drawImage(im,...r,-w/2,-h/2,w,h);ctx.restore();return true;
}
