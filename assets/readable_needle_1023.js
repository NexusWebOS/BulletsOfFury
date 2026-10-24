"use strict";
/* The audited 7x7 sky tracer collapsed to a one-pixel-wide core. Reuse the
   existing PixelLab art at one authored .25 unit. Every direction and frame
   is prebaked; collision, targeting, release time and shot velocity stay native. */
const RN23_ART={"version":1,"owner":"_BUILD_SOURCE/build_readable_needle_1023.py","unit":0.25,"angles":32,"cell":32,"banks":{"sky":{"key":"aq23_readable_sky","path":"assets/game/shared/combat/readable_needle_1023/sky.webp","frames":5,"fps":20,"stage":6,"source":"assets/game/shared/enemies/biome_fleet_1022/sky_needle.webp","sha256":"82f833192cb01dd0cc387844619a60aa18ee1073af89c0dfc7cb6ba08dc548fd"},"toxic":{"key":"aq23_readable_toxic","path":"assets/game/shared/combat/readable_needle_1023/toxic.webp","frames":5,"fps":20,"stage":7,"source":"assets/game/shared/enemies/pressure_1022/toxic_needle.webp","sha256":"4dec991639108860c78908995d777ed402e9c48247d71f26d2dc4237c21e4c14"},"water":{"key":"aq23_readable_water","path":"assets/game/shared/combat/readable_needle_1023/water.webp","frames":5,"fps":20,"stage":9,"source":"assets/game/shared/enemies/biome_fleet_1022/water_needle.webp","sha256":"a055eef96373177aebf9f94c664bc16cf4da955b3ce7789cf8043fb12b3505b5"},"magma":{"key":"aq23_readable_magma","path":"assets/game/shared/combat/readable_needle_1023/magma.webp","frames":5,"fps":20,"stage":2,"source":"assets/game/shared/enemies/biome_fleet_1022/magma_needle.webp","sha256":"d82771422cf9462fb78b878ea247702f9a80941c2ee4f992aceed6f1c1ee3abb"}}},RN23={base:{draw:ovSonicProjectileDraw,load:stageLoadBegin},draws:0};
for(const b of Object.values(RN23_ART.banks))XART._src[b.key]=b.path;
stageLoadBegin=function(n,keys){return RN23.base.load.call(this,n,[...(keys||[]),...Object.values(RN23_ART.banks).filter(b=>b.stage===n).map(b=>b.key)]);};
ovSonicProjectileDraw=function(b){const a=RN23_ART.banks[b?._bf22Theme];if(!a||b._bf22Form!=='needle'||Math.max(b.w||7,b.h||7)>14)return RN23.base.draw.apply(this,arguments);
 if(!XART.rdy(a.key))return RN23.base.draw.apply(this,arguments);
 const angle=Math.atan2(b.vy||0,b.vx||0)-Math.PI/2,bin=((Math.round(angle/TAU*32)%32)+32)%32,f=Math.floor(Math.max(0,efxClock-(b._bf22Born||0))*a.fps)%a.frames,i=bin*a.frames+f;
 ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),i%8*32,Math.floor(i/8)*32,32,32,Math.round(b.x-16),Math.round(b.y-16),32,32);RN23.draws++;return true;
};
window.BOF_READABLE_NEEDLES=RN23;
