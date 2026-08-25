/* Deterministic visual QA for the complete Stage 7 boss-clear -> Stage 8 portal handoff. */
(() => {
  run.mode = 'arcade';
  run.stage = 7;
  run._l78Entry = 0;
  curStage = STAGES[6];
  enemies.length = 0;
  eBullets.length = 0;
  pBullets.length = 0;
  boss = null;
  subBoss = null;
  bossActive = false;
  subBossActive = false;
  bossDefeated = true;
  player.reset();
  player.invuln = 1e9;
  player.x = (typeof camX !== 'undefined' ? camX : 0) + VW * 0.42;
  player.y = VH * 0.78;
  flyoverT = 0;
  flyoverScroll = mapScroll;
  flyoverStartX = player.x;
  flyoverStartY = player.y;
  l78entry = null;
  drawFlyover._clearStarted = false;
  drawFlyover._clearTicked = 0;
  drawFlyover._clearSting = false;
  drawFlyover._portalOpen = false;
  drawFlyover._portalTake = false;
  drawFlyover._portalClose = false;
  drawStageClear._init = false;
  drawStageClear._res = null;
  setState(GS.FLYOVER);

  let fastForwarded = false;
  let continued = false;
  window.__qaTick = () => {
    if (state === GS.STAGECLEAR && !fastForwarded && stateT > 0.45) {
      fastForwarded = true;
      Input.injectTap('enter');
    } else if (state === GS.STAGECLEAR && fastForwarded && !continued && stateT > 0.90) {
      continued = true;
      Input.injectTap('enter');
    }
  };
})();
