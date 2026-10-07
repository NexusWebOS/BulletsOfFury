"use strict";
/* Hard Corps choreography transfer, 1007: settle -> tell -> commit -> release ->
   clear crossing -> recover. Authored beams and modules keep their native pixels.
   This layer owns only Sovereign, the two pursuit bombers, and Herald. */
const HC1007={version:1,draws:{beam:0,warning:0},history:[]};
const HC1007_BASE={bomber:siegeBomberTick,bomberDraw:siegeBomberDraw,
 bomberHit:siegeBomberHit,book:er26Book,set:er26Set,war:er26WarTick,moduleDamage:mr27Damage,
 heraldTell:hd1003Tell,heraldTick:hd1003Tick,heraldBlit:hd1003Blit,
 heraldBreak:hd1003Break,bullets:drawBullets,begin:beginStage};
function hc1007Rank(){return diffKey==='easy'?-1:diffKey==='normal'?0:diffKey==='hard'?1:2;}
function hc1007Warm(){av3Warm();s81003WarningWarm();}
function hc1007Live(b){return !!b&&!b.dead&&b.hp>0&&!b.enter&&b._dyingT==null;}
function hc1007Log(b,event){const row={event,kind:b._ship||b.kind||b.name,t:b._hc1007?.clock||0};HC1007.history.push(row);if(HC1007.history.length>100)HC1007.history.shift();}
function hc1007Alive(b,id){
 if(!hc1007Live(b))return false;
 if(b._hd1003){const p=hd1003Part(b,id);return !!p&&hd1003Live(b,p);}
 if(b._bomber)return id==='core'||b._bomber.parts.some(p=>p.id===id&&p.hp>0);
 if(b._s4war)return mr27CanFire(b,id);
 return false;
}
function hc1007Origin(b,id){
 if(b._hd1003)return hd1003Muzzle(b,id);
 if(b._bomber){const p=siegeBomberParts(b).find(p=>p.id===id)||siegeBomberBay(b);return{x:p.x,y:p.y+(p.h||0)*.46};}
 return shipBossMount(b,id);
}
function hc1007Line(p,a,width=13,len=VH*1.55){return{x:p.x,y:p.y,ex:p.x+Math.cos(a)*len,ey:p.y+Math.sin(a)*len,width};}
function hc1007Hit(L,label){for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&s81003Distance(player.x,player.y,L)<L.width*.5+3)playerHit(label);});}
function hc1007Warn(b,L,p,alert=false){combatWarningDraw(b,{...L,laneShape:'line',progress:clamp(p,0,1),len:Math.hypot(L.ex-L.x,L.ey-L.y),fieldOnly:!alert,alertOnly:alert,alertY:b._s4war?82:48});HC1007.draws.warning++;}
function hc1007Beam(b,L,a,color,alpha=1){
 if(!hc1007Live(b)||alpha<=0||L.width<.5)return;
 av3Beam(ctx,L.x,L.y,a,Math.hypot(L.ex-L.x,L.ey-L.y),L.width,color,b._hc1007?.clock||0,alpha,true);HC1007.draws.beam++;
}
/* A full revolution is deliberately slow. Each 60-degree sector has one long
   damaging sweep, a .20s harmless dissolution, then a fully absent crossing.
   A new .42s warning precedes every reappearance. Angles never chase a pilot. */
function hc1007CrossStart(b,ids,color='ice'){
 const rank=hc1007Rank(),H=b._hc1007||(b._hc1007={clock:0,seq:0});
 const cycle=rank<0?2.55:rank===0?2.30:rank===1?2.08:1.94;
 H.cross={age:0,warm:rank<0?1.70:1.45,cycle,duration:cycle*6,
  on:cycle*.44,fade:.20,rewarn:.42,angle:Math.PI/4,
  ids:ids.slice(),color,width:rank<0?11:rank===0?13:15,pulse:-1,releases:0};
 H.lines=[];hc1007Warm();hc1007Log(b,'cross-charge');r30Sound('bossWeaponCharge');return H.cross;
}
function hc1007CrossState(b){
 const C=b._hc1007?.cross;if(!C)return null;
 const elapsed=Math.max(0,C.age-C.warm),local=elapsed%C.cycle,pulse=Math.floor(elapsed/C.cycle),a=C.angle+TAU*Math.min(1,elapsed/C.duration);
 let mode='gap',p=0,alpha=0;
 if(C.age<C.warm){mode='tell';p=C.age/C.warm;}
 else if(elapsed>=C.duration)mode='done';
 else if(local<C.on){mode='live';alpha=1;}
 else if(local<C.on+C.fade){mode='dissolve';alpha=1-(local-C.on)/C.fade;}
 else if(local>C.cycle-C.rewarn){mode='tell';p=(local-(C.cycle-C.rewarn))/C.rewarn;}
 const origin=b._hd1003?hd1003Muzzle(b,'head'):b._s4war?shipBossMount(b,'C'):{x:b.x,y:b.y+b.h*.12};
 const rays=C.ids.map((id,i)=>({id,angle:a+i*Math.PI/2,...hc1007Line(origin,a+i*Math.PI/2,C.width)})).filter(L=>hc1007Alive(b,L.id));
 return{mode,p,alpha,pulse,local,elapsed,angle:a,rays};
}
function hc1007CrossTick(b,dt){
 const H=b._hc1007,C=H.cross;if(!C)return true;
 if(!hc1007Live(b)){H.cross=null;return true;}C.age+=dt;
 const S=hc1007CrossState(b);
 if(!S.rays.length||S.mode==='done'){H.cross=null;hc1007Log(b,'cross-recover');return true;}
 if(S.mode==='tell')combatWarningTick(b,'hc-cross-'+S.pulse,Math.max(.001,S.p)*C.rewarn,C.rewarn);
 if(S.mode==='live'){
  if(C.pulse!==S.pulse){C.pulse=S.pulse;C.releases++;r30Sound('combatBeam0927');}
  for(const L of S.rays)hc1007Hit(L,'rotating cross laser');
 }
 return false;
}
function hc1007CrossDraw(b){
 const C=b._hc1007?.cross,S=hc1007CrossState(b);if(!C||!S||!hc1007Live(b))return;
 if(S.mode==='tell'){
  // The preview follows the physical rotor, then meets the release exactly.
  for(const L of S.rays)hc1007Warn(b,L,S.p);if(S.rays[0])hc1007Warn(b,S.rays[0],S.p,true);
 }else if(S.mode==='live'||S.mode==='dissolve')for(const L of S.rays)hc1007Beam(b,L,L.angle,C.color,S.alpha);
}
function hc1007Cancel(b){if(!b?._hc1007)return;b._hc1007.cross=null;b._hc1007.lines=[];eBullets=eBullets.filter(q=>q._hc1007Owner!==b);}
mr27Damage=function(b){const r=HC1007_BASE.moduleDamage.apply(this,arguments);if(b?._hc1007){b._hc1007.lines=b._hc1007.lines.filter(L=>hc1007Alive(b,L.id));eBullets=eBullets.filter(q=>q._hc1007Owner!==b||hc1007Alive(b,q._hc1007Part));if(b.dead)hc1007Cancel(b);}return r;};
beginStage=function(n){HC1007.history=[];const r=HC1007_BASE.begin.apply(this,arguments);if([4,5,6,8].includes(n))hc1007Warm();return r;};

/* Pursuit bomber directors. Space uses crossing/paired lances; Earth uses
   marked flak gates and a committed moving gun pass. Destroyed engines reduce
   relocation speed, destroyed cannon modules cancel their pending/released fire. */
function hc1007BomberSet(b,mode){
 const H=b._hc1007,B=b._bomber,rank=Math.max(0,hc1007Rank());H.mode=mode;H.age=0;H.lines=[];H.released=0;H.target={...targetShip(b.x,b.y)};
 H.from={x:b.x,y:b.y};H.to={x:clamp(camLeftX()+viewW()*(H.seq%2?.69:.31),camLeftX()+b.w*.52,camRightX()-b.w*.52),y:b.ty};
 H.warm=hc1007Rank()<0?1.65:[1.25,1.10,1.0][rank];B.mode='hc-'+mode;B.t=0;B.target={x:H.target.x,y:H.target.y};B.history.push(B.mode);if(B.history.length>50)B.history.shift();hc1007Log(b,mode);
 if(mode==='cross'){hc1007CrossStart(b,['laserL','laserR','laserL','laserR'],B.space?'ice':'fire');return;}
 if(mode==='lances'||mode==='strafe'){
  for(const id of ['laserL','laserR'])if(hc1007Alive(b,id)){
   const p=hc1007Origin(b,id),a=Math.atan2(H.target.y-p.y,H.target.x-p.x);
   H.lines.push({id,angle:a,delay:H.lines.length*.40,fire:false,...hc1007Line(p,a,mode==='lances'?19:29)});
  }
 }
 if(mode==='flak'){
  const count=hc1007Rank()<0?4:5,left=camLeftX()+48,span=viewW()-96;
  H.gap=clamp(Math.round((H.target.x-left)/span*(count-1)),0,count-1);H.flakCount=count;
  for(let k=0;k<count;k++)if(k!==H.gap){const p=siegeBomberBay(b),x=left+k*span/(count-1),y=clamp(H.target.y,290,VH-80);H.lines.push({id:'core',tx:x,ty:y,delay:Math.abs(k-H.gap)*.18,fire:false,...s81003Lane(p.x,p.y,x,y,26,Math.hypot(x-p.x,y-p.y))});}
 }
 if(mode==='cross'||mode==='lances'||mode==='strafe'||mode==='flak')r30Sound('bossWeaponCharge');
}
function hc1007BomberNext(b){const H=b._hc1007,B=b._bomber;
 const book=B.space?['lances','cross','strafe','lances']:['flak','strafe','lances','flak'];
 let mode=book[H.seq++%book.length];
 if(!B.parts.some(p=>p.id.startsWith('laser')&&p.hp>0))mode='flak';
 hc1007BomberSet(b,mode);
}
function hc1007BomberTick(b,dt){
 const B=b._bomber;if(b.dead||B.mode==='entry'||b.enter){if(b.dead)hc1007Cancel(b);return HC1007_BASE.bomber(b,dt);}
 let H=b._hc1007;if(!H){H=b._hc1007={clock:0,seq:0};hc1007BomberSet(b,'relocate');}
 H.clock+=dt;H.age+=dt;B.clock+=dt;B.t+=dt;b.flash=Math.max(0,(b.flash||0)-dt);for(const p of B.parts)p.flash=Math.max(0,p.flash-dt);
 H.lines=H.lines.filter(L=>hc1007Alive(b,L.id));B.bombs=B.bombs.filter(q=>!q.dead);
 // Existing art and module geometry stay attached to the moving ship.
 if(H.mode==='relocate'){
  const engines=B.parts.filter(p=>p.id.startsWith('engine')&&p.hp>0).length,dur=engines===2?1.30:engines===1?1.70:2.05;
  const t=clamp(H.age/dur,0,1),u=t*t*(3-2*t);b.x=lerp(H.from.x,H.to.x,u);b.y=lerp(H.from.y,H.to.y,u);
  if(t===1)hc1007BomberNext(b);return;
 }
 if(H.mode==='recover'){if(H.age>=(hc1007Rank()<0?2.1:1.45)+(B.parts.every(p=>p.hp<=0)?.5:0))hc1007BomberSet(b,'relocate');return;}
 if(H.mode==='cross'){if(hc1007CrossTick(b,dt))hc1007BomberSet(b,'recover');return;}
 if(H.mode==='strafe'){
  const travel=clamp((H.age-H.warm)/1.25,0,1),u=travel*travel*(3-2*travel);
  b.x=lerp(H.from.x,clamp(camLeftX()+viewW()*(H.seq%2?.33:.67),camLeftX()+b.w*.52,camRightX()-b.w*.52),u);
 }
 for(const L of H.lines){
  const age=H.age-L.delay;
  if(age<H.warm){if(age>=0)combatWarningTick(b,'hc-bomber-'+H.seq+'-'+L.id,age,H.warm);continue;}
  if(!L.fire){L.fire=true;H.released++;const p=hc1007Origin(b,L.id);L.x=p.x;L.y=p.y;
   if(H.mode==='lances'){L.liveAge=0;L.ex=p.x+Math.cos(L.angle)*VH*1.5;L.ey=p.y+Math.sin(L.angle)*VH*1.5;r30Sound('combatBeam0927');}
   else if(H.mode==='flak'){
    const q=groundTargetingSpawn({kind:'missile',owner:b,x:L.tx,y:L.ty,warn:.78,active:.34,radius:25,size:75,track:false,shake:2,onImpact:q=>explode(q.x,q.y,58,B.space?'blue':'red')});q._polishBomb={x:p.x,y:p.y};B.bombs.push(q);r30Sound('enemyMissile');
   }else{L.burst=0;r30Sound('enemyMG');}
  }
  if(H.mode==='lances'){
   L.liveAge+=dt;if(L.liveAge<.76)hc1007Hit(L,'committed bomber lance');
  }else if(H.mode==='strafe'){
   const count=hc1007Rank()<0?3:4+Math.max(0,hc1007Rank());
   while(L.burst<count&&age-H.warm>=L.burst*.18){const p=hc1007Origin(b,L.id),q=siegeBomberShot(b)(p.x,p.y,L.angle,4.7+Math.max(0,hc1007Rank())*.5);Object.assign(q,{_hc1007Owner:b,_hc1007Part:L.id});L.burst++;}
  }
 }
 const last=Math.max(0,...H.lines.map(L=>L.delay));if(H.age>H.warm+last+(H.mode==='flak'?1.4:1.25))hc1007BomberSet(b,'recover');
}
siegeBomberTick=function(b,dt){if(b?._bomber)return hc1007BomberTick(b,Math.min(.05,dt));return HC1007_BASE.bomber.apply(this,arguments);};
siegeBomberHit=function(b){const r=HC1007_BASE.bomberHit.apply(this,arguments);if(b?._hc1007){b._hc1007.lines=b._hc1007.lines.filter(L=>hc1007Alive(b,L.id));eBullets=eBullets.filter(q=>q._hc1007Owner!==b||hc1007Alive(b,q._hc1007Part));if(b.dead)hc1007Cancel(b);}return r;};
function hc1007BomberDraw(b){
 const H=b._hc1007;if(!H||!hc1007Live(b))return;hc1007CrossDraw(b);
 for(const L of H.lines){if(!hc1007Alive(b,L.id))continue;const age=H.age-L.delay;
  if(!L.fire&&age>=0){hc1007Warn(b,L,age/H.warm);if(H.mode==='flak')groundTargetReticleDraw(L.tx,L.ty,65,clamp(age/H.warm,0,1),.8);}
  if(H.mode==='lances'&&L.fire&&L.liveAge<.98)hc1007Beam(b,L,L.angle,b._bomber.space?'ice':'red',L.liveAge<.76?1:1-(L.liveAge-.76)/.22);
 }
}

/* Sovereign: a relay of committed bursts between left/right gun modules and a
   pulsed cross emitted by the destructible central lightning weapon. Rearming
   cancels the attack immediately and keeps the existing four-core revival. */
er26Book=function(b){return HC1007_BASE.book.apply(this,arguments).map(m=>b._ship==='stormsovereign'?(m==='sovereign-battery'?'hc-relay1007':m==='storm-lance1002'?'hc-cross1007':m):m);};
er26Set=function(b,mode){const r=HC1007_BASE.set.apply(this,arguments);if(b._ship!=='stormsovereign')return r;
 const H=b._hc1007||(b._hc1007={clock:0,seq:0,lines:[]});H.cross=null;H.lines=[];
 if(mode==='hc-cross1007'){H.seq++;hc1007CrossStart(b,['C','C','C','C'],'lightning');b._er26.dur=H.cross.warm+H.cross.duration+.1;}
 if(mode==='hc-relay1007'){
  H.seq++;H.warm=hc1007Rank()<0?1.5:1.1;H.shots=0;H.age=0;const T=targetShip(b.x,b.y);H.target={x:T.x,y:T.y};
  const ids=H.seq%2?['L','R']:['R','L'];for(const id of ids)if(mr27CanFire(b,id)){
   const p=shipBossMount(b,id),a=Math.atan2(T.y-p.y,T.x-p.x);H.lines.push({id,angle:a,delay:H.lines.length*.65,burst:0,...hc1007Line(p,a,26)});
  }b._er26.warm=H.warm;b._er26.dur=H.warm+2.35;
 }return r;
};
er26WarTick=function(b,dt){
 const R=b._er26,S=b._s4war,H=b._hc1007;
 if(b._ship!=='stormsovereign'||!H||!['hc-relay1007','hc-cross1007'].includes(R.mode))return HC1007_BASE.war.apply(this,arguments);
 H.clock+=dt;H.age=(H.age||0)+dt;R.warnings=[];
 if(!hc1007Live(b)){hc1007Cancel(b);return true;}
 stage4ShieldTick(b,dt);stage4ShieldSyncNodes(b);er26CoreTick(b,dt);
 if(S.shield.rearming){hc1007Cancel(b);er26Set(b,'recover');return true;}
 S.poseRot=0;S.scale=1;b._drawY=b.y;b._animKey='s4w_boss_energized_'+Math.floor(H.clock*10)%12;
 if(R.mode==='hc-cross1007'){
  if(hc1007CrossTick(b,dt)){er26Set(b,'recover');R.dur=Math.max(R.dur,1.35);}return true;
 }
 for(const L of H.lines){if(!hc1007Alive(b,L.id))continue;const age=H.age-L.delay;
  if(age<H.warm){if(age>=0){combatWarningTick(b,'hc-sovereign-'+H.seq+'-'+L.id,age,H.warm);R.warnings.push({slot:L.id,angle:L.angle,width:30,progress:age/H.warm});}continue;}
  const count=hc1007Rank()<0?3:4+Math.max(0,hc1007Rank());
  while(L.burst<count&&age-H.warm>=L.burst*.16){const q=er26WarShot(b,L.id,L.angle+(L.burst-(count-1)/2)*.025,5.0+Math.max(0,hc1007Rank())*.4,'lightningmg');if(q)Object.assign(q,{_hc1007Owner:b,_hc1007Part:L.id});L.burst++;}
 }
 if(R.t>=R.dur){er26Set(b,'recover');R.dur=Math.max(R.dur,1.30);}return true;
};

/* Herald's first three taught attacks retain their original order. Thereafter
   the living wings drive a slow eclipse cross, with no skull volley underneath.
   A broken wing disables its opposite pair immediately. */
hd1003Tell=function(b){const H=b._hd1003;
 if(H.seq>=3&&H.seq%4===3&&H.parts.some(p=>p.id.startsWith('wing')&&!p.dead)){
  H.seq++;H.mode='hc-cross1007';H.age=0;H.lanes=[];H.attack='eclipse-cross';H.history.push(H.attack);if(H.history.length>30)H.history.shift();
  b._hc1007=b._hc1007||{clock:0,seq:0,lines:[]};hc1007CrossStart(b,['wingL','wingR','wingL','wingR'],'alien');return;
 }return HC1007_BASE.heraldTell.apply(this,arguments);
};
hd1003Tick=function(b,dt){const H=b._hd1003;if(H.mode!=='hc-cross1007')return HC1007_BASE.heraldTick.apply(this,arguments);
 H.clock+=dt;H.age+=dt;b._hc1007.clock+=dt;b.fireCd=999;b._sba=null;b._drawY=b.y;
 if(hc1007CrossTick(b,dt)){H.mode='rest';H.age=-.30;H.lanes=[];}return true;
};
/* Modules remain opaque until their timed rupture. Only the authored hot
   discharge dissipates; solid parts cannot become translucent ghosts. */
hd1003Blit=function(p,P,flash=0,alpha=1){return HC1007_BASE.heraldBlit(p,P,flash,p.dead?1:alpha);};
hd1003Break=function(b,p){const was=p.dead,r=HC1007_BASE.heraldBreak.apply(this,arguments);if(!was){const d=b._hd1003.debris.find(d=>d.p===p);if(d){d.vx*=1.25;d.vy=65;}}return r;};
drawBullets=function(){const r=HC1007_BASE.bullets.apply(this,arguments);if(subBoss?._bomber)hc1007BomberDraw(subBoss);if(subBoss?._hd1003)hc1007CrossDraw(subBoss);if(boss?._s4war)hc1007CrossDraw(boss);return r;};
