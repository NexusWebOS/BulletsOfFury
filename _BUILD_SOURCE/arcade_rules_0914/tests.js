// ===== 306. ARCADE STOCKS AND CREDIT LIFECYCLE, 0914 =====
console.log('=== 306. Arcade stocks and credit lifecycle ===');
{
 const result=JSON.parse(vm.runInContext(`(function(){
  const save={run:{...run},DIFF,diffKey,player,InputTap:Input.tap,drawWorld,stageText,msgText,artReady,state,stateT,curStage,bossDefeated};const o={};
  try{
   // Exercise the real continue handler without depending on the VM canvas/font stubs.
   drawWorld=function(){};stageText=function(){};msgText=function(){};artReady=function(){return false;};
   player={dead:true,deathT:1,reset:function(){this.resetCount=(this.resetCount||0)+1;}};
   Input.tap=function(k){return k==='enter';};Input.mouse.down=false;
   for(const [key,lives,credits] of [['easy',7,7],['normal',5,5],['hard',3,3],['furious',3,1]]){
    run.mode='arcade';run.stage=1;run.contUsed=0;run.lives=0;run.bombs=0;diffKey=key;DIFF=difficultyForRun(run.mode,key);
    o[key+'Stock']=DIFF.startLives===lives&&difficultyDescription(DIFF_KEYS.indexOf(key)).startsWith(lives+' LIVES');
    for(let i=0;i<credits;i++){state=GS.CONTINUE;stateT=.5;drawContinue._vo=true;drawContinue(0);}
    o[key+'Credits']=run.contUsed===credits&&run.lives===lives&&state===GS.PLAY;
    run.lives=0;state=GS.CONTINUE;stateT=.5;drawContinue._vo=true;drawContinue(0);
    o[key+'Exhaustion']=state===GS.GAMEOVER&&run.contUsed===credits&&run.lives===0;
   }
   run.mode='arcade';run.stage=9;run.contUsed=3;diffKey='normal';DIFF=difficultyForRun(run.mode,diffKey);state=GS.CONTINUE;stateT=.5;drawContinue._vo=true;drawContinue(0);
   o.stage9Bank=run.contUsed===4&&state===GS.PLAY&&continueCap()===5;
   run.contUsed=5;run.lives=0;state=GS.CONTINUE;stateT=.5;drawContinue._vo=true;drawContinue(0);
   o.stage9NoRefund=state===GS.GAMEOVER&&run.contUsed===5&&run.lives===0;
   state=GS.PLAY;riftFallbackStart();o.directRetreatNoRefund=state===GS.GAMEOVER&&run.contUsed===5;
   run.mode='campaign';DIFF=difficultyForRun(run.mode,'normal');o.campaign=DIFF===DIFFS.normal&&DIFF.continues===-1&&continueCap()===1;
   o.baseUnchanged=DIFFS.normal.startLives===4&&DIFFS.furious.startLives===1;
   return JSON.stringify(o);
  }finally{Object.assign(run,save.run);DIFF=save.DIFF;diffKey=save.diffKey;player=save.player;Input.tap=save.InputTap;drawWorld=save.drawWorld;stageText=save.stageText;msgText=save.msgText;artReady=save.artReady;state=save.state;stateT=save.stateT;curStage=save.curStage;bossDefeated=save.bossDefeated;}
 })()`,ctxv));
 for(const k of Object.keys(result))ok(result[k],'Arcade credit lifecycle: '+k);
}
