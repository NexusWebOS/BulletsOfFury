"use strict";
/* Mike's seven selected Monster Mutator revisions. Authored waves retain their
   times/counts. Hulls stay upright; weapon pivots, warnings and damage share poses. */
for(const a of Object.values(MM1003_ART))XART._src[a.key]=a.path;
const MM1003_DEF={
 bluehybrid:{name:'Blue Hybrid',hp:34,w:130,h:87,score:1600,attack:'fan',cool:2.5},
 hexpyre:{name:'Hexpyre',hp:30,w:130,h:108,score:1900,attack:'cast',cool:3.1,rig:'hexpyre',scale:.13},
 hellram:{name:'Hellram',hp:32,w:108,h:75,score:1500,attack:'ram',cool:2.8},
 riflelocust:{name:'Rifle Locust',hp:26,w:116,h:105,score:1400,attack:'rifle',cool:2.6,rig:'riflelocust',scale:.12},
 impharrow:{name:'Imp Harrow',hp:20,w:110,h:62,score:1100,attack:'pair',cool:2.3},
 furnacemaw:{name:'Furnace Maw',hp:46,w:138,h:83,score:2200,attack:'siege',cool:3.0},
 hellhugger:{name:'Hellhugger',hp:7,w:90,h:92,score:950,attack:'claw',cool:2.4,rig:'hellhugger',scale:.09}
};
const MM1003_SLOTS={7:{s7sampler:'riflelocust',s7lamprey:'hellram',s7serpent:'hellhugger'},8:{s8manta:'bluehybrid',s8scout:'hexpyre',s8needlejet:'impharrow',s8gunship:'furnacemaw'}};
const MM1003={serial:0,debris:[],clock:0};
const MM1003_BASE={spawn:spawnEnemy,begin:beginStage,draw:drawEnemy,hit:hitEnemy,kill:killEnemy,
 entry:enemyEntrySweep,frenzy:enemyFrenzyTick,end:ai27End,movable:sepMovable,
 locks:_lockTargets,space:spaceTargets,play:updatePlay,bullets:drawBullets};
function mm1003Warm(){for(const a of Object.values(MM1003_ART))XART.rdy(a.key);er26Warm();s81003Warm();}
beginStage=function(n){MM1003.debris=[];MM1003.clock=0;MM1003.serial=0;const r=MM1003_BASE.begin.apply(this,arguments);if(n===7||n===8)mm1003Warm();return r;};
function mm1003Alive(e){return !!e&&!e.dead&&e._dyingT==null&&e.hp>0;}
function mm1003Disarmed(e){const A=e._mm1003,D=MM1003_DEF[e._mutator1003];const p=A.parts.filter(p=>D.attack==='claw'?p.kind==='claw'&&p.front:D.attack==='cast'?p.kind==='arm':p.kind==='gun');return p.length>0&&p.every(p=>p.dead);}
function mm1003Parts(e){
 const D=MM1003_DEF[e._mutator1003],R=MM1003_RIGS[D.rig];if(!R)return [];
 const parts=[],add=(p,id,kind)=>parts.push({...p,id,kind,hp:kind==='pod'?6:kind==='claw'?3:10,maxhp:kind==='pod'?6:kind==='claw'?3:10,dead:false,recoil:0});
 if(D.rig==='hexpyre')R.limbs.forEach((p,i)=>add(p,'arm'+i,'arm'));
 if(D.rig==='riflelocust'){R.guns.forEach((p,i)=>add(p,'gun'+i,'gun'));R.pods.forEach((p,i)=>add(p,'pod'+i,'pod'));}
 if(D.rig==='hellhugger')R.limbs.forEach((p,i)=>add(p,'claw'+i,'claw'));
 return parts;
}
spawnEnemy=function(type,x,y,opt={}){
 const kind=type.startsWith('mm1003_')?type.slice(7):MM1003_SLOTS[run.stage]?.[type];
 if(!MM1003_DEF[kind])return MM1003_BASE.spawn.apply(this,arguments);
 // A known native body supplies score/death/collision bookkeeping; remove its
 // old controller flags so only this authored rig owns motion and attacks.
 const e=MM1003_BASE.spawn('s8interceptor',x,y,opt);if(!e)return e;
 const D=MM1003_DEF[kind];e.type='mm1003_'+kind;e._mutator1003=kind;e._mutatorSlot1003=type;
 for(const k of ['_s8mega','_s7toxic','_alien1003','_orbit1003','_frRealmAI','_dr','_cn','_droid','_furyMove','_esh','_enemyShield','_frFlight','_entrySweep'])delete e[k];
 e.pattern='mutator1003';e.w=D.w;e.h=D.h;e.hp=e.maxhp=e._maxhp=kind==='hellhugger'?Math.max(3,Math.round(EHP(D.hp)*.32)):EHP(D.hp);e.score=D.score;
 e.shoots=false;e.fk=null;e._atk='none';e.spin=e._bank=e._frBank=0;e.vx=e.vy=0;e._noSep=true;e.ground=false;e._noHit=false;
 const n=++MM1003.serial;
 e._mm1003={id:n,phase:'entry',age:0,t:0,cycles:0,cd:.5+(n%3)*.25,homeX:clamp(x,camLeftX()+D.w*.6,camRightX()-D.w*.6),homeY:viewTopY()+viewH()*(.23+(n%3)*.07),parts:[],history:[],fired:0};
 e._mm1003.parts=mm1003Parts(e);mm1003Warm();return e;
};
enemyEntrySweep=function(e,dt){if(e._mutator1003)return;return MM1003_BASE.entry.apply(this,arguments);};
enemyFrenzyTick=function(e,dt){if(e._mutator1003)return;return MM1003_BASE.frenzy.apply(this,arguments);};
ai27End=function(e,prev){if(e?._mutator1003){if(e._ai27)e._ai27.dx=0;e._frFlight=false;e.spin=e._bank=e._frBank=0;}return MM1003_BASE.end.apply(this,arguments);};
sepMovable=function(e){if(e?._mutator1003)return false;return MM1003_BASE.movable.apply(this,arguments);};
function mm1003Set(e,phase){const A=e._mm1003;A.phase=phase;A.age=0;A.history.push({phase,t:A.t,x:e.x,y:e.y});if(A.history.length>24)A.history.shift();}
function mm1003Move(e,x,y,speed,dt){const dx=x-e.x,dy=y-e.y,d=Math.hypot(dx,dy),step=Math.min(d,speed*dt);if(d>.01){e.x+=dx/d*step;e.y+=dy/d*step;}return d<2;}
function mm1003Pose(e,p){
 const A=e._mm1003,D=MM1003_DEF[e._mutator1003],s=D.scale*(p.kind==='pod'?.88:p.kind==='claw'?.9:1);
 let angle=0;
 if(p.kind==='gun'){
  const tx=A.target?.x??player.x,ty=A.target?.y??player.y;
  angle=clamp(Math.atan2(ty-(e.y+p.attach[1]*D.scale),tx-(e.x+p.attach[0]*D.scale))-(p.side<0?2.20:.94),-.32,.32);
 }else if(p.kind==='arm')angle=p.side*(A.phase==='tell'?-.17:A.phase==='fire'?.12:Math.sin(A.t*1.8)*.06);
 else if(p.kind==='claw')angle=p.side*(p.front?(A.phase==='tell'?-.45:A.phase==='dash'?.32:0):Math.sin(A.t*3)*.05);
 else angle=p.side*Math.sin(A.t*1.6)*.03;
 const x=e.x+p.attach[0]*D.scale,y=e.y+p.attach[1]*D.scale-(p.recoil||0);
 let muzzle=p.kind==='gun'?[p.side*278,339]:p.kind==='arm'?p.palm:[0,0];
 return {x,y,s,angle,mx:x+(muzzle[0]*Math.cos(angle)-muzzle[1]*Math.sin(angle))*s,my:y+(muzzle[0]*Math.sin(angle)+muzzle[1]*Math.cos(angle))*s};
}
function mm1003Warning(e){
 const A=e._mm1003,D=MM1003_DEF[e._mutator1003],T=targetShip(e.x,e.y);
 A.target={x:T.x,y:T.y};A.warm=diffKey==='easy'?1.45:diffKey==='furious'?.9:diffKey==='hard'?1.05:1.2;A.fired=0;A.cycles++;
 if(D.attack==='ram'||D.attack==='claw'){
  A.target.x=clamp(T.x,camLeftX()+e.w*.5,camRightX()-e.w*.5);A.target.y=clamp(T.y,viewTopY()+90,VH-48);
  A.start={x:e.x,y:e.y};A.lane={x:e.x,y:e.y,ex:A.target.x,ey:A.target.y,width:e.w*.58,tx:A.target.x,ty:A.target.y};
 }else A.lane=s81003Lane(e.x,e.y+e.h*.3,T.x,T.y,22);
 mm1003Set(e,'tell');r30Sound('bossWeaponCharge');
 if(D.attack==='cast')for(const p of A.parts.filter(p=>!p.dead&&p.kind==='arm')){
  const q=groundTargetingSpawn({kind:'lava',owner:e,x:clamp(T.x+p.side*45,camLeftX()+36,camRightX()-36),y:T.y,warn:A.warm+.08,active:.52,radius:25,size:74,track:false,lane:false,shake:2});
  q._late27=true;q._mmPart=p.id;
 }
}
function mm1003Shot(e,x,y,angle,speed,kind='fire',large=false){
 const q=eShootT(x,y,angle,speed,kind==='rifle'?'mg':'s8pair',{w:kind==='rifle'?5:large?21:15,h:kind==='rifle'?15:large?21:15,silent:true,owner:e});
 if(!q||q.dead)return false;
 q._noArsenal=true;q._mutatorShot1003=e._mutator1003;q._mutatorOwner1003=e;
 if(kind!=='rifle'){q._er26Art=kind==='blue'?'ice':'fire';q._er26Large=large;q._er26Draw=large?32:23;}
 return true;
}
function mm1003Fire(e){
 const A=e._mm1003,D=MM1003_DEF[e._mutator1003],n=fr27Difficulty(),T=A.target;
 const shot=(x,y,a,kind='fire',large=false)=>mm1003Shot(e,x,y,a,kind==='rifle'?4.5+n*.35:2.6+n*.25,kind,large);
 const aimed=(x,y)=>Math.atan2(T.y-y,T.x-x);
 if(D.attack==='rifle'){
  if(A.fired<6&&A.age>=A.fired*.16){const guns=A.parts.filter(p=>p.kind==='gun'&&!p.dead),p=guns[A.fired%Math.max(1,guns.length)];
   if(p){const P=mm1003Pose(e,p);if(shot(P.mx,P.my,aimed(P.mx,P.my),'rifle')){p.recoil=3;r30Sound('enemyMG');}}A.fired++;
  }
 }else if(D.attack==='fan'&&A.fired===0){
  const x=e.x,y=e.y+e.h*.23;for(const k of [-2,-1,0,1,2])shot(x,y,aimed(x,y)+k*.20,'blue');A.fired=1;r30Sound('combatOrb0927');
 }else if(D.attack==='pair'&&A.fired<2&&A.age>=A.fired*.34){
  const x=e.x+(A.fired?1:-1)*e.w*.13,y=e.y+e.h*.28;shot(x,y,aimed(x,y)+(A.fired?.08:-.08));A.fired++;r30Sound('combatOrb0927');
 }else if(D.attack==='siege'&&A.fired<2&&A.age>=A.fired*.58){
  const side=A.fired?1:-1,x=e.x+side*e.w*.36,y=e.y+e.h*.21;
  for(const off of [-.16,0,.16])shot(x,y,aimed(x,y)+off,'fire',true);A.fired++;r30Sound('combatOrb0927');
 }else if(D.attack==='ram'&&A.fired===0){
  for(const side of [-1,1]){const x=e.x+side*e.w*.35,y=e.y+e.h*.15;shot(x,y,Math.PI/2+side*.2,'fire',true);}A.fired=1;r30Sound('combatOrb0927');
 }
}
function mm1003Tick(e,dt){
 if(!mm1003Alive(e))return;dt=Math.min(.05,dt);const A=e._mm1003,D=MM1003_DEF[e._mutator1003];A.t+=dt;A.age+=dt;e.spin=e._bank=e._frBank=0;
 for(const p of A.parts){p.recoil=Math.max(0,p.recoil-dt*26);p.flash=Math.max(0,(p.flash||0)-dt);}
 if(mm1003Disarmed(e)&&['tell','fire','dash'].includes(A.phase)){groundTargetingCancel(e);mm1003Set(e,'recover');}
 const pods=A.parts.filter(p=>p.kind==='pod'&&p.dead).length,speed=100-pods*22;
 if(A.phase==='entry'){if(mm1003Move(e,A.homeX,A.homeY,speed,dt))mm1003Set(e,'rest');return;}
 if(A.phase==='leave'){e.y+=speed*dt;if(e.y>VH+70)e.dead=true;return;}
 if(A.phase==='rest'){
  mm1003Move(e,A.homeX,A.homeY,speed,dt);A.cd-=dt;
  if(mm1003Disarmed(e)||A.cycles>=3||A.t>19){mm1003Set(e,'leave');return;}
  const busy=enemies.filter(q=>q!==e&&mm1003Alive(q)&&(['tell','fire','dash'].includes(q._mm1003?.phase)||['tell','fire'].includes(q._orbit1003?.phase))).length;
  if(A.cd<=0&&busy<(diffKey==='easy'?1:diffKey==='furious'?3:2)&&e.y<targetShip(e.x,e.y).y-95&&e.x>=camLeftX()+e.w*.45&&e.x<=camRightX()-e.w*.45)mm1003Warning(e);
  return;
 }
 if(A.phase==='tell'){
  combatWarningTick(e,'mm1003-'+A.id+'-'+A.cycles,A.age,A.warm);
  if(A.age>=A.warm){mm1003Set(e,D.attack==='ram'||D.attack==='claw'?'dash':'fire');if(A.phase==='dash')r30Sound('enemyApproach');}return;
 }
 if(A.phase==='dash'){
  const duration=D.attack==='claw'?.48:.65,u=clamp(A.age/duration,0,1);
  e.x=lerp(A.start.x,A.target.x,u);e.y=lerp(A.start.y,A.target.y,u);
  if(u>=1){mm1003Set(e,D.attack==='ram'?'backstep':'recover');A.fired=0;}
  return;
 }
 if(A.phase==='backstep'){
  // The native anti-point-blank gate correctly blocks firing on top of the pilot.
  // Withdraw visibly before the two plasma shots, keeping that safety rule.
  mm1003Move(e,A.homeX,A.homeY,145,dt);
  const T=targetShip(e.x,e.y);if(Math.hypot(T.x-e.x,T.y-e.y)>120&&A.age>.65)mm1003Set(e,'fire');
  return;
 }
 if(A.phase==='fire'){mm1003Fire(e);if(A.age>(D.attack==='rifle'?1.12:D.attack==='siege'?1.1:.7))mm1003Set(e,'recover');return;}
 if(A.phase==='recover'){
  // Returning to the firing pocket never follows the player or adds a second ram.
  if(D.attack==='claw'){if(A.age>1.0)mm1003Set(e,'leave');}
  else{mm1003Move(e,A.homeX,A.homeY,70,dt);if(A.age>1.35){A.cd=D.cool*(diffKey==='furious'?.75:diffKey==='easy'?1.3:1);A.homeX=clamp(A.homeX+(A.cycles%2?36:-36),camLeftX()+e.w*.65,camRightX()-e.w*.65);mm1003Set(e,'rest');}}
 }
}
function mm1003Blit(key,part,x,y,scale,angle=0,tint=null,alpha=1){
 if(!XART.rdy(key))return false;const im=tint?xartTint(key,tint,1):XART.get(key),r=part.rect,p=part.pivot;
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.translate(x,y);if(angle)ctx.rotate(angle);
 ctx.drawImage(im,...r,-p[0]*scale,-p[1]*scale,r[2]*scale,r[3]*scale);ctx.restore();return true;
}
function mm1003Draw(e){
 const A=e._mm1003,D=MM1003_DEF[e._mutator1003],tint=e.flash>0?'#ffffff':null;
 if(e._dyingT!=null||e.dead)return;
 if(A.phase==='tell'&&D.attack!=='cast')s81003Fov(A.lane,A.age/A.warm,true,e);
 const R=MM1003_RIGS[D.rig];
 if(R){
  if(R.thruster)mm1003Blit(R.key,R.thruster,e.x,e.y+R.thruster.attach[1]*D.scale,R.thruster.scale*(D.scale/.32),0,tint);
  for(const p of A.parts){if(p.dead)continue;const P=mm1003Pose(e,p);mm1003Blit(R.key,p,P.x,P.y,P.s,P.angle,p.flash>0?'#ffffff':tint);
   if(p.kind==='arm'&&(A.phase==='tell'||A.phase==='fire'))mm1003Blit(R.key,R.flames[Math.floor(A.t*10)%2],P.mx,P.my,D.scale*.60,0,null,.95);
  }
  mm1003Blit(R.key,R.body,e.x,e.y,D.scale,0,tint);
 }else{
  const a=MM1003_ART[e._mutator1003],r=a.rect;
  mm1003Blit(a.key,{rect:r,pivot:[r[2]/2,r[3]/2]},e.x,e.y,e.w/r[2],0,tint);
 }
}
drawEnemy=function(e){if(e._mutator1003)return mm1003Draw(e);return MM1003_BASE.draw.apply(this,arguments);};
function mm1003PartCenter(e,p){const P=mm1003Pose(e,p),v=p.kind==='gun'?[p.side*110,155]:p.kind==='arm'?[p.side*150,-35]:p.kind==='pod'?[p.side*170,0]:[p.side*135,p.front?150:-135];
 return {x:P.x+(v[0]*Math.cos(P.angle)-v[1]*Math.sin(P.angle))*P.s,y:P.y+(v[0]*Math.sin(P.angle)+v[1]*Math.cos(P.angle))*P.s,r:p.kind==='claw'?13:17};}
function mm1003Debris(e,p){
 const D=MM1003_DEF[e._mutator1003],R=MM1003_RIGS[D.rig],P=mm1003Pose(e,p);
 MM1003.debris.push({key:R.key,part:p,x:P.x,y:P.y,s:P.s,a:P.angle,vx:p.side*(80+Math.random()*50),vy:-30+Math.random()*70,spin:p.side*3,t:0});
 if(MM1003.debris.length>36)MM1003.debris.shift();
}
function mm1003PartHit(e,p,dmg,shot){
 if(!mm1003Alive(e)||p.dead)return false;const hit=enemyPoolDamage(p,'hp',dmg,'module','maxhp');p.flash=.16;markHit(e,.10);weaponHitSfx('normal');
 if(typeof stageStats!=='undefined')stageStats.dmgDealt+=hit;
 if(p.hp<=0){p.dead=true;mm1003Debris(e,p);const P=mm1003PartCenter(e,p);explode(P.x,P.y,25,'red');r30Sound('expSmall');
  for(const q of groundTargetingFx)if(q.owner===e&&q._mmPart===p.id)q.dead=true;
 }
 return true;
}
hitEnemy=function(e,dmg){
 if(e?._mutator1003&&mm1003Alive(e)&&_dmgBullet&&Number.isFinite(_dmgBullet.x+_dmgBullet.y)){
  const p=e._mm1003.parts.find(p=>{const P=mm1003PartCenter(e,p);return !p.dead&&Math.hypot(_dmgBullet.x-P.x,_dmgBullet.y-P.y)<=P.r;});
  if(p)return mm1003PartHit(e,p,dmg,_dmgBullet);
 }
 return MM1003_BASE.hit.apply(this,arguments);
};
killEnemy=function(e){
 if(e?._mutator1003&&!e._mm1003.broken){e._mm1003.broken=true;groundTargetingCancel(e);
  for(const p of e._mm1003.parts)if(!p.dead){mm1003Debris(e,p);p.dead=true;}
 }
 return MM1003_BASE.kill.apply(this,arguments);
};
function mm1003Target(e,p){
 if(p.proxy)return p.proxy;const t={kind:'mutator module',part:p,_retinaOwner:e,_retinaId:'mm1003-'+e._mm1003.id+'-'+p.id,_retinaHit:(d,q)=>mm1003PartHit(e,p,d,q)};
 Object.defineProperties(t,{x:{get:()=>mm1003PartCenter(e,p).x},y:{get:()=>mm1003PartCenter(e,p).y},w:{get:()=>mm1003PartCenter(e,p).r*2},h:{get:()=>mm1003PartCenter(e,p).r*2},hp:{get:()=>p.hp},dead:{get:()=>p.dead||!mm1003Alive(e)}});
 p.proxy=t;return t;
}
function mm1003Targets(list){const modules=[];for(const e of enemies)if(mm1003Alive(e)&&e._mutator1003)for(const p of e._mm1003.parts)if(!p.dead){const P=mm1003PartCenter(e,p);if(P.x>=camLeftX()&&P.x<=camRightX()&&P.y>=viewTopY()&&P.y<=VH)modules.push(mm1003Target(e,p));}return modules.concat(list);}
_lockTargets=function(){return mm1003Targets(MM1003_BASE.locks.apply(this,arguments));};
spaceTargets=function(){return mm1003Targets(MM1003_BASE.space.apply(this,arguments));};
updatePlay=function(dt){const r=MM1003_BASE.play.apply(this,arguments);if(state===GS.PLAY&&!BOFCinematicDirector.live){MM1003.clock+=dt;for(const f of MM1003.debris){f.t+=dt;f.x+=f.vx*dt;f.y+=f.vy*dt;f.a+=f.spin*dt;}MM1003.debris=MM1003.debris.filter(f=>f.t<.75);}return r;};
drawBullets=function(){const r=MM1003_BASE.bullets.apply(this,arguments);for(const f of MM1003.debris)mm1003Blit(f.key,f.part,f.x,f.y,f.s,f.a,null,1-f.t/.75);return r;};
