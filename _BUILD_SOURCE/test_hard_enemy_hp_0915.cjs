module.exports=function(vm,ctxv,ok){
  console.log('=== 304f. Hard enemy hull and shield health ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var campaign=difficultyForRun('campaign','hard'), arcade=difficultyForRun('arcade','hard');
    var normalShots=fodderShots(20,6,'normal'), hardShots=fodderShots(20,6,'hard');
    run.stage=5; diffKey='hard'; DIFF=campaign;
    var e={type:'s5gravity',hp:115,maxhp:115,w:40,h:40}; enemyShieldAutoEquip(e);
    return JSON.stringify({hardMul:FODDER_DIFF.hard,normalMul:FODDER_DIFF.normal,furiousMul:FODDER_DIFF.furious,
      campaignHp:campaign.eHp,arcadeHp:arcade.eHp,campaignBase:campaign===DIFFS.hard,arcadeCopy:arcade!==DIFFS.hard,
      normalShots:normalShots,hardShots:hardShots,shield:e._esh&&e._esh.energy,shieldExpected:Math.max(4,Math.round(115*.34)),
      bossSeparate:DIFFS.hard.eHp===1.10});
  })()`,ctxv));
  ok(q.hardMul===1.15,'Hard ordinary-enemy HP multiplier is exactly +15% over Normal');
  ok(q.normalMul===1&&q.furiousMul===1.60,'Normal and Furious ordinary-enemy tuning stays intact');
  ok(q.hardShots>=q.normalShots,'quantized shots-to-kill remains monotonic at Hard');
  ok(q.campaignHp===q.arcadeHp&&q.campaignBase&&q.arcadeCopy,'Campaign and Arcade share Hard combat tuning without mutating the base table');
  ok(q.shield===q.shieldExpected,'automatic enemy shield energy derives from the Hard-scaled hull');
  ok(q.bossSeparate,'boss and miniboss HP remains on the encounter-specific multiplier');
};


