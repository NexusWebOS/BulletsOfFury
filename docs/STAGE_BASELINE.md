# STAGE BASELINE — where every level stands before the pattern pass

    drop 0801ag · verify 235 passed / 0 failed

## Level art: replaced, all nine stages

The Stacked Level Art Pack is in. Sections stacked bottom-to-top per the handoff ("the game
scrolls upward, so sections connect bottom to top in the numbered order shown"), so section 01 is
the bottom of the stage and 04 the top.

| stage | new master | was | sections |
|---|---|---|---|
| 1 Rumble in the Jungle | 800x4800 | 800x3616 | 6 |
| 2 It's Hot in Here | 800x3663 | **480**x2693 | 4 |
| 3 Ice Still Can't See | 800x3400 | **480**x2693 | 4 |
| 4 Crouching Missiles | 800x3200 | **480**x2693 | 4 |
| 5 All for One | 800x3286 | **480**x2693 | 4 |
| 6 Heavy Turbulence | 800x3918 | **480**x2693 | 4 |
| 7 Not Another Sewer Level | 800x4062 | 800x3616 | 4 |
| 8 Furious Death | 800x3601 | **none** | 4 |
| 9 Bonus Stage | 800x3721 | **none** | 4 |

**This is the real fix for the hall of mirrors.** Six stages were 480 wide against an 800 world.
Stages 8 and 9 had no master at all.

Two handoff rules honoured rather than flattened away:

- **Upper layers stay separate** on 5 stages — canopy, rooftops, overpasses, signs. The handoff
  asks for it twice, and it is expensive to separate again once baked.
- **Magenta is keyed, not kept.** "Pure #FF00FF marks animated liquid or an intentionally
  replaceable keyed area." Keyed by FLOOD FILL from the borders rather than a colour sweep — a
  sweep would punch holes anywhere the dense 16-bit terrain uses a warm highlight. 101k px keyed
  on stage 1, 224k on stage 2, 169k on stage 3, 125k on stage 4.

Old masters backed up to `_quarantine/masters0801ag`.

**One thing the pack does not carry:** stage 7's sewage is not magenta in the source sections
(0 pure-magenta px across all four), though the handoff says it should be. Its liquid will not
animate until that art arrives keyed.

## Enemy waves: the current baseline

| stage | waves | wave builders in use | distinct enemy types |
|---|---|---|---|
| 1 | 29 | vRow x3 | 20 |
| 2 | 22 | *none — all hand-placed* | 14 |
| 3 | 28 | Columns, Rush, Sweep, vRow x12 | 16 |
| 4 | 33 | Columns, Cross x2, Loop, LoopCurve | 29 |
| 5 | 13 | Sweep, vRow x3 | 7 |
| 6 | 44 | Rush x2, Split, Sweep x2, vRow x3 | 17 |
| 7 | **18** | *none* | **6** |
| 8 | **4** | *none* | **3** |

The AI pattern library from your hand-drawn sheets survived every cull and is intact:
`aiWaveRush` (sheet 1), `aiWaveSplit` (sheet 2), `aiWaveSweep` (pattern #1), `aiWaveColumns`,
`aiWaveCross`, `aiWaveLoop`, `aiWaveLoopCurve`, plus `aiAttach`/`aiTick` and the sequenced
`aiDelay`/`aiQueueTick` staggering.

**Where the gaps are, plainly:**

- **Stage 8 has 4 waves and 3 enemy types.** It is the finale and it is nearly empty.
- **Stage 7 has 18 waves, 6 types, and no pattern builders at all** — everything is hand-placed.
- **Stage 2 has 22 waves and no builders either**, despite having 14 types available.
- Stage 5 is thin at 13 waves / 7 types.
- Stages 4 and 6 are the most developed and are the model to work from.

## Ready for the stage-by-stage pass

Send the pattern drawings whenever. For each stage I can give you the wave-by-wave timeline
(spawn time, builder, enemy, count, direction) so you can see exactly what is there before
deciding what changes.
