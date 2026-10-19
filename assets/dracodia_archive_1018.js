"use strict";
/* Dracodia's archive: physical swipes, spiraling electricity, committed code
   bombs and finite half-health downloads. Five form pools remain authoritative. */
const D20={base:{start:v18StartAttack,attack:v18AttackTick,tick:r30Tick,draw:r30DrawBoss,rig:v18Rig,
 enter:v18Enter,clear:v18Clear,morph:j3Morph,arena:v17ArenaDraw,spawn:spawnEnemy,mega:s8MegaTick,
 enemy:drawEnemy,hit:hitEnemy,kill:killEnemy,targets:_lockTargets,update:updatePlay,bullets:drawBullets,shot:v18Shot,
 load:stageLoadBegin,begin:beginStage,aiBegin:ai27Begin,aiEnd:ai27End,entry:enemyEntrySweep,
 frenzy:enemyFrenzyTick,route:eb11OwnsRoute,contact:target17BossContact},clock:0,serial:0,events:[],
 sparks:[],blasts:[],models:new Map(),masks:new Map(),draws:{},
 book:['downloadLegion','scytheReap','spiralLightning','codeBombs','voidRoar','coreMissiles','armLasers'],
 roster:{bastion:{name:'IRON BASTION',hpx:1.10,size:250,role:'siege',mini:true},
  camo:{name:'CAMO COLOSSUS',hpx:1.15,size:240,role:'missile',mini:true},
  halberd:{name:'BLUE ARCHIVE GUNSHIP',sourceHP:1060,size:270,role:'cannon',mini:true},
  spear:{name:'CRYO ARCHIVE',sourceHP:190,size:170,role:'ice',key:'nsb_cryo_spear'},
  brood:{name:'BROOD ARCHIVE',sourceHP:180,size:168,role:'toxic',key:'nsb_spawncarrier_intact_v2'}}};
function d20Main(b){return v18Owned(b)&&j3State(b).encounter===2&&b._r30.v18.form===0;}
function d20Live(b){return v18Owned(b)&&r30Live(b)&&b._r30.mode==='fight';}
function d20Rank(){return Math.min(2,v18Diff());}
function d20Log(event,data={}){D20.events.push({event,t:D20.clock,...data});if(D20.events.length>900)D20.events.shift();}
function d20Keys(){return [...Object.values(D20_ART.models).flatMap(m=>[m.full,...Object.values(m.parts),...m.download]),...Object.values(D20_ART.fx).flatMap(b=>b.frames)].map(a=>a.key);}
for(const a of [...Object.values(D20_ART.models).flatMap(m=>[m.full,...Object.values(m.parts),...m.download]),...Object.values(D20_ART.fx).flatMap(b=>b.frames)])XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){return D20.base.load.call(this,n,n===8?[...(keys||[]),...d20Keys(),...Object.values(D20.roster).map(r=>r.key).filter(Boolean)]:keys);};
function d20Warm(){let ready=true;for(const k of [...d20Keys(),'av3_laser_beams','av3_laser_muzzles'])if(!XART.rdy(k))ready=false;for(const r of Object.values(D20.roster))if(r.key&&!XART.rdy(r.key))ready=false;return ready;}
beginStage=function(){D20.sparks=[];D20.blasts=[];D20.clock=0;D20.events=[];return D20.base.begin.apply(this,arguments);};
function d20Art(a,x,y,size,angle=0,alpha=1){if(!a)return false;const im=a.image||XART.rdy(a.key)&&XART.get(a.key);if(!im)return false;
 const k=size/a.w;ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.translate(x,y);ctx.rotate(angle);ctx.drawImage(im,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();D20.draws[a.key]=(D20.draws[a.key]||0)+1;return true;}
function d20Fx(name,t,x,y,size,angle=0,alpha=1,loop=true){const bank=D20_ART.fx[name];if(!bank)return;const u=Math.floor(t*bank.fps),a=bank.frames[loop?u%bank.frames.length:Math.min(bank.frames.length-1,u)];return d20Art(a,x,y,size*(bank.renderScale||1),angle,alpha);}
function d20Mask(a){if(D20.masks.has(a.key))return D20.masks.get(a.key);const im=a.image||XART.rdy(a.key)&&XART.get(a.key);if(!im)return null;
 const c=document.createElement('canvas');c.width=a.w;c.height=a.h;const g=c.getContext('2d',{willReadFrequently:true});g.drawImage(im,0,0);const v=g.getImageData(0,0,a.w,a.h).data,m=new Uint8Array(a.w*a.h);for(let i=0;i<m.length;i++)m[i]=v[i*4+3];D20.masks.set(a.key,m);return m;}
function d20Legacy(kind){if(D20.models.has(kind))return D20.models.get(kind);const key=D20.roster[kind]?.key;if(!key||!XART.rdy(key))return null;
 const im=XART.get(key),c=document.createElement('canvas');c.width=c.height=320;const g=c.getContext('2d',{willReadFrequently:true}),k=256/Math.max(im.width,im.height);g.imageSmoothingEnabled=false;g.drawImage(im,160-im.width*k/2,160-im.height*k/2,im.width*k,im.height*k);
 const make=(image,id)=>({key:'d20_'+kind+'_'+id,image,w:320,h:320,pivot:[160,160]}),full=make(c,'full'),parts={},seams=kind==='spear'?[132,188]:[112,208];
 for(const id of ['core','left','right']){const p=document.createElement('canvas');p.width=p.height=320;const z=p.getContext('2d');z.drawImage(c,0,0);z.globalCompositeOperation='destination-in';z.fillStyle='#fff';
  if(id==='left')z.fillRect(0,0,seams[0],320);else if(id==='right')z.fillRect(seams[1],0,320-seams[1],320);else z.fillRect(seams[0],0,seams[1]-seams[0],320);parts[id]=make(p,id);}
 const measured=kind==='spear'?{left:[108,214],right:[212,214]}:{left:[80,247],right:[240,247]},muzzles={};
 for(const id of ['left','right']){const a=parts[id],v=a.image.getContext('2d').getImageData(0,0,320,320).data,want=measured[id];let distance=Infinity;
  for(let y=0;y<320;y++)for(let x=0;x<320;x++)if(v[(y*320+x)*4+3]>80){const d=(x-want[0])**2+(y-want[1])**2;if(d<distance){distance=d;muzzles[id]=[x,y];}}}
 const model={full,parts,mounts:{core:[160,160],...muzzles},muzzles,download:[]};D20.models.set(kind,model);return model;}
function d20Model(kind){return D20_ART.models[kind]||d20Legacy(kind);}
function d20Rig(e){const A=e._d20,M=d20Model(A.kind);if(!M)return[];const k=D20.roster[A.kind].size/320;
 return A.parts.filter(p=>p.hp>0).map(p=>({p,a:M.parts[p.id],k,x:e.x,y:e.y,anchor:[160,160],rot:0}));}
function d20At(e,x,y){const A=e._d20;if(!A||A.phase==='download'||A.phase==='erase')return null;if(A.kind==='bomb')return A.parts[0];
 for(const v of d20Rig(e).reverse()){const px=Math.floor((x-e.x)/v.k+160),py=Math.floor((y-e.y)/v.k+160),m=d20Mask(v.a);if(px>=0&&py>=0&&px<v.a.w&&py<v.a.h&&m?.[py*v.a.w+px]>48)return v.p;}return null;}
function d20Mount(e,id,muzzle=false){const A=e._d20,M=d20Model(A.kind),a=(muzzle?M.muzzles:M.mounts)[id],k=D20.roster[A.kind].size/320;return{x:e.x+(a[0]-160)*k,y:e.y+(a[1]-160)*k};}
function d20Enemy(kind,x,y,owner,mini=D20.roster[kind]?.mini){const r=D20.roster[kind];if(!r)return null;
 const e=D20.base.spawn('s8interceptor',x,y,{});if(!e)return null;for(const k of Object.keys(e))if(k.startsWith('_'))delete e[k];
 const baseHP=r.hpx?(220+8*120)*r.hpx:r.sourceHP,sourceHP=Math.ceil(baseHP*DIFF.eHp*(coopActive()?1.5:1)),hp=mini?Math.ceil(sourceHP*.5):sourceHP;
 Object.assign(e,{type:'d20_'+kind,name:r.name,pattern:'s8mega',x,y,w:r.size*.72,h:r.size*.62,vx:0,vy:0,spin:0,hp,maxhp:hp,_maxhp:hp,
  ground:false,shoots:false,fk:null,_atk:'none',score:mini?1800:700,dropOk:false,flash:0,_noSep:true,_noHit:true,_continueEligible:false});
 const side=Math.round(hp*.22);e._d20={id:++D20.serial,kind,owner,sourceHP,mini,phase:'download',t:0,age:0,cycle:0,round:0,next:0,
  home:{x,y},parts:['core','left','right'].map(id=>({id,hp:id==='core'?hp-side*2:side,maxhp:id==='core'?hp-side*2:side,flash:0})),direct:null};
 d20Log('download-start',{kind,id:e._d20.id,hp,sourceHP,mini,x,y});return e;}
function d20Bomb(b,target){const m=d20BossMount(b,'core');if(!m)return null;const e=D20.base.spawn('s8interceptor',m.x,m.y,{});if(!e)return null;for(const k of Object.keys(e))if(k.startsWith('_'))delete e[k];
 const hp=[12,16,20][d20Rank()];Object.assign(e,{type:'d20_codebomb',name:'CODE BOMB',pattern:'s8mega',w:24,h:24,hp,maxhp:hp,_maxhp:hp,vx:0,vy:0,spin:0,ground:false,shoots:false,fk:null,_atk:'none',score:120,dropOk:false,flash:0,_noSep:true,_noHit:false,_noBodyContact:true,_continueEligible:false});
 e._d20={id:++D20.serial,kind:'bomb',owner:b,phase:'flight',t:0,age:0,start:{x:e.x,y:e.y},target:{...target},flight:[1.25,1.10,.95][d20Rank()],warm:[1.10,.95,.85][d20Rank()],parts:[{id:'core',hp,maxhp:hp,flash:0}]};
 d20Log('code-bomb',{id:e._d20.id,target:{...target},warning:e._d20.flight+e._d20.warm});r30Sound('timedBombBeep');return e;}
function d20Detonate(e){const A=e._d20;e.dead=true;e.hp=0;D20.blasts.push({owner:A.owner,x:A.target.x,y:A.target.y,t:0,life:1.3,radius:54,hit:new Set()});d20Log('code-detonation',{x:A.target.x,y:A.target.y});r30Sound('timedBombBlast');shake=Math.max(shake,6);}
function d20Tell(e){const A=e._d20,P=targetShip(e.x,e.y);A.phase='tell';A.t=0;A.round=0;A.next=0;A.target={x:P.x,y:P.y};A.warning=[1.12,.96,.82][d20Rank()];
 A.ports=['left','right'].filter(id=>A.parts.some(p=>p.id===id&&p.hp>0));if(D20.roster[A.kind].role==='cannon'&&A.parts[0].hp>0)A.ports.push('core');
 A.origins=A.ports.map(id=>({...d20Mount(e,id,true),id}));A.angles=A.origins.map(m=>Math.atan2(A.target.y-m.y,A.target.x-m.x));
 combatWarningTick(e,'archive-'+A.id+'-'+A.cycle,0,A.warning);r30Sound('bossWeaponCharge');d20Log('archive-tell',{kind:A.kind,id:A.id,warning:A.warning,ports:A.ports.slice()});}
function d20Fire(e){const A=e._d20,r=D20.roster[A.kind],rank=d20Rank();if(!A.origins.length)return;const i=A.round%A.origins.length,m=A.origins[i];if(!A.parts.some(p=>p.id===m.id&&p.hp>0))return;
 if(eBullets.filter(q=>q._d20Owner===A.owner).length>=[48,66,90][rank])return;
 const aim=A.angles[i],special=A.cycle%2===1,heavy=r.role==='cannon'&&m.id==='core',kind=r.role==='ice'?'ice':r.role==='toxic'?'s7acid':r.role==='missile'?'emissile':r.role==='siege'&&special||heavy?'s8pair':'s8slug',fan=r.role==='ice'?3+rank*2:special&&r.role==='siege'?3:1;
 for(let j=0;j<fan;j++){const a=aim+(j-(fan-1)/2)*.14,q=eShootT(m.x,m.y,a,kind==='emissile'?3.2+rank*.28:3.5+rank*.28,kind,{owner:e,noMuzzle:true,silent:j>0,w:kind==='emissile'?10:9,h:kind==='emissile'?20:12,szMul:.65});
  if(q){q._d20Owner=A.owner;q._d20Actor=e;q._noArsenal=true;q.homing=false;if(heavy){q.w=q.h=24;q.szMul=1.25;r30Sound('enemyBossCannon');}if(kind==='emissile'){q._shootable=true;q._weaponProof=false;q.hp=2;}
   if(r.role==='ice'){q._l23fx='cryo_ball';q.w=q.h=12;}wm26EnemyShot(m.x,m.y,a,kind,e);}}
 d20Log('archive-shot',{id:A.id,kind:A.kind,port:m.id,x:m.x,y:m.y,round:A.round});}
function d20EnemyTick(e,dt){const A=e._d20;A.t+=dt;A.age+=dt;e.shoots=false;e.vx=e.vy=0;e.spin=0;for(const p of A.parts)p.flash=Math.max(0,p.flash-dt);
 if(!d20Live(A.owner)&&A.phase!=='erase'){A.phase='erase';A.t=0;e._noHit=true;}
 if(A.phase==='erase'){if(A.t>=.8)e.dead=true;return;}
 if(A.kind==='bomb'){
  if(A.phase==='flight'){const u=clamp(A.t/A.flight,0,1);e.x=lerp(A.start.x,A.target.x,u);e.y=lerp(A.start.y,A.target.y,u)-Math.sin(u*Math.PI)*30;if(u>=1){A.phase='arming';A.t=0;e.x=A.target.x;e.y=A.target.y;}}
  else if(A.phase==='arming'&&A.t>=A.warm)d20Detonate(e);return;
 }
 if(A.phase==='download'){e._noHit=true;if(A.t>=2.0){A.phase='settle';A.t=0;e._noHit=false;r30Sound('teleportIn');d20Log('download-complete',{kind:A.kind,id:A.id});}return;}
 e._noHit=false;if(e._frozen||e._mercuryLock>0||e._shieldStun>0)return;
 if(A.phase==='settle'){if(A.t>=.60)d20Tell(e);return;}
 if(A.phase==='tell'){combatWarningTick(e,'archive-'+A.id+'-'+A.cycle,A.t,A.warning);if(A.t>=A.warning){A.phase='fire';A.t=0;d20Log('archive-release',{id:A.id,kind:A.kind,reaction:A.warning});}return;}
 if(A.phase==='fire'){if(A.round<[5,7,9][d20Rank()]&&A.t>=A.next){d20Fire(e);A.round++;A.next+=.19;}
  if(A.t>1.95){A.phase='recover';A.t=0;A.cycle++;}return;}
 if(A.phase==='recover'){e.x=A.home.x+Math.sin(A.t*2+A.id)*Math.min(28,viewW()*.045);if(A.t>=[1.5,1.15,.85][d20Rank()])d20Tell(e);}
}
function d20Download(e,erasing=false){const A=e._d20,r=D20.roster[A.kind],M=d20Model(A.kind);if(!M)return;const u=clamp(A.t/(erasing?.8:2),0,.99999),a=M.download.length?M.download[Math.min(M.download.length-1,Math.floor((erasing?u:1-u)*M.download.length))]:null;
 if(a)d20Art(a,e.x,e.y,r.size);else{const p=erasing?1-u:u;ctx.save();const size=r.size;ctx.beginPath();ctx.rect(e.x-size/2,e.y-size/2,size,size*p);ctx.clip();d20Art(M.full,e.x,e.y,size);ctx.restore();}
 d20Fx('transfer_loop',A.age,e.x,e.y,r.size*1.06,0,Math.sin(u*Math.PI)*.85);
 d20Fx('storm_loop',A.age,e.x,e.y,r.size*1.22,0,.28);if(!erasing)groundTargetReticleDraw(e.x,e.y,r.size*.68,u,.45);
}
function d20EnemyDraw(e){const A=e._d20;if(e.dead||e._dyingT!=null)return;
 if(A.phase==='download'||A.phase==='erase'){d20Download(e,A.phase==='erase');return;}
 if(A.kind==='bomb'){d20Fx('bomb_charge',A.age,e.x,e.y,48,0,1);if(e.flash>0){const bank=D20_ART.fx.bomb_charge,a=bank.frames[Math.floor(A.age*bank.fps)%bank.frames.length],size=48*(bank.renderScale||1);ctx.save();ctx.globalAlpha=clamp(e.flash/.16,0,1)*.85;ctx.drawImage(xartTint(a.key,'#fff',1),e.x-size/2,e.y-size/2,size,size);ctx.restore();}
  const progress=A.phase==='flight'?A.t/(A.flight+A.warm):(A.flight+A.t)/(A.flight+A.warm);groundTargetReticleDraw(A.target.x,A.target.y,135,progress,.9);return;}
 for(const v of d20Rig(e)){d20Art(v.a,e.x,e.y,D20.roster[A.kind].size);const flash=Math.max(e.flash||0,v.p.flash||0);if(flash>0){let white=v.a.white;
   if(!white){const c=document.createElement('canvas');c.width=v.a.w;c.height=v.a.h;const z=c.getContext('2d');z.drawImage(v.a.image||XART.get(v.a.key),0,0);z.globalCompositeOperation='source-in';z.fillStyle='#fff';z.fillRect(0,0,c.width,c.height);white=v.a.white=c;}
   ctx.save();ctx.globalAlpha=clamp(flash/.16,0,1)*.85;const k=v.k;ctx.drawImage(white,e.x-160*k,e.y-160*k,320*k,320*k);ctx.restore();}}
 if(A.phase==='tell')for(const [i,m]of A.origins.entries())if(A.parts.some(p=>p.id===m.id&&p.hp>0))combatWarningDraw(e,{x:m.x,y:m.y,ex:A.target.x,ey:A.target.y,width:18+(D20.roster[A.kind].role==='ice'?40:0),progress:A.t/A.warning});
}
hitEnemy=function(e,dmg){if(!e?._d20)return D20.base.hit.apply(this,arguments);const A=e._d20;if(e.dead||e._dyingT!=null||e._noHit||!(dmg>0))return;
 const q=_dmgBullet,direct=A.direct;A.direct=null;let p=A.parts.find(p=>p.id===direct&&p.hp>0);
 if(!p&&Number.isFinite(q?.x)&&Number.isFinite(q?.y))p=d20At(e,q.x,q.y);if(!p&&Number.isFinite(_lastHitX)&&Number.isFinite(_lastHitY))p=d20At(e,_lastHitX,_lastHitY);p=p||A.parts[0];
 dmg=Math.max(0,elementalDamageResult(e,'enemy',q,dmg,e.x,e.y).dmg||0);if(!dmg)return;markHit(e);markHit(p);const dealt=Math.min(p.hp,dmg);p.hp-=dealt;e.hp=A.parts.reduce((s,p)=>s+Math.max(0,p.hp),0);stageStats.dmgDealt+=dealt;weaponHitSfx('normal');
 if(p.hp<=0&&p.id!=='core'){const m=d20Mount(e,p.id);unitDeathFX({...m,w:38,h:40},'turret','purple');d20Log('archive-module-break',{kind:A.kind,id:A.id,part:p.id});}
 if(A.parts[0].hp<=0||e.hp<=0){e.hp=0;killEnemy(e);}return true;
};
killEnemy=function(e){if(e?._d20){const A=e._d20;if(A.kind==='bomb'&&!e.dead&&A.phase!=='erase'){D20.blasts.push({owner:A.owner,x:e.x,y:e.y,t:0,life:1.05,radius:0,hit:new Set()});d20Log('code-bomb-intercepted',{id:A.id});}
 eBullets=eBullets.filter(q=>q._d20Actor!==e);d20Log('archive-destroyed',{kind:A.kind,id:A.id});}return D20.base.kill.apply(this,arguments);};
_lockTargets=function(){const base=D20.base.targets.apply(this,arguments),out=[];for(const e of base){if(!e?._d20){out.push(e);continue;}const A=e._d20;if(e.dead||e._dyingT!=null||e.hp<=0||e._noHit)continue;
 if(A.kind==='bomb'){out.push(e);continue;}for(const p of A.parts)if(p.hp>0){const target=retinaDynamicPiece(e,'archive '+A.id+' '+p.id,p.id,()=>({...d20Mount(e,p.id),hp:p.hp,dead:e.dead||e._dyingT!=null||e.hp<=0||e._noHit||p.hp<=0}),d=>{A.direct=p.id;hitEnemy(e,d);},p.id==='core'?58:44,54);target.name=e.name+' '+({core:'Core',left:'Left Battery',right:'Right Battery'}[p.id]);out.push(target);}}return out;};
s8MegaTick=function(e,dt){return e?._d20?d20EnemyTick(e,dt):D20.base.mega.apply(this,arguments);};
drawEnemy=function(e){return e?._d20?d20EnemyDraw(e):D20.base.enemy.apply(this,arguments);};
enemyEntrySweep=function(e){if(!e?._d20)return D20.base.entry.apply(this,arguments);};
enemyFrenzyTick=function(e){if(!e?._d20)return D20.base.frenzy.apply(this,arguments);};
eb11OwnsRoute=function(e){return !!e?._d20||D20.base.route.apply(this,arguments);};
ai27Begin=function(e){if(!e?._d20)return D20.base.aiBegin.apply(this,arguments);const old=ai27Context;ai27Context=null;return old;};
ai27End=function(e,prior){if(!e?._d20)return D20.base.aiEnd.apply(this,arguments);ai27Context=prior;};
v18Enter=function(b){D20.base.enter.apply(this,arguments);if(v18Owned(b)){const N=b._r30.v18;N.archiveDepth=1;N.archiveEnergy=0;N.hoverTime=0;N.hoverPose=null;}};
// Source coordinates were inspected in the shipping 320-square plates. The
// same transformed rig owns the visible palms, core, Retina locks and muzzles.
const D20_MOUNTS={core:[160,139],left:[75,198],right:[245,198]};
function d20BossMount(b,id){const v=v18Rig(b).find(v=>v.p.id===id&&!v.p.destroyed);return v?{...v19WorldPoint(v,D20_MOUNTS[id]),module:id}:null;}
function d20HoverStep(b,dt){const N=b._r30.v18;N.hoverTime=(N.hoverTime||0)+dt;
 const pad=v18Size(b)*.37+20,lo=camLeftX()+pad,hi=camRightX()-pad,mid=(lo+hi)/2,r=Math.max(0,(hi-lo)/2),
  x=mid+Math.sin(N.hoverTime*.82)*r,y=N.home.y+Math.sin(N.hoverTime*1.34)*8,mix=1-Math.exp(-dt*3.5);
 return{x:lerp(b.x,x,mix),y:lerp(b.y,y,mix)};}
function d20Start(b,type){if(type==='armLasers'&&!b.parts.some(p=>['left','right'].includes(p.id)&&!p.destroyed))return d20Start(b,'coreMissiles');
 const N=b._r30.v18,rank=d20Rank(),tell=[1.35,1.16,.98][rank];let active=type==='downloadLegion'?12:type==='codeBombs'?5.8:3.8;
 N.acting=null;N.swipe=null;N.attack={_d20:true,type,t:0,tell,active,next:0,n:0,started:false,origin:{x:b.x,y:b.y},target:{x:player.x,y:player.y},ports:[],targets:[],lanes:[]};b._r30.attack=N.attack;
 if(type==='armLasers'){const live=['left','right'].filter(id=>b.parts.some(p=>p.id===id&&!p.destroyed)),order=live.slice();if(rank===2&&live.length===2)order.push(live[0]);let at=0;
  N.attack.arms=order.map((id,i)=>{const warm=i?[1.05,.88,.74][rank]:tell,q={id,at,tell:warm,life:[.68,.75,.82][rank],recover:.26,target:null};at+=warm+q.life+q.recover;return q;});
  active=N.attack.active=Math.max(.2,at-tell);}
 combatWarningTick(b,'d20-'+N.seq,0,tell);r30Sound(type==='downloadLegion'?'shadowCharge':'bossWeaponCharge');d20Log('main-tell',{type,tell});}
v18StartAttack=function(b){if(!d20Main(b))return D20.base.start.apply(this,arguments);const N=b._r30.v18;if(N.hoverPose)Object.assign(b,N.hoverPose);const seq=N.seq,type=D20.book[seq%D20.book.length],old=['scytheReap','voidRoar','heartSpores'].indexOf(type);
 if(old>=0){N.seq=old;D20.base.start(b);N.seq=seq+1;}else{N.seq++;d20Start(b,type);}};
j3Morph=function(b){if(d20Main(b)&&r30Live(b)&&b._r30.mode==='fight'&&j3State(b).attacks<D20.book.length){v18StartAttack(b);return;}return D20.base.morph.apply(this,arguments);};
v18Shot=function(b,p,a,speed,kind,large=false){if(!d20Main(b)||kind!=='missile')return D20.base.shot.apply(this,arguments);const m=d20BossMount(b,'core');if(!m)return null;
 const q=f1003bShot(b,m.x,m.y,a,speed,kind,large);if(q){q._v18Owner=q._d20Owner=b;q._d20Module='core';q._d20Origin={x:m.x,y:m.y};
  // Shared interception rules classify the physical missile, not its retained
  // authored code-warhead picture. It must not inherit an energy-orb proof.
  q.kind='emissile';q._weaponProof=false;q.homing=false;q.ang=a;delete q._finaleTurn;
  b._r30.v18.shots=(b._r30.v18.shots||0)+1;d20Log('core-missile',{x:m.x,y:m.y,module:'core'});}return q;};
function d20ArmState(b,id){const P=b._r30.v18.attack;return P?.arms?.find(q=>q.id===id&&q.target&&P.t>=q.at&&P.t<q.at+q.tell+q.life+q.recover);}
function d20ArmLane(b,q){const m=d20BossMount(b,q.id);if(!m||!q.target)return null;const a=Math.atan2(q.target.y-m.y,q.target.x-m.x),len=Math.hypot(viewW(),viewH())+100;
 return{x:m.x,y:m.y,ex:m.x+Math.cos(a)*len,ey:m.y+Math.sin(a)*len,width:[18,20,22][d20Rank()],module:q.id};}
function d20ArmTick(b,P){for(const [i,q]of P.arms.entries()){const t=P.t-q.at;if(t<0||t>=q.tell+q.life+q.recover)continue;
  if(!q.target){q.target={x:player.x,y:player.y};r30Sound('bossWeaponCharge');d20Log('arm-charge',{side:q.id,tell:q.tell,target:{...q.target}});}
  if(!b.parts.some(p=>p.id===q.id&&!p.destroyed)){q.disabled=true;continue;}
  combatWarningTick(b,'d20-arm-'+b._r30.v18.seq+'-'+i,Math.min(t,q.tell),q.tell);
  if(t<q.tell){shake=Math.max(shake,t/q.tell*1.6);continue;}if(t>=q.tell+q.life)continue;
  const L=d20ArmLane(b,q);if(!L)continue;if(!q.released){q.released=true;r30Sound('combatBeam0927');shake=Math.max(shake,3);d20Log('arm-laser',{side:q.id,reaction:q.tell,origin:{x:L.x,y:L.y},target:{...q.target}});}
  for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&s81003Distance(player.x,player.y,L)<L.width*.5+4)playerHit('Dracodia '+q.id+' arm laser');});
 }}
function d20Finish(b){const N=b._r30.v18;N.archiveDepth=1;N.archiveEnergy=0;N.attack=null;b._r30.attack=null;b._r30.cd=[1.05,.85,.65][d20Rank()];b._noHit=false;j3State(b).attacks++;d20Log('main-recover');}
function d20MainTick(b,dt){const S=b._r30,N=S.v18,P=N.attack,rank=d20Rank();P.t+=dt;const u=P.t-P.tell;N.archiveEnergy=clamp(P.t/P.tell,0,1);combatWarningTick(b,'d20-'+N.seq,Math.min(P.t,P.tell),P.tell);
 if(P.type==='armLasers')d20ArmTick(b,P);
 if(u<0){shake=Math.max(shake,P.t/P.tell*2);return;}if(!P.started){P.started=true;r30Sound(P.type==='spiralLightning'?'geyserLightning':P.type==='codeBombs'?'shadowRelease':'teleportIn');d20Log('main-release',{type:P.type,reaction:P.tell});}
 if(P.type==='spiralLightning'){
  if(u<P.active-.65&&u>=P.next){P.next=u+[.26,.23,.21][rank];const count=2+rank,base=P.n*.26,origin=d20BossMount(b,'core');
   if(origin)for(let i=0;i<count;i++)D20.sparks.push({owner:b,origin:{...origin},t:0,angle:base+i*TAU/count,speed:102+rank*10,spin:.72+rank*.08,x:origin.x,y:origin.y});P.n++;if(P.n%3===1)r30Sound('element_lightning_hit');}
 }else if(P.type==='coreMissiles'){
  if(u<P.active-.5&&u>=P.next){P.next=u+[.9,.76,.64][rank];const m=d20BossMount(b,'core');if(m){const a=Math.atan2(P.target.y-m.y,P.target.x-m.x);
   for(let i=-1;i<=1;i++)v18Shot(b,m,a+i*[.22,.25,.28][rank],2.7+rank*.18,'missile');P.n++;r30Sound('missileLaunch');}}
 }else if(P.type!=='armLasers'){
  const back=v19Ease(clamp(u/.95,0,1)),returning=v19Ease(clamp((u-(P.active-1))/.95,0,1));N.archiveDepth=1-(back-returning)*.47;
  b.y=lerp(P.origin.y,viewTopY()+viewH()*.20,back-returning);b._noHit=N.archiveDepth<.90;
  if(P.type==='codeBombs'&&u<3.6&&u>=P.next){P.next=u+.82;const offsets=[0,-110,110,-55,55],i=P.n++,target={x:clamp(P.target.x+offsets[i%offsets.length],camLeftX()+65,camRightX()-65),y:clamp(P.target.y+(i%2?-65:0),viewTopY()+200,VH-65)};d20Bomb(b,target);}
  if(P.type==='downloadLegion'&&!P.downloaded&&u>=.95){P.downloaded=true;const mini=['halberd','bastion','camo'][(N.archiveWave||0)%3],live=enemies.filter(e=>e._d20?.owner===b&&e._d20.kind!=='bomb'&&!e.dead&&e._dyingT==null&&e._d20.phase!=='erase');N.archiveWave=(N.archiveWave||0)+1;
   const y=viewTopY()+viewH()*.32;if(!live.some(e=>e._d20.mini)&&live.length<1+rank){const e=d20Enemy(mini,worldWidth()/2,y,b,true);if(e)live.push(e);}
   for(let i=0;i<rank&&live.length<1+rank;i++){const e=d20Enemy(i%2?'brood':'spear',camLeftX()+viewW()*(i?.78:.22),viewTopY()+viewH()*.19,b,false);if(e)live.push(e);}}
 }
 if(u>=P.active){d20Finish(b);}
}
v18AttackTick=function(b,dt){return b?._r30?.v18?.attack?._d20?d20MainTick(b,dt):D20.base.attack.apply(this,arguments);};
// The native clock/dialogue remain authoritative. This wrapper moves only the
// main body; a physical swipe keeps its planted, committed shoulder geometry.
r30Tick=function(b,dt){if(!d20Main(b)||!d20Live(b))return D20.base.tick.apply(this,arguments);const N=b._r30.v18;
 if(N.swipe)return D20.base.tick.apply(this,arguments);const P=N.attack,pose=d20HoverStep(b,clamp(dt||0,0,.05));N.hoverPose=pose;Object.assign(b,pose);
 const out=D20.base.tick.apply(this,arguments);N.hoverPose=null;
 if(b._r30.v18===N&&d20Main(b)&&d20Live(b)&&!N.swipe){b.x=pose.x;if(!P?._d20||!['codeBombs','downloadLegion'].includes(P.type))b.y=pose.y;}return out;};
v18Rig=function(b){const rig=D20.base.rig.apply(this,arguments);if(!d20Main(b))return rig;const N=b._r30.v18,depth=N.archiveDepth||1;
 return rig.map(source=>{let v=depth===1?source:{...source,k:source.k*depth,x:b.x+(source.x-b.x)*depth,y:b.y+(source.y-b.y)*depth,ax:b.x+(source.ax-b.x)*depth,ay:b.y+(source.ay-b.y)*depth,w:source.w*depth,h:source.h*depth};
  const q=d20ArmState(b,v.p.id);if(!q||q.disabled||v.p.destroyed)return v;const t=N.attack.t-q.at,point=D20_MOUNTS[q.id],
   base=Math.atan2(point[1]-v.anchor[1],point[0]-v.anchor[0]),aim=clamp(fztWrap(Math.atan2(q.target.y-v.ay,q.target.x-v.ax)-base),-.85,.85),
   mix=v19Ease(t/.45)*(1-v19Ease((t-q.tell-q.life)/q.recover)),rot=aim*mix,
   dx=((v.a.bounds[0]+v.a.bounds[2])/2-v.anchor[0])*v.k,dy=((v.a.bounds[1]+v.a.bounds[3])/2-v.anchor[1])*v.k;
  return{...v,rot,x:v.ax+dx*Math.cos(rot)-dy*Math.sin(rot),y:v.ay+dx*Math.sin(rot)+dy*Math.cos(rot)};});};
target17BossContact=function(b){if(d20Main(b)&&b._r30.v18.attack?._d20)return false;return D20.base.contact.apply(this,arguments);};
function d20Warnings(b){const P=b._r30.v18.attack;if(!P?._d20)return;
 if(P.type==='armLasers'){for(const q of P.arms){const t=P.t-q.at,L=d20ArmLane(b,q);if(!q.disabled&&L&&t>=0&&t<q.tell){combatWarningDraw(b,{...L,progress:t/q.tell,fieldOnly:true});groundTargetReticleDraw(q.target.x,q.target.y,72,t/q.tell,.75);combatWarningDraw(b,{x:L.x,y:L.y,progress:t/q.tell,alertOnly:true,alertX:L.x,alertY:L.y-38});}}return;}
 if(P.t>=P.tell)return;const u=P.t/P.tell;
 combatWarningDraw(b,{x:b.x,y:b.y,progress:u,alertOnly:true,alertX:b.x,alertY:b.y-135});
 const m=d20BossMount(b,'core');if(!m)return;
 if(P.type==='spiralLightning'){const count=2+d20Rank();for(let i=0;i<count;i++){const a=i*TAU/count;combatWarningDraw(b,{x:m.x,y:m.y,ex:m.x+Math.cos(a)*280,ey:m.y+Math.sin(a)*280,len:280,width:26,progress:u,fieldOnly:true});}}
 else if(P.type==='coreMissiles')combatWarningDraw(b,{x:m.x,y:m.y,ex:P.target.x,ey:P.target.y,width:165,progress:u});
 else groundTargetReticleDraw(P.target.x,P.target.y,125,u,.7);
}
function d20ArmEffects(b){const N=b._r30.v18,P=N.attack;if(P?.type!=='armLasers')return;
 for(const v of v18Rig(b)){const q=d20ArmState(b,v.p.id);if(!q||q.disabled||v.p.destroyed)continue;const t=P.t-q.at,L=d20ArmLane(b,q),charge=clamp(t/q.tell,0,1),fade=1-clamp((t-q.tell-q.life)/q.recover,0,1);
  ctx.save();ctx.translate(v.ax,v.ay);ctx.rotate(v.rot);ctx.globalCompositeOperation='lighter';ctx.globalAlpha=(.1+.2*charge)*fade*(.8+.2*Math.sin(N.age*24));
  ctx.drawImage(xartTint(v.key,'#c25aff',1),-v.anchor[0]*v.k,-v.anchor[1]*v.k,320*v.k,320*v.k);ctx.restore();
  d20Fx('lightning_loop',N.age*1.5,L.x,L.y,35+charge*37,N.age*1.8,.3+charge*.55);
  av3Muzzle(ctx,L.x,L.y,25+charge*42,'void',N.age,.3+charge*.7);
  if(t>=q.tell&&t<q.tell+q.life)av3Beam(ctx,L.x,L.y,Math.atan2(L.ey-L.y,L.ex-L.x),Math.hypot(L.ex-L.x,L.ey-L.y),L.width,'void',t-q.tell,1);
 }}
function d20MainBody(b){v19Body(b);const N=b._r30.v18,m=d20BossMount(b,'core');if(m&&N.attack?.type!=='armLasers')d20Fx('lightning_loop',b._r30.clock,m.x,m.y,75*(N.archiveDepth||1),0,N.archiveEnergy*.5);d20ArmEffects(b);}
r30DrawBoss=function(b){if(!d20Main(b)||!b._r30.v18.attack?._d20)return D20.base.draw.apply(this,arguments);d20Warnings(b);if(b._r30.v18.archiveDepth>=.90)d20MainBody(b);};
function d20Arena(b){const out=D20.base.arena.apply(this,arguments);if(!v18Owned(b)||j3State(b).encounter!==2)return out;const energy=b._r30.v18.archiveEnergy||0,t=b._r30.clock;
 ctx.save();ctx.globalCompositeOperation='lighter';for(let i=0;i<2;i++)d20Fx('storm_loop',t*.28+i,worldWidth()*(i?.76:.24),viewTopY()+viewH()*.44,viewW()*.98,i?t*.035:-t*.035,.12+energy*.12);ctx.restore();
 // A distant Dracodia belongs behind downloaded hulls, not painted over them.
 if(d20Main(b)&&b._r30.v18.attack?._d20&&b._r30.v18.archiveDepth<.90)d20MainBody(b);return out;}
v17ArenaDraw=d20Arena;aa5ArenaDraw=d20Arena;
function d20Cleanup(b){D20.sparks=D20.sparks.filter(q=>q.owner!==b);D20.blasts=D20.blasts.filter(q=>q.owner!==b);eBullets=eBullets.filter(q=>q._d20Owner!==b);
 for(const e of enemies)if(e._d20?.owner===b&&!e.dead){e._d20.phase='erase';e._d20.t=0;e._noHit=true;}
 if(b?._r30?.v18){b._r30.v18.archiveDepth=1;b._r30.v18.archiveEnergy=0;}}
v18Clear=function(b){d20Cleanup(b);return D20.base.clear.apply(this,arguments);};
updatePlay=function(dt){const out=D20.base.update.apply(this,arguments);if(state!==GS.PLAY||run.stage!==8)return out;dt=clamp(dt||0,0,.05);D20.clock+=dt;
 for(const q of D20.sparks){q.t+=dt;const r=28+q.t*q.speed,a=q.angle+q.t*q.spin;q.x=q.origin.x+Math.cos(a)*r;q.y=q.origin.y+Math.sin(a)*r;
  if(q.t>.12)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-q.x,player.y-q.y)<12)playerHit('spiraling code lightning');});}
 D20.sparks=D20.sparks.filter(q=>d20Live(q.owner)&&q.t<6&&q.x>camLeftX()-100&&q.x<camRightX()+100&&q.y>viewTopY()-140&&q.y<VH+110);
 for(const q of D20.blasts){q.t+=dt;if(q.radius>0&&q.t>=.18&&q.t<.48)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!q.hit.has(seat)&&Math.hypot(player.x-q.x,player.y-q.y)<q.radius){q.hit.add(seat);playerHit('code bomb blast');}});}
 D20.blasts=D20.blasts.filter(q=>d20Live(q.owner)&&q.t<q.life);return out;};
function d20SparksDraw(){for(const q of D20.sparks)d20Fx('lightning_loop',q.t,q.x,q.y,42,q.angle+q.t*q.spin+Math.PI/2,1);}
drawBullets=function(){const out=D20.base.bullets.apply(this,arguments);d20SparksDraw();
 for(const q of D20.blasts)d20Fx('bomb_burst',q.t,q.x,q.y,q.radius?170:78,0,1,false);return out;};
globalThis.BOF_DRACODIA_ARCHIVE=D20;
