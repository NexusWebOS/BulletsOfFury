/* Visual QA: clean critical hull plus production death-lattice projectiles/muzzles. */
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
  b.hp = Math.floor(b.maxhp * 0.24);
  b.fireCd = 999;
  b._sbPhase = 1;
  b._sbStep = 0;
  b._sbm = 0;
  b._sbmT = 999;

  const keepY = b.y;
  const origMove = shipBossManoeuvre;
  shipBossManoeuvre = function (subject, dt) {
    if (subject !== b) return origMove(subject, dt);
    subject.x = (typeof camX !== 'undefined' ? camX : 0) + VW * 0.5;
    subject.y = keepY;
    shipBossMuzzleTick(subject, dt);
    return true;
  };
  let qaFrame = 0;
  window.__qaTick = function () {
    qaFrame++;
    if ((qaFrame % 18) === 0 && subBoss === b && !b.dead) shipBossAttack(b);
  };
  shipBossAttack(b);
})();
