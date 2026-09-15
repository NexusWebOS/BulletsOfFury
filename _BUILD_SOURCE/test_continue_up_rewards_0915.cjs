const fs=require('fs');
const path=require('path');

module.exports=function(vm,ctxv,ok){
  console.log('=== 324. Continue Up reward boundaries ===');
  const gameCode=fs.readFileSync(path.resolve(__dirname,'..','assets','game.js'),'utf8');
  ok(gameCode.includes('continueRewardEliteKill(e);'),'the real enemy death chokepoint resolves eligible elite rewards');
  ok(gameCode.includes("continueRewardResolve(b,b.x,b.y,'miniboss')"),'the real miniboss death completion resolves its deathless encounter reward');
  ok(gameCode.includes("continueRewardResolve(boss,boss&&boss.x,boss&&boss.y,'boss')"),'the real boss death chokepoint resolves its deathless encounter reward');

  const out=JSON.parse(vm.runInContext(`(function(){
    const save={run:{...run},DIFF,diffKey,powerups,stageStats,stageStats2,coopOn,state,stateT,player,
      tap:Input.tap,mouse:Input.mouse.down,drawWorld,stageText,msgText,artReady,arcadeBanner,
      campaign:{unlockedMax:campaign.unlockedMax,rank:Object.assign({},campaign.rank)},pilotIndex,
      lizzieSkinUnlocked,coleUnlocked,furyLegacyShip};const o={};
    try{
      powerups=[];stageStats={deaths:0,pickupsSeen:0,pickups:0};stageStats2={deaths:0,pickupsSeen:0,pickups:0};coopOn=false;
      run.mode='arcade';run.stage=1;run.contUsed=0;run.contBonus=0;diffKey='hard';DIFF=difficultyForRun(run.mode,diffKey);

      const p=continueRewardDrop(240,100,'test');
      o.physical=p.kind==='continueup'&&p._continueSource==='test'&&powerups.length===1&&stageStats.pickupsSeen===1;
      let banner='';arcadeBanner=function(s){banner=s;};continueRewardCollect(p);
      o.collect=run.contBonus===1&&continueCap()===4&&banner==='CONTINUE UP - 4 READY';

      const clean={};continueRewardMark(clean);const n0=powerups.length;
      o.deathless=continueRewardResolve(clean,220,90,'miniboss')&&powerups.length===n0+1&&powerups[powerups.length-1]._continueSource==='miniboss';
      o.single=!continueRewardResolve(clean,220,90,'miniboss')&&powerups.length===n0+1;
      const lost={};continueRewardMark(lost);stageStats.deaths++;
      o.deathBlocks=!continueRewardResolve(lost,220,90,'boss')&&powerups.length===n0+1;

      stageStats.deaths=0;stageStats2.deaths=0;coopOn=true;const coop={};continueRewardMark(coop);stageStats2.deaths=1;
      o.coopEitherSeatBlocks=!continueRewardResolve(coop,220,90,'miniboss');coopOn=false;

      powerups=[];diffKey='normal';const ordinary={_continueEligible:true,x:240,y:100};
      o.normalEliteBlocked=!continueRewardEliteKill(ordinary)&&powerups.length===0;
      diffKey='hard';const ace={_continueEligible:true,x:240,y:100};
      o.hardElite=continueRewardEliteKill(ace)&&powerups.length===1&&powerups[0]._continueSource==='elite';
      o.eliteSingle=!continueRewardEliteKill(ace)&&powerups.length===1;
      diffKey='furious';const ace2={_continueEligible:true,x:240,y:100};
      o.furiousElite=continueRewardEliteKill(ace2)&&powerups.length===2;

      run.mode='campaign';run.stage=1;run.contBonus=4;run.contUsed=2;diffKey='normal';DIFF=difficultyForRun(run.mode,diffKey);
      o.unlimited=continueCap()===-1;
      run.stage=9;o.riftReserve=continueCap()===STAGE9_CONTINUES+4;
      const snap=campSnapshot();run.contBonus=0;run.contUsed=0;campApply(snap);
      o.saveRestore=run.contBonus===4&&run.contUsed===2;

      run.mode='arcade';run.stage=1;run.contUsed=3;run.contBonus=1;diffKey='hard';DIFF=difficultyForRun(run.mode,diffKey);
      drawWorld=function(){};stageText=function(){};msgText=function(){};artReady=function(){return false;};
      player={dead:true,deathT:1,reset:function(){this.resetCount=(this.resetCount||0)+1;}};
      Input.tap=function(k){return k==='enter';};Input.mouse.down=false;state=GS.CONTINUE;stateT=.5;drawContinue._vo=true;drawContinue(0);
      o.spendsBonus=state===GS.PLAY&&run.contUsed===4&&run.lives===DIFF.contLives;
      run.lives=0;state=GS.CONTINUE;stateT=.5;drawContinue._vo=true;drawContinue(0);
      o.exhaustsAugmentedBank=state===GS.GAMEOVER&&run.contUsed===4;
      return JSON.stringify(o);
    }finally{
      Object.assign(run,save.run);DIFF=save.DIFF;diffKey=save.diffKey;powerups=save.powerups;stageStats=save.stageStats;stageStats2=save.stageStats2;
      coopOn=save.coopOn;state=save.state;stateT=save.stateT;player=save.player;Input.tap=save.tap;Input.mouse.down=save.mouse;
      drawWorld=save.drawWorld;stageText=save.stageText;msgText=save.msgText;artReady=save.artReady;arcadeBanner=save.arcadeBanner;
      campaign.unlockedMax=save.campaign.unlockedMax;campaign.rank=save.campaign.rank;pilotIndex=save.pilotIndex;
      lizzieSkinUnlocked=save.lizzieSkinUnlocked;coleUnlocked=save.coleUnlocked;furyLegacyShip=save.furyLegacyShip;
    }
  })()`,ctxv));
  for(const k of Object.keys(out))ok(out[k],'Continue Up rewards: '+k);
};
