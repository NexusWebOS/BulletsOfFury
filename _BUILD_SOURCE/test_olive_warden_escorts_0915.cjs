module.exports=function(vm,ctxv,ok){
  console.log('=== 323. Olive Warden solo encounter (October 1) ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={sub:subBoss,active:subBossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      bullets:eBullets,pb:pBullets,en:enemies,plan:stagePlan,px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln};var o={};
    function spawn(k){run.stage=4;curStage=STAGES[3];diffKey=k;DIFF=DIFFS[k];stagePlan=[];enemies=[];pBullets=[];eBullets=[];
      player.x=worldWidth()*.42;player.y=610;player.dead=false;player.invuln=999;spawnSubBoss('olivewarden');var b=subBoss;
      b.enter=false;b.x=worldWidth()/2;b.y=b._s4war.homeY;b._drawY=b.y;b.fireCd=999;subBossActive=true;return b;}
    try{
      for(const difficulty of ['easy','normal','hard','furious']){
        const b=spawn(difficulty),S=b._s4war;
        S.drones.push({role:'gunner',hp:100,dead:false});stage4MiniEscortEnsure(b);
        o[difficulty+' clears existing helper state']=S.drones.length===0&&!S.summoned;
        for(let i=0;i<600;i++)stage4MiniDirector(b,1/60);
        o[difficulty+' fights alone without resummoning']=S.drones.length===0&&!S.summoned;
        o[difficulty+' retains hull attacks']=eBullets.some(q=>!q._s4EscortRole);
        o[difficulty+' has no invisible escort shots']=eBullets.every(q=>!q._s4EscortRole);
      }
      return JSON.stringify(o);
    }finally{subBoss=save.sub;subBossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      eBullets=save.bullets;pBullets=save.pb;enemies=save.en;stagePlan=save.plan;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Olive Warden escorts: '+k);
};
