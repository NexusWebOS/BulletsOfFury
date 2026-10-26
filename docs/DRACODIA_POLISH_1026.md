# Dracodia loop, fade, sound, speech and body polish - October26

Mike requested smooth initial/download loops, a frame-based 25% to 100% skeleton
fade before lightning, progressively louder strike sounds, one closing speech
roar/arm lift and an intact first-host body after arm destruction.
[Current audible 61.73s arm-break/transformation/full-speech recording](http://127.0.0.1:53746/_shots/dracodia_polish_1026/video/take-6c1b7f70/dracodia-final-transformation.mp4).
Earlier takes are preserved.

## Runtime

`assets/dracodia_polish_1026.js` loads after RD26. It blends adjacent cyclic
authored poses at 32 subframe steps, including last-to-first, using premultiplied
canvas composition. Three reusable source-sized canvases retain the actual
registered art, fixed pivots and proportional scale; no per-pose fitting or new
generated sprites. Rise and download share the existing continuous phase.
Carrier/material/wire loop seams are pixel-continuous. The 24 indexed opacity
frames increase the rising carrier from 25% to 100% before lightning begins.

Every original and ending strike beat receives rising shared-mixer gain.
The ending reuses the approved combatBeam0927 sample/pool through the separately
gated rd27Lightning cue (25ms gate), without adding a sound per secondary bolt.
Original 24 native beats remain. 57 actual recorded releases were accepted,
with strictly increasing requested gain from 0.20 to 1.00.
Decoded audio is audible at -3.7dB peak; the cinematic has no new
download, synthesized audio or pending effect timers.

The earlier FEAR ME line retains its text and uses face 4; only the last line
keeps face 5, the authored roar bank and native scream. Native speech runs to
completion into live combat. No dialogue lines are skipped.

## First-host body and arms

The old narrow arm/core strip removed crown/shoulder/body pixels together with
the arms. The owning stage78 builder now preserves the full-width upper body
and shoulders, with a lower anatomical arm seam. The same full 512 canvas and
source pixels remain. It also measures 90 opaque arm target anchors across 45
source poses; native non-muzzle part points use them. Claw muzzle/FOV sockets,
protected 33.3/33.3/33.4 budget, actual arm debris and hit flashes remain native.

The fall had a second problem: it returned to an older core-only plate after
core exhaustion. RD27 now draws the same complete connected recovery body
during that native fall, retaining actual destroyed-arm and flash state. The
original fall clock, protected rebirth, position, explosions and progression
remain with their owners.

Rebuild masks/targets/manifests/registry through
`python _BUILD_SOURCE/build_stage78_review_1025.py`. No atlas or paid generation
work was needed. Boss Cinematics has the current recipe and evidence reference.

## Verification

- 41 native Chromium checks pass: cyclic carrier/material/wire pixels,
  all 24 opacity frames, increasing beat gain, exactly one closing roar, actual
  intact upper-body pixels after arm damage, matching full-body fall pixels,
  all 90 opaque targets, native health/protection/reveal, real damaged pixels
  and flash expiry, no page/console errors. Native screenshots inspected.
- 25 recording and 8 playback checks pass. The film includes staggered
  actual arm breaks, collapse, rising/fading skeleton, download/lightning,
  whiteout, all native speech, one final roar and combat resumption. Decoded
  frames inspected; audio playback and Range seeking pass. Roughly
  59.3 native frames/s and no asset errors.
- JS/Python syntax and installed skill validation pass. Required test_fl.js
  exits 1 before assertions/final summary due existing missing
  `_BUILD_SOURCE/retired_art_archive_1022.cjs`; this is not a green full suite.

Use probe, recorder and playback helpers with `--polish`. Evidence:
`docs/qa/dracodia_polish_1026.json` and `_shots/dracodia_polish_1026/`.
The film uses explicitly labelled native damage checkpoints; it is not a full
boss fight. No game.js/test_fl.js edits, commit or push.
