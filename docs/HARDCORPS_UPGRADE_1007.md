# October 7 — Contra-inspired encounter and engine upgrade

Mike requested Stage4 boss/terrain, Stage5 and6 minibosses, Stage6 Rebels/blue ace, Herald, every final encounter and copied form, chromium spell art, warnings and engine repairs.

## Encounter changes

| Encounter | New behavior |
|---|---|
| Stage4 Sovereign | Gun relay and a destructible-emitter four-way rotating cross. Beams dissolve into real crossing intervals. Existing energy-core destruction/revival remains authoritative. |
| Stage5 miniboss | Repositioning batteries, committed lances and a pulsed rotating cross. |
| Stage6 miniboss | Flak gates, strafes and warned lances. |
| Stage6 Rebels | Rookhook has separate winch, chain and open/closed clamp; committed launch, dodge/cut/roll escape, seat-owned reel and bounded edge throw. Nyx cloak/introduction/uncloak uses a helix above/below the hull with warned ambushes. |
| Stage6 blue ace | Alternating outward wing salvos with a center corridor and punishable recovery. |
| Stage8 Herald | Wing-owned eclipse cross; broken wing and beam disappear through an opaque physical ejection/blast, with immediate hazard cancellation. |
| Finale phase1 / mutated host | Mutation Spear: articulated arm strike. |
| Finale phase2 / ghost | Spectral Rail Relay: independently owned committed emitter attacks. |
| Phase3 home colossus | Crown Gate: articulated arm gate. |
| Copy0 / host | Chromium Pincer. |
| Copy1 / helicopter | Sonic Broadside horizontal pass. |
| Copy2 / Furnace | Furnace Bellows. |
| Copy3 / Cryo | Staggered Cryo Shutters with relay crossing gaps. |
| Copy4 / Sovereign | Rotating Storm Scissors with dissipation intervals. |
| Copy5 / Knight | Shield bait and sword riposte, using actual authored poses and hand-mounted weapons. |
| Copy6 / Harrier | Turbine Press. |
| Copy7 / Warden | Claw Vault. |
| Copy8 / Code Hammer | Raised-hand chromium rift spell, interruptible by destroying its targetable Hammer. |

The added final-boss signatures run between the original donor controllers' moves. The donor pauses during a signature and recovery; its saved damage, destroyed modules, emergency behavior and nine HP pools remain intact.

## Chromium rift

Eight generated whole-body cast cells share measured reactor, hand and hammer-head anchors. The free hand lifts above the helmet before release. A **2.6s warning** commits the rift to a fixed world position; its edge corridors remain outside the pull. Pull strength grows toward the center. The slowest pilot can escape with ordinary movement on Easy, Normal, Hard and Furious.

The active rift lasts5.6–6.2s. Alternating chromium lightning forks have .90s warnings, short active beats and harmless fading intervals. Damage and visuals use the same owned geometry. Somersault, roll and Decker dash escape; each co-op seat is evaluated separately. Breaking the Hammer, clearing the encounter, switching forms or losing the owner cancels the spell. Recovery is1.2s with no pull. The original Hammer controller resumes afterwards.

The black void and symbiote coil now have16 frames each with simulation-timed intermediate blending. Blending applies to energy only. The new `finale_transform_1007.js` renders opaque combat pieces twisting apart and assembling in sequence. The speech uses the exact combat torso/arms through `j3Body`, retaining dialogue, portraits, voice cues and ending ownership.

## Terrain and engine

Stage4 uses a generated1024×1536 lost desert airbase with abandoned hangars, radar, fuel tanks, wrecks, aprons and looping roads. Native adjacent seam rows match exactly. Scenery remains in world coordinates; original map progression and ground anchoring stay intact, with continuous highway pursuit.

The engine fixes timestep-dependent hostile rounds, fast-round tunneling and wrong-seat co-op collision queries. Authored projectile reels retain their animation; static rounds use simulation clocks. Bullet warnings prioritize actual incoming threats, stay bounded, deduplicate per emitter and support constant-width laser lanes.

Chaingun mounting now repairs stale death/reset state and incomplete cache readiness; barrel/muzzle clocks belong to each seat's simulation. Actual weapon-pickup cycles were verified for all nine pilots. The intermittent reported disappearance was not reproducible with a warm cache; the specific stale/reset/cache defects were repaired.

Rebel and blue-ace death sequences use the pilot's `DS_DUR`, `DS_CRASH` and540–900degree spin envelope, with anchored fire, crash and explosion. Opaque pieces no longer fade prematurely. Arena architecture uses fixed world anchors so it stops following the player horizontally.

## Verification and integration

- Full regression: **7,681 passed,0 failed**, final success banner and exit0.
- Current integrated native reports: **563 checks passed**, zero page/console/missing-art errors. Includes real damage controls, module cancellation, independent co-op behavior, pause stability, ordinary slow-pilot input and exact terrain seams.
- Evidence: `docs/qa/hardcorps_upgrade_1007.json`; native review `_shots/hardcorps_upgrade_1007/review.html`.
- These are controlled playtests, not a claim of an unassisted campaign clear or final human difficulty balance.

New script order after `finale_ai_1006.js`: engine, encounter bosses, lost airbase, Rebel air, final patterns, final art, final Hammer/effects, transformations. Corresponding regressions are appended after the existing finale AI test. `game.js` remains LF; `test_fl.js` remains CRLF.

Exact generated sources, prompts and hashes are under `_ART_SOURCES/hardcorps_1007`; owner builder is `_BUILD_SOURCE/build_hardcorps_finale_1007.py`. The40 final-boss production cells total5,751,522bytes. No shared atlas repack, deleted source recovery data, commit or publication in this pass.

## Immediate play routes

Use the existing Password menu: `BOSS4`, `MINI5`, `MINI6`, `REBEL6`, `HARR6`, `MINI8`, `FINAL1`, `FINAL2`, `FINAL3`; copies `HOST8`, `HELI8`, `FURN8`, `CRYO8`, `STORM8`, `KNIGHT`, `ACE8`, `WARD8`, `HAMR8`. These use the ordinary difficulty/pilot selection and existing encounter launcher.
