"use strict";
/* One whole native chassis, source-driven treads and two independent twin guns. */
const DC40={events:[],base:{set:s7mSet,next:s7mNext,tick:s7mTick,pose:s7mPose,bank:sw28Bank,blit:s7mBlit,muzzle:s7mMuzzle,hit:s7mHit,targets:s7mTargets,warnings:s7mWarnings,slug:sw28Slug,barrel:bh25DredgerBarrel,rupture:d27ModuleRupture,debris:d27ModuleDebrisDraw,intercept:enemyOrdnanceCanIntercept,ready:target17Ready,load:stageLoadBegin,update:updatePlay}};
for(const [id,a]of Object.entries(DC40_ART)){ER28_ART['dc40_'+id]=a;XART._src[a.key]=a.path;XART.rdy(a.key);}
function dc40Own(b){return run.stage===7&&!!b?._s7mod?.tank;}
function dc40Live(b,id){return dc40Own(b)&&!b.dead&&b._s7mod.mode!=='dead'&&(!id||s7mLive(b._s7mod,'gun').some(p=>p.id===id));}
function dc40Log(event,data={}){DC40.events.push({event,t:efxClock,...data});if(DC40.events.length>500)DC40.events.shift();}
stageLoadBegin=function(n,keys){if(n===7){l23FovWarm();Snd.prepare?.(['enemyMachineGunHeavy','bossWeaponCharge','combatToxic0927','jetDash']);}return DC40.base.load.call(this,n,[...(keys||[]),...(n===7?Object.values(DC40_ART).map(a=>a.key):[])]);};
enemyOrdnanceCanIntercept=function(q){return q?._dc40Owner?false:DC40.base.intercept.apply(this,arguments);};
target17Ready=function(b,ports){return dc40Own(b)&&b._s7mod.mode.startsWith('dc40-')?false:DC40.base.ready.apply(this,arguments);};
function dc40Cancel(b,id){for(const q of eBullets)if(q._dc40Owner===b&&(!id||q._dc40Gun===id))q.dead=true;}
s7mSet=function(b,mode){if(dc40Own(b)){
 // The displayed native budget includes the guns. A spent core cannot defeat them.
 if(mode==='dead'&&b._s7mod.core<=0&&s7mLive(b._s7mod,'gun').length)return;
 if(b._s7mod.core<=0&&['dc40-circle','er28-mortar'].includes(mode))mode='dc40-guns';
 if(['er23-surge','tank-charge'].includes(mode))mode='dc40-ram';
 if(['er28-guns','chain','aim','tank-cross','er23-pincer','pressure-salvo'].includes(mode))mode='dc40-guns';
 }
 const r=DC40.base.set.call(this,b,mode),M=b?._s7mod;if(!dc40Own(b))return r;
 M.dc40=null;M.dc40Recoil??={gunL:0,gunR:0};M.dc40Track??=0;
 if(mode.startsWith('dc40-')){
  const angle=Math.atan2(player.y-b.y-60,player.x-b.x);
  M.dc40={mode,cd:0,round:0,angle,from:{x:b.x,y:b.y},phase:'warn',hits:new Set()};
  M.warn=mode==='dc40-guns'?1.15:mode==='dc40-circle'?1.5:M.n===2?.85:1.05;
  if(mode==='dc40-ram'){
   const y=clamp(player.y-32,b.y+70,VH-115),x=clamp(player.x,camLeftX()+96,camRightX()-96),d=Math.hypot(x-b.x,y-b.y);
   Object.assign(M.dc40,{end:{x,y},back:{x:worldWidth()/2,y:VH*.46},dash:clamp(d/(M.n===2?760:640),.20,.42)});b._s4MiniSafe=true;
  }else b._s4MiniSafe=false;
  if(mode==='dc40-circle'){
   const count=16+M.n*2;M.dc40.angles=Array.from({length:count},(_,i)=>-Math.PI/2-5*Math.PI/6+i/(count-1)*5*Math.PI/3);
   combatAudio0927(b,'bossWeaponCharge',.55);
  }
  dc40Log('attack-start',{mode,x:b.x,y:b.y});
 }
 if(mode==='dead'){dc40Cancel(b);M.dc40Recoil={gunL:0,gunR:0};}
 return r;
};
s7mNext=function(b){if(!dc40Own(b))return DC40.base.next.apply(this,arguments);const M=b._s7mod;
 if(M.n===2&&!M.od&&b.hp<=b.maxhp*.5)return DC40.base.next.apply(this,arguments);
 M.dc40Choices=(M.dc40Choices||0)+1;const armed=s7mLive(M,'gun').length>0;
 let next;if(M.core<=0)next=M.er28Last==='dc40-guns'?'dc40-ram':'dc40-guns';
 else if(M.dc40Choices%3===1)next='dc40-circle';
 else if(M.er28Last!=='dc40-ram'&&Math.abs(player.x-b.x)<95)next='dc40-ram';
 else{const book=(armed?['dc40-guns','er28-mortar','dc40-ram']:['er28-mortar','dc40-ram']).filter(k=>k!==M.er28Last);next=book[Math.floor(er23Random(M)*book.length)];}
 M.seq++;M.er28Last=next;return s7mSet(b,next);
};
function dc40RecoilFrame(M,id){const t=M.dc40Recoil?.[id]||0;return t>.075?1:t>.04?2:t>0?3:0;}
function dc40GunAngle(b,id){const M=b._s7mod,A=M.dc40,side=id==='gunL'?-1:1;
 let a=(A?.mode==='dc40-guns'?A.angle:Math.atan2(player.y-b.y-70,player.x-b.x-side*43))-Math.PI/2;
 if(A?.mode==='dc40-guns'&&M.t>=M.warn)a+=Math.sin((M.t-M.warn)*2.4+side)*.12;
 a=side<0?clamp(a,-.14,.68):clamp(a,-.68,.14);return Math.round(a*64/TAU)*TAU/64;
}
s7mPose=function(b){const out=DC40.base.pose.apply(this,arguments);if(!dc40Own(b))return out;const M=b._s7mod;
 for(const p of out)if(p.id==='gunL'||p.id==='gunR'){
  p.x=p.id==='gunL'?-43:43;p.y=66;p.a=dc40GunAngle(b,p.id);p.w=p.h=76;
  p.dc40Frame=dc40RecoilFrame(M,p.id)*64+er28Dir(p.a);p.target={x:p.x,y:p.y};
 }return out;
};
sw28Bank=function(b,p){if(!dc40Own(b))return DC40.base.bank.apply(this,arguments);
 if(p.id==='gunL'||p.id==='gunR')return{name:'dc40_gun',f:p.dc40Frame};
 if(p.id==='body')return{name:'dc40_body',f:Math.floor(b._s7mod.dc40Track||0)};
 if(p.id==='core')return{name:'dc40_top',f:0};return DC40.base.bank.apply(this,arguments);
};
function dc40Barrel(b,id,barrel=0){const p=s7mPose(b).find(p=>p.id===id),q=s7mWorld(b,p),a=DC40_ART.gun,
 xy=a.sockets[p.dc40Frame][((barrel%2)+2)%2];return{x:q.x+xy[0]-a.pivot[0],y:q.y+xy[1]-a.pivot[1],a:Math.PI/2+p.a,angle:Math.PI/2+p.a,barrel};}
s7mMuzzle=function(b,id){if(!dc40Own(b))return DC40.base.muzzle.apply(this,arguments);
 if(id==='gunL'||id==='gunR')return dc40Barrel(b,id);
 if(id==='dorsal')return{...s7mWorld(b,{x:0,y:-62}),a:-Math.PI/2};return DC40.base.muzzle.apply(this,arguments);
};
bh25DredgerBarrel=function(b,id,barrel=0){return dc40Own(b)?dc40Barrel(b,id,barrel):DC40.base.barrel.apply(this,arguments);};
s7mBlit=function(name,i,x,y,w,h,rot,alpha,flash){const b=SW28.actor;if(name!=='tank'||!dc40Own(b))return DC40.base.blit.apply(this,arguments);const M=b._s7mod;
 if(i===0)return er28Blit('dc40_body',Math.floor(M.dc40Track||0),x,y,flash>0);
 if(i===1){const id=x<b.x?'gunL':'gunR',p=s7mPose(b).find(p=>p.id===id);return er28Blit('dc40_gun',p.dc40Frame,x,y,flash>0);}
 if(i===2){const ok=er28Blit('dc40_top',0,x,y,flash>0);if(flash<=0&&M.mode!=='dead'&&M.core>0){
   const A=M.dc40,k=A?.mode==='dc40-circle'?clamp(M.t/M.warn,0,1):0;
   ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha*=k?(.3+.7*k)*PXG_STEPS[2+Math.floor(M.clock*(10+20*k))%4]:.18;er28Blit('dc40_top_glow',0,x,y);ctx.restore();
  }return ok;}
 return DC40.base.blit.apply(this,arguments);
};
function dc40Shot(b,p,id){if(!sw28Budget(b))return null;const q=eShootT(p.x,p.y,p.a,4.7+b._s7mod.n*.2,'s7shard',{owner:b,noMuzzle:true,silent:true,w:6,h:14});
 Object.assign(q,{_er28Slug:true,_dc40Owner:b,_dc40Gun:id||null,_s7modOwner:b,_weaponProof:true,_shootable:false,_noArsenal:true,_boss:true});return q;
}
sw28Slug=function(b,id){if(!dc40Own(b))return DC40.base.slug.apply(this,arguments);if(!dc40Live(b,id))return;
 b._s7mod.dc40Recoil[id]=.11;
 for(let barrel=0;barrel<2;barrel++){
  const p=dc40Barrel(b,id,barrel);dc40Shot(b,p,id);
  navalFlash(null,p,.55,'weapon_muzzle_toxic',{n:4,hpx:20,life:.065,follow:()=>dc40Live(b,id)?dc40Barrel(b,id,barrel):null});
 }
 dc40Log('twin-turret-burst',{id,barrels:2});
};
function dc40Ram(b,dt){const M=b._s7mod,A=M.dc40,u=M.t-M.warn;
 if(u<0){combatWarningTick(b,'dredger-ram',M.t,M.warn);return;}
 if(u<A.dash){const v=clamp(u/A.dash,0,1),old={x:b.x,y:b.y+68};b.x=lerp(A.from.x,A.end.x,v*v);b.y=lerp(A.from.y,A.end.y,v*v);
  for(const seat of seatList())withSeat(seat,()=>{if(!A.hits.has(seat)&&!player.dead&&s81003Distance(player.x,player.y,{...old,ex:b.x,ey:b.y+68})<57){A.hits.add(seat);playerHit('Caustic Dredger rush');}});
  if(A.phase!=='dash'){A.phase='dash';combatAudio0927(b,'jetDash',.5);dc40Log('ram-release',{from:A.from,to:A.end,duration:A.dash});}
 }else if(u<A.dash+.66){const v=clamp((u-A.dash)/.66,0,1),ease=1-Math.pow(1-v,2);b._s4MiniSafe=false;b.x=lerp(A.end.x,A.back.x,ease);b.y=lerp(A.end.y,A.back.y,ease);
  if(A.phase!=='reverse'){A.phase='reverse';dc40Log('reverse-start');}
 }else{
  b._s4MiniSafe=false;b.x=A.back.x;b.y=A.back.y;
  if(A.phase!=='open'){A.phase='open';dc40Log('mid-screen-opening',{seconds:1.65,y:b.y});}
  if(u>=A.dash+.66+1.65)s7mSet(b,'recover');
 }
}
s7mTick=function(b,dt){const M=b?._s7mod;if(!dc40Own(b))return DC40.base.tick.apply(this,arguments);
 const old={x:b.x,y:b.y};M.lean=0;M.dc40Track??=0;M.dc40Recoil??={gunL:0,gunR:0};
 for(const id of ['gunL','gunR'])M.dc40Recoil[id]=Math.max(0,M.dc40Recoil[id]-dt);
 let r;if(!M.mode.startsWith('dc40-')||!M.dc40)r=DC40.base.tick.apply(this,arguments);
 else{
  sw28Common(b,dt);const A=M.dc40,u=M.t-M.warn;
  if(M.mode==='dc40-ram')dc40Ram(b,dt);
  else if(u<0){if(A.mode==='dc40-guns'&&M.t<M.warn*.42)A.angle=Math.atan2(player.y-b.y-60,player.x-b.x);combatWarningTick(b,'dredger-'+M.mode,M.t,M.warn);}
  else if(M.mode==='dc40-guns'){
   const live=s7mLive(M,'gun');A.cd-=dt;
   if(A.cd<=0&&live.length){A.cd+=(M.n===2?.115:.14);for(const p of live)sw28Slug(b,p.id);A.round++;combatAudio0927(b,'enemyMachineGunHeavy',.2);}
   if(u>=2.45||!live.length)s7mSet(b,'recover');
  }else if(M.mode==='dc40-circle'){
   A.cd-=dt;if(A.cd<=0&&A.round<3){A.cd=.42;A.round++;const p=s7mMuzzle(b,'dorsal');
    for(const a of A.angles){const q=dc40Shot(b,{...p,a});if(q){q.vx*=.59;q.vy*=.59;q._dc40Circle=true;}}
    navalFlash(null,p,.75,'weapon_muzzle_toxic',{n:4,hpx:32,life:.12,follow:()=>dc40Live(b)?s7mMuzzle(b,'dorsal'):null});combatAudio0927(b,'combatToxic0927',.4);dc40Log('top-cannon-wave',{round:A.round,count:A.angles.length});
   }if(u>1.5)s7mSet(b,'recover');
  }r=true;
 }
 M.lean=0;b._drawY=b.y+M.drop-M.height;
 if(M.mode!=='dead')M.dc40Track=(M.dc40Track+(b.y-old.y)/1.5+8*1000)%8;
 return r;
};
s7mHit=function(b,dmg,x,y,id){const M=b?._s7mod,coreBefore=M?.core;
 if(dc40Own(b)&&M.core<=0&&(id||s7mAt(b,x,y))==='core'){
  if(Number.isFinite(dmg)&&dmg>0&&M.mode!=='dead'){M.coreFlash=.08;markHit(b,.08);}return true;
 }
 const r=DC40.base.hit.apply(this,arguments);if(dc40Own(b)){
 if(M.core<=0&&s7mLive(M,'gun').length){
  b._s7FinalNoBar=false;
  if(coreBefore>0){const p=s7mMuzzle(b,'dorsal');s7mFX(p.x,p.y,110,false);combatAudio0927(b,'combatModule0927',.2);dc40Log('core-exhausted-guns-live',{remaining:M.parts.reduce((n,p)=>n+p.hp,0)});if(['dc40-circle','er28-mortar'].includes(M.mode))s7mSet(b,'recover');}
 }
 for(const p of b._s7mod.parts)if(p.hp<=0&&p.id.startsWith('gun')){dc40Cancel(b,p.id);b._s7mod.dc40Recoil[p.id]=0;}
 if(b.dead||b._s7mod.mode==='dead')dc40Cancel(b);
 }return r;
};
s7mTargets=function(b){const out=DC40.base.targets.apply(this,arguments);if(!dc40Own(b))return out;
 return out.filter(q=>q.hp>0&&!q.dead).map(q=>{
  const id=q._retinaId;if(id!=='gunL'&&id!=='gunR')return q;
  return retinaDynamicPiece(b,id,'toxic module',()=>{const part=b._s7mod.parts.find(p=>p.id===id),p=dc40Barrel(b,id,id==='gunL'?0:1);return{x:p.x,y:p.y-2,hp:part.hp,dead:b.dead||b._s7mod.mode==='dead'||part.hp<=0};},d=>s7mHit(b,d,0,0,id),32,42);
 });
};
// Keep native rupture/flight/terminal-blast ownership, with the current actual gun
// in its baked heading bank. The retired four-barrel plate is never resurrected.
d27ModuleRupture=function(b,part,shape,palette){if(!dc40Own(b)||!part?.id.startsWith('gun'))return DC40.base.rupture.apply(this,arguments);
 const r=DC40.base.rupture.call(this,b,part,{...shape,debrisImage:null},palette);if(r){const side=part.id==='gunL'?-1:1,unit=clamp(Math.max(shape.w,shape.h),24,100);
  D27_MODULE_DEBRIS.push({image:null,_dc40Owner:b,x:shape.x,y:shape.y,w:shape.w,h:shape.h,vx:side*(100+unit*.65),vy:-105-unit*.28,rot:shape.rot||0,spin:side*(5+unit*.025),t:0,life:.62+unit*.002,stage:run.stage,palette:palette||'green'});
 }return r;
};
d27ModuleDebrisDraw=function(){const r=DC40.base.debris.apply(this,arguments);for(const d of D27_MODULE_DEBRIS)if(d._dc40Owner)er28Blit('dc40_gun',er28Dir(d.rot),d.x,d.y);return r;};
function dc40Warning(b,front){const M=b._s7mod,A=M.dc40;if(!A||M.t>=M.warn||b.dead)return;const k=clamp(M.t/M.warn,0,1);
 if(A.mode==='dc40-circle'){
  if(front)return;const q=s7mMuzzle(b,'dorsal'),color=l23FovPhase(k);ctx.save();ctx.globalAlpha*=.6+.16*Math.sin(M.clock*(7+k*17));
  const a=DC40_ART['circle_'+color],im=XART.get(a.key),d=Math.min(440,viewW()*.94);if(XART.rdy(a.key)&&im)ctx.drawImage(im,q.x-d/2,q.y-d/2,d,d);ctx.restore();
 }else if(A.mode==='dc40-guns'&&!front){
  for(const part of s7mLive(M,'gun'))for(let barrel=0;barrel<2;barrel++){
   const p=dc40Barrel(b,part.id,barrel);for(const offset of [-.12,.12]){const a=dc40GunAngle(b,part.id)+Math.PI/2+offset;combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*VH*1.3,ey:p.y+Math.sin(a)*VH*1.3,width:15,progress:k,fieldOnly:true});}
  }
 }else if(A.mode==='dc40-ram'&&!front)combatWarningDraw(b,{x:A.from.x,y:A.from.y+68,ex:A.end.x,ey:A.end.y+68,len:Math.hypot(A.end.x-A.from.x,A.end.y-A.from.y),width:130,progress:k,fieldOnly:true});
}
s7mWarnings=function(front){const r=DC40.base.warnings.apply(this,arguments);for(const b of [boss,subBoss])if(dc40Own(b))dc40Warning(b,front);return r;};
updatePlay=function(dt){const r=DC40.base.update.apply(this,arguments);for(const q of eBullets)if(q._dc40Owner&&(!dc40Live(q._dc40Owner,q._dc40Gun)||q._dc40Circle&&q._dc40Owner._s7mod.core<=0))q.dead=true;return r;};
