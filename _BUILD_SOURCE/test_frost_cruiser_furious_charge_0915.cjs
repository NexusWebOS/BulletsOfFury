module.exports=function(vm,ctxv,ok){
  console.log('=== 318. Frost Cruiser Furious volley-charge combo ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={sub:subBoss,active:subBossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      locks:playerLocks,bullets:eBullets,px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln};var o={};
    try{
      run.stage=3;curStage=STAGES[2];diffKey='furious';DIFF=DIFFS.furious;player.x=120;player.y=470;player.dead=false;player.invuln=1e9;playerLocks=[];eBullets=[];
      spawnSubBoss('frostcruiser');var b=subBoss;b.enter=false;b.x=worldWidth()/2;b.y=shipBossStationY(b);b._drawY=b.y;b.hp=b.maxhp*.24;
      jungleCruiserDirector(b,1/60);var J=b._jc;o.enrageRoute=J.enraged&&J.state==='furyRocketCharge';
      var states=[J.state],guard=0;while(J.state==='furyRocketCharge'&&guard++<220){jungleCruiserDirector(b,1/60);updatePlayerLocks(1/60);if(states[states.length-1]!==J.state)states.push(J.state);}
      o.comboVolley=eBullets.filter(function(x){return x._frostSpiral;}).length===6&&J.state==='furyChargeWarn';
      for(var i=0;i<42;i++)jungleCruiserDirector(b,1/60);var early=J.furyAimX;player.x=worldWidth()-90;
      for(var k=0;k<8;k++)jungleCruiserDirector(b,1/60);var preLock=J.furyLocked;
      for(var n=0;n<6;n++)jungleCruiserDirector(b,1/60);var locked=J.furyAimX,lockFlag=J.furyLocked;player.x=90;
      for(var m=0;m<12;m++)jungleCruiserDirector(b,1/60);var after=J.furyAimX;
      o.lateCommit=!preLock&&lockFlag&&early<worldWidth()*.4&&locked>worldWidth()*.7&&after===locked;
      while(J.state==='furyChargeWarn'&&guard++<320)jungleCruiserDirector(b,1/60);
      o.dashVector=J.state==='furyDash'&&J.furyVX>0&&J.furyVY>0&&Math.hypot(J.furyVX,J.furyVY)>759;
      o.dangerous=!b._jcGhost&&J.ghost===false;
      while(J.state==='furyDash'&&guard++<420)jungleCruiserDirector(b,1/60);
      o.offscreenReturn=J.state==='furyReturn'&&b._jcGhost&&b.y<0;
      while(J.state==='furyReturn'&&guard++<650)jungleCruiserDirector(b,1/60);
      o.bounded=J.state==='recover'&&!b._jcGhost&&Math.abs(b.y-shipBossStationY(b))<1;
      diffKey='hard';DIFF=DIFFS.hard;playerLocks=[];eBullets=[];spawnSubBoss('frostcruiser');var h=subBoss;h.enter=false;h.x=worldWidth()/2;h.y=shipBossStationY(h);h.hp=h.maxhp*.24;jungleCruiserDirector(h,1/60);
      o.furiousOnly=h._jc.state==='rageMissiles'&&h._jc.state!=='furyRocketCharge';
      return JSON.stringify(o);
    }finally{subBoss=save.sub;subBossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      playerLocks=save.locks;eBullets=save.bullets;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Frost Cruiser Furious charge: '+k);
  ok(vm.runInContext(`FROST_FURY_LOCK<FROST_FURY_TELL&&FROST_FURY_TELL-FROST_FURY_LOCK>.3&&FROST_FURY_DASH===760`,ctxv),'charge follows for most of its tell, then leaves a final committed dodge window');
  ok(vm.runInContext(`jungleCruiserDrawUnder.toString().includes("furyWarning")&&jungleCruiserDrawUnder.toString().includes("combatWarningDraw")`,ctxv),'Furious body charge uses the shared green/yellow/red FOV');
};
