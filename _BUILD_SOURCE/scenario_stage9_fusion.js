async () => {
  beginStage(9); setState(GS.PLAY); player.reset(); player.invuln=1e9;
  player.x=worldWidth()/2; player.y=VH-50; snapCamToPlayer(); gravityModeStart(); gravityMode.phase='active';
  enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0;
  stagePlan=[]; waveIdx=999; subBossTriggered=true; subBossDone=true; bossWarned=true;
  spawnBoss('tidalfusion'); boss.enter=false; boss._s9fusion.t=1.45;
  window.__s9FusionFrames=0;
  window.__qaTick=()=>{
    window.__s9FusionFrames++;
    if(window.__s9FusionFrames===75 && boss && boss._s9fusion && boss._s9fusion.phase==='twins'){
      boss._s9fusion.left.hp=2; s9FusionHit(boss,4);
    }
    if(window.__s9FusionFrames===150 && boss && boss._s9fusion && boss._s9fusion.phase==='twins'){
      boss._s9fusion.hit=boss._s9fusion.right;
      boss._s9fusion.right.hp=2; s9FusionHit(boss,4);
    }
  };
  const keys=['nst9_voidwater_master','ngm_ship_0','ns9_warpsen_intact','ns9_warpsen_damaged',
    'ns9_warpsen_critical','ns9_gatecore_0','ns9_tidal_intact'];
  await new Promise(resolve=>{ const until=performance.now()+20000; const poll=()=>{
    if(keys.every(k=>XART.rdy(k))||performance.now()>until)resolve();else setTimeout(poll,50);
  };poll(); });
}
