# Fury pilot performances and framed Chronos portrait — November 2

Mike approved the nine pilot identities in the first cast gallery and requested seated/dispatch scenes, walking/running, emotional and physical reactions, illustrated shots with their own ships, a dialogue portrait for Chronos, and GitHub publication.

This adds 198 transparent full-body frames (22 per pilot), bringing the library to 252 pilot frames, plus nine 1536×1024 illustrated hangar stills and one 512×512 framed Chronos dialogue portrait. Cole, Axel, Decker, Maverick, Freezer, Juggernaut, Yuri, Lizzie and Falva retain their approved faces, clothes and glasses. The canonical visible spelling remains CHRONOS; legacy cronos IDs are preserved. His ribbed compact helmet, outward horns and curved cyan U-shaped visor fill the dialogue bezel.

Each pilot now has:

- Four walking and four running stride keys.
- Seated idle/speaking/laughing and side-on dispatch, typing and command poses, including authored chair/console props.
- Sad, angry, ecstatic, happy, airborne cheering, falling, standing laughter and floor laughter.
- One illustrated scene with the pilot in front of their reference-matched aircraft.

The aircraft scenes were generated from freshly exported, visually inspected current game aircraft, including top/front/rear views. They are illustrations guided by those references; the original aircraft sprites remain the live movement assets. The low-resolution native hangar compositions used as generation guides are retained separately from the selected illustrations.

## Sources and rebuilding

Built-in `image_gen` produced the 37 source images: one portrait, 27 character sheets and nine ship scenes. Exact prompts, image roles and reference paths are retained in `_ART_SOURCES/cast_performance_1102/prompts.json` and `specs/`. Original generated PNGs are in `generated/`; native aircraft exports, identity boards, hashes and composition guides are in `references/`.

Run these in order:

1. `python _BUILD_SOURCE/build_cast_cinematics_1102.py` only when rebuilding the original54 poses/four heads.
2. `python _BUILD_SOURCE/build_cast_performance_1102.py` for the expanded banks, selected illustrations, framed portrait, manifests and registry.
3. `python _BUILD_SOURCE/build_cast_gallery_1102.py` last, to combine both libraries into the expanded review.

`export_cast_ships_1102.py` records current native aircraft via `XART.get` and the actual game context. `record_cast_ship_scenes_1102.py` recreates the native composition guides under the source reference directory, so it cannot overwrite selected illustrated runtime scenes.

Runtime output is `assets/game/shared/cinematics/cast_performance_1102/`. Individual actor PNGs are768×1024, common pivot384,960. Each source bank uses one proportional scale. Locomotion uses a measured hip projection for horizontal registration; airborne cheering reserves100px above the ground, and two running keys reserve32px. Seated/floor poses retain their lower silhouette. Connected actor/prop masks exclude neighbouring sheet fragments; alpha<=8 matte residue is discarded. Source PNGs are unchanged. Lossless WebP sheets, measured rectangles, common scales and SHA-256 hashes accompany exports. No shared atlas changes.

`assets/cast_performance_1102.js` extends the existing lazy `BOF_CUTSCENE_CAST` library. Call `key(pilot,pose)`/`draw(pilot,pose,x,ground,height)` or `stride(pilot,'walk'|'run',seconds,x,ground,height)` for authored four-key movement. These are staged cutscene stride loops, not a new gameplay locomotion system. Existing scenes remain directed by their native owners. The four native Chronos portrait aliases now choose the framed close-up; dialogue timing, combat and ending whitening retain their original owners.

Review `docs/previews/cast_cinematics_1102/standalone.html` directly with no server, or use `index.html` through an existing repository server. The gallery has all nine pilots, six categories, stride playback/pause and dark/light/checker backgrounds. Portable embedded previews use half-size actor thumbnails and perceptual WebP compression; full-resolution PNG links, source PNGs and lossless runtime sheets remain available.

## Verification

The expanded native Edge Chromium probe passes **313/313**, with zero page/console/missing-asset errors. It covers every new actor through `XART.get` and the game's own `ctx.drawImage`, all four Chronos aliases by rendered-byte equality, all nine illustrated scenes, visible jump/floor silhouettes, distinct stride keys and actual changing preview pixels. All gallery categories, local-file loading, mobile overflow, missing assets and page/console errors are checked. Evidence: `docs/qa/cast_performance_1102.json`; screenshots/contact sheets are under ignored `_shots/cast_performance_1102/`.

The original cast probe passes **79/79**, with zero page/console/missing-asset errors. It also checks actual first-contact and compact dialogue, native trap speech, ending whitening, the original54 poses/four heads and pilot portrait selection. Evidence: `docs/qa/cast_cinematics_1102.json`. Final check counts are recorded in these receipts. Source and native screenshots are visually inspected; pixel assertions do not independently certify likeness or smooth anatomical interpolation.

JavaScript syntax checks cover `assets/game.js` and all cast runtime/registry files. The required full `node _BUILD_SOURCE/test_fl.js` still exits1 before assertions or its final summary because `UNUSED_ASSETS/retired_art_1022/manifest.json` is missing, matching the recorded baseline. This task does not change `assets/game.js` or the full-suite fixture. Existing unrelated staged/unstaged/untracked work is preserved; publication is limited to the requested cast work.
