module.exports=function(vm,ctxv,ok){
  console.log('=== 321. Olive Warden Hard/Furious assault cycle ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={sub:subBoss,active:subBossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      bullets:eBullets,pb:pBullets,en:enemies,plan:stagePlan,px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln};var o={};
    function spawn(k){run.stage=4;curStage=STAGES[3];diffKey=k;DIFF=DIFFS[k];stagePlan=[];enemies=[];pBullets=[];eBullets=[];
      player.x=worldWidth()*.5;player.y=610;player.dead=false;player.invuln=999;spawnSubBoss('olivewarden');var b=subBoss;b.enter=false;b.x=worldWidth()/2;b.y=b._s4war.homeY;b._drawY=b.y;b.fireCd=999;subBossActive=true;return b;}
    function beats(k,mode,secs){var b=spawn(k),S=b._s4war;stage4WarfareSetMode(b,mode);eBullets=[];for(var t=0;t<secs;t+=1/60)stage4MiniDirector(b,1/60);return eBullets.filter(x=>x._s4Mini&&x._s4wKind==='machine').length;}
    try{
      var hardBurst=beats('hard','burst',1),normalBurst=beats('normal','burst',1);o.rapidSpread=hardBurst>normalBurst&&hardBurst>=20;
      var hardCenter=beats('hard','center',.72),normalCenter=beats('normal','center',.72);o.rapidCenter=hardCenter>normalCenter&&hardCenter>=18;
      var b=spawn('hard'),S=b._s4war,H,maxStep=0,prev={x:b.x,y:b.y},seen={},ramUnsafe=false,returnSafe=false,returnClears=false;
      for(var i=0;i<1250;i++){
        stage4MiniDirector(b,1/60);seen[S.mode]=1;var d=Math.hypot(b.x-prev.x,b.y-prev.y);if(d>maxStep)maxStep=d;prev={x:b.x,y:b.y};
        if(S.mode==='hardRam')ramUnsafe=ramUnsafe||!b._s4MiniSafe;
        if(S.mode==='hardReturn')returnSafe=returnSafe||!!b._s4MiniSafe;
        if(seen.hardReturn&&S.mode==='burst'&&!b._s4MiniSafe){returnClears=true;break;}
      }
      H=S.miniHard;o.sequence=['hardCircle','hardGlide','hardWarn','hardRam','hardReturn'].every(k=>seen[k]);
      o.circleShots=eBullets.some(x=>x._s4Mini&&x._s4wKind==='machine');
      o.ram=ramUnsafe&&S.miniRamCount===1;o.safeReturn=returnSafe&&returnClears;
      o.continuous=maxStep<28;
      o.upright=shipBossVisualPose.toString().indexOf('_s4war.poseRot')<0;
      b=spawn('hard');S=b._s4war;stage4MiniHardSet(b,'hardWarn');for(i=0;i<45;i++)stage4MiniDirector(b,1/60);var lane=S.miniHard.lane;player.x=80;for(i=0;i<20;i++)stage4MiniDirector(b,1/60);
      o.locked=S.miniHard.locked&&Math.abs(S.miniHard.lane-lane)<.001;
      o.sharedWarn=stage4MiniHardTick.toString().indexOf('combatWarningTick')>=0&&stage4MiniHardWarningDraw.toString().indexOf('combatWarningDraw')>=0;
      b=spawn('normal');S=b._s4war;for(i=0;i<1500;i++)stage4MiniDirector(b,1/60);o.normalIsolation=!S.miniHard&&!Object.keys(seen).some(function(k){return false;})&&!/^hard/.test(S.mode)&&S.miniRamCount===0;
      b=spawn('furious');S=b._s4war;stage4WarfareSetMode(b,'rockets');S.t=3.11;stage4MiniDirector(b,1/60);o.furiousInherits=S.mode==='hardCircle';
      o.returnCollisionGate=updatePlay.toString().indexOf('!subBoss._s4MiniSafe')>=0;
      return JSON.stringify(o);
    }finally{subBoss=save.sub;subBossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      eBullets=save.bullets;pBullets=save.pb;enemies=save.en;stagePlan=save.plan;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Olive Warden Hard assault: '+k);
};
