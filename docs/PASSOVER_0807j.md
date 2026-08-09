# PASSOVER — drop 0807j   (THE APPROVED SMOKE SET ONLY)

Build: `BulletsOfFury_0807j`
Harness: **2,138 assertions / 196 sections / 0 failing**, twice, reaching the banner.
Cells: **9,567 / 9,567 resolve, 0 at the wrong size.**

---

## 1. MEASURED WHICH ONES WERE "THE FLAT SPRITES" RATHER THAN GUESSING

Mike: *"you can may use the smoke chimney, remove the flat sprites, just use the smoke, the smoke
underneath, the smoke rings. those are all solid."*

Mean channel bias separates dust from smoke cleanly — dust runs warm, smoke sits neutral — and it
agreed with his call exactly, which is the useful part: the reading was not a judgement, it was a
measurement that happened to match.

    KEPT
      nsd_diss   6690 colours   neutral  +4    "the smoke"
      nsd_fog    4518           neutral -56    "the smoke underneath"
      nsd_ring   3926           neutral +10    "the smoke rings"
      nsd_chim   3841           neutral  -2    the chimney
    DROPPED
      nsd_dust   4812           WARM    +98    dust, not smoke
      nsd_devil    57           WARM   +106    dust, and genuinely flat — 57 colours
      nsd_steam  2772           white          steam, not smoke

`nsd_devil` at 57 colours is the one that is unambiguously flat; the two others go because they
are dust and steam rather than smoke, which is what he asked to keep.

## 2. THE SHEET WAS REPACKED, NOT LEFT WITH HOLES

Removing 24 frames from a packed sheet leaves dead pixels that still decode. The survivors were
pulled back out and repacked tight:

    2112x1614 -> 2112x872
    13.6 MB -> 7.4 MB decoded     1.6 MB -> 1.1 MB on disk

Verified after: 9,567 cells resolve, none at the wrong size, no broken paths.

## 3. WHERE THE DAMAGE STATES STAND

    above 65%     nothing
    65% -> 35%    nsd_diss    1 vent
    35% -> 15%    nsd_chim    2 vents, looping
    below 15%     nxp_upward  2 vents + nsd_chim rising off the fire

`nsd_fog` and `nsd_ring` are installed and approved but not yet placed. The obvious homes:
**fog** as low stage ambience, **rings** off a heavy cannon muzzle. Say the word and I will wire
either.

## 4. STILL OPEN FROM THE PLAYTHROUGH

Eight: stats screen · dialogue box art · liftoff music · L2 miniboss routing into lava · the tank
on the mountain · the runway plate · retiring the beach water · L2/L3 boss assembly spacing.
