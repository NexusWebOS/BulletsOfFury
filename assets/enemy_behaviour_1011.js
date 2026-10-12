"use strict";
/* Regular enemies: establish a visible attack, commit, recover, then reposition.
   Native controllers retain their weapons, mounts, routes and damage pools. */
const EB11={clock:0,nextTell:0,serial:0,
 base:{begin:ai27Begin,end:ai27End,play:updatePlay,stage:beginStage,draw:drawEnemy,mega:s8MegaTick,navalGate:navalInSix,maneuver:jetManeuverTick},
 profiles:{
  easy:   {rate:1,   cooldown:1,   tell:.78,recovery:.40,slots:1,spacing:.30,cycles:2},
  normal: {rate:1,   cooldown:1,   tell:.62,recovery:.34,slots:2,spacing:.23,cycles:2},
  hard:   {rate:1.10,cooldown:.90,tell:.54,recovery:.30,slots:2,spacing:.18,cycles:3},
  furious:{rate:1.42,cooldown:.70,tell:.46,recovery:.26,slots:3,spacing:.12,cycles:5},
  insanity:{rate:1.58,cooldown:.62,tell:.44,recovery:.25,slots:3,spacing:.10,cycles:6}
 },
 queueKeys:['_s2Act','_s3Act','_s4Act','_s5Act','_s6Act','_s7Act','_s9Act'],
 aimed:new Set(['s6lancer','s6dart','s7lamprey','s7pipe','s7sampler','s7serpent','s9interceptor']),
 // Only narrow gun salvos repeat. Mine rings, spawners and heavy explosives do not.
 double:new Set(['cruc','s3fighter','s4interceptor','s5frigate','s5interceptor','s5skimmer',
  's6lancer','s6dart','s6skimmer','s7pipe','s7skimmer','s9interceptor','s9comet']),
 station:new Set(['cruc','pod','s3crystal','s4command','s5frigate','s5gravity','s5station','s5satellite',
  's5minelayer','s5portalmine','s6lancer','s6mine','s6buoy','s6probe','s6thunder','s6turbine',
  's7barge','s7mine','s9beacon','s9ring','s9gunship','s9prism','s9gateturret','s9singularity'])};
function eb11Profile(){return EB11.profiles[diffKey]||EB11.profiles.normal;}
function eb11RamSpeed(){return diffKey==='easy'?.85:diffKey==='hard'?1.12:diffKey==='furious'?1.32:diffKey==='insanity'?1.42:1;}
function eb11Owns(e){return ai27Owns(e)&&!e._amini&&!e._mini&&!e.boss&&!e._boss;}
function eb11Queue(e){for(const key of EB11.queueKeys)if(e[key])return e[key];return null;}
// These controllers already own an exit, ram, scroll anchor or finite engagement.
// The legacy age-based downward push must not displace their firing pockets.
function eb11OwnsRoute(e){return !!(e._volc||e._s3ice||e._s4chase||e._s5space||e._s6storm||e._s7toxic||e._s8mega||e._s9void||e._af10Jet);}
function eb11Ready(e){
 if(!e||e.dead||e._dyingT!=null||e._shieldStun>0||e._stagger>0||e._mercuryLock>0||e._frozen)return false;
 const A=e._ai27,p=targetShip(e.x,e.y),pad=Math.max(66,Math.max(e.w||24,e.h||24)*.48+22);
 return !!(p&&!p.dead&&!p.out&&A?.visible&&A.seen>=.50&&A.flinch<=0&&Math.hypot(p.x-e.x,p.y-e.y)>=pad);
}
function eb11Target(e){const p=targetShip(e.x,e.y);return {x:p.x,y:p.y};}
function eb11Release(e,q){
 const aim=aimPlayer,lock=q._eb11.target;
 // P2's space-salvo closure reads this field before installing its own aim helper.
 q._p2Aim={...lock};aimPlayer=(x,y)=>Math.atan2(lock.y-y,lock.x-x);
 try{(q.release||q.fn)();}finally{aimPlayer=aim;}
 q._eb11.releases++;e._eb11.attacks++;
}
function eb11QueueTick(e,key,dt){
 const q=e[key];if(!q)return;
 const P=eb11Profile(),tag=key.replace('Act','AtkT'),durKey=key.replace('Act','AtkDur');
 // Cyclone's empty action is a flight animation clock; its ram controller
 // owns the tell/impact. It must never wait for a gun scheduler slot.
 if(e._s6storm==='s6cyclone'){
  q.t+=dt;e[tag]=q.t;if(!q.fired&&q.t>=q.at){q.fired=true;(q.release||q.fn)();}
  if(q.t>=q.dur){e[key]=null;e[tag]=null;}return;
 }
 const E=e._eb11||(e._eb11={attacks:0,age:0});
 if(!q._eb11){
  const tail=Math.max(P.recovery,(q.dur||.7)-(q.at||.3));
  q.at=Math.max(P.tell,(q.at||.3)*(diffKey==='hard'?.94:diffKey==='furious'?.86:1));
  const repeat=(diffKey==='furious'||diffKey==='insanity')&&EB11.double.has(e.type)&&(E.cycles||0)%2===(EB11.station.has(e.type)?1:0);
  q.dur=q.at+(repeat?.22:0)+tail;q.t=0;
  q._eb11={id:++EB11.serial,started:false,target:null,releases:0,repeat};
  e._fcd=Math.max(P.recovery,(e._fcd||1)*P.cooldown);e[durKey]=q.dur;
 }
 const Q=q._eb11;
 if(e.dead||e._dyingT!=null){e[key]=null;e[tag]=null;return;}
 if(!Q.started){
  if(!eb11Ready(e))return;
  const busy=enemies.filter(o=>o!==e&&!o.dead&&o._dyingT==null&&eb11Queue(o)?._eb11?.started&&!eb11Queue(o).fired).length;
  if(busy>=P.slots||EB11.clock<EB11.nextTell)return;
  Q.started=true;Q.target=eb11Target(e);EB11.nextTell=EB11.clock+P.spacing;
 }
 // A stun or camera departure does not silently consume a queued attack.
 // Re-entering starts a new full tell and locks a new target.
 if(!q.fired&&!eb11Ready(e)){
  q.t=0;Q.started=false;Q.target=null;e[tag]=0;return;
 }
 q.t+=dt;e[tag]=q.t;
 if(!q.fired){
  combatWarningTick(e,'field1011-'+Q.id,q.t,q.at);
  if(q.t>=q.at){eb11Release(e,q);q.fired=true;}
 }else if(Q.repeat&&Q.releases===1&&q.t>=q.at+.22){
  if(eb11Ready(e))eb11Release(e,q);else Q.repeat=false;
 }
 if(q.t>=q.dur){
  e[key]=null;e[tag]=null;E.cycles=(E.cycles||0)+1;
  // A held enemy has an engagement and a departure, not an endless sine loop.
  if(EB11.station.has(e.type)&&E.cycles>=(diffKey==='hard'?4:Math.max(3,P.cycles)))E.leave=true;
  if(e._ap10Flight)e._ap10Flight.x=clamp(e._ap10Flight.x+(E.cycles%2?48:-48),camLeftX()+e.w*.7,camRightX()-e.w*.7);
 }
}
ai27Begin=function(e,dt){
 const previous=EB11.base.begin.apply(this,arguments);if(!eb11Owns(e))return previous;
 const A=e._eb11||(e._eb11={attacks:0,age:0});A.age+=dt;
 if(eb11Ready(e)){
  const extra=dt*(eb11Profile().rate-1);
  // Native queued fleets already divide _fcd by DIFF.eFire. Their extra step is
  // applied once per attack above; generic/ship/arsenal cooldowns use this path.
  for(const key of ['fireCd','_volCd','_burstCd'])if(Number.isFinite(e[key])&&e[key]>0)e[key]=Math.max(0,e[key]-extra);
  if((e.pattern==='naval'||e.pattern==='s1tank')&&!(e._burst>0)){
   for(const key of ['_shotCd','_idle'])if(e[key]>0)e[key]=Math.max(0,e[key]-extra);
  }
  if(e._modTurret?.mode==='wait')e._modTurret.timer-=extra;
  if(e._dr?.phase==='idle')e._dr.cd-=extra;
 }
 return previous;
};
function eb11NativeController(base){return function(e,dt){
 if(!eb11Owns(e))return base.apply(this,arguments);
 const E=e._eb11||(e._eb11={attacks:0,age:0});
 // A station abandoned outside the camera still has a bounded lifetime.
 if(EB11.station.has(e.type)&&E.age>30&&!eb11Queue(e)?._eb11?.started)E.leave=true;
 if(E.leave){
  e.y+=125*dt;e.spin=e._bank=0;
  if(e.y>VH+Math.max(100,e.h))e.dead=true;return;
 }
 const x=e.x,y=e.y,r=base.apply(this,arguments),q=eb11Queue(e);
 // Fast crossing craft need enough on-screen runway to show their tell. They
 // bank/decelerate through it, then resume their original crossing route.
 if(q?._eb11&&!q.fired&&e._ai27?.visible){e.x=x+(e.x-x)*.25;e.y=y+(e.y-y)*.38;}
 return r;
};}
volcTick=eb11NativeController(volcTick);s3IceTick=eb11NativeController(s3IceTick);
s4ChaseTick=eb11NativeController(s4ChaseTick);s5SpaceTick=eb11NativeController(s5SpaceTick);
s6StormTick=eb11NativeController(s6StormTick);s7ToxicTick=eb11NativeController(s7ToxicTick);
s9VoidTick=eb11NativeController(s9VoidTick);
s8MegaTick=function(e,dt){
 const r=EB11.base.mega.apply(this,arguments),A=e._frRealmAI;
 // The side-entry spread wing used its offscreen spawn x as its permanent
 // home. It could hover forever outside the firing gate. Fly into a real lane.
 if(A)A.home=clamp(A.home,camLeftX()+Math.max(55,e.w*.6),camRightX()-Math.max(55,e.w*.6));
 return r;
};
navalInSix=function(e){return EB11.base.navalGate(e)&&eb11Ready(e);};
jetManeuverTick=function(e,dt){
 const J=e._jetManeuver;
 if(J?.mode!=='dash'||e._s6storm!=='s6dart')return EB11.base.maneuver.apply(this,arguments);
 // The wave table selects this controller instead of s6StormTick. Previously
 // its offscreen windup ended in a silent corner-to-corner flyby on every rank.
 const D=J._eb11||(J._eb11={phase:'entry',age:0});D.age+=dt;e._frFlight=false;e.spin=0;
 if(e._stagger>0){e._stagger=Math.max(0,e._stagger-dt);return;}
 if(D.phase==='entry'){
  const x=clamp(e.x,camLeftX()+55,camRightX()-55),y=PLAY.y+70;
  e.x+=clamp(x-e.x,-115*dt,115*dt);if(e.y<y)e.y+=Math.min(y-e.y,135*dt);
  if(eb11Ready(e)&&e.y>=y){
   D.phase='tell';e._s6Act={t:0,at:eb11Profile().tell,dur:eb11Profile().tell+.34,fired:false,release:()=>{
    const p=s6Hardpoint(e,0,.38),a=aimPlayer(p.x,p.y);
    for(const o of [-.09,-.03,.03,.09])eShootT(p.x,p.y,a+o,5.1,'s6tracer',{silent:o>-.09});
    stage6Muzzle(e,0,.38,.58,.10);
   }};
  }
 }else if(D.phase==='tell'){
  eb11QueueTick(e,'_s6Act',dt);const Q=e._s6Act?._eb11;
  if(Q?.target)D.target={...Q.target};
  if(!e._s6Act){D.phase='dive';const p=D.target||targetShip(e.x,e.y);D.angle=Math.atan2(p.y-e.y,p.x-e.x);Audio.SFX.jetDash?.();}
 }else{
  const speed=diffKey==='easy'?260:diffKey==='hard'?380:diffKey==='furious'||diffKey==='insanity'?500:320;
  e.spin=D.angle-Math.PI/2;e.x+=Math.cos(D.angle)*speed*dt;e.y+=Math.sin(D.angle)*speed*dt;
 }
 if(e.x<camLeftX()-100||e.x>camRightX()+100||e.y>VH+100||D.age>18)e.dead=true;
};
ai27End=function(e,previous){
 // Realm engagement speed/cycles belong to its controller. Multiplying every
 // correction a second time caused overshoot and made Furious fire LESS often.
 if(e?._frRealmAI){e._frFlight=false;if(e._ai27)e._ai27.dx=0;}
 return EB11.base.end.apply(this,arguments);
};
updatePlay=function(dt){if(state===GS.PLAY)EB11.clock+=Math.min(.05,dt);return EB11.base.play.apply(this,arguments);};
beginStage=function(){EB11.clock=0;EB11.nextTell=0;return EB11.base.stage.apply(this,arguments);};
drawEnemy=function(e){const r=EB11.base.draw.apply(this,arguments),q=eb11Queue(e),Q=q?._eb11;
 if(e.dead||e._dyingT!=null||!Q?.started||q.fired||!Q.target)return r;
 const p=combatHardpoint(e,0,.34),progress=clamp(q.t/q.at,0,1);
 // Fixed-heading fans and radial patterns charge at their source; drawing an
 // aimed lane over those would incorrectly advertise their eventual trajectory.
 if(EB11.aimed.has(e.type))combatWarningDraw(e,{x:p.x,y:p.y,ex:Q.target.x,ey:Q.target.y,progress,width:24});
 else drawBossRetina(e,e.x,e.y,(1-progress)*TAU,1);
 return r;
};
