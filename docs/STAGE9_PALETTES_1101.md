# Stage9 fleet palette separation / November1

Mike requested distinct black/blue, purple/pink, black/pink and related colors
instead of a uniformly teal roster. Ten existing designs now use selected
material ramps through the original source builder:

| Palette | Models |
| --- | --- |
| Black / cobalt blue | Interceptor, Jumper, Water Harrier |
| Violet / pink | Ring Spinner, Laser Ring, Prism Beam, Prism Orb |
| Black / rose pink | Gate Vessel, Gravity Leech, Prism Minelayer |

The other nine identities retain their selected art: pink Comet, pink/blue Manta,
liquid blue Current Breaker, Beacon, Beam Gunship, Water Skimmer, Echo Fighter,
Singularity and Tidal Fighter. Their exact bank metadata/hashes are unchanged.
All projectile, beam, mine, grenade, muzzle, exhaust and splash banks retain
their authored colors. This is a hull/material pass, not the queued dark-weapon
variant pass or a change to the biome.

Built-in ImageGen produced the selected three-ship material guide. Its exact
prompt/output is in `palette-generation.json` beside `palettes.json` and the
workspace PNG under `_BUILD_SOURCE/stage9_amplify_1101/`. The generated guide is
a color reference only; none of its new raster geometry replaces live hulls.
The selected ramps transfer through `build_stage9_amplify_1101.py` before the
existing directional banks are packed. The same ramp applies to every hull and
module frame; source-derived glow/shield masks retain exact alpha. Black metals
retain ordered shading, unchanged dark contours and brightest specular tips;
energy colors retain measured luminance. No runtime filters or sprite rotation.

The owning manifest retains19 models,177 even-cell banks and23 shape sources,
plus the separate palette guide.96 recolored banks assert exact alpha retention.
All19 model geometries, cells, pivots, scale, module joints and gun sockets are
unchanged. There are no game.js, attack, HP, cue, hit-flash or collision changes.

`probe_stage9_palettes_1101.py` passes35 native Chromium/export checks: retained
banks/geometry, actual blue/pink rendered pixels, real hit damage or shield
absorption with white pixel flash and expiry, native attack releases, gun-mouth
alpha and no game/asset/console errors. Native screenshots/contact sheet are in
`_shots/stage9_palettes_1101/`.

Recording, partial local publication and decoded playback are owned by
`record_stage9_palettes_1101.py`, `publish_stage9_palettes_1101.py` and
`verify_stage9_palette_preview_1101.py`. They replace only the ten affected clips;
all144 unrelated guide cards and nine other Stage9 clips remain exact, including
Current Breaker's overhead-flight film. The observer uses native movement input
and labeled invulnerability, without enemy HP/phase/attack-clock writes.

Review: http://127.0.0.1:8805/current/stage9-water-refit-1101.html#enemy=stage9-s9prism

Syntax passes. Required full test_fl exits1 before assertions/final summary on
the pre-existing missing ignored `UNUSED_ASSETS/retired_art_1022/manifest.json`.
No commit or push.

Published playback passes14/14 additional checks (49 focused checks total).
The ten fresh films total167.79s at59.6–60 native fps, with full H264/AAC
decode and audible PCM peaks0.311–0.362, without clipping or browser errors.
All154 guide cards remain;144 unchanged cards and nine other Stage9 films
are verified exact. Playback screenshots and publication.json retain receipts.
