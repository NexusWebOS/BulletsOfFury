# PASSOVER — drop 0807h   (PER-CLASS EXPLOSION SETS, AND ONE SMOKE REEL TO RULE THEM)

Build: `BulletsOfFury_0807h`
Harness: **2,130 assertions / 195 sections / 0 failing**, twice, reaching the banner.

---

## 1. THE CLASS SETS WERE ALREADY DEFINED — EXCEPT THE BOSS

Mike: *"tanks get there own sets, the jets/planes of the enemies get there own set, minibosses
get there own set, and bosses get a combination of the explosions, as well its own originating
one, i believe we had this defined but if not, we can now."*

Checked before changing anything. It WAS defined, and correctly:

    tank    nxp_smoke   + nxp_radial
    jet     nxp_white   + nxp_barrage
    mini    nxp_dense   + nxp_barrage
    boss    nxp_ring    + nxp_smoke

Three of the four were right. **The boss was the one that was not** — it ran two families like
everything else, where the spec asks for the whole set. It now opens with its own originating
blast (`nxp_ring`) and the chain behind it walks the combination:

    tank    1 family in the chain     stays on its own set
    jet     1 family                  stays on its own set
    mini    2 families
    boss    7 families                barrage, clus, radial, ring, white, smoke, dense

Asserted, including that a tank does NOT borrow the boss combination — a big death should be
distinguishable from a routine one.

## 2. ⚠ I DISABLED THE BLED SMOKE AND DELETED A FEATURE DOING IT

`nx_smoke` is bled — every frame carries fragments of its neighbours, from being sliced off a
packed sheet on the wrong grid. I looked for the master to re-cut it: **it is not on disk.**

So my first move was a flag that switched the reel off everywhere. **An assertion immediately
failed: the Magma Colossus uses those frames for its damage smoke** — authored puffs that appear
only once it is hurt — and switching the reel off silently removed that.

Retiring bad art must not mean losing what the art was doing. Every smoke site in the game now
resolves through a single `SMOKE_FAM`, pointed at `ntr_smkH` — 275 colours against nx_smoke's 37,
and the best-shaded smoke that exists in this project. `nx_smoke` is referenced nowhere.

**When the FX-Packs smoke lands, point SMOKE_FAM at it and every smoke in the game upgrades in
one edit.** Six assertions were pinning the literal `'nx_smoke_0'`; they resolve through the
variable now, so the suite cannot freeze the game to the broken reel.

## 3. WHAT I STILL NEED FROM YOU

* **A shaded smoke reel from the FX-Packs chat** — or the master sheet `nx_smoke` was cut from,
  so I can re-slice it on the right grid. This is the last piece of the damage states; there is
  no well-shaded smoke anywhere in the project and I cannot author one.

## 4. STILL OPEN FROM THE PLAYTHROUGH

Eight: stats screen · dialogue box art · liftoff music · L2 miniboss routing into lava · the tank
on the mountain · the runway plate · retiring the beach water · L2/L3 boss assembly spacing.
