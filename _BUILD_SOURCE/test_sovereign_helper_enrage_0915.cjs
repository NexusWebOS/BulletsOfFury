module.exports=function(vm,ctxv,ok){
  console.log('=== 326. Sovereign generator-hit helper enrage ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={boss:boss,active:bossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      bullets:eBullets,pb:pBullets,en:enemies,plan:stagePlan,px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln};var o={};
    function spawn(k){run.stage=4;curStage=STAGES[3];diffKey=k;DIFF=DIFFS[k];stagePlan=[];enemies=[];pBullets=[];eBullets=[];
      player.x=worldWidth()*.5;player.y=650;player.dead=false;player.invuln=999;spawnBoss('stormsovereign');var b=boss;
      b.enter=false;b.x=worldWidth()/2;b.y=b._s4war.homeY;b._drawY=b.y;b.fireCd=999;bossActive=true;
      stage4CoreTurretSpawnMissing(b,.5);for(var t of b._s4war.coreTurrets){t.spawnT=1;t.materialize=1;}return b;}
    function hitNode(b,n){b._s4ShieldHit=n;return stage4ShieldAbsorbHit(b,1,n.x,n.y);}
    try{
      var b=spawn('normal'),S=b._s4war,n=S.shield.nodes[0];hitNode(b,n);
      o.normalNoRage=!S.coreEnrage&&S.coreEnrageCount===0&&S.coreTurrets.every(t=>!t.rage);
      b=spawn('hard');S=b._s4war;n=S.shield.nodes[0];hitNode(b,n);
      o.hardTrigger=!!(S.coreEnrage&&S.coreEnrage.active)&&S.coreEnrageCount===1&&S.coreEnrage.dur===5.6;
      o.redState=S.coreTurrets.every(t=>t.rage&&t.state==='rage'&&t.rageFrom);
      stage4CoreEnrageTick(b,.25,2);var t0=S.coreEnrage.t;hitNode(b,n);
      o.oncePerNode=S.coreEnrageCount===1&&S.coreEnrage.t===t0&&n._coreRageTriggered;
      for(var i=0;i<32;i++)stage4CoreEnrageTick(b,1/60,2);
      var left=S.coreTurrets.find(t=>t.side<0),right=S.coreTurrets.find(t=>t.side>0);
      o.sideStations=S.coreEnrage.mode==='fire'&&left.x<camLeftX()+90&&right.x>camRightX()-90&&left.y>270&&right.y>270;
      o.facesInward=Math.cos(left.ang)>0&&Math.cos(right.ang)<0;
      for(i=0;i<120;i++)stage4CoreEnrageTick(b,1/60,2);
      var rage=eBullets.filter(x=>x._s4CoreRage),sides=new Set(rage.map(x=>x._s4CoreSide));
      o.staggeredStreams=rage.length>20&&sides.has(-1)&&sides.has(1)&&rage.every(x=>x._s4RageLane===x._s4CoreSide);
      o.gapWindows=S.coreEnrage.gaps>=4&&S.coreEnrageGapWindows>=4;
      o.offsetLanes=Math.max.apply(null,rage.filter(x=>x._s4CoreSide<0).map(x=>x.ang||Math.atan2(x.vy,x.vx)))<
                    Math.min.apply(null,rage.filter(x=>x._s4CoreSide>0).map(x=>x.ang||Math.atan2(x.vy,x.vx)));
      for(i=0;i<300&&S.coreEnrage;i++)stage4CoreEnrageTick(b,1/60,2);
      o.cleanExit=!S.coreEnrage&&S.coreFormationMode==='home'&&S.coreTurrets.every(t=>!t.rage&&t.state==='windup');
      b=spawn('furious');S=b._s4war;n=S.shield.nodes[1];hitNode(b,n);o.furiousDuration=S.coreEnrage&&S.coreEnrage.dur===6.8;
      S.coreTurrets[0].dead=true;stage4CoreEnrageEnd(b);n=S.shield.nodes[2];hitNode(b,n);
      o.survivorCanRage=!!S.coreEnrage&&S.coreTurrets.filter(t=>!t.dead).every(t=>t.rage);
      return JSON.stringify(o);
    }finally{boss=save.boss;bossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      eBullets=save.bullets;pBullets=save.pb;enemies=save.en;stagePlan=save.plan;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Sovereign helper enrage: '+k);
};
