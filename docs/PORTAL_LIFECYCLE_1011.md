# Portal forming, looping and closing — October 11, 2026

Mike approved the BOF redesign and requested separate forming and closing
animations, plus a fix for looping in the game. Each of the five portals now
has three 32-frame banks: **form, loop, close**. The review page can play each
bank independently or show the complete sequence, ending closed.

[Open the review](previews/portals_1011/index.html?effect=blue_rift&phase=sequence&revision=lifecycle).

| Portal | Forming | Closing | Frame / pivot |
|---|---|---|---|
| Ion-blue rift | Ignition branches into curved blue plasma blades | Blades curl inward, implode and fade | 384 × 384 / 192, 192 |
| Crimson rift | Matching scarlet ignition and assembly | Red implosion and fading sparks | 384 × 384 / 192, 192 |
| Emerald rift | Jade plasma builds around the dark aperture | Green coils collapse to a mint spark | 384 × 384 / 192, 192 |
| Chromium singularity | Black chrome ribs unfold around a widening throat | Throat pinches shut and ribs dissolve inward | 384 × 384 / 192, 192 |
| Fury breach gate | Purple membrane ignites inside stationary machinery | Membrane collapses; the armored shell remains | 512 × 640 / 256, 352 |

There are 480 main frames across fifteen animations, plus 96 independently
usable gate-membrane component frames. Forming and closing are separately
generated animations. Closing is not the opening reversed. Frame 32 of closing
is a terminal transparent frame, or the original stationary shell for the gate.

## Art ownership and alignment

Built-in `image_gen` generated the new animation sheets from the approved BOF
plates. All native-alpha sources and exact prompts are retained under
`_ART_SOURCES/portal_lifecycle_1011/`. The initial blue outputs had the wrong
row layout; those are retained as `*-first-grid.png`, and are not exported.
An explicit 4 × 8 reference canvas corrected the generation grid. Red and green
are generated palette edits of the accepted blue forming/closing sheets.

`_BUILD_SOURCE/prepare_portal_lifecycle_1011.py` owns the reference grids.
`_BUILD_SOURCE/build_portal_lifecycle_1011.py` owns PNG frames, equal-cell sheets,
one-shot/loop WebPs, the manifest, `assets/portal_lifecycle_art_1011.js` and the
`pl11_` art-taxonomy record. Export directory:
`assets/game/shared/fx/portal_lifecycle_1011/`.

One proportional scale is measured at the full-open endpoint of each phase;
small ignition and collapse poses retain their authored size. The dark throat,
or central ignition after it closes, is registered to one fixed pivot. Extra
transparent padding increases the earlier 320 × 320 canvas to 384 × 384 without
resizing its approved loop pixels. The game retains the same physical drawing
scale. All phase canvases and pivots match within a family. The gate's shell
and mask are the same assets throughout all phases.

Onion inspection caught five closing gate poses whose tiny throat had been
misidentified as a nearby bright strand. The builder records a measured local
window for those poses. The final formation and first closing cell lock to the
exact approved loop pose. Closing's terminal cell leaves no residual effect.

## Continuous playback and live use

The circular-formation follow-up adds one clockwise turn while each portal
forms. A quintic ease starts and ends with zero angular speed, returning to
the exact original orientation before the open loop begins. Rotation uses
the same simulation-owned formation time, so scrubbing, pause and replay
remain deterministic. The registered aperture stays fixed; there is no orbit
or changing scale. Loop and closing playback retain their authored motion.

For the armored gate, the existing membrane component turns inside the
existing aperture mask, then the stationary shell is composited above it.
The preview and game both use this renderer and lazily load its two fixed
gate layers. Onion controls sample neighboring formation times, including
their rotations. Source PNGs, sheets and raw WebPs retain their authored poses;
the complete native sequence captures include the additional runtime turn.

`assets/portal_lifecycle_1011.js` is shared by the game and preview. Opening and
closing clamp at their last frames; only the open bank wraps. Consecutive
authored frames blend with premultiplied-alpha weights, including frame 32 into
frame 1. This is a playback blend: source drawings are not warped or replaced
by generated intermediate poses. Exact frame stepping remains available with
Continuous playback disabled. A rounding guard prevents an exact requested
frame from falling back by one because of floating-point precision.

Finite sequences fit whole idle cycles into their allotted time so closing
starts at the same physical pose. The complete preview plays formation,
two idle cycles and closure, then stops; Replay begins a new sequence.

`assets/portal_encounters_1011.js` applies the approved chromium void to the
Stage 8 reformation/arena transition and the blue rift to the homeward/arrival
portal. The void continues using the encounter's original simulation clock
and anchor. It no longer multiplies accumulated time by the new phase's clock.
Encounter durations, ship motion and the arena reveal remain owned by the
existing encounter code. The world-camera expansion is proportional. Pause
does not advance the portal clock. The other colors and armored gate are
available in the complete asset package and review.

## Verification

- `node --check`: game.js, both new runtime scripts, generated registry and preview.
- Full `_BUILD_SOURCE/test_fl.js`: **8,700 passes, 0 failures**, final summary and exit 0.
- Existing `_BUILD_SOURCE/probe_playthrough_finale_1011.py`: **14 passes, 0 failures**, exit 0.
- `_BUILD_SOURCE/probe_portal_lifecycle_1011.py`: **144 passes, 0 failures**, exit 0;
  no page, console or missing-asset errors. Checks cover native images, joins,
  all registered frames, circular formation pixels and fixed pivots, stationary
  gate armor, Stage 8 handoff/pause, homeward phases and preview controls.
  Results are recorded in `docs/qa/portal_lifecycle_1011.json`. The circular-motion
  pass reran the full 8,700-check suite and this expanded native probe; the
  separate 14-check finale result above is from the preceding lifecycle pass.

All ten new main-phase onion sheets, the final gate closure and the mobile
preview were visually inspected. The circular formation also has native
five-pose contact sheets for each portal (`*_forming-turn-native.png`). Native captures,
full-sequence WebPs, screenshots and probe logs are in
`_shots/portal_lifecycle_1011/`. Prior portal packs and other local work remain
preserved. No commit or push was made during this pass.
