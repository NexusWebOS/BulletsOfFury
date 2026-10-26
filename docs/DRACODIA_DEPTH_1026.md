# Dracodia depth download — October26

Latest revision: [accelerating loops, flash-covered reveal and Boss Cinematics skill](DRACODIA_CLIMAX_1026.md).
It supersedes the preflash settling described below; this earlier evidence remains archived.

Mike requested downward lightning strikes, electricity swirling around the body,
and new forming views that turn in depth like the floating skeletal carrier.
[Current audible 36-second recording](http://127.0.0.1:53746/_shots/dracodia_depth_1026/video/take-31d5ec7b/dracodia-final-transformation.mp4). Earlier recordings are preserved.

`assets/dracodia_depth_1026.js` loads after the existing download owner and its
new art registry. The body remains upright while front, profile and armored-back
poses rotate around its vertical axis. The original 24-pose skeletal carrier
stays visible inside unbuilt bands. Completed bands reveal the matching material
view; the final front view blends into the actual native ce20Body renderer before
the whiteout. A shared chest anchor, native scale and continuous position carry
the completed body into speech.

The electrical wrap uses separate rear and foreground helix passes around the
body. Main strikes start above the playfield and travel downward through and
below the assembly. Both use the existing authored blue lightning art. Native
24-beat timing and shared-mixer lightning cues remain; there are no extra queued
sounds or new damage owners. Five form pools, protection, the 25.6s arena reveal,
28.5s speech handoff, native combat hits and defeat remain with their existing
owners. The fusion cue remains combatEnergy0927.

## Art and rebuild

SpriteCook pixel-engine-v1.5 generated 12 transparent 286x286 poses from the
exported actual 320x320 final-body reference. The paid job used 26 credits.
Reference asset: `f2f2d956-f64b-444c-8bb3-c495f7b43e74`.
Animation asset: `f6a6647c-3094-4e1d-a634-7c4af5598e80`.
Job: `b86c6abb-b05f-4e57-9679-e77e16c59fab`.

The compiler selects source poses 0–8 from front to back, then reflects 7–1 for
the opposite half. This produces 16 continuous depth views without the generated
late back-to-front jump. Every cell uses the same 512x512 canvas, 256,256 pivot,
one scale of 1 and fixed 113,117 source translation. There is no per-frame fitting.
The wire layer comes from the source alpha edges/material creases. Original and
normalized contact sheets were inspected before native activation.

Run `python _BUILD_SOURCE/build_dracodia_depth_1026.py` to reproduce the two
2048x2048 sheets, art registry and registered taxonomy entry. Source files,
generation settings, hashes, source selection and runtime cells are in
`_BUILD_SOURCE/dracodia_depth_1026/`; runtime copies and manifest are under
`assets/game/levels/stage_08/boss/dracodia_depth_1026/`. No signed URLs, new atlas
edits or generated player aircraft are involved.

## Verification

- 24 native Chromium checks pass, including actual depth-view pixels,
  narrower profiles, different back art, upright orientation, visible rear/front
  swirl pixels, downward strikes, all 24 native beats, preserved health pools,
  continuous speech position, actual white hit pixels and normal flash expiry.
  The first carrier matches exactly; the completed renderer comparison differs
  by 62 pixels on its 245760-pixel capture, within the existing render tolerance.
- All 15 recording checks and 6 playback checks pass. The 36.05s film
  fully decodes, has -5.1dB audible sound, runs at roughly
  59.1 native frames/s, and plays/seeks with audio in Chromium.
  The decoded film contact sheet was inspected. No page, console or asset errors.
- JavaScript syntax checks pass. Required `node _BUILD_SOURCE/test_fl.js` exits 1
  before assertions/final summary because the existing
  `_BUILD_SOURCE/retired_art_archive_1022.cjs` helper is missing.

Reproduce with the existing probe, recorder and playback helper, each with
`--depth`: `probe_dracodia_download_reveal_1025.py`,
`record_dracodia_transformation_1025.py`, and
`check_dracodia_transformation_video_1025.py` under `_BUILD_SOURCE/`.
Evidence: `docs/qa/dracodia_depth_1026.json` and `_shots/dracodia_depth_1026/`.
The video is a native-damage transformation checkpoint, not a full boss fight.
This pass did not edit game.js/test_fl.js, commit or push.
