# Stage 4 and Stage 6 playtest repairs — October 13, 2026

These changes address Mike's latest main-game playtest. The work is installed in
the GitHub coding checkout; no commit or push was requested.

- Stage 4 generator positions now follow their parent ship, so camera movement
  cannot slide the hull over a core. Helpers sit between sockets. Core balls,
  fusion split balls and pursuit balls use authored blue electricity and matching
  impacts instead of falling through to the orange fireball renderer.
- Locked Stage 6 scenes own their update. Ordinary enemies, hazardous projectiles
  and outgoing combat effects are cleared; waves cannot spawn behind the scene.
  Native dialogue and demonstrations continue, while pickups are preserved.
- The Stage 6 miniboss suspends friendly wing ships, shots, damage and pressure
  bonuses. Surviving allies return after the miniboss's actual defeat.
- Rebel sound cues are prewarmed. Interrupted music resumes using the same media
  element, suspended effects contexts recover, and cold attack sounds are not
  queued to play late. User volume settings and the voice budget are preserved.
- Voss's turbo wake follows his actual flight, remains through his return outside
  the arena, and fades after his visible descent from above. The introductory
  exhibition uses the same final position for the ship and wake. His first dash
  respects the target shown by its warning.
- Mini-aircraft use silver (Stage 1), camo green (Stage 4), and black/blue (Stage 6)
  across headings and barrel rolls, with cached palette conversion.

The native tests use the actual shipping page, gameplay controllers, collision,
media and renderer. They are controlled encounter fixtures, not a complete human
campaign playthrough or a measurement of Mike's laptop speakers.

See the focused reports for reproduction commands, scope and portable evidence:

- `docs/S4_CORE_ACCESS_1013.md` — 121 checks across all four difficulties.
- `docs/STAGE6_SEQUENCE_1013.md` — dialogue isolation, demos and solo miniboss.
- `docs/REBEL_AUDIO_TURBO_1013.md` — 125 checks across Edge, Chrome and Firefox.
- `docs/FORMATION_PALETTES_1013.md` — all 12 affected animation sheets.

The full legacy suite also contains a historical October 11 fixed-anchor fixture.
That fixture intentionally loads its original layer, so its fixed-position check
does not describe the final Stage 4 override. The native Stage 4 probe loads the
complete shipping page and verifies the current moving-core behavior, including
camera sweeps, actual bullets/beams/guided missiles, destruction and regeneration.

Final combined validation: 332 focused native checks passed, 12 palette sheets
verified, and the full `_BUILD_SOURCE/test_fl.js` ended with BUILD OK / 0 ERRORS
and exit 0. `assets/game.js` and all changed gameplay modules pass syntax checks.
The final Stage 6 gate also advances Cole's visual effect clocks and clears demo
shots on the beat transition, preserving tutorial animation without live combat.
Combined summary: `docs/qa/stage_repairs_1013.json`.