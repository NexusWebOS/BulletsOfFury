"use strict";
/* Projectile animation only: spread count, damage, hit boxes and muzzle stay owned
   by the weapon. Forge uses this same draw path, so preview matches flight. */
for(const a of Object.values(SPREAD1001_ART))XART._src[a.key]=a.path;
function spreadDraw1001(b){
 /* 1017 - Mike: "spread fire, should no longer be the large slugs. should be our actual bullet graphics, but
    spread style." A plain spread pellet now flies as the machine gun's own round (the mgcf_ per-level plate
    the gun draws), turned along its line - the plate points UP at angle 0, so heading + PI/2. Infused
    pellets already wear the element's bullet round (element_arsenal_1011, same as the gun). If the plate
    has not decoded this returns false and drawBullets falls to the nca_87 round pack, also bullet art.
    The 1001 slug reels stay registered (SPREAD1001_ART) for the Forge's records; nothing flies them. */
 const lv=clamp(b.lv||1,1,5);if(b._inf||typeof mgcfFrame!=='function')return false;
 const key='mgcf_'+lv+'_'+mgcfFrame(b);if(!XART.rdy(key))return false;
 return drawMfx(key,b.x,b.y,Math.atan2(b.vy||-1,b.vx||0)+Math.PI/2,22+lv*1.4,null,1,null,null);
}
