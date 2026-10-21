# Boss redesign — October 20, 2026

Implemented in the main Bullets of Fury coding folder. Preview: `_shots/boss_redesign_1020/review.html`.

## Encounters

- Phoenix: whole connected left/right wings, complete left/right legs and talons, separate skull, body and tail. Original collar/hip material underlaps the joints. Two added heavy cannon pods have their own HP, alpha targets, flashes, muzzles and debris. Both pods must be destroyed before the four-corner Swoon book begins. The torso retains the original copied-form main HP budget; side-module damage also damages that budget.
- Swoon: depth recession, offscreen departure, nonrepeating random X-corner entries, committed diagonal paths, real swept talon contacts, return and recovery. Breaking wings reduces the number of dives and slows the surviving passes. Asterisks and angled arrows sit clear of the top HUD and lower boss bar. This corner-only glyph is Mike's explicit exception to the ordinary no-arrow-box instruction. There are no muzzle-anchored arrow boxes. The copied form's fire rotor is retired; the original campaign volcano boss is unchanged.
- Helicopter: randomized X and + route directions, machine-gun strafes, two full gun/missile orbits with a warned reversal, ascent and a fast top bomber pass. Corrupted atomic missiles have fixed targets, radius at least220, staggered nonoverlapping blasts and an upper opposite-corner escape. Real muzzle flashes follow the living gun modules. Destruction cancels pending owned attacks.
- Stage5 Hammer: chrome-and-blue identity retained. PixelLab entrance, overhead motion, side swings, spins, dance, throw and held-chaingun reels replace retired body recordings. The existing spikeball and approved recovery reel remain. The measured side-counter solver reads the actual new hammer-head coordinates. The native controller, armor, cooldowns, password clock and shield behavior remain authoritative. Duplicate actor/wall drawing is suppressed only within the old body draw scope.
- Chaingun pickup: special-style crate, physical hammer strike, the actual `micon_chaingun_1`, icon absorption and white transition into a held gun. There is no back-mounted gun. Stage8 uses the same choreography with its corrupted appearance.
- Code Hammer: Dracodia skull/code-heart identity, two-handed energy hammer, absorbing digital shield, charge volleys, side attacks, spin, independent thrown hammer, remade rotating spikeball, and the held gun. The skystrike leaves the screen and lands on a committed target; code waves travel left/right. The impact and both wave paths are warned.
- Final break: knee snap, trembling energy core and throw, three-quadrant luminaire blast with a named safe quarter. The field is committed in world space and cannot follow the scrolling camera. The safe quarter is adjacent to a living pilot's current quarter. The subsequent crossed-arm fire charge permanently removes the hammer; the remaining book uses actual alternating fist positions and two-fist ground slams with scattered fire.
- Phase gates at65% and28% prevent burst damage from silently skipping the new choreography. The digital field visibly absorbs capped damage. Directly breaking the hammer may trigger the final break early as a reward; it cannot restore the weapon later.

## Input and transitions

Removed the two `retinaScanHeld()` exclusions from left/right roll detection. Native roll and somersault cooldowns, pilot availability and Lizzie's heavy-mount restriction remain. Real browser keyboard tests cover acquiring, locked and queued Multi-Retina states, left/right rolls and somersaults for both seats.

Intact copied forms use matching PixelLab download meshes. A damaged Phoenix or hammerless rage return derives an outline mesh from its current authored rig once and caches it, capped at six layouts. A download cannot briefly resurrect a broken cannon, wing or hammer. Live native armor and the mesh share a pivot and progressive scan. No new paid generation is needed for each damage combination.

## Human-readable asset ownership

- Stage5 blue body/gun/action/counter PNGs: `assets/game/levels/stage_05/boss/hammer_redesign_1020/`.
- Stage8 corrupted Hammer PNGs: `assets/game/levels/stage_08/boss/hammer_redesign_1020/`.
- Stage8 whole Phoenix parts, pods and warning glyph: `assets/game/levels/stage_08/boss/phoenix_swoon_1020/`.
- Shared family registry: `assets/game/shared/boss_redesign_1020/manifest.json`; runtime registry `assets/hammer_redesign_art_1020.js`.
- Original inputs, generation IDs, accepted raw clips and normalization decisions: `_ART_SOURCES/boss_redesign_1020/`.
- Earlier duplicate exports from this pass are archived under `_ART_SOURCES/boss_redesign_1020/retired_exports/`, outside runtime assets. No unique source art was deleted.

Fixed canvases and one pivot per bank are preserved. No per-frame fitting. Clipped outgoing throw frames become the native independent weapon. Stray chaingun helmet/leg sparks were removed while retaining the approved body and moving held barrel. Sixteen counter poses reuse nine decoded images per direction, saving14MiB compared with32 separate512px images. Missile art and attack recordings preload before combat; audio uses existing shared mixer/retrigger gates.

Builders: `_BUILD_SOURCE/build_phoenix_swoon_1020.py`, `_BUILD_SOURCE/build_hammer_redesign_1020.py`, `_BUILD_SOURCE/build_dracodia_download_1019.py`. Every PixelLab job ID is preserved in the provenance ledger. Observed balance before/after generation: $7.24/$6.27.

## Verification

- Complete `_BUILD_SOURCE/test_fl.js`:8,938 checks, final BUILD OK banner, zero errors and exit0.
- Native Edge attack/module matrix:163/163.
- Native damage, escape, warning, audio and download checks:76/76.
- Real keyboard/co-op Multi-Retina checks:21/21, including cooldown enforcement.
- Native Stage5 physical counter and stance feedback:18/18.
- Total:278 native checks; no page, renderer or update errors in the saved reports. Eleven approved sound routes were decoded and played through the native mixer.
- Required game syntax check and new-script syntax checks passed.

Reels, actual PNG frame viewer, per-module exports, complete logs and JSON reports are linked from the review page. These are scripted encounter tests across Easy/Normal/Hard/Furious, not a claim of full campaign or no-hit completion. Browser QA here used Edge; no new Firefox performance claim is made.

Existing unrelated game/Overdrive changes were preserved. No commit or push was performed.


## Regenerated corner warning

Mike rejected the original square/star and arrow tile. PixelLab Pixen job
`c8a76938-b76b-466a-b2e5-6f05e6fb092c` supplies the new eight-point asterisk
and ivory/amber diagonal arrow. Original rejected source is preserved beside
the replacement. Fixed64x64 canvas and32,32 pivot; transparent border; original
corner positions, rotation, timing and FOV owners retained. New versioned PNG
and registry script URL avoid stale browser art. Generation cost: $0.0077.

Focused native Edge verification13/13, no browser/draw/missing-asset errors:
all four arrows point toward the opposite corner, visibly draw the new image,
and stay clear of HUD bars. Actual native captures and enlarged review tile:
`_shots/boss_redesign_1020/corner-warning-v2-*`. Initial fixture results are
retained: two angle expectations had reversed canvas-Y signs; the fixture now
uses the existing threaded-server queue setting and handles its unused favicon.
No gameplay timing, damage or difficulty changes. Earlier278/8938 results
above describe the completed encounter pass; they were not rerun for this icon.


## BOF chevron warning variants (current, replaces Pixen warning)

Mike requested the built-in image generator and the existing BOF arrow/asterisk
designs. The image generator received the actual orange triple-chevron escape
arrow and hollow yellow impact asterisk as references. The selected generated
three-chevron arrow is proportionally normalized and oriented down-right; the
original hollow asterisk is reused directly. Four64x64 fixed-canvas diagonal
exports share32,32 pivots. Native rendering continues using the existing quarter
turns, marker positions and FOV/timing owners; no gameplay changes.

Sources, raw generated master, exporter, references and exact prompt records:
`_ART_SOURCES/boss_redesign_1020/corner_warning_v3/`. Versioned runtime image:
`assets/game/levels/stage_08/boss/phoenix_swoon_1020/corner_warning_v3.png`.
Focused native Edge checks13/13 with zero browser, draw or missing-asset errors;
all four directions, visible native pixels and HUD clearance verified. Preview:
`_shots/boss_redesign_1020/warning-variants-v3.html`. Earlier Pixen and crude
warning sources remain preserved as rejected art. No additional PixelLab calls.
