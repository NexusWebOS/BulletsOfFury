/* scenario_route.js — run the END transition leaving the stage you passed with --stage.
 *
 *   python3 _BUILD_SOURCE/shoot.py --state PLAY --stage 2 \
 *           --script _BUILD_SOURCE/scenario_route.js --seconds 2 --fps 10 --warm 20 --gif
 *
 * The outbound routes are normally only reachable by killing a stage boss, so they are effectively
 * invisible to the capture tool — which is how six of them stayed unbuilt behind a debug flag for
 * as long as they did. This drops straight into GS.OUTBOUND for the join leaving --stage.
 *
 * ⚠ Each shoot.py screenshot is a separate evaluate, so the next frame sees the real wall-clock
 * gap as its dt and the route completes in far fewer captures than --seconds/--fps implies. The
 * 2->3 route is 478 frames (~8s) of game time; expect it to be over well inside a 2s capture.
 * Aim early rather than assuming the route did not run.
 */
(() => {
  const from = run.stage;
  player.reset();
  player.invuln = 1e9;
  setState(GS.OUTBOUND);
  outbound = null;
  outboundStart(from);
})();
