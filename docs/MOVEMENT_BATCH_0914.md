# Shared glide, Frost Cruiser tracking and chopper motion

ENG-03: the shared horizontal glide helper is now used by the Frost Cruiser and Jungle Overlord-X. It accepts an explicit target X, clamps the hull's target inside the camera, limits speed, cannot overshoot, and rejects invalid/negative frame deltas. Later Warden choreography remains its separate S4-06 deliverable.

S3-05: Frost Cruiser samples the player's X every 200ms and follows at 175px/s (205 enraged), without the old side-zone wobble. Initial acquire falls from 1.35s to 0.90s. At the fully offscreen north turn it samples a clamped return lane, descends vertically at 150px/s instead of 92, resumes horizontal follow for 1.15s at its station, then commits to the existing laser charge. The Jungle Cruiser keeps its existing return behavior. New laser width/sweep, sounds, difficulty attacks and HP are separate pending work; no source art changed.

S1-07: chopper orbit angle now latches once when entering orbit instead of adding a half turn based on its current side every frame. Pursuit uses delayed player sampling and bounded horizontal glide. Orbit entry is speed bounded on both axes. The vertical bob's smoothing is frame-rate independent. Weapon sequencing, projectile functions, charge tells and ram/recovery states remain the existing authored patterns.

Validation: 14 focused Frost/helper checks plus 9 chopper checks pass, including 30/120Hz pursuit comparison, orbit continuity, bounds, reaction delay, return alignment, collision restoration and laser commitment. Syntax passed. Full suite completed with 3850 passes and 58 known failures (exit 1), no new names against the recorded pilot-reveal baseline (including the intermittent Stage-1 sand-tank assertion). No existing test assertions were edited for this batch.

Native Chromium inspected the real Stage-3 ship tracking and committed return, then transition through frostTrack into beamCharge. Stage-1 chopper crossed the centre with its orbit phase unchanged. Both review tabs reported zero console errors. This is controlled movement verification, not a full natural fight or difficulty balance audit. Screenshots/hashes and checks: [QA record](qa/movement_batch_0914.json).

Reproduction generators: `_BUILD_SOURCE/create_frost_follow_0914_review.py` and `_BUILD_SOURCE/create_chopper_motion_0914_review.py`. Serve the repository and open the matching `_shots/<name>/review.html`; step in bounded batches. Nothing committed or pushed.
