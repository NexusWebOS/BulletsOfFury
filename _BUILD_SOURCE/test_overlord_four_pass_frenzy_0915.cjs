module.exports=function(vm,ctxv,ok){
  console.log('=== 314. Jungle Overlord-X four-pass half-health frenzy ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={boss:boss,bossActive:bossActive,run:{stage:run.stage},curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      loop:weaponFeedbackLoop,cue:stageRevisionCue,rain:ovPassRain,beep:Audio.SFX.retinaLockBeep};var o={};
    try{
      run.stage=1;curStage=STAGES[0];diffKey='normal';DIFF=DIFFS.normal;player.x=112;player.y=432;
      weaponFeedbackLoop=function(){};stageRevisionCue=function(){};Audio.SFX.retinaLockBeep=function(){};
      var rains=[];ovPassRain=function(b,Q){rains.push(Q.pass);};
      spawnBoss('damkeeper');boss._ovIntro.done=true;boss.enter=false;boss._noHit=false;boss._ovInit=1;boss._enraged=true;boss._ovPassUsed=false;boss._ovPassSeq=null;
      boss._ovState='fight';boss._ovChargeCd=0;boss.fireCd=999;boss.x=240;boss.y=112;boss._pivot=0;
      var seen=[],last=-9,guard=0;
      while(guard++<1800){
        updateOverlordX(boss,1/60);
        if(boss._ovState==='chargeTell'&&boss._chargeTell&&boss._chargeTell.pass!==last){last=boss._chargeTell.pass;seen.push({pass:last,dir:boss._chargeTell.dir,base:boss._chargeTell.baseLane});player.x=last%2?380:100;}
        if(seen.length===4&&boss._ovState==='reentry')break;
      }
      o.startsAtHalf=seen.length>0&&boss._ovPassUsed;
      o.four=seen.length===4&&seen.map(function(x){return x.pass;}).join(',')==='0,1,2,3';
      o.alternates=seen.map(function(x){return x.dir;}).join(',')==='1,-1,1,-1';
      o.distinct=new Set(seen.map(function(x){return x.base;})).size===4;
      o.rainOnly=rains.length>4&&rains.every(function(n){return n===1||n===3;})&&rains.indexOf(1)>=0&&rains.indexOf(3)>=0;
      o.returns=boss._ovState==='reentry'&&!boss._ovPassSeq;
      o.bounded=guard<1800;
      return JSON.stringify(o);
    }finally{boss=save.boss;bossActive=save.bossActive;run.stage=save.run.stage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;weaponFeedbackLoop=save.loop;stageRevisionCue=save.cue;ovPassRain=save.rain;Audio.SFX.retinaLockBeep=save.beep;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Overlord four-pass frenzy: '+k);
  ok(vm.runInContext(`OV_PASS_LANES.length===4&&updateOverlordX.toString().includes("Q.pass===1||Q.pass===3")`,ctxv),'only alternating passes two and four own the downward bullet rain');
};
