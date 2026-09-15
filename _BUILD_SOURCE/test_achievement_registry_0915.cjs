module.exports=function(vm,ctxv,ok){
  console.log('=== 304k. persistent achievement registry ===');
  const out=JSON.parse(vm.runInContext(`(function(){
    const save={get:localStorage.getItem,set:localStorage.setItem,remove:localStorage.removeItem,
      state:achievementState,last:achievementLastUnlock,queue:achievementSteamQueue,
      mode:run.mode,pilot:run.pilot,stage:run.stage,contUsed:run.contUsed,diff:diffKey,coop:coopOn};
    let store={};const o={};
    try{
      localStorage.getItem=k=>Object.prototype.hasOwnProperty.call(store,k)?store[k]:null;
      localStorage.setItem=(k,v)=>{store[k]=String(v);};
      localStorage.removeItem=k=>{delete store[k];};
      achievementState=achievementEmpty();achievementLastUnlock=null;achievementSteamQueue=[];

      const defs=achievementList(),ids=defs.map(d=>d.id),steam=defs.map(d=>d.steamKey);
      o.definitionCount=defs.length===66;
      o.uniqueIds=new Set(ids).size===66;
      o.uniqueSteamKeys=steam.every(Boolean)&&new Set(steam).size===66;
      o.campaignFamily=defs.filter(d=>d.family==='campaign_clear').length===9&&
        defs.filter(d=>d.family==='campaign_clear').every(d=>d.points===100&&d.title.indexOf('Campaign Clear - ')===0);
      o.stageFamilies=defs.filter(d=>d.family==='stage_clear').length===9&&
        defs.filter(d=>d.family==='stage_nodeath').length===9&&defs.filter(d=>d.family==='stage_nomissile').length===9;
      o.difficultyFamilies=defs.filter(d=>d.difficulty==='hard').length===9&&
        defs.filter(d=>d.difficulty==='furious').length===9&&
        defs.filter(d=>d.difficulty==='hard').every(d=>d.points===200)&&
        defs.filter(d=>d.difficulty==='furious').every(d=>d.points===500);
      o.weaponFamily=defs.filter(d=>d.family==='weapon_max').length===7&&defs.filter(d=>d.family==='weapon_max').every(d=>d.points===20);
      o.specialAwards=achievementDefinition('run_no_continue').points===1000&&
        achievementDefinition('run_no_continue').reward==='trophy_avatar_no_continue'&&
        defs.filter(d=>d.family==='boss_speed').length===4;
      o.emptyProfile=achievementPoints()===0&&Object.keys(achievementProfileSnapshot().unlocked).length===0;

      const meta={mode:'campaign',pilot:'yuri',nested:{stage:9}};
      o.firstUnlock=achievementUnlock('campaign_clear_yuri',meta)===true;
      meta.nested.stage=1;
      o.metaClone=achievementState.unlocked.campaign_clear_yuri.meta.nested.stage===9;
      o.secondUnlock=achievementUnlock('stage_clear_1',{difficulty:'normal'})===true;
      o.duplicateRefused=achievementUnlock('campaign_clear_yuri',{mode:'arcade'})===false;
      o.unknownRefused=achievementUnlock('does_not_exist')===false;
      o.pointsOnce=achievementPoints()===110;
      o.lastUnlock=achievementLastUnlock.id==='stage_clear_1'&&achievementLastUnlock.points===10&&achievementLastUnlock.persisted;
      o.steamQueue=achievementSteamQueue.length===2&&achievementSteamQueue[0].steamKey==='BOF_CAMPAIGN_CLEAR_YURI'&&achievementSteamQueue[1].steamKey==='BOF_STAGE_1_CLEAR';
      o.singleProfileKey=Object.keys(store).length===1&&Object.keys(store)[0]===ACHIEVEMENT_STORE_KEY&&ACHIEVEMENT_STORE_KEY.indexOf('slot')<0;

      achievementState=achievementEmpty();achievementReload();
      o.persistentReload=achievementUnlocked('campaign_clear_yuri')&&achievementUnlocked('stage_clear_1')&&achievementPoints()===110;
      const snap=achievementProfileSnapshot();snap.unlocked.campaign_clear_yuri.at=-1;
      o.snapshotCopy=achievementState.unlocked.campaign_clear_yuri.at!==-1;
      store[ACHIEVEMENT_STORE_KEY]='{broken';achievementReload();
      o.corruptRecovery=achievementPoints()===0&&Object.keys(achievementState.unlocked).length===0;
      store[ACHIEVEMENT_STORE_KEY]=JSON.stringify({version:1,unlocked:{does_not_exist:{at:4},stage_clear_2:{at:5}}});achievementReload();
      o.unknownPruned=!achievementUnlocked('does_not_exist')&&achievementUnlocked('stage_clear_2')&&achievementPoints()===10;
      o.futureSteamMapping=defs.every(d=>/^BOF_[A-Z0-9_]+$/.test(d.steamKey));

      achievementState=achievementEmpty();achievementSteamQueue=[];run.mode='campaign';run.stage=3;coopOn=false;
      diffKey='easy';let got=achievementStageComplete(2,{deaths:0,missiles:0},null);
      o.easyDisciplineOnly=got.join(',')==='stage_nomissile_2';
      diffKey='normal';got=achievementStageComplete(3,{deaths:0,missiles:0},null);
      o.normalCleanStage=got.includes('stage_clear_3')&&got.includes('stage_nodeath_3')&&got.includes('stage_nomissile_3');
      got=achievementStageComplete(4,{deaths:1,missiles:1},null);
      o.dirtyStageOnlyClears=got.join(',')==='stage_clear_4';
      coopOn=true;got=achievementStageComplete(5,{deaths:0,missiles:0},{deaths:1,missiles:0});
      o.coopDeathBlocksNoDeath=got.includes('stage_clear_5')&&!got.includes('stage_nodeath_5')&&got.includes('stage_nomissile_5');
      got=achievementStageComplete(6,{deaths:0,missiles:0},{deaths:0,missiles:1});
      o.coopMissileBlocksDiscipline=got.includes('stage_clear_6')&&got.includes('stage_nodeath_6')&&!got.includes('stage_nomissile_6');

      achievementState=achievementEmpty();run.stage=1;diffKey='hard';let foe={_fightClock:{seconds:90}};
      got=achievementEncounterDefeat(foe,'boss');
      o.hardBossAndTier=got.includes('boss_hard_1')&&got.includes('stage1_boss_under_120')&&!got.includes('stage1_boss_under_60');
      o.encounterDedupe=achievementEncounterDefeat(foe,'boss').length===0;
      foe={_fightClock:{seconds:40}};diffKey='normal';got=achievementEncounterDefeat(foe,'boss');
      o.fastTierExclusive=got.includes('stage1_boss_under_60')&&!got.includes('stage1_boss_under_120');
      foe={_fightClock:{seconds:80}};got=achievementEncounterDefeat(foe,'miniboss');
      o.minibossTimer=got.join(',')==='stage1_miniboss_under_120';
      run.stage=2;diffKey='furious';got=achievementEncounterDefeat({_fightClock:{seconds:500}},'boss');
      o.furiousBoss=got.join(',')==='boss_furious_2';

      achievementState=achievementEmpty();run.pilot='decker';run.mode='arcade';run.contUsed=0;diffKey='normal';got=achievementRunComplete();
      o.runClear=got.includes('campaign_clear_decker')&&got.includes('run_no_continue')&&achievementPoints()===1100;
      achievementState=achievementEmpty();run.contUsed=2;got=achievementRunComplete();
      o.continueBlocksAward=got.join(',')==='campaign_clear_decker'&&!achievementUnlocked('run_no_continue');
      achievementState=achievementEmpty();
      o.weaponThreshold=!achievementWeaponMax(3,4)&&achievementWeaponMax(3,5)&&achievementUnlocked('weapon_max_laser')&&!achievementWeaponMax(3,5);
      o.runtimeHooks=computeStageResults.toString().includes('achievementStageComplete')&&
        triggerVictory.toString().includes('achievementRunComplete')&&bossDie.toString().includes('achievementEncounterDefeat')&&
        hitSubBoss.toString().includes("achievementEncounterDefeat(b,'miniboss')")&&applyPowerup.toString().split('achievementWeaponMax').length===3;
      return JSON.stringify(o);
    }finally{
      localStorage.getItem=save.get;localStorage.setItem=save.set;localStorage.removeItem=save.remove;
      achievementState=save.state;achievementLastUnlock=save.last;achievementSteamQueue=save.queue;
      run.mode=save.mode;run.pilot=save.pilot;run.stage=save.stage;run.contUsed=save.contUsed;diffKey=save.diff;coopOn=save.coop;
    }
  })()`,ctxv));
  for(const k of Object.keys(out))ok(out[k],'Achievement registry: '+k);
  return out;
};
