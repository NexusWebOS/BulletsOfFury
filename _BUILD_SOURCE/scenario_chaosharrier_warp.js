() => {
  beginStage(5);
  setState(GS.PLAY);
  player.reset();
  player.invuln = 1e9;
  enemies.length = 0;
  eBullets.length = 0;
  pBullets.length = 0;
  powerups.length = 0;
  subBossDone = false;
  subBossTriggered = true;
  warmStage(5);
  spawnSubBoss('chaosharrier');
  subBossActive = true;
  subBoss.enter = false;
  subBoss.y = VH * 0.26;
  subBoss._chaos.visible = true;
  subBoss._chaos.state = 'track';
  subBoss._chaos.cool = 99;
  subBoss._chaos.t = 0;
  chaosHarrierBegin(subBoss, 'warp_twin');
  stageTimer = 20;
  spawnClock = 9999;
  if (typeof waveIdx !== 'undefined') waveIdx = 999;
}
