'use strict';
/* One canonical T-joint assembly, raster-authored at 32 headings. Only the
   existing flight/catch positioning and depth scale run during gameplay. */
const RH1110={base:{tool:c35Tool,load:stageLoadBegin},heads:RH1110_HEADS,last:null};
XART._src.rh1110_flight='assets/game/shared/combat/rigid_hammer_1110/flight.webp';
XART._src.rh1110_flight_hit='assets/game/shared/combat/rigid_hammer_1110/flight_hit.webp';
function rh1110Warm(){return['rh1110_flight','rh1110_flight_hit'].map(k=>XART.rdy(k)).every(Boolean);}
stageLoadBegin=function(n,keys){return RH1110.base.load.call(this,n,[...(keys||[]),...(n===5?['rh1110_flight','rh1110_flight_hit']:[])]);};
c35Tool=function(at,angle,flash=0,scale=1){if(!rh1110Warm())return false;const f=((Math.round(angle/TAU*32)%32)+32)%32,p=RH1110.heads[f],sx=f%8*384,sy=Math.floor(f/8)*512,k=.72*scale,key=flash>0?'rh1110_flight_hit':'rh1110_flight';ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(key),sx,sy,384,512,at.x+(sx-p[0])*k,at.y+(sy-p[1])*k,384*k,512*k);ctx.restore();RH1110.last={frame:f,head:{...at},jointAngle:Math.PI/2,scale:k};return true;};
globalThis.BOF_RIGID_HAMMER_1110=RH1110;
