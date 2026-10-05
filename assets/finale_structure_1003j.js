'use strict';
/* Encounter identity and copied combat form are separate state machines.
   0: drone/mutation. 1: ghost. 2: Dracula and his eight persistent lives.
   Life budgets calibrated against initialized campaign bosses, October 3, 2026.
   Knight gets 1.5 host lives instead of importing Hammer's multi-armor budget. */
const J3_BASE={spawn:spawnBoss,tick:r30Tick,form:r30Form,attack:r30Attack,attackTick:r30AttackTick,
 draw:r30DrawBoss,hit:modularHit,gauge:fmcGauge,bar:drawHealthBarV2,visible:bossHealthVisible,
 frac:bossHealthFraction,pose:r30Pose,parts:r30Parts,targets:retinaBossTargets,
 shot:f1003bShot,update:updatePlay,controls:s6OpeningControlsLocked,enemyShot:eShootT,
 rebelDamage:rebelSquadDamage,rebelTick:rebelSquadTick,pause:pauseTapped};
const J3_SOURCE_HP={
 easy:[1200,874,1236,1728,2112,1800,2139,2028],
 normal:[2600,1829,2590,3168,3872,3900,4489,3716],
 hard:[3300,2012,3236,3961,4840,4950,4938,4647],
 furious:[4100,2378,3365,4680,5720,6150,5836,6150],
 insanity:[4700,2835,4011,5580,6820,7050,6959,7330]
};
const J3={dialogueLive:false};
RF28_K.shield=[0,0,0];RF28_K.noShields=true;
// Source encounter grammar: Rime's open gates / cannon relay / orb siege,
// and the Warden's portal volley / leaping shock waves, with alien additions.
F1003B_FORMS[3].book=['iceGates','iceLance','iceSiege','glacierPress','gravity'];
F1003B_FORMS[7].book=['wardenMG','stomp','scissor','portalVolley','gravity','code'];
const J3_CUSTOM=new Set(['iceGates','iceSiege','glacierPress','portalVolley']);
function j3State(b){return b?._r30?.finale1003j;}
function j3Log(b,event,data={}){b._r30.history.push({event,encounter:j3State(b).encounter,mimic:j3State(b).mimic,...data});}
function j3Health(b,hp,max){b.hp=Math.max(0,hp);b.maxhp=b._vPhaseHp=max;const core=b.parts.find(p=>p.id==='core');if(core){core.hp=b.hp;core.maxhp=max;core.destroyed=false;}}
function j3Save(b){const J=j3State(b);if(J.encounter!==2)return;J.hp[J.active]=b.hp;if(J.mimic!=null)J.modules[J.mimic]=b.parts;}
function j3Next(J){for(let n=0;n<8;n++){const i=(J.active+1+n)%8;if(J.hp[i]>0)return i;}return -1;}
function j3Clear(b){r30Clear(b);S81003.beams=S81003.beams.filter(q=>q.owner!==b);b._r30.attack=null;b._r30.shield=0;b._r30.returning=null;}
function j3Encounter(b,n){
 const S=b._r30,J=j3State(b);J.encounter=n;J.mimic=null;J.attacks=0;S.base=J3_SOURCE_HP[diffKey]?.[0]||2600;
 if(n===0){J3_BASE.form(b,0);b.name='THE MUTATED DRONE';}
 else{S.finale1003b=false;S.modular1003c=false;S81003_BASE.form(b,n);b.name=n===1?'THE GHOST IN THE CODE':'THE VILE COLOSSUS';}
 S.base=J3_SOURCE_HP[diffKey]?.[0]||2600;S.fx=[];S.walls=[];S.orbitals=[];S.returning=null;S.ghostHidden=false;S.wallAge1003=0;
 // Ghost is a single complete authored specter, with no invisible arm HP.
 if(n===1)b.parts=b.parts.filter(p=>p.id==='core');
 const hp=n===2?J.hp[J.active]:Math.ceil(S.base*(n===1?1.15:1));j3Health(b,hp,n===2?J.max[J.active]:hp);
 if(n!==1)for(const p of b.parts)if(p.id!=='core'){p.hp=p.maxhp=Math.ceil(hp*.18);p.destroyed=false;}
 b._noHit=false;b.enter=true;b.ty=n===2?220:215;b.x=worldWidth()/2;b.y=b.ty;S.cd=1.25;S.seq=0;S.t=0;
 S.mode=n===0?'arrival1003j':n===2?'coronation1003j':'reveal1003j';
 j3Log(b,'encounterStart',{hp:b.hp,max:b.maxhp});
}
spawnBoss=function(){const r=J3_BASE.spawn.apply(this,arguments);if(boss?._r30){
 const max=(J3_SOURCE_HP[diffKey]||J3_SOURCE_HP.normal).slice(),S=boss._r30;
 S.finale1003j={encounter:0,mimic:null,active:0,max,hp:max.slice(),modules:[],attacks:0,visited:[],gaugeLife:-1};
 j3Encounter(boss,0);
 }return r;};
function j3Mimic(b,i){
 const S=b._r30,J=j3State(b);j3Save(b);J.active=i;J.mimic=i;J.attacks=0;
 J3_BASE.form(b,i);S.pools=J.max;S.base=J.max[i];
 if(J.modules[i])b.parts=J.modules[i];else for(const p of b.parts)if(p.id!=='core'){
  p.hp=p.maxhp=Math.ceil(J.max[i]*(p.spec?.hp||.18));p.destroyed=false;
 }
 j3Health(b,J.hp[i],J.max[i]);S.mode='reveal1003j';S.t=0;S.cd=1.1;b.enter=true;
 if(!J.visited.includes(i))J.visited.push(i);j3Log(b,'mimicEnter',{id:f1003bDef(b).id,hp:b.hp,max:b.maxhp});
}
function j3Home(b){
 const S=b._r30,J=j3State(b);j3Save(b);const next=j3Next(J);if(next<0)return j3FinalDeath(b);
 J.active=next;j3Encounter(b,2);S.mode='reveal1003j';S.t=0;J.attacks=0;j3Log(b,'draculaReturn');
}
function j3Morph(b,to){const S=b._r30;j3Save(b);j3Clear(b);S.mode='transform1003j';S.t=0;j3State(b).destination=to;b.enter=true;r30Sound('teleportIn');j3Log(b,'transformStart',{to});}
function j3FinalDeath(b){const S=b._r30;j3Clear(b);S.finale1003b=false;S.modular1003c=false;S81003_BASE.form(b,2);j3State(b).mimic=null;S.form=7;S.mode='finalFall';S.t=0;S.origin={x:b.x,y:b.y};S.nextBurst=0;b.enter=true;b.hp=0;j3Log(b,'finalDeath');r30Sound('expBig');}
r30Break=function(b){const J=j3State(b);if(!J)return F1003B_BASE.break.apply(this,arguments);const S=b._r30;if(S.mode!=='fight')return;
 j3Save(b);j3Clear(b);b.hp=0;b.enter=true;S.t=0;S.origin={x:b.x,y:b.y};S.nextBurst=0;
 if(J.encounter<2){S.mode='encounterFall1003j';Audio.stopMusic();j3Log(b,'encounterDefeated');r30Sound('expBig');}
 else{J.hp[J.active]=0;if(J.hp.every(h=>h<=0))j3FinalDeath(b);else j3Morph(b,'home');}
};
modularHit=function(dmg){const b=boss,J=j3State(b);if(!J)return J3_BASE.hit.apply(this,arguments);
 if(!r30Live(b)||!(dmg>0)||!Number.isFinite(dmg))return;
 if(b._r30.finale1003b){const r=J3_BASE.hit.apply(this,arguments);j3Save(b);return r;}
 const p=b.parts.includes(b._lastPart)&&!b._lastPart.destroyed?b._lastPart:b.parts[0],dealt=Math.min(dmg,b.hp);
 b.hp-=dealt;p.flash=.12;markHit(b,.12);stageStats.dmgDealt+=dealt;
 if(p.id!=='core'){p.hp=Math.max(0,p.hp-dmg);if(!p.hp){p.destroyed=true;r30FX(b,b.x,b.y,100);r30Sound('combatModule0927');}}
 b.parts[0].hp=b.hp;j3Save(b);if(!b.hp)r30Break(b);
};
// The first two encounters cannot borrow a transformation. Dracula alone owns it.
r30Attack=function(b){const J=j3State(b),S=b?._r30;if(!J)return J3_BASE.attack.apply(this,arguments);
 if(J.encounter===2&&J.attacks>=(J.mimic==null?3:f1003bDef(b).book.length))return j3Morph(b,J.mimic==null?J.active:'home');
 if(J.mimic!=null&&J3_CUSTOM.has(f1003bDef(b).book[S.seq%f1003bDef(b).book.length])){
  const type=f1003bDef(b).book[S.seq++%f1003bDef(b).book.length],Q=r30Pose(b);J.attacks++;
  const P=S.attack={type,j3Signature:f1003bDef(b).id,t:0,tell:diffKey==='easy'?1.65:1.2,active:3.1,next:0,fired:0,seq:S.seq,lanes:[],
   tx:clamp(player.x,camLeftX()+60,camRightX()-60),ty:clamp(player.y,260,VH-70),fromX:Q.x,fromY:Q.y};
  P.gap=clamp(Math.round((Math.atan2(P.ty-Q.y,P.tx-Q.x)-Math.PI/2)/.13+6),1,11);
  P.sweepWarnings=[];for(let i=0;i<13;i++)if(Math.abs(i-P.gap)>1){const a=Math.PI/2+(i-6)*.13;P.sweepWarnings.push({x:Q.x,y:Q.y+45,ex:Q.x+Math.cos(a)*430,ey:Q.y+45+Math.sin(a)*430,width:13});}
  if(type==='portalVolley'){P.portal={x:clamp(P.tx+(P.seq%2?110:-110),camLeftX()+85,camRightX()-85),y:180};P.sweepWarnings=[];P.tell=1.55;}
  r30Sound('bossWeaponCharge');j3Log(b,'signature',{source:P.j3Signature,type});return;
 }
 if(J.encounter===0||J.mimic!=null){J3_BASE.attack(b);J.attacks++;const P=S.attack;
  P.j3Signature=f1003bDef(b).id;
  if(P.type==='iceLance'){P.tell=3;P.active=1.2;}
  if(['rotorMG','iceMG','wardenMG','magma','missiles','bombing','eruptions'].includes(P.type)){P.active=P.type==='bombing'?3.2:P.type==='eruptions'?3.4:2.6;P.next=0;}
  // The Warden cuts with his independent claws; the old copy fired two generic lasers.
  if(P.type==='scissor'){P.lanes=[];P.active=1.7;P.tell=1.1;P.tx=clamp(P.tx,camLeftX()+70,camRightX()-70);}
  j3Log(b,'signature',{source:P.j3Signature,type:P.type});return;
 }
 const ghost=J.encounter===1,book=ghost?['ghost','codeRain','ghost','bombs']:['arms','tentacles'];
 const type=book[S.seq++%book.length],n=r30Difficulty();J.attacks++;
 S.attack={type,t:0,tell:ghost?1.08:1.2,active:type==='ghost'?(2+Math.min(2,n))*1.85:2.6,next:0,cycle:0,cycleTime:1.85,strikeAt:1.12,gap:S.seq%6,
 tx:clamp(player.x,camLeftX()+60,camRightX()-60),ty:clamp(player.y,245,VH-70),fromX:b.x,fromY:b.y};
 r30Sound('bossWeaponCharge');combatWarningTick(b,'j3-'+J.encounter+'-'+S.seq,0,S.attack.tell,true);j3Log(b,'attack',{type});
};
function j3Volley(b,P,u){
 const id=P.j3Signature,type=P.type,n=r30Difficulty(),ports=f1003bMuzzles(b),aim=m=>Math.atan2(P.ty-m.y,P.tx-m.x);
 const shot=(m,a,speed,kind,big=false)=>f1003bShot(b,m.x,m.y,a,speed,kind,big);
 P.fired++;const k=P.fired;
 if(type==='rotorMG'){
  P.next=u+.13;for(const m of ports)if((k%8<3&&m.side<0)||(k%8>=4&&k%8<7&&m.side>0))shot(m,Math.PI/2+m.side*(.08+u*.14),4.5,'code');
 }else if(type==='iceMG'){
  P.next=u+.28;for(const [i,m]of ports.entries())if(i%2===k%2)for(const d of [-.13,.13])shot(m,aim(m)+d,3.5,'ice');
 }else if(type==='wardenMG'){
  P.next=u+.16;for(const m of ports)if(k%7<5)shot(m,Math.PI/2+m.side*(.30*Math.sin(u*1.8)),4.2,'toxic');
 }else if(type==='magma'){
  P.next=u+.8;for(const m of ports)for(let i=-2;i<=2;i++)shot(m,aim(m)+i*.20,2.1+Math.abs(i)*.22,'fire',true);
 }else if(type==='missiles'){
  P.next=u+(id==='storm'?.46:.7);for(const m of ports){const a=aim(m)+(id==='harrier'?m.side*.42:0);shot(m,a,2.4,'missile');}
 }else if(type==='bombing'){
  P.next=u+.6;for(const m of ports){const a=Math.PI/2+m.side*.18;shot(m,a,1.8,'missile');}
 }else if(type==='eruptions'){
  // Furnace's advancing firewall leaves a two-column escape corridor.
  P.next=u+1.05;const gap=(P.seq+k)%7;for(let i=0;i<8;i++)if(i!==gap&&i!==gap+1){const m={x:camLeftX()+viewW()*(i+.5)/8,y:b.y+105};shot(m,Math.PI/2,1.9+n*.12,'fire',true);}
 }
 r30Sound(type.endsWith('MG')?'enemyMachineGunHeavy':type==='magma'||type==='eruptions'?'combatOrb0927':'enemyBossCannon');
}
r30AttackTick=function(b,dt){const J=j3State(b),S=b?._r30;if(!J)return J3_BASE.attackTick.apply(this,arguments);
 if(J.encounter===1||J.encounter===2&&J.mimic==null){S81003_BASE.attackTick(b,dt);S.returning=null;return;}
 const P=S.attack;if(!P)return;
 if(J3_CUSTOM.has(P.type)){
  P.t+=dt;const u=P.t-P.tell;combatWarningTick(b,'j3-'+S.form+'-'+P.seq,Math.min(P.t,P.tell),P.tell);
  if(u<0)return;
  if(!P.started){P.started=true;r30Sound(P.portal?'teleportIn':'combatOrb0927');}
  if(u>=P.next){P.next=u+(P.type==='iceSiege'?.9:.72);P.fired++;
   const Q=r30Pose(b),guns=fmcRig(b).filter(v=>v.spec.tags?.includes(P.type==='portalVolley'?'wardenMG':'iceLance'));
   if(P.type==='iceGates'||P.type==='glacierPress'){
    for(let i=0;i<13;i++)if(Math.abs(i-P.gap)>1)f1003bShot(b,Q.x,Q.y+45,Math.PI/2+(i-6)*.13,3.3,'ice');
   }else for(const [i,v] of guns.entries())if(i%2===P.fired%2){const m=fmcPoint(v,...v.spec.emit),a=Math.atan2(P.ty-m.y,P.tx-m.x);
    if(P.type==='iceSiege'){const q=f1003bShot(b,m.x,m.y,a,1.9,'ice',true);if(q){q._j3Fuse=1.15;q._j3Burst='ice';q._j3Age=0;}}
    else for(const d of [-.22,0,.22])f1003bShot(b,m.x,m.y,a+d,3.5,'toxic');
   }
   r30Sound(P.type==='portalVolley'?'enemyBossCannon':'combatOrb0927');
  }
  if(u>=P.active){S.attack=null;S.cd=1.3;S.ghostHidden=false;}return;
 }
 const volley=['rotorMG','iceMG','wardenMG','magma','missiles','bombing','eruptions'].includes(P.type);
 // Retain the existing warnings, laser collision, generated audio and modular
 // knight combo; replace only the generic volley that made each copy identical.
 const next=P.next;if(volley)P.next=Infinity;J3_BASE.attackTick(b,dt);
 if(volley&&S.attack===P){P.next=next;const u=P.t-P.tell;if(u>=0&&u<=P.active&&u>=P.next)j3Volley(b,P,u);}
 if(S.attack!==P)return;
 const u=P.t-P.tell;
 if(P.type==='scissor'&&u>=0){
  for(const v of r30Parts(b).filter(v=>v.p.spec?.role==='claw')){
   const tip=fmcPoint(v,.5,.92);for(const seat of seatList())withSeat(seat,()=>{if(Math.hypot(player.x-tip.x,player.y-tip.y)<30)playerHit('alien Warden pincer');});
  }
 }
 if(P.type==='turbines'&&u>=0&&u>(P.j3FanNext||0)){P.j3FanNext=u+.8;for(const v of fmcRig(b).filter(v=>v.spec.role==='fan'))f1003bRing(b,v.x,v.y,6,'code',P.fired++*.3);}
};
f1003bShot=function(b,x,y,a,speed,kind,large){const q=J3_BASE.shot.apply(this,arguments);
 if(q&&j3State(b)&&kind==='toxic'){delete q._er26Art;q.kind='s7laser';q._noArsenal=true;}
 return q;};
r30Pose=function(b){const J=j3State(b);if(!J)return J3_BASE.pose.apply(this,arguments);
 const S=b._r30,P=S.attack;if(J.encounter===1||J.encounter===2&&J.mimic==null)return S81003_BASE.pose(b);
 const Q=J3_BASE.pose(b);
 if(P?.type==='glacierPress'){Q.y+=Math.sin(clamp((P.t-P.tell)/P.active,0,1)*Math.PI)*64;}
 if(P?.portal){const u=P.t/P.tell;Q.alpha=u<.30?1-u/.30:u<.65?0:clamp((u-.65)/.28,0,1);if(u>=.65){Q.x=P.portal.x;Q.y=P.portal.y;}}
 if(P?.j3Signature==='chopper'&&['rotorMG','bombing'].includes(P.type)){Q.x+=Math.sin(P.t*.9)*55;}
 if(P?.type==='scissor'&&P.t>=P.tell){const u=clamp((P.t-P.tell)/P.active,0,1),f=Math.sin(u*Math.PI);Q.x=lerp(Q.x,P.tx,f);Q.y=lerp(Q.y,P.ty-90,f);}
 return Q;
};
function j3Timers(b,dt){const S=b._r30;S.t+=dt;S.clock+=dt;b.t+=dt;b.flash=Math.max(0,(b.flash||0)-dt);for(const p of b.parts){p.flash=Math.max(0,(p.flash||0)-dt);p.kick=Math.max(0,(p.kick||0)-dt);}for(const f of S.fx)f.t+=dt;S.fx=S.fx.filter(f=>f.t<.7);}
r30Tick=function(b,dt){const J=j3State(b);if(!J)return J3_BASE.tick.apply(this,arguments);const S=b._r30;dt=Math.min(.05,dt);
 for(const q of eBullets.filter(q=>q._j3Fuse&&!q.dead)){q._j3Age+=dt;if(q._j3Age>=q._j3Fuse){q.dead=true;f1003bRing(b,q.x,q.y,7,q._j3Burst,.18);r30FX(b,q.x,q.y,60);r30Sound('expSmall');}}
 if(['finalFall','escape','reunion','done'].includes(S.mode))return F1003B_BASE.tick(b,dt);
 if(S.mode==='fight'){
  if(J.encounter===2&&!S.attack&&S.cd<=0&&J.attacks>=(J.mimic==null?3:f1003bDef(b).book.length))return j3Morph(b,J.mimic==null?J.active:'home');
  J3_BASE.tick(b,dt);j3Save(b);return;
 }
 j3Timers(b,dt);b.enter=true;eBullets.length=0;for(const seat of seatList())withSeat(seat,()=>{player.invuln=Math.max(player.invuln||0,.3);});
 if(S.mode==='arrival1003j'){b.y=lerp(-170,b.ty,clamp(S.t/2,0,1));if(S.t>=2){S.mode='takeover';S.t=0;j3Log(b,'mutationStart');r30Sound('combatAlien0927');}return;}
 if(S.mode==='takeover'&&S.t>=5.2){S.mode='fight';S.t=0;b.enter=false;bossPhaseMusic(8,1);j3Log(b,'fightStart');return;}
 if(S.mode==='encounterFall1003j'){
  b.y=S.origin.y+S.t*S.t*30;if(S.t>S.nextBurst){S.nextBurst=S.t+.22;r30FX(b,b.x+Math.sin(S.t*17)*65,b.y+Math.cos(S.t*11)*50,110);r30Sound('expBig');}
  if(S.t>=2.8){S.mode='encounterReform1003j';S.t=0;b.x=worldWidth()/2;b.y=215;}return;
 }
 if(S.mode==='encounterReform1003j'&&S.t>=3){j3Encounter(b,J.encounter+1);bossPhaseMusic(8,J.encounter+1);r30Sound('bossPhase');return;}
 if(S.mode==='coronation1003j'){
  const life=fmcGauge(b).charge;if(life!==J.gaugeLife&&life>=0){J.gaugeLife=life;r30Sound('combatEnergy0927');j3Log(b,'lifeFill',{life});}
  if(S.t>=4.7){S.mode='fight';S.t=0;b.enter=false;j3Log(b,'fightStart');}return;
 }
 if(S.mode==='transform1003j'&&S.t>=1.25){const to=J.destination;if(to==='home')j3Home(b);else j3Mimic(b,to);return;}
 if(S.mode==='reveal1003j'&&S.t>=1.15){S.mode='fight';S.t=0;b.enter=false;j3Log(b,'fightStart');}
};
// One health-bar housing. Eight fills belong only to Dracula's introduction.
fmcGauge=function(b){const J=j3State(b);if(!J)return J3_BASE.gauge.apply(this,arguments);const S=b._r30;
 if(S.mode==='coronation1003j'){
  const t=Math.max(0,S.t-.3),n=clamp(Math.floor(t/.5),0,7);return{charge:n,color:F1003B_FORMS[n].color,under:n?F1003B_FORMS[n-1].color:null,frac:clamp((t-n*.5)/.40,0,1)};
 }
 return{charge:-1,color:J.encounter===0?'#e74f66':J.encounter===1?'#b8e9ff':F1003B_FORMS[J.active].color,under:null,frac:clamp(b.hp/Math.max(1,b.maxhp),0,1)};
};
bossHealthVisible=function(b){return j3State(b)?['fight','takeover','reveal1003j','coronation1003j','transform1003j'].includes(b._r30.mode):J3_BASE.visible.apply(this,arguments);};
bossHealthFraction=function(b){return j3State(b)?fmcGauge(b).frac:J3_BASE.frac.apply(this,arguments);};
drawHealthBarV2=function(kind){const b=boss;if(kind!=='boss'||!j3State(b))return J3_BASE.bar.apply(this,arguments);
 const flag=b._r30.modular1003c;b._r30.modular1003c=true;try{return J3_BASE.bar.apply(this,arguments);}finally{b._r30.modular1003c=flag;}
};
function j3Body(b,alpha=1){const J=j3State(b);if(J.encounter===0||J.mimic!=null)return f1003bBodyDraw(b,alpha);
 ctx.save();ctx.globalAlpha*=alpha;for(const v of r30Parts(b)){r30Blit(v.key,v.x,v.y,v.w,v.h,v.rot,v.alpha);
  const hit=Math.max(v.p.flash||0,b.flash||0);
  if(hit>0)fmcWhiteBlit(v.key,v.x,v.y,v.w,v.h,v.rot,v.alpha*Math.min(1,hit*9));}
 ctx.restore();
}
r30DrawBoss=function(b){const J=j3State(b);if(!J)return J3_BASE.draw.apply(this,arguments);const S=b._r30,T=S.t;
 if(['escape','reunion','done'].includes(S.mode))return S81003_BASE.draw(b);
 if(S.mode==='arrival1003j')return r30Blit('vile24_robot_gray',b.x,b.y,230,230,0,1);
 if(S.mode==='fight'){
  J3_BASE.draw(b);const P=S.attack;if(P?.portal&&P.t<P.tell){r30Blit('vile25_phantom_ground_portal',P.portal.x,P.portal.y,135,75,0,.85);groundTargetReticleDraw(P.portal.x,P.portal.y,100,P.t/P.tell,.9);}return;
 }
 if(S.mode==='takeover')return J3_BASE.draw(b);
 if(['encounterFall1003j','finalFall'].includes(S.mode)){j3Body(b,Math.max(0,1-T/3));for(const f of S.fx)r30Blit('fx_'+Math.min(3,Math.floor(f.t/.7*4)),f.x,f.y,f.size,f.size,0,1-f.t/.7);return;}
 const rebuild=S.mode==='encounterReform1003j',out=S.mode==='transform1003j',duration=rebuild?3:out?1.25:1.15;
 if(!rebuild)j3Body(b,S.mode==='coronation1003j'?clamp(T/.7,0,1):out?1-clamp(T/duration,0,1):clamp(T/.7,0,1));
 if(T<duration){const f=clamp(T/duration,0,1)*11,i=Math.floor(f),a=Math.min(1,T/.12,(duration-T)/.2)*.8;
  cwdCell('morph',i,b.x,b.y,340,370,a*(1-(f-i)));if(i<11)cwdCell('morph',i+1,b.x,b.y,340,370,a*(f-i));}
};

/* Rebel ships remain complete authored plates, including all four measured
   pitch frames. Hull damage no longer deletes rectangular wing slices. */
function j3RebelHull(q){q.shield=q.shieldMax=0;q.rfRegen=true;for(const p of fr27RebelModules(q))p.hp=p.max;}
rebelSquadTick=function(b,dt){for(const q of b._rebels.ships)j3RebelHull(q);const r=J3_BASE.rebelTick.apply(this,arguments);for(const q of b._rebels.ships)j3RebelHull(q);return r;};
rebelSquadHitTest=function(b,x,y){const hit=FR27_BASE.rebelHit(b,x,y);b._rebels.frHit=null;return hit;};
rebelSquadDamage=function(b,dmg){const R=b._rebels,q=R.ships[R.hit];if(!q||!R.frIntro?.done||q.dead||q.mode==='entry'||q.warp>0)return;
 j3RebelHull(q);R.frHit=null;return FR27_REBEL_DAMAGE.apply(this,arguments);};
retinaBossTargets=function(b){if(!b?._rebels)return J3_BASE.targets.apply(this,arguments);const R=b._rebels;if(!R.frIntro?.done||b.dead)return[];
 return R.ships.filter(q=>!q.dead&&q.mode!=='entry'&&!(q.warp>0)).map(q=>retinaDynamicPiece(b,q.key+'-hull','rival',()=>({x:q.x,y:q.y,hp:q.hp,dead:q.dead||q.mode==='entry'||q.warp>0}),d=>{R.hit=q.i;R.frHit=null;hitBoss(d);},62,70));
};
fr27RebelDrawShip=function(q){
 const f=q.evadeT>0?Math.min(7,Math.floor((1-q.evadeT/.38)*8)):0,key='rr_roll_'+REBEL_SHIPS[q.i]+'_'+f,k=XART.rdy(key)?key:'rr_ship_'+REBEL_SHIPS[q.i];if(!XART.rdy(k))return;
 const pitch=q.frSomersault&&q.evadeT>0&&q.rfHeading==null&&XART.rdy('fr27_rebel_pitch');let im=XART.get(k),sx=0,sy=0,cw=im.width,ch=im.height,w=SHIP_DRAW_H*1.5,h=w*ch/cw;
 if(pitch){const row=H3_PITCH[q.i],r=row[clamp(Math.floor((1-q.evadeT/.38)*4),0,3)],s=SHIP_DRAW_H*1.5/Math.max(...row.map(a=>Math.max(a[2],a[3])));im=XART.get('fr27_rebel_pitch');sx=r[0]-3;sy=r[1]-3;cw=r[2]+6;ch=r[3]+6;w=cw*s;h=ch*s;}
 ctx.save();ctx.translate(q.x,q.y);if(q.rfHeading!=null)ctx.rotate(q.rfHeading-Math.PI/2);ctx.imageSmoothingEnabled=false;ctx.globalAlpha=q.frCloak>0?.3:1;
 ctx.drawImage(im,sx,sy,cw,ch,-w/2,-h/2,w,h);
 if(q.flash>0){const white=xartTint(pitch?'fr27_rebel_pitch':k,'#ffffff',1);
  if(white){ctx.globalAlpha=(q.frCloak>0?.3:1)*Math.min(1,q.flash*9);ctx.drawImage(white,sx,sy,cw,ch,-w/2,-h/2,w,h);}}
 ctx.restore();if(q.frCast)combatWarningDraw(q,{x:q.x,y:q.y+28,ex:q.frCast.tx,ey:q.frCast.ty,progress:q.frCast.t/1.1,width:q.frCast.kind==='orb'?75:28,alpha:.3});
};
/* Run the world during protected radio dialogue. Only scheduled combat waits;
   flight, scrolling, ship animation, particles and dialogue clocks keep moving. */
pauseTapped=function(){if(h3Locked())return false;return J3_BASE.pause.apply(this,arguments);};
s6OpeningControlsLocked=function(){if(J3.dialogueLive)return false;return J3_BASE.controls.apply(this,arguments);};
eShootT=function(){if(J3.dialogueLive)return{dead:true,x:arguments[0],y:arguments[1],vx:0,vy:0};return J3_BASE.enemyShot.apply(this,arguments);};
updatePlay=function(dt){
 if(state!==GS.PLAY||!(fb2TalkActive()||h3RebelIntro()))return J3_BASE.update.apply(this,arguments);
 const plan=stagePlan,time=stageTimer,wave=waveIdx,spawn=spawnClock,release=H3.release;
 J3.dialogueLive=true;stagePlan=[];eBullets.length=0;groundTargetingReset();polishLanes=[];
 AV3.clock+=Math.max(0,dt);
 for(const e of enemies)e.fireCd=Math.max(e.fireCd||0,dt+1);
 try{H3_UPDATE(dt);}finally{stagePlan=plan;stageTimer=time;waveIdx=wave;spawnClock=spawn;J3.dialogueLive=false;}
 eBullets.length=0;groundTargetingReset();polishLanes=[];
 av3AudioTick(0);if(typeof Snd!=='undefined'&&Snd)for(const c of ['laser_burn','cole_laser6','cole_laser7','firewall_burn'])if(!AV3.loops.has(c))Snd.loopOff('av3_'+c);
 if(fb2Talk?.beats[fb2Talk.i]?.kind!=='demo')pBullets.length=0;
 Input.clearTaps?.();H3.release=release||!h3Locked();
};
