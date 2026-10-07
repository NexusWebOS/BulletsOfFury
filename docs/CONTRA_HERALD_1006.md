# Contra study transferred to Herald — October 6

The existing Stage 8 Herald miniboss now staggers its skull cannons, preserves each arm's full warning, and removes an arm's active shots when that arm breaks. This is the first production transfer from the complete visual study of all 35 numbered encounters in [Shadowserg's Contra: Hard Corps run](https://www.youtube.com/watch?v=iooQeqdyB8E). It uses Herald's already approved six authored components. The four original bosses / eleven forms in the study lab remain candidates.

## Source lessons and resulting play

The closest reference is encounter 27, Cyborg Bros: recognize separate suspended cannon owners, read the source of each shot, and reassess space as hardware is destroyed. Blade (02) and Takedda (25) reinforce that the visible surviving assembly should explain the next threat. Living Warhead (35) supplies rupture/collapse punctuation. These are design transfers; Herald retains its own anatomy, red ordnance, wing lances and skull weak point.

During a skull cycle the boss commits to the captured player position. Move away from that aim, read the two fan edges, and continue moving through the second arm's delayed release. The lead arm alternates on successive skull cycles. Destroying an arm erases its pending warning and already released shots immediately; the other arm's fan remains live. Removing both guns adds 0.45 seconds to the subsequent rest, giving a longer opportunity to damage the remaining head/core.

| Difficulty | Full warning per cannon | Second release delay | Bullets per cannon |
| --- | ---: | ---: | ---: |
| Easy | 1.50 s | 0.36 s | 3 |
| Normal | 1.22 s | 0.32 s | 3 |
| Hard | 1.08 s | 0.28 s | 5 |
| Furious | 0.96 s | 0.24 s | 7 |

These are BOF values, not measurements from Contra. Warning lines show each fan's centre and outer edges; the second warning remains visible after the first release. All bullets in a fan share the same nozzle snapshot before recoil. Density and existing bullet speeds remain unchanged. A long update processes crossed release slots once. Cleanup uses encounter and part ownership, leaving other owners' shots intact. Death clears dangerous emissions before cosmetic destruction.

## Authored effects

`hc1006_signature` registers the unchanged 1448×1086 generated reel, four columns by three rows of 362-pixel cells. Only two four-frame clips are used: blue/white joint discharge at the broken attachment (0.65 s, 74-pixel draw), and warm casing breach at fatal core damage (1 s, 190-pixel draw). They never deal damage and never loop. Existing authored muzzle charge/flash marks each release; existing explosions and detached components finish the death cascade. The joint arc is visibly distinct. The breach shares space with the existing explosions and reads as part of their combined destruction.

The contact/dust row is retained unused. The earlier pressure-ring reel with one-pixel padding remains a lab candidate. Source pixels, prompt and measured alpha metadata are archived under `_ART_SOURCES/contra_fx_1006/`; `_BUILD_SOURCE/build_contra_fx_1006.py --write` copies the source exactly and emits the native manifest. Running the builder without arguments verifies the source/deployed hashes and manifest. The art taxonomy records its cosmetic role. No shared atlas was repacked.

## Verification and review

The baseline full suite passed 7,407 assertions. The final suite passed 7,445, including 38 added checks for staggered release, complete warnings, nozzle snapshots, alternating lead side, owner cleanup, longer disarmed recovery, catch-up and packaged art. Exit 0 and the final FALVA/LIZZIE success banner were confirmed. Game and Herald syntax checks pass.

The native Chromium probe passes all 41 checks with zero page/console errors. It verifies the real halfway scheduler on all four difficulties, separate release beats, disarm, native effect draws, six component renders, original FOV/Retina, real missile/gun damage, wing removal, weak point, destruction and resumed stage/finale progression. Audio cue dispatch is checked in muted captures.

Eight fixtures use real keyboard movement from both extreme edges on all difficulties, with Juggernaut's actual minimum base speed 2.392, no shield, no invulnerability, no roll/somersault/special and real damage active. Each escapes one skull cycle without a contact. A stationary Furious control is hit and dies. Support fire is cleared for these focused fixtures; arbitrary starts, co-op routes and complete encounter balance still require play review. Other capture fixtures protect the pilot for inspection and are not unassisted clears.

Open `_shots/contra_herald_1006/review.html` for actual native captures. Launch `index.html` and enter **MINI8** through the normal password menu to play. Portable results and final file hashes: `docs/qa/contra_herald_1006.json`. Reproduce with `node _BUILD_SOURCE/test_fl.js`, `python _BUILD_SOURCE/probe_contra_herald_1006.py`, and `python _BUILD_SOURCE/build_contra_fx_1006.py`.

Local only, uncommitted and not pushed. Existing Stage 8 finale, approved art, HP, rewards, stage trigger and earlier user work are preserved. See `_STAGING/contra_study_1005/BOSS_FIGHT_ATLAS.md` for the complete source study and `ENCOUNTER_KIT.md` for remaining designs.
