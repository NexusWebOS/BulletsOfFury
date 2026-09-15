module.exports=function(vm,ctxv,ok){
  console.log('=== 316. Frost Cruiser charged full-viewport sweep ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={sub:subBoss,active:subBossActive,run:{stage:run.stage},curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      warn:combatWarningTick,beamAudio:jungleCruiserBeamAudio,hit:playerHit,crackle:Audio.SFX.crackle,
      px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln};var o={};
    try{
      run.stage=3;curStage=STAGES[2];diffKey='normal';DIFF=DIFFS.normal;player.x=100;player.y=390;player.dead=false;player.invuln=1e9;
      var warns=0,crackles=0,hits=0,audio=[];combatWarningTick=function(owner,id,elapsed,dur){if(id==='frost-cruiser-sweep'&&dur===3)warns++;};
      jungleCruiserBeamAudio=function(b,on){audio.push(on?'start':'end');b._jc.beamSound=on;};Audio.SFX.crackle=function(){crackles++;};
      playerHit=function(){if(player.invuln>0)return;hits++;player.invuln=60;};
      spawnSubBoss('frostcruiser');var b=subBoss;b.enter=false;b.x=worldWidth()/2;b.y=shipBossStationY(b);b._drawY=b.y;
      jungleCruiserSetState(b,'beamCharge');var J=b._jc,dir=J.beamDir,locked=J.beamAng;
      for(var i=0;i<170;i++){if(i===20)player.x=worldWidth()-80;jungleCruiserDirector(b,1/60);}
      o.threeSecondTell=J.state==='beamCharge'&&J.t>2.8&&warns===170;
      o.committed=dir===1&&J.beamDir===dir&&Math.abs(J.beamAng-locked)<.001;
      for(;J.state==='beamCharge'&&i<220;i++)jungleCruiserDirector(b,1/60);
      var angles=[],guard=0;while(J.state==='beamSweep'&&guard++<400){jungleCruiserDirector(b,1/60);angles.push(J.beamAng);}
      o.singleSweep=angles.length>280&&angles.length<330&&angles.every(function(a,k){return !k||a>=angles[k-1]-1e-9;});
      o.fullViewport=angles[0]<-.76&&Math.max.apply(null,angles)>.76;
      o.recovers=J.state==='recover'&&guard<400;
      o.crackleCadence=crackles>=10&&crackles<=12;
      o.audio=audio.join(',')==='start,end';
      J.state='beamSweep';J.beamActive=true;J.beamAng=0;b.x=worldWidth()/2;b.y=shipBossStationY(b);player.x=b.x;player.y=b.y+180;player.invuln=0;jungleCruiserBeamHit(b);
      o.contact=hits===1;
      spawnSubBoss('junglecruiser');var j=subBoss;j.enter=false;j.x=worldWidth()/2;j.y=shipBossStationY(j);jungleCruiserSetState(j,'beamCharge');
      for(var n=0;n<80&&j._jc.state==='beamCharge';n++)jungleCruiserDirector(j,1/60);
      o.jungleUntouched=j._jc.state==='beamSweep'&&n<80;
      return JSON.stringify(o);
    }finally{subBoss=save.sub;subBossActive=save.active;run.stage=save.run.stage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      combatWarningTick=save.warn;jungleCruiserBeamAudio=save.beamAudio;playerHit=save.hit;Audio.SFX.crackle=save.crackle;
      player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Frost Cruiser sweep: '+k);
  ok(vm.runInContext(`FROST_BEAM_WIDTH===42*1.25&&FROST_BEAM_CHARGE===COMBAT_WARNING_SECONDS`,ctxv),'Frost beam visual/collision width is exactly 25% larger and uses the shared warning clock');
  ok(vm.runInContext(`jungleCruiserDrawUnder.toString().includes("cfx_stage4_chain_lightning")&&jungleCruiserDrawUnder.toString().includes("rgba(1,5,13")`,ctxv),'charge draw uses authored crackling lightning over a darkened arena');
};
