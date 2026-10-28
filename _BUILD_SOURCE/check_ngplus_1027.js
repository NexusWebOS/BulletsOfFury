()=>{
 const checks={},ratios=[],notes=[];const ok=(name,v)=>checks[name]=!!v;
 function boot(stage,role,kind,ng){diffKey='furious';debugStartFight({stage,role,kind},{pilot:'cole'});run.ngplus=ng;
  if(role==='mini')spawnSubBoss(kind);else spawnBoss(kind);BOFCinematicDirector.cancel();setState(GS.PLAY);return role==='mini'?subBoss:boss;}
 const jobs=[[1,'mini','razorback'],[1,'boss','damkeeper'],[2,'mini','magmaward'],[2,'boss','infernoreaver'],[3,'boss','cryospear'],[3,'mini','rimewall'],[4,'boss','stormsovereign'],[5,'boss','chromehammer'],[6,'mini','siegebomber'],[6,'boss','warhive'],[6,'boss','rebelsquad'],[7,'mini','dualscoopdredger'],[7,'boss','sludgeemperor'],[8,'mini','heralddeath'],[8,'boss','vileexistence'],[9,'mini','voidhorizon'],[9,'boss','tidalfusion']];
 function values(b){if(b._s7mod)return {hull:b.maxhp,core:b._s7mod.coreMax,part:b._s7mod.parts[0].max};
  if(b._r30)return {hull:b.maxhp,copy:j3State(b).max[8],arm:b.parts.find(p=>p.id!=='core')?.maxhp};
  if(b._hammer)return {hull:b.maxhp,hammer:b._hammer.hammerMax,chain:b._hammer.chainMax};
  if(b._whv)return {hull:b.maxhp,ace:b._whv.aceMax,core:b._whv.coreMax};
  if(b._rebels)return {hull:b.maxhp,ship:b._rebels.ships[0].maxhp||b._rebels.ships[0].max};
  return {hull:b.maxhp,part:b.parts?.find(p=>p.maxhp)?.maxhp};}
 for(const [stage,role,kind]of jobs){let b=boot(stage,role,kind,false);if(stage===7)s7mInit(b);const a=values(b);
  b=boot(stage,role,kind,true);if(stage===7)s7mInit(b);const z=values(b),r={stage,role,kind,base:a,ng:z,ratios:{}};
  for(const k of Object.keys(a))if(a[k]>0&&z[k]>0)r.ratios[k]=z[k]/a[k];ratios.push(r);
  ok(kind+'-health25',Object.keys(r.ratios).every(k=>Math.abs(z[k]-a[k]*1.25)<=1));
 }
 run.ngplus=false;let e=spawnEnemy('s6dart',180,100),base=e.hp;
 run.ngplus=true;e=spawnEnemy('s6dart',180,100);ok('ordinary-enemy-health25',Math.abs(e.hp/base-1.25)<.00001);ok('enemy-has-element',!!NG27_ART[e._ng27Element]);
 const alias={hp:10,maxhp:10,max:10};ng27Health(alias);ng27Health(alias);
 ok('health-aliases-scale-once',alias.hp===12.5&&alias.maxhp===12.5&&alias.max===12.5);
 const q=eShootT(e.x,e.y,Math.PI/2,3,'mg',{owner:e});ok('native-shot-element-and-physics',q._ng27Shot&&q._el===e._ng27Element&&q.vy>0&&q.kind==='mg');
 ok('ordinary-bullet-stays-unshootable',!enemyOrdnanceCanIntercept(q));
 const missile=eShootT(e.x,e.y,Math.PI/2,3,'emissile',{owner:e});ok('missile-retains-native-owner',!missile._ng27Shot&&enemyOrdnanceCanIntercept(missile));
 run.forgeForms={};run.forge={};run.forgeElems={};run._respecBase23=true;ensureForgeForms();
 ok('all-nine-dark-forms-free',FORGE_WEAPONS.every(w=>run.forgeForms[w]?.dark?.lv===1));
 ok('dark-is-discovered',run.forgeElems.dark===1);
 const selections=[];for(const w of FORGE_WEAPONS){run.weapon=w;selections.push(forgeSelect(w,'dark')==='ok'&&run.infusion?.elem==='dark');}
 ok('all-nine-select-and-infuse',selections.every(Boolean));
 run.stage=1;ok('ngplus-weapon-family-unlocks',laserMistIsUnlocked()&&chaingunIsUnlocked()&&yuriLightningOrbIsUnlocked());
 ok('ngplus-loadout-has-earned-late-weapons',crateWeaponPool(true).includes(6));
 run.forge={};ok('unused-free-arsenal-does-not-offer-paid-respec',!hf23HasForms());
 delete run._forgeBudget23;campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A'};campaign.unlockedMax=6;run.mode='campaign';run.stage=6;
 const budget=hf23Budget();ok('free-dark-does-not-spend-upgrade-points',budget.spent===0&&run.forgeCombos===10);
 run.weapon=0;run.ngplus=false;let a=elementalDamageResult({type:'neutral'},'enemy',{kind:'mg'},10,100,100).dmg;
 run.ngplus=true;let z=elementalDamageResult({type:'neutral'},'enemy',{kind:'mg'},10,100,100).dmg;ok('player-damage12',Math.abs(z/a-1.12)<.00001);
 ok('maverick-homing-stats-fixed',elementalDamageResult({type:'neutral'},'enemy',{kind:'mavlaser'},10,100,100).dmg===a);
 const c={mode:'fight',cd:2,fireCd:1,t:4,warning:{t:.2,tell:1},recover:{state:'recover',t:1}};
 const clocks=ng27Clocks(c);c.cd-=.02;c.fireCd-=.02;c.t+=.02;c.warning.t+=.02;c.recover.t+=.02;ng27Advance(clocks);
 ok('attack-countdown15',Math.abs(c.cd-(2-.02*1.15))<1e-9&&Math.abs(c.fireCd-(1-.02*1.15))<1e-9);
 ok('recovery-clock15',Math.abs(c.recover.t-(1+.02*1.15))<1e-9);ok('warning-and-scene-clocks-unchanged',c.t===4.02&&c.warning.t===.22);
 const warned={mode:'fight',child:{phase:'warn',cd:1,t:.2}};const pausedClocks=ng27Clocks(warned);warned.child.cd-=.02;warned.child.t+=.02;ng27Advance(pausedClocks);
 ok('warning-countdowns-remain-native',warned.child.cd===.98&&warned.child.t===.22);
 const saved=NG27.base.reward;let rewards=0;NG27.base.reward=()=>rewards++;bossDefeated=false;ap10StageXReward();bossDefeated=true;ap10StageXReward();NG27.base.reward=saved;ok('stagex-requires-defeat',rewards===1);
 const rewardResults=[];
 for(const route of ['left','right']){
  boot(6,'boss',route==='left'?'warhive':'rebelsquad',false);run.mode='campaign';run._gp4StageX=route;run._ap10XReward=false;
  campaign.stageX1004={route,done:false};run._forgeBudget23={v:1,cleared:[1,2,3,4,5,6],spent:0,reset:0};run.forgeCombos=12;run.lives=3;run.bombs=2;
  bossDefeated=true;boss.dead=true;boss.hp=0;
  FS11.proof={route,kind:boss.kind,ref:boss};FS11.receipt=null;
  ap10StageXReward();const first={combos:run.forgeCombos,lives:run.lives,bombs:run.bombs,tier:run.missileTier,bonus:hf23Budget().bonus27,mk2:fs11Enhanced()};
  ap10StageXReward();const same=run.forgeCombos===first.combos&&run.bombs===first.bombs&&run.lives===first.lives;
  rewardResults.push({route,...first,same});ok('stagex-'+route+'-reward-once',same&&first.combos===13&&first.lives===4&&first.bombs>=12&&first.mk2&&first.bonus===1);
 }
 notes.push({rewardResults});run.ngplus=true;
 const snap=campSnapshot();ok('campaign-save-retains-ngplus',snap.ngplus===true);run.ngplus=false;
 const applied=campApply(snap);ok('save-load-keeps-ngplus-and-dark',applied&&run.ngplus&&FORGE_WEAPONS.every(w=>forgeFormsFor(w).dark));
 ok('stagex-bonus-survives-save',run.forgeCombos===13&&hf23Earned()===13);
 // A real earned campaign receipt opens NG+, and debug fights cannot create one.
 const receipt=P2M.receipt,proof=P2M.proof,finale=run._trueFinaleCleared;
 P2M.receipt=null;P2M.proof={stages:[1,2,3,4,5,6,7],pilot:run.pilot};run.mode='campaign';run.stage=8;run._trueFinaleCleared=false;
 ok('debug-fight-does-not-unlock-ngplus',!bonusModesUnlockFromCampaign()&&!bonusModesAreUnlocked());
 run._trueFinaleCleared=true;ok('final-clear-unlocks-ngplus',bonusModesUnlockFromCampaign()&&bonusModesAreUnlocked());
 P2M.receipt=receipt;P2M.proof=proof;run._trueFinaleCleared=finale;
 run.ngplus=false;
 const f={mode:'fight',cd:2};const before=NG27.events.length;ok('normal-campaign-disabled',!ng27On());
 run.ngplus=true;for(const a of Object.values(NG27_ART))XART.rdy(a.key);
 return {checks,ratios,notes};
}
