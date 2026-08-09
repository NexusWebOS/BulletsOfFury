# PASSOVER — drop 0808h   (THE _t VARIANTS ARE GONE)

Build: `BulletsOfFury_0808h`
Harness: **2,261 assertions / 207 sections / 0 failing — three runs, identical.**

---

## 1. ONE THRUSTER SYSTEM, EVERYWHERE

Mike: *"in cinematics, gameplay, stage intros, we always use these with the thrusters. no more
static graphics with the thrusters built in."* Then: *"those are the thruster variants. remove
those. were not using them anymore."*

All nine `ship_<pilot>_t` cells removed. **162 ship cells -> 153.** Every pilot keeps sixteen
frames plus the plain one — `_l`, `_r`, `_nf`, `_pv0-4`, `_br0-7` — and the flame is drawn live
from `nthp_` on the measured mounts.

Every caller moved over:

    drawShipSprite   REFUSES '_t' whatever it is passed, draws plain hull + live thruster
    the launch       was suf='_t' — now the plain hull
    the intro        was drawShipSprite(...,'_t') — now plain
    the bank/roll    two fallbacks to '_t' when the plain frame was missing — both closed
    the RIVAL        the last one, drawing '_t' whenever level. Now on the same thruster
                     the player uses; he flies the same airframes, he should burn the same way.

## 2. WHY THEY HAD TO GO, MEASURED

`_t` is not the same aircraft:

    axel  98 -> 259  (+161px)    decker +57    maverick +54    lizzie +44    yuri +20

The flame is part of the sprite, so drawing a `_t` to a target HEIGHT shrinks the airframe by
however much flame is attached. That is why the ship changed size between play and the cinematic,
and why no mount table could ever line up against it — the hull it was aligning to was a
different size in every scene.

## 3. ⚠ THE HARNESS HAD IT BACKWARDS, IN WRITING

One assertion read:

    // ALL NINE PILOTS have a flameless airframe to overlay onto
    if(!XART.rdy('ship_'+pk+'_t')) ...

**It called `_t` the FLAMELESS one.** It is the exact opposite — `_t` is the flame-baked variant
and the plain `ship_<pilot>` is flameless. So the suite was requiring the baked-in art to exist,
under a comment claiming the reverse. That is a large part of why both systems survived side by
side for so long: the tests were defending the wrong one.

Inverted — the plain hull must exist, and `_t` must NOT.

## 4. ⚠ AND I BROKE SHIP RENDERING BEFORE GETTING THERE

Removing the cells, I also repacked the ship atlas to reclaim the 0.43 Mpx and wrote it out as a
standalone PNG — while leaving it registered in `BOFX.cells`, which routes through the packed-sheet
mechanism with a sheet id that does not exist. **Every ship went unresolved: 21 failures.**

Reverted the repack, kept the removal. The nine cells' pixels are still in the sheet, unreferenced
and costing 0.43 Mpx — a trade I will take over a broken airframe. Repacking that sheet is its own
job.

## 5. AND THE PACK LANDED

`CF_BOFFinalArtSources-Vol_2.zip`: rosters for stages 1-8, 30 boss sheets, 45 player-weapon files
with manifests, and VFX. **`Stage01-roster-source.png` is the stage 1 art I reported as missing** —
1254x1254, a 4x4 grid of 313px cells, magenta-keyed: four tanks, four boats, four aircraft
including a tilt-rotor, and four props.

That is what `racer`, `intcp` and `topgun` should be drawing.

## 6. NEXT

Cut the stage 1 roster off that sheet, register it, wire the three air roles to real art — then
build the waves on units that exist.
