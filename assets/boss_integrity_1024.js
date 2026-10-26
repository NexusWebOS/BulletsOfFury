"use strict";
// Rendering corrections only. Native parts retain health, sockets, collisions,
// attacks, hit flashes and one defeat/progression owner.
const BI24={base:{rupture:d27ModuleRupture,frame:v18Frame},events:[],draws:{}};
for(const a of Object.values(BI24_ART.sheets))XART._src[a.key]=a.path;
for(const [name,a]of Object.entries(BI24_ART.banks))for(let f=0;f<a.count;f++){
 BOFX.cells['bi24_'+name+'_'+f]=['bi24_'+name,f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h];
 BOFX.cells['bi24_'+name+'_hit_'+f]=['bi24_'+name+'_hit',f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h];
}
BI24.cache=new Map();BI24.current=new WeakMap();BI24.damagePlates=new Map();
function bi24Keys(){return Object.values(BI24_ART.sheets).map(a=>a.key);}
function bi24Warm(){return bi24Keys().map(k=>XART.rdy(k)).every(Boolean);}
const bi24Load=stageLoadBegin,bi24Stage8Keys=v18Keys,bi24Stage8Warm=v18Warm;
stageLoadBegin=function(n,keys){return bi24Load.call(this,n,[...(keys||[]),...([5,8].includes(n)?bi24Keys():[])]);};
v18Keys=function(){return [...bi24Stage8Keys(),...bi24Keys()];};
v18Warm=function(){const old=bi24Stage8Warm();return bi24Warm()&&old;};
function bi24Sample(name,u=0){const a=BI24_ART.banks[name];return a?{a,f:Math.min(a.count-1,Math.floor(clamp(u,0,1)*(a.count-1)))}:null;}
function bi24DamagePlate(q,b){
 const phoenix=ph21Own(b),ids=phoenix?['cannonL','cannonR']:['left','right'],dead=ids.map(id=>!!b.parts.find(p=>p.id===id)?.destroyed);
 if(!dead.some(Boolean))return null;const {a,f}=q,key=a.key+':'+f+':'+dead.join(),cached=BI24.damagePlates.get(key);if(cached)return cached;
 const c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,0,0,a.w,a.h);const d=g.getImageData(0,0,a.w,a.h);
 for(let y=0;y<a.h;y++)for(let x=0;x<a.w;x++){
  const side=x<a.w/2?0:1;if(!dead[side])continue;
  if(phoenix){const at=a.sockets[f][side?'right':'left'];if(Math.abs(x/2-at[0])>=14||y/2<at[1]-34||y/2>at[1]+3)continue;}
  else if(x>224&&x<288)continue;
  const i=(y*a.w+x)*4,light=(d.data[i]*.3+d.data[i+1]*.59+d.data[i+2]*.11)*.48;d.data[i]=light;d.data[i+1]=light;d.data[i+2]=light*1.08;
 }
 g.putImageData(d,0,0);if(BI24.damagePlates.size>=24)BI24.damagePlates.delete(BI24.damagePlates.keys().next().value);BI24.damagePlates.set(key,c);return c;
}
function bi24Draw(q,b,size,rot=0){
 if(!q)return false;const {a,f}=q,flash=Math.max(b.flash||0,...(b.parts||[]).map(p=>p.flash||0),b._lastPart?.flash||0),key=flash>0?a.white:a.key;
 if(!XART.rdy(key))return false;const k=size/a.w;
 ctx.save();ctx.translate(b.x,b.y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;
 const damaged=flash>0?null:bi24DamagePlate(q,b);
 if(damaged)ctx.drawImage(damaged,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);
 else ctx.drawImage(XART.get(key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
 BI24.current.set(b,{...q,size,k,rot,x:b.x,y:b.y,key});BI24.draws[a.key]=(BI24.draws[a.key]||0)+1;return true;
}
function bi24PhoenixSocket(b,side,barrel=0){
 const q=bi24AttackPose(b,'phoenix'),a=q.a.sockets[q.f][side],Q=ph21State(b),k=360/256*Q.scale,c=Math.cos(Q.angle),s=Math.sin(Q.angle),dx=(a[0]-128+(barrel%2?4:-4))*k,dy=(a[1]-128)*k;
 return{x:b.x+dx*c-dy*s,y:b.y+dx*s+dy*c};
}
const bi24Talon=ph21TalonPoint;
ph21TalonPoint=function(v){return v._bi24?{x:v.x,y:v.y}:bi24Talon.apply(this,arguments);};
const bi24PhMuzzle=ph21Muzzle;
ph21Muzzle=function(b,id,barrel=0){return ph21Own(b)&&ph21State(b)?bi24PhoenixSocket(b,id==='cannonL'?'left':'right',barrel):bi24PhMuzzle.apply(this,arguments);};
function bi24AttackPose(b,actor){
 let phase='recover',u=1;
 if(actor==='dracodia'){
  const P=b._r30.v18.attack;
  if(P){if(P.t<P.tell){phase='wind';u=P.t/P.tell;}
   else{phase=P.type==='rb23-pincer'?'strike':'recover';u=(P.t-P.tell)/Math.max(.4,P.active);}}
 }else{
  const Q=ph21State(b),A=Q.action;
  if(A&&['volley','fan','lance'].includes(A.mode)){
   if(A.t<A.tell){phase='wind';u=A.t/A.tell;}
   else{phase='strike';u=(A.t-A.tell)/.36;}
  }else if(A&&['recede','corner'].includes(A.mode)){phase='wind';u=clamp(A.t/.6,0,1);}
  else if(A?.mode==='dive'){phase='strike';u=A.t/A.duration;}
  else {phase='recover';u=(1+Math.sin(Q.age*3))*.5;}
 }
 return bi24Sample(actor+'_'+phase,u);
}
const bi24Body=v18Body;
v18Body=function(b){
 if(rb23Host(b)&&b._r30.mode==='fight'){
  const N=b._r30.v18;if(rb23Arms(b).length)N.bi24Rolled=false;
  else if(N.attack?.type==='rb23-roll')N.bi24Rolled=true;
  if(!N.bi24Rolled&&bi24Draw(bi24AttackPose(b,'dracodia'),b,360))return;
 }
 if(bi24Plated(b))return v19Body(b);
 return bi24Body.apply(this,arguments);
};
// Reassemble the existing authored ghost/colossus frame on its original canvas.
// Those plates were cut for targeting, not designed as independently rotating limbs.
const bi24NativeBody=v19Body,bi24NativeRig=v18Rig;
BI24.plates=new Map();
function bi24Plated(b){return v18Owned(b)&&!v19Native(b)&&['ghost','colossus'].includes(v18Model(b))&&b._r30.mode==='fight';}
function bi24PlateScale(b){const P=b._r30.v18.attack;return v18Size(b)/320*(P?._dr21?P.depth||1:b._r30.v18.archiveDepth||1);}
v18Rig=function(b){
 if(!bi24Plated(b))return bi24NativeRig.apply(this,arguments);
 const frame=v18Frame(b),k=bi24PlateScale(b);
 return b.parts.filter(p=>!p.destroyed).map(p=>{const a=frame[p.id],q=a.bounds;return{p,key:a.key,a,anchor:[160,160],ax:b.x,ay:b.y,x:b.x+((q[0]+q[2])/2-160)*k,y:b.y+((q[1]+q[3])/2-160)*k,w:(q[2]-q[0])*k,h:(q[3]-q[1])*k,k,rot:0,alpha:1,layer:p.id,spec:{role:p.id==='core'?'core':'weapon'},z:0};});
};
v19Body=function(b){
 if(!bi24Plated(b))return bi24NativeBody.apply(this,arguments);
 const frame=v18Frame(b),rows=['left','core','right'].map(id=>frame[id]).filter(Boolean);
 if(!rows.every(a=>XART.rdy(a.key)))return;
 const key=rows.map(a=>a.key).join('|');let plate=BI24.plates.get(key);
 if(!plate){const c=document.createElement('canvas');c.width=c.height=320;const g=c.getContext('2d');for(const a of rows)g.drawImage(XART.get(a.key),0,0);const white=document.createElement('canvas');white.width=white.height=320;const w=white.getContext('2d');w.drawImage(c,0,0);w.globalCompositeOperation='source-in';w.fillStyle='#fff';w.fillRect(0,0,320,320);plate={c,white};BI24.plates.set(key,plate);}
 const flash=Math.max(b.flash||0,...b.parts.map(p=>p.flash||0)),k=bi24PlateScale(b);ctx.drawImage(flash>0?plate.white:plate.c,b.x-160*k,b.y-160*k,320*k,320*k);
 BI24.draws[v18Model(b)+'_connected_plate']=(BI24.draws[v18Model(b)+'_connected_plate']||0)+1;
};
const bi24Donor=v19DonorDraw,bi24Paint=v19Paint;
v19DonorDraw=function(b){const old=BI24.painting,done=BI24.painted;
 if(ph21Own(b)&&ph21State(b)){BI24.painting=b;BI24.painted=false;}
 try{return bi24Donor.apply(this,arguments);}finally{BI24.painting=old;BI24.painted=done;}
};
v19Paint=function(v,b){
 if(BI24.painting===b){if(!BI24.painted){const q=bi24AttackPose(b,'phoenix');BI24.painted=bi24Draw(q,b,360*ph21State(b).scale,ph21State(b).angle);}return;}
 return bi24Paint.apply(this,arguments);
};
const bi24PhRig=v19VolcanoRig;
function bi24Local(b,x,y){const Q=ph21Own(b)?ph21State(b):null,k=360/512*(Q?.scale||1),a=-(Q?.angle||0),c=Math.cos(a),s=Math.sin(a),dx=x-b.x,dy=y-b.y;return{x:(dx*c-dy*s)/k+256,y:(dx*s+dy*c)/k+256,k};}
function bi24World(b,x,y){const Q=ph21Own(b)?ph21State(b):null,k=360/512*(Q?.scale||1),a=Q?.angle||0,c=Math.cos(a),s=Math.sin(a);x-=256;y-=256;return{x:b.x+(x*c-y*s)*k,y:b.y+(x*s+y*c)*k};}
const BI24_ZONES={core:[256,256,72,90],head:[256,188,60,74],wingL:[123,218,130,160],wingR:[389,218,130,160],clawL:[218,326,64,74],clawR:[294,326,64,74]};
v19VolcanoRig=function(b){
 if(!ph21Own(b)||!ph21State(b))return bi24PhRig.apply(this,arguments);
 const q=bi24AttackPose(b,'phoenix'),Q=ph21State(b),out=[];
 for(const p of b.parts){if(p.destroyed)continue;let z=BI24_ZONES[p.id];
  if(p.id.startsWith('cannon')){const side=p.id==='cannonL'?'left':'right',a=q.a.sockets[q.f][side];z=[a[0]*2,a[1]*2-20,52,76];}
  if(!z)continue;const at=bi24World(b,z[0],z[1]);out.push({p,key:q.a.key,a:q.a,anchor:q.a.pivot,ax:b.x,ay:b.y,k:360/512*Q.scale,rot:Q.angle,...at,w:z[2]*360/512*Q.scale,h:z[3]*360/512*Q.scale,alpha:1,layer:p.id,spec:p.spec,z:0,_bi24:true});
 }
 return out;
};
const bi24Eye=rb23Eye,bi24Point=rb23PartPoint;
rb23Eye=function(b){return rb23Host(b)&&rb23Arms(b).length?{x:b.x,y:b.y}:bi24Eye.apply(this,arguments);};
rb23PartPoint=function(b,p,muzzle=false){
 if(!rb23Host(b)||!rb23Arms(b).length)return bi24Point.apply(this,arguments);
 const q=bi24AttackPose(b,'dracodia'),a=q.a.arms[q.f][p.id];return a?bi24World(b,a[0]*2,(a[1]+(muzzle?12:0))*2):{x:b.x,y:b.y};
};
const bi24At=r30At;

function bi24Mask(q){const {a,f}=q,k=a.key+':'+f;let m=BI24.cache.get(k);if(m)return m;
 if(!XART.rdy(a.key))return null;const c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d',{willReadFrequently:true});
 g.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,0,0,a.w,a.h);m=g.getImageData(0,0,a.w,a.h).data;BI24.cache.set(k,m);return m;
}
r30At=function(b,x,y){
 if(ph21Own(b)&&ph21State(b)&&b._r30.mode==='fight'){
  if(!r30Live(b)||b._noHit)return null;const q=bi24AttackPose(b,'phoenix'),m=bi24Mask(q),at=bi24Local(b,x,y),px=Math.floor(at.x),py=Math.floor(at.y);
  if(!m||px<0||py<0||px>=q.a.w||py>=q.a.h||m[(py*q.a.w+px)*4+3]<48)return null;
  const X=px/2,Y=py/2,sockets=q.a.sockets[q.f];let id='core';
  for(const side of ['left','right']){const at=sockets[side];if(Math.abs(X-at[0])<13&&Y>at[1]-34&&Y<at[1]+3)id=side==='left'?'cannonL':'cannonR';}
  if(id==='core'){if(Y<117&&X>115&&X<141)id='head';else if(X<112&&Y<145)id='wingL';else if(X>144&&Y<145)id='wingR';else if(Y>150&&Y<185)id=X<128?'clawL':'clawR';}
  const part=ph21Part(b,id);return part&&ph21Vulnerable(b,part)?part:null;
 }
 if(rb23Host(b)&&rb23Arms(b).length&&b._r30.mode==='fight'){
  if(!r30Live(b)||b._noHit)return null;const q={...bi24AttackPose(b,'dracodia'),k:360/512},m=bi24Mask(q);if(!m)return null;
  const px=Math.floor((x-b.x)/q.k+q.a.pivot[0]),py=Math.floor((y-b.y)/q.k+q.a.pivot[1]);
  if(px<0||py<0||px>=q.a.w||py>=q.a.h||m[(py*q.a.w+px)*4+3]<48)return null;
  const id=x<b.x-48?'left':x>b.x+48?'right':'core',p=b.parts.find(p=>p.id===id);return p&&!p.destroyed&&p.hp>0?p:null;
 }
 return bi24At.apply(this,arguments);
};
const bi24Blue=ha21Blue;
ha21Blue=function(b){
 const old=bi24Blue.apply(this,arguments),h=b?._hammer;
 if(!ht23Own(b)||h.hammerDestroyed||h.hb20Pickup||h.hc11Counter||b._hammerTime&&b._hammerTime.mode!=='attack')return old;
 let name=null,u=0;
 if(['storm_raise','storm_rebuild','recharge1002','nova_charge','nova_release'].includes(h.state)||h.recovery?.status==='charging'){name='hold';u=h.t/1.2;}
 else if(['spell','spell_blast'].includes(h.state)){name='cast';u=h.state==='spell'?h.t/1.1:1;}
 else if(['hammer_stun','storm_stun','fr_stun'].includes(h.state)){name='kneel';u=h.t/.8;}
 if(!name)return old;
 const suffix=hf22Red(b)?'_red':fr27Armor(b)?.activated&&fr27Armor(b)?.hp>0?'_armor':'',bank='chronos_'+name+suffix,q=bi24Sample(bank,u);
 if(!q)return old;const a={...q.a,key:'bi24_'+bank+'_'+q.f,white:'bi24_'+bank+'_hit_'+q.f,tip:q.a.tips[q.f],_hf22:true,_bi24:true};
 if(!XART.rdy(a.key)||!XART.rdy(a.white))return old;
 return {a,k:1,rot:0,kind:'bi24_'+bank};
};
const bi24HammerDraw=hammerBossDraw;
hammerBossDraw=function(b){
 if(ht23Own(b)&&['hammer_stun','storm_stun','fr_stun'].includes(b._hammer.state)){
  const q=ha21Blue(b);if(q?.a._bi24){hammerBossAtmosphereDraw(b);ha21Body(b,q);hammerStunEffectsDraw(b);hammerRecoveryBurstDraw(b);return;}
 }
 return bi24HammerDraw.apply(this,arguments);
};
const bi24Rupture=v19Rupture,bi24HostRupture=v18Rupture;
function bi24WholeRupture(b,p){
 const at=rb23Host(b)?rb23PartPoint(b,p):(ph21Own(b)?v19VolcanoRig(b):v18Rig(b)).find(v=>v.p===p)||b;
 d27ModuleRupture(b,p,{x:at.x,y:at.y,w:55,h:65},'purple');
 BI24.events.push({type:'connected-actor-module-disabled',part:p.id});
}
v19Rupture=function(b,p){if(ph21Own(b)||rb23Host(b)||bi24Plated(b))return bi24WholeRupture(b,p);return bi24Rupture.apply(this,arguments);};
v18Rupture=function(b,p){if(ph21Own(b)||rb23Host(b)||bi24Plated(b))return bi24WholeRupture(b,p);return bi24HostRupture.apply(this,arguments);};
d27ModuleRupture=function(owner,part,shape,palette){
 if(run.stage===8&&owner?._r30&&shape?.debrisImage){
  const {debrisImage,...clean}=shape;
  BI24.events.push({type:'authored-rupture-without-png-tile',part:part?.id});
  return BI24.base.rupture.call(this,owner,part,clean,palette);
 }
 return BI24.base.rupture.apply(this,arguments);
};
v18Frame=function(b){
 if(!rb23Host(b)||b._r30.mode!=='fight')return BI24.base.frame.apply(this,arguments);
 // 0..5 and13..15 are the conversion into/out of the body, not idle motion.
 // Keep the established living anatomy, ping-pong the settled motion poses.
 const N=b._r30.v18,clock=b._r30.clock,n=Math.floor(clock*8)%12,f=6+(n<7?n:12-n);
 N._bi24Frame=f;b._r30.clock=f/V18_ART.models.infused.fps+.00001;
 try{return BI24.base.frame.apply(this,arguments);}finally{b._r30.clock=clock;}
};
