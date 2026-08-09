# CLEANUP PASS — 0801

    verify 91 passed / 0 failed · manifest 7045 -> 6836 keys
    everything reversible: _quarantine/fx0801g/_ledger.json

## Done

| ask | result |
|---|---|
| weather: get rid of the n6w sprites | 30 quarantined, all unused |
| weather: get rid of slash / snow burst | nwf_splash, 6 files |
| weather: keep fire, lightning, rain, snow, bliz | all kept and still registered |
| level 06 weather -> weather | 48 files merged |
| lizzie's folder -> special | 5 files |
| old retina no longer needed | 100 files (ret_, retA_, retB_) quarantined. All unused — the live retinas are the nbret_ set already in icons/ |
| np5 -> a folder that fits | 12 -> assets/fx/objects |
| alert icons + enemy approaching -> with hud icons | 3 -> assets/fx/icons |
| dialogue boxes -> a UI folder | 10 -> assets/ui/dialogue |
| menu buttons: remove chaos and elite | 2 |
| helixchain: delete | done earlier this session |
| MG graphics into their own folder | 36 -> assets/fx/machinegun (mgmuz_, nmg_, mfx_mg_) |
| 5 recoloured muzzle variants | nmgv_1..5 cut from nmg_2 |

**The 5 variants, measured after recolour:**

    nmgv_1  hue  40  gold      mean sat 0.56
    nmgv_2  hue 220  blue      mean sat 0.56
    nmgv_3  hue 100  green     mean sat 0.56
    nmgv_4  ----     WHITE     mean sat 0.05   desaturated, not hue-shifted
    nmgv_5  hue   0  red       mean sat 0.56

lv4 is desaturated rather than rotated because white has no hue to rotate to. The tiers match the
bullet colours measured off `mfx_mg_` earlier, so the muzzle and the pellet agree at every level.

## NOT done, and why

**weapons/ — I did not delete `lzr` (35 keys) or `iceshard` (4).** You said *"Idk if anything is
currently being used in here."* Both are, actively. Deleting them would have broken the laser and
ice weapons. Only the MG moved out. Say the word and they go.

**master/ renaming to MG-1 / LB-1 / FW-1.** 227 files, and every one is referenced by its current
key. Renaming means rewriting the manifest AND every call site together — doable, but it is a
dedicated pass with its own verification, not something to slip into a sweep.

**ncl6 pixel spill.** Needs measuring per sprite and trimming per edge — art work, and I would
want to show you before and after per sprite rather than do it blind.

**Retina rework** (target enemy centre, white flash bottom-to-top, flash on lock, sound). That is
a behaviour change with a new draw and a new sound cue. The old art is out of the way, so it is
clear to build, but it is a feature not a move.

**helixbeam as an enemy attack.** The sprites are in `_quarantine/fx0801d` and restorable. Wiring
them to an enemy is new behaviour — worth doing deliberately.

**boxes and pills merge with stage 6-9.** I could not find a stage 6-9 boxes/pills set to merge
INTO. Point me at it and it is a two-minute move.

---

# LEVELS REORGANISATION — 0801h

    manifest 6836 -> 6690 keys · 0 broken paths · verify 91 passed / 0 failed
    reversible: _quarantine/lv0801h/_ledger.json

    scenery/          84 quarantined   0 directly referenced
    endpieces/         5 quarantined
    race level        33 quarantined
    nl6c clouds       48 -> assets/fx/weather   (the level-6 sky background stayed put)

## Per-level folders

    assets/levels/level1   54    lvl1_master + dam, mapJungle, terrain, stack
    assets/levels/level2    2
    assets/levels/level3    2
    assets/levels/level4   11
    assets/levels/level5    3
    assets/levels/level6    5    including its sky background
    assets/levels/level7    2
    assets/levels/level8    1
    assets/levels/runways   6    nst4b and nst7 run/app/exit plates
    assets/levels/transitions 15  the 13 transition flats + the ncon connectors

`assets/graphics/` is gone — transition-flats was all it held, and it now sits with the runways
under levels, which is where the transition work actually reaches for it.

## A trap worth recording

Moving files broke 31 manifest paths, and 2 of them were the SHARED-FILE case this project has
hit before: two keys pointing at the same PNG, so moving it updated one key and orphaned the
other. `ncon_3_4` and `ncon_4_5` both pointed at the same plate.

Repaired by re-indexing every real file by basename and repointing. The other 29 had no file
anywhere in the tree — pre-existing dead entries (stage fonts, map fonts) that the move surfaced
rather than caused. Dropped them.

**0 broken paths now**, which is the first time that has been true this session.

---

# THREE DAMAGE STATES — 0801i

    170 sprites quarantined (4.6 MB) · manifest 6690 -> 6520
    all 12 bosses still composite to their master at diff 0
    0 states the code can request are missing
    reversible: _quarantine/st0801i/_ledger.json

Mike: *"intact/critical/destroyed should be fine."*

Dropped `damaged` (and its `_dam` equivalent on the older sectional units). 129 sprites per state
across 12 bosses, and at the size a boss part actually occupies on screen, `damaged` and
`critical` were the same silhouette with different scorch.

**The threshold moved rather than the ladder shortening at the top.** Critical now opens at 0.7,
where damaged used to:

    before   destroyed <=0    critical <0.34    damaged <0.7    intact
    after    destroyed <=0    critical <0.7                     intact

So a part still visibly changes at exactly the same point in its health. The fight reads the same
way; it just stops at three rungs instead of four. Changed in all four places that assigned it,
including `SX_STATES` for the sectional units.

## On levels 2 and 3

Mike: *"I know the level 2 and 3 boss are anchored pieces and remain unique bosses but both share
the same characteristics."*

Right, and they already share everything they can without sharing art. Both run `mechInit` ->
`genesisInit`, the same 8-component layout, the same chain-haul entrance, the same limb HP model,
the same cannon aim sweep. The ONLY thing they do not share is the pixels — mbg2 is magma, mbg3 is
cryo, and those are genuinely different sprites.

That is why they are 289 keys each and why neither can be deduped against the other. What they
share is code, and they already share all of it.
