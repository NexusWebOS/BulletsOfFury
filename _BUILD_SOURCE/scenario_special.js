/* scenario_special.js — fire the active pilot's SPECIAL and hold it up for the capture.
 *
 *   python3 _BUILD_SOURCE/shoot.py --state PLAY --stage 1 --pilot axel \
 *           --script _BUILD_SOURCE/scenario_special.js --seconds 3 --fps 6
 *
 * shoot.py sets run.pilot before this runs, so the same file serves every pilot — capture axel
 * and falva with it and the two frames are directly comparable, which is the only way to check
 * that Axel really is her sprite in another palette rather than something that merely looks
 * similar.
 *
 * startSpecial() has no entry gate and sets t=15, so the special outlives any reasonable capture
 * window and nothing needs topping up.
 */
(() => {
  player.reset();
  player.invuln = 1e9;
  startSpecial();
})();
