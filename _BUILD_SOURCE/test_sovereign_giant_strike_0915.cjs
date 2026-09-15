module.exports=function(vm,ctxv,ok){
  console.log('=== 329. Sovereign Furious giant lightning strike ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={boss:boss,active:bossActive,runStage:run.stage,runShield:run.shield,curStage:curStage,diffKey:diffKey,DIFF:DIFF,bullets:eBullets,pb:pBullets,en:enemies,plan:stagePlan,px:player.x,py:player.y,pdead:player.dead,palive:player.alive,pinv:player.invuln};var o={};
    function spawn(k){run.stage=4;curStage=STAGES[3];diffKey=k;DIFF=DIFFS[k];stagePlan=[];enemies=[];pBullets=[];eBullets=[];run.shield=3;player.x=worldWidth()*.5;player.y=VH-62;player.dead=false;player.alive=true;player.invuln=0;
      spawnBoss('stormsovereign');var b=boss;b.enter=false;b.x=worldWidth()/2;b.y=b._s4war.homeY;b._drawY=b.y;b.fireCd=999;bossActive=true;return b;}
    try{
      var n=spawn('normal');o.normalExcluded=!stage4GiantStrikeStart(n)&&!n._s4war.giantStrike;
      var h=spawn('hard');o.hardExcluded=!stage4GiantStrikeStart(h)&&!h._s4war.giantStrike;
      var b=spawn('furious'),S=b._s4war;o.starts=stage4GiantStrikeStart(b)&&S.mode==='giantStrike'&&S.giantStrikeCount===1;
      var G=S.giantStrike,R=stage4GiantStrikeBounds();o.safeCorners=Math.abs(R.safe-(camRightX()-camLeftX())*.17)<.001&&R.left>camLeftX()&&R.right<camRightX();
      stage4GiantStrikeTick(b,2.0);o.yellow=stage4GiantStrikeColor(G)==='yellow'&&!G.released;
      stage4GiantStrikeTick(b,1.0);o.red=stage4GiantStrikeColor(G)==='red'&&G.redWarned&&!G.released;
      stage4GiantStrikeTick(b,1.999);o.fullFiveSeconds=!G.released&&G.t<5;
      player.x=R.viewLeft+R.safe*.5;stage4GiantStrikeTick(b,.002);o.cornerSafe=G.released&&S.giantStrikeHits===0;
      player.x=(R.left+R.right)*.5;stage4GiantStrikeTick(b,.02);stage4GiantStrikeTick(b,.10);o.centralHitsOnce=S.giantStrikeHits===1&&Object.keys(G.hitSeats).length===1;
      S.finalGuns='active';S.finalGunShot=-1;var before=eBullets.length;stage4WarfareBossTick(b,.016);o.gunsSuspended=eBullets.length===before;
      stage4GiantStrikeTick(b,G.active+G.recover);o.recovers=S.giantStrike===null&&S.mode==='burst';
      var drawSource=stage4GiantStrikeDraw.toString();o.authoredArt=drawSource.indexOf('bmfx_alert_')>=0&&drawSource.indexOf('cfx_stage4_chain_lightning')>=0&&drawSource.indexOf('s4w_lightning_ball_')>=0;
      o.noWhiteFlash=!/flashScreen\s*=/.test(stage4GiantStrikeTick.toString()+stage4GiantStrikeDraw.toString());
      return JSON.stringify(o);
    }finally{boss=save.boss;bossActive=save.active;run.stage=save.runStage;run.shield=save.runShield;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;eBullets=save.bullets;pBullets=save.pb;enemies=save.en;stagePlan=save.plan;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.alive=save.palive;player.invuln=save.pinv;}
  })()`,ctxv));for(const k of Object.keys(q))ok(q[k],'Sovereign giant lightning: '+k);
};
