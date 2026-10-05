# October 3j — three encounters and Dracula's eight forms

The eight-form controller had replaced the three outer finale encounters. It reused `_r30.form` for both encounter identity and combat shape, so the ghost and Dracula encounters were bypassed. Mike explicitly corrected that sequence and the Stage 6 rebel/dialogue behavior.

## Authoritative runtime

`assets/finale_structure_1003j.js` loads after `combat_1003i.js`. `_r30.finale1003j.encounter` owns outer progression; `mimic` owns Dracula's current copied shape. Earlier 1003b/c historical test chapters describe intermediate builds, not the current campaign structure.

1. Normal drone flies in, followed by the visible mutation. The first actual fight is the articulated mutated drone, with orbiting/gravity pressure and claws. Furious HP: 4,100.
2. Defeating it destroys that body and reconstructs the ghost. The ghost has a separate 4,715 HP on Furious, teleporting claw cycles, code rain and bombs. It does not transform into the other bosses. Its single whole specter plate has one visible damage pool, without invisible arm health.
3. Defeating the ghost reveals the approved Dracula/Vile Colossus body and separate arms. Its one authored health-bar housing fills eight times in eight colors. Dracula uses arms/tentacles between the eight transformations. Each transformation completes its attack book before returning; depleted lives are skipped. Only exhausting all eight lives starts the final destruction, portal, reunion and single campaign reward.

Each copied life retains its actual HP and independent broken modules across switches. Weapons, shields, locks, hit flashes and emitters use the existing modular rig. The bar reads the current pool exactly. Phase music advances on the three outer encounters only; switching copied shapes does not restart or advance the boss score.

| Furious copied life | HP | Signature behavior |
| --- | ---: | --- |
| Orbital Host | 4,100 | Independently sweeping claws, gravity, code cannons |
| Hive Helicopter | 2,378 | Strafing alternating gun bursts, bomb runs, homing salvos, gravity |
| Alien Furnace | 3,365 | Five-shot molten fans, advancing firewalls with escape gaps, beam and orbit attacks |
| Cryo Hive | 4,680 | Rime-style open gates, four-cannon relay, bursting ice siege, advancing glacier pressure, gravity |
| Storm Organism | 5,720 | Missile batteries, independently aimed lightning barrel, committed ram and code guns |
| Null Knight | 6,150 | Modular powered blade, shield, teleports, chained leaps/slashes/sweeps and landing orbitals |
| Void Harrier | 5,836 | Turbine pull and fan volleys, spread missile salvos, carrier lance, gravity |
| Last Warden | 6,150 | Toxic suppression, leap/impact, actual claw pincer, portal volley, gravity and rail/code attack |

HP was checked after the source bosses initialized their runtime controllers, not just immediately after spawn. Warden's initialized modular pool differs greatly from its initial constructor HP. Knight has a deliberate single-life budget of 1.5 Host lives, rather than importing Hammer's entire armor/refill budget. Budgets for all five difficulties are explicit in the runtime.

## Stage 6

Rebel hull hits now go to the complete ship, without wing-slice damage caps, missing rectangular sections or stale wing locks. Every ordinary, roll and measured pitch frame is drawn whole, with a separate additive hit flash. Complete-hull Retina targets remain. All initial, formation and last-stand shields are disabled. Existing squad maneuvers, authored portraits and Stage X music remain.

Critical dialogue runs the existing world update. Steering, backgrounds, allied movement, effects and audio advance; scheduled waves wait. Player combat remains locked, hostile projectiles/ground hazards are suppressed, and invulnerability remains. Confirm/Start during a protected line cannot pause the world or dismiss its text. The original timed reading sequence remains. Cole's authored weapon demonstration completes and restores the previous loadout; the route choice and rebel combat release naturally afterward.

## Verification

- `node --check assets/game.js` and the new runtime: passed.
- `node _BUILD_SOURCE/test_fl.js`: **6,993 passes**, exit 0, final success banner reached. The first attempted run failed in the newly added test wrapper due to variable shadowing; it was corrected before the successful complete rerun.
- Native Chromium via `shoot.py`: **106 passing checks**, zero page/console errors: 86 encounter/rig/HP/live-radio checks, 15 complete dialogue/ship checks, 5 review/launcher checks.
- Natural drone → mutation → ghost → Dracula progression; natural traversal of all eight transformations; real projectile damage against every rig; persistent damaged modules/HP; no early reward; one final portal/reunion reward.
- Full timed Yuri and Cole conversations, Callisto demo and loadout restoration, natural rebel introduction/combat release, complete damaged frames and absent last-stand shields.
- Screenshots rendered through the game's own context and XART were inspected for each outer encounter, every modular form, four damaged pitch poses and readable live dialogue. The first visual pass caught Confirm opening Pause and hiding the dialogue; the final pass blocks that path and verifies PLAY state throughout the protected sequence.
- Local review: `_shots/finale_structure_1003j/review.html`; four launch buttons tested. Evidence: `docs/qa/finale_structure_1003j.json`.

These are controlled runtime/visual checks, not a human campaign clear or a final balance rating. No art was regenerated or atlas changed. Existing authored art, original warnings and generated combat audio remain. All earlier local work was preserved; no commit or push.
