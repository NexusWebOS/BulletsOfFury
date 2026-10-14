"use strict";
/* Stage 6 story beats own their frame. The stage's extension wave controllers
   must not run behind an introduction that has disabled the player's trigger. */
const S6Q13={scene:null,held:null,events:[],base:{play:updatePlay,begin:beginStage,
 wing:s6WingTick,draw:s6WingDraw,world:drawWorld,mini:spawnSubBoss,arsenal:s6WingArsenal,pressure:s6PressureMultiplier}};
function s6q13Log(event){S6Q13.events.push({event,stage:run.stage,time:stageTimer});if(S6Q13.events.length>60)S6Q13.events.shift();}
function s6q13Scene(){
 if(state!==GS.PLAY||run.stage!==6)return null;
 if(fb2TalkActive())return fb2Talk;
 if(!boss||boss.dead||!boss._rebels)return null;
 if(!boss._rebels.frIntro?.done)return boss._rebels;
 return boss._rebels.gang1004?.scene||null;
}
function s6q13Clear(){
 // Remove the outgoing wave without awarding kills, drops or chain explosions.
 enemies.length=0;eBullets.length=0;pBullets.length=0;groundTargetingReset();polishLanes=[];tb28Reset();
 for(const list of [explosions,particles,floaters,sprAnims,fadeOuts,pilotFx,zaps,aircraftBursts,wm26Releases])list.length=0;
 if(typeof pImpacts!=='undefined')pImpacts.length=0;
 if(typeof PW5!=='undefined')PW5.threats.length=0;
 if(typeof VP12!=='undefined')VP12.groups.length=0;
 if(typeof EP13!=='undefined')EP13.owner=null;
}
function s6q13Enter(scene){
 if(S6Q13.scene===scene)return;
 S6Q13.scene=scene;s6q13Clear();h3ClearCombat();
 if(typeof Snd!=='undefined')Snd.loopStopAll?.();s6q13Log('cinematic-start');
}
function s6q13VisualTick(dt){
 // The normal update chain also ages these authored visuals. Keep just that
 // lifecycle running; do not poll inputs, charge weapons or update collisions.
 CF1004.clock+=dt;
 for(const f of CF1004.effects)f.t+=dt;
 CF1004.effects=CF1004.effects.filter(f=>f.t<f.life);
 wm26Tick(dt);
 for(const seat of seatList()){
  const p=seatShip(seat);if(!p)continue;
  if(p._cfMuzzle){p._cfMuzzle.t+=dt;if(p._cfMuzzle.t>=p._cfMuzzle.life)p._cfMuzzle=null;}
  p._mgMuzT=Math.max(0,(p._mgMuzT||0)-dt);p._spaceMuzzle=Math.max(0,(p._spaceMuzzle||0)-dt);
 }
}
function s6q13Mini(){return run.stage===6&&!run._gp4StageX&&!subBossDone&&
 (subBossActive||subBossTriggered&&warnT>0);}
function s6q13ClearWingShots(){
 for(let i=pBullets.length-1;i>=0;i--)if(pBullets[i].ally||pBullets[i]._wingKey)pBullets.splice(i,1);
}
function s6q13HoldWing(){
 if(!s6Wing)return;
 if(!S6Q13.held||S6Q13.held.wing!==s6Wing){
  S6Q13.held={wing:s6Wing,ships:s6Wing.ships.slice()};s6Wing.ships=[];s6Wing.line=null;s6q13Log('miniboss-solo');
 }
 s6q13ClearWingShots();
}
function s6q13ResumeWing(){
 const held=S6Q13.held;if(!held)return;S6Q13.held=null;
 if(run.stage!==6||held.wing!==s6Wing)return;
 for(const q of held.ships){if(q.hp<=0||q.phase==='leave')continue;
  q.phase='arrive';q.t=0;q.y=VH+60+q.slot*22;q.target=null;q.think=0;
  q.fcd=Math.max(q.fcd||0,.8);q.missileCd=Math.max(q.missileCd||0,2);q.specialCd=Math.max(q.specialCd||0,4);
  q.specialT=0;q._s6qReturn=true;s6Wing.ships.push(q);
 }
 s6q13Log('wing-return');
}
spawnSubBoss=function(){const r=S6Q13.base.mini.apply(this,arguments);if(s6q13Mini())s6q13HoldWing();return r;};
s6WingArsenal=function(){if(s6q13Mini())return;return S6Q13.base.arsenal.apply(this,arguments);};
s6PressureMultiplier=function(){return s6q13Mini()?1:S6Q13.base.pressure.apply(this,arguments);};
s6WingTick=function(dt){if(s6q13Mini()){s6q13HoldWing();return;}
 s6q13ResumeWing();return S6Q13.base.wing.apply(this,arguments);};
s6WingDraw=function(){if(s6q13Mini())return;return S6Q13.base.draw.apply(this,arguments);};
drawWorld=function(){if(!s6q13Scene())return S6Q13.base.world.apply(this,arguments);
 const loot=powerups;powerups=[];try{return S6Q13.base.world.apply(this,arguments);}finally{powerups=loot;}};
beginStage=function(){S6Q13.scene=null;S6Q13.held=null;return S6Q13.base.begin.apply(this,arguments);};
updatePlay=function(dt){
 if(s6q13Mini())s6q13HoldWing();
 const scene=s6q13Scene();
 if(scene){
  s6q13Enter(scene);
  if(typeof AV3!=='undefined')AV3.clock+=dt;
  s6q13VisualTick(dt);
  // Advance only the actual native scene owner. This includes its authored
  // ship movement, weapon exhibitions, portraits, captions and sound cues.
  if(fb2TalkActive())fb2TalkTick(dt);
  else if(!boss._rebels.frIntro?.done)h3RebelTick(boss,dt);
  else rebelSquadTick(boss,dt);
  // Cole's exhibition uses the native player projectile array. Its last volley
  // must leave with the demo beat, rather than freeze behind the next caption.
  if(fb2Talk?.beats?.[fb2Talk.i]?.kind!=='demo'){
   pBullets.length=0;for(const seat of seatList())withSeat(seat,cf1004Cancel);
  }
  Input.clearTaps?.();
  if(!s6q13Scene()){S6Q13.scene=null;H3.release=false;player._tapHeld=false;player._tapT=null;s6q13Log('cinematic-end');}
  return;
 }
 S6Q13.scene=null;
 const r=S6Q13.base.play.apply(this,arguments),entered=s6q13Scene();
 if(entered)s6q13Enter(entered);
 if(s6q13Mini())s6q13HoldWing();
 return r;
};
window.BOF_STAGE6_SEQUENCE={snapshot:()=>({scene:!!s6q13Scene(),held:!!S6Q13.held,
 savedWing:S6Q13.held?.ships.length||0,events:S6Q13.events.slice()})};
