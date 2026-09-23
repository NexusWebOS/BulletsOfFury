module.exports=function(vm,ctxv,ok){
  console.log('=== 325. Sovereign Hard/Furious helper blockade ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={width:_wwCache[4],boss:boss,active:bossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      bullets:eBullets,pb:pBullets,en:enemies,plan:stagePlan,px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln};var o={};
    function spawn(k){_wwCache[4]=_levelCfg(4).plateW;run.stage=4;curStage=STAGES[3];diffKey=k;DIFF=DIFFS[k];stagePlan=[];enemies=[];pBullets=[];eBullets=[];
      player.x=280;player.y=650;player.dead=false;player.invuln=999;spawnBoss('stormsovereign');var b=boss;
      b.enter=false;b.x=worldWidth()/2;b.y=b._s4war.homeY;b._drawY=b.y;b.fireCd=999;bossActive=true;
      stage4ShieldSyncNodes(b);stage4CoreTurretSpawnMissing(b,.5);for(var t of b._s4war.coreTurrets){t.spawnT=1;t.materialize=1;}return b;}
    function fireCount(k,mode){var b=spawn(k),S=b._s4war;eBullets=[];for(var t of S.coreTurrets){t.state='fire';t.stateT=0;t.fireShot=0;t.mode=mode;t.burstLeft=4;t.aimTo=Math.PI/2;t.ang=Math.PI/2;}
      stage4CoreTurretTick(b,.40,2);return {count:eBullets.filter(x=>x._s4CoreSide).length,speed:eBullets.length?Math.hypot(eBullets[0].vx,eBullets[0].vy):0};}
    try{
      var b=spawn('normal'),S=b._s4war,normalShield=S.coreTurrets[0].maxShield;
      for(var i=0;i<270;i++)stage4CoreTurretTick(b,1/60,2);
      o.normalShield=normalShield===102;o.normalSocket=S.coreFormationMode==='socket'&&S.coreFormationMix===0;
      b=spawn('hard');S=b._s4war;o.hardShield=S.coreTurrets.every(t=>t.maxShield===Math.ceil(normalShield*1.5));
      for(i=0;i<210;i++)stage4CoreTurretTick(b,1/60,2);
      var left=S.coreTurrets.find(t=>t.side<0),right=S.coreTurrets.find(t=>t.side>0),center=(left.x+right.x)/2;
      o.socketCenters=S.coreTurrets.every(t=>Math.hypot(t.x-stage4CoreTurretTarget(b,t.side).x,t.y-stage4CoreTurretTarget(b,t.side).y)<3);
      o.threeTimesSize=Math.abs(S4H_SIZE-132*.8*3)<.001;
      player.x=520;for(i=0;i<45;i++)stage4CoreTurretTick(b,1/60,2);
      o.independentOfPlayer=Math.abs((left.x+right.x)/2-center)<1;
      o.completeHelpersInView=left.x-S4H_HALF>=camLeftX()-2&&right.x+S4H_HALF<=camRightX()+2;
      b=spawn('furious');S=b._s4war;var low=1e9,high=-1e9;
      for(i=0;i<360;i++){stage4CoreTurretTick(b,1/60,2);right=S.coreTurrets.find(t=>t.side>0);low=Math.min(low,right.y);high=Math.max(high,right.y);}
      o.furiousLevitates=high-low>65;o.furiousSideFire=Math.abs(right.ang-Math.PI)<.02;
      var normalDown=fireCount('normal','down'),hardDown=fireCount('hard','down'),furiousDown=fireCount('furious','down');
      o.fasterStraight=hardDown.count>normalDown.count&&furiousDown.count>hardDown.count;
      o.fasterRounds=hardDown.speed>normalDown.speed&&furiousDown.speed>hardDown.speed;
      var normalDiag=fireCount('normal','diag'),hardDiag=fireCount('hard','diag'),furiousDiag=fireCount('furious','diag');
      o.fasterDiagonal=hardDiag.count>normalDiag.count&&furiousDiag.count>=hardDiag.count;
      o.difficultyOnly=stage4CoreDifficulty().furious&&stage4CoreDifficulty().shieldMul===1.5;
      return JSON.stringify(o);
    }finally{_wwCache[4]=save.width;boss=save.boss;bossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      eBullets=save.bullets;pBullets=save.pb;enemies=save.en;stagePlan=save.plan;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Sovereign helper blockade: '+k);
};
