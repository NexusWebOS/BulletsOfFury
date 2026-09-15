module.exports=function(vm,ctxv,ok){
  console.log('=== 312. Jungle Overlord-X bottom flyover and whip ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={boss:boss,bossActive:bossActive,run:{stage:run.stage},curStage:curStage,diffKey:diffKey,DIFF:DIFF,loop:weaponFeedbackLoop,cue:stageRevisionCue};var o={};
    try{
      run.stage=1;curStage=STAGES[0];diffKey='normal';DIFF=DIFFS.normal;player.x=118;player.y=430;weaponFeedbackLoop=function(){};stageRevisionCue=function(){};
      spawnBoss('damkeeper');o.startsBelow=boss.y>VH&&boss._ovAirborne&&boss._ovIntro.fromX===118;o.shadowGate=!bossHealthVisible(boss);
      var crossed=false,minD=999;
      for(var i=0;i<72;i++){updateBoss(1/60);minD=Math.min(minD,Math.abs(boss.y-player.y));if(Math.abs(boss.y-player.y)<boss.h*.45)crossed=true;}
      o.crossesPlayer=crossed&&minD<8;o.centers=Math.abs(boss.x-VW/2)<1&&Math.abs(boss.y-boss.ty)<1;
      o.whip=boss._ovIntro.phase==='whip'&&!boss._ovAirborne;for(var j=0;j<14;j++)updateBoss(1/60);o.spin=Math.abs(boss._pivot)>1;
      for(var k=0;k<20;k++)updateBoss(1/60);o.gaugeWait=boss._ovIntro.phase==='fade'&&bossHealthVisible(boss);
      return JSON.stringify(o);
    }finally{boss=save.boss;bossActive=save.bossActive;run.stage=save.run.stage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;weaponFeedbackLoop=save.loop;stageRevisionCue=save.cue;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Overlord flyover intro: '+k);
  ok(vm.runInContext(`drawWorld.toString().indexOf('drawPlayer();')<drawWorld.toString().indexOf('overlordIntroOverflightDraw();')`,ctxv),'overflight hull and full-frame shadow render above the player');
  ok(vm.runInContext(`overlordIntroOverflightDraw.toString().includes("xartTint('ovbody_intact','#020407'")&&overlordIntroOverflightDraw.toString().includes('shadowRotor')`,ctxv),'shadow uses the complete authored body and rotor silhouettes');
};
