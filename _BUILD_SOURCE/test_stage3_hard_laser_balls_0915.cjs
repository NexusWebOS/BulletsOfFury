module.exports=function(vm,ctxv,ok){
  console.log('=== 319. Rime Wall Hard Retina laser pair ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={boss:boss,active:bossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      locks:playerLocks,bullets:eBullets,pb:pBullets,en:enemies,plan:stagePlan,
      px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln,roll:player.roll,somer:player.somer};var o={};
    try{
      run.stage=3;curStage=STAGES[2];diffKey='hard';DIFF=DIFFS.hard;stagePlan=[];enemies=[];pBullets=[];eBullets=[];playerLocks=[];
      player.x=120;player.y=610;player.dead=false;player.invuln=999;player.roll=null;player.somer=null;
      spawnBoss('cryospear');var b=boss;b.enter=false;b.x=worldWidth()/2;b.y=shipBossStationY(b);b._drawY=b.y;b.hp=b.maxhp*.49;b.fireCd=999;bossActive=true;
      o.starts=stage3BossHardLaserPair(b)&&playerLocks.length===1&&playerLocks[0].launches.length===2;
      for(var i=0;i<39;i++)updatePlayerLocks(1/60);
      var first=eBullets.filter(function(x){return x._s3LaserBall;});
      o.firstBeat=first.length===1&&first[0]._shootable&&first[0].hp===2;
      for(var j=0;j<16;j++)updatePlayerLocks(1/60);
      var pair=eBullets.filter(function(x){return x._s3LaserBall;});
      o.pair=pair.length===2&&pair[0]._lockId===pair[1]._lockId&&pair[0]._lockId===playerLocks[0].id;
      o.authored=pair.every(function(x){return x.kind==='s3mortar'&&x._l23fx==='rime_orb'&&x._s3StaticSpin;});
      var a0=Math.atan2(pair[0].vy,pair[0].vx);player.x=worldWidth()-80;
      for(var k=0;k<7;k++)updatePlay(1/60);
      var a1=Math.atan2(pair[0].vy,pair[0].vx);o.homes=Math.abs(a1-a0)>.02;
      player.roll={t:.01,dur:.4,dir:1};updatePlayerLocks(1/60);var state=playerLocks[0].state;
      var before=Math.atan2(pair[0].vy,pair[0].vx);player.x=80;
      for(var n=0;n<8;n++)updatePlay(1/60);
      var after=Math.atan2(pair[0].vy,pair[0].vx);o.evasion=state==='broken'&&Math.abs(after-before)<.0001;
      pair[0].x=player.x;pair[0].y=player.y-40;pBullets=[{x:pair[0].x,y:pair[0].y,w:8,h:12,kind:'mg',vx:0,vy:-8,dmg:1,t:0,dead:false}];updatePlay(1/60);
      o.shootable=pair[0].dead===true;
      pair[1].x=-80;pair[1].vx=-5;pair[1].y=300;pair[1].dead=false;updatePlay(1/60);o.exits=pair[1].dead===true;
      player.roll=null;playerLocks=[];eBullets=[];diffKey='normal';DIFF=DIFFS.normal;o.normal=!stage3BossHardLaserPair(b)&&playerLocks.length===0;
      diffKey='hard';DIFF=DIFFS.hard;b.hp=b.maxhp*.75;o.healthGate=!stage3BossHardLaserPair(b)&&playerLocks.length===0;
      spawnSubBoss('rimewall');var m=subBoss;m.enter=false;m.hp=m.maxhp*.4;o.wallOnly=!stage3BossHardLaserPair(m)&&playerLocks.length===0;
      return JSON.stringify(o);
    }finally{boss=save.boss;bossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      playerLocks=save.locks;eBullets=save.bullets;pBullets=save.pb;enemies=save.en;stagePlan=save.plan;
      player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;player.roll=save.roll;player.somer=save.somer;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Rime Wall Hard laser pair: '+k);
  ok(vm.runInContext(`stage3BossAttack.toString().includes("stage3BossHardLaserPair(b)")`,ctxv),'both below-half Rime Wall patterns call the shared Retina pair');
  ok(vm.runInContext(`stage3BossHardLaserPair.toString().includes("enemyLockOn")&&lockEvading.toString().includes("player.roll")&&lockEvading.toString().includes("player.somer")`,ctxv),'the pair inherits the shared roll and somersault lock break');
};
