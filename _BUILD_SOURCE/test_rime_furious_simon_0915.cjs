module.exports=function(vm,ctxv,ok){
  console.log('=== 320. Rime Wall Furious Simon-Says cannon feints ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={boss:boss,active:bossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      locks:playerLocks,bullets:eBullets,pb:pBullets,en:enemies,plan:stagePlan,
      px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln,roll:player.roll,somer:player.somer};var o={};
    try{
      run.stage=3;curStage=STAGES[2];diffKey='furious';DIFF=DIFFS.furious;stagePlan=[];enemies=[];pBullets=[];eBullets=[];playerLocks=[];
      player.x=worldWidth()*.5;player.y=610;player.dead=false;player.invuln=999;player.roll=null;player.somer=null;
      spawnBoss('cryospear');var b=boss;b.enter=false;b.x=worldWidth()/2;b.y=shipBossStationY(b);b._drawY=b.y;b.hp=b.maxhp*.20;b.fireCd=0;bossActive=true;
      shipBossAttack(b);var F=b._s3boss.furyFeint;
      o.liveRoute=!!F&&b._sbPat==='s3walloverdrive';
      o.fast=F&&Math.abs(F.beat-.34)<.0001&&F.seq.length*F.beat<2;
      o.colors=F&&F.colors.join(',')==='yellow,red,yellow,red,red'&&!F.colors.includes('green');
      o.mountGame=F&&new Set(F.seq).size===2&&F.seq[F.seq.length-1]===F.actual;
      o.oneRetina=playerLocks.length===1&&playerLocks[0].launches.length===2;
      var expected=F.actual;
      for(var i=0;i<4;i++)stage3BossTick(b,.341);
      o.fourBeats=b._s3boss.furyFeint&&b._s3boss.furyFeint.log.length===5;
      stage3BossTick(b,.40);
      var B=b._l23Beam,L=b._s3boss.lastFeintLog;
      o.release=!!B&&B._furySimon&&B.released&&B.slots.length===1&&B.slots[0]===expected;
      o.finalWins=L&&L.length===6&&L[4].type==='cue'&&L[4].color==='red'&&L[5].type==='fire'&&L[5].slot===L[4].slot;
      o.fixed=B&&B.spin===0&&B.sweepArc===0&&B.angles[0]===B.baseAngles[0];
      o.noAsterisk=stage3FuryFeintDraw.toString().indexOf('l23WarnSymbolDraw')<0&&stage3CoreWarningDraw.toString().indexOf('furyFeint')>=0;

      diffKey='hard';DIFF=DIFFS.hard;playerLocks=[];eBullets=[];b._l23Beam=null;b._s3boss.furyFeint=null;b._s3boss.charge=null;b._sbPhase=3;b._sbStep=0;b.hp=b.maxhp*.20;
      shipBossAttack(b);o.hardRoute=!b._s3boss.furyFeint&&!!b._l23Beam&&playerLocks.length===1;
      diffKey='normal';DIFF=DIFFS.normal;playerLocks=[];eBullets=[];b._l23Beam=null;b._s3boss.furyFeint=null;b._s3boss.charge=null;b._sbPhase=3;b._sbStep=0;
      shipBossAttack(b);o.normalRoute=!b._s3boss.furyFeint&&!!b._l23Beam&&playerLocks.length===0;
      return JSON.stringify(o);
    }finally{boss=save.boss;bossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      playerLocks=save.locks;eBullets=save.bullets;pBullets=save.pb;enemies=save.en;stagePlan=save.plan;
      player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;player.roll=save.roll;player.somer=save.somer;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Rime Wall Furious Simon-Says: '+k);
  ok(vm.runInContext(`l23FovDraw.toString().includes('B.fovColor')`,ctxv),'the authored FOV renderer accepts the Furious yellow/red override');
};
