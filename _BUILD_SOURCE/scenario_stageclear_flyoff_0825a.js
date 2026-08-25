/* Deterministic visual QA for the live STAGE X CLEAR -> fly-off -> stats handoff. */
(() => {
  enemies.length = 0;
  eBullets.length = 0;
  pBullets.length = 0;
  if (typeof boss !== 'undefined') boss = null;
  if (typeof subBoss !== 'undefined') subBoss = null;
  bossActive = false;
  subBossActive = false;
  bossDefeated = true;
  player.reset();
  player.invuln = 1e9;
  player.x = (typeof camX !== 'undefined' ? camX : 0) + VW * 0.5;
  player.y = VH * 0.78;
  flyoverT = 0;
  flyoverScroll = mapScroll;
  flyoverStartX = player.x;
  flyoverStartY = player.y;
  drawFlyover._clearStarted = false;
  drawFlyover._clearTicked = 0;
  drawFlyover._clearSting = false;
  drawStageClear._init = false;
  drawStageClear._res = null;
  setState(GS.FLYOVER);
})();
