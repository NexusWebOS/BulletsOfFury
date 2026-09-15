module.exports=function(vm,ctxv,ok){
  console.log('=== 313. Jungle Overlord-X eight-beat charge warning ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={boss:boss,bossActive:bossActive,run:{stage:run.stage},curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      loop:weaponFeedbackLoop,cue:stageRevisionCue,tick:combatWarningTick,beep:Audio.SFX.retinaLockBeep,blip:Audio.SFX.blip};
    var o={},beats=[],states=[],clock=0;
    try{
      run.stage=1;curStage=STAGES[0];diffKey='normal';DIFF=DIFFS.normal;player.x=136;player.y=432;
      weaponFeedbackLoop=function(){};stageRevisionCue=function(){};
      Audio.SFX.retinaLockBeep=function(){beats.push(clock);};Audio.SFX.blip=function(){beats.push(clock+100);};
      spawnBoss('damkeeper');boss._ovIntro.done=true;boss.enter=false;boss._noHit=false;boss._ovInit=1;
      boss._ovState='fight';boss._enraged=true;boss._ovChargeCd=0;boss._ovPhase=0;boss.fireCd=9;
      updateOverlordX(boss,1/60);o.started=boss._ovState==='chargeTell'&&boss._chargeTell.beat===-1;
      var startHp=boss.hp,lockedLane=null,postLockStable=true,redFrames=0,shootFrames=0;
      for(var i=0;i<110;i++){
        clock=i/60;updateOverlordX(boss,1/60);
        var T=boss._chargeTell;
        if(T){
          if(T.flash>0){redFrames++;if(ovChargeWarningProgress(T)>.99)states.push(T.beat);}
          if(T.locked&&lockedLane==null){lockedLane=T.lane;player.x=VW-76;}
          if(T.locked&&Math.abs(T.lane-lockedLane)>.001)postLockStable=false;
          if(!boss._noHit)shootFrames++;
        }
      }
      o.eight=beats.filter(function(t){return t<10;}).length===8;
      var real=beats.filter(function(t){return t<10;}),gaps=[];for(var j=1;j<real.length;j++)gaps.push(real[j]-real[j-1]);
      o.spacing=gaps.length===7&&gaps.every(function(g){return g>.16&&g<.24;});
      o.redEach=[0,1,2,3,4,5,6,7].every(function(n){return states.indexOf(n)>=0;})&&redFrames>=16;
      o.locksHalf=lockedLane!=null&&postLockStable;
      o.shootingWindow=shootFrames>70&&boss.hp===startHp;
      o.commits=boss._ovState==='chargeOff'&&boss._chg&&Math.abs(boss._chg.lane-lockedLane)<.001;
      o.duration=OV_CHARGE_BEATS===8&&Math.abs(OV_CHARGE_TELL-1.60)<1e-9&&Math.abs(OV_CHARGE_FLASH-.105)<1e-9;
      o.noExtraAlert=beats.every(function(t){return t<10;});
      return JSON.stringify(o);
    }finally{
      boss=save.boss;bossActive=save.bossActive;run.stage=save.run.stage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      weaponFeedbackLoop=save.loop;stageRevisionCue=save.cue;combatWarningTick=save.tick;Audio.SFX.retinaLockBeep=save.beep;Audio.SFX.blip=save.blip;
    }
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Overlord eight-beat warning: '+k);
  ok(vm.runInContext(`drawBossSprite.toString().split('ovChargeWarningProgress(T)').length===3`,ctxv),'both lane and overhead alert switch to red on each synchronized beat');
};
