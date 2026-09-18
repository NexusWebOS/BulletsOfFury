module.exports=function(vm,ctxv,ok){
  console.log('=== 331. Furious Razorback hyper tank ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={sub:subBoss,active:subBossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      bullets:eBullets,pb:pBullets,en:enemies,plan:stagePlan,locks:playerLocks,px:player.x,py:player.y,
      pdead:player.dead,palive:player.alive,pinv:player.invuln};var o={};
    function spawn(k){run.stage=1;curStage=STAGES[0];diffKey=k;DIFF=DIFFS[k];stagePlan=[];enemies=[];pBullets=[];
      eBullets=[];playerLocks=[];player.x=worldWidth()*.5;player.y=VH-72;player.dead=false;player.alive=true;
      player.invuln=999;spawnSubBoss('razorback');subBossActive=true;return subBoss;}
    function ready(b,state,attack,t){var R=b._rzb;R.state=state;R.trans=0;R.pt=4;R.at=t||0;R.attack=attack;
      R.beat=-1;R.mgBeat=-1;R.tgt={x:b.x,y:b.y};R.a=0;R.turret=0;R.hpSync=true;b.y=140;}
    try{
      var n=spawn('normal'),nw=n.w;o.normalUnchanged=!!n._rzb&&!n._rzb.furious&&!n._rzb.scale&&n.name==='RAZORBACK';
      var h=spawn('hard');o.hardDuoUnchanged=!!h._rzbPair&&h._rzbPair.actors.every(p=>!p._rzb.furious&&!p._rzb.scale);
      var b=spawn('furious'),R=b._rzb;o.furiousSingle=!!R&&!b._rzbPair&&R.furious&&b.name==='FURIOUS RAZORBACK';
      o.fiftyPercentLarger=R.scale===1.5&&Math.abs(b.w/nw-1.5)<.02&&b.w===b.h;
      var nd=Math.hypot(rzbWorld(n,57,96).x-n.x,rzbWorld(n,57,96).y-n.y),fd=Math.hypot(rzbWorld(b,57,96).x-b.x,rzbWorld(b,57,96).y-b.y);
      o.hardpointsScale=Math.abs(fd/nd-1.5)<.001;
      o.fasterProjectiles=Math.abs(rzbPxFrame(240,b)/rzbPxFrame(240,n)-1.22)<.001;
      var nq={x:0,y:0,_rzb:{tgt:{x:1000,y:0},a:0,at:0,attack:'suppression',travel:{left:0,right:0}}},fq={x:0,y:0,_rzb:{tgt:{x:1000,y:0},a:0,at:0,attack:'suppression',travel:{left:0,right:0},speedMul:1.62,turnMul:1.55,furious:true,scale:1.5}};
      for(var i=0;i<60;i++){razorbackMove(nq,1/60);razorbackMove(fq,1/60);}o.hyperMovement=fq.x>nq.x*1.60&&fq._rzb.speedMul===1.62&&fq._rzb.turnMul===1.55;
      ready(b,'guns','sonic',1.21);eBullets=[];R.waves=[];razorbackCombat(b);
      o.furiousSonic=eBullets.length===9&&eBullets.every(x=>x.kind==='rzbSonic'&&x._rzbFurious)&&R.waves.length===1&&R.waves[0].furious&&R.waves[0].arc===1.05;
      o.segmentedWave=R.waves[0].segments.length===5&&R.waves[0].segments.every((q,i,a)=>q[0]<q[1]&&(!i||a[i-1][1]<q[0]))&&R.waves[0].life===6;
      ready(b,'hull','nova',1.56);eBullets=[];R.waves=[];razorbackCombat(b);o.hyperNova=eBullets.length===28&&R.waves.length===1&&R.waves[0].furious;
      ready(b,'guns','missiles',0);playerLocks=[];razorbackCombat(b);o.razorRack=playerLocks.length===1&&playerLocks[0].launches.length===14;
      ready(b,'guns','suppression',0);var g=rzbWorld(b,-57,96),edgeX=g.x+RZB_R.gun*1.25;
      o.scaledHitbox=razorbackPartAt(b,edgeX,g.y)==='left';
      var beam={x:edgeX,w:2,top:g.y-50,bot:g.y+50};o.scaledBeam=razorbackBeamHit(b,beam)!==null;
      var src=rzbSprite.toString()+razorbackWaveDraw.toString()+razorbackProjectileDraw.toString();o.authoredRedPanels=!!BOFX.img.rzbf_hull_0&&!!BOFX.img.rzbf_turret&&src.indexOf('xartPalette')<0;
      return JSON.stringify(o);
    }finally{subBoss=save.sub;subBossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      eBullets=save.bullets;pBullets=save.pb;enemies=save.en;stagePlan=save.plan;playerLocks=save.locks;player.x=save.px;
      player.y=save.py;player.dead=save.pdead;player.alive=save.palive;player.invuln=save.pinv;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Furious Razorback: '+k);
};
