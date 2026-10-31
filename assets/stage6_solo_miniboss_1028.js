"use strict";
/* Stage6 miniboss: no NPC wing or callable ally; human co-op is unchanged. */
const S6SOLO={entering:0,held:null,base:{mini:spawnSubBoss,inner:spawnSubBoss__inner,wing:s6WingTick,launch:s6WingLaunch,draw:s6WingDraw,play:updatePlay,call:allyCall,allyTick:allyUpdate,allyDraw:allyDraw,ready:er28WingReady}};
function s6SoloScope(){return run.stage===6&&!run._gp4StageX;}
function s6SoloActive(){return s6SoloScope()&&(S6SOLO.entering>0||debugFight?.stage===6&&debugFight.role==='mini'||!bossActive&&(subBossActive||!!subBoss&&!subBossDone||subBossTriggered&&!subBossDone&&warnKind==='sub'&&warnT>0));}
function s6SoloHold(){
 if(!s6Wing)s6WingInit();
 if(!S6SOLO.held||S6SOLO.held.wing!==s6Wing)S6SOLO.held={wing:s6Wing,ships:[],ally:null};
 const H=S6SOLO.held;for(const q of s6Wing.ships)if(!H.ships.includes(q))H.ships.push(q);s6Wing.ships.length=0;
 if(ally){H.ally=ally;ally=null;}
 for(let i=pBullets.length-1;i>=0;i--)if(pBullets[i].ally||pBullets[i]._wingKey)pBullets.splice(i,1);
}
function s6SoloRelease(){
 const H=S6SOLO.held;if(!H)return;S6SOLO.held=null;
 if(!s6SoloScope()||H.wing!==s6Wing)return;
 for(const q of H.ships)if(q.hp>0&&!s6Wing.ships.some(p=>p.key===q.key)){q.phase='arrive';q.t=0;q.y=VH+65+q.slot*18;q.vx=q.vy=0;s6Wing.ships.push(q);}
 if(H.ally&&!ally){ally=H.ally;ally.phase='arrive';ally.t=0;ally.y=VH+70;}
}
function s6SoloSpawn(base,args){if(!s6SoloScope())return base.apply(this,args);S6SOLO.entering++;s6SoloHold();try{return base.apply(this,args);}finally{if(s6SoloScope())s6SoloHold();S6SOLO.entering--;}}
spawnSubBoss=function(){return s6SoloSpawn.call(this,S6SOLO.base.mini,arguments);};
spawnSubBoss__inner=function(){return s6SoloSpawn.call(this,S6SOLO.base.inner,arguments);};
er28WingReady=function(){const r=S6SOLO.base.ready.apply(this,arguments);if(s6SoloActive())s6SoloHold();return r;};
s6WingLaunch=function(){if(s6SoloActive()){s6SoloHold();return;}s6SoloRelease();return S6SOLO.base.launch.apply(this,arguments);};
s6WingTick=function(dt){if(s6SoloActive()){s6SoloHold();s6SupplyTick(s6Wing,dt);s6WingRadioTick(s6Wing,dt);return;}s6SoloRelease();return S6SOLO.base.wing.apply(this,arguments);};
s6WingDraw=function(){if(s6SoloActive()){s6SoloHold();s6SupplyDraw(s6Wing);return;}return S6SOLO.base.draw.apply(this,arguments);};
allyCall=function(){if(s6SoloActive())return false;return S6SOLO.base.call.apply(this,arguments);};
allyUpdate=function(){if(s6SoloActive()){s6SoloHold();return;}s6SoloRelease();return S6SOLO.base.allyTick.apply(this,arguments);};
allyDraw=function(){if(s6SoloActive())return;return S6SOLO.base.allyDraw.apply(this,arguments);};
updatePlay=function(){if(s6SoloActive())s6SoloHold();else s6SoloRelease();const r=S6SOLO.base.play.apply(this,arguments);if(s6SoloActive())s6SoloHold();return r;};
globalThis.BOF_STAGE6_SOLO_MINIBOSS_1028=S6SOLO;
