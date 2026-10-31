'use strict';
/* Final-spawn normalization avoids the old stacked stage ramp on a single pool.
   No Dracodia attack/art changes: proposed difficulty variants await approval. */
const BA99={base:{mini:spawnSubBoss,boss:spawnBoss},events:[]};
spawnSubBoss=function(){const out=BA99.base.mini.apply(this,arguments),b=subBoss;
 if(eh57Own(b)){
  const max=Math.round(3200*DIFF.eHp*(coopActive()?COOP_BOSS_MUL:1)*(run.ngplus?1.25:1)),w=b._s9rift.core;
  b.hp=b.maxhp=w.hp=w.maxhp=max;BA99.events.push({event:'horizon-budget',rank:diffKey,max,coop:coopActive(),ngplus:!!run.ngplus});
 }return out;
};
globalThis.BOF_BOSS_BALANCE_1031=BA99;
// The carrier's modules retain their current budgets. Only the following ace
// life changes: the 220s two-stage film exposed excessive time away from fire.
spawnBoss=function(){const out=BA99.base.boss.apply(this,arguments),b=boss;
 if(run.stage===6&&!run._gp4StageX&&b?._carrier17&&b._whv){
  b._whv.aceMax=Math.round(3600*DIFF.eHp*(coopActive()?COOP_BOSS_MUL:1)*(run.ngplus?1.25:1));
  BA99.events.push({event:'nightwing-budget',rank:diffKey,max:b._whv.aceMax});
 }return out;
};
