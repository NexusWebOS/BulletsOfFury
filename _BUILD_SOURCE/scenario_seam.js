/* scenario_seam.js — put the capture right on the launch -> PLAY seam.
 *
 *   python3 _BUILD_SOURCE/shoot.py --state PLAY --stage 2 \
 *           --script _BUILD_SOURCE/scenario_seam.js --seconds 6 --fps 6 --warm 90 --gif
 *
 * shoot.py's --state PLAY calls beginStage and then setState(GS.PLAY), which skips the launch
 * entirely — so the one sequence Mike is complaining about is the one the capture tool cannot
 * normally see. This drops back into GS.LAUNCH and fast-forwards to the brake, so the ~6 seconds
 * that follow are brake -> settle -> 3-2-1 -> GO -> play: the seam, with a couple of seconds of
 * real play after it.
 *
 * Why not just run the whole launch: it is ~18s, and the run phase is a runway roll that proves
 * nothing about the handoff. Why not use probe_seam.py: that steps every frame inside ONE
 * synchronous evaluate, so lazily-loaded art never arrives (the --warm trap, CLAUDE.md). It gives
 * exact numbers for the ship and the camera, which are art-independent, and tells you nothing
 * about the terrain. This one yields between captures, so the master is actually decoded.
 */
(() => {
  setState(GS.LAUNCH);
  // straight to the brake: the roll is authored and irrelevant to the seam
  drawLaunch._phase = 'brake';
  drawLaunch._pt    = 0;
  drawLaunch._dist  = SEG_B3 + 240;   // exactly where the run phase hands over
  drawLaunch._spd   = 1750;
  drawLaunch._go    = false;
  drawLaunch._num   = 99;
  drawLaunch._mus   = true;           // music already counted as started; no restart mid-capture
  drawLaunch._lastT = 0;              // keep the re-init guard from firing and resetting dist
})();
