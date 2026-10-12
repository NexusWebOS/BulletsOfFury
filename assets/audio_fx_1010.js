"use strict";
/* Authored crystalline ice: one physical muzzle, tiled at a common scale.
   Collider/timing remains with the existing boss and player beam owners. */
const AP10_FX={beam:av3Beam,muzzle:av3Muzzle,load:stageLoadBegin,
 charge:fusion30ChargeDraw,fusion:fusion30BulletDraw,iceBoss:l23BossBeamDraw,draws:{},ends:[]};
for(const bank of Object.values(AP10_FX_ART))for(const a of bank)XART._src[a.key]=a.path;
function ap10FxWarm(name){for(const a of AP10_FX_ART[name]||[])XART.rdy(a.key);}
stageLoadBegin=function(n,keys){return AP10_FX.load.call(this,n,[...(keys||[]),
 ...AP10_FX_ART.ice_laser.map(a=>a.key),...(AP10_FX_ART.fusion||[]).map(a=>a.key)]);};
function ap10IceColor(color){return /ice|rime|frost/i.test(String(color))||(run.stage===3&&av3Color(color)===1);}
function ap10IceFrame(t,release=false){return release?12+Math.min(3,Math.floor(t*16)):4+Math.floor(t*18)%8;}
function ap10FusionFrame(t){return 4+Math.floor(t*24)%8;}
function ap10FusionMuzzle(g,x,y,size,t,alpha=1,frame=ap10FusionFrame(t)){
 const a=AP10_FX_ART.fusion?.[frame];if(!a||!XART.rdy(a.key))return false;
 const k=size/128;g.save();g.imageSmoothingEnabled=false;g.globalAlpha*=alpha;
 g.drawImage(XART.get(a.key),72,208,128,142,x-64*k,y-118*k,128*k,142*k);g.restore();return true;
}
function ap10FusionBeam(g,x,y,angle,length,width,t,alpha=1){
 if(![x,y,angle,length,width].every(Number.isFinite)||length<=0||width<.5)return false;
 const a=AP10_FX_ART.fusion?.[ap10FusionFrame(t)];if(!a||!XART.rdy(a.key))return false;
 const k=width/72,step=Math.max(264*k,length/128);g.save();g.translate(x,y);g.rotate(angle+Math.PI/2);g.imageSmoothingEnabled=false;g.globalAlpha*=alpha;
 g.beginPath();g.rect(-136*k,-length,272*k,length);g.clip();
 for(let i=0,n=Math.min(128,Math.ceil(length/step));i<n;i++)g.drawImage(XART.get(a.key),0,16,272,264,-136*k,-(i+1)*step,272*k,step);
 g.restore();AP10_FX.draws.fusionBeam=(AP10_FX.draws.fusionBeam||0)+1;return true;
}
av3Muzzle=function(g,x,y,size,color,t=AV3.clock,alpha=1){
 if(/fusion|helix/i.test(String(color))&&ap10FusionMuzzle(g,x,y,size,t,alpha))return true;
 if(!ap10IceColor(color))return AP10_FX.muzzle.apply(this,arguments);
 const a=AP10_FX_ART.ice_laser[ap10IceFrame(t)];if(!XART.rdy(a.key))return AP10_FX.muzzle.apply(this,arguments);
 const k=size/148;g.save();g.imageSmoothingEnabled=false;g.globalAlpha*=alpha;
 g.drawImage(XART.get(a.key),38,342,148,98,x-74*k,y-54*k,148*k,98*k);g.restore();
 AP10_FX.draws.iceMuzzle=(AP10_FX.draws.iceMuzzle||0)+1;return true;
};
av3Beam=function(g,x,y,angle,length,width,color,t=AV3.clock,alpha=1,muzzle=true){
 // Harrier's first closing/opening sample may be ~1e-14px wide. Its
 // hundreds of quadrillions of tiles froze the main thread. Subpixel beams
 // have no visible pixels; every visible beam also has a finite tile budget.
 if(![x,y,angle,length,width].every(Number.isFinite)||length<=0||width<.5)return false;
 if(/fusion|helix/i.test(String(color))&&ap10FusionBeam(g,x,y,angle,length,width,t,alpha)){
  if(muzzle)ap10FusionMuzzle(g,x,y,clamp(width*2.8,28,78),t,alpha);return true;}
 if(!ap10IceColor(color))return AP10_FX.beam.apply(this,arguments);
 if(!(length>0&&width>0))return false;
 const a=AP10_FX_ART.ice_laser[ap10IceFrame(t)];if(!XART.rdy(a.key))return AP10_FX.beam.apply(this,arguments);
 const im=XART.get(a.key),k=width/78,h=224*k,step=Math.max(332*k,length/128);
 g.save();g.translate(x,y);g.rotate(angle+Math.PI/2);g.imageSmoothingEnabled=false;g.globalAlpha*=alpha;
 g.beginPath();g.rect(-h/2,-length,h,length);g.clip();
 for(let i=0,n=Math.min(128,Math.ceil(length/step));i<n;i++)g.drawImage(im,0,36,224,332,-112*k,-(i+1)*step,224*k,step);
 g.restore();if(muzzle)av3Muzzle(g,x,y,clamp(width*2.8,24,70),'ice',t,alpha);
 AP10_FX.draws.iceBeam=(AP10_FX.draws.iceBeam||0)+1;return true;
};
fusion30ChargeDraw=function(x,y,size){const q=clamp((run._spaceShadowCharge||0)/FUSION30_FULL,0,2),p=spaceShipHardpoints(x,y,size).nose;
 if(ap10FusionMuzzle(ctx,p.x,p.y,size*(.52+q*.3),efxClock,1,Math.min(3,Math.floor(q*2)))){
  spaceShadowIndicatorDraw(x,y,size);AP10_FX.draws.fusionCharge=(AP10_FX.draws.fusionCharge||0)+1;return;
 }return AP10_FX.charge.apply(this,arguments);};
fusion30BulletDraw=function(b){
 if(b._ap10FusionRelease){const f=12+Math.min(3,Math.floor(b.t/.24*4)),p=spaceShipHardpoints(player.x,player.y,SPACE_SHIP_SIZE).nose;
  if(ap10FusionMuzzle(ctx,p.x,p.y,b.w,b.t,1,f))return true;
 }
 if(b.kind==='spaceFusion'||b._cfFusion){const angle=b._cfChild?Math.atan2(b.vy,b.vx):-Math.PI/2;
  const x=b.x-Math.cos(angle)*b.h*.5,y=b.y-Math.sin(angle)*b.h*.5;
  if(ap10FusionBeam(ctx,x,y,angle,b.h,b.w,b.t||0))return true;
}return AP10_FX.fusion.apply(this,arguments);};
const AP10_FUSION_RELEASE=spaceShadowRelease;
spaceShadowRelease=function(charge){const r=AP10_FUSION_RELEASE.apply(this,arguments);
 if(r){const p=spaceShipHardpoints(player.x,player.y,SPACE_SHIP_SIZE).nose;
  pBullets.push({kind:'spaceFusionFx',_ap10FusionRelease:true,x:p.x,y:p.y,w:SPACE_SHIP_SIZE*.7,h:SPACE_SHIP_SIZE*.7,t:0,life:.24});}
 return r;};
// Boss charge and release consume the same authored reel as the active ice
// column, so all 16 poses have a physical owner rather than unused exports.
l23BossBeamDraw=function(b){const B=b?._l23Beam;
 if(!B||B.family==='inferno')return AP10_FX.iceBoss.apply(this,arguments);
 if(!B.released){AP10_FX.iceBoss.apply(this,arguments);
  for(let i=0;i<B.slots.length;i++){const p=shipBossMount(b,B.slots[i]),f=Math.min(3,Math.floor(B.t/Math.max(.01,B.warm)*4));
  const a=AP10_FX_ART.ice_laser[f];if(XART.rdy(a.key)){const k=(B.width||24)/78;
   ctx.save();ctx.translate(p.x,p.y);ctx.rotate(B.angles[i]+Math.PI/2);ctx.imageSmoothingEnabled=false;
   ctx.drawImage(XART.get(a.key),0,0,224,448,-112*k,-396*k,224*k,448*k);ctx.restore();}}
  return;
 }
 if(B.t>B.warm+B.active){const f=ap10IceFrame(B.t-B.warm-B.active,true);
  for(let i=0;i<B.slots.length;i++){const p=shipBossMount(b,B.slots[i]),a=AP10_FX_ART.ice_laser[f];if(XART.rdy(a.key)){
   const k=(B.width||24)/78;ctx.save();ctx.translate(p.x,p.y);ctx.rotate(B.angles[i]+Math.PI/2);ctx.imageSmoothingEnabled=false;
   ctx.drawImage(XART.get(a.key),0,0,224,448,-112*k,-396*k,224*k,448*k);ctx.restore();}}
  return;
 }return AP10_FX.iceBoss.apply(this,arguments);
};
