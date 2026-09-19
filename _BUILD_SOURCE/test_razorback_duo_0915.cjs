module.exports=function(vm,ctxv,ok){
  console.log('=== 330. Hard Razorback duo ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={sub:subBoss,active:subBossActive,done:subBossDone,triggered:subBossTriggered,
      runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,bullets:eBullets,pb:pBullets,
      en:enemies,plan:stagePlan,locks:playerLocks,px:player.x,py:player.y,pdead:player.dead,
      palive:player.alive,pinv:player.invuln,dmg:stageStats.dmgDealt};var o={};
    function spawn(k){run.stage=1;curStage=STAGES[0];diffKey=k;DIFF=DIFFS[k];stagePlan=[];enemies=[];
      pBullets=[];eBullets=[];playerLocks=[];player.x=worldWidth()*.5;player.y=VH-72;player.dead=false;
      player.alive=true;player.invuln=999;spawnSubBoss('razorback');subBossActive=true;return subBoss;}
    function ready(p){var R=p._rzb;R.state='guns';R.trans=0;R.pt=4;R.at=0;R.attack='suppression';
      R.tgt={x:p._rzb.homeX||p.x,y:VH*.27};p.x=R.tgt.x;p.y=R.tgt.y;R.a=0;R.hpSync=true;}
    try{
      var n=spawn('normal');o.normalSingle=!!n._rzb&&!n._rzbPair&&n.name==='RAZORBACK';
      var f=spawn('furious');o.furiousSeparate=!!f._rzb&&!f._rzbPair&&f._rzb.furious&&f.name==='FURIOUS RAZORBACK';
      var b=spawn('hard'),P=b._rzbPair,a=P&&P.actors;o.hardPair=!!P&&a.length===2&&!b._rzb&&b.name==='RAZORBACK DUO';
      o.fullIndependentHp=a.every(p=>p.maxhp===P.singleMax&&p.hp===P.singleMax)&&b.maxhp===P.singleMax*2;
      o.distinctHomes=Math.abs(a[0]._rzb.homeX-(camLeftX()+(camRightX()-camLeftX())*.28))<.01&&Math.abs(a[1]._rzb.homeX-(camLeftX()+(camRightX()-camLeftX())*.72))<.01;
      razorbackEnter(a[0],'guns');razorbackEnter(a[1],'guns');
      o.offsetAttackBooks=a[0]._rzb.attack!==a[1]._rzb.attack&&a[0]._rzb.attack==='suppression'&&a[1]._rzb.attack==='sonic';
      ready(a[0]);ready(a[1]);razorbackPairSync(b);
      var locks=retinaBossTargets(b);o.sixRetinaParts=locks.length===6&&locks.filter(t=>String(t._retinaId).startsWith('0:')).length===3&&locks.filter(t=>String(t._retinaId).startsWith('1:')).length===3;
      var L=rzbWorld(a[0],-57,96),R=rzbWorld(a[1],57,96),lh=a[0].hp,rh=a[1].hp;
      _dmgBullet=null;razorbackPairHit(b,11,L.x,L.y);o.leftOnly=a[0].hp<lh&&a[1].hp===rh&&b.hp===a[0].hp+a[1].hp;
      eBullets=[{_rzb:true,_rzbOwner:a[0],dead:false},{_rzb:true,_rzbOwner:a[1],dead:false}];
      razorbackClear(a[0]);o.projectileOwnership=eBullets[0].dead&&!eBullets[1].dead;
      o.gapNotSolid=!razorbackPairContact(b,(a[0].x+a[1].x)/2,a[0].y)&&razorbackPairContact(b,a[0].x,a[0].y);
      a[0]._rzb.attack='suppression';a[0]._rzb.at=0;a[0]._rzb.mgBeat=-1;
      a[1]._rzb.attack='sonic';a[1]._rzb.at=0;a[1]._rzb.beat=-1;
      eBullets=[];for(var i=0;i<95;i++)razorbackPairUpdate(b,1/60);
      o.independentPressure=eBullets.some(x=>x._rzbOwner===a[0])&&eBullets.some(x=>x._rzbOwner===a[1]);
      var alive=a[1].hp;a[0].dead=true;a[0].hp=0;a[0].dying=0;for(i=0;i<70;i++)razorbackPairUpdate(b,1/60);
      o.oneDeathContinues=a[0]._rzbGone&&!b.dead&&!a[1].dead&&a[1].hp===alive;
      for(const p of a){p._rzb.state='hull';p._rzb.trans=0;p._rzb.pools.hull=1;p._rzb.max.hull=1;p.hp=Math.max(1,p.hp);}
      a[1].dead=false;a[1]._rzbGone=false;a[1].hp=1;razorbackPairSync(b);_dmgBullet=null;
      razorbackPairHit(b,99,a[1].x,a[1].y);for(i=0;i<70;i++)razorbackPairUpdate(b,1/60);
      o.bothRequired=b.dead&&P.cleared&&a.every(p=>p._rzbGone);
      o.singleCompletion=b.dying===0&&b._deathFxStarted===true;
      return JSON.stringify(o);
    }finally{subBoss=save.sub;subBossActive=save.active;subBossDone=save.done;subBossTriggered=save.triggered;
      run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;eBullets=save.bullets;
      pBullets=save.pb;enemies=save.en;stagePlan=save.plan;playerLocks=save.locks;player.x=save.px;player.y=save.py;
      player.dead=save.pdead;player.alive=save.palive;player.invuln=save.pinv;stageStats.dmgDealt=save.dmg;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Hard Razorback duo: '+k);
};
