# Encounter passwords — October 5

Enter these in the normal Password menu, then choose your difficulty and pilot.
Encounter codes skip the regular stage waves while keeping the fight's introduction.
All codes fit the six-character input. Existing stage and Stage X codes still work.

| Stage | Main boss | Miniboss | Alternate encounter |
| --- | --- | --- | --- |
| 1 | `BOSS1` | `MINI1` | — |
| 2 | `BOSS2` | `MINI2` | — |
| 3 | `BOSS3` | `MINI3` | `ALT3` — Rime Wall |
| 4 | `BOSS4` | `MINI4` | — |
| 5 | `BOSS5` | `MINI5` | `HAMMER`, `HAMA` — musical Hammer fights |
| 6 | `BOSS6` / `HARR6` — Harrier | `MINI6` | `ALT6` — Blacksteel; `REBEL6` — five Rebels |
| 7 | `BOSS7` | `MINI7` | — |
| 8 | `BOSS8` — full finale | `MINI8` — Herald of Death | `ALT8` — existing Herald alternate slot |
| 9 | `BOSS9` | `MINI9` | — |

The finale has three separate outer encounters. Transformation copies belong to
the third encounter only. Phase entry codes keep their cinematics.

| Finale encounter | Password |
| --- | --- |
| Mutated drone, including drone arrival/mutation | `FINAL1` |
| Ghost, including new spectral introduction | `FINAL2` |
| Dracula / giant symbiote, including void introduction and eight-color fill | `FINAL3` |

These additional practice codes start a specific copy inside the third encounter.
The other copies retain their own health pools, as in the normal fight.

| Copy | Password |
| --- | --- |
| Mutated drone | `HOST8` |
| Helicopter | `HELI8` |
| Furnace | `FURN8` |
| Cryo | `CRYO8` |
| Storm | `STORM8` |
| Sword/shield knight | `KNIGHT` |
| Ace | `ACE8` |
| Warden | `WARD8` |

The original thirteen routes remain available:

| Destination | Password |
| --- | --- |
| Stage 1 | `FURY` |
| Stage 2 | `IRON` |
| Stage 3 | `DAM5` |
| Stage 4 | `STRM` |
| Stage 5 | `ORBT` |
| Stage 6 | `TURB` |
| Stage 7 | `SEWR` |
| Stage 8 | `DETH` |
| Stage 9 | `RIFT9` |
| Stage X Harrier, mountain/coast arena | `XHARR` |
| Stage X Rebels, mountain/coast arena | `XREBEL` |
| Stage 6 direct Harrier | `HARR6` |
| Stage 6 direct Rebels | `REBEL6` |

Stage 6 encounter routes include the player plus four allies. The normal stage
passwords still start the regular mission. Shortcuts are consumed once and cleared
on cancellation, so they cannot leak into the next ordinary run.

Registration: `assets/overnight_routes_1005.js`. Keyboard and native deployment
evidence: `_BUILD_SOURCE/probe_overnight_review_1005.py`; all 32 new encounter
destinations also exercised through the actual `startRun` path in
`_BUILD_SOURCE/probe_overnight_1005.py`.
