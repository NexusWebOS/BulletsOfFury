# DOOMSDAY CARRIER Mk II — the six-phase fight, as Mike specified it

Mike, 0905, verbatim:

> the first phase is the shield up, missiles. second phase is shield down, turrets going off, laser
> beam taps, charged strong large laser fire off's. phase 3 is shield up again, 1 or both bays down.
> phase 4 is shield down again, spread fire turret fire, laser beams more rapid, charged laser beam
> fire off's. phase 5 is turrets destroyed, phase 6 is he fires off laser beams FAST and constantly
> slides and we have to dodge the laser beams and shoot to destroy him. then it dies.

---

## ⚠ THE DRIVER IS THE CHANGE, NOT THE CONTENT

The fight today has **four** phases and they are chosen by HEALTH:

    phase = ratio>.75 ? 0 : ratio>.50 ? 1 : ratio>.25 ? 2 : 3
    CARRIER_MEGA_PHASE = ['BAY SIEGE','STORM CAGE','GRAVITY PRISM','DOOMSDAY FUSION']

Mike's six are **event-driven**. "Shield down" happens because the player broke it. "1 or both bays
down" and "turrets destroyed" are things the player ACHIEVES, not health bands the boss passes
through. Read as HP thresholds the fight would advance whether or not you did the work, and phases
3 and 5 would be lies — the shield could be up with both bays intact and the game would still call
it phase 3.

So the phase becomes a small state machine over the subsystems that already exist, and health is at
most a floor under it.

## Everything it needs is already built

| the spec says | the system that already exists |
|---|---|
| shield up / down | `b._bayShield` — `{up, hp, max, window, breakT}`, `CARRIER_SHIELD_HP`, and a `CARRIER_SHIELD_WINDOW` of 30s before it comes back |
| missiles | the bay warhead mechanic — `_carrierWarhead`, `carrierWarheadDraw`, the deflect at 27326 |
| bays down | `b._bay = {L, R}` at `CARRIER_BAY_HP` each, damaged ONLY by deflected warheads (Mike's own rule) |
| turrets | `b._mega.nodes` — FOUR destructible weakpoints (L1, L2, R2, R1), hp 18, `n.dead` |
| laser beam taps / charged fire-offs | the PRISM LANCE (0905j) — `S9_BEAM.doomsdaycarriermk2`, head/tile/cap, charge → burn → retract |
| sliding | `carrierMegaTick` already drives `b.x`; phase 6 needs a continuous slide rather than a step |

Nothing here needs new art. What is missing is the **sequencing**, plus two behaviours: a spread
turret pattern for phase 4 and a continuous slide for phase 6.

## The six, as states

1. **SHIELD UP — MISSILES.** Shield up, bays intact. Launches warheads; the player deflects them.
   Ordinary fire sparks off (`s6mb_ricochetimpact`, 0905j) — which is what teaches the mechanic.
2. **SHIELD DOWN — TURRETS + LASER TAPS.** Entered when the shield breaks. Turret nodes fire, the
   prism lance runs SHORT taps, and occasionally a long charged burn.
3. **SHIELD UP — BAYS FALLING.** Entered when one or both bays die. Shield returns; the pressure is
   that the player has already opened part of the boss.
4. **SHIELD DOWN AGAIN — SPREAD + RAPID.** Turret fire becomes a spread, lance taps come faster,
   charged burns still punctuate.
5. **TURRETS DESTROYED.** Entered when all four nodes are dead.
6. **THE RUN.** Lance fires FAST and continuously while the carrier slides across the field. Dodge
   and kill. Then it dies.

## ⚠ Traps to respect while building this

- **`M.phase` is recomputed from HP EVERY TICK.** Any state machine must OWN that variable, or the
  next tick overwrites it. This already cost a probe a wrong result in 0905j.
- **The bays are Mike's own mechanic and are immune to ordinary fire** (CLAUDE.md, twice). Phase 3
  must not become reachable by shooting the hull.
- **NO BOSS SPLITS** (CLAUDE.md, ruled twice). Turrets and bays are destructible sub-targets he
  authored, not the boss coming apart — do not let "phase 5: turrets destroyed" grow into pieces
  falling off.
- **`carrierThunderheadTick` and the launch/cannon reels early-return out of the fire dispatcher.**
  A phase change during either must not be swallowed.
- Phase transitions already flash, shake and `floatText` the phase name; six entries are needed in
  `CARRIER_MEGA_PHASE`, not four.
