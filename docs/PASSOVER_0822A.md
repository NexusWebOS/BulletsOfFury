# 0822a — THE APOSTROPHE, AND THE HYPHEN NOBODY HAD NAMED

The standing "THEN LET,S SHOW THEM" item, closed. It was **two** glyphs, not one, and the second
was never on any list.

| item | before | after |
|---|---|---|
| `'` apostrophe | sat on the baseline, indistinguishable from `,` | hangs at cap height |
| `-` hyphen | sat on the baseline, read as an **underscore** | sits mid-height |
| `,` `.` `:` | correct | **pixel-unchanged** |

---

## 1. ONE ROOT CAUSE, AND THE LIST ONLY CARRIED HALF OF IT

`glyphBox` bottom-aligns every glyph in the cap box (`dy = H - gh`). `FONT_DESC` exists for glyphs
that hang BELOW the baseline; there has never been a counterpart for ones that hang ABOVE it. So
every mark that is not a baseline mark was dropped onto the baseline.

⚠ **THE HYPHEN HAD THE SAME DISEASE AND WAS INVISIBLE BECAUSE NOBODY LOOKED AT IT NEXT TO A
LETTER.** Rendering the whole punctuation row at once is what surfaced it — the apostrophe was the
only one reported, and fixing only what was reported would have shipped `MID_AIR` as an underscore.
The row costs the same as the single glyph. Render the set, not the complaint.

## 2. THE PLATES CANNOT ANSWER IT — MEASURED, NOT ASSUMED

CLAUDE.md said not to write this table from the argument, and it was right for a reason stronger
than caution: the stage-face punctuation cells are **tight slices with a zero-pixel margin on all
four sides** (measured — ink bbox == full cell for p39, p44, p46). A tight slice carries no
vertical placement at all. The plate literally cannot say where the mark belongs.

`fury-dialogue-font-map.json` — Mike's own 0819 pack — does carry it. Against `A` spanning y 2..16:

    glyph   bounds    slack   above   ride
    '       2..8      8       0       0.00
    -       8..12     10      6       0.60
    .       11..16    9       9       1.00
    ,       11..18    7       9       1.29

⚠ **THE DERIVATION VALIDATES ITSELF ON THE TWO GLYPHS THAT WERE ALREADY RIGHT.** `.` falls out at
exactly 1.00, which IS the existing bottom-align default. `,` falls out above 1.0 — below the
baseline — which is exactly what `FONT_DESC` already computes (comma height 7 − period height 5 =
2, the same drop). The same formula that moves `'` and `-` leaves `.` and `,` untouched, and the
after-render confirms they did not move by a pixel. **A table that reproduces the correct cases
before it touches the broken ones is the only kind worth trusting here.**

## 3. THE FIX

`FONT_RIDE` — the fraction of leftover cap-box space belonging ABOVE the glyph. 1 = baseline (the
default, correct for `.` `:` `!` `?` `/` and the brackets), 0 = hung from cap height.

    const FONT_RIDE = {"'":0.00, '-':0.60};
    let dy = (H - gh) * (ch && FONT_RIDE[ch] != null ? FONT_RIDE[ch] : 1);

Two glyphs listed. Letters are unaffected by construction — they are all exactly cap height, so
`H - gh` is 0 and the multiplier cannot move them.

⚠ **THIS IS THE STAGE-FACE PATH ONLY.** `msgTextLeft` tries `bmfDraw(_msgFace, ...)` first and
returns on success, so dialogue with the 0819 BMF face up was already correct — that face has real
per-glyph metrics. This path is what every `stageText` caller uses (banners, stats, menus, the
password screen) AND what dialogue falls back to during the decode window, since `msgFaceUse`
returns null while `bmfReady` is false. **Stage 2 is literally called "IT'S HOT IN HERE"**, so the
banner carried the bug in Mike's own stage name.

## 4. `+` DOES NOT RENDER, AND THAT IS A DIFFERENT THING

Visible as a gap in the probe row. `sfont1_p43` exists in the manifest, but `+` is not in the
face's glyph map, so `stageText` takes the unmapped-space fallback. Untouched here — not this bug,
and not verified beyond the one render.

---

## HOW TO VERIFY

    node --check assets/game.js
    node _BUILD_SOURCE/test_fl.js            # 2,702 ok / 3 fail — IDENTICAL to before this drop
    python _BUILD_SOURCE/shoot.py --state TITLE --script probe_glyph.js --warm 200 --seconds 2 --fps 2

The three failures are the known environmental ones (preload count, two `_superseded/` ledger
checks — that folder is not committed, so they cannot pass on a fresh clone). Baseline was taken
before the change and diffed after: same count, same three lines.

The probe draws `A'B A,B A.B A-B A+B A:B` through the REAL `stageText` with cap/baseline guides —
it does not recompute glyphBox, per the "a probe that recomputes the thing under test cannot find
the bug" rule. Before/after shots: `docs/proofs/glyphride_before_0822a.png` / `_after_0822a.png`.

---

# 0822a PART 2 — THE 680 PLATE: WHAT IS ACTUALLY TRUE

Mike asked whether the scrolling resolution is 680. Measured on all eight stages, in the renderer:

    stage        WORLD_W  zoom   viewW   pan    ratio
    1, 4, 5, 6      680   1.00   480.0   200    1.417
    2, 3, 7, 8      800   0.85   564.7   235.3  1.417

**Framing is 680 everywhere** — every stage shows the same slice of world and pans the same
proportion. But only four stages are LITERALLY 680; the others are 800 plates scaled 0.85 to fake
the same framing.

## THE CONVERSION IS NOT FREE, AND THE OBVIOUS ROUTE GAINS NOTHING

⚠ **RESIZING AN 800 PLATE TO 680 IS THE SAME x0.85 REDUCTION.** It drops the same 15% of columns;
it only moves when they are dropped, from runtime to build time. It recovers no detail. Any plan
that says "just convert the plates" has to answer this first.

⚠ **AND THERE IS NO LOSSLESS CROP.** Measured the keyed (magenta) padding on every plate:

    stage 2  nst2_master_v2         800x4800   0 keyed cols   content 800
    stage 3  nst3_master_v2         800x4800   29 L + 40 R    content 731
    stage 7  nst7_master_v2         800x4062   0 keyed cols   content 800
    stage 8  blackhole800_rc2       800x5120   0 keyed cols   content 800

The magenta visible in a mid-plate band is where the art does not REACH on those rows, not a
margin — three of the four have zero fully-keyed columns. Cropping to 680 costs 120px of drawn art
on 2/7/8 and 51px on 3. **The only lossless path is Mike re-exporting the four at 680**, the way
stages 4/5/6 arrived.

## THE MOTION ARTIFACT IS REAL — AND THE FIRST TWO PROBES THAT "SHOWED" IT WERE BOTH INVALID

⚠ **PROBE 1 MEASURED ANIMATION, NOT THE CAMERA.** It stepped `drawScene` between camX values, so
water, enemies and effects advanced between samples. Stage 2's sampled row also came back as a
single 960px run — a flat region with no texture. It measured nothing and looked like a result.
⚠ **PROBE 3 FAILED ON MY OWN ROUNDING.** It wrote camX through `toFixed(4)` and then tested the
result against a 1e-6 tolerance, so a correct snap reported OFF-lattice. **A tolerance tighter than
the precision you kept is a broken test, not a finding.**

The valid probe isolates the transform: real plate, real scale, no game loop, a row picked for
maximum colour edges. Stage 2, one textured row, camX stepped sub-pixel:

    raw      1px-runs 136 139 134 140 139 140   spread 6   5 distinct distributions
    snapped  1px-runs 136 136 135 135 137 137   spread 2   identical camX reproduces exactly

Stage 1 at its integer 2.00 factor: camX=122 is IDENTICAL to camX=120, and the interior widths are
always multiples of 4. That is the control, and it is what "stable" looks like.

## CAM_SNAP — A DIAL AT 0, BECAUSE FEEL IS MIKE'S

`ctx.translate(-camX)` is never rounded and camX is eased, so it is permanently fractional; at
scale 1.70 that is a moving sampling phase. `camSnap()` puts camX on the device-pixel lattice.
Verified in the live game over 174 frames on stage 2:

    CAM_SNAP=0   174/174 frames OFF lattice, worst error 0.492 device px
    CAM_SNAP=1   174/174 frames ON  lattice, worst error 2.8e-14

⚠ **IT IMPROVES THE CRAWL, IT DOES NOT ABOLISH IT** (spread 6 -> 2; the residual is window
clipping at the canvas edge, the same order stage 1 shows at its stable scale). ⚠ **AND IT
QUANTISES THE CAMERA to 0.588 world px per step** — crawl traded for possible judder. This file
records that how panning FEELS is Mike's call, so it ships at 0: the current camera line for line.

Suite with the dial added: **2,702 ok / 3 fail, failure list identical to baseline.**

## ALSO CORRECTED

`worldWidth()`'s comment claimed MASTER_W was "only the default for the plates still authored at
800 (stages 2 and 3)". It is 2, 3, 7 AND 8 — the note omitted the two widest plates in the game.
