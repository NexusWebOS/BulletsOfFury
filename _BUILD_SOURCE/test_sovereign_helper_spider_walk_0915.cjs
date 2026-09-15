module.exports=function(vm,ctxv,ok){
  console.log('=== 327. Sovereign helper spider walk ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={boss:boss,active:bossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,bullets:eBullets,pb:pBullets,en:enemies,plan:stagePlan,px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln};var o={};
    function spawn(k){run.stage=4;curStage=STAGES[3];diffKey=k;DIFF=DIFFS[k];stagePlan=[];enemies=[];pBullets=[];eBullets=[];player.x=worldWidth()*.5;player.y=650;player.dead=false;player.invuln=999;
      spawnBoss('stormsovereign');var b=boss;b.enter=false;b.x=worldWidth()/2;b.y=b._s4war.homeY;b._drawY=b.y;b.fireCd=999;bossActive=true;stage4CoreTurretSpawnMissing(b,.5);for(var t of b._s4war.coreTurrets){t.spawnT=1;t.materialize=1;}return b;}
    function hit(b,n){b._s4ShieldHit=n;return stage4ShieldAbsorbHit(b,1,n.x,n.y);}
    try{
      var b=spawn('hard'),S=b._s4war,n0=S.shield.nodes[0],n1=S.shield.nodes[1];hit(b,n0);hit(b,n1);var R=S.coreEnrage;
      o.newNodeReacts=R&&R.walkActive&&R.reacts===1&&n1._coreRageTriggered;
      var minOff=0,maxOff=-999,upY=0,backY=0;
      for(var i=0;i<112;i++){stage4CoreEnrageTick(b,1/60,2);minOff=Math.min(minOff,R.walkOffset);if(i===100)upY=S.coreTurrets[0].y;}
      o.hardBounded=minOff>=-58.01&&minOff<-53&&R.walkSeenUp;
      o.edgePreserved=S.coreTurrets[0].x<camLeftX()+90&&S.coreTurrets[1].x>camRightX()-90;
      for(i=0;i<100;i++){stage4CoreEnrageTick(b,1/60,2);maxOff=Math.max(maxOff,R.walkOffset);if(i===60)backY=S.coreTurrets[0].y;}
      o.walksBack=R.walkSeenBack&&backY>upY+20;
      o.returnsBaseline=!R.walkActive&&Math.abs(R.walkOffset)<.001;
      hit(b,n0);o.retrigger=R.walkActive&&R.reacts===2&&R.walkT===0;
      for(i=0;i<55;i++)stage4CoreEnrageTick(b,1/60,2);
      var rage=eBullets.filter(x=>x._s4CoreRage),left=rage.filter(x=>x._s4CoreSide<0),right=rage.filter(x=>x._s4CoreSide>0);
      o.gapSurvives=left.length&&right.length&&S.coreEnrage.gaps>0&&Math.max.apply(null,left.map(x=>x.ang))<Math.min.apply(null,right.map(x=>x.ang));
      b=spawn('furious');S=b._s4war;n0=S.shield.nodes[0];hit(b,n0);hit(b,n0);R=S.coreEnrage;
      for(i=0;i<105;i++)stage4CoreEnrageTick(b,1/60,2);
      o.furiousBounded=R.walkDepth===72&&R.walkOffset>=-72.01&&R.walkOffset<-67;
      b=spawn('normal');S=b._s4war;n0=S.shield.nodes[0];hit(b,n0);hit(b,n0);o.normalIsolated=!S.coreEnrage&&S.coreEnrageCount===0;
      return JSON.stringify(o);
    }finally{boss=save.boss;bossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;eBullets=save.bullets;pBullets=save.pb;enemies=save.en;stagePlan=save.plan;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Sovereign spider walk: '+k);
};
