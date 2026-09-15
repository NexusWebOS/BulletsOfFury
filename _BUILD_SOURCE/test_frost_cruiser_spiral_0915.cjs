module.exports=function(vm,ctxv,ok){
  console.log('=== 317. Frost Cruiser Retina spiral rocket volley ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={sub:subBoss,active:subBossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      locks:playerLocks,bullets:eBullets,px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln};var o={};
    try{
      run.stage=3;curStage=STAGES[2];diffKey='hard';DIFF=DIFFS.hard;player.x=128;player.y=420;player.dead=false;player.invuln=1e9;
      playerLocks=[];eBullets=[];spawnSubBoss('frostcruiser');var b=subBoss;b.enter=false;b.x=worldWidth()/2;b.y=shipBossStationY(b);b._drawY=b.y;
      jungleCruiserSetState(b,'frostRocketCharge');var J=b._jc,L=playerLocks[0];
      o.hardOnly=J.hardVariant===true&&J.state==='frostRocketCharge';
      o.oneRetina=playerLocks.length===1&&L&&L.launches.length===FROST_ROCKET_COUNT;
      o.chargeSchedule=L&&Math.abs(L.launches[0].at-FROST_ROCKET_CHARGE)<1e-9&&Math.abs(L.launches[5].at-(FROST_ROCKET_CHARGE+5*FROST_ROCKET_GAP))<1e-9;
      for(var i=0;i<72;i++){jungleCruiserDirector(b,1/60);updatePlayerLocks(1/60);}
      o.noEarlyRelease=eBullets.length===0&&J.charge>.85&&L.state==='arming';
      for(;i<170;i++){jungleCruiserDirector(b,1/60);updatePlayerLocks(1/60);}
      var r=eBullets.filter(function(x){return x._frostSpiral;});
      o.sixRockets=r.length===6;
      o.alternates=r.map(function(x){return x._frostSlot;}).join('')==='LRLRLR';
      o.shootable=r.every(function(x){return x._shootable&&x.hp===1&&x.kind==='emissile';});
      o.spirals=r.every(function(x){return x._swirl&&x._swAmp===.82;})&&new Set(r.map(function(x){return x._swPh;})).size===6;
      o.sharedLock=r.every(function(x){return x._lockId===L.id;})&&L.missiles.length===6;
      o.combatSpeed=r.every(function(x){return x._accel===.032&&x._maxspd===5.65;});
      o.bounded=J.state==='edgeGun'&&J.charge===0;
      diffKey='normal';DIFF=DIFFS.normal;playerLocks=[];eBullets=[];spawnSubBoss('frostcruiser');var n=subBoss;n.enter=false;n.x=worldWidth()/2;n.y=shipBossStationY(n);
      for(var k=0;k<60;k++)jungleCruiserDirector(n,1/60);
      o.normalUntouched=!n._jc.hardVariant&&n._jc.state==='missiles'&&playerLocks.length===0;
      diffKey='furious';DIFF=DIFFS.furious;playerLocks=[];spawnSubBoss('frostcruiser');var f=subBoss;f.enter=false;f.x=worldWidth()/2;f.y=shipBossStationY(f);jungleCruiserSetState(f,'frostRocketCharge');
      o.furiousIncluded=f._jc.hardVariant&&playerLocks.length===1&&playerLocks[0].launches.length===6;
      return JSON.stringify(o);
    }finally{subBoss=save.sub;subBossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      playerLocks=save.locks;eBullets=save.bullets;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Frost Cruiser spiral volley: '+k);
  ok(vm.runInContext(`FROST_ROCKET_COUNT===6&&FROST_ROCKET_GAP===.18&&frostCruiserRocketLock.toString().includes("enemyLockOn")`,ctxv),'six alternating launches share the player Retina scheduler');
  ok(vm.runInContext(`jungleCruiserDrawUnder.toString().includes("rocketCharging")&&jungleCruiserDrawUnder.toString().includes("cfx_stage4_chain_lightning")`,ctxv),'both missile pods crackle with authored charge art before release');
};
