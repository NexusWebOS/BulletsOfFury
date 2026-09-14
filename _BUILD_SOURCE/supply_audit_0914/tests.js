// ===== 308. COMPLETE MISSILE SUPPLY FREQUENCY, 0914 =====
console.log('=== 308. missile supply frequency audit ===');
{
 const result=JSON.parse(vm.runInContext(`(function(){
  const save={run:{...run},diffKey,random:Math.random,powerups,player,boss,subBoss,bossActive,subBossActive,enemies,camX,curStage};const o={};
  try{
   run.stage=1;curStage=STAGES[0];camX=0;player={dead:false,x:240,y:400};enemies=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;
   for(const mode of ['campaign','arcade'])for(const key of ['easy','normal','hard','furious']){
    run.mode=mode;diffKey=key;run._missileBonus=null;powerups=[];Math.random=()=>.1;spawnContainer('mcrate');
    const boosted=key==='hard'||key==='furious';
    o[mode+key+'Scheduled']=powerups.length===1&&!!(run._missileBonus&&run._missileBonus.pending===1)===boosted;
   }
   diffKey='hard';run._missileBonus=null;powerups=[];Math.random=()=>.25;o.boundary=!missileSupplyBonusRoll();Math.random=()=>.24999;o.belowBoundary=missileSupplyBonusRoll();
   missileSupplyBonusTick(1.99);o.delay=powerups.length===0;powerups=[{kind:'missilepack',dead:false}];missileSupplyBonusTick(.02);o.blocked=powerups.length===1&&run._missileBonus.pending===1;
   powerups=[];missileSupplyBonusTick(.001);o.singleBonus=powerups.length===1&&powerups[0]._bonusSupply&&run._missileBonus.pending===0;
   powerups=[];missileSupplyBonusTick(100);o.noRecursion=powerups.length===0;
   missileSupplyBonusRoll();player.dead=true;const delay=run._missileBonus.delay;missileSupplyBonusTick(99);o.deadFreeze=run._missileBonus.delay===delay;player.dead=false;
   run.stage=2;missileSupplyBonusTick(2.01);o.carryStage=powerups.length===1&&run._missileBonus.pending===0;
   powerups=[];run._missileBonus=null;boss={hp:100,enter:false};bossActive=true;Math.random=()=>.1;
   bossMissileSupplyTick(5.59);o.firstBefore=powerups.length===0;bossMissileSupplyTick(.02);o.firstAfter=powerups.length===1&&boss._missileSupply.due===14.4&&!run._missileBonus;
   function randomDrop(k,r){diffKey=k;powerups=[];Math.random=()=>r;dropPowerup(240,100);return powerups[0]&&powerups[0].kind;}
   o.legacyAmmo=randomDrop('hard',.11)==='bomb'&&randomDrop('furious',.11)==='bomb'&&!randomDrop('normal',.11);
   o.noExtra=randomDrop('hard',.11801)===undefined;
   o.lifeIndependent=randomDrop('hard',.101)==='life';
   return JSON.stringify(o);
  }finally{Object.assign(run,save.run);diffKey=save.diffKey;Math.random=save.random;powerups=save.powerups;player=save.player;boss=save.boss;subBoss=save.subBoss;bossActive=save.bossActive;subBossActive=save.subBossActive;enemies=save.enemies;camX=save.camX;curStage=save.curStage;}
 })()`,ctxv));
 for(const k of Object.keys(result))ok(result[k],'Missile supply audit: '+k);
}
