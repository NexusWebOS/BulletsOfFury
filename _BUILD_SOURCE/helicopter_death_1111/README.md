# Helicopter accelerating death spirals — November11,2026

Mike requested that Dracodia's helicopter and the Stage1 helicopter on either difficulty spin uncontrollably, explode faster and faster, leave the screen, then shatter into visible debris with explosions trailing behind.

H126 replaces only those helicopter death visuals/directors. Native lethal damage and defeat owners still start each sequence. Whole airframes use64 offline yaw poses with baked rotor motion. The spin accelerates continuously, the wreck flies toward a lower side edge, and cook-off intervals fall from460ms toward55ms. Blasts stay at their emitted world positions to form a trail. Small actual-airframe pieces shed during the late spin. The final edge blast removes the hull and ejects real rotor/fuselage/pod pixel chunks, which tumble, travel offscreen and receive finite terminal explosions. No surviving hull fades or hangs in the air.

## Ownership and progression

- Stage1 applies to the actual damkeeper helicopter regardless of difficulty. Normal/Easy/Hard retain the actual critical metal body; Furious retains its existing green palette. Its original lethal-hit reward, Forge drop, enemy clear and post-helicopter raid remain native and occur once. Dam reveal remains at6.7s; the follow-up raid still opens at8.6s. The old stationary cook-off/fullscreen whiteout is replaced by the requested death spiral.
- Dracodia's form1 enters the native v19copyDeath state at real core exhaustion. Its visible spin/shatter lasts5.4s, then delegates to the original return/final-reform branch. Dead-copy HP remains0; main-life HP and remaining copies are never healed. Both non-final main-form return and last-copy terminal defeat were observed. Already destroyed pods remain absent through four authored hull variants.
- Dead wrecks expose no Retina targets or contact damage. Native weapon/lock cancellation remains in effect. Pause freezes motion, explosions and chunks together; native clear removes the copy's effect owner.
- Original game.js, Stage1 repair/raid owner, HC79 body/weapons, H125 weapon effects, D124 and native return code are byte-identical. No commit, push or installer.

## Authored source

Two appended owners: assets/helicopter_death_art_1111.js and assets/helicopter_death_1111.js. Packed images: assets/game/shared/combat/helicopter_death_1111/. Sources: _BUILD_SOURCE/helicopter_death_1111/.

1776 frames in176 banks and35 lossless PNG pages. Stage-scoped preload selects the appropriate hull family and shared explosions. Six spin families preserve the real hulls;166 actual-pixel fragments have eight authored tumble poses each. Four explosion sizes are exported directly from the approved H125 generated master. Source cells/pivots are fixed and even; all rendering uses ordinary integer source blits. Rotation, body/rotor combinations and chunk turns are baked offline, with no new runtime image rotation, scaling, tint, opacity animation, blend/filter or generated canvas effects. Reduced motion slows body/chunk rotation and skips the brightest explosion startup poses while preserving native timing/progression.

Eleven tagged Aseprite source documents and timeline.json preserve all banks. Thirty-three representative exports match integrated pixels exactly, including empty explosion ends. Actual Stage1 source textures/rotor frames were exported losslessly from XART; HC79 whole-body/pod sources and the original H125 explosion master remain archived with SHA256 provenance.

## Observed verification

78 scoped checks pass across native gameplay and source/export geometry. Native Normal and Furious Stage1 clips show the full sequence. Easy/Hard ownership and pause checks also pass. Checks cover accelerating spin/cook-off, a moving explosion trail, visible real-airframe chunks, once-only shatter/completion/reward, native dam/raid follow-up, Dracodia's main-life return without HP restoration, destroyed-pod identity, safe dead wrecks, pause/clear, reduced motion, complete preload, unchanged owners, and native last-copy final reform/terminal death. Completed browser captures have no page/console/draw errors. A socket reset printed only when one recorder closed its browser during HTTP teardown; the native checks and saved footage completed.

Required game.js and both new-script syntax checks pass. Required node _BUILD_SOURCE/test_fl.js still exits1 at the previously recorded missing difficultyHealthBaseline15 helper (combat_polish_0927b.js:151 / test_fl.js:4537), before its final summary. That unrelated failure remains unchanged.

## Finished media

helicopter-death-spirals.mp4 shows Stage1 Normal, Stage1 Furious, then Dracodia. Separate MP4/GIF clips are included. These are real-renderer encounter checkpoints with native lethal damage, an invulnerable presentation pilot and untouched death clocks during each chapter; they are not whole-campaign completion footage.
