"use strict";
/* Tidal Sovereign is Current Breaker's vehicle. Only his final defeat settles Stage9. */
const W9P15={spawning:false,events:[],base:{spawn:spawnEnemy,plan:buildStagePlan,pending:currentBreakerPending112,init:s9FusionBossInit,tick:s9FusionBossTick,draw:s9FusionBossDraw,shipDraw:shipBossDraw,die:bossDie,hit:hitBoss,enemyHit:hitEnemy,kill:killEnemy,test:bossHitTest,targets:retinaBossTargets,space:spaceTargets,spaceHit:spaceDamageTarget,set:cb112Set,update:updatePlay,load:stageLoadBegin,begin:beginStage,contact:target17BossContact,visible:bossHealthVisible}};
function w9p15Own(b){return !!b&&run.stage===9&&!run._gp4StageX&&!!b._w9p15;}
function w9p15Log(event,data={}){W9P15.events.push({event,t:efxClock,...data});if(W9P15.events.length>700)W9P15.events.shift();}
spawnEnemy=function(type){if(run.stage===9&&!run._gp4StageX&&type==='cbreak'&&!W9P15.spawning){CB112.dispatched=true;return null;}return W9P15.base.spawn.apply(this,arguments);};
buildStagePlan=function(n){const p=W9P15.base.plan.apply(this,arguments);if(n!==9||run._gp4StageX)return p;CB112.planned=false;CB112.dispatched=true;return p.filter(w=>!w._currentBreaker112);};
currentBreakerPending112=function(){return run.stage===9&&!run._gp4StageX?false:W9P15.base.pending.apply(this,arguments);};
s9FusionBossInit=function(b){const r=W9P15.base.init.apply(this,arguments);if(run.stage===9&&!run._gp4StageX&&b._ts58){b._w9p15={phase:'ship',t:0,actor:null,bursts:0,cycles:0,settled:false,shipHP:b.maxhp};w9p15Log('ship-with-pilot',{hp:b.maxhp});}return r;};
function w9p15Actor(b){const G=b._w9p15;if(G.actor)return G.actor;let e;
 W9P15.spawning=true;try{e=spawnEnemy('cbreak',G.wreck.x,G.wreck.y,{});}finally{W9P15.spawning=false;}
 if(!e)throw Error('Current Breaker boss actor could not be created');const i=enemies.indexOf(e);if(i>=0)enemies.splice(i,1);
 e._s9PilotOwner=b;e._s911.cancelled=false;e.dead=false;delete e._dyingT;e.name='CURRENT BREAKER';e._cb112.scale=1;e._cb112.human=true;e._s911.human=true;e._cb112.age=0;
 const hp=Math.ceil(difficultyHealthBaseline15(2200,2200*[1,1.24,1.5][s911Rank()])*(coopActive()?1.5:1));e.hp=e.maxhp=e._maxhp=hp;G.actor=e;G.pilotHP=hp;S911.heavy=e;
 w9p15Log('pilot-ejected',{hp,x:e.x,y:e.y});return e;
}
function w9p15Eject(b){const G=b._w9p15;G.phase='eject';G.t=0;G.wreck={x:b.x,y:b._drawY??b.y,hp:G.shipHP};G.bursts=0;
 ts58ClearShots(b);b._ts58.protected=true;b._ts58.charge=0;b._s9fusion.phase='pilot-eject';b.hp=1;b.enter=false;b._noBodyContact=true;
 G.wreck.fx={x:G.wreck.x,y:G.wreck.y,w:b.w,h:b.h,_ship:b._ship};for(const q of eBullets)q.dead=true;if(typeof unitDeathFX==='function')unitDeathFX(G.wreck.fx,'boss','blue');combatAudio0927(b,'expBoss',.3);shake=Math.max(shake,7);w9p15Log('vehicle-destroyed',{x:b.x,y:b.y});
}
function w9p15Sync(b){const e=b._w9p15.actor;if(!e)return;b.x=e.x;b.y=b._drawY=e.y;b.w=e.w;b.h=e.h;b.flash=e.flash||0;b.hp=Math.max(0,e.hp);b.maxhp=e.maxhp;}
function w9p15Ready(b){const G=b?._w9p15,e=G?.actor;return G?.phase==='pilot'&&!b.dead&&e&&!e.dead&&!cbgLiquid(e)&&!cbgDepth(e);}
bossHealthVisible=function(b){return w9p15Own(b)&&b._w9p15.phase!=='ship'?!b.dead&&b._w9p15.phase==='pilot':W9P15.base.visible.apply(this,arguments);};
bossDie=function(){const b=boss;if(w9p15Own(b)&&b.dead)return;if(w9p15Own(b)&&!b.dead){const G=b._w9p15;if(G.phase==='ship'){w9p15Eject(b);return;}if(G.phase==='eject'||G.settled)return;
 G.settled=true;G.phase='defeat';if(G.actor){s911Cancel(G.actor);G.actor.dead=true;G.actor.hp=0;G.actor._dyingT=0;}w9p15Sync(b);b.hp=0;w9p15Log('pilot-defeated');
 }return W9P15.base.die.apply(this,arguments);};
hitBoss=function(d){const b=boss;if(!w9p15Own(b)||b._w9p15.phase==='ship')return W9P15.base.hit.apply(this,arguments);if(b._w9p15.phase!=='pilot'||b.dead)return;hitEnemy(b._w9p15.actor,d);w9p15Sync(b);};
hitEnemy=function(e){const r=W9P15.base.enemyHit.apply(this,arguments);if(e?._s9PilotOwner)w9p15Sync(e._s9PilotOwner);return r;};
killEnemy=function(e){const b=e?._s9PilotOwner;if(w9p15Own(b)){if(!b.dead&&b._w9p15.phase==='pilot'){e.hp=0;w9p15Sync(b);bossDie();}return;}return W9P15.base.kill.apply(this,arguments);};
bossHitTest=function(x,y){const b=boss;if(!w9p15Own(b)||b._w9p15.phase==='ship')return W9P15.base.test.apply(this,arguments);if(!w9p15Ready(b))return false;const yes=s911OpaqueAt(b._w9p15.actor,x,y,1);if(yes){_lastHitX=x;_lastHitY=y;}return yes;};
target17BossContact=function(b){return w9p15Own(b)&&b._w9p15.phase!=='ship'?false:W9P15.base.contact.apply(this,arguments);};
function w9p15Targets(b){if(!w9p15Ready(b))return[];const e=b._w9p15.actor;return[retinaDynamicPiece(b,'current-breaker','water pilot',()=>({x:e.x,y:e.y,hp:e.hp,dead:e.dead}),(d,shot)=>{const old=_dmgBullet,src=_dmgSrc;_dmgBullet=shot||old;try{hitBoss(d);}finally{_dmgBullet=old;_dmgSrc=src;}},e.w,e.h)];}
retinaBossTargets=function(b){return w9p15Own(b)&&b._w9p15.phase!=='ship'?w9p15Targets(b):W9P15.base.targets.apply(this,arguments);};
spaceTargets=function(){const a=W9P15.base.space.apply(this,arguments),b=boss;if(!w9p15Own(b)||b._w9p15.phase==='ship')return a;return a.filter(t=>t!==b&&t._retinaOwner!==b&&t._spaceBossOwner!==b).concat(w9p15Targets(b));};
spaceDamageTarget=function(t,d,shot){const b=t?._retinaOwner||t;if(w9p15Own(b)&&b._w9p15.phase!=='ship'){if(w9p15Ready(b)){const old=_dmgBullet;_dmgBullet=shot||old;try{hitBoss(d);}finally{_dmgBullet=old;}}return;}return W9P15.base.spaceHit.apply(this,arguments);};
cb112Set=function(e,phase){if(e?._s9PilotOwner&&phase==='retreat'&&!e._s9PilotOwner.dead){const G=e._s9PilotOwner._w9p15;G.cycles++;e._s911.cancelled=false;e._cb112.cycleDone=false;e._cb112.age=0;e._cb112.scale=1;S911.heavy=e;phase=G.cycles%2?'grenade-charge':'tidal-charge';w9p15Log('pilot-cycle',{cycle:G.cycles});}return W9P15.base.set.call(this,e,phase);};
s9FusionBossTick=function(b,dt){if(!w9p15Own(b)||b._w9p15.phase==='ship')return W9P15.base.tick.apply(this,arguments);const G=b._w9p15;if(b.dead)return false;G.t+=dt;
 if(G.phase==='eject'){
  if(G.bursts<3&&G.t>.25+G.bursts*.29){const n=G.bursts++,x=G.wreck.x+[-78,70,0][n],y=G.wreck.y+[18,-28,0][n];unitDeathFX({x,y,w:44,h:44},'jet','blue');combatAudio0927(b,'groundBombImpact',.18);shake=Math.max(shake,4);}
  if(G.t>=.65){const e=w9p15Actor(b),q=e._cb112,A=e._s911,t=G.t-.65,home={x:worldWidth()/2,y:PLAY.y+150};q.age+=dt;
   if(t<.48){q.phase='flight-launch';q.t=t;e.x=G.wreck.x;e.y=G.wreck.y;A.head=Math.PI/2;}
   else if(t<2.15){const u=clamp((t-.48)/1.67,0,1),v=u*u*(3-2*u);q.phase='flight-exit';q.t=t-.48;e.x=lerp(G.wreck.x,home.x,v)+Math.sin(Math.PI*u)*135;e.y=lerp(G.wreck.y,home.y,v)+Math.sin(Math.PI*u)*125;A.head=Math.atan2(home.y-G.wreck.y+Math.cos(Math.PI*u)*125*Math.PI,home.x-G.wreck.x+Math.cos(Math.PI*u)*135*Math.PI);}
   else{q.phase='flight-return';q.t=Math.min(.419,t-2.15);e.x=home.x;e.y=home.y;A.head=Math.PI/2;}
   if(t>0.45&&!G.flightCue){G.flightCue=true;combatAudio0927(e,'jetDash',.1);}w9p15Sync(b);b.name='CURRENT BREAKER';
  }
  if(G.t>=3.35){G.phase='pilot';G.t=0;b._s9fusion.phase='current-pilot';b._ship=null;const e=G.actor;e._cb112.scale=1;e._cb112.human=true;e._s911.cancelled=false;cb112Set(e,'grenade-charge');w9p15Sync(b);w9p15Log('pilot-fight-start');}
  return true;
 }
 const e=G.actor;if(e&&!e.dead){e.flash=Math.max(0,(e.flash||0)-dt);cb112Tick(e,Math.min(.05,dt));w9p15Sync(b);}return true;
};
function w9p15Wreck(b){const G=b._w9p15,saved={x:b.x,y:b.y,_drawY:b._drawY,hp:b.hp,maxhp:b.maxhp,flash:b.flash},T=b._ts58,old={mode:T.mode,phase:T.phase,charge:T.charge};
 Object.assign(b,{x:G.wreck.x,y:G.wreck.y,_drawY:G.wreck.y,hp:G.shipHP*.08,maxhp:G.shipHP,flash:0});Object.assign(T,{mode:'wreck',phase:'wreck',charge:0});try{W9P15.base.shipDraw(b);}finally{Object.assign(b,saved);Object.assign(T,old);}}
s9FusionBossDraw=function(b){if(!w9p15Own(b)||b._w9p15.phase==='ship')return W9P15.base.draw.apply(this,arguments);const G=b._w9p15;if(G.phase==='eject'&&G.t<1.18)w9p15Wreck(b);if(G.actor&&(G.phase!=='defeat'||(b.dying||0)<.45))s911Draw(G.actor);return true;};
stageLoadBegin=function(n,keys){if(n===9){keys=[...(keys||[]),...Object.values(CB112_ART.banks).map(a=>a.key),...s911Keys()];Snd.prepare(['jetDash','expBoss','groundBombImpact','cfComboWater','bossWeaponCharge']);}return W9P15.base.load.call(this,n,keys);};
updatePlay=function(dt){const b=boss,r=W9P15.base.update.apply(this,arguments);if(w9p15Own(b)&&b._w9p15.actor&&(!boss||boss!==b||b.dead))s911Cancel(b._w9p15.actor);return r;};
beginStage=function(){const b=boss;if(w9p15Own(b)&&b._w9p15.actor)s911Cancel(b._w9p15.actor);return W9P15.base.begin.apply(this,arguments);};
window.BOF_STAGE9_PILOT_1115=W9P15;
