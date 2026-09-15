module.exports=function(vm,ctxv,ok){
  console.log('=== 328. Sovereign Hard/Furious chain lightning ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={boss:boss,active:bossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,bullets:eBullets,pb:pBullets,en:enemies,plan:stagePlan,px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln};var o={};
    function spawn(k){run.stage=4;curStage=STAGES[3];diffKey=k;DIFF=DIFFS[k];stagePlan=[];enemies=[];pBullets=[];eBullets=[];player.x=worldWidth()*.5;player.y=650;player.dead=false;player.invuln=999;
      spawnBoss('stormsovereign');var b=boss;b.enter=false;b.x=worldWidth()/2;b.y=b._s4war.homeY;b._drawY=b.y;b.fireCd=999;bossActive=true;stage4WarfareSetMode(b,'lightning');return b;}
    function at(b,t){b._s4war.t=t;stage4WarfareBossTick(b,0);}
    try{
      var b=spawn('normal'),S=b._s4war;at(b,1.13);var normalFirst=eBullets.filter(x=>x._s4ChainBolt);at(b,1.69);at(b,2.29);at(b,2.93);
      o.normalPreserved=normalFirst.length===2&&normalFirst[0]._s4ChainAngle===-.24&&normalFirst[1]._s4ChainAngle===.24&&S.chainBolts===5&&S.chainOrbs===1;
      var normalSpeed=Math.hypot(normalFirst[0].vx,normalFirst[0].vy),normalWidth=Math.max.apply(null,normalFirst.map(x=>Math.abs(x._s4ChainAngle)));
      b=spawn('hard');S=b._s4war;at(b,1.13);var hardFirst=eBullets.filter(x=>x._s4ChainBolt);at(b,1.69);at(b,2.29);at(b,2.93);
      o.hardDoubles=hardFirst.length===4&&S.chainBolts===9&&S.chainOrbs===1;
      o.hardWidens=Math.max.apply(null,hardFirst.map(x=>Math.abs(x._s4ChainAngle)))>normalWidth&&new Set(hardFirst.map(x=>x._s4ChainAngle)).size===4;
      o.hardFaster=Math.hypot(hardFirst[0].vx,hardFirst[0].vy)>normalSpeed;
      b=spawn('furious');S=b._s4war;at(b,.83);var furyFirst=eBullets.filter(x=>x._s4ChainBolt);at(b,1.19);at(b,1.63);at(b,2.03);at(b,2.41);at(b,2.79);
      var orbs=eBullets.filter(x=>x._s4ChainOrb),furyProfile=stage4SovereignChainProfile();
      o.furiousFaster=furyProfile.beats[0]<1&&Math.hypot(furyFirst[0].vx,furyFirst[0].vy)>Math.hypot(hardFirst[0].vx,hardFirst[0].vy);
      o.furiousWidest=Math.max.apply(null,furyFirst.map(x=>Math.abs(x._s4ChainAngle)))===.46;
      o.furiousBalls=orbs.length===3&&orbs.every(x=>x._shootable&&x._s4ChainOrbIndex>=0)&&S.chainOrbs===3;
      o.alternatingRacks=orbs[0]._s4wLift.side===-1&&orbs[1]._s4wLift.side===1&&orbs[2]._s4wLift.side===-1;
      at(b,3.35);o.fasterCycle=S.mode==='giantStrike'&&!!S.giantStrike;
      o.tagged=eBullets.filter(x=>x._s4ChainBolt).every(x=>x._s4ChainGroup>=0&&x._s4ChainAngle!=null);
      return JSON.stringify(o);
    }finally{boss=save.boss;bossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;eBullets=save.bullets;pBullets=save.pb;enemies=save.en;stagePlan=save.plan;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;}
  })()`,ctxv));for(const k of Object.keys(q))ok(q[k],'Sovereign chain lightning: '+k);
};
