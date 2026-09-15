module.exports=function(vm,ctxv,ok){
  console.log('=== 311. Jungle Overlord-X gauge entrance ===');
  const result=JSON.parse(vm.runInContext(`(function(){
    var save={boss:boss,bossActive:bossActive,run:{mode:run.mode,stage:run.stage},curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      music:Audio.startMusic,blip:Audio.SFX.blip,select:Audio.SFX.select};var out={},music=[],blips=0,selects=0;
    try{
      run.mode='campaign';run.stage=1;curStage=STAGES[0];diffKey='normal';DIFF=DIFFS.normal;
      Audio.startMusic=function(k){music.push(k);};Audio.SFX.blip=function(){blips++;};Audio.SFX.select=function(){selects++;};
      spawnBoss('damkeeper');out.spawn=boss.enter&&boss._noHit&&boss._ovIntro.phase==='approach'&&!bossHealthVisible(boss);
      var hp=boss.hp;hitBoss(999);out.invulnerable=boss.hp===hp&&!bossHitTest(boss.x,boss.y);
      for(var i=0;i<104;i++)updateBoss(1/60);out.fade=boss._ovIntro.phase==='fade'&&bossHealthVisible(boss)&&bossHealthFraction(boss)===0&&bossHealthAlpha(boss)<1;
      for(var j=0;j<31;j++)updateBoss(1/60);var early=bossHealthFraction(boss);
      for(var k=0;k<70;k++)updateBoss(1/60);var late=bossHealthFraction(boss);out.fill=boss._ovIntro.phase==='fill'&&late>early&&late<1;
      for(var q=0;q<80;q++)updateBoss(1/60);out.done=boss._ovIntro.done&&!boss.enter&&!boss._noHit&&bossHealthFraction(boss)===1;
      out.chimes=blips===8&&selects===1;out.music=music.length===1&&music[0]==='boss1';
      updateBoss(1/60);out.fight=boss._ovInit===1&&boss._ovState==='fight';
      return JSON.stringify(out);
    }finally{boss=save.boss;bossActive=save.bossActive;run.mode=save.run.mode;run.stage=save.run.stage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;Audio.startMusic=save.music;Audio.SFX.blip=save.blip;Audio.SFX.select=save.select;}
  })()`,ctxv));
  for(const k of Object.keys(result))ok(result[k],'Overlord gauge intro: '+k);
  ok(vm.runInContext(`drawHealthBarV2.toString().includes('bossHealthAlpha')`,ctxv),'shared boss-bar renderer owns the entrance fade');
};
