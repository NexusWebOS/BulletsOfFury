/* Visual proof for the 0826 non-naval spacing pass.
   Starts from the measured Stage-4 tank / bomber / Dambreaker squeeze, lets the real separator
   solve it, then holds the solved positions while Chromium captures the actual game renderer. */
(() => {
  run.stage=4; curStage=STAGES[3];
  player.reset(); player.x=340; player.y=470; player.invuln=1e9; snapCamToPlayer();
  enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0;
  stagePlan=[]; waveIdx=999; stageTimer=12; spawnClock=9999;
  subBossTriggered=true; subBossDone=true; aminiTriggered=true; bossWarned=true;

  const tank=spawnEnemy('roadtank',200,419,{inPlace:1});
  tank.x=200; tank.y=419; tank._lvlY=levelSrcY()+tank.y; tank.shoots=false; tank.fireCd=999;

  const mini=spawnArsenalMini('dambreaker');
  mini.x=349; mini.y=258; mini.vy=0; mini.shoots=false; mini.fireCd=999;

  const bomber=spawnEnemy('s1jetBomber',244,380,{inPlace:1});
  bomber.x=244; bomber.y=380; bomber.vy=0; bomber.shoots=false; bomber.fireCd=999;

  const drone=spawnEnemy('mdrone',530,175,{inPlace:1,pattern:'sine',amp:26});
  drone.x=530; drone.y=175; drone.vy=0; drone.shoots=false; drone.fireCd=999;

  enemySeparate(1/60);
  for(const e of [tank,mini,bomber,drone]){
    const x=e.x, y=e.y;
    Object.defineProperty(e,'x',{configurable:true,get:()=>x,set:()=>{}});
    Object.defineProperty(e,'y',{configurable:true,get:()=>y,set:()=>{}});
    Object.defineProperty(e,'dead',{configurable:true,get:()=>false,set:()=>{}});
    Object.defineProperty(e,'hp',{configurable:true,get:()=>1e9,set:()=>{}});
  }
})();
