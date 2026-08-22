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

---

# 0822b — THE LAST TWO TESTER ITEMS ARE BOTH ALREADY DEAD

Re-measured before working them, per the pattern this file keeps recording. Both are closed, and
the measuring turned up one thing that IS live and was on no list.

| item | verdict |
|---|---|
| a waterfall in the middle of the road | **DEAD** — zero fall blits on any of the eight stages |
| signs that scroll when told not to | **DEAD** — the only signs are stage 4's, already switched off |
| the `+` glyph not rendering | **NOT A BUG** — no game text contains one |
| stage 2 lava fall / stage 7 sludge fall | ⚠ **NEVER RENDERED, and that is new** |

## 1. THE WATERFALL — GONE TWICE OVER

`FALL_FOR` is `{2:'nlf_lava', 7:'nlf_sludge'}`. Stage 4's entry went in 0810f (Mike, twice: "why
the waterfall is still on level 4") and stage 1's in 0819d. Instrumented `ctx.drawImage` inside
`drawLiquidFalls` and drove all eight stages: **0 blits everywhere.** The road cannot have a
waterfall on it because nothing draws one anywhere in the game.

⚠ **AND THE `drawLiquidFalls(0)` CALL SITE IS NOT THE BUG IT LOOKS LIKE.** The `loopMaster` branch
passes a hard-coded 0 instead of the scroll position, which reads as an obvious defect. It is
stage 5 only, stage 5 has no `FALL_FOR` entry, and the function bails on `!fam` before the 0 is
ever used. Worth writing down because it will look like the answer to the next person too.

⚠ **THE OTHER CALL SITE PASSES `_srcYPub`, NOT RAW `srcY`, AND THAT IS CORRECT** — despite the
function's own comment calling its parameter "the master-space y of the top of the visible
window". The blit puts master row `srcY` at `_floorDy + _winTop`, so row R lands at
`R - srcY + _floorDy + _winTop`; with `_srcYPub = srcY - _floorDy - _winTop`, `d.y - _srcYPub`
expands to exactly that. It is the same mapping the props use. **Read the arithmetic, not the
parameter name.**

## 2. ⚠ THE FALL SYSTEM IS INERT IN BOTH DIRECTIONS — THE TWO HALVES NEVER MEET

    FALL_FOR (art)      2 -> nlf_lava,  7 -> nlf_sludge
    liquids.drops       1 -> {y764, x139..660},  4 -> {y2904, x0..799}

**The two stages with fall ART have no PLACEMENT, and the two stages with placement have had their
art removed.** So stage 2's lava fall and stage 7's sludge fall have never drawn a pixel. The art
is registered and present (`nlf_lava_0/1`, `nlf_sludge_0/1` all resolve), so this is authored work
that never ships.

Whether stages 2 and 7 SHOULD have falls is Mike's call, and the fix is data, not code: an
authored span per stage. 0810f already set the rule — *"if stage 4 ever wants a fall it needs an
authored span, not the full width"* — and stage 1's `{y:764, x139..660}` is the shape of a real
one. **Do not invent spans**; a full-width entry is the signature of something derived from a keyed
region rather than placed by hand, which is exactly what got stage 4 removed.

## 3. THE SIGNS — ONE STAGE, ALREADY OFF, AND PINNED ANYWAY

Signs live in `window.BOFRS[stage]`, NOT `cfg.signs` — a first probe read the cfg, got zero on all
eight stages and would have "proved" there are no signs at all. **Zero is not a result until you
know you read the right table.** Measured properly:

    stage 4   10 signs   SIGNS_OFF true   0 blits   master row 2760 INVARIANT over 200 frames
    all others  0 signs

Stage 4 is the only stage that ever had them and Mike retired them in 0813j. They draw nothing.
And the mapping is locked regardless: signs, props and terrain all read the single published
`_masterSrcY` (`sy = y - _masterSrcY`), so a sign cannot drift from the ground by construction —
that is 0813c, and the invariant row confirms it.

⚠ **WHAT "SCROLL" MEANS IS STILL MIKE'S, AND IT IS THE ONLY LIVE PART OF THIS ITEM.** His words
were *"they do not scroll ever, they are objects that stay put"*. Objects that stay put ON THE MAP
travel up the screen as the level advances, which is what the code now does. If he means
SCREEN-fixed, that is a different design and a different fix.

## 4. THE `+` GLYPH IS NOT A BUG

0822a flagged `+` rendering as a gap. It is not in the face's glyph map, but no rendered string
contains one — the only `+` in a text call is `'STAGE '+run.stage+' CLEAR'`, which is JavaScript
concatenation. Nothing to fix.

## 5. ALSO CORRECTED IN CLAUDE.md

`cfg.props` "holds exactly ONE prop game-wide, nst4_crash_overlay" — it is `props:[]` now and the
overlay went with the old stage-4 plate. Measured: props 0 on all eight stages.

---

## HOW TO VERIFY

    node --check assets/game.js
    node _BUILD_SOURCE/test_fl.js       # 2,702 ok / 3 fail, unchanged - no code changed in 0822b

0822b is measurement and documentation only. The only edits are to CLAUDE.md.

---

# 0822c — VERIFYING 0822a ON THE REAL SCREENS, NOT A SYNTHETIC ROW

0822a proved `FONT_RIDE` on a probe row and one string. But it moves glyphs for EVERY `stageText`
caller, and that is the whole UI. Checked the composed screens.

    node _BUILD_SOURCE/verify_atlas_0806z.js
      all 8 stages play 100s without throwing · no blank placeholders
      9,960 keys from 87 sheets · 157 loose        RESULT: PASS

⚠ **THE PILOT CARD IS WHERE THE HYPHEN FIX ACTUALLY PAYS.** Axel's bio carries "HIGH-SPEED
ENGAGEMENTS" and "HIT-AND-RUN TACTICS". Bottom-aligned those read `HIGH_SPEED` and `HIT_AND_RUN`
— an underscore in the middle of Mike's own copy, on the first screen of the game, and nobody had
reported it. They render as hyphens now. **The bug was always in front of us; the synthetic row is
only what made it legible.**

Only three strings in the build contain an apostrophe — `"IT'S HOT IN HERE"` (stage 2's subtitle),
`"ICE STILL CAN'T SEE"` (stage 3's) and `"FREEZER'S ORB"`. Two of the three are STAGE SUBTITLES, so
the "LET,S" defect was on a banner every run, not only in one dialogue frame.

## THE 0809-ERA PILOT CARD AND STATS COMPLAINTS DO NOT REPRODUCE

The pre-import CLAUDE.md carried four; captured at `--state PILOT` and `--state STAGECLEAR`:

| complaint | now |
|---|---|
| bio wraps mid-hyphen | wraps at SPACES; HIGH-SPEED and HIT-AND-RUN stay intact |
| periods render as `▪` | **not a defect** — p46 IS a 64x66 carved square, measured |
| emblem overlaps its text | emblem sits beside AFTERBURNER, no overlap |
| stats labels half a row above their bars, COLE/RANK collide | labels sit on their bars; COLE/RANK/C is its own column |

⚠ **"PERIODS RENDER AS ▪" IS THE SAME MISTAKE THIS FILE WARNS ABOUT FROM THE OTHER DIRECTION** — a
carved stone face's period IS a block, and reading it as a rendering fault would have "fixed" the
artist's own glyph. Measure the plate before calling a shape wrong.

The `%` borrow (closed in 0821j) also confirmed live: ACCURACY, MISSILE HITS and SPECIAL HITS all
render `0%` in the same khaki as their digits.

No code changed in 0822c.
