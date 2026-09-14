# Tempest fighter passes — Mike's revised flight direction

Latest revision: Mike requested complete offscreen thrusts and physical returns.
See `docs/TEMPEST_RETURN_0913.md`; its exit-based maneuver supersedes the timed
braking and return described in this original fighter-pass record.

After reviewing the native duo recording, Mike requested red-to-green flashes,
south-facing jets, rapid turns and slides, and charged thrusts toward his ship
with sounds. This supersedes the duo's earlier fixed nose-up/one-axis direction.
The stored original solo Tempest and the reviewed source engines remain intact.

Both active duo hulls start nose south. Between committed passes, they bank into
their existing travel paths and turn north when passing below the pilot. The new
director gives one brother at a time a pair of fast lateral slides, an aiming
charge, an afterburner pass, a braking turn and a fast return to the upper arena.
Black reserves its turn so gray can finish an existing crossing and clear the
screen; neither ship can own a committed pass while the other owns one.

The whole authored hull pulses red while aiming. At 780ms the cue turns green,
locks the target, and holds for 220ms before ignition. Thrust follows its committed
velocity without homing. Speed is 840 world pixels/second, rising to 960 in hell
and frenzy; the gray survivor retains its 15% increase. A phase gate or death
cancels the maneuver, its cue and engine hold. Offscreen ships are unhittable.

The drawn hull, aperture geometry, body contact and enclosing broad phase rotate
together. Front and rear muzzle directions derive from the physical aperture on
the rotated hull. Pellets, delayed needles and laser lanes leave that muzzle;
disabled apertures remain disabled during both ordinary and new maneuvers. Angled
lasers still clip below the screen-space MINI BOSS gauge.

The existing authored Dambreaker twin engine flames provide exhaust, attached to
the Tempest tail bells and extended under thrust. Dedicated code-owned aliases
reuse the game's charge, retina, RCS, booster, engine and brake samples, with
explicit mixer/gating rows. The engine bed uses the game's ordinary held-loop
lifecycle and fades after the pass. No atlas or authored hull files changed.

Implementation: `_BUILD_SOURCE/tempest_source_0913/fighter.js` and `adapter.js`,
embedded by `_BUILD_SOURCE/integrate_tempest_duo_0913.py`. The one-time
`integrate-fighter.py` installs rotating hardpoints and sound aliases. Source
records in the same directory are historical inputs; `assets/game.js` is the
actual self-contained runtime.

Verification: `_BUILD_SOURCE/probe_tempest_fighter_0913.py` runs the actual game,
captures red/green/thrust for each brother, checks motion and rotated port damage,
compares gauge pixels with banked lasers on/off, and records real-input footage
with frame-stamped game sound. Its demonstration pilot is invincible; no health
gates are accelerated in this recording. Suite section 295 verifies commitment,
physical gun directions, aperture disablement, pass cancellation and sound rows.

Video: `_shots/tempest_fighter_0913/BulletsOfFury_Tempest_FighterPasses.mp4`.
Results: `docs/qa/tempest_fighter_0913.json`.

Final validation: syntax checks passed. All 12 new fighter assertions pass, and
real Chromium passed 10 checks with zero page or console errors. Two complete
suite runs each finished with 3,658 passes and 61 failures (exit 1). Sixty failure
names match the takeover baseline; the additional Stage 1 sand-wave sampling
failure is already present in `_shots/tempest_duo_0913/test_fl.log`, recorded
before these flight changes. The validation JSON records that evidence and no
unexplained failure names. No unrelated Stage 1 code or existing assertions were
changed to alter this result.

The final encoded movie was inspected and fully decoded: 30 seconds, 900 frames,
960×1024 at 30 fps, zero decode errors, with stereo game sound. The completed
video is retained; its silent picture and temporary WAV intermediates were
removed to conserve disk space. Nothing committed or pushed.
