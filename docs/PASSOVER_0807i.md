# PASSOVER — drop 0807i   (THE FX PACK IS IN)

Build: `BulletsOfFury_0807i`
Harness: **2,130 assertions / 195 sections / 0 failing**, twice, reaching the banner.
Full verification: **PASS — 9,591 cells resolve, 0 blanks across 20 screens and 8 stages.**

---

## 1. SEVEN SMOKE SETS INSTALLED, 56 FRAMES

`ColeForge_Smoke_Dust_FX_Vol1` shipped as **individual frames**, not a packed sheet — which is
exactly why none of it has nx_smoke's cross-frame bleed. Measured colour depth on install:

    nsd_fog     ground_fog_creep     3661 colours
    nsd_chim    smoke_chimney_loop   3625     a rising column, anchored, and it LOOPS
    nsd_ring    smoke_ring_vortex    3539
    nsd_diss    smoke_dissipate      3537     a puff that thins out
    nsd_steam   steam_vent_burst     2454
    nsd_dust    dust_landing_puff    1222
    nsd_devil   dust_devil_spin        54

Against `ntr_smkH`'s 275 and the bled `nx_smoke`'s 37. All seven clean at every edge. Packed into
one sheet (`nca_78`, 2112x1614) and bucketed `common`, so it does not bloat a single stage.

Prefix checked for collisions before naming — `nsd_` was clear.

## 2. THE DAMAGE STATES, FINISHED

    above 65%     nothing
    65% -> 35%    nsd_diss    1 vent   a puff that dissipates — light, transient damage
    35% -> 15%    nsd_chim    2 vents  a chimney column. It LOOPS, so it reads as ONGOING
                                       rather than as an event that already happened
    below 15%     nxp_upward  2 vents  the fire plume at the vent,
                  + nsd_chim           with the column rising off it

The looping matters more than it sounds: a dissipating puff says *something just happened*, a
looping column says *this thing is still broken*. That is the difference between an effect and a
state, and the state is what Mike asked for.

`SMOKE_FAM` now points at `nsd_chim`, so every other smoke in the game — the Magma Colossus
damage smoke, the explosion smoke, the sx marker — upgraded to 3625 colours in the same edit.
`nx_smoke` is referenced nowhere.

## 3. WHAT IS LEFT IN THE PACK

Four sets are installed but unused, and all four have an obvious home when you want them:

    nsd_dust    dust_landing_puff    a ground unit landing / a tank tread kicking up
    nsd_fog     ground_fog_creep     stage ambience, low and drifting
    nsd_steam   steam_vent_burst     a pipe or vent set-piece
    nsd_ring    smoke_ring_vortex    a heavy cannon muzzle ring

## 4. STILL OPEN FROM THE PLAYTHROUGH

Eight: stats screen · dialogue box art · liftoff music · L2 miniboss routing into lava · the tank
on the mountain · the runway plate · retiring the beach water · L2/L3 boss assembly spacing.
