/* Visual QA scene for Stage 8's real miniboss path. */
(() => {
  player.reset();
  player.invuln = 1e9;
  enemies.length = 0;
  eBullets.length = 0;
  if (typeof boss !== 'undefined') boss = null;
  if (typeof subBoss !== 'undefined') subBoss = null;

  if (typeof spawnSubBoss === 'function') spawnSubBoss('spawncarrier');
  const b = (typeof subBoss !== 'undefined') ? subBoss : null;
  if (!b) return;
  b.enter = false;
  b.x = (typeof camX !== 'undefined' ? camX : 0) + VW * 0.5;
  b.y = 154;
  b.ty = 154;
  b.fireCd = 999;
  b._sbm = 0;
  b._sbmT = 999;

  /* Keep only this visual-QA subject in place while production attack logic runs. */
  const keepY = b.y;
  const origMove = shipBossManoeuvre;
  shipBossManoeuvre = function (subject, dt) {
    if (subject !== b) return origMove(subject, dt);
    subject.x = (typeof camX!=='undefined'?camX:0) + VW*0.5;
    subject.y = keepY;
    shipBossMuzzleTick(subject, dt);
    return true;
  };
  /* The screenshot clock samples exact frames. Trigger the production attack routine on a known
     cadence so the capture is guaranteed to contain both its short muzzle reel and its rounds. */
  let qaFrame = 0;
  window.__qaTick = function () {
    qaFrame++;
    if ((qaFrame % 24) === 0 && subBoss === b && !b.dead) shipBossAttack(b);
  };
  shipBossAttack(b);
})();
