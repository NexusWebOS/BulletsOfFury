"use strict";
/* Thunderhead's weather reactor. Native modules, HP, rewards and hit flashes
   remain FB112's authority. All new appearance changes are authored frames. */
const THS114={base:{start:fb112Start,tick:fb112Tick,draw:fb112Draw,cancel:fb112Cancel,
 keys:fb112Keys,ready:fb112Ready,weather:bg6Draw,grade:bg6WeatherGrade,
 projectile:drawCombatFinalProjectile,early:ovSonicProjectileDraw,
 intercept:enemyOrdnanceCanIntercept,begin:beginStage,load:stageLoadBegin},
 owner:null,events:[],reduced:matchMedia('(prefers-reduced-motion: reduce)').matches,
 keys:[],limits:{rounds:24,marks:3,impacts:4}};
for(const B of Object.values(THS114_ART.banks))for(const p of B.pages){XART._src[p.key]=p.path;THS114.keys.push(p.key);}
function th114Own(b){return b?._fb112?.model==='thunder';}
function th114Log(b,event,data={}){const row={event,t:b.t,attack:b._fb112.attack,...data};THS114.events.push(row);if(THS114.events.length>1200)THS114.events.shift();fb112Log(b,'storm-'+event,data);}
function th114State(b){return b._th114||(b._th114={clock:0,weather:.3,release:0,next:0,marks:[],impacts:[],muzzle:[],fields:[],strikeSerial:0,dead:false,open:b._fb112.open});}
function th114Blit(name,f,x,y){const B=THS114_ART.banks[name];if(!B)return false;
 f=clamp(f|0,0,B.frames-1);const c=B.cells[f];if(!XART.rdy(c[0]))return false;
 ctx.drawImage(XART.get(c[0]),c[1],c[2],B.cw,B.ch,Math.round(x-B.cw/2),Math.round(y-B.ch/2),B.cw,B.ch);return true;}
fb112Keys=function(){return [...THS114.base.keys(),...THS114.keys];};
fb112Ready=function(){return THS114.base.ready()&&THS114.keys.every(k=>XART.rdy(k));};
stageLoadBegin=function(n,keys){if(n===6)Snd.prepare(['bossWeaponCharge','combatEnergy0927','combatBeam0927','overlordWind','geyserLightning','alertLockon']);return THS114.base.load.call(this,n,n===6&&fb112Rank()?[...(keys||[]),...THS114.keys]:keys);};
fb112Cancel=function(b){const out=THS114.base.cancel.apply(this,arguments);if(th114Own(b)){
 const S=th114State(b);S.marks.length=S.impacts.length=S.muzzle.length=0;for(const f of S.fields)f.dead=true;S.fields.length=0;S.dead=true;
 for(const r of eBullets)if(r._th114Owner===b)r.dead=true;
 th114Log(b,'cancel');}return out;};
beginStage=function(){if(THS114.owner)fb112Cancel(THS114.owner);THS114.owner=null;return THS114.base.begin.apply(this,arguments);};
function th114Core(b){return fb112PartPoint(b,b._fb112.core);}
function th114Muzzle(b,at){const S=th114State(b);if(S.muzzle.some(f=>f.age<.04&&Math.hypot(f.x-at.x,f.y-at.y)<2))return;S.muzzle.push({x:at.x,y:at.y,age:0});if(S.muzzle.length>6)S.muzzle.shift();}
function th114Round(b,at,angle,speed,family,part=null){
 if(part&&part.hp<=0)return null;const live=eBullets.filter(r=>!r.dead&&r._th114Owner===b);
 if(live.length>=THS114.limits.rounds)return null;
 // Native enemy bullets use .15*w/.15*h as contact half-size. Art size is
 // independent: a cyclone's42px contact diameter must not become a6px target.
 const dimensions={cyclone:[140,140],tornado:[38,100],tempest:[180,180],orb:[50,50]},D=dimensions[family],field=family==='tornado'||family==='tempest';
 const r=field?{x:at.x,y:at.y,vx:Math.cos(angle)*speed*70,vy:Math.sin(angle)*speed*70,age:0,hits:new Set(),w:D[0],h:D[1]}:eShootT(at.x,at.y,angle,speed,'l6bolt',{owner:b,silent:true,noMuzzle:true,w:D[0],h:D[1]});
 Object.assign(r,{_th114Owner:b,_th114Part:part,_th114Family:family,_th114Born:b.t,
 _th114Life:family==='tempest'?5.8:family==='tornado'?4.5:4.2,
 _weaponProof:true,_shootable:false,_noArsenal:true,_boss:true,_committed:true});
 if(field){const S=th114State(b);if(S.fields.length>=4)return null;S.fields.push(r);}
 if(family!=='orb')th114Muzzle(b,at);th114Log(b,'round',{family,x:at.x,y:at.y,part:part?.id,angle});return r;
}
enemyOrdnanceCanIntercept=function(r){return r?._th114Owner?false:THS114.base.intercept.apply(this,arguments);};
function th114RoundDraw(r){if(!r?._th114Owner)return false;if(r.dead)return true;
 const age=r._th114Owner.t-r._th114Born,name=r._th114Family,B=THS114_ART.banks[name];let f=Math.floor(age*B.fps)%B.frames;
 if(name==='tornado')f=age<.2?Math.min(3,Math.floor(age*20)):age>r._th114Life-.2?16+Math.min(3,Math.floor((age-r._th114Life+.2)*20)):4+Math.floor(age*20)%12;
 return th114Blit(name,f,r.x,r.y);}
ovSonicProjectileDraw=function(r){return r?._th114Owner?th114RoundDraw(r):THS114.base.early.apply(this,arguments);};
drawCombatFinalProjectile=function(r){return r?._th114Owner?th114RoundDraw(r):THS114.base.projectile.apply(this,arguments);};
function th114Mark(b,x,y){const S=th114State(b);if(S.marks.length>=THS114.limits.marks)return;
 const P={x:clamp(x,camLeftX()+55,camRightX()-55),y:clamp(y,viewTopY()+100,VH-42),age:0,warm:2,id:++S.strikeSerial,hits:new Set()};
 S.marks.push(P);th114Log(b,'lightning-mark',{id:P.id,x:P.x,y:P.y,warm:P.warm});}
function th114StrikeTick(b,dt){const S=th114State(b);
 for(const P of S.marks){P.age+=dt;combatWarningTick(P,'storm-ground-'+P.id,P.age,P.warm);
  if(P.age>=P.warm){P.struck=true;S.impacts.push({...P,age:0});combatAudio0927(P,'geyserLightning',.1);th114Log(b,'lightning-impact',{id:P.id,x:P.x,y:P.y,warning:P.age});}}
 S.marks=S.marks.filter(P=>!P.struck);
 for(const P of S.impacts){P.age+=dt;if(P.age<=.22)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!P.hits.has(seat)&&((player.x-P.x)/44)**2+((player.y-P.y)/22)**2<1){P.hits.add(seat);playerHit('Thunderhead ground lightning');th114Log(b,'ground-hit',{id:P.id,seat});}});}
 S.impacts=S.impacts.filter(P=>P.age<.58).slice(-THS114.limits.impacts);
}
function th114FieldsTick(b,dt){const S=th114State(b);
 for(const f of S.fields){f.age+=dt;f.x+=f.vx*dt;f.y+=f.vy*dt;
  if(b.dead||f._th114Part?.hp<=0||f.age>=f._th114Life){f.dead=true;continue;}
  // One hit per seat per front; a roll/shield still uses the native hit owner.
  // Contact never deletes this moving weather front, and art completes recovery.
  if(f.age>.2&&f.age<f._th114Life-.2)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&player.invuln<=0&&!f.hits.has(seat)&&Math.abs(player.x-f.x)<f.w/2&&Math.abs(player.y-f.y)<f.h/2){f.hits.add(seat);playerHit('Thunderhead '+f._th114Family);th114Log(b,'storm-contact',{family:f._th114Family,seat});}});
 }
 S.fields=S.fields.filter(f=>!f.dead);
}
fb112Start=function(b){if(!th114Own(b))return THS114.base.start.apply(this,arguments);
 const q=b._fb112,S=th114State(b);q.seq++;
 const book=q.open?['storm-tempest','storm-thunder','storm-cyclone','storm-tornado']:['storm-cyclone','storm-tornado','storm-thunder','storm-tempest'];
 q.attack=book[(q.seq-1)%book.length];fb112Set(b,'warn');q.dur=q.attack==='storm-tempest'?2.8:q.attack==='storm-thunder'?1.9:1.6;
 const T=targetShip(b.x,b.y);q.target={x:clamp(T.x,camLeftX()+80,camRightX()-80),y:clamp(T.y,270,VH-65)};
 S.release=0;S.next=0;S.pulses=0;S.stormLane=clamp(q.target.x,camLeftX()+180,camRightX()-180);S.camera=[camLeftX(),camRightX()];
 q.dir=q.seq%2?1:-1;q.parts.forEach(p=>{p.angle=Math.PI/2;});
 combatAudio0927(b,'bossWeaponCharge',.4);th114Log(b,'charge',{duration:q.dur,target:q.target});
};
function th114Release(b){const q=b._fb112,S=th114State(b);S.release=q.seq;th114Muzzle(b,th114Core(b));
 combatAudio0927(b,q.attack==='storm-thunder'?'geyserLightning':'overlordWind',.5);
 th114Log(b,'release',{weather:S.weather});
 if(q.attack==='storm-tornado'){
  const pods=q.parts.filter(p=>p.type==='pressure'&&p.hp>0);
  if(pods.length)for(const p of pods){const at=fb112Bore(b,p),side=p.index===0?-1:1;th114Round(b,at,Math.PI/2+side*.16,1.25,'tornado',p);}
  else th114Round(b,th114Core(b),Math.PI/2,1.55,'tornado');
 }
 if(q.attack==='storm-tempest'){
  const at=th114Core(b),angle=Math.atan2(VH+160-at.y,S.stormLane-at.x);th114Round(b,at,angle,1.35,'tempest');
  combatAudio0927(b,'combatBeam0927',.4);combatAudio0927(b,'geyserLightning',.3);
 }
}
fb112Tick=function(b,dt){if(!th114Own(b))return THS114.base.tick.apply(this,arguments);
 const before=b.t,out=THS114.base.tick.apply(this,arguments);if(b.t===before)return out;
 const q=b._fb112,S=th114State(b);THS114.owner=b;S.clock+=dt;
 if(S.open!==q.open){S.open=q.open;S.marks.length=S.impacts.length=0;for(const f of S.fields)f.dead=true;S.fields.length=0;for(const r of eBullets)if(r._th114Owner===b)r.dead=true;th114Log(b,'core-open-clear');}
 const weatherTarget=b.dead?0:q.phase==='warn'||q.phase==='attack'?(q.attack==='storm-tempest'?1:q.attack==='storm-thunder'?.88:q.attack==='storm-tornado'?.68:.48):.38;
 S.weather+=clamp(weatherTarget-S.weather,-dt*.28,dt*.35);
 for(const f of S.muzzle)f.age+=dt;S.muzzle=S.muzzle.filter(f=>f.age<.16);
 for(const r of eBullets)if(r._th114Owner===b&&(b.dead||r._th114Part?.hp<=0||b.t-r._th114Born>r._th114Life))r.dead=true;
 if(b.dead){if(!S.dead)fb112Cancel(b);return out;}
 th114StrikeTick(b,dt);
 th114FieldsTick(b,dt);
 if(q.phase!=='attack')return out;
 if(S.release!==q.seq)th114Release(b);
 const at=th114Core(b),T=targetShip(b.x,b.y);
 if(q.attack==='storm-cyclone'){
  if(q.t>=S.next&&S.pulses<3){for(const da of[-.4,0,.4])th114Round(b,at,Math.PI/2+da,2.2,'cyclone');
   for(const p of q.parts.filter(p=>p.type==='gun'&&p.hp>0)){p.recoil=.09;th114Round(b,fb112Bore(b,p),Math.PI/2,3.3,'orb',p);}
   S.pulses++;S.next+=.8;combatAudio0927(b,'combatEnergy0927',.25);}
 }else if(q.attack==='storm-thunder'){
  if(q.t>=S.next&&S.pulses<4){const dx=[0,-85,85,0][S.pulses];th114Mark(b,T.x+dx,T.y);S.pulses++;S.next+=.78;}
 }else if(q.attack==='storm-tempest'){
  if(q.t>=S.next&&S.pulses<3){const flank=S.pulses%2?1:-1;th114Mark(b,S.stormLane+flank*155,300+S.pulses*60);S.pulses++;S.next+=1.2;}
 }
 const duration=q.attack==='storm-cyclone'?4.5:q.attack==='storm-tornado'?4.9:q.attack==='storm-thunder'?5.4:6.4;
 if(q.t>duration&&S.marks.length===0&&S.impacts.length===0){fb112Set(b,'recover');q.wait=q.attack==='storm-tempest'?2.1:1.4;th114Log(b,'recovery');}
 return out;
};
function th114Retina(P){const progress=clamp(P.age/P.warm,0,1),colour=progress<.55?0:progress<.82?1:2,f=colour*8+(colour===2&&Math.floor(P.age*14)%2?6:7);th114Blit('retina',f,P.x,P.y);}
fb112Draw=function(b){const out=THS114.base.draw.apply(this,arguments);if(!th114Own(b)||b.dead||!fb112Ready())return out;
 const q=b._fb112,S=th114State(b),at=th114Core(b),charging=q.phase==='warn',active=q.phase==='attack';
 const level=charging?Math.min(3,Math.floor(q.t/q.dur*4)):active?3:0,phase=THS114.reduced?2:Math.floor(S.clock*(charging?12+level*3:12))%8;
 if(q.core.flash<=0)th114Blit('core',level*8+phase,at.x,at.y);
 for(const f of S.muzzle)th114Blit('muzzle',Math.min(3,Math.floor(f.age*24)),f.x,f.y);
 for(const f of S.fields)th114RoundDraw(f);
 for(const P of S.marks)th114Retina(P);
 for(const P of S.impacts){if(P.age<(THS114.reduced?.09:.24))th114Blit('bolt',Math.floor(P.age*24)%8,P.x,P.y-256);th114Blit('impact',Math.min(13,Math.floor(P.age*24)),P.x,P.y);}
 if(charging){
  const progress=clamp(q.t/q.dur,0,1);
  l23WarnSymbolDraw(b,{family:'rime',t:progress,warm:1,released:false,blinkT:q.t,alertX:at.x,alertY:at.y+60});
  if(q.attack==='storm-cyclone')for(const d of[-.4,0,.4])combatWarningDraw(b,{x:at.x,y:at.y,ex:at.x+Math.sin(d)*600,ey:at.y+Math.cos(d)*600,width:42,progress,fieldOnly:true});
  if(q.attack==='storm-tornado')for(const p of q.parts.filter(p=>p.type==='pressure'&&p.hp>0)){const m=fb112Bore(b,p);combatWarningDraw(b,{x:m.x,y:m.y,ex:m.x+(p.index===0?50:-50),ey:VH+50,width:72,progress,fieldOnly:true});}
  if(q.attack==='storm-tempest')combatWarningDraw(b,{x:at.x,y:at.y,ex:S.stormLane,ey:VH+100,width:200,progress,fieldOnly:true});
 }
 return out;
};
function th114Weather(){const b=THS114.owner;if(!b||run.stage!==6||(!b.dead&&b!==boss)||b._fb112.death>3)return false;
 const S=th114State(b),t=S.clock,grade=clamp(Math.round(S.weather*6),1,6);
 // World-space tiles and two independently drifting cloud banks. No render clock.
 for(let y=128;y<650;y+=256)for(let x=170;x<worldWidth()+340;x+=340)th114Blit('grade',grade,x,y);
 for(let i=0;i<3;i++){
  const x=((i*265+t*9)%(worldWidth()+288))-144,y=65+i*185;
  th114Blit('cloud_far',Math.floor(t*3+i)%6,x,y);
 }
 for(let i=0;i<3;i++){
  const x=((i*435-t*17)%(worldWidth()+384)+(worldWidth()+384))%(worldWidth()+384)-192;
  th114Blit('cloud_near',Math.floor(t*4+i*2)%6,x,150+i*135);
 }
 const f=(S.weather>.65?8:0)+Math.floor(t*24)%8;
 for(let y=128;y<650;y+=256)for(let x=170;x<worldWidth()+340;x+=340)th114Blit('rain',f,x,y);
 return true;
}
bg6Draw=function(){return th114Weather()?undefined:THS114.base.weather.apply(this,arguments);};
bg6WeatherGrade=function(){if(run.stage===6&&th114Own(boss)&&!boss.dead)return;return THS114.base.grade.apply(this,arguments);};
globalThis.BOF_THUNDERHEAD_STORM_1104={state:THS114,art:THS114_ART,owns:th114Own};
