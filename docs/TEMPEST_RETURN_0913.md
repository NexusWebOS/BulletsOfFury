# Tempest complete thrust exit and return

Mike requested that each jet face its thrust direction, fly offscreen, and then
fly back onscreen. This replaces the earlier timed braking and short return in
the active duo's fighter maneuver. Existing slides and red/green cues remain.

During the charge, the hull turns toward the locked thrust vector. Ignition
waits until the nose finishes that turn. The committed velocity and nose then
stay aligned throughout the outbound pass, with no tracking of a late dodge.

Thrust continues until the entire rotated hull clears any camera edge by 90
world pixels, including room for its exhaust. There is no elapsed-time brake
inside the viewport. The jet turns back while stationary and fully offscreen,
holding for at least 350ms and completing its turn before inbound movement.

The return target is a visible upper-arena position chosen when the jet exits.
It flies there at 560 world pixels/second with its nose along the flight path.
There is no teleport or timed early completion. It banks toward the pilot at
the arrival position, then releases the pass so its brother can take a turn.
Hull/port hit geometry stays rotated; offscreen actors remain unhittable.
Phase changes and death retain their existing pass cancellation.

The outbound and inbound legs use the game's booster and held engine sound.
Braking and turning cues happen offscreen. Authored exhaust follows the tail
on return as well as outbound thrust. No artwork or stage assignments changed.

Implementation: `_BUILD_SOURCE/tempest_source_0913/fighter.js`, embedded in
`assets/game.js` by `_BUILD_SOURCE/integrate_tempest_duo_0913.py`. Suite section
296 is maintained in `fighter-return-tests.js` in the same source directory.

Validation: syntax checks passed. All eight new return assertions and the 12
existing fighter assertions pass. The complete suite finished with **3,666
passes / 61 failures**, exit 1; zero new failure names against the preceding
fighter baseline. Real Chromium passed **14 checks / 0 failures**, with zero
page or console errors. Both brothers completed two exits and two physical
returns in the recording, with zero heading mismatches or position jumps.

Run the actual-game probe with
`python _BUILD_SOURCE/probe_tempest_fighter_0913.py --return-pass`.
Its recording uses real movement input, an invincible demo pilot, and unchanged
health gates. The final movie is 30 seconds, 900 frames, 960×1024 at 30 fps,
with stereo game sound. Encoded frames were inspected and the entire movie
decoded without errors. Results: `docs/qa/tempest_return_0913.json`.

Video: `_shots/tempest_return_0913/BulletsOfFury_Tempest_ExitAndReturn.mp4`.
Earlier recordings remain intact. Nothing committed or pushed.
