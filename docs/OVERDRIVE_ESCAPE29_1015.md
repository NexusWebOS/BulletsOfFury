# Overdrive Escape29 — Dead Signal breakout, 2026-10-15

Build `overdrive1015-escape29-r1`. Local expansion update; no commit or push.

## Route and combat

Stage 3 keeps its top-down assault, with orthogonal wall, barrier, crate, barrel
and red-relay art. Dead structures become the existing authored rubble. Yuri
has one hit, lives, and no health strip in this stage, the escape, and Prism
Bastion. Other missions retain their existing health rules.

Gosfer now has 840 HP (up from 300), accelerated streams and movement, rolls,
and physical vaults across the linked barriers. Shield ownership remains:
only Gosfer's rounds break those barriers. The existing portrait conversation,
fear animation, lightning transformation, Retina-locked anti-prone rounds and
Last Hope transition remain. Roll/jump vulnerability windows are explicit.
Defeat opens the north elevator instead of triggering the old automatic clear.

The elevator ascends, blacks out with a new power-down cue, restores emergency
power/red alarm, then accelerates. Hotwire's portrait warns about the floor
hatch; generated Overdrive-font SHOOT ME text marks the shootable hatch. Hold
Retina and shoot it before the timer expires. Its hinge tips 45 degrees into
a 28-second drone slide. Only aim and fire are accepted in that section.
Drones enter through ceiling vents, orbit, retreat on hits, return and explode.
Both drone fire and Yuri's rounds travel; player rounds can intercept theirs.

The service corridor is a side-view run-and-gun route with lower floor drops,
cover crates, jumps, vaults, rolls, crouching, prone crawling and cover/peek
fire. No platform-jumping course. Existing Pixel25 enemies enter from the right.
Halfway, the explosion front advances at 212 px/sec even during vaults; Yuri
runs at 255. Barrel fire blows the metal door. Down+roll slides through the
breach, then a drop/fade transfers into Prism Bastion as visible LEVEL 4.
Checkpoints consume a life on retry (hatch, slide, corridor, self-destruct).

Visible campaign order is 2 -> 3 -> 4 (Prism Bastion) -> 5 (Machinists) ->
6 (Desert Breaker) -> 7 (Convoy). Internal IDs and saved-password slots are
preserved; the pinned password list uses the new visible numbering.

Prism Bastion retains its Three.js geometry, eight rooms, original enemy banks,
and Helios encounter. Its regular enemy and turret rounds are faster finite-
speed projectiles. The reactor's ray pattern emits travelling bolts instead
of direct ray damage. Cover impacts play metal audio and kick the camera.
Up+jump vaults the player's wall; the renderer changes cover layering as Yuri
crosses it. Top-down vaults can queue a roll or prone landing; rolls recover
after five seconds. Existing north-moving side-fire clips remain available.

## Art and input

238 runtime PNG exports, including 13 authored aim selections per facing,
16 run, 16 vault, 16 roll, 8 low-step, 16 crawl, 7 cover/peek, 12 slide-motion
frames per facing, directional slide stills, animated drones, and scenery.
Right-facing banks are declared mirrors, not extra generated drawings.
The angle labels are nominal selection bins; generated poses are not exact
mathematical 15-degree rotations. They are whole-body art, not rotated limbs.
Barrel metadata drives flash and projectile sockets, including reverse slide.
Fixed 192x224 actor canvas/root96,160 and proportional half-scale; no per-frame
fit. All frames have even dimensions and binary alpha. Existing art is retained.
Authorship, generation IDs, prompts and rejected candidates are retained under
`art/escape29/source/escape29`; provenance is in `art/escape29/provenance.json`.
415 included PixelLab generations used this pass; 1275 remain. One corrected
reverse slide came from built-in imagegen after the PixelLab pose retries.

Side-view M30/Genesis six-button controls: A fire, B jump/vault, C cover,
X roll, Y grenade, Z Retina; Down crouches, Down+X slides, Mode+X toggles prone.
Hold Retina and use D-pad for free aim. During the drone slide, movement,
jump and roll are disabled. In top-down stage 3 the existing directional-fire
layout stays: Mode+A vault, C roll, Mode+X prone; queue C while vaulting to roll.
In the base view, Up+B vaults the wall; the existing side-shoot controls remain.
Keyboard defaults: WASD/arrows move, R or K jump, Space/H/V roll, F prone,
Shift/C cover, I/N Retina, J/Z fire, U grenade. Rebinding stays supported.

## Verification and limits

43 native Chromium checks pass, plus 4 continuous-route/cover checks and
6 final rubble/elevator/input-handoff checks (53 total). The
ordinary-input drone slide and full corridor/chase both clear; the corridor
sample finishes with zero deaths. No health, invulnerability, geometry or
enemy edits are used during those playthroughs. Separate fixtures isolate
boss transitions, damage, vaults, and the hatch. This is not a complete
input-only Gosfer clear or physical M30 test. Synthetic raw receiver inputs
verify the printed button mapping; physical timing/feel still needs playtest.

Native pixels, onion overlays, root/scale, muzzle locations, drone hit flash
and expiry, cover layering, pause, respawns and the level4 handoff inspected.
All 820 tracked prior PNG hashes match. Zero page/console/asset errors in the
final runs; intentional aborted audio streams during music changes/navigation
are recorded separately. Export audit checks all 238 frames. Syntax checks
pass; required base suite reaches BUILD OK / 0 ERRORS / exit0.

Runtime owners: `js/combat29.js`, `js/escape29.js`, with scoped hooks in core,
main, fortress, frontend, HUD27, Ground20 and Prism Bastion. Builder:
`_research/build_escape29.py`. Native probes: `_research/probe_escape29.py`
and `_research/probe_escape29_route.py`. QA: `docs/qa/overdrive_escape29_1015.json`,
`docs/qa/overdrive_escape29_route_1015.json`,
`docs/qa/overdrive_escape29_final_1015.json`, `docs/qa/escape29_views`.
Review: `art/escape29/preview.html`. Local preview port8781.
No `assets/game.js` edit. Preserve unrelated existing local work.
