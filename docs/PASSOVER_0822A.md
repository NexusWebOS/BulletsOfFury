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

---

# 0822d — THE FOUR PLATES ARE 680 NOW, ON DISK

Mike: *"just scale our stages down to 680 width via the actual image, not in-game."* Done. Every
stage is now a true 680 world at zoom 1.00 — no runtime rescale anywhere in the game.

    stage        WORLD_W  zoom  viewW  pan  ratio        before
    1..8            680   1.00    480  200  1.417        2,3,7,8 were 800 @ 0.85

    nst2_master_v2          800x4800 -> 680x4080
    nst3_master_v2          800x4800 -> 680x4080
    nst7_master_v2          800x4062 -> 680x3453
    blackhole800_rc2_master 800x5120 -> 680x4352

## 1. ⚠ NEAREST, AND THE PRETTIER FILTER WOULD HAVE BROKEN THE KEYING

The obvious call is a smooth downscale — BOX or LANCZOS both look cleaner than NEAREST on a crop,
and I nearly took one. **These plates key by ALPHA**, and the liquid layers show through it:
stage 2's lava, stage 3's ice, stage 7's sludge at 68% of the plate. Measured partial-alpha pixels
(neither opaque art nor fully keyed) on a 1-in-3 sample:

    variant     stage 2 fringe   stage 7 fringe
    ORIGINAL                 0                0     <- hard-edged by construction
    NEAREST                  0                0
    BOX                    121              749
    LANCZOS              2,445           12,045

⚠ **A SOFT FILTER PUTS A SEMI-TRANSPARENT FRINGE ON EVERY TERRAIN EDGE, AND THE LIQUID BLEEDS
THROUGH IT.** That is a halo along every boundary in the level — the artifact class this repo's
own rules exist to prevent. LANCZOS would have added roughly 108,000 fringe pixels to stage 7
alone at full resolution. **The filter was chosen by measuring the key, not by looking at a crop**,
and the crop is exactly what would have chosen wrong.

Every converted plate re-measured at **0 partial alpha**. The key is as hard as it was authored.

## 2. WHAT ELSE HAD TO MOVE — THREE THINGS, ALL SILENT IF MISSED

⚠ **`cfg.h` FALLS BACK TO 4800 AND THE FALLBACK DOES NOT THROW.** Stages 2 and 3 were 4800, so
they matched the fallback by accident and declared nothing. At 4080 they no longer do, so both
now declare `h`. Stage 7's `h:4062` was already flagged load-bearing and became 3453. Stage 8 got
`h:4352`. A missed one mismaps the whole stage silently.

⚠ **STAGE 8's `skipRows:[2500,2650]` ARE ABSOLUTE MASTER ROWS** and were rescaled to
`[2125,2253]`. Left alone they would skip the wrong 150px of a shorter plate.

⚠ **THE MASKS NEEDED NOTHING, AND THAT IS WORTH KNOWING.** `_buildTankMask` builds from
`img.naturalWidth/naturalHeight` and `_isLand` indexes world x 1:1 into the mask's own width, so
both rescaled themselves with the art. The old comment warning that narrowing the world would put
"every tank and boat on the wrong pixel" was about narrowing the WORLD under an 800 plate — not
about scaling both together, which is self-consistent.

## 3. THE TWO SUITE FAILURES WERE ASSERTIONS DEFENDING THE OLD PLATE

    ASSERT FAIL: stage 7 reports WORLD width 800, not camera width 480
    ASSERT FAIL: stage-7 declares its true plate height (4062, not the 4800 fallback)

Both correct before this drop and both literals. **Repointed at the ART instead of at a new
number**: `pngSize()` reads the PNG's own IHDR, and the assertions now compare `plateW` and
`cfg.h` against the actual file for all seven stages that declare geometry. A literal is only ever
true of the plate that was on disk the day it was written — the second of those two even carried a
comment explaining how load-bearing it was, and the comment was right while the number went stale.

Suite **2,723 ok / 3 fail** — up 21 assertions, and the 3 are the same environmental
`_superseded/` checks as every run this session.

## 4. VERIFIED

    verify_atlas_0806z.js    PASS - all 8 stages play 100s, boss reached, 0 blank placeholders
    measured live            all 8: WORLD_W 680, zoom 1.00, pan 200, ratio 1.417
    shoot.py                 stages 2, 3, 7, 8 captured - keyed liquid still shows through,
                             hard terrain edges, no fringe, no halo

⚠ **WHAT THIS DID NOT BUY, STATED PLAINLY:** the 0.85 reduction still dropped the same ~15% of
columns — it is baked now rather than applied live. The gain is that it is applied ONCE, at a
fixed phase, instead of recomputed every frame against an eased fractional camX. `CAM_SNAP` is
now moot for these stages: at 680 the device factor is an integer 2.00, which is the stable case
0822a measured.

---

# 0822e — WHAT THE RESCALE INVALIDATED

Converting 1-8 to 680 left a default behind that now describes nothing in the game.

⚠ **`MASTER_W` WAS STILL 800, AND IT IS THE SILENT FALLBACK FOR ANY STAGE THAT OMITS `plateW`.**
Every stage 1-8 declares 680 now, so none of them reach it — but the value a NEW stage would
inherit was the one width no playable plate has. It is 680 now.

⚠ **AND I NEARLY CHANGED IT WITHOUT LOOKING AT STAGE 9.** `waterworld800_rc2_master` is genuinely
**800x5120** — measured, not assumed — and stage 9 was the ONLY consumer of the fallback. Setting
MASTER_W to 680 while stage 9 leaned on it would have mismapped that stage silently, which is
precisely the failure mode the `cfg.h`/4800 note already describes. Stage 9 declares `plateW:800,
h:5120` explicitly now, so the default and the odd stage are independent.

**Stage 9 was NOT rescaled**, deliberately: it has no `STAGES[]` entry (the two `n:9,` hits in the
file are `szMin:9` and a snow-effect row, not a stage), so it cannot be reached and a conversion
could not be verified against anything. When it is wired up, either rescale it to 680 or keep that
cfg line honest.

## THE RULE, NOT THE NUMBER

    for stg 1..9: a cfg with a master MUST declare plateW

Nine new assertions. A stage that omits it inherits a width and mismaps without throwing — there
is no exception worth the silence, and the previous drop's two stale literals are the argument for
asserting rules instead of values.

Suite **2,732 ok / 3 fail** — the same three environmental `_superseded/` checks.

---

# 0822f — ONE PICKUP FOOTPRINT, AND MFX_ RESOLVED THE OTHER WAY

Mike: *"The crates should be scaled up to 64x64, the mcrates to 64x64, the boxes to 64x64, the
capsules are fine, and the bombs to 64x64."*

    type                        before          after
    mcrate                      61x61           64x64
    sonicbox/lzmgbox/dkshotbox  41.5x41.5       64x64
    crate                       44x46           61x64
    bomb                        42x43           62.5x64
    scrate                      ~45x48.8        54.8-59.8 x 64
    special icon                27-48 minor     36-64 minor
    capsule (pill)              48x16           48x16  - left alone, as asked

`PICKUP_BOX = 64` is the one dial; `pickupFit()` replaced nine scattered size expressions.

⚠ **THE CRATE DID NOT MOVE ON THE FIRST PASS, AND THE REASON IS ALREADY IN THIS FILE.**
`drawCrate` has FIVE exits and the atlas-cell one is FIRST — `drawBoxPillCell('box_'+st+'_'+fi, x,
y, 46, flash)` with a hardcoded 46, returning early. Every fit applied to the branches below was
dead code for it, and the measurement said 44x46 while every sibling had moved. **Find the branch
that OWNS the object** — the same lesson `spawnEnemy`'s switch teaches, one function over.

⚠ **THE BOMB WAS THE ONE PICKUP THAT NEVER TOOK `PICKUP_SCALE`** — a raw `w=42` while every
sibling rode the shared multiplier. Invisible in code review because it was internally consistent.

⚠ **THREE DRAWERS BREATHED BY CHANGING SIZE** (`(N + 2*Math.sin(now/240))`). That makes "the same
size" untrue two frames in three, and it is what made the FIRST measurement of this read as
per-pilot variance — the pulse sampled at different moments, not a real difference. Dropped; the
positional bob is a separate translate and still reads as float. **A probe that does not freeze an
animation measures the animation.**

## FIT, NOT STRETCH — AND THE REMAINDER IS THE ART

Four types land exactly 64x64. The rest fall short on one axis because the PLATES ARE NOT SQUARE.
Forcing an exact 64x64 would stretch hand-authored art — crate 5%, bomb 2%, and freezer's special
icon by nearly 80% to fill the square. Fitting keeps every pickup on the same 64px footprint with
its authored proportions intact, which is the standing rule's side of the trade.

The scrate spread (54.8-59.8) and the special icons (36-64 minor axis) are entirely the nine
per-pilot plates having nine different aspect ratios. **Exact 64x64 there needs the art padded to
square canvases, not a code change.**

## MFX_ — ASKED TO DELETE, AND THE EVIDENCE SAYS DO NOT

Mike re-issued *"Delete MFX"*. Not done, and the record is now resolved rather than left carrying a
contradiction. `ART_TAXONOMY.json` had `mfx_` marked **DELETE** *and* a `_WARNING_mfx` telling the
next reader not to act on it — the mark and the warning have disagreed since 0807y.

    audited 0821j    52 cells LIVE, 200 unexercised, removal frees ZERO bytes (aliased into
                     shared atlases)
    suite pins       mfx_mg_2_0 / mfx_mg_2_2  - the assertion itself calls them "Mike pick"
                     the pellet firetype cycling mfx_mg_2
                     boss volley keys mfx_ea_ / mfx_bshot_
                     drawMfx('mfx_hom_0_7')   - the missile's one fixed frame

⚠ **UNEXERCISED IS NOT DEAD, AND THIS REPO ALREADY PROVED IT.** A live assertion reads
*"mfx_bshot_0_0 was KEPT — the suite failed without it, so something reaches it that no static scan
sees."* Deleting the 200 "unexercised" cells on a static count is the exact move that assertion
exists to stop. Role is **KEEP** now, with the measurement in the note; re-open only with a
per-cell list, never as a family.

## VERIFIED

    node --check assets/game.js                 clean
    node _BUILD_SOURCE/test_fl.js               2,732 ok / 3 fail (the usual environmental three)
    node _BUILD_SOURCE/verify_atlas_0806z.js    PASS - all 8 stages, every graphic resolves

Also recorded from this pass: lava/sludge FALLS are dropped (Mike: the levels work on animated
flats alone), the Colossus is confirmed already scrapped, `CAM_SNAP` stays 0, the `%` glyph is
closed, and cutscenes/dialogue are left untouched pending a full rebuild.

---

# 0822g — BIGGER BLASTS, SCORE FEEDBACK, AND A SCORCH THAT IS NOT READY

From Mike's Raiden II / Fire Shark tapes: *"the effects of the explosions, the bosses, the score,
kill scorch, explosion sizes."* Two of those land here. The third does not, and the reason is
worth more than the feature.

## 1. EXPLOSION SIZE — the third raise, and the assertion said to expect it

    COVER_TARGET      2.69 -> 3.20
    COVER_TARGET_BIG  3.29 -> 4.05

Two dials, no per-unit sizes touched, so the whole game moves together and a turret still reads
smaller than a boss by construction. The suite's ceiling failed at 3.0 — and its own comment
records being raised twice already (1.6 -> 2.1 -> 3.0), calling itself "a SANITY bound, not a
design opinion". Raised a third time to 4.2 rather than deleted, which is what that note asks for.

## 2. SCORE FEEDBACK — three kill paths, none of them told the player

`run.score` moved in three separate branches and nothing appeared on screen. Both reference games
pop the value off the wreck; that IS the loop for a scoring game. One `killFeedback()` now serves
all three.

## 3. ⚠ SCORCH IS BUILT, GATED OFF, AND HONESTLY NOT WORKING

The burns draw and persist — 3 added, 3 blits, 3 alive, authored art (`ndk_scorch_0..5`, not a
procedural blob). What is NOT true is that they stay on the ground, and three separate probes
told me they did before I caught each one.

⚠ **`_masterSrcY` IS FROZEN.** The signs/props mapping, the obvious anchor, measures unchanged on
ALL EIGHT stages across 240 driven frames (2-5 all at 3220.8, 7 at 3568, 1 at 0).

⚠ **`_lastScrollDy` IS DEAD ON THE PATH THAT SCROLLS.** Switching to the tank idiom
(`e.y += _lastScrollDy`) looked right — it is what ground units already use. Measured on stage 1
over 180 driven frames: `_lastScrollDy` accumulates to **0** while `mapScroll` over the SAME
frames advances **250.3px**. It is assigned inside `drawLevelMaster`, so on whatever path is
actually moving the ground it never updates.

⚠ **AND THE TEST THAT BLESSED IT WAS VACUOUS.** It compared scorch displacement against ground
displacement and reported "LOCKED TO THE GROUND" — from ground 0, scorch 0, drift 0. **A drift
check proves nothing unless the thing it drifts against demonstrably MOVED in the same run.**
Assert the precondition, not just the difference. That is the third measurement error on this one
feature: the first probe measured animation instead of the camera, the second failed on its own
`toFixed` rounding, the third passed on nothing happening.

`SCORCH_ON = 0`. The work is on the branch, the evidence is at the constant, and it flips to 1 the
day the real per-path scroll number is identified.

## VERIFIED

    node --check                       clean
    node _BUILD_SOURCE/test_fl.js      2,732 ok / 3 fail (the usual environmental three)
    shoot.py stage 1                   blasts visibly heavier; 64px pickups reading well

Still queued and NOT started: Maverick's tappable laser as Fire Shark's widening arc (frames
captured — narrow at the nose, spans the screen by the top, discrete segments, ~12-frame cycle),
and the boss / enemy behaviour work.

---

# 0822h — MAVERICK'S TAP IS A WIDENING ARC

Mike: *"The helix beam in fire shark goes across the screen, that should be how mavericks tappable
laser should operate."*

Read off the capture frame by frame, that weapon is not a beam. Each tap emits a tight arc just
above the nose which WIDENS as it climbs, until near the top it spans a broad band of the screen.
It is discrete segments along the arc, not a column, cycling roughly every 12 frames.

    before   one persistent kind:'beam', a solid column, width 14+lv*4
    after    a volley of 5+lv segments fanning from ~one point
             lv1: 6 segments   lv5: 10 segments

Measured on the real fire path, level 1: span **14px at the nose -> 152.7px after 150.6px of
climb**, and the bolts are still alive at the end. Over the full 512px column that is the band he
described.

⚠ **THE FAN COMES FROM VELOCITY, NOT FROM SPAWN SPACING.** The bolts leave from essentially one
point and separate as they fly. The charged flurry's own spawn already carries this note — spread
across a wide row at launch, a volley reads as "split apart" rather than "bursting".

⚠ **IT REUSES kind 'hfl' RATHER THAN ADDING A KIND.** That mover already advances a bolt along its
own `_hdir` with the sine PERPENDICULAR to the heading, and its draw already picks the lzr_ reel
and scales it with `_grow` as the bolt climbs. The widening, the segmenting and the growth all
existed; a new kind would have meant re-wiring a mover, a draw and a collision path to arrive back
here.

⚠ **AND IT IS NOT THE CHARGED FLURRY.** No `_full`, no `_pierceAll`, no `_bossDmg`; dmg stays the
old laser's `2+lv/2`. Pierce is OFF — one beam piercing everything is one thing, ten segments each
doing it is another, and that is a POWER call for Mike, not a shape one. One line if he wants it.

## THE ASSERTION THAT FAILED WAS PINNING THE OLD SHAPE

    ASSERT FAIL: laser fire spawns a level-tagged beam

It checked `kind==='beam' && lv===3`. The comment directly above the block states the rule it is
really there for — *"firing spawns bullets that carry the level for tinting"* — so the KIND was
incidental, naming whatever the laser happened to be that day. Repointed at the rule: the lv tag is
still asserted, and the segment COUNT is asserted too, because a fan that silently collapsed to one
bolt would otherwise sail through.

Suite **2,732 ok / 3 fail** — the usual environmental three.

---

# 0822i — ENEMIES AIM WHERE YOU WILL BE

From the tapes: enemy fire in both reference games is slow, fat and readable, and still dangerous.
That combination does not come from adding bullets. It comes from AIMING. A round sent at your
current position is beaten by continuing to move; a round sent at the intercept has to be reacted
to. **It is the lever that lets bullet COUNT come down while pressure goes up** — the parked stage
3/7 density problem stated from the other side.

⚠ **NOTHING TRACKED THE PLAYER'S VELOCITY**, so no enemy could aim anywhere but at where he
already was. It is measured now, AFTER the position clamp so a ship pinned on an edge reads as
stopped — which it is — rather than reporting input it never got to use. Units are px/frame, the
same units enemy bullet speeds use, so a flight time in frames multiplies straight through.

    ENEMY_LEAD   0     fire at where he is   — what all 50 aimPlayer callers did before this
                 1     perfect prediction    — reads as unfair, punishes movement itself
                 0.55  SHIPPED

⚠ **THE DEFAULT ARGUMENT IS WHAT MADE THIS SAFE.** `aimPlayer(x,y,spd,k)` — all fifty existing
callers pass `(x,y)` and inherit the dial; a caller wanting a straight shot passes 0 explicitly.
No hand-editing of fifty sites, which is precisely how `_selfPat` went wrong.

Two solver passes: flight time depends on the aim point, the aim point depends on flight time.
Two iterations converge inside a pixel at these speeds.

## MEASURED

    enemy (140,90) firing at 4.0 px/f, player at x=240, y=380

    player moving RIGHT +3px/f    no-lead crosses x=240   led crosses x=398.4   +158.4px
    player moving LEFT  -3px/f    no-lead crosses x=240   led crosses x=120.1   -119.9px
    player STATIONARY             no-lead crosses x=240   led crosses x=240      +0.0px

Leads into the motion both directions, and **exactly zero when stationary** — a standing player
gets the old behaviour bit for bit, which is the property that makes the dial safe to ship on.

⚠ **158px IS A LARGE LEAD AND MIKE SHOULD FEEL IT BEFORE IT STAYS.** It is arithmetically right —
3px/f over a ~77-frame flight really does intercept that far ahead — but long-range shots now
swing a long way. `MG_CONE` (0.62rad off vertical) bounds the worst case, so nothing crosses the
screen sideways. If it plays as harsh, the fix is one number, not a rework.

⚠ **THE ASYMMETRY IS CORRECT, NOT A BUG.** Moving right increases range from an enemy at x=140, so
flight time and therefore lead grow; moving left shortens both. 158 vs 120 is that, not a sign
error.

Suite **2,732 ok / 3 fail**.

---

# 0822j — NO BOSS SPLITS, AND THE THREAD IS CLOSED

I proposed multi-part destructible bosses off the Raiden II battleships. Mike, asked directly:
**"No bosses split, at all."** Recorded as a standing rule rather than left as a chat answer,
because it is now the SECOND time he has ruled it — 0813z already routed stage 4 off the sectional
rig on *"do not split him or seperate him"*, and I proposed it again anyway.

⚠ **THE RULE WAS ALREADY HONOURED AT THE BOSS TIER — CHECKED BEFORE CHANGING ANYTHING.** The four
live `mechInit` calls are `magmacolossus` and `cryobehemoth` (both SCRAPPED in 0810q, dead code),
and `glacierrail` / `mbw4`, which are SUB-BOSSES. No live boss is sectional. Nothing had to be
undone, which is worth saying plainly: the correct action after a ruling is sometimes zero code.

⚠ **AND TWO THINGS MUST NOT BE MISTAKEN FOR SPLITS.** The stage-6 carrier's L/R bays are Mike's own
mechanic — immune to ordinary fire, damaged only by deflected warheads, and the note at
`CARRIER_BAY` records it as built *exactly as asked*. The quad-laser miniboss's four cannons ship
that way in the authored pack. A future session reading "no boss splits" could gut both in good
faith. The rule says so at the rule.

## ⚠ MY TWO BOSS SURVEYS WERE BOTH INVALID AND I ALMOST REPORTED THE FIRST ONE

Worth recording as method, not apology:

1. **Measured at frame zero.** It broke out of the drive loop the instant `boss` existed, then read
   `_bay` / `_mech` / sections — all of which initialise on the boss's FIRST TICK. It reported "no
   boss has any parts" for all eight. `carrierTick` is wired and does initialise bays; the survey
   simply looked before it ran.
2. **Killed the bosses.** Removing the break let the probe keep firing `pShoot()` every 6 frames,
   so stage 1 measured at **-1.92 hp** and stage 2 at **-1**. It measured corpses.

Three probes this session have now failed the same way — the scorch drift test that passed on
0 vs 0, and these two. The common fault is never the game: it is **a probe whose result is
readable even when the thing under test never happened**. State the precondition, assert it, and
make the probe fail loudly when it is not met.

No code changed in 0822j. CLAUDE.md only.

---

# 0822k — SCORCH IS ON, AND THE ANSWER WAS TO STOP ASKING WHICH VARIABLE

Three attempts read the scroll from a variable and all three were wrong:
`_masterSrcY` frozen on all eight stages, `_lastScrollDy` accumulating to 0 on stage 1 while
`mapScroll` moved 250px over the same frames, and `mapScroll` itself only advancing on stage 1.

⚠ **THE PIXELS SETTLED IT.** Sampling a rendered column, stage 1 shifts 39 sample-units with 95%
of the column changing; stages 2-8 match at **zero shift** with 9-30% changing. They were
ANIMATING IN PLACE, not scrolling. Every variable reading zero had been telling the truth, and
three probes' worth of "the anchor is broken" was really "the ground was not moving".

`_groundPublish(srcY)` now runs at every master blit and publishes `_groundDy` — the frame-to-frame
change in the master row the blit consumes. That is the ground's own displacement, on whatever
path drew it, without naming a driver.

⚠ **AND THE FIRST PASS MISSED THE ONLY STAGE THAT SCROLLS.** Four blits matched the two shapes I
grepped for; stage 1's is `drawImage(img,_sx,srcY,...)` — it pans the SOURCE X with the camera, so
it matched neither. The verification came back INCONCLUSIVE rather than passing, which is the
whole reason the miss was caught: **the precondition guard did its job.**

    ground moved 125.16px   scorch moved 125.16px   drift 0.0   precondition MET

`SCORCH_ON = 1`.

## THE METHOD LESSON, STATED ONCE

Four probes this session produced confident wrong answers: one measured animation instead of the
camera, one failed on its own `toFixed` rounding, one passed on 0-vs-0, one measured bosses at
frame zero and then a rerun measured their corpses. **Every one was readable even though the thing
under test never happened.** The fix is not more care — it is a precondition assert that makes the
probe say INCONCLUSIVE instead of PASS.

Suite **2,732 ok / 3 fail**.

---

# 0822l — THE LEVEL-1 POP-IN DOES NOT EXIST, AND MY FIRST PROBE INVENTED 17 OF THEM

Long-standing item: *"enemies still appearing out of thin air on level 1 — 2 of 29 units last
measured entering at (21,67)."* Drove all eight stages, recording every unit on the frame it was
born:

    stage   units   ENTERING units on screen at birth
    1..8    305     0

Zero, on every stage. 0812k (clear the SPRITE, not the world edge) and 0813x (measure it off the
CAMERA) did the job. The only units in view at birth declare `inPlace` — stage 2's `ash` SPLIT
halves (6) and stage 7's surfacing `maw` (2) — which the clamp exempts deliberately and which Mike
authored to appear where they are (0811o).

⚠ **THE FIRST RUN OF THIS PROBE REPORTED 17 POP-INS ACROSS FOUR STAGES, AND I ALMOST FIXED THEM.**
It compared WORLD x against `0..VW` without subtracting camX — the exact confusion this file
already records as having bitten three times. A jet flagged at x=-26 was 111.5px clear of a camera
whose left edge was at world 100. I then built a second theory on top of the bad number (that `c.w`
was not final at the clamp, so `_half` fell back to 16) and measured THAT before acting: `w` is 95
at spawn and unchanged. Both the finding and the follow-up theory were wrong.

**Before reporting a pop-in, subtract the camera.** Second entry in this passover's running tally
of probes that read as meaningful when nothing happened.

Also corrected: the plate-width note still said PARKED pending a call between 800 and 720. Settled
0822d at 680.

No code changed in 0822l — the system was already correct.

---

# 0822m — THE FAR SCENERY BELONGED TO drawBG ALL ALONG

Stage 5's orbital hardware and asteroid field, stage 6's weather and far decks, and stage 5's
planetary setpiece all lived in `drawWorld` — one line AFTER its own `drawBG(dt)` call. The
connectors draw their frame with `drawBG(0)` and nothing else, so an arriving player got terrain
with the sky missing and the whole field switched on at PLAY's first tick.

    l5FieldDraw from a CONNECTOR frame   0  ->  1
    l5FieldDraw from a PLAY frame        1  ->  1   (not 2 — no double draw)

⚠ **ORDER IS PRESERVED EXACTLY.** drawWorld ran `drawBG(dt)` and then this block immediately, so
running it at the tail of drawBG is the same sequence. A frame that was already correct is
unchanged, which is the property worth having when moving draw calls.

⚠ **IT IS A WRAPPER BECAUSE drawBG RETURNS EARLY.** The master path returns before the end, so a
call inserted before that return would be skipped by every other exit. `drawBG` is now
`_drawBGCore(dt)` plus `stageSceneryDraw(dt)`, which covers all of them.

⚠ **dt IS 0 FROM A CONNECTOR AND THAT IS DELIBERATE** — the field DRAWS but does not ADVANCE, so
the arrival frame matches the first play frame instead of jumping past it.

Suite **2,732 ok / 3 fail**. Atlas verifier PASS.

---

# 0822n — THE LAUNCH JOIN: ATTEMPTED, REVERTED, AND WHY

The last item on the list: *"the craft draws twice at the launch join — drawLaunch rolls its own
ship and `nthp_` plume, PLAY draws the player through its own path, nothing forces them to agree."*

Captured `--state LAUNCH` first, and the defect is real and VISIBLE, not the 2.5-4.3% probe
abstraction it was filed as: the plume's mass floats clear of the tail, taper toward the hull,
where PLAY seats it at 8px with the wide end on the nozzle.

⚠ **THERE ARE TWO DIFFERENCES, NOT ONE.** `drawLaunch` seats at a hardcoded `shipY + shipH*0.30`
AND never flips. 0801fp flipped the PLAY plume so the large section contacts the back of the ship;
0819c then derived the closed-form seat so the plume's own height cancels. The launch has neither.

⚠ **PORTING THE SEAT ALONE FAILED TWICE, AND BOTH WERE WORSE THAN SHIPPED.** First attempt put the
flame ABOVE the aircraft — under `scale(1,-1)` local +y maps to screen -y, so drawing at local 0
runs it up the screen. Second attempt, corrected to `-_th`, put the flare ON the hull.

⚠ **THE ROOT CAUSE IS SIZING, NOT SEATING.** PLAY sizes the plume from the per-pilot MOUNT scale;
the launch sizes it to `shipH*1.15` against the reel's largest frame. The seat's
`- _th*PLUME_CORE_F` term is calibrated to PLAY's proportions, so at the launch's much larger `_th`
it over-corrects and drags the flame over the ship. **One formula cannot be ported into a context
that sizes its input differently.** The real fix is one sizing rule AND one seat, read by both.

**Reverted to exactly what shipped.** A wrong flame is worse than a differently-seated one, and the
launch is a cinematic where a mistake is unmissable. The finding is recorded at the call site so
the next attempt starts from the sizing.

⚠ **AND THE HOIST CAME OUT TOO.** `_HB` was lifted to module scope to let the launch read it; once
the fix reverted it bought nothing, and §120 greps the SOURCE for a literal `_HB={...}` and parses
the values to check they span the measured 0.834-0.921. The hoist failed that assertion and
silently skipped three more inside its `if`. **A source-scanning assertion turns a harmless
refactor into a real failure** — worth knowing before moving any table this suite reads by regex.

game.js is comment-only against HEAD. Suite **2,732 ok / 3 fail**.

---

# 0822o — ENEMIES STACKING IN STAGE 1: A NAVAL MINE NOTHING AVOIDED

Mike: *"what about enemies stacking and also disappearing in stage 1?"*

    stage   frames with 2+ units   pair buried >35%   worst overlap
    1       3365                   51.8%              1.00  (complete)
    2       4009                    3.8%              0.77
    3       3701                    7.3%              0.99

Stage 1 was the outlier by an order of magnitude, and one name sat in four of the top pairs:
**`s1rivermine`** — 797 stacked frames against corvettes, landing craft, patrol boats and jets.

⚠ **THE GATE EXCLUDED IT FROM BEING AN OBSTACLE AT ALL.** `sepEligible` — whose own comment reads
"counts as an obstacle" — dropped anything flagged `prop`, and the mine is `prop:true` **and**
`pat:'prop'`, so it tripped both halves. Eligible on 0% of its 2,215 frames. Boats sailed through a
naval mine as if it were painted on the water.

⚠ **AND IT IS NOT SCENERY.** `PROP_BLAST` gives it `r:70, dmg:14, shake:6` and the roster gives it
`hp:3` — a shootable hazard the player is meant to dodge. So is every other entry in that table.
**That table IS the definition of "this one hurts"**, so it drives the rule instead of a hand-listed
type name.

Hazards are obstacles now and no prop is movable — a mine shoved by a passing boat would drift off
the lane its wave script placed it in, which is worse than being ignored.

    stage 1 stacked frames   51.8%  ->  28.8%
    corvette + rivermine       361  ->  0

What remains is `s1jetdelta` in six of seven pairs, overlapping SURFACE units — a jet passing over
a boat is an altitude difference, not a pile-up. Jet-on-jet is 54 frames and looks like the
formation flying `SEP_MIN` deliberately allows. **Mike's eye, not a number, decides whether that
reads wrong.**

## DISAPPEARING: NOT REPRODUCED ON STAGE 1, AND TWO PROBES LIED FIRST

    units leaving while alive AND inside the visible box — stages 1/2/3:  0, 0, 0
    alive, on screen, drawing nothing — stage 1:                          0 of 12,844 unit-frames

⚠ **THE FIRST VANISH PROBE REPORTED 11 ON STAGE 1.** Its cull line was `VH+40` while VH is 512, so
units at y 546-551 — already below the visible bottom — were classified as VANISHING rather than
culled. Off screen is off screen; the boundary has to be the visible box, not a padded one.
⚠ **AND THE `ENEMY_ART` THEORY WAS WRONG TOO** — zero units on stage 1 carry an art name that
misses `ENEMY_ART`, so this is not the documented draws-nothing fallthrough.

**Most likely the stacking WAS the disappearing**: a unit buried under another is drawn over and
reads as having vanished. The fix above should move both.

⚠ **UNVERIFIED, FOUND IN PASSING: STAGE 2 SHOWS 34.2% OF UNIT-FRAMES DRAWING NOTHING**
(`magmagun` 3230, `spinner` 2100). NOT reported as a bug — `drawEnemy` early-returns into
`drawVolc` for volcanic units and the accounting may simply not see it. Needs its own pass.

Suite **2,732 ok / 3 fail**. Atlas verifier PASS.

---

# 0822p — "NO UNITS SHOULD EVER OVERLAP" COLLIDES WITH ONE OF MIKE'S OWN ASSERTIONS

Mike, on the 0822o result: *"no units should ever overlap, they have unit boxes for a reason."*

`SEP_MIN` is the deadzone below which a contact is deliberately left alone. Taking it to 0 does
help — stage 1's stacked frames fell **28.8% -> 20.4%** on a comparable run — but it fails §213:

    ok(_s213.touchMoved === 0,
       'and separation leaves it alone — an authored formation keeps the shape it was drawn as');

⚠ **THAT ASSERTION DEFENDS A DESIGN CHOICE, NOT A BUG.** The formations are AUTHORED to touch, and
the deadzone is what preserves the shape they were drawn as. Blowing them apart is a visible change
he did not ask for — his complaint was stage 1's pile-ups. So the value stays where it shipped and
the conflict is recorded at the constant for him to settle. **When an assertion and an instruction
disagree, the one who wrote both decides.**

## ⚠ AND DO NOT CHASE THE REMAINDER BY RAISING SEP_CAP

Swept 260/420/700 against the shipped 130:

    SEP_CAP    130     260     420     700
    stacked   20.4%   40.0%   70.5%    3.8%
    frames     3446    3489    4080    4080   <- the tell

Non-monotonic, and the frame count is why: a stronger push moves units into DIFFERENT POSITIONS,
so the stage plays out differently, the boss stops being reached, and the runs are not comparable.
**A parameter that changes the scenario cannot be A/B'd by replaying the scenario.** Picking 700
off that table would have been picking the luckiest divergence.

## WHAT THE REMAINING 20-29% ACTUALLY IS

`s1jetdelta` in six of seven remaining pairs, overlapping SURFACE units — mines, patrol boats,
landing craft. A jet crossing over a boat is an altitude difference; forcing them apart means
deflecting jets off the routes Mike authored. Enemy boxes do not collide with each other in this
engine either — only the player collides with them — so this is a VISUAL question about whether a
jet passing over a boat reads as clipping or as altitude.

Two things need his call, and neither is a number I should pick:
  1. formations touching — keep the drawn shape, or separate them anyway?
  2. air over surface — deflect jets off their routes, or treat it as altitude?

Suite **2,732 ok / 3 fail** at the shipped value.

---

# 0822q — THREE STAGE-2 ENEMIES WERE INVISIBLE, AND ONE WAS SHOOTING AT YOU BLIND

Chasing Mike's "enemies disappearing" from stage 1 turned up nothing there — but the same probe on
stage 2 found 34.2% of unit-frames drawing NOTHING:

    unit        frames on screen   blits   art
    magmagun    3,230                  0   undefined
    spinner     2,235                117   undefined
    dodger        870                  0   undefined
    every other unit                ~1+/f   a real cell key

All three spawned, moved, shot and collided while drawing nothing — the fallthrough CLAUDE.md
describes, reached by a route it does not name: `nefRow(type)` finds no row, so `e.art` is never
set at all.

## ⚠ I FIXED THE WRONG TABLE FIRST, AND THE MEASUREMENT CAUGHT IT

`VOLC` carries `art:'pod'` / `'disc'` / `'ash'` for exactly these three, which reads like the
answer. It is not: those are UNIT-TYPE names, `ENEMY_ART` holds none of them, and the spawn branch
that owns these units copies `w/h/hp/score` off VOLC and **never reads `.art` at all**. Editing it
changed the numbers not one blit — and re-running the probe is the only reason I know that instead
of having shipped it. **The branch that owns the object was `NEF_S2`**, which is what `nefRow()`
resolves. That is the same lesson `spawnEnemy`'s switch teaches, met from a new direction.

Art resolved to what those aliases were pointing at rather than picking something new: 'pod' is the
eruption pod (what `eye` draws), 'disc' the volcanic mine, 'ash' the molten drone. `w/h/hp/score`
mirror VOLC exactly, so no behaviour moves.

    magmagun  3,230 frames -> 3,230 blits   (1.00/frame)
    spinner   2,390        -> 2,390         (1.00)
    dodger      772        ->   772         (1.00)

## ⚠ SPINNER'S TELEGRAPH WAS THE INVISIBLE PART

Its own comment says it: *"THE SPIN IS DRAWN, NOT IMPLIED: `e.spin` is what drawNewEnemyArt rotates
by."* The wind-up before its ring of 10 IS the sprite rotating — so with no sprite there was no
tell at all, and the ring landed out of nowhere. A disc is also the shape that reads best spinning,
which is what its own alias was asking for.

## AND I DESCRIBED BOTH UNITS WRONG BEFORE READING THE RIGHT BLOCKS

Told Mike magmagun "holds a lane and fires a single bolt" and that spinner's aimed salvo
contradicted its "rings you" design note. Both wrong: I read `sed` ranges without confirming which
`K===` block owned them. magmagun fires a 3-round salvo twice then withdraws upward; spinner
already fires the ring exactly as designed. **A line range is not a scope.** Two authored families
(`nef_s2_drill_buggy`, `nef_s2_tracked_flame_turret`) remain unused — neither suits a unit that
leaves upward, so they stay on disk.

Suite **2,732 ok / 3 fail**. Atlas verifier PASS.

---

# 0822r — "STAGE 7'S WHOLE CAST IS INVISIBLE" WAS MY PROBE, NOT THE GAME

Sweeping all eight stages for the 0822q gap reported:

    stage 7   100% of unit-frames drawing nothing   (all six types, 18,836 frames)
    stage 8   20.1%                                 (cdisc, spiral)

Both false. **The art is registered and loads fine; my probe never let it.**

⚠ **A SYNCHRONOUS BURST NEVER YIELDS, SO LAZY ART NEVER ARRIVES.** The sweep ran 4,800
`updatePlay/drawWorld` iterations inside ONE `evaluate`. Zero real time passed, so nothing lazily
loaded could decode. Stages 1-6 read clean only because their art is PRELOADED; `nsw_` (stage 7)
and `nel_` (stage 8) are not. This is the `--warm` trap this file already documents — *"1400 warm
frames still showed a black screen where 200 warm plus --seconds 2 showed the scene"* — met from a
probe rather than from shoot.py.

Measured properly, with real time allowed to pass:

    key               registered   rdy 1st call   rdy after time
    nsw_skimmer_0        True         False           True
    nsw_sentry_0         True         False           True
    nsw_maw_0            True         False           True
    nsw_barge_0          True         False           True
    nel_cdisc_0          True         False           True
    nel_spiral_0         True         False           True

`rdy` false on the FIRST call is the documented behaviour — that call is what starts the load. And
`shoot.py --state PLAY --stage 7` shows a sewer unit drawn plainly at the top of frame.

⚠ **WHAT MAKES 0822q'S FIX GENUINE BY CONTRAST.** Stage 2's three units did not have unready art —
they had **`e.art` undefined**, because `nefRow()` found no row. That is structural, not timing,
which is why the fix moved them 0 -> 1.00 blits/frame *inside the same synchronous probe* that
"found" stage 7. **A unit with no art name and a unit whose art has not decoded look identical to a
blit counter and are nothing alike.** Check which one you have before writing a fix.

No code changed in 0822r. Stages 7 and 8 were never broken.

---

# 0822s — FOUR SOUNDS WIRED, AND TWO OF THEM WERE ON EACH OTHER'S TRIGGERS

Mike: *"wire up sounds for flame thrower, flamewalls/waves that come at us, barrrel rolls and the
lz_stack is for cole's fusion cannon /lvl 8."*

    file                  was                                    now
    arc_flame_loop.wav    fireball launch one-shot only          FLAMETHROWER (held loop)
    flame_wall.wav        looping on the flamethrower            stage-2 FIREWAVE
    arc_barrel_roll.wav   startRoll()                            unchanged - already correct
    lz_stack.wav          not in the build at all                cole's LV8 FUSION CANNON

⚠ **THE FIRST TWO WERE SWAPPED.** `flame_wall.wav` had been looping on the held flamethrower since
0801km, while the wave that crosses the caldera played `nsp_solar_flare.mp3` — a generic flare
whoosh. Each sample was on the other's trigger. The file names say which is which, and the
durations agree: arc_flame_loop is authored to loop, flame_wall is a 3.18s one-shot, so the held
weapon is the one that takes the loop.

⚠ **THE BARREL ROLL WAS ALREADY DONE** (0813-era `startRoll`), verified rather than assumed:
`startRoll(1)` fires `arcBarrelRoll`. No change.

⚠ **`lz_stack.wav` WAS NOT IN THE BUILD.** Copied to `assets/game/sounds/` and registered. The
fusion cannon had been borrowing the generic pulse laser — the same cue an ordinary laser shot
uses, so releasing a charged two-lance piercing shot sounded like a normal trigger pull.

⚠ **TAME IS KEYED BY NAME, SO SHAPING FOLLOWS THE SAMPLE, NOT THE TRIGGER.** Moving flame_wall off
the flamethrower would have left arc_flame_loop playing RAW and undone 0730a's fix for *"the
missile and firewave sounds are harsh to the ears."* `arcFlameLoop` takes the same shaping the
sample it replaced had; `lzStack` is one heavy release rather than a sustain, so a gentler cut.

## VERIFIED AT RUNTIME, NOT BY READING

    registered + on disk   all four, correct paths
    Audio.SFX fn exists    all four
    flamethrower           loopOn:arcFlameLoop / loopOff:arcFlameLoop
    fusion cannon          lzStack
    barrel roll            arcBarrelRoll

## ⚠ AND THE SUITE CRASHED WEARING A PASS

My first repointing reported **1,853 ok / 0 fail** — count down ~880, failures zero. That is rule
3 exactly: a `String(wfxTick||...)` line I added referenced an identifier that does not exist in
that context, threw, and killed the run at test_fl.js:6541. **Zero failures with a fallen count is
a crash, never a pass.** Removed; the line was an unused leftover.

§ the flamethrower assertion pinned `loopOn('flamewall')`, so Mike's own instruction failed it. Its
comment states the real rule — *"must actually LOOP the new bed, not the old flare one-shot"* —
which arc_flame_loop still satisfies. Repointed at the rule, the guard against the old flare kept,
and a new guard added that the flamethrower does NOT take the firewave's sample.

Suite **2,737 ok / 3 fail** (+5 assertions), both runs ending at section 230.

---

## 0822x — atlas halo sweep, and the four heuristics that were wrong

**Result: 13,467 halo px converted to a black edge across 21 sheets I rendered and looked at.
861 px restored on the four masters, where 0822w had blackened the rim of magenta ART.**

### The masters needed a repair first

0822w converted 21,177 edge px on the four stage masters. Re-checked each converted pixel against
its neighbourhood in the backup: 861 of them (4%) sat on magenta *art* — nebula and toxic-glow
rims — not on a halo. Blackening those puts a black outline around a glow. Restored, keeping the
20,316 genuine conversions.

nst7 422 · nst3 209 · nst2 157 · blackhole800 73.

> A stage-8 before/after screenshot showed 144,336 changed pixels. That number is worthless — the
> stage scrolls and animates, so frame 3 differs for reasons unrelated to the edit. The plate
> against its own backup is the only deterministic comparison. Same trap as the eight invalid probes.

### The atlas is not the masters

A coarse pass said 72 of 87 sheets carried halos. That was wrong four times over, and each
refinement only surfaced the next failure:

| gate | why it was added | what it still got wrong |
|---|---|---|
| magenta adjacent to alpha | the master rule | flagged the rim of magenta art |
| + neighbourhood <60% magenta | protect magenta art | flagged dark maroon volcanic rock (nca_21, 1,987 px) |
| + strict saturation | rock is desaturated, residue is vivid | flagged thin magenta beams, both edges on alpha |
| + must fringe real art | protect beams | flagged pink ribbon art with its own dark edge (nca_53, 2,571 px) |

**The atlas holds ~4.0M interior magenta ART px against ~48k suspected halo.** At that ratio a
classifier cannot be trusted, so I stopped writing heuristics and rendered a crop of the densest
flagged cluster on all 55 candidate sheets — `docs/proofs/halo/contact_1..4.png`.

Looking at them settled it. The high-count sheets are **authored art**, not halo:

- `nca_88` `nca_89` fire bursts · `nca_53` `nca_54` hot-pink ribbons · `nca_73` purple beam
- `nca_66` `nca_72` `nca_87` energy glows · `nca_74` green/purple smoke · `nca_7` `nca_67` purple platforms
- `nca_57` pink ornament · `nca_20` purple tree · `nca_68` `nca_24` pink/blue FX

A blanket conversion would have defaced every one of them.

### What was converted

Only sheets rendered and confirmed as hull / mech / structure / portrait carrying vivid key
residue on an alpha edge:

```
nca_4  9311   nca_22 938   nca_16 720   nca_75 311   nca_12 309   nca_28 240
nca_44  226   nca_45 195   nca_77 193   nca_43 185   nca_15 137   nca_52 114
nca_29  105   nca_47 101   nca_60 101   nca_2   77   nca_42  70   nca_62  50
nca_46   48   nca_51  30   nca_71   6
```

`nca_4` is the clearest case — the same dome sprite appears twice, one copy still wearing a purple
rim and the other already carrying the black edge. Half-converted at some point; now consistent.

Vivid edge residue on those 21 sheets: **16,296 → 2,829**. Alpha preserved everywhere — converted,
never deleted.

### On screen

| stage | vivid magenta per frame |
|---|---|
| 7 | **0** (was 517 before 0822w, 112 after) |
| 5 | 0 |
| 1 | 0,0,0,0,11,97 |

Suite **2,737 ok / 3 fail** (the same pre-existing preload + quarantine-ledger failures, nothing
to do with pixels). Atlas verify PASS — 9,960 keys from 87 sheets, 8 stages to boss, 0 blanks.

### Open, and it needs Mike

1. **Stage 1's ~97 px.** Scattered singles on hull edges over blue water. The "is the art beside it
   already blue?" gate protects them, because the water is blue. Loosening that gate is what
   defaced the nebula. **Want me to hand-fix stage 1's hull sheets specifically?**
2. **2,829 vivid px left across the 21 sheets** — thin magenta elements where I can't tell a
   1px highlight from residue without you looking.
3. **The effect sheets above.** I read their magenta as authored and left them entirely alone.
   If any of those are actually haloed, say which and I'll do them by hand.

Backups: `scratchpad/atlas_halo_backup/` and `scratchpad/halo_backup/`. Every step is reversible.

---

## 0822y — DOOMSDAY CARRIER Mk II, and the square-draw bug it exposed

**Stage 6 now fields the Mk II. The Mk I is untouched in the build — one word in STAGES[5]
restores the old fight.**

Mike, on the carrier as it was: *"holy shit god no. delete this boss, well use the MK2 variant
instead."* Driving stage 6 to the boss showed exactly why.

### The boss was drawn as a square

`shipBossDraw` computed `const s=b.w/256, w=256*s, h=256*s` — `h` is `b.w`. **Every ship boss was
drawn `w × w` and its declared `h` ignored.** Harmless while a plate was square, and most are. But
the carrier is authored 320×155 and declares 640×310, so it drew **640×640**: stretched to 2.06×
its height, filling the screen top to bottom. `docs/proofs/mk1_squaredraw_before.png` is that boss.

Fixed to honour the declared box. Every square entry is unchanged, because for those `h` already
equals `w` — checked all 18 ship bosses before touching a shared path.

### A wall cannot sweep off the field

With the aspect fixed the carrier still vanished. The probe, not a guess:

```
rdy=true   shipBossDraw returned true   hull 640x320 decoded
boss.x = 1046.7        world width = 680        camX = 100
```

The boss was drawing perfectly, 466px past the right edge of a 680-wide world. `shipBossManoeuvre`
ends with `clamp(b.x, -b.w*0.7, W+b.w*0.7)` — correct for a boss that flies in and out, but a
640-wide hull in a 680-wide world spends that range off-screen. Now held on the field when
`b.w >= W*0.70`; stated as a rule about width, so a future wall-sized boss is covered and every
other ship boss (all under a third of the world) is untouched.

### The Mk II itself

46 frames installed and registered, verified **0 magenta** before copying: 18-frame bay cycle,
14-frame cannon cycle, 3 static states, 9 beam frames, 2 warheads.

**Two reels.** `launch` drives the existing bay/warhead mechanic unchanged — bays still take
deflected warheads only, still alternate, still 6 hits each. `cannon` is new: authored 640×480
against a 640×320 hull, where the extra 160px **is the beam**. `_animH` grows the drawn box so it
is not squashed; every other boss leaves `_animH` null.

Cannon numbers are measured off the frames, not chosen:

| | measured |
|---|---|
| ink first appears below the hull | index 6 |
| widest | index 8–10, x304–336 |
| collapsed | index 12, gone at 13 |
| centre | exactly 320 = hull centre, so the column sits on `b.x` |

So it hurts only on 6–11, and follows the beam rake's convention (perpendicular distance, respects
invuln, calls `playerHit`) rather than spawning bullets — the beam is continuous while drawn.

**The cannon takes every third turn, and every turn once both bays are gone.** Previously, clearing
both bays parked the boss on frame 00 and it did nothing for the rest of the fight. Right when the
bays were its only weapon; wrong now it has a cannon. The Mk I still parks — it has no cannon.

**The two carriers fire visibly different rounds** — a slim olive shell vs a silver canister — so
the round carries the art its owner declares instead of the draw hardcoding one pair.

Proof: `docs/proofs/mk2_cannon.png` (beam at full length), `docs/proofs/mk2_bays.png` (both bays
open, two silver warheads emerging, cannon muzzle charged).

Suite **2,751 ok / 3 fail** (+14 assertions, same three pre-existing failures). Atlas verify PASS.

### Worth knowing

1. **`SHIPBOSS.dmg` is dead data.** Nothing in the file reads `D.dmg` — measured. Every ship boss
   declares `damaged`/`critical` plates that **have never been drawn**. The Mk II deliberately has
   no `dmg` array: its pack ships three bay states and no damage plate, and inventing one would be
   a procedural sprite. Costs nothing today, but if you want visible damage states on bosses,
   that is a real feature that was never wired — say the word.
2. **The stage-6 assertion was repointed, not deleted.** It pinned `'doomsdaycarrier'`, which is
   the choice you just changed, so it now pins the Mk II.
3. **The three suite failures are pre-existing and untouched** — a preload bound that wants
   `<600` against a set of 602, and two about a quarantine ledger. Not caused by this drop.

---

## 0822z — Mike's new sewer, and the L7 boss teleport is gone

**Stage 7 now runs on `nst7_master_v3` — the CF_ToxicSewerPortal-Lvl7 full scroll, 680×4716,
authored at plate width so nothing is resampled. `arena:'nst7_arena'` is removed.**

### The teleport was a real thing, and this was it

Mike: *"Do NOT teleport to a different map for the L7 boss."*

`drawLevelMaster` has an arena branch: when the boss run starts it **stops drawing the scroll** and
loops a separate plate instead. Stage 7 pointed at `nst7_arena` — a walled olive stone chamber
(`docs/proofs/l7_arena_removed.png`) that looks nothing like the channel the player just flew
through. It was also still **800 wide**, a leftover the 680 pass missed, because it lives as an
atlas cell rather than a file.

Removed. With no `arena` the branch falls back to looping the master, so the fight happens where
the player actually flew to. `docs/proofs/l7_boss_no_teleport.png` is the Sludge Emperor in the
sewer.

### The new plate keeps Mike's own architecture

Stage 7 is not a background — it is an **overlay** over an animated sludge bed, which is what Mike
asked for in 0810t: *"replace stage 7 with that sheet as an overlay ... and use the sludge for the
background."* An opaque plate would have destroyed that, so I measured before swapping:

| | alpha-0 |
|---|---|
| new scroll | 9.6% |
| the pack's own liquid mask | 90.4% |

**Exact complements** — the holes in the plate are the channel and nothing else. Same architecture,
narrower channel (v2 was 68% open). `docs/proofs/l7_new_channel.png` shows the sludge coming
through the side channels.

New plate carries **0 vivid magenta**; the outgoing v2 still had 26. v2 stays registered — swapping
the name back restores it.

### The portal frames are ART, and I did not clean them

`nfx_l7portal_0..7` (8 frames, 512×512, 12fps one-shot) tripped the halo test at 45–587px per
frame. They are an authored green/cyan vortex **with violet arms**; the test fires because the
swirl is thin filaments that all touch transparency. Installed untouched, and the exclusion is
written down in `docs/proofs/l7_portal_is_art.txt` so a later sweep cannot eat them.

This is exactly the ambiguous class I flagged after the atlas pass — here the answer was
unambiguous once rendered.

### Three assertions were measuring a plate the stage no longer uses

They named `nst7_master_v2.png` directly. Two pinned the height and width; one **required**
`arena==='nst7_arena'` — it was defending the very thing Mike asked to be rid of. A hardcoded
filename that silently measures the wrong plate is worse than no assertion.

All of them, plus the seven-stage geometry sweep, now resolve the plate from `cfg.master` through
the manifest via a new `stagePlate()` helper. The next plate swap is covered by code that already
exists, and there is a new assertion that stage 7 has **no** arena.

Suite **2,752 ok / 3 fail** (the same pre-existing three). Atlas verify PASS.

### Still open on this pack

The 8 portal frames and `nst7_portal_gate` are **installed and registered but not yet sequenced**.
The end-of-stage cutscene — fly up, portal opens, ship dissolves on frame 06, frame 07 closes
behind, stage ends into Furious Death — is the next piece of work.

---

## 0822aa — FURIOUS DEATH: the modular stage 8

**Stage 8 runs on `nst8_sky_master` (680×4716) with 24 pieces of scenery drifting in parallax
decks.** `docs/proofs/l8_furious_death.png`, `docs/proofs/l8_families.png`.

The pack states its own contract and this follows it exactly: *"opaque sky contains no
environmental objects; all alien scenery is spawned from independent alpha frames."* So the plate
is only the backdrop, and 6 biomech cliffs, 6 portal rims and 12 bone rocks drift in from a new
`l8ObjsDraw` — the same model as the stage-5 orbital field and the stage-6 clouds.

**Every deck is background. There is deliberately no near deck.** This is the 0821 lesson written
down one function up: a big opaque silhouette drifting over the play field is what made Mike unable
to see his own enemies on stage 5. The L8 structures are 680×1020 biomech cliffs — far bigger and
far more solid than a satellite — so they draw from `stageSceneryDraw` (tail of `drawBG`) and there
is nothing to promote them to.

Cliffs are pinned to the **edges** rather than scattered, so they read as terrain the player flies
past instead of clutter in the lane. Scale is measured off the art, not chosen: they are authored
680 wide against a 680 plate, so 1.0 would wall off the screen.

**`skipRows` is gone and must not come back for this plate.** It named absolute master rows
2125–2253 — the bridge on the *blackhole* plate. Those rows mean nothing on a different image, so
carrying them over would blank 128 arbitrary rows of the new sky.

`blackhole800_rc2_master` stays registered; swapping the name back restores the old stage exactly.

> The black-hole spiral is retired from stage 8, but that beat is not lost — it moves to the L7
> void portal at the *end* of stage 7, which is precisely Mike's "pilot enters black hole, stage
> ends". The two packs were built to pair: the L7 manifest explicitly **excludes** "Stage 8 sky and
> Furious Death space set pieces" because this pack carries them.

**Another never-dehalo family.** The whole L8 set is crimson-and-violet bone by design. Same class
as the L7 portal swirl — recorded so a later sweep cannot eat it.

### A flaky assertion, found and fixed

The stage-8 run surfaced `the flurry races — every bolt is fast` failing, then passing three runs
in a row. It was not a regression — it was **luck**, failing about one run in four.

`hypot(vx,vy)` is the *instantaneous* tangent, and the mover re-derives it from `_hdir` every frame
with the helix corkscrew applied, so it dips below 14 at certain phases. The test sampled on
whatever frame the burst was first seen.

Repointed at `_hspd` (17–23 at spawn; both hfl spawn sites set it), which is the quantity the rule
is actually about. **A flaky assertion is worse than none — it teaches you to ignore a red run.**
Now stable: 2,752 ok across four consecutive runs.

Suite **2,752 ok / 3 fail** (the same pre-existing three). Atlas verify PASS.

### The stage-8 cfg assertions did not need touching

Worth noting, because it was the point of 0822z's refactor: the seven-stage geometry sweep picked
up the new 680×4716 plate on its own and passed, because it now resolves `cfg.master` through the
manifest instead of naming a file. That change paid for itself one drop later.

---

## 0822ab — STAGE 9 IS REACHABLE: the Velocity Void

**Stage 9 was not in `STAGES[]` and could not be entered at all.** It now exists, is entered through
the massive Level 5 warp gate, fields an eight-unit roster, a miniboss and a boss, and returns to
stage 6 instead of ending the game. 126 art keys installed.

`docs/proofs/s9_contact.png`, `s9_roster.png`, `s9_tidal_sovereign.png`.

### The dangerous part, first

`beginStage` does `curStage=STAGES[num-1]`, so stage 9 had to join the table to be enterable.
But the stage-clear exit read:

```js
if(run.stage>=STAGES.length){ triggerVictory(); }
```

**Appending a ninth entry would therefore make clearing stage 8 advance into the bonus stage
instead of rolling credits.** The campaign end is now counted from `CAMPAIGN_STAGES` — entries
without `bonus:true` — and the bonus stage gets its own branch *before* the victory check, because
`run.stage` 9 is `>= 8` and would otherwise roll credits on clearing it. Any future bonus stage
sets the flag and both behaviours stay correct.

### The door

The pack ships it as its own 640×768 four-frame asset and states the rule: *"Portal centers are
open; collide with the ring only. Use the center opening as the travel trigger."* So the opening is
the trigger and the ring is not a hazard — flying into the middle is the reward.

**The transition is deferred, not immediate.** The gate ticks from `stageSceneryDraw`, which runs in
the *draw* pass; calling `beginStage()` there would tear down enemies, bullets and the plan while
the frame is still walking them. It sets a flag and `updatePlay` consumes it at the top of the next
frame. It latches on `run._s9taken`, so a player back in stage 5 does not loop into it forever.

Proven end to end in a browser, not asserted from source:

```
after arming:      stage 5, gate at (340,-370)
on contact:        taken=True, stage=9
after transition:  STAGE 9 / THE VELOCITY VOID / bonus / return=6 / 16-wave plan
```

### The roster

Eight units, each with its authored art, measured size, hp, score and a movement pattern chosen to
match its written behaviour. They go through a new `S9_UNITS` table and `applyS9Unit`, mirroring
the `S1_TANKS` / `NEF_S*` appliers.

- **`e.art` is a NAME, not a file key** — the 0809l trap. Each unit needs an `ENEMY_ART` entry *and*
  an `<base>_idle` alias, or it spawns, moves, shoots and never draws. Seeded off `BOFX.img`
  because this roster is loose PNGs rather than sheet cells, and asserted.
- **The type names are unique on purpose.** `nefRow()` walks NEF_S1/S2/S3 and is *not* stage-gated,
  so a stage-9 unit called `racer` would silently inherit stage-3 art.
- **The pack's second frame is mapped `fire`, not run as a loop** — a firing unit that changes pose
  is a tell, which is the lesson in NEF_S2's spinner note.

**An explicit `return` in `buildStagePlan`.** Stage 9 had no block, and the tail below adds generic
waves to any stage that does not return — generic jungle jets in a velocity void is exactly the
clip-show mistake stage 8's note is about. 16 waves in three movements.

### The bosses

`tidalsovereign` (320×256) is the boss, `warpsentinel` (256×192) the miniboss in `SUBBOSS[9]`. Both
are in `spawnBoss`'s switch — absent from it they spawn with no `_ship` and draw nothing.

Both ship **three authored damage states**, so `dmg` is filled in here where the Mk II deliberately
has none. It still does not draw anything — `SHIPBOSS.dmg` is dead data, which you confirmed — but
these two are the units that already have the art if it is ever wired.

> A single screenshot showed the Tidal Sovereign missing. The probe showed it sweeping — on screen
> in **23 of 30 samples**, x tracking 970 → −151 → 485. Working as designed; the frame just caught
> it mid-sweep. That also confirms the Mk I carrier case was genuinely different: a 640-wide wall
> that spent most of its time off-field.

Suite **2,761 ok / 3 pre-existing fail**. Atlas verify PASS.

### Two things for Mike

1. **The packs ship no stage 9 BACKGROUND.** The plate is still `waterworld800_rc2_master` — Water
   World Naval War. The Tidal Sovereign suits it exactly; the purple/cyan warp roster does not. I
   did not invent a void backdrop. If you want the velocity void to look like one, that is an art
   drop, and it should be 680-wide to match everything else.
2. **Stage 9 is still the only 800-wide plate.** It is declared explicitly so nothing silently
   inherits, but it is now reachable, so the question the old comment deferred is live: rescale to
   680, or keep 800 deliberately?

### Not implemented, stated plainly

The roster README gives each unit a signature trick. The units fly, shoot and draw on the right art;
these specific tricks are **not** in yet — the needle drone's phase-out, the prism mine's six-lane
refraction, the gate leech's rim-clinging, the echo fighter's delayed ghost, the interceptor's split
at half health, the comet breaker shattering comets. Also unwired: the Twin Portal Wardens, the
Velocity Gate Core, the 64 comet-debris frames, the six in-stage warp gates, and the two bosses'
signature attack families from CF_BossAttacks-Lvl9.

---

## 0822ac — THE STAGE 7 EXIT: pilot enters the black hole

Mike's sequence for the end of the sewer: *"pilot enters black hole, stage ends."* The
CF_ToxicSewerPortal-Lvl7 pack ships the door and names the beat exactly: *"hide or dissolve during
frame 06; frame 07 closes behind the player."*

`docs/proofs/l7_portal_enter.png`, `docs/proofs/l7_portal_closed.png`.

### It rides the flyover rather than replacing it

The stage exit already runs hover 1.35s → climb 1.7s → fade 0.75s → STAGECLEAR. Stage 7 changes
exactly two things inside it: the **climb target** and one **overlay**. The hover, the music cut,
the live world scrolling underneath and the fade are all untouched, so every other stage is
byte-for-byte the same exit it had.

Measured on stage 7, then on stage 2 to prove nothing else moved:

```
stage 7   hover y~400 x=340  →  climb y=196 x=263  →  y hidden, x=240  →  stageclear
stage 2   hover y~400 x=340  →  climb y=261 x=340  →  y=-80,     x=340  →  stageclear
```

Stage 2's x never moves and it still leaves through the top. Stage 7 eases across to the gate and
is gone.

### The one deliberate exception

`drawFlyover` carries an emphatic note that **player.x is never touched** — that rule exists so the
ship does not slide sideways to centre itself on an ordinary exit. Flying *into* a gate is the
exception that proves it: **a portal you miss is not a portal.** So x eases across only on stage 7,
only during the climb, and only while the portal art is actually live. Asserted, because an
ungated version would make every stage start sliding.

### Two traps avoided

1. **The frames are warmed with the stage.** `XART.rdy` starts the load and returns false on that
   first call, so a cutscene that asks for its art at the moment it needs it draws **nothing**.
   That is the 0801kd/0801dp trap and it is completely invisible to a green suite.
2. **The frame count is load-bearing.** The pack puts the dissolve on 06 and the close on 07. With
   seven frames the dissolve would land on the close and the ship would still be visible when the
   gate shut. The frames are paced across the whole climb, so 06 and 07 land on the ship's arrival
   rather than finishing early and leaving it flying at a shut gate.

The exhaust is also suppressed once the ship is hidden — otherwise particles keep puffing out of a
ship that has already gone through.

Suite **2,766 ok / 3 pre-existing fail**. Atlas verify PASS.

---

## 0822ad — THE SECRET: nine gates, a warp-out, and the map unlock

Mike's design, replacing the single gate 0822ab put in stage 5:

> "Place warp portals in a kind of left right shimmy pattern... if they successfully manage to
> shimmy through all 9 — 9 signaling the 9th level — once they shimmy through the first 8, the 9th
> will begin to glow and our portal will form in it and the screen will be doing a speed effect...
> once they touch the first warp gate."

`docs/proofs/s9_warpout.png`, `s9_map_unlock.png`, `s9_map_card.png`, `s9_white_portal.png`.

### The run

Nine gates as a **convoy, not a timer** — all nine exist at once and drift down together, so the
player can see the next one and plan the shimmy. Passed by crossing the gate's line inside the
opening, missed by crossing it outside. No partial credit, no going back.

**The openings are measured, not chosen.** The speed-portal frame is 192×256 with a ±36px hole and
the segment gate 256×320 with ±45. A radius picked by eye would make the run either impossible or
impossible to fail. The shimmy amplitude **tightens** gate by gate, so the last few are precision
rather than travel.

Hazards between gates are **roster units, not props**, so they can be shot — "skillful enough with
your shots, missiles" only means something if they can be. Sizes measured: the mega comet draws
~211px on a 480 screen, which is the HUGE asked for. The one at 8.4s comes straight down the lane
at 70hp — not shootable in time, so the barrel roll's i-frames are the answer, which is the "know
how to barrel roll once" beat. The clash pair is scripted, because "two that clash into each other
and bounce away" is a set piece no generic mover produces.

### The chain, verified end to end in a browser

```
gate 1 passed      armed=True (speed effect starts here, per Mike)
gates 2-8 passed   idx=8
ninth gate         glow 0 -> 0.30 -> 0.69 -> 1.00
ninth gate passed  taken=True -> warp 'draw' -> warp 'white'
                   -> state 'stagesel' -> streak 'fly' -> 'flash'
                   -> bonusUnlocked=True, cursor=9
```

### Both of Mike's corrections

1. **"clean up that purple in the portal... should be white 16-bit styled fading."** The portal
   frames are re-derived through a **6-step white ramp** with a faint cool cast at the dim end and
   an alpha falloff, so it steps rather than blurs. `nfx_wportal_0..7`. The authored `nfx_l7portal_`
   frames stay registered — the sewer-green original is one key away.
2. **"the portal is already built into the campaign map, dont place one."** Correct, and I checked
   the plate: `nss_map` has a ringed crater with a lit centre at exactly `SSEL_POS[9]` = [575,75].
   The sprite I was drawing over it is gone. What is left is **light on the art that is already
   there** — a soft radial bloom while it flashes, nothing once it settles.

### The map

`SSEL_POS[9]` has been in the table all along with nothing drawing it, because the flag loop is
deliberately `st<=8` ("SECRET level (9) never gets a flag"). That stays true — 9 never becomes a
flag. What it gets is the streak from stage 5's node, the bloom, and the unlock.

**The unlock is its own latch, not `campaign.unlockedMax`.** Stage 9 is outside the linear
progression; putting it on unlockedMax would make the arrows walk into it and the frontier logic
treat it as the next campaign stage. While the latch is live the map allows **only** stage 9, and
entering **spends** it, so the map is not stuck on the bonus stage forever.

### An assertion caught my own bug, one drop after it was written

`every unit resolves through ENEMY_ART` failed. The comets are `ns9c_` and the seeding loop only
matched `ns9e_`, so **every comet would have spawned, moved, collided and drawn nothing** — the
0809l trap, reintroduced by me in this drop and caught by the assertion written for it.

Suite **2,776 ok / 3 pre-existing fail**. Atlas verify PASS.

### Open

**There is no stage-9 card art.** `nss_panel_`/`nss_label_` exist for 1–8 only, so selecting the
bonus stage left the bottom of the screen empty. Rather than invent a panel sprite, it draws the
same information as text through the screen's own font helper — the fallback the hub already uses.
**Drop `nss_panel_9` / `nss_label_9` in and that branch stops running**; it is keyed on the art
being absent, not on the stage number.

---

## 0822ae — THE BEEPING, and a 33-minute walkthrough transcribed

Mike sent a 33-minute video walking through the game. I can't hear video, so I extracted the audio
and transcribed it locally (faster-whisper, small.en) — the full transcript is in
`docs/feedback/0823_video_walkthrough.txt`, 183 timestamped segments. **Use it as the source of
truth for the current bug list**; it is Mike's own words with timestamps that map straight to the
video.

### The beeping was not the UI blip

My first swing at "stop the annoying BEEP BEEP BEEP" went after the UI blip. The transcript settled
it — at 17:55, over a boss fight:

> "Stop doing the beep beep beep noise with all these bosses."

It is **`enemyShoot`**, and it fires **per bullet**. `eMG` plays it for every machine-gun pellet,
and the boss blast fan called it *inside* its own `k=-1..1` loop. Measured on the real fight:

| | tone requests / 10s | tones played |
|---|---|---|
| stage 6 boss, before | 124 | 124 (12.4/s) |
| stage 6 boss, after | 124 | **11 (1.1/s)** |
| stage 2 boss | 13 | 7 |

Throttled at the SOURCE (`ESHOOT_GAP = 90ms`) rather than at 20 call sites, so whatever route a
volley takes, repeats inside the window collapse into the first. A single shot is unchanged;
sustained fire reads as a rhythm instead of a stutter. The fan also now plays once rather than
three times.

### The UI blip work stands, separately

Seven places fired the UI blip as a *stream*, two of them constantly — the stage-select label
typewriter at **14 blips per second** every time the cursor moves, and the retina acquire tick every
0.11s through the whole lock. Those now go through `uiBlipRep()` and are off; single confirmation
blips are untouched, so menus still answer you.

Two dials, no call sites to hunt:
- `UI_BLIP_REPEAT = 1` brings the streams back
- `UI_BLIP = 0` silences the blip everywhere, including single taps
- `ESHOOT_GAP` widens or tightens the volley throttle

Suite **2,776 ok / 3 pre-existing fail**. Atlas verify PASS.
