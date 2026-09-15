module.exports=function(vm,ctxv,ok){
  console.log('=== 332. Sovereign shared unpowered-ram warning ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={boss:boss,active:bossActive,runStage:run.stage,runShield:run.shield,curStage:curStage,diffKey:diffKey,DIFF:DIFF,bullets:eBullets,plan:stagePlan,px:player.x,py:player.y,pdead:player.dead,palive:player.alive,pinv:player.invuln};var o={};
    try{run.stage=4;curStage=STAGES[3];diffKey='normal';DIFF=DIFFS.normal;stagePlan=[];eBullets=[];run.shield=3;player.x=worldWidth()*.30;player.y=VH-62;player.dead=false;player.alive=true;player.invuln=0;
      spawnBoss('stormsovereign');var b=boss,S=b._s4war;b.enter=false;b.x=worldWidth()/2;b.y=S.homeY;b._drawY=b.y;b.fireCd=999;bossActive=true;
      o.shieldBlocks=!stage4RamStart(b);S.shield.active=false;S.shield.rearming=false;for(const n of S.shield.nodes)n.dead=true;o.starts=stage4RamStart(b)&&S.mode==='ramTell';
      stage4RamTick(b,.20);var B=b._combatWarnings['sovereign-unpowered-ram'];o.green=B&&B.t===.20&&!B.released&&l23FovPhase(B.t/B.warm)==='green';var first=S.ram.lane;
      player.x=worldWidth()*.72;stage4RamTick(b,.19);stage4RamTick(b,.02);var locked=S.ram.lane;o.yellow=S.ram.locked&&l23FovPhase(b._combatWarnings['sovereign-unpowered-ram'].t)==='yellow'&&locked!==first;
      player.x=worldWidth()*.12;stage4RamTick(b,.42);o.committed=S.ram.locked&&S.ram.lane===locked&&l23FovPhase(b._combatWarnings['sovereign-unpowered-ram'].t)==='red';
      stage4RamTick(b,.18);B=b._combatWarnings['sovereign-unpowered-ram'];o.releases=B.released&&S.mode==='ramDive'&&S.ram.lane===locked;
      var ds=stage4RamShadowDraw.toString(),ts=stage4RamTick.toString();o.sharedDraw=ds.includes('combatWarningDraw')&&!ds.includes('l23FovDraw');o.sharedTick=ts.includes("combatWarningTick(b,'sovereign-unpowered-ram'");
      return JSON.stringify(o);
    }finally{boss=save.boss;bossActive=save.active;run.stage=save.runStage;run.shield=save.runShield;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;eBullets=save.bullets;stagePlan=save.plan;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.alive=save.palive;player.invuln=save.pinv;}
  })()`,ctxv));for(const k of Object.keys(q))ok(q[k],'Sovereign shared ram warning: '+k);
};
