# Dracodia DNA palette and drone conversion review - October26

Mike requested the DNA code match his final-form palette, then a recording of
the drone transforming into the first combat form for review.
[Current audible 14.95s drone-to-phase1 film](http://127.0.0.1:53746/_shots/drone_host_1026/take-c2a01a4b/drone-to-dracodia-phase1.mp4).
Conversion begins at 4.46s; phase1 combat starts at 8.92s.
The existing conversion is 4.3 native seconds. This pass records that entrance
as-is; it does not redesign the drone conversion.

## Palette

The DNA-only palette now matches the final form's dark violet metal,
red-magenta energy and pale highlights. The canonical final-body reference
and actual rendered palette were inspected. Green-biased pixels in the 12
code and 32 liquid frames are mapped through a luminance-preserving ramp.
Neutral/dark metal, source alpha, frame sizes, pivots and proportions remain.
The maximum decoded luminance error is 0.4934 on a 255 scale;
all 44 decoded cells preserve exact alpha. Original 44 green sources remain
byte-identical for their existing arena/ending owners.

The owning DNA builder creates two isolated palette sheets and registers
`assets/dracodia_dna_palette_1026.js`. The runtime uses cached source-sized
cells only for RD28's strands, fluid and skeletal code fill. Stage8 preloads
the two palette images; no runtime pixel-color processing or green-source
replacement is needed. No shared atlas repack or paid generation.

Rebuild with `python _BUILD_SOURCE/build_dracodia_dna_1026.py`. Source hashes,
palette stops, per-cell alpha/luminance checks, sheet metadata and hashes are
in `_BUILD_SOURCE/dracodia_dna_1026/source-manifest.json`. The builder also
owns the rd28p_ taxonomy registration. Native palette preview:
`_shots/dracodia_palette_1026/probe/native-11.5.png`.

## Drone recording and verification

`record_drone_host_1026.py` captures from native entrance time 0 through portal,
drone arrival, complete conversion and six seconds of first-form combat.
No damage fixtures, phase changes or animation timer skips are used. Cole
observes with idle controls/weapons and God mode; native boss health and all
parts remain full in combat. Dialogue, conversion shriek and combat sounds
play through their original mixer routes.

- 48 native cinematic checks pass, including actual violet/magenta DNA
  pixels and all prior formation, health, body, loop, fade, audio and roar checks.
- 10 recording checks and 6 playback checks pass. The film fully
  decodes at about 59.5 native frames/s with -7.3dB sound,
  Range seeking and no page/console/asset errors. Native palette and decoded
  drone contact frames were inspected.
- JS/Python syntax and installed Boss Cinematics validation pass. The full
  test_fl suite still exits 1 before assertions/final summary on existing missing
  `_BUILD_SOURCE/retired_art_archive_1022.cjs`; it is not green.

Reproduce native palette verification with the existing cinematic probe's
`--palette` flag. Use `record_drone_host_1026.py` and
`check_drone_host_video_1026.py` for the entrance recording/playback.
QA: `docs/qa/dracodia_palette_drone_1026.json`. Earlier takes remain.
No game.js/test_fl.js edits, commit or push.
