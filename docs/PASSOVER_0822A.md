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
