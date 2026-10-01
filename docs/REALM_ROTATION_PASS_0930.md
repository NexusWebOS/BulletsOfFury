# Stage 8 finale and portable rotations — September 30, 2026

Implemented locally in the existing game checkout. Earlier cinematic, weapon and encounter work is preserved. No commit or push was made for this pass.

## Encounter behavior

- Three combat forms: the gray host visibly possessed by the black symbiote; a ghost with knight and rolling-mass attacks; a modular colossus with independent arms, tentacles and possessed helicopter/Furnace transformations.
- Every broken form falls and erupts in exclusive black/red explosions. Music and the boss bar stop. An escape pause precedes rising fragments, fusion and the next gauge fill. Only the final return grants boss rewards.
- The final form has four complete life layers on Normal, Hard, Furious and Insanity. Warning/recovery timing, projectile speed, shield strength and wall durability vary by difficulty. Attack sequences have committed aim and open lanes.
- Generated binary bolts, shootable code bombs, dark-matter projectiles, tentacle strikes, reform effects and an opening/closing portal. The final portal returns the pilot to the sewer approach with four other pilots and an identity-aware radio welcome.
- Destructible data walls hold defensive lanes. Binary walls advance faster. Both begin between the pilot and boss, leave an open lane, show cracks and break into glyph fragments. Floating constructs bypass terrain-scroll movement; that correction is necessary for missiles to catch them.
- Binary shields fit the current rendered form, have their own gauge and Retina target, absorb hits before the hull, and visibly break. Hit tests and moving module locks resolve the same pose used by drawing.

## Art and rotations

Six new built-in image-generation source images are preserved in `_ART_SOURCES/realm_0930`. `build_realm_art_0930.py` reproduces 31 transparent runtime components/effect cells in `assets/game/realm_0930`. Equal animation cell origins are retained; wall/shield states share a row crop so damage states do not jump. Source briefs and reference identities are in `docs/realm_0930/art_provenance.json`.

Normal steering no longer selects the extreme bank/edge-on roll images. All nine pilots use the approved neutral hull through small 5-degree yaw steps. Explicit barrel rolls and somersaults keep their authored reels. Existing space-flight poses are preserved.

`rotation5_0930.js` resolves rotated actor blits into cached 5-degree sprites with stable padding/pivots. The 48 MiB cache has both source and per-angle eviction; generating all 72 angles of one large sprite cannot escape the cap. Non-orthogonal transforms remain an explicit fallback, counted by `ROT5.fallbacks` (zero in the focused native checks).

The local porting export contains **2,414 source frames / 1,996 deduplicated PNG pages**, each with 72 headings (0–355 degrees). Coverage includes packed enemy/boss/miniboss actor families, all normal pilot frames, newer modular encounter pieces, space-ship parts and masks, and anchored chaingun parts. The manifest includes source rectangles, scale, clockwise convention, cell size, stable center and hashes. Space palettes/luminance and separate masks preserve the nine pilot variants.

The export is **4.38 GiB** under `_ART_SOURCES/rotation5_0930`; it is not a runtime dependency. Regenerable PNG pages are ignored by Git, while catalog, metadata and the exporter are retained. The playable release collector follows registered runtime assets and does not collect this source archive. Source art is capped at a 384-pixel working edge for these pages; original high-resolution art remains unchanged. These are planar heading frames, not newly painted three-dimensional pitch poses.

## Verification

- Syntax checks: game, realm and rotation modules passed.
- Full suite with the new module loaded: **6,114 passing lines, final BUILD OK banner, 0 errors**.
- New regression cases cover takeover protection, all four difficulty profiles, four final life layers, shield interception, destructible gaps, false death without rewards, and fragment reformation.
- Native Chromium checks cover every attack family and three-form transitions; actual launched missiles reach the boss modules, shields and walls. Machine gun, laser, orb and chaingun fire damage the modular host through `updatePlay`.
- Nine-pilot steering contact sheet and all three forms inspected. Rotation page dimensions validated; no missing export assets. Warm colossus render sample: 4.2 ms median / 6.7 ms p95, including a pixel readback. This is a local focused render measurement, not an end-to-end performance guarantee.
- One earlier suite run exposed the old charge-hold fixture being interrupted by random enemy damage. The fixture now isolates charge ownership with protected player/no wave spawns; the full rerun passes. Production charge behavior is unchanged.

Evidence: `docs/qa/realm_0930.json`; screenshots here and `_shots/realm_*0930`; full test log `_shots/realm_0930/full_suite.log`.

## Reproduction and remaining review

Run from the repository root:

```
python _BUILD_SOURCE/build_realm_art_0930.py
python _BUILD_SOURCE/export_rotation5_0930.py
node _BUILD_SOURCE/test_fl.js
python _BUILD_SOURCE/probe_realm_0930.py
python _BUILD_SOURCE/probe_realm_combat_0930.py
python _BUILD_SOURCE/probe_realm_visual_0930.py
```

The exporter resumes completed entries. Remove a specific exported entry/page before intentionally rebuilding changed source art. Native probes use real game art and combat routes, but do not replace a human balance playthrough. Furious fight duration and the readability of the dense colossus attacks still deserve that playtest. Future anchor art or shear-based renderers need adding to the export catalog or resolving the counted fallback; do not assume the historical catalog covers new content.
