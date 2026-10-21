"use strict";
/* PixelLab-authored avian replacement for the Stage8 volcano copy only.
   Native Furnace clocks, warnings, HP pools and damage remain authoritative. */
const PH20={base:{rig:v19VolcanoRig,enter:v18Enter,shot:fztShot,projectile:furnaceProjectileDraw,draw:v19DonorDraw,beam:fztBeamDraw},draws:{},identity:'Corrupted Fire Phoenix'};
if(PH20_ART.beam)PH20_ART.beam.footprintWidth=Math.max(PH20_ART.beam.bounds[2]-PH20_ART.beam.bounds[0],...(PH20_ART.beam.frames||[]).map(a=>a.bounds[2]-a.bounds[0]));
Object.assign(VP23_ART,{parts:PH20_ART.parts,socket:PH20_ART.socket,flame:PH20_ART.flame});
VH19_ART.banks=PH20_ART.head.banks;
for(const a of [...Object.values(PH20_ART.parts),PH20_ART.socket,...Object.values(PH20_ART.head.banks).flat(),...['feather','plume','beam'].map(k=>PH20_ART[k]).filter(Boolean)])XART._src[a.key]=a.path;
for(const a of [...Object.values(PH20_ART.motion||{}).flat(),...['plume','beam'].flatMap(k=>PH20_ART[k]?.frames||[])])XART._src[a.key]=a.path;
V19_ART.volcanoMuzzles=PH20_ART.muzzles;
for(const id of ['left','right','head','core','legL','legR'])V19_ART.volcanoMounts[id]=(PH20_ART.parts[id==='core'?'reactor':id==='legL'?'thighL':id==='legR'?'thighR':id]||PH20_ART.parts.torso).anchor;
const ph20Keys=v18Keys,ph20Warm=v18Warm;
function ph20ExtraKeys(){return [...['feather','plume','beam'].map(k=>PH20_ART[k]?.key).filter(Boolean),...Object.values(PH20_ART.motion||{}).flat().map(a=>a.key),...['plume','beam'].flatMap(k=>(PH20_ART[k]?.frames||[]).map(a=>a.key))];}
v18Keys=function(){return [...ph20Keys(),...ph20ExtraKeys()];};
v18Warm=function(){let ready=ph20Warm();for(const key of ph20ExtraKeys())if(!XART.rdy(key))ready=false;return ready;};
v18Enter=function(b){const out=PH20.base.enter.apply(this,arguments);if(vp23Own(b)){b.name=PH20.identity;for(const p of b.parts)p.spec.label=({shoulderL:'Left wing armor',shoulderR:'Right wing armor',left:'Left furnace cannon',right:'Right furnace cannon',ventL:'Left fire wing',ventR:'Right fire wing',legL:'Left talon / tail',legR:'Right talon / tail',core:'Furnace heart',head:'Phoenix skull'})[p.id]||p.id;}return out;};
v19VolcanoRig=function(b){if(!vp23Own(b)||gd4Create(b,2).p._fz.phase==='head')return PH20.base.rig.apply(this,arguments);
 if(!b.parts.every(p=>p._vp23))vp23Modules(b);const P=vp23Pose(b),{F,N}=P,k=v18Size(b)/320,out=[],c=Math.cos(P.root),s=Math.sin(P.root);
 const root=at=>({x:b.x+(at[0]-160)*k*c-(at[1]-160)*k*s,y:b.y+(at[0]-160)*k*s+(at[1]-160)*k*c});
 const add=(id,at,rot=P.root,scale=1)=>{const bank=PH20_ART.motion?.[id],index=P.live?(id==='reactor'?Math.round(P.charge*8):Math.floor(P.t*8)%8):0,a=bank?.[index]||VP23_ART.parts[id],p=b.parts.find(q=>q.id===a.owner);if(!p||p.destroyed)return null;const anchor=a.anchor,q=a.bounds,K=k*scale,dx=((q[0]+q[2])/2-anchor[0])*K,dy=((q[1]+q[3])/2-anchor[1])*K,cc=Math.cos(rot),ss=Math.sin(rot),v={p,key:a.key,a,anchor,ax:at.x,ay:at.y,k:K,rot,x:at.x+dx*cc-dy*ss,y:at.y+dx*ss+dy*cc,w:(q[2]-q[0])*K,h:(q[3]-q[1])*K,alpha:1,layer:id,spec:{role:p.spec.role},_vp23:true,z:out.length};out.push(v);return v;};
 // Slow bilateral wingbeats become a deliberate draw-back on charge. All
 // feather sections follow their physical wing root rather than orbiting it.
 for(const tag of ['L','R']){const sign=tag==='L'?-1:1,wing=P.root+sign*((P.live?Math.sin(P.t*2.6)*.07:0)-P.charge*.15-P.fold*1.05),a=VP23_ART.parts['upper'+tag],at=root(a.anchor);
  const inner=add('upper'+tag,at,wing);const outerAnchor=inner?vp23Point(inner,VP23_ART.parts['vent'+tag].anchor):root(VP23_ART.parts['vent'+tag].anchor);add('vent'+tag,outerAnchor,wing+sign*(-P.fold*.40+(P.live?Math.sin(P.t*2.6-.35)*.045:0)));
 }
 add('torso',root(VP23_ART.parts.torso.anchor));
 for(const tag of ['L','R']){const sign=tag==='L'?-1:1,haunch=add('thigh'+tag,root(VP23_ART.parts['thigh'+tag].anchor),P.root+sign*P.fold*.45);if(haunch){const talon=vp23Point(haunch,VP23_ART.parts['foot'+tag].anchor);add('foot'+tag,talon,P.root-sign*P.fold*.9);const tail=vp23Point(haunch,VP23_ART.parts['flare'+tag].anchor);add('flare'+tag,tail,P.root+sign*(P.fold*.65+(P.live?Math.sin(P.t*4)*.04:0)));}}
 for(const side of ['left','right']){const tag=side==='left'?'L':'R',sign=side==='left'?-1:1;add('shoulder'+tag,root(VP23_ART.parts['shoulder'+tag].anchor));
  const a=VP23_ART.parts[side],tip=V19_ART.volcanoMuzzles[side],aim=P.root+(P.live?F.arm[side]?.a||0:0),base=Math.atan2(a.anchor[0]-tip[0],tip[1]-a.anchor[1]);let at=root(a.anchor),rot=P.live?aim-base:P.root;
  const Q=N.swipe?.q;if(Q?.id===side){at={x:b.x+Q.off.x,y:b.y+Q.off.y};rot=v19SwipeRotation(b,side,rot);}else if(P.live)at=fztPt(at.x,at.y,aim,-P.recoil*6*k);
  add(side,at,rot);
 }
 add('reactor',root(VP23_ART.parts.reactor.anchor),P.root,1+P.heat*.035);
 add('head',root(VP23_ART.parts.head.anchor),P.root);
 return out.sort((a,b)=>Number(b.layer===b.p.id)-Number(a.layer===a.p.id));
};
// The two feather plumes are tail ribbons in this anatomy. Preserve their
// authored silhouettes, fixed pivots and hit flash instead of the old chimney FX.
const ph20Paint=v19Paint;
const ph20Socket=vp23Socket;
vp23Socket=function(p,id){if(vp23Proxy(p)&&['ventL','ventR'].includes(id)){const v=v19VolcanoRig(p._gp4Host).find(v=>v.layer===id);return v?vp23Point(v,v.anchor):null;}return ph20Socket.apply(this,arguments);};
const ph20Emitter=vp23Emitter;
vp23Emitter=function(F,x,y){if(vp23Own(boss)&&gd4Create(boss,2).p._fz===F&&F.phase==='core'&&F.attack==='rotor'){const id=(x-boss.x)*Math.cos(F.a)+(y-boss.y)*Math.sin(F.a)<0?'ventL':'ventR';return vp23Socket(gd4Create(boss,2).p,id)||{x,y};}return ph20Emitter.apply(this,arguments);};
v19Paint=function(v,b){if(!vp23Own(b)||!v._vp23||!v.layer.startsWith('flare'))return ph20Paint.apply(this,arguments);VP23.base.paint.call(this,v,b);VP23.draws[v.layer]=(VP23.draws[v.layer]||0)+1;};
fztShot=function(p){const first=eBullets.length,result=PH20.base.shot.apply(this,arguments);if(vp23Proxy(p))for(const q of eBullets.slice(first)){q._ph20Feather=true;q._ph20Owner=p._gp4Host;}return result;};
furnaceProjectileDraw=function(q){const a=PH20_ART.feather;if(!q._ph20Feather||!a||!XART.rdy(a.key))return PH20.base.projectile.apply(this,arguments);ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(q.x,q.y);ctx.rotate(Math.atan2(q.vy,q.vx)+Math.PI/2);
 if(q._pt11Wave){const size=(q.h||34)*64/Math.max(1,a.bounds[3]-a.bounds[1]);for(let i=0;i<7;i++)ctx.drawImage(XART.get(a.key),((i-3)/3)*(q.w||112)*.42-size/2,-size/2,size,size);PH20.draws.featherWall=(PH20.draws.featherWall||0)+1;}
 else{const size=Math.max(30,(q.w||12)*3);ctx.drawImage(XART.get(a.key),-size/2,-size/2,size,size);}ctx.restore();PH20.draws.feather=(PH20.draws.feather||0)+1;return true;};
function ph20Plume(at,a,heat=1){const source=PH20_ART.plume,art=source?.frames?.[Math.floor((gd4Create(boss,2).p._fz.t||0)*24)%16]||source;if(!art||!XART.rdy(art.key))return;const k=.32+heat*.18;ctx.save();ctx.translate(at.x,at.y);ctx.rotate(a+Math.PI);ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(art.key),-64*k,-64*k,128*k,128*k);ctx.restore();PH20.draws.plume=(PH20.draws.plume||0)+1;}
fztBeamDraw=function(q){const source=PH20_ART.beam,a=source?.frames?.[Math.floor(q._ph20Time*24)%16]||source;if(!q._ph20||!a||!XART.rdy(a.key))return PH20.base.beam.apply(this,arguments);const width=Math.max(5,q.width*2),scale=width/Math.max(12,source.footprintWidth),tile=a.h*scale,im=XART.get(a.key),length=q.len;ctx.save();ctx.translate(q.x,q.y);ctx.rotate(q.a);ctx.imageSmoothingEnabled=false;ctx.beginPath();ctx.rect(-width*1.8,0,width*3.6,length);ctx.clip();for(let y=-tile+(q._ph20Time*150)%tile;y<length;y+=tile)ctx.drawImage(im,-a.w*scale/2,y,a.w*scale,a.h*scale);ctx.restore();PH20.draws.beam=(PH20.draws.beam||0)+1;};
v19DonorDraw=function(b){if(!vp23Own(b))return PH20.base.draw.apply(this,arguments);const F=gd4Create(b,2).p._fz;for(const q of F.beams){q._ph20=true;q._ph20Time=F.t;}
 // Native flame damage is drawn through the same PixelLab beam bank. Suppress
 // only that one visual call synchronously; controller/collisions are untouched.
 const beam=av3Beam;av3Beam=function(g,x,y,a,len,width){const q=F.beams.find(v=>v.kind==='flame'&&Math.hypot(v.x-x,v.y-y)<.01);if(q&&PH20_ART.beam)return fztBeamDraw(q);return beam.apply(this,arguments);};
 try{PH20.base.draw.apply(this,arguments);}finally{av3Beam=beam;}
 for(const side of ['left','right'])if(!vp23Missing(b,side)){const q=F.beams.find(v=>v._vp23Emitter===side),flash=F.fx.some(v=>v.key==='fzt_cannon_flash'&&side==='right');if(q||flash)ph20Plume(furnaceMuzzle(gd4Create(b,2).p,side),q?.a??F.a+F.arm[side].a,1);}
 if(F.phase==='core'&&F.charge>.1&&!vp23Missing(b,'core'))ph20Plume(vp23Socket(gd4Create(b,2).p,'reactor'),Math.PI,F.charge);
};
globalThis.BOF_DRACODIA_PHOENIX={state:PH20,rig:v19VolcanoRig,warm:()=>v18Warm()};
