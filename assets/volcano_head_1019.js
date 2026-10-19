"use strict";
/* Detached Stage8 symbiote head: generated turning poses and physical eye lamps.
   The native Furnace controller still owns timing, widths, damage and recovery. */
const VH19={base:{rig:v19VolcanoRig,paint:v19Paint,at:v19AtRect,combat:furnaceHeadCombat,keys:v18Keys,warm:v18Warm,load:stageLoadBegin},draws:{},version:'volcano-head-1019'};
function vh19Own(b){return !window.VH19_OFF&&v19Native(b)&&b._r30.v18.form===2&&gd4Create(b,2).p._fz.phase==='head';}
function vh19Keys(){return Object.values(VH19_ART.banks).flatMap(v=>v.map(a=>a.key));}
for(const bank of Object.values(VH19_ART.banks))for(const a of bank)XART._src[a.key]=a.path;
function vh19Warm(){let ready=true;for(const key of vh19Keys())if(!XART.rdy(key))ready=false;return ready;}
v18Keys=function(){return [...VH19.base.keys(),...vh19Keys()];};
v18Warm=function(){const base=VH19.base.warm();return vh19Warm()&&base;};
stageLoadBegin=function(n,keys){return VH19.base.load.call(this,n,n===8?[...(keys||[]),...vh19Keys()]:keys);};
function vh19Descriptor(b){
 if(!vh19Own(b))return null;const F=gd4Create(b,2).p._fz,Q=F._v19Head||{phase:'charge',roll:0,charge:0},C=f17Tune(),spin=Q.phase==='spin';
 const bank=VH19_ART.banks[spin?'spin':'charge'];let index=0;
 if(spin){let nearest=Infinity;for(let i=0;i<bank.length;i++){const d=Math.abs(fztWrap(Q.roll-bank[i].angle));if(d<nearest){nearest=d;index=i;}}}
 else{const charge=Q.phase==='recover'?1-clamp((F.at-C.warm-C.active)/C.recover,0,1):Q.charge;index=Math.round(clamp(charge||0,0,1)*(bank.length-1));}
 const a=bank[index];if(!XART.rdy(a.key)){vh19Warm();return null;}
 return {a,index,bank:spin?'spin':'charge',rotation:fztWrap((Q.roll||0)-a.angle),k:v18Size(b)/320};
}
v19VolcanoRig=function(b){const rig=VH19.base.rig.apply(this,arguments),pose=vh19Descriptor(b);if(!pose)return rig;
 return rig.map(v=>{if(v.layer!=='head')return v;const {a,k,rotation:rot}=pose,q=a.bounds,dx=((q[0]+q[2])/2-64)*k,dy=((q[1]+q[3])/2-64)*k,c=Math.cos(rot),s=Math.sin(rot);
  return {...v,key:a.key,a,anchor:a.pivot,k,rot,x:v.ax+dx*c-dy*s,y:v.ay+dx*s+dy*c,w:(q[2]-q[0])*k,h:(q[3]-q[1])*k,_vh19:true,spec:{...v.spec,px:.5,py:.5}};});
};
v19AtRect=function(v,x,y){if(!v._vh19)return VH19.base.at.apply(this,arguments);const c=Math.cos(-v.rot),s=Math.sin(-v.rot),dx=x-v.ax,dy=y-v.ay,px=Math.floor((dx*c-dy*s)/v.k+64),py=Math.floor((dx*s+dy*c)/v.k+64),m=v18Mask(v.a);
 return !!(m&&px>=0&&py>=0&&px<v.a.w&&py<v.a.h&&m[py*v.a.w+px]>48);
};
v19Paint=function(v,b){if(!v._vh19)return VH19.base.paint.apply(this,arguments);
 // Charge brightness is already confined to the generated eye apertures.
 // Preserve the separate native owner/part hit flash below.
 if(ctx.globalCompositeOperation==='lighter')return;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(v.ax,v.ay);ctx.rotate(v.rot);const rect=[-64*v.k,-64*v.k,v.a.w*v.k,v.a.h*v.k];ctx.drawImage(XART.get(v.key),...rect);
 const flash=Math.max(v.p.flash||0,b.flash||0);if(flash>0){ctx.globalAlpha*=clamp(flash/.12,0,1)*.8;ctx.drawImage(xartTint(v.key,'#ffffff',1),...rect);}ctx.restore();VH19.draws[v.key]=(VH19.draws[v.key]||0)+1;
};
function vh19Sockets(b,origin=b){const pose=vh19Descriptor(b);if(!pose)return null;const {a,k,rotation}=pose,c=Math.cos(rotation),s=Math.sin(rotation);return a.eyes.map(([x,y])=>{x=(x-64)*k;y=(y-64)*k;return {x:origin.x+x*c-y*s,y:origin.y+x*s+y*c};});}
furnaceHeadCombat=function(p,dt){const b=p?._gp4Host;if(!b||!vh19Own(b))return VH19.base.combat.apply(this,arguments);const F=p._fz,nb=F.beams.length,nt=F.tells.length,result=VH19.base.combat.apply(this,arguments),sockets=vh19Sockets(b,p);
 if(!sockets)return result;
 const beams=F.beams.slice(nb).filter(q=>q.kind==='eye'),tells=F.tells.slice(nt),Q=F._v19Head;
 beams.forEach((q,i)=>{const at=sockets[i%2],end=fztPt(at.x,at.y,q.a,q.len);Object.assign(q,{x:at.x,y:at.y,ex:end.x,ey:end.y,_vh19:true});});
 tells.forEach((q,i)=>{const at=sockets[i%2],angle=Q.roll+(i%2?1:-1)*.14,len=Math.hypot(q.ex-q.x,q.ey-q.y),end=fztPt(at.x,at.y,angle,len);Object.assign(q,{x:at.x,y:at.y,ex:end.x,ey:end.y,_vh19:true});});
 return result;
};
