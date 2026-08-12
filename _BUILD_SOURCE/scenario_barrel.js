/* scenario_barrel.js — park a line of fuel barrels on screen and detonate the first one.
 *
 *   python3 _BUILD_SOURCE/shoot.py --state PLAY --stage 1 \
 *           --script _BUILD_SOURCE/scenario_barrel.js --seconds 2 --fps 12 --warm 200
 *
 * Barrels are shootable prop-enemies, and the player never fires in shoot.py — so a blast is
 * unreachable from a capture without help. This places a file of them and kills the bottom one,
 * which lets propBlast run for real: its own FX, then the chain into the neighbours.
 *
 * A line rather than a single barrel on purpose. The chain is recursive and lands on one frame,
 * and the thing worth looking at is whether that still reads as a RUN of blasts spreading up the
 * file rather than one flat pop.
 */
(() => {
  player.reset();
  player.invuln = 1e9;
  enemies.length = 0; eBullets.length = 0;
  // out of the player's lap so the blast is not judged through a screen-shake at point blank
  player.x = worldWidth() * 0.5;
  player.y = VH * 0.86;
  const bx = worldWidth() * 0.5;
  for (let i = 0; i < 4; i++) spawnEnemy('s1fuelbarrel', bx, VH * 0.30 + i * 52, {});

  /* The script runs ONCE, before shoot.py's warm — so detonating here would put the whole blast
     behind the warm and every captured frame would show the aftermath. Fire it on a frame count
     instead, a little past the warm, so the capture opens on the detonation itself.
     205 against --warm 200: the first shot lands within a few frames of the bang. */
  let n = 0;
  const origLoop = window.loop;
  window.loop = function () {
    if (++n === 205) {
      const b = enemies.find(e => e.type === 's1fuelbarrel' && !e.dead);
      if (b) { b.hp = 0; killEnemy(b); }        // the real kill path, so propBlast runs as it does in play
    }
    return origLoop.apply(this, arguments);
  };
})();
