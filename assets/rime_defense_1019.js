"use strict";
/* Stage3 Rime Wall: cold weapons, permanent shoulder emitters and a critical core.
   Frost Cruiser shares the new charge art; its encounter remains independently owned. */
const RD19={events:[],draws:{},base:{book:er26Book,set:er26Set,combat:er26Combat,tick:er26Tick,
 at:mr27At,hull:mr27HullAt,damage:mr27Damage,mount:shipBossMount,slug:sa14Slug,targets:retinaBossTargets,
 charge:sa14ChargeFx,draw:mr27Draw,bullets:drawBullets,projectile:er26ProjectileDraw,
 groundDraw:groundTargetingDraw,groundHit:groundTargetingStrikePlayers,contact:target17BossContact,
 load:stageLoadBegin,begin:beginStage},cfg:[
 {warm:1.65,beam:1.20,mortar:1.90,ram:1.55,dash:.68,back:.92,waves:1,gap:.72,fall:1.50,radius:20,recover:1.0},
 {warm:1.40,beam:1.35,mortar:1.65,ram:1.25,dash:.56,back:.82,waves:2,gap:.65,fall:1.35,radius:21,recover:.75},
 {warm:1.18,beam:1.50,mortar:1.40,ram:1.08,dash:.47,back:.74,waves:3,gap:.56,fall:1.20,radius:23,recover:.60},
 {warm:1.02,beam:1.60,mortar:1.20,ram:.96,dash:.40,back:.66,waves:4,gap:.48,fall:1.10,radius:24,recover:.48},
 {warm:.95,beam:1.68,mortar:1.12,ram:.90,dash:.38,back:.62,waves:4,gap:.44,fall:1.05,radius:24,recover:.44}]};
for(const bank of Object.values(RD19_ART.banks))for(const a of bank)XART._src[a.key]=a.path;
XART._src[RD19_ART.bullet.key]=RD19_ART.bullet.path;
function rd19Owns(b){return run.stage===3&&b?._ship==='cryospear';}
function rd19Ice(b){return run.stage===3&&['cryospear','frostcruiser'].includes(b?._ship);}
function rd19Cfg(){return RD19.cfg[target17Rank()];}
function rd19Log(event,b,data={}){RD19.events.push({event,ship:b?._ship,...data});if(RD19.events.length>200)RD19.events.shift();}
function rd19State(b){return b._rd19||(b._rd19={age:0,exposed:false,turn:null,beam:null,serial:0,charge:0});}
function rd19Disarmed(b){return rd19Owns(b)&&!!b._mr27?.parts.length&&b._mr27.parts.every(p=>p.dead||p.hp<=0);}
function rd19Ready(){let ready=true;for(const bank of Object.values(RD19_ART.banks))for(const a of bank)if(!XART.rdy(a.key))ready=false;return ready;}
stageLoadBegin=function(n,keys){const extra=n===3?Object.values(RD19_ART.banks).flat().map(a=>a.key):[];
 if(n===3){extra.push(RD19_ART.bullet.key);for(let i=0;i<8;i++)extra.push('l23fx_rime_orb_'+i);}
 if(n===3)for(let i=0;i<12;i++)extra.push('l23fx_rime_laser_'+i);
 return RD19.base.load.call(this,n,[...(keys||[]),...extra]);};
beginStage=function(){RD19.events=[];RD19.draws={};return RD19.base.begin.apply(this,arguments);};
function rd19Port(b,side){const r=MR27_ART.rime.cells[0],k=Math.min(b.w/r[2],b.h/r[3]),sx=side<0?201:491;
 return{x:b.x+(sx-r[0]-r[2]/2)*k,y:(b._drawY??b.y)+(184-r[1]-r[3]/2)*k};}
shipBossMount=function(b,slot){if(rd19Owns(b)&&/^ICE_SHOULDER_[LR]$/.test(slot))return rd19Port(b,slot.endsWith('L')?-1:1);
 return RD19.base.mount.apply(this,arguments);};
function rd19CoreAt(b,x,y){if(!Number.isFinite(x+y))return false;const p=mr27Shape(b,'core'),u=(x-p.x)/p.w+.5,v=(y-p.y)/p.h+.5;
 if(u<0||u>=1||v<0||v>=1)return false;const m=RD19_ART.coreMask,n=m.n;
 return Math.floor(parseInt(m.rows[Math.floor(v*n)],16)/Math.pow(2,n-1-Math.floor(u*n)))%2===1;}
mr27At=function(b,x,y){if(!rd19Owns(b)||!b._mr27)return RD19.base.at.apply(this,arguments);
 if(b.dead||b.enter||b._noHit)return null;
 // Live weapon assemblies retain their independent routing ahead of the hull.
 const id=RD19.base.at.apply(this,arguments);if(id&&id!=='core')return id;
 if(rd19CoreAt(b,x,y))return 'core';
 if(rd19Disarmed(b)){const p=mr27Shape(b,'core');
  // An open reactor accepts a shot through the nose conduit. The solid core
  // plate above owns impact; the retired nose must not consume that round.
  if(Math.abs(x-p.x)<p.w*.40&&y>p.y&&y<(b._drawY??b.y)+b.h*.60)return null;
 }return id;};
target17BossContact=function(b,x,y){if(!rd19Owns(b))return RD19.base.contact.apply(this,arguments);
 if(b.dead||b.enter||b._noHit)return false;
 // Projectile access to the open conduit never removes the ramming hull.
 if(RD19.base.hull(b,x,y))return true;
 return b._mr27.parts.some(part=>{if(part.dead)return false;const p=mr27Shape(b,part.id),dx=x-p.x,dy=y-p.y,c=Math.cos(p.rot),s=Math.sin(p.rot);
  return Math.abs(dx*c+dy*s)<p.w*.48&&Math.abs(-dx*s+dy*c)<p.h*.48;});};
mr27Damage=function(b,dmg,x,y){if(!rd19Owns(b)||!b._mr27)return RD19.base.damage.apply(this,arguments);
 const critical=rd19Disarmed(b)&&rd19CoreAt(b,x,y),exposed=rd19Disarmed(b),id=mr27At(b,x,y),part=mr27Part(b,id),hp=part?.hp;
 const result=RD19.base.damage.call(this,b,dmg*(critical?3:exposed?1.5:1),x,y);
 if(part&&part.hp<hp)markHit(part,.20);
 if(critical){rd19Log('critical-core-hit',b,{damage:result});b._rd19Critical=Math.max(b._rd19Critical||0,.15);}
 return result;};
retinaBossTargets=function(b){const a=RD19.base.targets.apply(this,arguments);
 if(!rd19Disarmed(b)||b.dead||b.enter||b._noHit)return a;
 const state=()=>({...mr27Shape(b,'core'),hp:b.hp,dead:b.dead||b.enter||b._noHit||!rd19Disarmed(b)}),p=state();
 return [...a.filter(q=>q!==b),retinaImpactTarget(b,'rd19-core','critical ice reactor',state,p.w,p.h)];};
er26Book=function(b){if(!rd19Owns(b))return RD19.base.book.apply(this,arguments);
 return rd19Disarmed(b)?['rd19-ram','rd19-mortars','rd19-ram','rd19-mortars']:
 ['sa14-mg','rd19-lasers','sa14-rockets','rd19-mortars','sa14-ice'];};
er26Set=function(b,mode){const r=RD19.base.set.apply(this,arguments);if(!rd19Owns(b))return r;
 const C=rd19State(b),R=b._er26,c=rd19Cfg();C.beam=null;C.charge=0;
 if(mode==='recover'&&rd19Disarmed(b))R.dur=c.recover;
 if(!mode.startsWith('rd19-'))return r;
 C.turn={serial:++C.serial,from:{x:b.x,y:b.y},aim:{x:player.x,y:player.y},wave:0,shot:0,released:false};
 R.warm=mode==='rd19-ram'?c.ram:mode==='rd19-mortars'?c.mortar:c.warm;
 R.live=mode==='rd19-ram'?c.dash+c.back:mode==='rd19-mortars'?(c.waves-1)*c.gap+.5:c.beam+.24;
 R.dur=R.warm+R.live;R.warnings=[];b._l23Beam=null;
 if(mode==='rd19-lasers'){
  const slots=['L','R'].filter(s=>mr27CanFire(b,s));
  C.beam={family:'rime',slots,angles:slots.map(s=>{const p=shipBossMount(b,s);return Math.atan2(player.y-p.y,player.x-p.x);}),
   t:0,warm:R.warm,active:c.beam,retract:.24,width:target17Rank()>1?20:18,released:false};
 }rd19Log('attack',b,{mode,warm:R.warm,exposed:C.exposed});Audio.SFX.iceBreathStart?.();return r;};
function rd19BeamHit(b,B){const len=Math.max(VW,VH)*1.25;
 for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.invuln>0)return;
  const half=B.width*.32+(player._hx||9)*.55;
  for(let i=0;i<B.slots.length;i++){const p=shipBossMount(b,B.slots[i]),a=B.angles[i],dx=Math.cos(a),dy=Math.sin(a),x=player.x-p.x,y=player.y-p.y;
   if(x*dx+y*dy>=0&&x*dx+y*dy<=len&&Math.abs(x*dy-y*dx)<half){playerHit('Rime cannon laser');break;}}
 });}
function rd19Lasers(b,dt){const C=rd19State(b),R=b._er26,T=C.turn,B=C.beam;if(!B)return;
 for(let i=B.slots.length-1;i>=0;i--)if(!mr27CanFire(b,B.slots[i])){B.slots.splice(i,1);B.angles.splice(i,1);}
 if(!B.slots.length){er26Set(b,'recover');return;}
 B.t=R.t;C.charge=R.t<R.warm?clamp(R.t/R.warm,0,1):Math.max(0,1-(R.t-R.warm)*4);
 if(R.t<R.warm*.55)T.aim={x:player.x,y:player.y};
 if(R.t<R.warm)for(let i=0;i<B.slots.length;i++){const p=shipBossMount(b,B.slots[i]);B.angles[i]=Math.atan2(T.aim.y-p.y,T.aim.x-p.x);}
 // Keep the gun pose on its committed beam angle throughout the release;
 // native idle tracking must not pull the muzzle away from its own laser.
 for(let i=0;i<B.slots.length;i++){const part=mr27Part(b,B.slots[i]==='L'?'gunL':'gunR');part.rot=B.angles[i]-Math.PI/2;}
 if(R.t<R.warm){
  combatWarningTick(b,'rime-beam-'+T.serial,R.t,R.warm);
 }else{if(!B.released){B.released=true;for(let i=0;i<B.slots.length;i++)mr27Fire(b,B.slots[i],B.angles[i]);
   Audio.SFX.enemyHeavyLaser?.();rd19Log('ice-lasers',b,{slots:B.slots.slice(),angles:B.angles.slice()});}
  if(R.t<R.warm+B.active)rd19BeamHit(b,B);
 }}
function rd19Mortars(b){const C=rd19State(b),T=C.turn,c=rd19Cfg(),seats=[];
 for(const seat of seatList())withSeat(seat,()=>{if(!player.dead)seats.push({seat,x:player.x,y:player.y});});if(!seats.length)return;
 for(let i=0;i<2;i++){const side=i?-1:1,target=seats[(T.wave+i)%seats.length],offset=seats.length===1&&i?(T.wave%2?78:-78):0;
  const q=groundTargetingSpawn({kind:'glacial',owner:b,track:false,lane:false,x:clamp(target.x+offset,camLeftX()+c.radius+12,camRightX()-c.radius-12),
   y:clamp(target.y+(i? -22:0),PLAY.y+80,VH-40),warn:c.fall+i*.12,active:.62,radius:c.radius,size:c.radius*2,
   sound:'iceOrbImpact',shake:4,targetSeat:target.seat});
  Object.assign(q,{_rd19Mortar:true,_late27:true,side,launch:{...rd19Port(b,side)},serial:T.serial});
  rd19Log('mortar-launch',b,{side,x:q.x,y:q.y,warn:q.warn,radius:q.radius,source:q.launch});
 }T.wave++;Audio.SFX.combatOrb0927?.();}
function rd19Ram(b,dt){const C=rd19State(b),R=b._er26,T=C.turn,c=rd19Cfg();
 if(R.t<R.warm){if(R.t<R.warm*.55)T.aim={x:player.x,y:player.y};
  b.x=clamp(T.from.x+Math.sin(R.t*22)*4*(R.t/R.warm),camLeftX()+b.w*.45,camRightX()-b.w*.45);
  const p={x:b.x,y:b.y+b.h*.2};sa14Warning(b,p,{x:T.aim.x,y:T.aim.y},b.w*.56,R.t/R.warm);
  C.charge=clamp(R.t/R.warm,0,1);combatWarningTick(b,'rime-ram-'+T.serial,R.t,R.warm);return;
 }
 if(!T.released){T.released=true;T.start={x:b.x,y:b.y};T.to={x:clamp(T.aim.x,camLeftX()+b.w*.40,camRightX()-b.w*.40),y:clamp(T.aim.y-24,R.home+65,VH-b.h*.28)};
  rd19Log('ram-release',b,{from:T.start,to:T.to});Audio.SFX.chargeDash?.();shake=Math.max(shake,6);}
 const t=R.t-R.warm,ease=u=>{u=clamp(u,0,1);return u*u*(3-2*u);};C.charge=Math.max(0,1-t*2);
 if(t<c.dash){const u=ease(t/c.dash);b.x=lerp(T.start.x,T.to.x,u);b.y=lerp(T.start.y,T.to.y,u);}
 else{const u=ease((t-c.dash)/c.back),home=clamp(er26Station(b,0)+(T.serial%2?30:-30),camLeftX()+b.w*.45,camRightX()-b.w*.45);
  b.x=lerp(T.to.x,home,u);b.y=lerp(T.to.y,R.home,u);}}
er26Combat=function(b,dt){if(!rd19Owns(b)||!b._er26.mode.startsWith('rd19-'))return RD19.base.combat.apply(this,arguments);
 const C=rd19State(b),R=b._er26,T=C.turn,c=rd19Cfg();if(!T){er26Set(b,'recover');return;}
 R.warnings=[];if(R.mode==='rd19-ram')rd19Ram(b,dt);
 else{const span=C.exposed?40:22,speed=C.exposed?2.5:1.3;
  b.x=clamp(T.from.x+Math.sin(R.t*speed)*span,camLeftX()+b.w*.43,camRightX()-b.w*.43);b.y+=clamp(R.home-b.y,-80*dt,80*dt);b._drawY=b.y;
  if(R.mode==='rd19-lasers')rd19Lasers(b,dt);
  else{C.charge=R.t<R.warm?clamp(R.t/R.warm,0,1):Math.max(.12,1-(R.t-R.warm)*.6);
   if(R.t<R.warm){combatWarningTick(b,'rime-mortar-'+T.serial,R.t,R.warm);
    for(const side of [-1,1]){const p=rd19Port(b,side);R.warnings.push({...p,angle:-Math.PI/2,width:22,progress:R.t/R.warm});}}
   else{T.shot-=dt;if(T.wave<c.waves&&T.shot<=0){rd19Mortars(b);T.shot=c.gap;}}
  }}b._drawY=b.y;b._sa14.glow=C.charge;return true;};
er26Tick=function(b,dt){if(!rd19Owns(b))return RD19.base.tick.apply(this,arguments);
 mr27Init(b);const C=rd19State(b);C.age+=dt;b._rd19Critical=Math.max(0,(b._rd19Critical||0)-dt);
 if(!C.exposed&&rd19Disarmed(b)){C.exposed=true;b.name='RIME WALL - CORE CRITICAL';C.beam=null;
  groundTargetingCancel(b);er26Set(b,'rd19-ram');rd19Log('core-exposed',b);Audio.SFX.shieldBreak?.();}
 const r=RD19.base.tick.apply(this,arguments);
 if(b._er26.mode==='recover'){C.charge=Math.max(0,C.charge-dt*4);b._sa14.glow=C.charge;}
 return r;};
sa14Slug=function(b){const first=eBullets.length,r=RD19.base.slug.apply(this,arguments);
 if(rd19Owns(b))for(const q of eBullets.slice(first))if(q._sa14Slug)q._rd19IceSlug=true;return r;};
function rd19ColdBullet(q){return q._rd19IceSlug||(run.stage===3&&q._coldTracer1002);}
er26ProjectileDraw=function(q){if(!rd19ColdBullet(q))return RD19.base.projectile.apply(this,arguments);
 const key=RD19_ART.bullet.key;if(!XART.rdy(key))return true;const im=XART.get(key),h=25,w=h*im.width/im.height;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(q.x,q.y);ctx.rotate(Math.atan2(q.vy,q.vx)-Math.PI/2);ctx.drawImage(im,-w/2,-h/2,w,h);ctx.restore();RD19.draws.bullets=(RD19.draws.bullets||0)+1;return true;};
drawBullets=function(){const all=eBullets,own=all.filter(q=>rd19ColdBullet(q)&&!q.dead);eBullets=all.filter(q=>!rd19ColdBullet(q));
 try{RD19.base.bullets.apply(this,arguments);}finally{eBullets=all;}for(const q of own)er26ProjectileDraw(q);};
function rd19Effect(bank,x,y,scale,age,alpha=1){const frames=RD19_ART.banks[bank];if(!frames?.length)return false;
 const a=frames[Math.floor(Math.max(0,age)*18)%frames.length];if(!XART.rdy(a.key))return false;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;ctx.drawImage(XART.get(a.key),x-a.pivot[0]*scale,y-a.pivot[1]*scale,a.w*scale,a.h*scale);ctx.restore();
 RD19.draws[bank]=(RD19.draws[bank]||0)+1;return true;}
function rd19ChargeDraw(b,p,k,t){
 rd19Effect('swirl',p.x,p.y,rd19Owns(b)?.72:.58,t,.35+k*.55);
 rd19Effect('charge',p.x,p.y,rd19Owns(b)?.37:.31,t,.35+k*.55);
}
sa14ChargeFx=function(b,p,k,t){if(!rd19Ice(b))return RD19.base.charge.apply(this,arguments);
 const core=mr27Shape(b,'core');rd19ChargeDraw(b,core,k,t);};
mr27Draw=function(b){const r=RD19.base.draw.apply(this,arguments);if(!rd19Ice(b)||b.dead||b.enter)return r;
 const C=rd19Owns(b)?rd19State(b):null,R=b._er26;
 if(C?.beam){const old=b._l23Beam;b._l23Beam=C.beam;try{l23BossBeamDraw(b);}finally{b._l23Beam=old;}}
 const k=C?.charge||b._sa14?.glow||0;
 if(rd19Owns(b)){
  const portK=R.mode==='rd19-mortars'?k:(C?.exposed ? .14 : 0);
  if(typeof sg19Shoulders==='function')sg19Shoulders(b,portK);
  else if(portK>0)for(const side of [-1,1]){const p=rd19Port(b,side);rd19Effect('charge',p.x,p.y,.27,C.age,.25+portK*.75);}
  if(C?.exposed&&k<.02){const p=mr27Shape(b,'core');rd19Effect('swirl',p.x,p.y,.56,C.age,.45);}
 }else if(R.mode!=='recover'&&R.t<R.warm&&k<.02){const core=mr27Shape(b,'core');rd19ChargeDraw(b,core,clamp(R.t/Math.max(.1,R.warm),0,1),R.clock);}
 return r;};
groundTargetingStrikePlayers=function(q){if(!q._rd19Mortar)return RD19.base.groundHit.apply(this,arguments);
 for(const seat of seatList())withSeat(seat,()=>{if(player.dead||q.hitSeats[seat])return;
  if(dist2(player.x,player.y,q.x,q.y)<=q.radius*q.radius){q.hitSeats[seat]=1;playerHit('Cryogenic laser mortar');}});};
groundTargetingDraw=function(){const all=groundTargetingFx,own=all.filter(q=>q._rd19Mortar&&!q.dead);groundTargetingFx=all.filter(q=>!q._rd19Mortar);
 try{RD19.base.groundDraw.apply(this,arguments);}finally{groundTargetingFx=all;}
 for(const q of own){if(q.delay>0)continue;
  if(!q.impact){groundTargetReticleDraw(q.x,q.y,q.radius*2,groundTargetingPhase(q),.95);
   if(q.t<.40){const u=q.t/.40,p=q.launch;ctx.save();ctx.translate(p.x,p.y-u*125);ctx.rotate(Math.PI);rd19Effect('mortar',0,0,.30,q.t,1-u);ctx.restore();}
   const fall=clamp((q.t-q.warn+.36)/.36,0,1);if(fall>0)rd19Effect('mortar',q.x,lerp(viewTopY()-35,q.y,fall),1.15,q.t,.95);
  }else{const u=(q.t-q.warn)/q.active;rd19Effect('mortar',q.x,q.y,1.15,q.t,Math.min(1,(1-u)*2));
   rd19Effect('swirl',q.x,q.y,.48,q.t,Math.max(0,1-u));}
 }};
window.BOF_RIME_DEFENSE={state:RD19,ready:rd19Ready,disarmed:rd19Disarmed,coreAt:rd19CoreAt,port:rd19Port};
