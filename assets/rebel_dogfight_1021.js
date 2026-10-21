"use strict";
/* Personal dogfight books and squad manoeuvres. Native combat, audio, hit/death
   and Retina owners remain authoritative. All trajectories have committed FOVs. */
const RD21={base:{init:rg4Init,tick:rebelSquadTick,attack:rg4Attack,act:rg4AttackTick,ramHit:ra4RamHit,
 gun:ra4Gun,warning:rg4Warning,ship:fr27RebelDrawShip,damage:rebelSquadDamage,
 targets:retinaBossTargets,clear:rg4Clear,heavy:rbal19Heavy,helix:ra4Helix,nova:ra4Nova,ordDraw:rg4OrdnanceDraw,wingNavigate:s6WingNavigate},events:[],draws:0};
const rd21Rank=()=>diffKey==='easy'?0:diffKey==='normal'?1:diffKey==='hard'?2:3;
const rd21Log=(event,data={})=>{RD21.events.push({event,time:rg4State()?.age||0,...data});if(RD21.events.length>250)RD21.events.shift();};
const rd21Live=q=>q&&!q.dead&&q.hp>0;
function rd21State(b){const G=b?._rebels?.gang1004;if(!G)return null;
 if(!G.rd21){G.rd21={next:9,cycle:0,fleet:null};for(const q of b._rebels.ships){if(!q._rd21Pool&&rd21Live(q)){q._rd21Pool=true;const old=q.hp;q.max=Math.max(1,Math.round(q.max*.92));q.hp=Math.min(q.hp,q.max);b.hp=Math.max(0,b.hp-old+q.hp);}q._rd21Scale=1;q._rd21Cloak=q.key==='nyx';}
  b.maxhp=b._rebels.ships.filter(q=>!q.dead).reduce((a,q)=>a+q.max,0);rd21Log('squad-book-ready');}
 return G.rd21;
}
rg4Init=function(b){const G=RD21.base.init.apply(this,arguments);rd21State(b);return G;};
function rd21Personal(q,R,G,kind){const p=ra4Target(q,q.rg4.serial++),ref=p.ref,warm=[1.8,1.5,1.3,1.15][rd21Rank()];
 q.rg4.armed=null;q.rg4.n++;q.rg4._rbal19Gun=null;q.evadeT=0;
 const A=q.rg4.act={kind,_rd21:true,phase:'charge',t:0,warm,target:p,tx:ref.x,ty:ref.y,
  a:Math.atan2(ref.y-q.y-30,ref.x-q.x),shot:0,cd:0,ox:q.x,oy:q.y,hit:new Set()};
 G.releaseAt=Math.max(G.releaseAt,G.age+warm+.8);combatWarningTick(A,'rd21-'+q.rg4.n,0,warm);
 (Audio.SFX.bossWeaponCharge||Audio.SFX.retinaCharge)?.();rd21Log('personal-charge',{pilot:q.key,kind,warm});return A;
}
rg4Attack=function(q,R,G,forced){if(rd21State(boss)?.fleet||q.key==='nyx'&&q._rd21Cloak){q.rg4.cd=.8;return;}
 const kind=forced||q.rg4.armed;
 if(R.ships.some(s=>s!==q&&rd21Live(s)&&s.rg4?.act?.phase!=='recover'&&['rookhook','depthram','swervehelix'].includes(s.rg4?.act?.kind))){q.rg4.cd=.6;return;}
 if(['rockets','windspread','turbo','helix','cloak'].includes(kind)&&R.ships.some(s=>s!==q&&rbal19Heavy(s))){q.rg4.cd=.6;return;}
 if(q.key==='kaia'&&(kind==='rockets'||kind==='windspread'))return rd21Personal(q,R,G,'windspread');
 if(q.key==='voss'&&kind==='turbo')return rd21Personal(q,R,G,'depthram');
 if(q.key==='jace'&&kind==='helix')return rd21Personal(q,R,G,'swervehelix');
 if(q.key==='nyx'&&kind==='cloak')return rd21Personal(q,R,G,'shadowcast');
 return RD21.base.attack.apply(this,arguments);
};
function rd21Finish(q,G,cd=5){q.rg4.act=null;q.rg4.cd=cd;q.rg4.gunCd=Math.max(q.rg4.gunCd||0,1);q.rfHeading=null;q._rd21Scale=1;
 if(q.key==='nyx'){q._rd21Cloak=true;q.frCloak=10;}rd21Log('personal-recovery',{pilot:q.key});}
function rd21Round(q,A,off,shadow=false){const a=A.a+off,z=rg4Round(q,a,[2.5,2.8,3,3.2][rd21Rank()], 's6orb',
 {_rd21Wind:!shadow,_rd21Shadow:shadow,owner:q,w:shadow?24:18,h:shadow?24:24});
 wm26Emit?.(q,z.x,z.y,a,'mg',null,{size:shadow?25:20,life:.10});return z;}
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act;if(!A?._rd21)return RD21.base.act.apply(this,arguments);
 dt=Math.min(.05,dt);A.t+=dt;
 if(A.phase==='charge'){
  if(A.t<A.warm*.6){const p=A.target.ref;A.tx=p.x;A.ty=p.y;A.a=Math.atan2(p.y-q.y-30,p.x-q.x);}
  combatWarningTick(A,'rd21-'+q.rg4.n,Math.min(A.t,A.warm),A.warm);
  if(A.kind==='depthram')q._rd21Scale=lerp(1,.30,clamp(A.t/(A.warm*.68),0,1));
  if(A.kind==='swervehelix'){q.x=clamp(A.ox+Math.sin(A.t*3.3)*32,camLeftX()+65,camRightX()-65);q.rfHeading=Math.PI/2+Math.cos(A.t*3.3)*.20;}
  if(A.t<A.warm)return;
  A.phase='fire';A.t=0;A.cd=0;A.fx=0;A.fy=0;A.start={x:q.x,y:q.y};
  if(A.kind==='depthram'){A.end={x:clamp(A.tx,camLeftX()+35,camRightX()-35),y:clamp(A.ty+95,PLAY.y+80,VH+90)};Audio.SFX.chargeDash?.();}
  if(A.kind==='swervehelix'){A.end={x:clamp(A.tx,camLeftX()+65,camRightX()-65),y:clamp(A.ty-100,PLAY.y+105,VH*.64)};}
  rd21Log('personal-release',{pilot:q.key,kind:A.kind});
 }
 if(A.phase==='fire'){
  if(A.kind==='windspread'||A.kind==='shadowcast'){
   if(A.cd<=0){const shadow=A.kind==='shadowcast',offsets=shadow?[-.20,0,.20]:[-.36,-.18,0,.18,.36];for(const off of offsets)rd21Round(q,A,off,shadow);
    b20Cue(shadow?'shadowRelease':'enemyGun');A.shot++;A.cd=.65;
    if(A.shot>=[1,2,2,3][rd21Rank()]){A.phase='recover';A.t=0;}else{A.phase='charge';A.t=0;A.warm=[1.05,.95,.85,.78][rd21Rank()];}}
   A.cd-=dt;
  }else if(A.kind==='depthram'){
   const duration=[1.05,.95,.85,.78][rd21Rank()],u=clamp(A.t/duration,0,1),ease=u*u;
   q.x=lerp(A.start.x,A.end.x,ease);q.y=lerp(A.start.y,A.end.y,ease);q._rd21Scale=lerp(.30,1.45,u);q.rfHeading=Math.PI/2;
   if(q._rd21Scale>.8)ra4RamHit(q,A);ra4TurboTrace(q,A,q._rd21Scale);
   if(u>=1){A.phase='recover';A.t=0;A.back={x:q.x,y:q.y};}
  }else if(A.kind==='swervehelix'){
   const u=clamp(A.t/.8,0,1);q.x=lerp(A.start.x,A.end.x,u)+Math.sin(u*Math.PI)*24;q.y=lerp(A.start.y,A.end.y,u);
   q.rfHeading=Math.PI/2+Math.sin(u*TAU)*.20;
   if(A.t>=.62&&!A.released){A.released=true;A.a=Math.atan2(A.ty-q.y-32,A.tx-q.x);ra4Helix(q,G,A);}
   if(A.t>=1.15){A.phase='recover';A.t=0;}
  }
 }else if(A.phase==='recover'){
  if(A.kind==='depthram'){const u=clamp(A.t/1.25,0,1),x=camLeftX()+viewW()*(q.i%2?.76:.24),y=PLAY.y+90;
   q.x=lerp(A.back.x,x,u);q.y=lerp(A.back.y,y,u);q._rd21Scale=lerp(1.45,1,u);q.rfHeading=-Math.PI/2;}
  if(A.t>1.3)rd21Finish(q,G,A.kind==='depthram'?8:5.5);
 }
};
function rd21Reveal(q,reason){if(!q._rd21Cloak||q.dead)return false;q._rd21Cloak=false;q.frCloak=0;q._ra7Reveal=.55;q._rd21Visible=7;
 q.rg4.act=null;q.rg4.armed='cloak';q.rg4.cd=.8;av3Sound('teleport_in',.8);rd21Log('nyx-revealed',{reason});return true;}
function rd21NyxLock(b,q){let locked=false;for(const seat of seatList())withSeat(seat,()=>{
 const match=t=>t?._retinaOwner===b&&String(t._retinaId).startsWith('nyx');
 if(retina.phase==='locked'&&match(retina.target))locked=true;
 if(player._retinaScan?.marks.some(m=>m.phase==='locked'&&match(m.target)))locked=true;
 });if(locked)rd21Reveal(q,'retina');}
rebelSquadDamage=function(b,dmg){const q=b?._rebels?.ships[b._rebels.hit],shot=typeof _dmgBullet==='undefined'?null:_dmgBullet;
 if(q?.key==='nyx'&&dmg>0&&((typeof _dmgSrc!=='undefined'&&_dmgSrc==='missile')||shot&&(shot.kind==='missile'||shot.kind==='bomb'||shot._retinaLaunch||shot._missile||shot._missileVariant)))rd21Reveal(q,'missile');
 return RD21.base.damage.apply(this,arguments);};
retinaBossTargets=function(b){const targets=RD21.base.targets.apply(this,arguments),q=b?._rebels?.ships.find(q=>q.key==='nyx'&&rd21Live(q));
 if(!q||!q._rd21Cloak||!b._rebels.frIntro?.done||b._rebels.gang1004?.scene)return targets;
 if(!targets.some(t=>String(t._retinaId).startsWith('nyx')))targets.push(retinaDynamicPiece(b,'nyx','rival',()=>({x:q.x,y:q.y,hp:q.hp,dead:q.dead}),d=>{b._rebels.hit=q.i;hitBoss(d);},92,92));return targets;};
const RD21_PINS={star:[[0,-1],[.95,-.31],[.59,.81],[-.59,.81],[-.95,-.31]],bowling:[[0,-1],[-.5,0],[.5,0],[-1,1],[1,1]],H:[[-1,-1],[-1,1],[0,0],[1,-1],[1,1]],X:[[-1,-1],[1,-1],[0,0],[-1,1],[1,1]]};
function rd21FleetStart(b,G,D){const R=b._rebels,name=['star','bowling','H','X'][D.cycle++%4];
 D.fleet={name,phase:'assemble',t:0,shots:false};G.rebelBoxes=[];
 for(const q of R.ships){if(!rd21Live(q))continue;q.rg4.act=null;q.rg4.supply=null;q.rg4._rbal19Gun=null;q._rd21From={x:q.x,y:q.y};q.evadeT=0;}
 rd21Log('formation',{name});}
function rd21Fleet(b,G,D,dt){const F=D.fleet;if(!F)return;F.t+=dt;const R=b._rebels,live=R.ships.filter(rd21Live);G.releaseAt=G.age+2;
 const cx=camLeftX()+viewW()/2,sx=Math.min(115,viewW()*.30),cy=PLAY.y+viewH()*.29,sy=Math.min(65,viewH()*.11),pins=RD21_PINS[F.name];
 for(const q of live){const pin=pins[q.i%5],home={x:cx+pin[0]*sx,y:cy+pin[1]*sy};
  if(F.phase==='assemble'){const u=clamp(F.t/1.8,0,1),v=u*u*(3-2*u);q.x=lerp(q._rd21From.x,home.x,v);q.y=lerp(q._rd21From.y,home.y,v);q.rfHeading=Math.PI/2+(home.x-q._rd21From.x)*.001*(1-u);}
  else if(F.phase==='tell'){q.x=home.x;q.y=home.y;q.rfHeading=Math.PI/2;const A=q._rd21Volley;A.t=F.t;combatWarningTick(A,'rd21-fleet-'+D.cycle,Math.min(A.t,A.warm),A.warm);}
  else if(F.phase==='scatter'){const u=clamp(F.t/2.0,0,1),side=q.i%2?1:-1;q.x=lerp(home.x,cx+side*(viewW()*.52+60),u);q.y=lerp(home.y,VH+135+q.i*12,u);q.rfHeading=Math.atan2(VH+150-home.y,side*(viewW()*.52+60));}
  else if(F.phase==='return'){const u=clamp(F.t/2.0,0,1),v=u*u*(3-2*u);q.x=lerp(cx+(q.i-2)*42,home.x,v);q.y=lerp(VH+110,home.y,v);q._rd21Scale=lerp(.36,1,u);q.rfHeading=lerp(-Math.PI/2,Math.PI/2,clamp((u-.72)/.28,0,1));}
 }
 if(F.phase==='assemble'&&F.t>=1.8){F.phase='tell';F.t=0;const warm=[1.8,1.5,1.3,1.15][rd21Rank()];for(const q of live){const target=ra4Target(q,D.cycle);q._rd21Volley={t:0,warm,locked:true,target,a:Math.atan2(target.ref.y-q.y,target.ref.x-q.x),shot:0};}Audio.SFX.retinaCharge?.();}
 else if(F.phase==='tell'&&F.t>=[1.8,1.5,1.3,1.15][rd21Rank()]){for(const q of live){const A=q._rd21Volley;for(let i=0;i<2;i++){ra4Rocket(q,G,A);A.shot++;}q._rd21Volley=null;}F.phase='hold';F.t=0;rd21Log('formation-volley',{name:F.name,missiles:live.length*2});}
 else if(F.phase==='hold'&&F.t>=1.1){F.phase='scatter';F.t=0;}
 else if(F.phase==='scatter'&&F.t>=2){F.phase='return';F.t=0;rd21Log('south-return',{name:F.name});}
 else if(F.phase==='return'&&F.t>=2){for(const q of live){q._rd21Scale=1;q.rfHeading=null;q.rg4.gunCd=1;q.rg4.cd=Math.max(1.6,q.rg4.cd);}D.fleet=null;D.next=G.age+[15,13,12,11][rd21Rank()];}
}
ra4Gun=function(q,G,dt){if(rd21State(boss)?.fleet||q._rd21Cloak||q._rd21Scale<.8)return;return RD21.base.gun.apply(this,arguments);};
rebelSquadTick=function(b,dt){const G=b?._rebels?.gang1004,D=rd21State(b);if(G&&D?.fleet&&!G.scene)G.releaseAt=G.age+2;
 const r=RD21.base.tick.apply(this,arguments);if(!G||!D||b.dead||G.scene||!b._rebels.frIntro?.done)return r;
 const live=b._rebels.ships.filter(rd21Live);for(const q of live){if(q.key==='nyx'){rd21NyxLock(b,q);if(q._rd21Cloak){q.frCloak=10;q.rg4._rbal19Gun=null;}else{q.frCloak=0;q._rd21Visible=Math.max(0,(q._rd21Visible||0)-dt);if(!q._rd21Visible&&!q.rg4.act)q._rd21Cloak=true;}}
  if(!D.fleet&&!q.rg4.act&&!q.evadeT)q.rfHeading=Math.PI/2+Math.sin(G.age*1.9+q.i)*.16;}
 if(!D.fleet&&G.age>=D.next&&live.length>=2&&!live.some(q=>q.rg4.act&&q.rg4.act.phase!=='recover'))rd21FleetStart(b,G,D);
 rd21Fleet(b,G,D,Math.min(.05,dt));return r;};
function rd21Fov(owner,x,y,a,w,p){combatWarningDraw(owner,{x,y,ex:x+Math.cos(a)*1000,ey:y+Math.sin(a)*1000,width:w,progress:p,fieldOnly:true,laneShape:'line'});}
rg4Warning=function(q,A){if(RD21.painting)return;if(A?.kind==='slug'&&A.phase==='charge'){rd21Fov(A,q.x,q.y+32,A.a,2*(23+Math.hypot(viewW(),viewH())*.06),A.t/A.warm);return;}if(!A?._rd21)return RD21.base.warning.apply(this,arguments);if(A.phase!=='charge')return;
 const p=A.t/A.warm,offsets=A.kind==='windspread'?[-.36,-.18,0,.18,.36]:A.kind==='shadowcast'?[-.2,0,.2]:[0];
 for(const off of offsets)rd21Fov(A,q.x,q.y+32,A.a+off,A.kind==='depthram'?82:A.kind==='swervehelix'?110:A.kind==='shadowcast'?28:20,p);
 if(A.kind==='windspread'||A.kind==='shadowcast')ra4LockWarning({...A,locked:true},q.key);
};
fr27RebelDrawShip=function(q){const scale=q._rd21Scale||1,scaled=scale!==1,A=q.rg4?.act,T=q.rg4?._rbal19Gun;ctx.save();if(scaled){drawUnitShadow(q.x,q.y,90*scale,90*scale,.24,q);ctx.translate(q.x,q.y);ctx.scale(scale,scale);ctx.translate(-q.x,-q.y);}
 try{RD21.painting=true;RD21.base.ship.apply(this,arguments);
  if(A?.kind==='depthram'&&Math.floor((q.t||0)*12)%2===0){const p=air13Pose(q.key,'heading',Math.PI/2);if(p)air13Blit(p,q.x,q.y,SHIP_DRAW_H*1.5*p.d.referenceRatio,.32,'#ffffff');}
 }finally{RD21.painting=false;ctx.restore();}
 if(q.dead)return;ctx.save();try{
  if(T){const a=Math.atan2(T.ty-q.y-28,T.tx-q.x-T.side*18);rd21Fov(T,q.x+T.side*18,q.y+28,a,12,T.t/T.warm);}
  if(A)rg4Warning(q,A);
  if(q._rd21Volley){const V=q._rd21Volley;for(const side of [-1,1])rd21Fov(V,q.x+side*27,q.y+42,V.a,22,V.t/V.warm);ra4LockWarning(V,q.key);}
  if(A?.kind==='swervehelix'&&(A.phase==='charge'||A.phase==='fire'&&!A.released))ra4Blit(ra4Palette('nhxsb_g_2')||ra4Palette('nhxsb_g_1'),q.x,q.y+42,45,45,(q.t||0)*5);
  RD21.draws++;
 }finally{ctx.restore();}};
rg4Clear=function(G){const r=RD21.base.clear.apply(this,arguments);if(G?.rd21)G.rd21.fleet=null;for(const q of boss?._rebels?.ships||[]){q._rd21Volley=null;q._rd21Scale=1;}return r;};
globalThis.BOF_REBEL_DOGFIGHT={state:RD21,formation:rd21FleetStart,reveal:rd21Reveal};
rbal19Heavy=function(q){const A=q?.rg4?.act;return !!(rd21Live(q)&&A?._rd21&&A.phase!=='recover')||RD21.base.heavy.apply(this,arguments);};
ra4Helix=function(q,G,A){const n=G.ord.length,r=RD21.base.helix.apply(this,arguments);for(const o of G.ord.slice(n))if(q.key==='jace')o._rd21Nova=true;return r;};
ra4Nova=function(G,o){if(o._rd21Nova&&o.t<.85)return;return RD21.base.nova.apply(this,arguments);};
rg4OrdnanceDraw=function(o,G){const r=RD21.base.ordDraw.apply(this,arguments);if(o._rd21Nova&&!o.dead){for(let i=0;i<8;i++)rd21Fov(o,o.x,o.y,i*TAU/8,16,clamp(o.t/.85,0,1));}return r;};
// Rook shares the authored charge/ram impact vocabulary with Juggernaut.
// Bursts follow phase changes and real contacts, never ambient particle spam.
const rd21RamTick=rg4AttackTick;
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act,ram=q.key==='rook'&&A?.kind==='ram';
 if(ram&&!A._rd21RamWarm){A._rd21RamWarm=true;weaponFeedbackWarm('juggernaut');b20Cue('juggernautChargeStart');}
 const phase=A?.phase,r=rd21RamTick.apply(this,arguments);
 if(ram&&A.phase!==phase){if(A.phase==='fire'){weaponFeedbackBurst('ram',q.x,q.y,96,.28,A.a);b20Cue('juggernautRamLaunch');}
  else if(A.phase==='recover'){weaponFeedbackBurst('ram',q.x,q.y,80,.25,A.a);b20Cue('juggernautRamStop');}}
 return r;};
ra4RamHit=function(q,A){const before=A.hit.size,r=RD21.base.ramHit.apply(this,arguments);if(q.key==='rook'&&A.hit.size>before){weaponFeedbackBurst('ram',q.x,q.y,108,.32,A.a);b20Cue('juggernautRamImpact');}return r;};
// Allies deliberately cover incoming Rebel missiles through their ordinary
// gun/missile arsenal. The shared projectile collision owner resolves the hit.
s6WingNavigate=function(q,W,dt){const supply=RD21.base.wingNavigate.apply(this,arguments),G=rg4State();q._rd21Intercept=null;
 if(supply||!G?.rd21||G.scene||q.phase!=='fight'||q.dodgeT>0)return supply;
 const candidates=eBullets.filter(m=>m._ra4Rocket&&!m.dead&&m._shootable&&m.hp>0&&m.y>PLAY.y+20&&m.y<q.y-40&&Math.abs(m.x-q.x)<180);
 const score=m=>Math.hypot(m.x-q.x,m.y-q.y)+W.ships.filter(a=>a!==q&&a._rd21Intercept===m).length*150;
 candidates.sort((a,b)=>score(a)-score(b));const m=candidates[0];if(m){q.target=m;q._rd21Intercept=m;q.gx=clamp(m.x,camLeftX()+34,camRightX()-34);q.gy=Math.max(q.gy||q.y,q.y);}
 return supply;};
