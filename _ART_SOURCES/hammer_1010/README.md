# Hammer Chromium and committed strikes — October 10

Mike requested that Hammer's background dive become dangerous only on the
player's plane, that damage no longer cancel the strike, that Chromium absorb
rather than reflect, and that shield/core/spike/side swing animation use the
Neo Geo treatment.

Generated with the built-in `image_gen` tool, in edit mode against the actual
single-headed Hammer reference. Exact generation prompts, including corrective
edits, are in `prompts.json`. All intact frames retain the head and two arms.
The whole boss identity and its existing encounter specifications remain.

`returned/` retains the selected original native RGBA sheets. The right raw
sheet is kept as provenance; the selected right edit removes rear appendages.
The first generated left reel faced the wrong direction and was not shipped.

`_BUILD_SOURCE/prepare_hammer_1010.py` owns the cropped/padded approved references.
`_BUILD_SOURCE/build_hammer_1010.py` owns the six banks and their registrations:

| Bank | Frames | Canvas | Fixed pivot |
| --- | ---: | --- | --- |
| Shield formation | 16 | 512 × 512 | 256, 224 |
| Right swing | 16 | 512 × 512 | 256, 224 |
| Left swing | 16 | 512 × 512 | 256, 224 |
| Chromium wall | 16 | 512 × 256 | 256, 128 |
| Core energy | 16 | 384 × 384 | 192, 192 |
| Energy spike | 16 | 256 × 512 | 128, 448 |

The importer crops/translates the existing native-alpha pixels and uses one
nearest-neighbor proportional scale per bank. It does not fit frames
independently, rotate/mirror the whole body, repaint edges or invent in-betweens.
Left swing rectangles are individually measured because poses cross the source
grid boundaries. Exported canvases/pivots remain fixed; source frames 10, 9, 8
are ordered into the continuous leftward release. Significant armor, head,
hammer and feet are kept within their own exported cells.

Shipping PNGs and their SHA256 manifest are under
`assets/game/levels/stage_05/boss/hammer_1010/`. Generated runtime metadata is
`assets/hammer_art_1010.js`; physical source translations are recorded here in
`registration.json`. New intact poses draw at the existing .70 body scale;
warning/damage tips use that same scale. No shared atlas was edited.
The side warning includes the entire measured curved release; the strike
retains its original 38-pixel impact width.

Native pixel contact sheets, actual gameplay contact/damage fixtures and timed
formation/side swing/orbital/spike clips are produced by
`_BUILD_SOURCE/probe_hammer_1010.py` through `shoot.py`. The test uses the game's
`XART.get` and its own canvas `drawImage`, not cached-canvas identity.
