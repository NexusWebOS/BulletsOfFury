'use strict';
/* October 23 player-review corrections. Part pools are real damage budgets;
   projectile collision, held beams and Retina use the same exposed geometry. */
const ER23={events:[],base:{intercept:enemyOrdnanceCanIntercept,reaverInit:er26Init,
 reaverHit:av3ReaverHit,reaverAt:av3ReaverAt,at:mr27At,bomberAt:siegeBomberAt,
 coreAt:stage4CoreTurretAt,shieldAt:stage4ShieldNodeAt,coreTarget:stage4CoreTurretTarget,
 throwReflect:hammerThrowReflect,throwTick:hammerBoomerangTick,targetable:hammerWeaponTargetable,
 warning:hf22ThrowWarning,state:hammerState,damage:hammerBossDamage}};
ER23.base.bossAt=bossHitTest;ER23.base.bossHit=hitBoss;
bossHitTest=function(x,y){const b=boss;
 if(b?._ship==='stormsovereign'&&!b.dead&&!b.enter){
  b._s4ShieldHit=stage4ShieldNodeAt(b,x,y,2);b._s4CoreHit=stage4CoreTurretAt(b,x,y,2);
  if(b._s4ShieldHit||b._s4CoreHit)return true;
  const H=b._s4war?.shield;
  if(H?.active&&H.nodes.some(n=>!n.dead&&Math.abs(x-n.x)<32&&y>n.y+40))return false;
  if(b._s4war?.coreUnlocked&&b._s4war.coreTurrets.some(n=>!n.dead&&n.materialize>=.92&&Math.abs(x-n.x)<50&&y>n.y+48))return false;
 }
 const r=ER23.base.bossAt.apply(this,arguments);
 if(r&&b?._hammer?.throw&&b._hammerModuleHit==='hammer'&&!hammerMissile(_dmgBullet)){b._hammerModuleHit=null;return false;}return r;
};
hitBoss=function(dmg){const b=boss;
 // Detached objectives stay vulnerable even while the hull is in a depth pass.
 // Hull damage clamps must never absorb a projectile intended for a generator.
 if(b?._ship==='stormsovereign'&&!b.dead){
  if(b._s4CoreHit){const p=b._s4CoreHit;b._s4CoreHit=null;stage4CoreTurretDamage(b,p,dmg);weaponHitSfx('normal');return;}
  if(b._s4ShieldHit){stage4ShieldAbsorbHit(b,dmg,_lastHitX,_lastHitY);weaponHitSfx('normal');return;}
 }return ER23.base.bossHit.apply(this,arguments);
};
function er23Log(event,data={}){ER23.events.push({event,t:efxClock,...data});if(ER23.events.length>400)ER23.events.shift();}
function er23Sonic(q){return !!q&&(q.kind==='sg10pressure'||q.kind==='rzbSonic'||q._ovSonicWave);}
enemyOrdnanceCanIntercept=function(q){return !er23Sonic(q)&&ER23.base.intercept.apply(this,arguments);};

function er23ReaverBudget(b){const M=b?._av3Reaver;if(!M||M.er23Budget===b.maxhp)return;const prior=M.er23Budget;M.er23Budget=b.maxhp;
 const ratios=Object.fromEntries(M.parts.map(p=>[p.id,prior?Math.max(0,p.hp)/p.maxhp:1]));
 const weights={core:.34,wingL:.12,wingR:.12,gunL:.15,gunR:.15,nose:.12};let assigned=0;
 for(const p of M.parts){p.hp=p.maxhp=p.id==='core'?b.maxhp:Math.floor(b.maxhp*weights[p.id]);if(p.id!=='core')assigned+=p.hp;}
 const core=av3Part(b,'core');core.hp=core.maxhp=b.maxhp-assigned;
 for(const p of M.parts)p.hp=p.maxhp*ratios[p.id];b.hp=M.parts.reduce((n,p)=>n+p.hp,0);
 er23Log('reaver-budget',{total:b.maxhp,parts:M.parts.map(p=>({id:p.id,hp:p.hp}))});
}
er26Init=function(b){const r=ER23.base.reaverInit.apply(this,arguments);er23ReaverBudget(b);return r;};
av3ReaverAt=function(b,x,y){const id=ER23.base.reaverAt.apply(this,arguments);if(id!=='core')return id;
 // Open firing corridors to the wings and guns instead of consuming shots on
 // the protected central plate below their actual pixels.
 for(const p of b._av3Reaver.parts)if(p.id!=='core'&&!p.dead){const q=av3PartPoint(b,p),shape=av3PartPose(b,p);
  if(Math.abs(x-q.x)<Math.max(9,shape.w*.28)&&y>q.y)return null;}
 return id;
};
av3ReaverHit=function(b,dmg,x,y,part){
 if(!b?._av3Reaver)return ER23.base.reaverHit.apply(this,arguments);
 er23ReaverBudget(b);if(b.dead||b.enter||b._noHit||!(dmg>0))return;
 const id=part||(Number.isFinite(x)&&Number.isFinite(y)?av3ReaverAt(b,x,y):'core'),p=av3Part(b,id);if(!p||p.dead)return;
 if(id==='core'&&b._av3Reaver.parts.some(q=>q.id!=='core'&&!q.dead)){p.flash=.12;weaponHitSfx('shield');return;}
 const actual=Math.min(dmg,p.hp),oldHP=b.hp;
 // The native hit owner retains elemental damage, sounds, reward and death.
 AV3_R.hit.call(this,actual,x,y);const dealt=Math.min(p.hp,Math.max(0,oldHP-b.hp));
 p.hp-=dealt;p.flash=.16;if(p.hp<=0)av3Break(b,p);
 b.hp=b._av3Reaver.parts.reduce((n,q)=>n+Math.max(0,q.hp),0);
 if(dealt>0)av3Sound('impact_metal',.75,.10);
};
ER23.base.reaverTargets=retinaBossTargets;
retinaBossTargets=function(b){if(!b?._av3Reaver)return ER23.base.reaverTargets.apply(this,arguments);if(b.dead||b.enter||b._noHit)return [];
 er23ReaverBudget(b);const attached=b._av3Reaver.parts.some(p=>p.id!=='core'&&!p.dead);
 return b._av3Reaver.parts.filter(p=>!p.dead&&(!attached||p.id!=='core')).map(p=>{const q=av3PartPose(b,p);return retinaDynamicPiece(b,'reaver-'+p.id,p.id,()=>({...av3PartPoint(b,p),hp:p.hp,dead:b.dead||p.dead}),d=>{const at=av3PartPoint(b,p);av3ReaverHit(b,d,at.x,at.y,p.id);},q.w*.75,q.h*.8);});
};

function er23ModuleLane(b,x,y){
 const parts=(b?._mr27?.parts||[]).filter(p=>!p.dead);
 for(const p of parts){const q=mr27Shape(b,p.id),half=Math.max(12,q.w*.48);
  if(Math.abs(x-q.x)<=half&&y>q.y+q.h*.50&&y<(b._drawY??b.y)+b.h*.55)return true;}
 return false;
}
mr27At=function(b,x,y){const id=ER23.base.at.apply(this,arguments);
 if(id==='core'&&er23ModuleLane(b,x,y))return null;return id;
};
siegeBomberAt=function(b,x,y,pad=0){
 if(!b?._bomber||b.dead||b.enter||!Number.isFinite(x+y))return null;
 const list=siegeBomberParts(b),live=list.filter(q=>q.id!=='core'&&b._bomber.parts.find(p=>p.id===q.id)?.hp>0);
 for(const q of live.slice().reverse())if(Math.abs(x-q.x)<q.w*.5+Math.max(4,pad)&&Math.abs(y-q.y)<q.h*.5+Math.max(4,pad))return q.id;
 // Rear guns sit behind the broad core plate. Rounds travel through these
 // columns until they reach a live physical module; no homing is required.
 for(const q of live)if(Math.abs(x-q.x)<q.w*.5+Math.max(4,pad)&&y>q.y+q.h*.5&&y<b.y+b.h*.6)return null;
 return ER23.base.bomberAt.apply(this,arguments);
};
stage4CoreTurretAt=function(b,x,y,pad=0){
 if(!b?._s4war?.coreUnlocked)return ER23.base.coreAt.apply(this,arguments);
 return b._s4war.coreTurrets.find(t=>!t.dead&&t.materialize>=.92&&Math.abs(x-t.x)<48+pad&&Math.abs(y-t.y)<48+pad)||null;
};
stage4ShieldNodeAt=function(b,x,y,pad=0){
 const H=b?._s4war?.shield;if(!H?.active)return null;
 return H.nodes.find(n=>!n.dead&&Math.abs(x-n.x)<30+pad&&Math.abs(y-n.y)<40+pad)||null;
};
stage4CoreTurretTarget=function(b,side){const q=ER23.base.coreTarget.apply(this,arguments);
 // Both exposed helpers remain inside player movement bounds on wide and
 // narrow screens. They do not follow the hull through its depth manoeuvres.
 if(b?._ship==='stormsovereign'){q.x=clamp(q.x,camLeftX()+65,camRightX()-65);q.y=clamp(q.y,viewTopY()+95,viewTopY()+viewH()*.52);}return q;
};

// A missile reverses the detached tool's orbit; recall time stays independent.
hammerThrowReflect=function(b){const T=b?._hammer?.throw;if(!T?._hf22Origin)return ER23.base.throwReflect.apply(this,arguments);
 if((T.er23ReflectCd||0)>0)return false;T.er23Direction=-(T.er23Direction||1);T.er23ReflectCd=.16;T.hitCd=.12;
 b20Cue('hammerMagnet');er23Log('hammer-direction-reversed',{direction:T.er23Direction});return true;
};
hammerWeaponTargetable=function(b){if(b?._hammer?.throw?._hf22Origin)return b._hammer.throw.phase!=='return';return ER23.base.targetable.apply(this,arguments);};
hammerBoomerangTick=function(b,dt){const T=b?._hammer?.throw;
 if(T&&!T._hf22Origin&&T.phase==='swirl'){T._hf22Origin={x:T.x,y:T.y};T._hf22Age=0;T.er23Orbit=0;T.phase='hf22_orbit';}
 if(!T?._hf22Origin||T.phase!=='hf22_orbit')return ER23.base.throwTick.apply(this,arguments);
 T._hf22Age+=dt;T.t+=dt;T.angle+=dt*20;T.er23ReflectCd=Math.max(0,(T.er23ReflectCd||0)-dt);
 T.er23Orbit=(T.er23Orbit??0)+dt*(T.er23Direction||1);const age=.2+((T.er23Orbit%2.4)+2.4)%2.4;
 const at=hf22Orbit(b,age,T._hf22Origin);T.x=at.x;T.y=at.y;hammerBoomerangHit(T,dt);
 if(T._hf22Age>=4.8){T.phase='return';T.t=0;b20Cue('hammerMagnet');er23Log('hammer-planned-recall');}return true;
};
hf22ThrowWarning=function(){}; // The hammer and authored asterisk own this tell.
hammerState=function(b,s){const r=ER23.base.state.apply(this,arguments);
 if(b?._hammer&&['spin','revenge_charge'].includes(s)&&run.stage===5)ht23Say(b,'Dodge THIS!');return r;
};
hammerBossDamage=function(b,dmg){const h=b?._hammer,q=_dmgBullet;
 if(h?.throw&&b._hammerModuleHit==='hammer'&&!hammerMissile(q))return 0;
 if(h?.state==='ball'&&q&&!(/missile|gmiss|volley/i.test(q.kind||'')||q._manualMissile)){h.er23BallFlash=.16;}
 return ER23.base.damage.apply(this,arguments);
};
window.BOF_ENCOUNTER_REVISION=ER23;
ER23.base.warfareInit=stage4WarfareInit;
stage4WarfareInit=function(b){const r=ER23.base.warfareInit.apply(this,arguments);if(b?._ship==='stormsovereign'&&b._s4war){b._s4war.shieldThresholds=[.50];b._s4war.shieldThresholdIndex=0;}return r;};

// The last-quarter guns still deploy; removing the extra shield gate must not
// remove his final offensive phase.
ER23.base.warfareAfter=stage4WarfareAfterDamage;
stage4WarfareAfterDamage=function(b){const r=ER23.base.warfareAfter.apply(this,arguments),S=b?._s4war;
 if(b?._ship==='stormsovereign'&&S&&!S.mini&&b.hp>0&&b.hp<=b.maxhp*.251&&S.finalGuns==='off'){
  S.finalGuns='deploying';S.finalGunT=0;S.finalGunShot=.30;stage4CoreTurretSpawnMissing(b,.25);stage4WarfareSound('bossWeaponCharge','enemyBossCannon');
 }return r;
};

for(const a of Object.values(ER23_ART.frost)){XART._src[a.key]=a.path;XART._src[a.key+'_hit']=a.path.replace('.webp','_hit.webp');}
ER23.base.frostPlate=pt11Plate;ER23.base.frostTick=mr27Tick;ER23.base.frostFire=mr27Fire;
function er23TurretAngle(p){if(p)p.rot=Math.round(clamp(p.rot||0,-1.2,1.2)/.05)*.05;}
mr27Tick=function(b,dt){const r=ER23.base.frostTick.apply(this,arguments);if(pt11Frost(b))for(const p of b._mr27.parts)er23TurretAngle(p);return r;};
mr27Fire=function(b,slot,a){const r=ER23.base.frostFire.apply(this,arguments);if(pt11Frost(b))for(const p of b._mr27.parts)er23TurretAngle(p);return r;};
pt11Plate=function(name,f,x,y,k=1,rot=0,flash=0,form=null){const a=name==='ice_parts'&&ER23_ART.frost[f];
 if(!a)return ER23.base.frostPlate.apply(this,arguments);const key=a.key+(flash>0?'_hit':'');if(!XART.rdy(key))return false;
 const frame=Math.round((clamp(rot,-1.2,1.2)+1.2)/.05),sx=frame%a.cols*a.w,sy=Math.floor(frame/a.cols)*a.h;
 ctx.drawImage(XART.get(key),sx,sy,a.w,a.h,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.w,a.h);return true;
};

ER23.base.partTick=er26Tick;
er26Tick=function(b,dt){er23ReaverBudget(b);return ER23.base.partTick.apply(this,arguments);};

/* The exposed fortress reactor alternates committed wind/lightning spreads
   and a two-orb pincer. Guns remain independently destructible native objects. */
ER23.base.fortressTick=warhiveTick;ER23.base.fortressDraw=warhiveDraw;
function er23Fortress(b,dt){
 if(!b?._cargo17Mini||b.dead||!sc13Open(b)){if(b?.er23Reactor)delete b.er23Reactor;return;}
 const C=b.er23Reactor||(b.er23Reactor={phase:'ready',t:0,seq:0});C.t+=dt;
 if(C.phase==='ready'&&C.t>.65){const m=sc13Core(b),T=targetShip(m.x,m.y);C.phase='tell';C.t=0;C.seq++;C.origin={x:m.x,y:m.y};C.angle=Math.atan2(T.y-m.y,T.x-m.x);
  C.offsets=C.seq%2?[-.48,-.24,0,.24,.48]:[-.34,.34];C.warm=target17Rank()>=3?.85:1.15;combatAudio0927(b,'bossWeaponCharge',.8);
 }
 if(C.phase==='tell'){
  combatWarningTick(b,'fortress-reactor-'+C.seq,C.t,C.warm);
  if(C.t>=C.warm){const m=sc13Core(b);for(const off of C.offsets){const q=stage4WarfareShot(b,m,C.angle+off,C.seq%2?4.1:2.8,C.seq%2?'lightning':'orb');q._er23Fortress=true;q._weaponProof=true;q._s3kOriginalProof=true;}
   combatAudio0927(b,'enemyBossCannon',.5);C.phase='ready';C.t=0;er23Log('fortress-reactor-volley',{kind:C.seq%2?'wind-lightning':'pincer'});}
 }
}
warhiveTick=function(b,dt){const r=ER23.base.fortressTick.apply(this,arguments);er23Fortress(b,dt);return r;};
warhiveDraw=function(b){const r=ER23.base.fortressDraw.apply(this,arguments),C=b?.er23Reactor;
 if(C?.phase==='tell'&&!b.dead){const m=sc13Core(b);for(const off of C.offsets)combatWarningDraw(b,{x:m.x,y:m.y,ex:m.x+Math.cos(C.angle+off)*VH*1.5,ey:m.y+Math.sin(C.angle+off)*VH*1.5,width:C.seq%2?22:32,progress:C.t/C.warm,fieldOnly:true});}return r;
};

/* Dredger decisions react to observed spacing, then commit. A seeded shuffle
   prevents a fixed five-move loop and never changes an already shown lane. */
ER23.base.dredgerSet=s7mSet;
s7mSet=function(b,mode){const r=ER23.base.dredgerSet.apply(this,arguments);if(b?._s7mod?.tank){b._s4MiniSafe=mode==='er23-surge';}return r;};
ER23.base.dredgerNext=s7mNext;ER23.base.dredgerTick=s7mTick;ER23.base.dredgerDraw=s7mDraw;
function er23Random(M){M.er23Seed=(Math.imul(M.er23Seed??102307,1664525)+1013904223)>>>0;return M.er23Seed/4294967296;}
s7mNext=function(b){const M=b?._s7mod;if(!M?.tank)return ER23.base.dredgerNext.apply(this,arguments);
 if(M.n===2&&!M.od&&b.hp<=b.maxhp*.5)return ER23.base.dredgerNext.apply(this,arguments);
 const near=Math.abs(player.x-b.x)<75,armed=s7mLive(M,'gun').length>0;
 let book=armed?['tank-cross','caustic-lob','tank-mortar','er23-pincer','er23-surge']:['tank-orbits','caustic-lob','tank-mortar','er23-surge'];
 if(near)book.push('er23-surge');if(M.od)book.push('pressure-salvo');book=book.filter(k=>k!==M.er23Previous);
 const next=book[Math.floor(er23Random(M)*book.length)];M.seq++;M.er23Previous=next;s7mSet(b,next);
 if(next.startsWith('er23-')){M.warn=M.n===2?.80:1.05;M.er23Origin={x:b.x,y:b.y};M.er23Aim={x:player.x,y:player.y};M.er23Angle=Math.atan2(player.y-b.y,player.x-b.x);M.er23Pass=0;M.er23Shots=0;M.er23Hit=new Set();}
 er23Log('dredger-choice',{next,near,armed});
};
s7mTick=function(b,dt){const M=b?._s7mod;if(!M?.tank||!M.mode.startsWith('er23-')||b.dead)return ER23.base.dredgerTick.apply(this,arguments);
 M.t+=dt;M.clock+=dt;b.flash=Math.max(0,(b.flash||0)-dt);M.coreFlash=Math.max(0,(M.coreFlash||0)-dt);for(const p of M.parts)p.flash=Math.max(0,p.flash-dt);b._drawY=b.y;
 const surge=M.mode==='er23-surge',active=M.t-M.warn;
 if(active<0){combatWarningTick(b,'dredger-'+M.mode+'-'+M.er23Pass,M.t,M.warn);return true;}
 if(surge){const previous={x:b.x,y:b.y},speed=M.n===2?440:330;
  b.x=clamp(b.x+Math.cos(M.er23Angle)*speed*dt,camLeftX()+90,camRightX()-90);b.y=clamp(b.y+Math.sin(M.er23Angle)*speed*dt,viewTopY()+120,VH-105);
  for(const seat of seatList())withSeat(seat,()=>{if(!M.er23Hit.has(seat)&&!player.dead&&s81003Distance(player.x,player.y,{...previous,ex:b.x,ey:b.y})<65){M.er23Hit.add(seat);playerHit('Caustic Dredger rush');}});
  if(!M.er23DashCue){M.er23DashCue=true;combatAudio0927(b,'jetDash',.5);}
  if(active>.55){M.er23DashCue=false;if(M.n===2&&M.er23Pass++===0){M.t=0;M.warn=.75;M.er23Angle=Math.atan2(player.y-b.y,player.x-b.x);M.er23Hit.clear();}else s7mSet(b,'recover');}
 }else{
  const beat=Math.floor(active/.24);if(beat>M.er23Shots-1&&beat<4){M.er23Shots=beat+1;for(const p of s7mLive(M,'gun')){const q=s7mMuzzle(b,p.id),side=p.id.endsWith('L')?-1:1;
    for(const off of [-.10,.10])s7mShot(b,q.x,q.y,M.er23Angle+side*(.28-beat*.06)+off,3.8+M.n*.25,'acid');}s7mSound('bossfireSludgeemperor');}
  if(active>1.10)s7mSet(b,'recover');
 }return true;
};
s7mDraw=function(b){const r=ER23.base.dredgerDraw.apply(this,arguments),M=b?._s7mod;
 if(M?.mode.startsWith('er23-')&&M.t<M.warn&&!b.dead){if(M.mode==='er23-surge'){const a=M.er23Angle;combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x+Math.cos(a)*250,ey:b.y+Math.sin(a)*250,width:140,progress:M.t/M.warn,fieldOnly:true});}
  else for(const p of s7mLive(M,'gun')){const q=s7mMuzzle(b,p.id),side=p.id.endsWith('L')?-1:1;for(let beat=0;beat<4;beat++)for(const off of [-.10,.10]){const a=M.er23Angle+side*(.28-beat*.06)+off;combatWarningDraw(b,{x:q.x,y:q.y,ex:q.x+Math.cos(a)*VH,ey:q.y+Math.sin(a)*VH,width:20,progress:M.t/M.warn,fieldOnly:true});}}}return r;
};

// Herald's attacks now all follow a predator vocabulary: wing-feather lanes,
// talon pursuit, crossing swoop, then head/eye lances after disarmament.
ER23.base.heraldTell=hd1003Tell;
hd1003Tell=function(b){const H=b._hd1003;if(!H)return ER23.base.heraldTell.apply(this,arguments);
 if(hd19Disarmed(b))return hd19Start(b,H.seq%2?'core-lance':'core-fury');
 const wing=['wingL','wingR'].some(id=>hd1003Live(b,hd1003Part(b,id))),guns=['gunL','gunR'].some(id=>hd1003Live(b,hd1003Part(b,id)));
 const book=['talon-dive','swoop',...(wing?['feathers','wing-rake']:[]),...(guns?['cannon-rake']:[])];
 const kind=book[(H.seq*3+Math.floor(H.clock*7))%book.length];
 if(kind==='wing-rake'||kind==='cannon-rake')return hd19Start(b,kind);
 hp22Start(b,kind);if(target17Rank()>=3&&kind!=='feathers')H._hp22.total=2;
};

/* Charging, idle and stun use fixed whole-actor animation banks. The native
   Chromium wall stays in front of him; its missile counter lane remains open. */
ER23.base.hammerTick=hammerBossTick;ER23.base.hammerDraw=hammerBossDraw;
ER23.base.bluePose=ha21Blue;ER23.base.corruptPose=hb20Pose;ER23.base.wall=hm10WallActive;
ER23.base.head=hammerHeadPoint;ER23.base.committed=hammerStrikeCommitted;
function er23ChargePose(b,kind){const bank=kind+'_charge'+(hf22Red(b)?'_red':kind==='blue'&&fr27Armor(b)?.activated&&fr27Armor(b)?.hp>0?'_armor':''),a=ER23_ART.banks[bank];if(!a||!XART.rdy(a.key))return null;
 const frame=Math.floor(efxClock*14)%8,cell=[(frame%a.cols)*a.w,Math.floor(frame/a.cols)*a.h,a.w,a.h];
 return {a:{key:a.key,white:a.key+'_hit',sheet:a.key,cell,w:a.w,h:a.h,pivot:a.pivot,tip:ER23_ART.chargeTips[kind],glow:ER23_ART.chargeTips[kind],bounds:[0,0,a.w,a.h],_hf22:true,_er23:true,bank,frame},k:1,rot:0,kind:bank};
}
ER23.base.hammerCell=hf22Cell;hf22Cell=function(a,x,y,flash=0){if(a?._er23)return er23DrawBank(a.bank,a.frame,x,y,flash>0);return ER23.base.hammerCell.apply(this,arguments);};
ER23.base.wallDraw=hm10WallDraw;hm10WallDraw=function(b){if(!b.dead&&b?._hammer?.recovery?.status==='charging'&&ER23_ART.banks.shield_wall){const name=hf22Red(b)?'shield_wall_red':'shield_wall';return er23DrawBank(name,Math.floor(efxClock*16)%ER23_ART.banks[name].count,b.x,b.y+10);}return ER23.base.wallDraw.apply(this,arguments);};
ha21Blue=function(b){const h=b?._hammer;if(!h||b.dead||b._gp4Host||b._hammerTime)return ER23.base.bluePose.apply(this,arguments);
 if(h.er23DepthCombo)return hf22PairPose(b,h.er23DepthCombo);
 if(h.recovery?.status==='charging'||['hammer','storm_idle','shield','storm_raise','recharge1002'].includes(h.state)&&!h.hammerDestroyed)return er23ChargePose(b,'blue')||ER23.base.bluePose.apply(this,arguments);
 const q=ER23.base.bluePose.apply(this,arguments);if(h.er23BallFlash>0&&q?.a){const a=HF22_ART.legacyRed[q.a.key];if(a&&XART.rdy(a.key))return {...q,a};}return q;
};
hb20Pose=function(b){if(hb20Own(b)){const A=hb20State(b)?.action;if(['charge','shield'].includes(A?.type))return er23ChargePose(b,'corrupt')||ER23.base.corruptPose.apply(this,arguments);}return ER23.base.corruptPose.apply(this,arguments);};
hm10WallActive=function(b){return !b.dead&&b?._hammer?.recovery?.status==='charging'||ER23.base.wall.apply(this,arguments);};
hammerHeadPoint=function(b){const h=b?._hammer;
 if(h&&!h.throw&&['spin','revenge_charge'].includes(h.state)){const q=ha21Blue(b);if(q?.a?.tip)return hb20World(q.a,q.a.tip,b,1,0);}
 if(h&&!h.throw&&h.recovery?.status==='charging'&&ER23_ART.chargeTips?.blue){const a=ER23_ART.banks.blue_charge,p=ER23_ART.chargeTips.blue;return{x:b.x+p[0]-a.pivot[0],y:b.y+p[1]-a.pivot[1]};}
 // Stage5's original whirlwind already contains both hands and the hammer.
 // Its authored head landmark owns contact; an independent orbit detaches it.
 if(h&&run.stage!==5&&['whirlwind','whirl_turn','fr_twirl'].includes(h.state)){const angle=(h.whirl?.reel||h.t*20);return{x:b.x+Math.cos(angle)*105,y:b.y+Math.sin(angle)*50};}
 return ER23.base.head.apply(this,arguments);
};
hammerStrikeCommitted=function(b){return !!b?._hammer?.er23DepthCombo||ER23.base.committed.apply(this,arguments);};
hammerBossTick=function(b,dt){const h=b?._hammer;if(!h)return ER23.base.hammerTick.apply(this,arguments);h.er23BallFlash=Math.max(0,(h.er23BallFlash||0)-dt);
 if(h.er23DepthCombo&&!b.dead){const P=h.er23DepthCombo;P.clock+=dt;h.t+=dt;hj22PairTick(b,P);
  if(P.clock>=hf22PairDuration(P)){delete h.er23DepthCombo;hammerState(b,'giant_recover');}return;
 }
 const before=h.state,r=ER23.base.hammerTick.apply(this,arguments);
 if(before==='giant_sweep'&&h.state==='giant_recover'&&!b.dead&&!(typeof c25Own==='function'&&c25Own(b))&&['hard','furious'].includes(diffKey)){
  h.er23DepthCombo=hj22Pair(b,'blue',{x:h.tx,y:h.ty});hammerState(b,'er23_depth_combo');er23Log('depth-second-down-and-sweeps',{difficulty:diffKey});
 }
 return r;
};
hammerBossDraw=function(b){const h=b?._hammer;if(!h)return ER23.base.hammerDraw.apply(this,arguments);
 if(!b.dead&&h.state==='ball'&&h.er23BallFlash>0&&ER23_ART.banks.ball_flash){hammerBossAtmosphereDraw(b);hf22Aura(b);er23DrawBank('ball_flash',((Math.round((h.angle||0)/TAU*24)%24)+24)%24,b.x,b.y);return;}
 if((b.dead||['hammer_stun','storm_stun','fr_stun'].includes(h.state))&&ER23_ART.banks.stun){
  hammerBossAtmosphereDraw(b);er23DrawBank(hf22Red(b)?'stun_red':'stun',Math.floor((b.dead?(b.dying||0):h.t)*12)%8,b.x,b.y,b.flash>0);hammerStunEffectsDraw(b);hammerRecoveryBurstDraw(b);return;
 }
 const r=ER23.base.hammerDraw.apply(this,arguments);
 // HA21 paints the wall once, after its whole actor.
 if(h.er23DepthCombo)hj22PairDraw(b,h.er23DepthCombo);
 if(!b.dead&&['spin','revenge_charge'].includes(h.state)){
  const at=hammerHeadPoint(b);hj22Light('blue',at);combatWarningDraw(b,{x:b.x,y:b.y-120,ex:b.x,ey:b.y,progress:clamp(h.t/(h.state==='spin'?HAMMER_SPIN_TIME:2),0,1),alertOnly:true,alertX:b.x,alertY:b.y-120});
 }
 // Keep the held hammer inside the whole Stage5 plate, including HAMA. Only a
 // deliberate throw/counter release may invoke the detached-weapon owner.
 if(!b.dead&&run.stage!==5&&!(typeof c25Own==='function'&&c25Own(b))&&['whirlwind','whirl_turn','fr_twirl'].includes(h.state)){const at=hammerHeadPoint(b);hf22Tool(b,at,h.whirl?.reel||h.t*20);}
 return r;
};
ER23.base.spinDraw=hammerBoomerangSpinDraw;
hammerBoomerangSpinDraw=function(b){if(run.stage===5&&!b._hammerTime)return;return ER23.base.spinDraw.apply(this,arguments);};
ER23.base.corruptField=b20Field;ER23.base.corruptStart=hb20Start;
b20Field=function(){const A=hb20Own(boss)&&hb20State(boss)?.action;if(A?.type==='throw')return;return ER23.base.corruptField.apply(this,arguments);};
hb20Start=function(b,type){const A=ER23.base.corruptStart.apply(this,arguments);if(A?.type==='throw'){A.duration=A.tell+5.35;A.er23Direction=1;A.er23Orbit=0;A.er23LastAge=0;}return A;};
ER23.base.corruptTool=hb20ToolAt;ER23.base.corruptDamage=modularHit;
hb20ToolAt=function(b,A){if(!hb20Own(b)||A?.type!=='throw')return ER23.base.corruptTool.apply(this,arguments);
 const age=Math.max(0,A.t-A.tell),source=hf22Row('corrupt_throw',4),origin=hb20World(source,source.tip,A.origin,1,0);
 const delta=Math.max(0,age-(A.er23LastAge||0));A.er23LastAge=age;A.er23Orbit=(A.er23Orbit||0)+delta*(A.er23Direction||1);
 if(age<4.8)return hf22Orbit(b,.2+((A.er23Orbit%2.4)+2.4)%2.4,origin);
 const from=hf22Orbit(b,.2+((A.er23Orbit%2.4)+2.4)%2.4,origin),ready=hf22Row('corrupt_throw',0),to=hb20World(ready,ready.tip,b,1,0),u=clamp((age-4.8)/.55,0,1);return{x:lerp(from.x,to.x,u),y:lerp(from.y,to.y,u)};
};
modularHit=function(dmg){const b=boss,A=hb20Own(b)&&hb20State(b)?.action;
 if(A?.type==='throw'&&A.t>A.tell&&b._lastPart?.id==='hammer'){
  if(hammerMissile(_dmgBullet)&&(A.er23HitAt==null||A.t-A.er23HitAt>.16)){A.er23HitAt=A.t;A.er23Direction=-(A.er23Direction||1);b20Cue('hammerMagnet');}return;
 }return ER23.base.corruptDamage.apply(this,arguments);
};
