# Enemy HUD palettes and pilot frames — October 8, 2026

Installed in the live game: solid glowing enemy health fills, stage-specific frames,
compact cyan shield sub-bars where the encounter reports a shield, and the shallower
health-only frame everywhere else. The player HUD rows in the artwork gallery remain
concept previews; this change installs the enemy components.

| Stage | Health palette |
|---|---|
| 1 — Jungle | Emerald / lime green |
| 2 — Lava | Red / scarlet |
| 3 — Ice | Pale ice blue |
| 4 — Desert airbase | Light sandy brown / tan |
| 5 — Space | Light lavender |
| 6 — Sky / rain | Royal blue |
| 7 — Sewer | Toxic chartreuse green |
| 8 — Alien void | Dark purple with crimson / magenta highlight |
| 9 — Water space | Watery azure blue |
| X — Harrier route | Blue health in a gunmetal twin-turbine frame |

Stage 6 and Stage X Rebels use five individually anchored, independent HP bars:
Voss red steel and V insignia; Nyx violet with a cyan spiral; Rook orange with
grapple-hook ends; Kaia teal with radio-signal ends; Jace crimson with razor wings.
The bars follow world-space ship positions and use the existing cloak/death filters.
No aggregate Rebel bar is added. Rebel shields were already absent in this build.

## Files and loading

- `assets/enemy_hud_art_1007c.js`: explicit source paths and measured crop/well coordinates.
- `assets/enemy_hud_1007c.js`: renderer, stage preload keys, stage retirement and Rebel anchoring.
- `assets/game/levels/stage_01..09/ui/enemy_bars_1007c.png`: generated theme sheets.
- `assets/game/levels/stage_06/ui/{harrier_bars,rebel_bars}_1007c.png`: custom encounter art.
- `_ART_SOURCES/hud_enemy_bars_1007/`: exact prompts, generated-source provenance, hashes and source rectangles.
- `_ART_SOURCES/hud_themes_1007/review.html`: updated selectable gallery, including Harrier and Rebels.

Stage X internally runs Stage 6 plus `run._gp4StageX`; only that route's `warhive`
encounter selects the Harrier housing. Stage 5's Chaos Harrier keeps the space palette.

Only the current stage's sheet is queued; Stage 6 also queues its two route sheets.
Previous stage image roots and derived canvases retire through the existing memory
owner. Native-size frame canvases are built once and reused; a 24-entry cap bounds
resize caching. No pixel readback, new Image objects, or canvas allocations happen
in a steady-state bar draw. Eleven authored PNGs add 18.03 MiB on disk. Source art
remains at its generated resolution, with transparency intact; no shared atlas was edited.

The renderer clears the baked example fill inside the cached frame, replaces it with
the authored empty recess, then clips an authored luminous fill sample to live HP.
It never displays the example 75% value as game health. Thin shield fills use the
same method. Boss introductions keep their existing visibility and alpha gates;
Hammer's recovery overlay and the final boss's health/charge fraction remain connected.
No HP, damage, movement, attacks, or difficulty values changed. `assets/game.js`
is byte-identical to its pre-task state (SHA256
`0413d3cd1e0f92703986a67d7966e740dd44b3fd421586292e2c824e4bfc91ca`).

## Verification

- Required base game suite: **7,952 passes, 0 errors**, reached its final summary.
- JavaScript syntax checks passed for game.js and both new layers.
- Native Chromium: **245 checks passed**, zero page/console errors. Captures were
  inspected at gameplay size. Checks cover all nine stage boss and miniboss palettes,
  all four frame variants at 0/25/50/75/100% HP and shield, stage texture retirement,
  Harrier versus normal Stage 6 routing, and all five Rebels on Easy, Normal, Hard,
  and Furious in both Stage 6 and Stage X, including cloak and death suppression.
- Gallery: all eleven tabs resolve and only the selected image is present.
- Native evidence and machine-readable results: `_shots/enemy_hud_1007c/review.html`
  and `validation.json`; regression log `_shots/enemy_hud_1007c_suite.txt`.

These are controlled rendering/encounter fixtures, with an invulnerable player and
selected HP values. They verify this HUD change; they are not survival or balancing
measurements. Entrance phases were advanced through their real controllers, and the
Stage 9 sentinels were defeated through their hit handler to reveal Tidal Sovereign.
The existing legacy VM suite does not load every extension, so the new layers are
covered by the native Chromium checks rather than by that suite alone.
