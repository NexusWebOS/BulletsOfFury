# Physical final-boss transformations — October 7

`assets/finale_transform_1007.js` loads last, after the combat engine, generated
HC7 art/runtime and final-boss pattern upgrades.

- `j3Morph` snapshots the current visible combat pieces before the established
  attack cleanup. Destroyed modules and hidden collision proxies are omitted.
- During `transform1003j`, whole authored components unlock, rotate independently,
  and contract along a corkscrew. During `reveal1003j`, the next actual combat rig
  seats its torso, limbs and tools in sequence. Components use alpha 1 throughout;
  no procedural sprites, rectangular art slicing or body crossfades were added.
- HC7's generated helix passes behind/over the assembly; its smooth void reel
  covers the compact form change. Only those energy effects blend frames.
- `dr5Monologue` calls `j3Body(b,1)` with the actual combat pose. This is the same
  `colossus_body` and articulated arm art as the fight. Its original portrait,
  mouth animation, all twelve lines, 34-character text clock and two shrieks
  remain owned by the existing cinematic code.

This layer does not replace or wrap `r30Tick`, write HP, assign modules, invoke
extra timers, alter dialogue or award rewards. The existing 1.25-second outward
transition and 1.15-second reveal still control gameplay protection and all nine
saved pools. Only the synchronous pose query temporarily selects fight geometry;
its mode/attack/return/visibility fields are restored in a `finally` block.

## Verification

Native probe: `_BUILD_SOURCE/probe_finale_transform_1007.py`.

69 native Chromium checks passed, with zero page, console or missing-file errors.
Each of nine forms was damaged through `modularHit`, had a real module destroyed,
went home, and returned through the actual transition controller. Every life and
damaged module object persisted. Native draw arguments proved full opacity and
no destroyed module, while simulation clocks advanced exactly once per step.
The Knight legitimately filters its module array on revisit; the test checks the
same component objects rather than requiring the same container array.

The probe also checks render-only calls, interruption back to combat, actual
speech body image keys, preserved dialogue timing/text/shrieks and delegation to
the existing protected final-death renderer. Visual evidence includes all nine
outward/reveal/ready captures and a full Warden-to-Hammer animation:

- `_shots/finale_transform_1007/review.html`
- `_shots/finale_transform_1007/warden-to-hammer.gif`
- `_shots/finale_transform_1007/combat-body-monologue.png`
- `docs/qa/finale_transform_1007.json`

Headless regression hook: `_BUILD_SOURCE/test_finale_transform_1007.cjs` (load
after all other October 7 modules). Native results are controlled fixtures, not
a claim of campaign completion or human difficulty validation.
