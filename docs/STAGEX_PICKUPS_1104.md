# Stage X pickups — November4

Generated a dedicated chrome, gunmetal, royal-blue and amber power supply box (P) and horizontal speed capsule (S with chevrons). Built-in image_gen created the source sheets after SpriteCook and PixelLab connection preflights failed; no external-service generation is claimed. Raw sources are preserved. Aseprite cleaned the exterior matte, retained enclosed ivory lettering, selected one canonical shell per item and exported8 blue-light palette frames plus a white hit cell. Static silhouettes, fixed pivots, binary alpha and even64/36 cells keep text readable without wobble. Frame duration100ms, idle0–7, hit8. Capsule/power use64cell; loose speed uses36cell.

assets/stagex_pickups_1104.js follows the authoritative stageXArenaActive() predicate, covering Rival24 and both campaign routes while leaving regular Stage6 and all other stages unchanged. Native drawCrate/drawCapsule owners are wrapped; only loose speed is filtered for its dedicated drawer. Source-over/integer blits; no runtime alpha/glow/scale/rotation. Native box/capsule HP, random reward selection (including shield outcomes), hit flash timer, collection, speed1–5 cap and sounds stay unchanged. Native fallback remains while the new art loads. One index script was appended; game.js is untouched by this pass.

Sources/rebuild: _BUILD_SOURCE/stagex_pickups_1104/build.lua (Aseprite --batch --script, hidden/waited process). Source-generated PNGs, editable .aseprite files and metadata are stored alongside it. Runtime PNGs are assets/game/levels/stage_06/pickups/stagex_1104/. Original generation images were not overwritten. Boundaries, alpha and static silhouettes were inspected at native scale.

23 focused native Edge checks and39 asset checks pass. Verified all8 crate frame rects at fixed size, authored white hit selection, capsule/loose speed draws, both Stage X route flags, unrelated-stage exclusion, actual bullet damage/hit flash, native break/reward, speed0→1 and cap5. Native page/draw errors:0. The QA fixture starts after the protected Stage X entrance card; no gameplay entrance change was made. Native screenshot/evidence: _shots/stagex_pickups_1104/.

Syntax checks pass. Broad required test_fl.js still exits1 at its existing missing difficultyHealthBaseline15 helper in combat_polish_0927b.js:151, before summary. This is not a green full regression suite. No commit/push.


## Superseded power-box animation

The original power light loop was replaced by a genuine16-view yaw turn and16 angle-matched hit cells after Mike requested rotational frames. Speed artwork stays upright. Current rebuild and evidence: STAGEX_BOX_ROTATION_1104.md.
