"use strict";
/* Late campaign pressure uses complementary native toxic roles. Ground armor
   stays in the central floor strip at spawn and after every movement pass. */
const SEWER17={next:4,age:0,serial:0,spawned:0,base:{spawn:spawnEnemy,end:ai27End,play:updatePlay,begin:beginStage,profile:eb11Profile,cancel:ep13Cancel}};
function sewer17Band(e){const W=worldWidth(),half=(e.w||58)*.55;return {l:W*.34+half,r:W*.66-half};}
function sewer17Clamp(e){if(run.stage!==7||e?._modTank!==7)return;const q=sewer17Band(e);e.x=clamp(e.x,q.l,q.r);e._noSep=true;e._lane=e.x;e._lockX=e.x;}
spawnEnemy=function(){const start=enemies.length,r=SEWER17.base.spawn.apply(this,arguments);for(const e of enemies.slice(start))sewer17Clamp(e);return r;};
ai27End=function(e){const r=SEWER17.base.end.apply(this,arguments);sewer17Clamp(e);return r;};
eb11Profile=function(){const P=SEWER17.base.profile.apply(this,arguments);if(run.stage!==7)return P;
 const rank=target17Rank();return {...P,rate:P.rate*[1,1.15,1.25,1.32,1.35][rank],cooldown:P.cooldown*[1,.90,.80,.70,.65][rank],slots:P.slots+(rank>=2?1:0),spacing:Math.max(.07,P.spacing*.8),cycles:P.cycles+1};};
ep13Cancel=function(e){const r=SEWER17.base.cancel.apply(this,arguments);if(run.stage===7&&e){e._ep13Next=EP13.clock+(target17Rank()>=3?4:6);e._ep13Cycles=Math.min(e._ep13Cycles||0,1);}return r;};
function sewer17Wave(dt){if(run.stage!==7||state!==GS.PLAY||bossActive||subBossActive||warnT>0||bossDefeated||story)return;
 // Extra pressure must not refill the crowd gates forever and postpone the
 // authored miniboss/boss. Existing enemies keep fighting through the approach.
 if(bossWarned||stageTimer>=curStage.length-3||(!subBossDone&&!subBossTriggered&&stageTimer>=curStage.length*Math.max(0,(SUBBOSS[7]?.at||.45)-.03)))return;
 SEWER17.age+=dt;SEWER17.next-=dt;if(SEWER17.next>0)return;
 const rank=target17Rank(),cap=[5,8,11,14,16][rank],alive=enemies.filter(e=>!e.dead&&e._dyingT==null).length;
 if(alive>=cap||eBullets.length>ep13Profile().cap-20){SEWER17.next=.5;return;}
 const W=worldWidth(),seq=SEWER17.serial++%4;
 const waves=[
  [['s7lamprey',.40,-80],['s7sampler',.65,-122]],
  [['s7skimmer',-.12,PLAY.y+74],['s7tank',.50,-100]],
  [['s7serpent',.40,-80],['s7serpent',.60,-140]],
  [['s7barge',.50,-100],['s7skimmer',1.12,PLAY.y+115]]
 ];
 const rows=waves[seq].slice(0,rank===0?1:2);
 for(const [type,fx,y] of rows){const e=spawnEnemy(type,W*fx,y,{_side:fx>1?-1:1,_stagger:.18*rows.indexOf(rows.find(r=>r[0]===type))});
  if(e){e._sewer17Reinforcement=true;SEWER17.spawned++;}}
 SEWER17.next=[12,9,6.4,4.4,3.8][rank];
}
updatePlay=function(dt){const r=SEWER17.base.play.apply(this,arguments);for(const e of enemies)sewer17Clamp(e);sewer17Wave(dt);return r;};
beginStage=function(){SEWER17.age=0;SEWER17.next=4;SEWER17.serial=0;SEWER17.spawned=0;return SEWER17.base.begin.apply(this,arguments);};
window.BOF_SEWER_ASSAULT={state:SEWER17,band:sewer17Band};
