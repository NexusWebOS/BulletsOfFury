# Gameplay bug fixes — 2026-09-13

Mike asked Codex to continue improving and fixing the game. This pass fixes
reproduced collision and weapon-audio bugs using the existing encounter designs
and authored assets.

## Razorback pellets

During the guns phase, a pellet over the sealed central armor disappeared
without doing damage. `subBossHitPart` already recognized exposed parts, but
`subBossSolidAt` had no Razorback branch, so ordinary projectiles were consumed
by its broad rectangle before damage routing rejected the hit.

The collision predicate now uses `razorbackPartAt`. Shots through bare armor,
destroyed guns and invulnerable transitions continue flying; live exposed guns,
the turret and the final hull still stop and receive shots.

## Held laser damage

The held-laser update sampled the miniboss's center row. This missed the
Razorback's exposed guns. It also prevented the laser from reaching a Tempest
brother when the duo's aggregate center lay beyond the beam's endpoint.

The active Tempest duo's column fallback used unrotated aperture widths and
hull geometry, despite its new rotated art and physical hardpoints. A laser
through the outer edge of a quarter-turned front port did no damage.

Held lasers now intersect their actual finite width and endpoints against
exposed Razorback circles and rotated Tempest rectangles. Live apertures keep
their existing targeting priority, and the nearer intersected brother receives
damage. Destroyed ports, offscreen targets and hulls outside the beam cannot
receive phantom hits. The actual held-beam update and native damage entry points
use the same geometry. Other minibosses retain their existing routes.

## Cole nuclear impacts

Three actual nuclear impacts roughly 1.3 seconds apart played the first and
third detonation, with the middle one rejected by the live sample mixer's
1.8-second retrigger gate. The cue existed and decoded; its cooldown silenced it.

The nuclear detonation cooldown is now 120ms. Three separate impacts receive
their own existing pooled voices, while a rapid duplicate remains throttled.
The approved sample, volume and filters are unchanged. The three-cue mixer
render measures RMS 0.0688 and peak 0.3684, with no clipping, voice cuts or errors.

## Evidence and validation

- Before-change Chromium reproduction: 10 checks pass, confirming the failures
  and the unaffected exposed-part behavior. The archived runtime SHA-256 matches
  the preceding validated build. Baseline mode serves that exact snapshot.
- After-change Chromium: 11 checks pass with zero page or console errors.
- Existing native Razorback playtest: 19 checks pass, including turns, sonic
  attacks, individually launched missiles, phase order, invulnerability and death.
- All 14 new section-297 assertions pass. Syntax checks pass. The complete suite
  finishes with **3,680 passes / 61 failures**, exit 1, and **zero new failure
  names** against the preceding return-pass baseline.
- Actual canvas screenshots were inspected. Results and hashes:
  `docs/qa/game_bugfix_0913.json`. Logs, before/after screenshots and the six-second
  three-nuke sound sample are in `_shots/game_bugfix_0913/`.

Run `python _BUILD_SOURCE/probe_bugfix_0913.py` for targeted browser verification.
The fixture freezes movement for one frame when isolating laser geometry;
it exercises the real held-beam update and damage routes. The separate original
Razorback probe runs its live attack and phase progression.

The runtime remains self-contained in `assets/game.js`. Readable sources are
`_BUILD_SOURCE/bugfix_0913/beam.js`, `tests.js`, and the Tempest `fighter.js` and
`adapter.js`. For rebuilding these edits, run the Tempest integration script
then `_BUILD_SOURCE/bugfix_0913/integrate.py`.

Existing uncommitted work and earlier recordings were preserved. Nothing
committed or pushed. Spaceship transformation replay and weapon balance remain
separate design decisions recorded in the handoff.
