# BOF boss review and Normal completion — October 31, 2026

The strongest immediate improvement was to Event Horizon. Its continuous spin and white level-4 core lasers remain, but its health no longer receives an excessive stack of stage/adaptive multipliers. The long uninterrupted lasers now fire in short, warned bursts with real movement gaps. Hard and Furious now ask for different dodges, rather than presenting nearly the same fight with different health.

Normal now concludes after the actual Stage 5 Chronos defeat. The game saves the clear immediately, retains the existing results and Forge rewards, flies the selected pilot back to Earth and Fury HQ, then offers Hard or Furious. Both choices explain the changes and fade to pilot selection for a fresh Stage 1 operation. Furious is identified as the intended experience and the route to the true ending.

## Changes installed

### Event Horizon — Stage 9 miniboss

| Item | Previous behavior | Current behavior |
|---|---|---|
| Solo health | Audit spawn: Hard 7,857 / Furious 9,287. Earlier powered-loadout film: 10,965. | Hard **3,520** / Furious **4,160**, one consistent visible/core pool. |
| Health modifiers | Stage ramp, pressure and encounter floor could stack on the single pool. | Explicit final-spawn budget; native co-op ×1.5 and NG+ ×1.25 apply once. |
| Spin | Shared hull/optic/beam rotation at 0.60 revolutions/s. | Preserved continuously through charge, fire, recovery and travel. |
| Spiral | Two continuous arms for 4.7s. | Hard: 3 × 0.20s pulses, 0.68s gaps. Furious: 4 × 0.22s pulses, 0.52s gaps. |
| Beam/sweep | Long continuously rotating rays. | Hard: 2 pulses; Furious: 3 pulses. Warning and core recharge appear between pulses. |
| Orbs | Three shots on both ranks. | Hard: 3 at 220px/s; Furious: 5 at 250px/s. |
| Radial fire | Dense repeated rings without a deliberate escape sector. | 12/16 candidate lanes, a committed open sector, slower Hard cadence. Ordinary rounds remain unshootable. |
| Half-health | Native exact 50% gate, water material, smoke and UFO dashes. | Preserved; a large hit cannot skip the phase. |
| Dash warning | Corridor appeared only during the final edge charge. | Committed corridor appears from the initial charge, allowing time to relocate. |
| Re-entry | Return path could be damaged while still offscreen; next attack began immediately on arrival. | Protected return followed by a visible foreground recovery. |
| Hit feedback | Sustained fire could continually refresh the solid white body. | Actual hit flash, 65ms with a separate 160ms retrigger gate; damage continues normally. |
| Audio | Sustained laser voice followed the whole fire state. | Sustain follows actual live beams; individual pulse/charge/orb/boost cues remain audible. |

The old lasers were not mathematically impossible. A conservative movement test found a route, but the old spiral squeezed reachable positions down to 306 cells at its tightest sample. The revised Furious spiral retained at least 8,540 cells in that test. This measures room to maneuver, not human success rate. The model used the slowest unupgraded ship (143.52px/s), a 3px grid, 10px beam clearance, three native beam samples per 50ms, and no roll or somersault. It excludes regular bullets, input latency and subsequent re-aiming. Hard and Furious are not ranked by that one cell-count metric; Furious has an extra pulse, extra orb shots, a heavier radial volley and more dash decisions.

### Carrier and Nightwing — Stage 6 boss

The carrier's ten modules, passive fans, hull dependency, burning exposed hull and destruction remain unchanged. A suspicious health mismatch immediately after spawn was a transient: the existing setup reconciles the pools correctly before combat. No repair to those pools was needed.

Only the following Nightwing life was shortened: **3,960 HP on Hard / 4,680 on Furious**, with native co-op and NG+ modifiers retained. The audit's old Furious ace pool was about 5,810 HP. The old full recording lasted 220.57s and spent substantial time in travel/turning windows. The new native recording lasts 104.05s through defeat and fly-off. This is an observed comparison, not a controlled claim that the health reduction alone halved the fight: targeting, pickups and route timing vary between recordings.

Its teal identity, direction-matched turns, shadow, thrusters, dual turret fire, committed targeting, wind charge and dash rings are retained. The right place to add future difficulty is a more demanding committed attack choice, not restoring another large HP multiplier.

### Tidal Sovereign — Stage 9 boss

Furious keeps the current water arsenal. Hard now has smaller spreads and fewer simultaneous landings:

| Attack | Hard | Furious |
|---|---:|---:|
| Forward water spread | 3 lanes per turret, slower cadence | 5 lanes per turret |
| Mortars per turn | 3 | 4 |
| Falling fan geysers per rain turn | 4 | 6 |
| Lamp bubbles per turn | 6 | 10 |
| Non-wall charge | Existing tell +0.25s | Existing tell |
| Minimum recovery | 1.65s | 1.15s |

The native three water-wall alerts, wave art, wave sounds and full warning duration are identical on both ranks. Grenades still launch from fans and explode; forward spread still comes from the forward turrets. Re-entry after Slip N Slide is protected until he reaches the foreground. His native health remains 5,500 Hard / 6,500 Furious in the audit fixture.

## Normal's new finish

1. A real Normal Chronos defeat writes a verified completion autosave immediately, including the earned chaingun, current pilot/loadout, Forge ledger and score. Completed co-op saves also retain the second pilot and score.
2. Existing score tally, co-op bonuses and Forge choices finish before the new return flight. Tally bonuses are settled once.
3. The selected aircraft flies toward Earth and arrives at Fury HQ. A second active player is retained, and both players reselect their pilots in the native player-one/player-two order.
4. An avatar-free, native-size menu displays: “You may have won the battle, but you didn't win the war. Only the strongest will make it to the end, Commander. Do you have what it takes?”
5. Hard explains higher health budgets, faster fire, denser waves and Hard boss patterns, with 3 lives / 3 continues. Furious explains its upgraded patterns, intended experience, 3 lives / 1 continue and true-ending route.
6. Confirm fades to pilot select with that difficulty and the original campaign/arcade mode. The subsequent operation starts fresh at Stage 1; NG+ is not accidentally inherited.

Normal cannot continue into campaign Stages 6–8. Existing optional Stage 9 detour saves from before the Stage 5 clear are preserved. Old Normal saves already in campaign Stages 6–8 return to the new choice. Normal NG+ also respects the Stage 5 finish.

The completion has an independent archive so a fresh operation cannot erase it. When the regular auto slot is empty, the load screen can recover this archived completion. Loading it reopens the difficulty choice instead of replaying Chronos or launching Stage 6. A storage failure displays a failure message and blocks restart until the save succeeds. Debug recordings and the menu preview never write completion data.

All 451 return/menu/fade frames are even-sized authored cells, with 13 editable Aseprite banks. The flight uses the actual nine pilot aircraft, existing Earth/HQ art and the approved menu-only frame. New effects do not use live sprite rotation, resizing or alpha animation.

## Remaining encounters: findings and next decisions

The review combines current controller/health inspection, fresh native Event Horizon and carrier/Nightwing fights, focused Tidal tests, and the latest available recordings for the other late encounters. It is not a new human survival clear of every boss. Initial HP samples below are not necessarily the total damage required across armor refills, components or separate lives; older films can also carry higher adaptive-pressure budgets.

| Encounter | What is working | What may still feel below standard | Recommended next pass |
|---|---|---|---|
| Chronos, Stage 5 | Difficulty-specific hammer combo, armor/rage identity, separate gun form. | Multiple refills/transitions make one displayed HP number misleading. Full suite still flags older opening-jump/chromium expectations. | Replay the current opening and each refill without GOD; compare tell, hit window and rage damage separately before changing health. Keep Normal/Hard/Furious swing counts. |
| Fortress, Stage 6 mini | Six laser batteries + passive fans gate the reactor; no allies. Existing film 82.33s. | All parts must stay reachable by the basic gun after a player death; bright reactor lightning can obscure small rounds. | Test every individual part with minimum weapon level and no Retina missiles. Preserve the all-parts gate and laser-only front batteries. |
| Carrier/Nightwing | Modular carrier now leads to a shorter ace life. New film 104.05s. | Flight invulnerability and repeated wind turns can still dominate a low-damage run. | Measure the percentage of time actually hittable, then change recovery frequency before increasing HP. |
| Rough Riders | Five different roles, original Gasline, Nyx's Retina cloak gate, Decker's reflection sequence and distinct flight patterns. Existing film 165.85s. | Five simultaneous threats, retinas, dialogue and friendly fire can exceed what the player can read. Raw 8,600 combined Furious HP is not the only difficulty driver. | Give one rider ownership of the heavy attack while the others reposition/light-fire. Preserve spacing, warning anchors and Nyx visibility rules. Test with shield sequence and with no missiles. |
| Sumpjaw pair, Stage 7 mini on Furious | Independent gill/heart pools and overhead bars; staggered heavy attacks. 2,232 combined native HP; film 74.04s. | Screen-edge landings and the surviving creature's visibility are the practical fairness risks. | Keep one heavy attack at a time; verify all four gills after death/respawn with the basic weapon. Hard retains Dredger, making Furious meaningfully different. |
| Warden, Stage 7 boss | Canisters protect the core, live barrels draw in front, final core spins/hops and scatters toxic shots. Sample 6,150 Furious HP; film 133.09s. | If a canister or turret becomes hard to hit, the required-parts gate turns into dead time. Hops plus lingering toxic scatter can close a landing exit. | Measure component exposure and keep a full movement corridor at each landing. Increase challenge with aimed swats, not more protected hull HP. |
| Herald of Death, Stage 8 mini | Red identity, deliberate six-slice storm ritual, shootable skulls, missile depth returns and one-pass glass. Sample 3,616 Furious HP; latest ritual film 148.77s. | Long invulnerable ritual/desperation intervals and bright hit flashes can dominate the encounter. Extra shards would rapidly make it unfair. | Preserve the requested paced ritual; restrict overlapping heavy attacks, test glass lifetime and verify the 15–20% transition cannot stall a low-missile run. No new HP increase. |
| Dracodia, Stage 8 boss | Separate arm budgets, complete body/ball transition, gated portals, articulated claws, copied arenas and terminal sequence. | Many owners and copied lives make accumulated phase time and stale full-fight recordings a larger risk than raw HP. An old complete movie does not prove the current full run. | Record a fresh uninterrupted run on each intended rank and log per-life active/recovery/background time. No new Dracodia attacks, art or difficulty variants were activated in this pass. |
| Event Horizon, Stage 9 mini | Now has explicit health, real laser gaps, rank-specific patterns and readable re-entry. New film 70.32s. | Burst prediction, horizontal-dash coverage and fights with no speed upgrades still need human testing. | Start weekend testing here, with basic speed and without relying on GOD or constant roll invulnerability. |
| Tidal Sovereign, Stage 9 boss | Coherent water sockets, fan mortars, three-wall warnings and deliberate second half. Distinct Hard counts now verified. | Large lamp bubbles and late geysers can narrow the path after the visible attack ends. Existing film 147.84s. | Check maximum simultaneous bubble/ground hazards; preserve finite cleanup and a clear route after each wall. |

### Difficulty strategy

**Normal, Stages 1–5:** teach each mechanic clearly, one main threat at a time, readable tells and recoveries. Stop at Chronos with the new save/choice. There is no need to maintain a separate full Normal campaign ending.

**Hard:** retain the boss's identity and required modular targets; introduce stronger pattern choices with fewer concurrent hazards and longer recovery. Health should buy enough time to learn an attack book, not add several repeats after the player has solved it.

**Furious:** add deliberate decisions—alternating attack direction, the approved four-hit hammer sequence, Sumpjaw pair, extra committed pulses/volleys and meaningful phase transitions. Do not shorten necessary warning reactions just because fire cadence increases. Keep an escape route for the slowest unupgraded pilot. Prefer one heavy-pattern owner at a time over several unavoidable aimed attacks.

Working playtest targets, not automatic rules: roughly 60–100s per miniboss and 90–150s per single full boss with an appropriate late-game weapon. Squadron and multi-life finales can exceed that, but their extra time must contain new decisions rather than protected travel or repeat loops. Compare time-to-defeat together with foreground uptime and minimum-loadout damage; a raw HP table alone will mislead us.

### Dracodia proposals — approval still required

These are design suggestions only. His current attacks, art, arm dependencies, copied-life repairs and final-death rules remain intact.

| Form | Hard direction | Furious direction |
|---|---|---|
| Drone/first host | Committed claw rake, then eye fan, with a clear recovery. | Alternate rakes and optical rotations; avoid stacking an aimed beam on the only open claw exit. |
| Final demon | Teach rake → double jump slash and the ground-mine Luminaire separately. | Alternate the combos and Luminaire in a less predictable order, with the northern escape preserved. |
| Corrupted Chronos | Keep the approved two downward strikes and clear throw release. | Keep the approved two downward strikes plus two sideways strikes; rage changes pressure, never the hammer design. |
| Helicopter | Committed twin gun lanes, then a separately warned pod volley. | Alternate pods and movement to change the dodge while keeping a genuine gap between gun lanes. |
| Brain | Fewer geysers with a clear escape flank; eye attack is readable. | More committed geyser decisions between eye casts, without a full-field beam/geyser overlap. |
| Phoenix | Four readable corner passes and a clear return window. | Shuffled corners and the approved 8–12 Order of the Phoenix echoes, with one committed target per echo. |

## Verification and limits

- **33 focused native checks passed** for Event Horizon, Normal's defeat/results/save/reload, both choices, fresh pilot selection, campaign/arcade, Normal NG+, bonus compatibility and desktop/mobile text fit.
- **12 later-balance native checks passed** for carrier pools, both Nightwing budgets, Tidal attack counts, protected re-entry, three full wall alerts and actual fresh Hard start.
- Native movement diagnostics found surviving paths for both old examples and all three revised examples. They support the increased maneuvering room; they are not a no-hit certification.
- Fresh full native films reached actual defeat for Event Horizon and carrier/Nightwing using native GOD and input-only aiming. No enemy health, phase or timer was changed during filming. The Normal film is explicitly a staged preview of the real flight/menu/fade and writes no completion save.
- New films decode fully and contain audible audio. Headless recording performance includes capture/host overhead; these are not a 60fps production certification. Expected `ERR_ABORTED` audio preloads during stage/music switches were retained in the reports; no HTTP missing-asset responses or browser/draw errors occurred.
- Syntax checks pass. Core `assets/game.js` remains byte-for-byte unchanged: `024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de`.
- The full repository suite still exits nonzero with the **same five baseline failures**: minimum flash hold; Chronos dialogue/opening jump; jump-to-chromium ordering; unchosen Stage X route persistence; Stage X right-branch launch. No additional failures were introduced. These are reported, not marked green or silently bypassed.
- The six pending Stage 6/9 concept pairs are still concepts. No unapproved alternative was put into the game. No GitHub upload was requested or performed during this pass.

Reproduction: `_BUILD_SOURCE/test_boss_balance_1031.py`, `_BUILD_SOURCE/test_later_boss_balance_1031.py`, `_BUILD_SOURCE/audit_boss_dodges_1031.py`; authored return/menu rebuild: `_BUILD_SOURCE/build_normal_finale_1031.py`. Raw checks, health samples, movement counts, media audits and full-suite log are retained with this review.
