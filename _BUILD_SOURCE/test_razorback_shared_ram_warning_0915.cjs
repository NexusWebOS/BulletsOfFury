module.exports=function(vm,ctxv,ok){
  console.log('=== 333. Razorback shared body-ram warning ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={sub:subBoss,active:subBossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,bullets:eBullets,plan:stagePlan,locks:playerLocks,px:player.x,py:player.y,pdead:player.dead,palive:player.alive,pinv:player.invuln};var o={};
    function spawn(k){run.stage=1;curStage=STAGES[0];diffKey=k;DIFF=DIFFS[k];stagePlan=[];eBullets=[];playerLocks=[];player.x=worldWidth()*.24;player.y=VH-70;player.dead=false;player.alive=true;player.invuln=999;spawnSubBoss('razorback');subBossActive=true;var b=subBoss._rzbPair?subBoss._rzbPair.actors[0]:subBoss,R=b._rzb;R.state='guns';R.trans=0;R.attack='ram';R.at=.20;R.beat=-1;R.tgt={x:b.x,y:b.y};R.a=0;b.y=145;return b;}
    try{var n=spawn('normal'),R=n._rzb;razorbackCombat(n);var B=n._combatWarnings['razorback-body-ram'];o.green=B&&l23FovPhase(B.t/B.warm)==='green'&&!B.released;var lane=R.ramX;
      player.x=worldWidth()*.78;R.at=.40;razorbackCombat(n);o.yellow=R.ramLocked&&R.ramX===lane&&l23FovPhase(B.t/B.warm)==='yellow';player.x=worldWidth()*.08;R.at=.80;razorbackCombat(n);o.red=R.ramX===lane&&l23FovPhase(B.t/B.warm)==='red';R.at=1.01;razorbackCombat(n);o.release=B.released&&R.tgt.x===lane&&R.tgt.y===VH*.68;
      razorbackNext(n);o.reset=R.ramLocked===false;
      var h=spawn('hard'),H=h._rzb;razorbackCombat(h);o.hardPairLane=H.pairSide===-1&&H.ramX<worldWidth()*.5;
      var f=spawn('furious'),F=f._rzb;razorbackCombat(f);o.furious=F.furious&&f._combatWarnings['razorback-body-ram'].warm===1;
      var ds=razorbackDraw.toString(),cs=razorbackCombat.toString();o.sharedDraw=ds.includes('combatWarningDraw')&&!ds.includes("strokeStyle='rgba(255,200,36");o.sharedTick=cs.includes("combatWarningTick(b,'razorback-body-ram'");
      return JSON.stringify(o);
    }finally{subBoss=save.sub;subBossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;eBullets=save.bullets;stagePlan=save.plan;playerLocks=save.locks;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.alive=save.palive;player.invuln=save.pinv;}
  })()`,ctxv));for(const k of Object.keys(q))ok(q[k],'Razorback shared ram warning: '+k);
};
