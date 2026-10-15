# Smooth motion — authored source archive

`returned/` contains thirteen accepted built-in imagegen sheets. `prompts.json`
preserves their exact briefs and local reference paths. `reference/` contains
native renderer exports of the current 80 roster slots, the nine pilot ships,
Furyship, ship dimensions/nozzle rigs and Hammer electrical style reference.

`reels.json` owns source-cell assignments. `manifest.json` records source crops,
native canvas sizes, common pivots and translation registrations.
`provenance.json` records source/reference/output SHA256s and registry hash.

Rebuild the 208 cells and registry together with
`python _BUILD_SOURCE/build_smooth_motion_1009.py`. The builder only normalizes
authored pixels and makes the cobalt-only Furyship palette masks. It does not
create sprite geometry. No shared atlas is edited.

Reference exporters require `--refresh-reference` to replace existing source
references intentionally. They bypass this motion owner's replacement hooks
when capturing the original rig. Do not run them as part of ordinary rebuilding.

Live scope, encounter sequencing, native verification and remaining work:
`docs/SMOOTH_MOTION_1009.md`.
