# Chronos avatars and Fury full-body cutscene poses — November 2

Mike asked for Chronos face avatars that resemble the actual character, followed by pseudo-3D full-body poses for every pilot.

The approved cast is now expanded in [CAST_PERFORMANCE_1102.md](CAST_PERFORMANCE_1102.md): 198 additional body frames, nine illustrated pilot/ship scenes and a framed dialogue close-up. The same gallery combines both libraries. The four dialogue aliases now select that framed close-up; the original four unframed heads remain available. Run the combined gallery builder last after rebuilding either art library. The details below describe the original source bank and its verification.

## Delivered art and live routing

Built-in `image_gen` produced four Chronos head-and-shoulder views and six complete full-body key poses for each of the nine Fury pilots: Cole, Axel, Decker, Maverick, Freezer, Juggernaut, Yuri, Lizzie and Falva. Body poses are neutral, speaking gesture, salute, walking turn, rear look-back and back neutral. These are six individual authored poses, not a smooth turntable or an interpolated walk/talk animation.

Chronos follows the current canonical `_ART_SOURCES/chronos_motion_1025/keys-regular.png`: ribbed rounded dome, outward temple horns, one curved blue visor, rounded gunmetal shoulders and circular blue reactor. The former separate-eye/long-faceplate avatar is preserved on disk. Existing keys `fb1002_hammer_portrait`, `fb2_hammer_avatar`, `h3_hammer_portrait` and `cin30_cronos` now resolve the new neutral head. His three other views are registered separately. Native speech, portrait whitening, combat, HP and ending owners remain authoritative.

Pilot faces come from current `pilotPortrait(pilot,'idle')` pixels exported through `XART.get` and a Chromium canvas. Existing complete body art supplies clothing. Yuri explicitly follows the mohawk/bearded portrait rather than the obsolete young black-haired body head. Maverick and Juggernaut keep their current portrait aviators. Cole retains his approved mature face and olive harness suit; the other distinct costumes and glasses are retained.

The pilot frames are a lazy, opt-in cutscene library. Existing scene performances have not been globally replaced. Future scenes can request `BOF_CUTSCENE_CAST.key(pilot,pose)` or draw through `BOF_CUTSCENE_CAST.draw(pilot,pose,x,ground,height)` in the native context. No new animation loop or static-sprite rotation is used.

## Source and export ownership

- Exact prompts: `_ART_SOURCES/cast_cinematics_1102/prompts.json`.
- Original generated PNGs: `_ART_SOURCES/cast_cinematics_1102/generated/`.
- Identity references/native portrait export receipt: `_ART_SOURCES/cast_cinematics_1102/references/`.
- Native reference exporter: `_BUILD_SOURCE/export_cast_refs_1102.py`.
- Rebuild: `python _BUILD_SOURCE/build_cast_cinematics_1102.py`.
- Runtime PNGs/lossless WebP sheets/manifest: `assets/game/shared/cinematics/cast_1102/`.
- Registry/runtime: `assets/cast_cinematics_art_1102.js`, `assets/cast_cinematics_1102.js`.
- Standalone review: `docs/previews/cast_cinematics_1102/standalone.html` opens directly with all images embedded and needs no server. The smaller `index.html` is also available when reviewing through an existing repository HTTP server.

Every body frame is512×1024 with a common256,976 ground/support pivot; every Chronos frame is512×512 with a common256,480 lower bust pivot. The horizontal body pivot projects the main hip silhouette to the boot baseline, avoiding the lateral jump caused by measuring just one lower boot in a turning pose. Each bank has one proportional source scale. Measured connected-figure rectangles prevent the walking toes from being clipped at the generator's nominal cell edges. There is no per-frame fitting, mirroring or part reconstruction. Only alpha<=8/255 export matte residue is discarded; source files are unchanged. The red fringe visible in source-image inspection is largely alpha1–5, and is absent from the native exports. Source rectangles, pivots, scale and source/output SHA-256 hashes are in the manifest. No shared atlas is edited.

## Verification and limits

`node --check` passes for `assets/game.js` and both new JavaScript files. `_BUILD_SOURCE/probe_cast_cinematics_1102.py` passes79/79 in actual Edge Chromium, with zero page/console/missing-network-asset errors. It checks all58 images via the game's own `XART.get` and `ctx.drawImage`, source/export bounds, all four live Chronos aliases by actual rendered bytes, native ending portrait whitening, actual first-contact/trap owners, unchanged pilot portrait selection, all gallery tabs, mobile overflow and direct local-file use of the standalone gallery. All nine six-pose native strips, the first-contact and compact dialogue images, and the light-background gallery were visually inspected. The probe accounts for the game's `{alpha:false}` context by measuring against a known RGB background rather than asserting transparent canvas bytes.

Durable QA: `docs/qa/cast_cinematics_1102.json`. Native screenshots/logs: ignored `_shots/cast_cinematics_1102/` and `_shots/cast_cinematics_1102-*.log`.

The required full `node _BUILD_SOURCE/test_fl.js` exits1 before assertions or final summary because `UNUSED_ASSETS/retired_art_1022/manifest.json` is missing, matching the current recorded baseline. The older `probe_dialogue_fit_1020.py` also exits1: it has existing layout assertion failures and then throws in its fixture at `ui20Polygon` because an expected polygon is undefined. An A/B run excluding only the two new cast scripts reproduces that same exception and assertion-failure names; the unrelated existing probe/runtime is not rewritten in this art task. Both logs are retained. No whole-campaign playthrough or personal-likeness approval is claimed by pixel assertions.

Existing dirty work is retained. No `assets/game.js` or full-suite edits, commit or push.
