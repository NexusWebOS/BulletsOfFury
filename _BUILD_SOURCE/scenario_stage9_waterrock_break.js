async () => {
  beginStage(9); setState(GS.PLAY); player.reset(); player.invuln=1e9;
  player.x=worldWidth()/2; player.y=VH-55; snapCamToPlayer(); gravityModeStart(); gravityMode.phase='active';
  enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0; s9WaterReset();
  stagePlan=[]; waveIdx=999; subBossTriggered=true; subBossDone=true; bossWarned=true;
  const rock=spawnEnemy('riftrock',worldWidth()/2,300,{}); rock.x=worldWidth()/2; rock.y=300;
  window.__s9RockFrames=0; window.__qaTick=()=>{
    window.__s9RockFrames++; if(window.__s9RockFrames===42 && !rock.dead) killEnemy(rock);
  };
  const keys=['nst9_voidwater_master','ngm_ship_0','ns9_comet_lg0_0','ns9_comet_md0_0'];
  for(let i=0;i<8;i++)keys.push('ns9fx_water_'+i);
  await new Promise(resolve=>{ const until=performance.now()+20000; const poll=()=>{
    if(keys.every(k=>XART.rdy(k))||performance.now()>until)resolve();else setTimeout(poll,50);
  };poll(); });
}
