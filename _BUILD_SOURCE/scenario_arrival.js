/* scenario_arrival.js — watch the level arrive, rather than the 8 seconds of runway before it.
 *
 *   python3 _BUILD_SOURCE/shoot.py --state PLAY --stage 1 \
 *           --script _BUILD_SOURCE/scenario_arrival.js --seconds 3 --fps 6 --warm 120
 *
 * The opening is 14.6s and the part worth looking at is COAST — 8.0s to 11.4s — where the stage
 * master descends into place over open water. Jumping the clock there is the only way to catch it:
 * shoot.py's dt inflates between captures, so an unassisted run blows through the whole cinematic
 * in a handful of shots.
 *
 * Nothing is faked. The state, the clock and the draw are the game's own; only the starting time
 * is moved, the same way coleSceneApply moves a stage forward.
 */
(() => {
  if (typeof openingStart === 'function') {
    openingStart(1);
    setState(GS.OPENING);
    /* start just before COAST opens, so the first captures catch the master's bottom edge coming
       down out of the top of the screen rather than already landed */
    opening.t = OPEN_T[2] - 0.15;
    opening.scroll = 4200;      // the ocean has been moving for a while by now
  }
})();
