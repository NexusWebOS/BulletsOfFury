() => {
  beginStage(7); setState(GS.PLAY); player.reset();
  player.x=worldWidth()/2; player.y=440; player.invuln=1e9;
  enemies.length=0; eBullets.length=0; pBullets.length=0;
  powerups.length=0; particles.length=0; explosions.length=0;
  stagePlan=[{t:9999,fn:function(){}}]; waveIdx=0; stageTimer=20; spawnClock=9999;
  boss=null; bossActive=false; spawnBoss('sludgeemperor');
  boss.enter=false; boss.x=worldWidth()/2; boss.y=178; boss.ty=178;
  boss._s7warden.final.phase='fight'; boss._s7warden.noHit=false;
  bossActive=true; s7WardenMode(boss,'chain');
  XART.rdy('cfx_stage7_warden_machine_round');
  if(XART._touch)XART._touch('cfx_stage7_warden_machine_round');
}
