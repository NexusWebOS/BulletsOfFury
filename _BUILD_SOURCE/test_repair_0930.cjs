module.exports=function(vm,ctxv,ok,nativePlayerHit){
 const fs=require('fs'),path=require('path');
 for(const f of ['fusion_art_0930.js','fusion_0930.js','repair_art_0930.js','repair_0930.js','encounter_art_0930.js','encounters_0930.js'])
  vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== 380. Fusion overload, upgrade previews, modular replacements and fitted art ===');
 for(const pack of ['fusion_0930','repair_0930','encounters_0930']){
  const data=JSON.parse(fs.readFileSync(path.join(__dirname,'..',vm.runInContext('bofAssetPath('+JSON.stringify('assets/game/'+pack+'/manifest.json')+')',ctxv))));
  for(const [name,a] of Object.entries(data)){
   const p=path.join(__dirname,'..',a.path),png=fs.readFileSync(p),w=png.readUInt32BE(16),h=png.readUInt32BE(20);
   ok(a.frames.every(r=>r[0]>=0&&r[1]>=0&&r[2]>0&&r[3]>0&&r[0]+r[2]<=w&&r[1]+r[3]<=h),pack+'/'+name+' atlas rectangles are in bounds');
  }
 }
 ctxv.__repairRealHit=nativePlayerHit;
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={};const savedHit=playerHit;playerHit=__repairRealHit;ht27Stop();debugFight=null;coopOn=false;diffKey='furious';DIFF=DIFFS.furious;run.mode='campaign';run.pilot='yuri';
  function setup(){beginStage(5);setState(GS.PLAY);story=null;special=null;player.reset();player.out=false;gravityMode.phase='active';run.spaceMode=true;run.spaceWeapon=1;run.spaceLevels=[3,3,3];enemies=[];pBullets=[];eBullets=[];powerups=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;}
  setup();o['space slot uses Fusion name and tier icon']=spaceWeaponName()==='FUSION CANNON'&&spaceWeaponIconKey()==='space_fusion_icon_3';
  for(const [p,z]of [[100,1],[150,1.5],[199,2]]){pBullets=[];spaceShadowRelease(FUSION30_FULL*p/100);const b=pBullets.find(b=>b.kind==='spaceFusion');o[p+' percent safely releases the correct size']=!!b&&b.scale===z&&!player.dead;}
  for(const stage of [5,9]){setup();run.stage=stage;run.shield=5;player.invuln=99;run._spaceShadowHeld=true;run._spaceShadowCharge=FUSION30_FULL*1.99;const before=stageStats.deaths;spaceShadowTick(.02,true);const once=stageStats.deaths;spaceShadowTick(.5,true);
   o['stage '+stage+' overload kills once through protection']=player.dead&&once===before+1&&stageStats.deaths===once&&run.shield===0&&run.spaceWeapon===0&&!pBullets.some(b=>b.kind==='spaceFusion');}
  setup();run.stage=4;run.spaceMode=false;
  const save={weapon:run.weapon,level:run.wlevel,forge:run.forge};let levels=[];
  for(const lv of [1,2,3,4,5]){const P=forgePreviewNew(3,'ice',lv);forgePreviewSwap(P,240,300,()=>levels.push([run.wlevel,run.forge[3].lv,run.infusion.lv]));}
  o['all preview tiers reach the real weapon, forge and infusion']=levels.every((a,i)=>a.every(n=>n===i+1));
  o['preview restores the live loadout']=run.weapon===save.weapon&&run.wlevel===save.level&&run.forge===save.forge;
  const e=spawnEnemy('s4interceptor',240,180,{});e._esh=null;e._noHit=false;e._r30.left.hp=1;_dmgBullet={x:e.x-e.w*.4,y:e.y,kind:'mg',lv:3};hitEnemy(e,2);_dmgBullet=null;
  o['destroyed jet module stops only its own muzzle']=e._r30.left.hp===0&&modularJetPoint(e,-1)._disabled&&!modularJetPoint(e,1)._disabled;
  o['neutral hits stay white; weakness hits use the opposing element']=hitFlashColor({})==='#ffffff'&&hitFlashColor({_hitFlashColor:'#ff3b30'})==='#ff3b30'&&hitFlashColor({_hitFlashColor:'#83d9ff'})==='#83d9ff';
  run.stage=5;run.spaceMode=true;powerups=[];spaceArmorySpawnBox(200,200,'spacehelper');o['explicit stage5 helper reward is rerolled']=powerups.length===1&&powerups[0]._hqReward!=='spacehelper';
  for(const route of ['HAMMER','HAMA']){ht27Stop();setState(GS.PASSWORD);pwInput=route;submitPassword();startRun(5);boss.hp=boss.maxhp*.5;boss._noHit=false;boss.enter=false;
   const d=boss._hammerTime;d.mode='attack';d.locked=false;d.shield=false;d.clock=40;d.attack=0;if(d.hama)d.hama.attacks=0;const states=[];
   for(let i=0;i<(d.hama?16:8);i++){ht27Attack(boss,d);if(d.mode==='attack')states.push(boss._hammer.state);}
   o[route+' exposes all eight combat families']=['warn','spin','whirl_warn','curl','spell','chain_warn','storm_raise','mega_charge'].every(s=>states.includes(s));
   hammerStormStart(boss);o[route+' recovery is protected from a music cut']=ht27CombatSequence(boss);}
  ht27Stop();
  playerHit=savedHit;return o;
 })())`,ctxv));
 for(const [name,pass]of Object.entries(out))ok(pass,name);
};
