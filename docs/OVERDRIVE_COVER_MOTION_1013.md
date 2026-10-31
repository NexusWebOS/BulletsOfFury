# Overdrive cover and infantry repair — October 13, 2026

The fortress now includes six straight horizontal concrete bunker walls. These
and the tall side walls survive bullets, explosions and vehicle rams; their
collision remains active. Existing wood, barrels, crates and relays retain
their destruction behavior.

F toggles prone. Moving while prone crawls. Cover plus fire raises Yuri through
the authored pop-up frames without moving his feet through the collision slab.
Retina plus fire while in cover blindfires with modest spread while keeping the
body protected. Blindfire rounds emit only during the raised-rifle poses, and
their visual socket is registered to the authored barrel tip instead of the
ground collision coordinate. Releasing fire lowers him. Controller mappings are documented
by the owning Help screen. A held upgrade is replaced by a new gun pickup;
Tab and the wheel cannot swap it. An exhausted gun returns to unlimited rifle.

The prior fortress pathfinder passed a waypoint displacement directly into
movement as if it were a unit direction. This produced velocities over 20
pixels per tick near walls. Directions are now normalized before acceleration;
robot movement eases into the desired velocity. Aiming turns gradually and
nearby robots separate. Reinforcements are queued by progress and enter above
the camera's north edge, rather than being instantiated in view.

Projected enemy torso hitboxes use swept elliptical tests at the same vertical
lift as the visible bullet. A projectile passing through a robot's visible body
can connect without having to intersect its narrow ground footprint. Gosfer
uses a matching projected body test, smoother movement and a prominent health
bar directly below the player HUD, with introduction fill.

## Authored artwork

Built-in image generation produced five retained source images under
`expansion/topdown/art/cover_motion_1013/source`, each with its exact prompt.
Identity references were the existing Yuri north seed, robot south frame and
Gosfer south frame. A final blindfire pass uses Yuri's south-facing seed so his
back truly presses against the northern wall while the rifle reaches behind
his shoulder. The earlier rear-view blindfire candidate remains in source.
No source painting, motion interpolation, silhouette
warping or per-pose fitting was used.

The owning builder is `_research/build_cover_motion_1013.py`. It exports 55
even-sized frames with audited crops, bounds, source hashes and bank scale:

- Yuri north: eight lateral sidestep, eight pop-up, eight blindfire and eight
  rear knockback drawings. The last sequence falls away without changing into
  the old south-facing front pose.
- Robot south: eight strafe drawings.
- Gosfer south: eight strafe and six forward walk drawings.
- One straight concrete cover wall.

All character exports are 320 × 320 with anchor (160,256). The cover object is
320 × 192 with anchor (160,160). The original eight-direction locomotion banks
remain available. New north-facing sidestep covers the principal upward assault
lane; this pass does not claim newly authored sidesteps for every facing.
Source generation delivered six Gosfer walk drawings on its last row instead
of eight. The builder records and exports the six actual drawings, rather than
duplicating frames. Contact sheets include registered neighbor onion overlays.

The manifest merges into `TD_ASSAULT_ART`; it must load after the existing Yuri
motion manifest and before gameplay modules. The normal ART loader warms the
new keys and uses the game renderer for verification.

## Verification

Native Chromium `probe_cover_motion_1013.py`: 15 passing checks, zero failures,
zero page/console/missing-asset errors. Tests exercise F through actual input,
indestructible cover damage, anchored peeking, blindfire protection, real
sidestep selection, no swapping, pickup replacement, swept body hit acceptance
and rejection, bounded enemy acceleration, rear death poses and Gosfer torso
hits. Native gameplay captures and all authored contact sheets were visually
reviewed. Portable results: `docs/qa/overdrive_cover_motion_1013.json`.

The existing assault probe now checks fixed-position peeking and fires at
Gosfer from an open flank around the new concrete cover. It passes all 38
checks, with zero browser errors. Its pursuit bot completes 150 seconds with
88 hull; this deterministic fixture is not a human difficulty assessment.
Portable result: `docs/qa/overdrive_cover_assault_regression_1013.json`.
Whole-build integration and required base
regression are recorded by the parent update. Physical controller handling and
human difficulty assessment are not claimed by this focused fixture.
