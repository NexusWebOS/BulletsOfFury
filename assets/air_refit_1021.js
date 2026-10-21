"use strict";
/* PixelLab hull/motion replacements. Fixed128 cells, one fuselage pivot and
   shared textures for the center/port/starboard modules. Native deaths stay. */
const AF21={base:{pose:air13Pose,blit:air13Blit,rebel:air13DrawRebel,ship:fr27RebelDrawShip,
 enemy:drawEnemy,get:XART.get,touch:XART._touch,tint:xartTint,load:stageLoadBegin,muzzle:wm26Emit,tick:rebelSquadTick},
 aliases:new Map(),sourceAliases:new Map(),tags:new WeakMap(),tints:new Map(),actor:null,painting:null,draws:0,records:[]};
for(const a of Object.values(AF21_ART.sheets))XART._src[a.key]=a.path;
for(const[id,M]of Object.entries(AF21_ART.models)){for(const alias of M.aliases)AF21.aliases.set(alias,{id,M});AF21.aliases.set(id,{id,M});}
for(const[alias,id]of Object.entries(AF21_ART.reusedFamilies))if(AF21_ART.models[id])AF21.aliases.set(alias,{id,M:AF21_ART.models[id],palette:alias.startsWith('stealth_')?({stealth_red:'#ff333f',stealth_green:'#43db59',stealth_orange:'#ff9d35'})[alias]:alias.startsWith('l6v_r')?'#295ce3':alias.startsWith('l6v_b')?'#142943':null});
// Retired flight plates must not remain a hidden decode/readiness dependency.
// Redirect only numeric flight/damage frames. Destruction reels and weapon art
// retain their own source keys and native lifetime.
for(const M of Object.values(AF21_ART.models))for(const source of Object.values(M.sourceKeys||{})){
 if(typeof source!=='string'||!source)continue;
 const family=source.replace(/_\d+$/,'_');AF21.sourceAliases.set(source,M.banks.idle.key);
 if(family!==source)for(const key of Object.keys(XART._src))if(key.startsWith(family)&&/^\d+$/.test(key.slice(family.length)))AF21.sourceAliases.set(key,M.banks.idle.key);
}
XART._touch=function(key){return AF21.base.touch.call(this,AF21.sourceAliases.get(key)||key);};
function af21Pose(id,kind='idle',value=0){const model=AF21.aliases.get(id);if(!model)return null;const M=model.M,B=M.banks[kind]||M.banks.idle;if(!XART.rdy(B.key))return null;
 const f=kind==='idle'?0:Math.floor(((value%1+1)%1)*B.frames)%B.frames;
 const d=AIR13.aliases.get(id)||AM13_ART[id]||M;return{_af21:true,id:model.id,kind,M,d,m:B,f,key:B.key,im:XART.get(B.key),palette:model.palette,rotation:0};}
function af21Tint(p,color){const key=p.key+'|'+p.f+'|'+color;let im=AF21.tints.get(key);if(im)return im;im=document.createElement('canvas');im.width=im.height=128;const g=im.getContext('2d'),c=p.m.cells[p.f];g.drawImage(p.im,...c,0,0,128,128);
 if(color===p.palette){const data=g.getImageData(0,0,128,128),d=data.data,hex=color.slice(1),rgb=[0,2,4].map(n=>parseInt(hex.slice(n,n+2),16)),peak=Math.max(...rgb,1),target=rgb.map(n=>n/peak);
  for(let i=0;i<d.length;i+=4){if(!d[i+3])continue;const v=Math.max(d[i],d[i+1],d[i+2]),lo=Math.min(d[i],d[i+1],d[i+2]),sat=(v-lo)/Math.max(1,v);if(sat<.22||v<28)continue;
   const white=Math.max(0,(v-205)/50);for(let k=0;k<3;k++)d[i+k]=Math.round(v*(target[k]*(1-white)+white));}g.putImageData(data,0,0);
 }else{g.globalCompositeOperation='source-atop';g.fillStyle=color;g.fillRect(0,0,128,128);}
 if(AF21.tints.size>=128)AF21.tints.delete(AF21.tints.keys().next().value);AF21.tints.set(key,im);return im;}
function af21Draw(p,x,y,span,alpha=1,flash=null,module=null){const size=span*128/p.M.span,c=p.m.cells[p.f],palette=flash||p.palette,im=palette?af21Tint(p,palette):p.im,painting=AF21.painting;
 AF21.painting=true;ctx.save();try{ctx.translate(x,y);ctx.rotate(p.rotation||0);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 if(module!=null){const r=p.m.modules[module],sx=palette?r[0]:c[0]+r[0],sy=palette?r[1]:c[1]+r[1];ctx.drawImage(im,sx,sy,r[2],r[3],(r[0]-64)*size/128,(r[1]-64)*size/128,r[2]*size/128,r[3]*size/128);}
 else if(palette)ctx.drawImage(im,-size/2,-size/2,size,size);else ctx.drawImage(im,...c,-size/2,-size/2,size,size);
 }finally{ctx.restore();AF21.painting=painting;}AF21.draws++;if(AF21.currentEnemy)AF21.currentEnemy._af21Rendered={id:p.id,kind:p.kind,frame:p.f,key:p.key};return true;}
air13Pose=function(id,kind='heading',value=Math.PI/2){
 if(AF21.currentEnemy&&AF21.requestPose&&AF21.aliases.get(id)?.id===AF21.requestPose.id)return{...AF21.requestPose,rotation:kind==='heading'?value-Math.PI/2:0};
 const q=AF21.actor,A=q?.rg4?.act;let k=kind==='roll'?'roll':'idle',v=kind==='roll'?value:0,rotation=kind==='heading'?value-Math.PI/2:0;
 if(q){if(q.frSomersault&&q.evadeT>0){k='somer';v=1-q.evadeT/.38;}
  else if(A?.kind==='depthram'&&['fire','recover'].includes(A.phase)){k='somer';v=A.phase==='fire'?.12+Math.min(.06,A.t*.06):.20+Math.min(.79,A.t/1.3*.79);}
  else if(kind!=='roll'&&(Math.abs((q.rfHeading??Math.PI/2)-Math.PI/2)>.08||q._rd21From&&rg4State()?.rd21?.fleet)){k='drift';v=(q.t||0)/1.1;}
  else if(kind!=='roll'&&(q._ra4GunFlash>0||q._rg4Muzzle>0||q.rg4?.launchFlash>0||A?.phase==='fire')){k='attack';v=(q.t||0)*2.5;}}
 const p=af21Pose(id,k,v);if(!p)return AF21.base.pose.apply(this,arguments);p.rotation=rotation;return p;};
air13Blit=function(p,x,y,span,alpha=1,flash=null){if(p?._af21)return af21Draw(p,x,y,span,alpha,flash);return AF21.base.blit.apply(this,arguments);};
air13DrawRebel=function(q,opt={}){const old=AF21.actor;AF21.actor=q;const somer=q.frSomersault;
 if(q.key==='nyx'&&!q._rd21Cloak&&q._ra7Reveal>0)opt={...opt,alpha:lerp(.14,1,clamp(1-q._ra7Reveal/.55,0,1))};
 // The retired helper's guard skipped true somersault banks; keep its module
 // clips and flash path while the new pose selector supplies those frames.
 if(somer&&q.evadeT>0)q.frSomersault=false;AF21.somer=somer;
 try{return AF21.base.rebel.call(this,q,opt);}finally{q.frSomersault=somer;AF21.somer=false;AF21.actor=old;}};
const af21PoseSomer=air13Pose;
air13Pose=function(id,kind,value){if(AF21.somer&&AF21.actor?.evadeT>0){const p=af21Pose(id,'somer',1-AF21.actor.evadeT/.38);if(p)return p;}return af21PoseSomer.apply(this,arguments);};
fr27RebelDrawShip=function(q){const old=AF21.actor;AF21.actor=q;try{return AF21.base.ship.apply(this,arguments);}finally{AF21.actor=old;}};
rebelSquadTick=function(b,dt){const r=AF21.base.tick.apply(this,arguments);for(const q of b._rebels.ships){if(q.evadeT>0&&!(q._af21Evade>0))q.frSomersault=(q.i+(q.rg4?.n||0))%3===1;q._af21Evade=q.evadeT;}return r;};
wm26Emit=function(owner){if(owner&&AF21.aliases.has(owner.type||owner.key))owner._af21FireAt=efxClock;return AF21.base.muzzle.apply(this,arguments);};
XART.get=function(key){const im=AF21.base.get.apply(this,arguments);if(im)AF21.tags.set(im,{key});return im;};
xartTint=function(key,color){const im=AF21.base.tint.apply(this,arguments);if(im)AF21.tags.set(im,{key,color});return im;};
drawEnemy=function(e){const model=AF21.aliases.get(e.type);if(!model||e._bob20||e.dead||e._dyingT!=null)return AF21.base.enemy.apply(this,arguments);
 const now=efxClock;if(!e._tut&&Number.isFinite(e.fireCd)&&e.fireCd>(e._af21LastCd??e.fireCd)+.04)e._af21FireAt=now;e._af21LastCd=e.fireCd;
 const request=e._air13Motion,roll=request?.kind==='roll'||e._barrelT>0,somer=request?.kind==='somer',kind=roll?'roll':somer?'somer':now-(e._af21FireAt??-999)<.4?'attack':Math.abs(e.vx||0)>.15||Math.abs(e.spin||0)>.08?'drift':'idle';
 const phase=roll||somer?(request?request.t/request.dur:1-e._barrelT/.72):kind==='attack'?(now-e._af21FireAt)/.4:now/1.15,p=af21Pose(e.type,kind,phase);
 if(!p)return AF21.base.enemy.apply(this,arguments);const original=ctx.drawImage;let replaced=false;
 function replaceHull(im,...args){const tag=AF21.tags.get(im),key=tag?.key||'';if(AF21.painting)return original.call(this,im,...args);
  const [dx,dy,dw,dh]=args.slice(-4),cx=dx+dw/2,cy=dy+dh/2;
  const exact=key===(model.M.sourceKeys?.[e.type]||''),eligible=exact||(!replaced&&im?.width>=32&&im?.height>=32&&Math.max(Math.abs(dw),Math.abs(dh))>=Math.max(e.w||32,e.h||32)*.65&&this.globalAlpha>=.75&&this.globalCompositeOperation==='source-over'&&(Math.hypot(cx-e.x,cy-e.y)<Math.max(e.w||32,e.h||32)*.55||Math.hypot(cx,cy)<20));
  if(!eligible)return original.call(this,im,...args);replaced=true;ctx.drawImage=original;
  try{const d=AIR13.aliases.get(e.type),span=Math.max(e.w||32,e.h||32)*(d?.nativeRatios?.[e.type]||1);af21Draw(p,cx,cy,span,1,tag?.color||(e.flash>0?hitFlashColor(e):null));e._af21Rendered={id:model.id,kind,frame:p.f,key:p.key};}
  finally{ctx.drawImage=replaceHull;}return;
 }
 const previous=AF21.currentEnemy,previousPose=AF21.requestPose;AF21.currentEnemy=e;AF21.requestPose=p;ctx.drawImage=replaceHull;
 try{return AF21.base.enemy.apply(this,arguments);}finally{ctx.drawImage=original;AF21.currentEnemy=previous;AF21.requestPose=previousPose;}
};
stageLoadBegin=function(n,keys){const extra=[];for(const M of Object.values(AF21_ART.models))if(M.stages.includes(n))for(const B of Object.values(M.banks))extra.push(B.key);return AF21.base.load.call(this,n,[...(keys||[]),...extra]);};
globalThis.BOF_AIR_REFIT={state:AF21,art:AF21_ART,pose:af21Pose,draw:af21Draw};
