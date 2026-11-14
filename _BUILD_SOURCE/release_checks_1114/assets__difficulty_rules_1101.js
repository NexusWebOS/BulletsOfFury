"use strict";
/* Normal -> Hard -> Furious uses compound15% steps. Native warnings, flight,
   projectile speed, lives and counts retain their independent ownership. */
const DR15={step:1.15,keys:['normal','hard','furious'],base:{EHP,encounterFloor:encounterFloorDifficultyMul},events:[]};
function difficultyEnhancement15(key=diffKey){const i=DR15.keys.indexOf(key);return i<0?1:Math.pow(DR15.step,i);}
function difficultyHealth15(normal,key=diffKey){return Math.max(1,Math.round(normal*difficultyEnhancement15(key)));}
function difficultyHealthBaseline15(normal,legacy){return DR15.keys.includes(diffKey)?difficultyHealth15(normal):legacy;}
function turretSpeed15(normal=1){return normal*difficultyEnhancement15();}
function turretInterval15(normal,legacy=normal){return DR15.keys.includes(diffKey)?normal/difficultyEnhancement15():legacy;}
for(const key of ['hard','furious']){
 const f=difficultyEnhancement15(key);FODDER_DIFF[key]=f;
 DIFFS[key].eHp=DIFFS.normal.eHp*f;DIFFS[key].eFire=DIFFS.normal.eFire*f;
}
EHP=function(baseHp){
 if(!DR15.keys.includes(diffKey))return DR15.base.EHP.apply(this,arguments);
 const stage=run?.stage||1,pressure=combatThreat(stage),party=coopActive()?COOP_EHP_MUL:1;
 const normal=Math.max(1,Math.round(fodderShots(baseHp,stage,'normal')*PLAYER_REF_DMG*pressure.hp*party));
 return difficultyHealth15(normal);
};
encounterFloorDifficultyMul=function(stage){return DR15.keys.includes(diffKey)?difficultyEnhancement15():DR15.base.encounterFloor.apply(this,arguments);};
for(const row of Object.values(BALANCE_HP_1007))for(const key of ['hard','furious'])row[key]=row.normal;
for(const key of ['hard','furious'])BALANCE_HAMMER_HP_1016[key]=difficultyHealth15(BALANCE_HAMMER_HP_1016.normal,key);
// Every persistent Dracodia life derives from the same Normal source row.
// The native first-host shares, copied-form gates and late init retain control.
for(const key of ['hard','furious'])J3_SOURCE_HP[key]=J3_SOURCE_HP.normal.map(hp=>difficultyHealth15(hp,key));
for(const key of ['hard','furious'])IC21_TUNING[key].hp=IC21_TUNING.normal.hp.map(hp=>difficultyHealth15(hp,key));
// Pure mount solvers scale only angular tracking, never attack/body clocks.
for(const name of ['s911Mounts','s811Mounts','s711MountGuns']){
 const fn=globalThis[name];if(typeof fn!=='function')continue;
 globalThis[name]=function(e,dt,...rest){return fn.call(this,e,turretSpeed15(dt),...rest);};
}
if(typeof s711Aim==='function'){const aim=s711Aim;s711Aim=function(e,dt){return aim.call(this,e,turretSpeed15(dt));};}
if(typeof stage4CoreDifficulty==='function'){
 const config=stage4CoreDifficulty;
 stage4CoreDifficulty=function(){
  const actual=config.apply(this,arguments);if(!DR15.keys.includes(diffKey))return actual;
  const key=diffKey;let normal;try{diffKey='normal';normal=config.apply(this,arguments);}finally{diffKey=key;}
  return {...actual,shieldMul:normal.shieldMul*difficultyEnhancement15(),aimGain:turretSpeed15(normal.aimGain),diagBeat:turretInterval15(normal.diagBeat),diagGap:turretInterval15(normal.diagGap)};
 };
}
DIFF=difficultyForRun(run.mode,diffKey);
globalThis.BOF_DIFFICULTY_RULES_15={state:DR15,multiplier:difficultyEnhancement15,health:difficultyHealth15,turretSpeed:turretSpeed15,interval:turretInterval15};
