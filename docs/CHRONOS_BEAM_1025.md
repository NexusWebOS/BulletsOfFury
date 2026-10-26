# Chronos rotary gun and unarmed rage — October25

Mike's latest direction supersedes permanent red hammer attacks: rage begins at 15% HP after the full charge, permanently discards the hammer, retreats into the background, gathers energy and fires two-handed waves. Restore landing FOV warnings for the regular/chromium depth jump. Keep the gun until destroyed, with its health bar and Retina target.

Final owner: `assets/chronos_beam_1025.js`, loaded after C29. Source/build owner: `_BUILD_SOURCE/build_chronos_beam_1025.py`; generated fixed-cell manifests and lossless sheets are C30_ART. No game.js edits in this pass.

The gun uses the stationary whole-body grip and minimal shared recoil. PixelLab generated sixteen physical rotary cluster phases including the muzzle face; the original receiver stays fixed. The prior build froze the muzzle below row187 and largely changed barrel shading. Rounds now use the authored native brass .50-cal tracer renderer at14x32 with10x24 collision and existing native MG audio. Gun HP, alpha damage/flash, Retina and destruction/recall remain native.

Charge alpha is cleaned to remove faint edge islands. Current-pose contour emissions, native energy bolts, a brief white release and shock ring strengthen the transformation. Red remains permanent. Whole unarmed casting keys were generated with GPT; PixelLab supplies nine hip-to-forward-palm thrust frames. The red actor retreats smoothly to .42 scale, commits a green/yellow/red FOV, thrusts both hands, and emits the authored cyan/white wave. Native segment damage respects seats and invulnerability. Actual scaled actor alpha owns damage; no ghost hammer target remains. Existing traced aura and hit flashes are preserved.

## Provenance

Sources: `_ART_SOURCES/chronos_beam_1025/`. GPT `cast-gpt.png` and `wave-gpt.png`. PixelLab rotor job `4e06f5ed-da45-4a0d-a41f-845a5becbd44`; thrust job `09f8bb2b-e6c0-4134-a5a2-2a12d4fa5bf1`. User GIFs were inspected frame by frame for anticipation, release and energy-wave posture. Character identity remains Chronos. Complete actor plates, uniform even256 cells/common128,90 pivot; rotor104x208/common54,46; wave192x384. Rebuild through owning Python compiler, not hand-edited manifest rows.

## Verification and review

- `_BUILD_SOURCE/probe_chronos_beam_1025.py`:19/19 native behavior checks.
- `_BUILD_SOURCE/probe_chronos_beam_pixels_1025.py`:8/8, including all sixteen distinct muzzle faces, visible projectile pixels, actual red-body damage and flash expiry, player contact damage and restored landing FOV.
- Inspected native screenshots and decoded recording frames for grip, rotation, charge, warnings, waves and hit flash/expiry.
- `_BUILD_SOURCE/record_chronos_beam_1025.py`:56-second audible Furious review. Invulnerability and labelled native checkpoints; **not a continuous full-fight clear**. Gun0–20s; destruction20s; depth jump/FOV27s; charge37s; background waves43s onward.
- `_BUILD_SOURCE/verify_chronos_beam_1025.py`:6/6 playback, decoded audio, recorded states and frame preview checks. No browser page/console errors. Local HTTP reset from cancelling the original metadata stream is expected in the blob-seek workaround.
- `node --check assets/game.js` and the new owner pass. Required `node _BUILD_SOURCE/test_fl.js` exits1 **before assertions/final summary** because `_BUILD_SOURCE/retired_art_archive_1022.cjs` is missing, matching the previously recorded blocker. No claim of full-suite success.

Review: `docs/previews/chronos_frames_1025/index.html?revision=rotary-rage-1025`. The previous C29 review is archived as `committed-gun-review.html`; preserve the metadata-cancel/blob playback workaround for reliable local seeking. Video and verification output remain under ignored `_shots/chronos_beam_1025/`. No commit/push.
