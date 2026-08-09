# PASSOVER — drop 0807g   (THE EFFECT ART, AUDITED PROPERLY)

Build: `BulletsOfFury_0807g`
Harness: **2,122 assertions / 194 sections / 0 failing**, twice, reaching the banner.

---

## 1. YOU WERE RIGHT ON ALL THREE COUNTS

Measured the ink colour count and edge contact of every candidate rather than eyeballing them:

    reel        colours   state
    ntr_smkL       13     clipped on 5 of 8 frames        flat — unusable
    ntr_fire       13     clipped on 5 of 8 frames        flat — unusable
    nx_smoke       37     ⚠ CROSS-FRAME BLEED
    ntr_smkH      275     clipped on 5 of 8 frames        the best smoke that exists
    nxp_* (x8)  1173-1525 clean                           the shaded set you remembered
    nqm_vent     2313     clipped                         NOT smoke — a vent port with a flame

**`nxp_smoke` is an explosion.** Confirmed — rendering all eight `nxp_` reels shows every one of
them is a fire burst. The name is wrong, not the art.

**`nx_smoke` is not clipped — it is BLED.** Rendered at native 136x136 over a checkerboard, every
frame carries fragments of its NEIGHBOURING frames alongside the main puff. It was sliced from a
packed sheet on the wrong grid. That is the documented trap in this project — *"packed
multi-frame sheets have cross-frame bleed; always slice from individual frames"* — and this reel
is a victim of exactly it.

**And the other explosion effects do exist:** the whole `nxp_` family, 1173-1525 colours, 256x256,
eight frames each, clean edges. Contact sheet attached.

## 2. ⚠ BUT THERE IS NO WELL-SHADED SMOKE IN THE GAME

That is the finding I did not expect and cannot code around. Every reel with real shading is an
EXPLOSION; every reel that is actually smoke is 13-37 colours, or bled, or cut.

    ntr_smkH   275 colours   the best smoke in the project, and it is cut on 5 of 8 frames

So the damage states now use what is genuinely best available rather than what the filenames
promised:

    65% -> 35%   ntr_smkH    1 vent, light
    35% -> 15%   ntr_smkH    2 vents, heavier
    below 15%    nxp_upward  2 vents — 1407 colours, a rising plume, properly shaded
                             AND ntr_smkH layered above it, so a burning unit still smokes

**The smoke gap needs art, not code.** If you have a shaded smoke reel on the drive — or the
source sheet `nx_smoke` was sliced from, so I can re-cut it on the right grid — that is the one
thing that would finish this properly.

## 3. ⚠ AND A NOTE ON THE DELETE LIST

`nqm_vent` sits in the `nqm_` family, which is the single biggest block on
`UNUSED_ART_CANDIDATES.txt` and the one I said I would delete first. It turned out to be a
2313-colour asset worth looking at. It was not the right art for this — but I found that by
RENDERING it, not by trusting the shortlist.

That is the second time this week the delete list has nearly cost something. Nothing on it should
go without a look first.

## 4. STILL OPEN

Eight from the playthrough list: stats screen · dialogue box art · liftoff music · L2 miniboss
routing into lava · the tank on the mountain · the runway plate · retiring the beach water ·
L2/L3 boss assembly spacing.
