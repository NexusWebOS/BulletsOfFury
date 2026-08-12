/* scenario_flyover.js — the end-of-stage exit, which is otherwise only reachable by beating a boss.
 *
 *   python3 _BUILD_SOURCE/shoot.py --state PLAY --stage 1 \
 *           --script _BUILD_SOURCE/scenario_flyover.js --seconds 3 --fps 6 --warm 120
 *
 * Counting the ships in the frame is the whole test: the bug was that drawWorld drew the real
 * player while drawFlyover drew a second copy on top, so the level ended with the ship sitting in
 * the background and a duplicate climbing away.
 *
 * The hover beat is 1.35s and the climb 1.7s, so a ~3s capture covers hover, climb and the fade.
 */
(() => {
  player.reset();
  player.invuln = 1e9;
  enemies.length = 0; eBullets.length = 0;
  flyoverT = 0;
  flyoverScroll = mapScroll;
  flyoverStartX = player.x;
  flyoverStartY = player.y;
  if (typeof drawFlyover === 'function') drawFlyover._musicCut = false;
  setState(GS.FLYOVER);
})();
