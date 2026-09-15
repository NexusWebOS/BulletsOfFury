module.exports=function(vm,ctxv,ok){
  console.log('=== 304h. Stage 2 Hard encounter HP and fire absorption ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    const save={boss:boss,bossActive:bossActive,sub:subBoss,subActive:subBossActive,stage:run.stage,cur:curStage,diff:diffKey,D:DIFF,floaters:floaters};
    try{
      run.stage=2;curStage=STAGES[1];floaters=[];
      diffKey='normal';DIFF=DIFFS.normal;spawnBoss('infernoreaver');const nb=boss.maxhp;boss=null;bossActive=false;spawnSubBoss__inner('magmaward');const nm=subBoss.maxhp;subBoss=null;subBossActive=false;
      diffKey='hard';DIFF=DIFFS.hard;spawnBoss('infernoreaver');const hb=boss.maxhp,br=elementalDamageResult(boss,'boss',{kind:'flame',_fire:true},100,boss.x,boss.y);boss=null;bossActive=false;
      spawnSubBoss__inner('magmaward');const hm=subBoss.maxhp,mr=elementalDamageResult(subBoss,'subboss',{kind:'flame',_fire:true},100,subBoss.x,subBoss.y);
      return JSON.stringify({nb:nb,nm:nm,hb:hb,hm:hm,bossRatio:hb/nb,miniRatio:hm/nm,bossDamage:br.dmg,miniDamage:mr.dmg,bossReaction:br.reaction,miniReaction:mr.reaction,
        floorMul:encounterFloorDifficultyMul(2),furious:(diffKey='furious',DIFF=DIFFS.furious,encounterFloorDifficultyMul(2))});
    }finally{boss=save.boss;bossActive=save.bossActive;subBoss=save.sub;subBossActive=save.subActive;run.stage=save.stage;curStage=save.cur;diffKey=save.diff;DIFF=save.D;floaters=save.floaters;}
  })()`,ctxv));
  ok(q.floorMul===1.25,'Stage 2 Hard uses the exact +25% encounter-floor multiplier');
  ok(Math.abs(q.bossRatio-1.25)<.001,'the live Furnace Tyrant Hard HP is exactly 25% above Normal');
  ok(Math.abs(q.miniRatio-1.25)<.001,'the live Magma Ward Hard HP is exactly 25% above Normal');
  ok(q.bossDamage===50&&q.bossReaction==='absorb-fire','the Stage-2 boss retains exactly half same-element fire damage');
  ok(q.miniDamage===50&&q.miniReaction==='absorb-fire','the Stage-2 miniboss retains exactly half same-element fire damage');
  ok(q.furious===1.30,'Furious keeps its existing encounter multiplier');
};
