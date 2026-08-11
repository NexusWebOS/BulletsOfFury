# HARNESS TRIAGE — drop 0810a

    verify_0730a   311 passed / 17 failed  (TRUNCATED)  ->  423 passed / 8 failed  (complete)
    test_fl       2094 passed /  2 failed  (unchanged, both environment)

---

## 1. THE HEADLINE NUMBER WAS FOR A TRUNCATED RUN

`verify_0730a` was crashing 424 lines from the end — `pth.join(ROOT, IMG[SS[st].master])` threw
`ERR_INVALID_ARG_TYPE` when stage 6's stagestack entry named a plate that no longer exists. Node
exits, the suite prints no banner, and the pass count looks like a complete run because nothing
says otherwise.

**Nearly a fifth of the suite had never executed.** Every total reported before this drop — mine
included — was for a partial pass. Guarded, so a missing key fails one assertion and names the
stage instead of killing the process.

That is the **third** assert-then-use crash found this drop, after `_chroma_backup` in this file
and `_superseded` in `test_fl`. The shape is always the same:

    ok(fs.existsSync(p), '...');     // correctly fails
    fs.readFileSync(p);              // and then throws, taking the suite with it

A failing assertion must fail. It must never abort the run.

## 2. THE BIGGEST CAUSE OF FALSE FAILURES: FIXED-SIZE SLICES

Five assertions read a function by slicing a fixed byte count and searching inside it:

    const blk = src.slice(i, i+7500);    // pcDraw is 12,844 chars
    const blk = src.slice(i, i+9000);    // socket constants live at 11409 and 11455
    const blk = src.slice(i, i+2600);    // the MG markers are at 4579 and 4879

Every one of them reported **the code is gone** when the truth was **the function grew**. The MG
one is the clearest: it asserts `indexOf(A) < indexOf(B)`, both came back `-1`, and `-1 < -1` is
false — so a correct ordering failed on two absences.

`pcDraw` now reads via a brace-matched `fnSource()` helper. The MG block was widened.

**Five of the seventeen failures were this, and nothing was actually wrong in the game.**

## 3. STALE ASSERTIONS — RED BECAUSE THE DESIGN MOVED ON

Each of these was testing a decision that was later reversed or superseded. Rewritten to assert
what replaced it, so the record survives and the current decision is what is protected.

**The per-level projectile grid.** Asserted that every level had its own `nep_<stage>_*` set and
that the arsenal path ran ahead of FIRETYPES. Mike reversed exactly this:

> *"I found the projectile problem. you've been use the wrong family the entire time.. your using
> the 1st screenshot family when it should've been the other 2."*

Bosses now draw their own `bfx_` plate, everything else falls through to FIRETYPES. `nep_`/`nbp_`
is registered and deliberately never consulted — 14 orphaned keys survive, all level 9, safe to
delete when you want them gone.

**The pilot card header.** Pinned `cy+ch*0.112` for the callsign; it is 0.108 now. Asserting the
ORDER instead — name in the header band, callsign below it, body below both — which still catches
a callsign above a name or a body overrunning the header, and survives a designer nudging a row.

**The emblem.** Pinned "82% and nudged 6% right", a hand correction for it sitting off-centre. The
code aspect-fits and CENTRES it in the measured socket now, which is the better answer and makes
the nudge meaningless.

**Falva's charge.** Looked for the literal `'fchg_0'`, which the code never contains: it does
`CHG_SET[pilot] || 'fchg_'` then `pre+'0'`. A dynamic lookup was never going to produce that
string. Asserting the mechanism.

**The stage-master sweep.** Read `BOFX.stagestack`, a table **nothing in game.js consults** — only
this file does. Its stage-6 row still names `nst6_master`, deleted on purpose ("delete all of
stage 6's backgrounds"). Repointed at `_levelCfg().master`, the key the engine actually draws.

**The drone count.** `ok(B===12)` broke when the three arsenal minis gained profiles. Derived from
the rosters now, so a drone added without a profile fails here rather than silently inheriting
cryoeye's behaviour from `droneInit`'s fallback.

**The sub-boss sweep.** Demanded every `SUBBOSS` entry spawn, which contradicted `DEAD_SUBBOSS`
existing at all — and only ever passed because that retirement was broken. Skips retired kinds,
driven off `DEAD_SUBBOSS` itself.

## 4. WHAT IS STILL RED, AND WHY

### Five: ⚠ WRONG MACHINE — not a defect, and not a packaging mistake

    the original lv3 sprite is backed up
    and the shipped lv3 sprite differs from it
    chain frames backed up before the recolour
    the 8 green and blue lasers were cleaned of chroma spill
    all 9 masters backed up before the halo pass

All five check `_chroma_backup/`. The two `test_fl` failures are the same thing for `_superseded/`.

**Mike: "thats cause were not on the local machine with BOF on it."**

That is the answer, and it corrects what I had assumed. I searched the Desktop and Downloads,
found nothing, and inferred the folders had been excluded when the build was zipped. They were not
excluded — **this tree is a copy on a secondary machine, and the working folders live on the
primary one.** `_chroma_backup`, `_superseded` (126MB) and `_halo_backup` are all there.

So the correct reading of these seven is **"cannot be checked from here"** — not "the art is
wrong", and not "the backups were lost". They assert that art operations are REVERSIBLE, and the
evidence for that is on the other machine.

    THIS TREE (secondary)   verify 423/8    test_fl 2094/2
    PRIMARY MACHINE         expect          verify 423/3    test_fl 2096/0

The 0807c passover reported **2,095 / 191 / 0** for `test_fl`, which is exactly what a run on the
primary machine looks like — that number has always been the primary's, and it corroborates this.

**WHEN NEXT ON THE PRIMARY MACHINE** (Mike expects to be, ~3 hours from this drop):

1. Re-run both harnesses there. Those seven should go green with no code change. If any of them
   still fails, THAT is a real finding — it would mean a backup genuinely went missing rather than
   being on the other box.
2. The three real gaps in the next section are machine-independent and will still be red.
3. Nothing in this drop's code needs re-checking on that machine; the fixes are all in files that
   travel with the tree.

### ⚠ CORRECTION — I claimed three real gaps. There is ONE.

Two of the three were the SAME mistake I had just finished documenting for other assertions:
treating the absence of an exact string as evidence of absent behaviour. I wrote the rule down and
then broke it twice in the same pass.

**The supply-box RNG exists.** `mslPackRoll()` does exactly the authored split:

    const r = Math.random();
    return r<0.50 ? 'missilepack2' : (r<0.80 ? 'missilepack' : 'missilepack10');

The assertion searched for `"_r<0.50 ? 'missilepack2'"` — with an underscore. The variable is `r`.
My triage regex required the underscore too, so it confirmed my own error rather than testing it.
I was one step from writing a second implementation of a working feature. It now rolls the real
function 2000 times and checks the distribution: **50% / 28% / 21%**.

**The flamethrower fallback is not missing — it is unnecessary.** The assertion wanted a fallback
for when the getImageData composite is unavailable under `file://`. Drop 0801bb solved that by
*deleting the composite*: "Mirroring at draw time produces the same symmetric column with no pixel
reads at all, so the composite is gone and there is exactly one path left." Verified: **no
`getImageData` anywhere in the flame draw path**, so there is nothing to taint and nothing to fall
back from. The failure class is structurally impossible, not handled.

`flamePair()` does survive as dead code — defined, called from nowhere. Safe to delete when you
want it gone. Also note its comment claims "_flameRaw below is that path, and flameDraw uses it" —
**`_flameRaw` does not exist anywhere in the file.** A comment describing a fix that was never
written, left behind when the better fix landed.

### One: genuinely missing, and your call

**No weapon icons exist at all.** `micon_*` has **zero** keys. `index.html`'s out-of-screen
EQUIPPED box builds `micon_<weapon>_<level>` and guards with `XART.rdy`, so it silently draws its
frame and never an icon. Verified in the running game: the equip canvas has **0 lit pixels**. The
assertion names levels 6/7/8 (gold VI, black VII, purple VIII) but 1-5 are missing too.

That is the only one. See the correction above for the two I got wrong.

## 5. THE PATTERN WORTH KEEPING

Of seventeen failures: **seven were false** (fixed windows, stale literals), **four were stale**
(design moved on), **five are the wrong machine**, **one is a real gap**. Zero were the thing a red
test usually means — working code that broke.

    verify_0730a   311/17 (truncated)  ->  454 passed / 6 failed (complete)
    of the 6: five are the primary machine's backup folders, one is the missing weapon icons.

**Every single false failure had the same cause: matching source TEXT instead of testing
BEHAVIOUR.** Fixed byte windows, a variable renamed from `_r` to `r`, a key built as `pre+'0'`
instead of written as `'fchg_0'`, a layout constant nudged 0.112 -> 0.108. In each case the game
was correct and the test was describing an implementation that had moved on.

I made that same mistake twice myself while triaging — see the correction in §4 — which is the
strongest argument for the rule below.

A suite in that state trains you to ignore it. The two rules that would have prevented most of it:

1. **Never abort on a failed check.** Assert, then guard the use.
2. **Never read a function with a fixed byte count.** Brace-match it, or you are testing its length.
3. **Never assert on an exact source string when you can run the thing.** Call `mslPackRoll()` 2000
   times and check the split; do not grep for the ternary that implements it. Every false failure
   here was a string match, and a string match fails on a rename while a behavioural check does not.
