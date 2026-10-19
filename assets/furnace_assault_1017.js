"use strict";
/* Stage2 only. Native armor pools, shield, hit routing, tells and beam
   collision remain authoritative. PixelLab head/laser poses share sockets. */
const FURNACE17={art:typeof F17_ART==='undefined'?null:F17_ART,
 base:{combat:furnaceHeadCombat,draw:furnaceDraw,beam:fztBeam,beamDraw:fztBeamDraw,
 cannon:furnaceCannon,load:stageLoadBegin,rawBeam:PT11.base.furnaceBeam},
 events:[],draws:{head:0,laser:0,flame:0},last:null};
function f17Own(b){return run.stage===2&&b?._furnace&&!b._gp4Host;}
function f17Log(event,data={}){FURNACE17.events.push({event,...data});if(FURNACE17.events.length>180)FURNACE17.events.shift();}
function f17Keys(){return FURNACE17.art?Object.values(FURNACE17.art).flatMap(v=>v.frames||[]).flatMap(a=>[a.key,a.glowKey].filter(Boolean)):[];}
for(const bank of Object.values(FURNACE17.art||{}))for(const a of bank.frames||[]){XART._src[a.key]=a.path;if(a.glowKey)XART._src[a.glowKey]=a.glowPath;}
function f17Warm(){for(const k of f17Keys())XART.rdy(k);}
stageLoadBegin=function(n,keys){return FURNACE17.base.load.call(this,n,n===2?[...(keys||[]),...f17Keys()]:keys);};
function f17Tune(){return diffKey==='easy'?{warm:2.15,active:6.4,recover:1.55,width:9}:
 diffKey==='hard'?{warm:1.65,active:4.0,recover:1.05,width:11}:
 ['furious','insanity'].includes(diffKey)?{warm:1.45,active:3.0,recover:.85,width:12}:
 {warm:1.85,active:5.8,recover:1.3,width:10};}
function f17State(b){const F=b._fz;if(!F._f17||F._f17.serial!==F.serial){F._f17={serial:F.serial,
 phase:'charge',roll:0,charge:0,dir:F.dir||1,origin:{x:b.x,y:b.y},sound:false,release:false};
 f17Log('head-windup',{serial:F.serial,difficulty:diffKey});}return F._f17;}
function f17Descriptor(b){
 const Q=f17State(b),A=FURNACE17.art;
 if(A){const bank=Q.phase==='spin'?A.spin:A.charge,frames=bank?.frames;
  if(frames?.length){let i=Math.min(frames.length-1,Math.round(Q.charge*(frames.length-1)));
   if(Q.phase==='spin'){let nearest=Infinity;for(let j=0;j<frames.length;j++){const distance=Math.abs(fztWrap(Q.roll-(frames[j].angle||0)));if(distance<nearest){nearest=distance;i=j;}}}
   const a=frames[i];
   if(XART.rdy(a.key))return {a,rotation:fztWrap(Q.roll-(a.angle||0)),index:i,bank:Q.phase==='spin'?'spin':'charge',scale:1.1*FZT_S*.66};
  }
 }
 // Authored neutral fallback only while the new loose bank decodes.
 const a=PT11_ART.furnace_head[0];if(!XART.rdy(a.key)){f17Warm();return null;}
 return {a:{...a,pivot:[128,132],eyes:[[95,142],[161,142]]},rotation:Q.roll,index:0,bank:'authored-fallback',scale:1.1*FZT_S*.66};
}
function f17Sockets(b){const pose=f17Descriptor(b),Q=f17State(b);
 if(!pose){const c=Math.cos(Q.roll),s=Math.sin(Q.roll);return [-1,1].map(side=>({x:b.x+side*16*c-6*s,y:b.y+side*16*s+6*c}));}
 const {a,rotation,scale}=pose,c=Math.cos(rotation),s=Math.sin(rotation);
 return a.eyes.map(([x,y])=>{x=(x-a.pivot[0])*scale;y=(y-a.pivot[1])*scale;return{x:b.x+x*c-y*s,y:b.y+x*s+y*c};});
}
furnaceHeadCombat=function(b,dt){
 if(!f17Own(b))return FURNACE17.base.combat.apply(this,arguments);
 const F=b._fz,Q=f17State(b),C=f17Tune(),t=F.at,u=clamp((t-C.warm)/C.active,0,1);
 F.a=0;F.rollLive=false;Q.roll=Q.dir*Math.PI*2*u;
 Q.phase=t<C.warm?'charge':t<C.warm+C.active?'spin':'recover';
 Q.charge=t<C.warm?clamp(t/C.warm,0,1):Q.phase==='spin'?1:1-clamp((t-C.warm-C.active)/C.recover,0,1);F.charge=Q.charge;
 if(!Q.sound){Q.sound=true;fztSfx('furnaceLaserCharge');fztSfx('furnaceReactorHum');}
 // The last part of the tell fixes the station. Laser direction is a
 // committed circular sweep; it never follows the player during release.
 if(t<C.warm-.55){b.x=Q.origin.x+Math.sin(F.t*.7)*Math.min(30,worldWidth()*.035)*dt;b.y=Q.origin.y;}
 const sockets=f17Sockets(b),length=Math.hypot(worldWidth(),viewH())+160;
 if(Q.phase==='charge'){
  const strength=.5+Q.charge*2.8;shake=Math.max(shake||0,strength);
  combatWarningTick(b,'f17-eyes-'+F.serial,t,C.warm);
  for(let i=0;i<2;i++){const p=sockets[i],a=(i?1:-1)*.13,e=fztPt(p.x,p.y,a,length);
   F.tells.push({x:p.x,y:p.y,ex:e.x,ey:e.y,progress:t/C.warm,width:C.width*FZT_S,kind:'line'});}
 }else if(Q.phase==='spin'){
  if(!Q.release){Q.release=true;fztSfx('furnaceLaserBurst');f17Log('head-lasers',{serial:F.serial,seconds:C.active});}
  const fade=Math.min(1,(t-C.warm)/.16,(C.warm+C.active-t)/.18);
  if(fade>.02)for(let i=0;i<2;i++){const p=sockets[i],a=Q.roll+(i?1:-1)*.13,n=F.beams.length;
   FURNACE17.base.rawBeam(F,p.x,p.y,a,length/FZT_S,C.width*fade,'eye');
   for(const q of F.beams.slice(n)){q._f17Laser=true;q.owner=b;q.fade=fade;q.clock=F.t;}
  }
  shake=Math.max(shake||0,.7);
 }
 if(t>=C.warm+C.active+C.recover){Q.completed=true;f17Log('head-rotation-complete',{radians:Q.roll,serial:F.serial});furnaceNext(b);}
};
fztBeam=function(F,x,y,a,len,width,kind){
 if(f17Own(boss)&&boss._fz===F&&kind==='flame'){
  const n=F.beams.length,out=FURNACE17.base.rawBeam.apply(this,arguments);
  for(const q of F.beams.slice(n)){q._f17Flame=true;q.clock=F.t;}
  return out;
 }
 return FURNACE17.base.beam.apply(this,arguments);
};
furnaceCannon=function(b,t,period,lockPose){
 const F=b._fz,oldBeat=F?.shotBeat,n=eBullets.length,out=FURNACE17.base.cannon.apply(this,arguments);
 if(!f17Own(b)||F.phase!=='arms'||F.pools.right<=0||F.shotBeat===oldBeat)return out;
 const released=eBullets.slice(n).find(q=>q._fzt&&q.kind==='fztFireball');if(!released)return out;
 F._f17CannonCount=(F._f17CannonCount||0)+1;
 if(F._f17CannonCount%2===0){
  const a=released.ang-Math.PI/2,speed=['furious','insanity'].includes(diffKey)?3.65:diffKey==='hard'?3.3:2.85;
  Object.assign(released,{vx:-Math.sin(a)*speed,vy:Math.cos(a)*speed,w:112,h:34,ang:a,kind:'pt11FireWave',
   _pt11Wave:true,_pt11Scale:.64,_weaponProof:true,_shootable:false,_f17CannonWave:true});
  fztSfx('furnaceFlameRelease');f17Log('cannon-wave',{x:released.x,y:released.y,angle:a,serial:F.serial});
 }else f17Log('cannon-magma',{x:released.x,y:released.y,serial:F.serial});
 return out;
};
function f17PaintHead(b){
 const F=b._fz,Q=f17State(b),pose=f17Descriptor(b);if(!pose)return false;
 const {a,rotation,index,bank,scale}=pose,im=XART.get(a.key),jitter=Q.phase==='charge'?Q.charge*1.35:0;
 const dx=Math.sin(F.t*57)*jitter,dy=Math.cos(F.t*49)*jitter;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(b.x+dx,b.y+dy);ctx.rotate(rotation);
 const rect=[-a.pivot[0]*scale,-a.pivot[1]*scale,a.w*scale,a.h*scale];ctx.drawImage(im,...rect);
 if(a.glowKey&&XART.rdy(a.glowKey)){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.15+.55*Q.charge;ctx.drawImage(XART.get(a.glowKey),...rect);ctx.restore();}
 const flash=Math.max(b.flash||0,F.flash.head||0);
 if(flash>0){const hit=xartTint(a.key,hitFlashColor(b),.9);if(hit){ctx.save();ctx.globalAlpha=clamp(flash/.16,0,1)*.85;ctx.drawImage(hit,...rect);ctx.restore();}}
 ctx.restore();FURNACE17.draws.head++;FURNACE17.last={key:a.key,bank,index,rotation,roll:Q.roll,sockets:f17Sockets(b),phase:Q.phase,flash};return true;
}
furnaceDraw=function(b){
 const F=b?._fz;if(!f17Own(b)||F.phase!=='head'||b.dead)return FURNACE17.base.draw.apply(this,arguments);
 ctx.save();ctx.imageSmoothingEnabled=false;
 for(const q of F.tells)fztTellDraw(q,b);
 f17PaintHead(b);
 const r=F.pools.head/Math.max(1,F.max.head);fztSmoke({x:b.x+25*FZT_S,y:b.y+8*FZT_S},r,.28);
 for(const q of F.beams)fztBeamDraw(q);
 for(const e of F.fx){const u=1-e.life/e.max;fztSprite(e.key,e.x,e.y,(e.a||0)+u*(e.spin||0),e.s*(.7+u*.65),1-u);}
 ctx.restore();return true;
};
fztBeamDraw=function(q){
 if(q._f17Flame){FURNACE17.draws.flame++;return av3Beam(ctx,q.x,q.y,q.a+Math.PI/2,q.len,q.width*2,'fire',q.clock||0,1,true);}
 if(q._f17Laser){const bank=FURNACE17.art?.laser,frames=bank?.frames;if(frames?.length){const a=frames[Math.floor((q.clock||0)*24)%frames.length];
   const i=frames.indexOf(a),root=FURNACE17.art.laser_root?.frames[i],tip=FURNACE17.art.laser_tip?.frames[i];
   if(root&&tip&&[a,root,tip].every(p=>XART.rdy(p.key))){const k=.85,join=tip.h-tip.pivot[1],bodyLength=Math.max(0,q.len-join*k),step=a.h*k;
    ctx.save();ctx.translate(q.x,q.y);ctx.rotate(q.a+Math.PI);ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=clamp(q.fade??1,0,1);
    ctx.save();ctx.beginPath();ctx.rect(-a.pivot[0]*k,-bodyLength,a.w*k,bodyLength);ctx.clip();
    for(let j=0;j<Math.ceil(bodyLength/step);j++)ctx.drawImage(XART.get(a.key),-a.pivot[0]*k,-(j+1)*step,a.w*k,step);
    ctx.restore();ctx.drawImage(XART.get(tip.key),-tip.pivot[0]*k,-q.len-tip.pivot[1]*k,tip.w*k,tip.h*k);
    ctx.drawImage(XART.get(root.key),-root.pivot[0]*k,-root.pivot[1]*k,root.w*k,root.h*k);
    ctx.restore();FURNACE17.draws.laser++;return true;}
  }}
 return FURNACE17.base.beamDraw.apply(this,arguments);
};
globalThis.BOF_FURNACE_ASSAULT={state:FURNACE17,warm:f17Warm,sockets:f17Sockets,tune:f17Tune};
