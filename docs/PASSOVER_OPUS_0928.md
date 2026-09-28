# Bullets of Fury — major passover for Opus

**Date:** September 28, 2026. **Owner:** Mike / ColeForge. **Purpose:** continue from the verified September 27–28 repair build without losing Mike's designs or repeating finished work.

Read this before older passovers. Read `AGENTS.md` and the opening engine cautions in `CLAUDE.md` as well. The September 13 handoff and many older checklist statuses describe historical builds. Their failure counts and Stage 6 assignments are not the current baseline.

## Current source and delivery

- This batch starts from main `4ad8549de9e49cbef2d4b10ccce638ba7081c500` and includes the complete local repair change set, generated runtime art, generation provenance, probes, regression coverage and playable-build tooling. Mike explicitly requested this upload and passover.
- Mike's active local checkout is `C:/Users/Mike/Desktop/Github Coding/BulletsOfFury`. The verified repair workspace is `C:/Users/Mike/Documents/New project/bof-repair-0927`. Their gameplay files were compared by SHA-256 before this upload. Use `git log -1` and `git status` to establish the actual incoming revision on another machine.
- The Overdrive expansion already lives separately under `expansion/`. HotWire/Phoenix references in dialogue are story hooks, not integration of the expansion into the base game. Do not merge it into base gameplay or the playable ZIP.
- Local playable archive: `C:/Users/Mike/Documents/New project/release_0927/BulletsOfFury-playable-2026-09-27.zip`. The historical filename remains, but the archive contains the September 28 repairs. Size: **499,012,361 bytes**. The adjacent build report and committed QA snapshot record its checksum.
- `_shots/`, local backups and the playable ZIP are intentionally excluded from Git. Small native screenshots and portable QA evidence are committed under `docs/proofs/opus_passover_0928/` and `docs/qa/opus_passover_0928.json`. Regenerate larger captures with the supplied probes.

## Latest verified baseline

The mandatory full suite reached `==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====` on September 28: **5,576 passing assertions**. The portable QA snapshot records the assertion count. Do not carry forward the September 13/18/22 failure counts as if they still apply.

`node --check assets/game.js`, addon syntax checks, and `git -c core.whitespace=cr-at-eol diff --check` passed. Native Chromium probes ran against both source and the compressed release. These are controlled encounter checks, often using immunity and explicitly selected attack states. They do **not** establish a full unassisted campaign victory, physical-controller compatibility, subjective balance, or a speaker-level audio audition.

Native release captures: [Harrier combat](proofs/opus_passover_0928/harrier-combat.png), [centered escape portal](proofs/opus_passover_0928/toxic-portal-open.png), [mutated Stage 8 vessel](proofs/opus_passover_0928/alien-first-form.png).

## What is implemented in this batch

| Area | Current implementation and evidence |
| --- | --- |
| Single and multi Retina | Holding C retains one selected target while missiles repeat or are tapped. Y is the separate rebindable multi-lock, acquiring visible targetable units one at a time. The old C-driven multi-scan must not return. Native controls checks cover single-target retention and four-target/four-round volleys. |
| Stage 1 | Patrol boats fire spreads from live turret muzzles, without the extra horizontal hull volley. Sonic-wave windup uses FOV/asterisk warnings and audio. Preserve the existing helicopter choreography and module explosions. |
| Stage 2/3 | Upgraded dangerous attacks have shared FOV tells. Magma cannon cadence increases by difficulty. Laser-eye collision uses separate eye lanes, leaving the gap safe. Stage 3 uses large visible ice balls and distinct boss/miniboss attack families. |
| Stage 4 | A modular-jet flash path had an extra Canvas restore. The repaired renderer keeps the context stack balanced. A native 45-second combat probe covered eight kills and three affected jet types without screen jumps. Encounter scrolling resumes through a ramp. Destroyed miniboss gun routines switch to rockets; rocket speeds and helpers scale by difficulty. |
| Space death and Shadow Orb | Real death removes Akimbo, resets Volley Missiles to base level 1 and equips Laser Cannon level 0. Shield absorption does not do that. Shadow Orb has a charge percentage/meter, ready marker and its own charge/release samples. |
| Stage 5 / HAMMER | Furious gets a second full Chromium armor layer, activation animation, protected healing checkpoints, critical front hammer twirl, interruptible restoration and red rage jumps. HAMMER uses the same mechanics and supports continues. The soundtrack cue no longer resets an unfinished activation. |
| Healing counter | A selected hammer can be hit by guided missiles through the body-wall phase. Guided/volley missiles retain the selected target while taking a flank route around the wall. A hammer hit cancels healing, reverses the HP actually granted and stuns the boss. Front-facing body rockets remain blocked. Native regular/password tests cover ordinary and critical healing, body flank hits, volley core damage and activation across the cue. |
| Stage 6 opening | The live sky continues through fly-in; HUD fades in without the old teleport jump. Dialogue leads into rapid lock alerts, a Retina descends onto the pilot, fighters uncloak and pass north, and upward-launched missiles curve back toward the player. Interceptions use real explosion/debris effects. |
| Harrier launch and route | Bay jets launch forward/north, scale up and roll out. The post-miniboss Harrier crosses left and five rebels cross right. A paused/dimmed route choice precedes banking and the chosen fight. Dialogue includes HotWire/Phoenix and a rebel parley. Rebels have individual overhead bars and independently hittable modules. |
| Stage 6 Harrier combat | `warhive` is the actual Harrier boss. Hull, engines and bay are selectable/damageable; the carrier bar tracks synchronized pools. Boss music starts. The latest native probe dealt exactly 120 HP, exposed four Retina targets, and handed off to the separately scaled Ace. |
| Stage 6 miniboss | Current assignment is **Eclipse Siege Bomber (`siegebomber`)**, not Tempest Brothers. Its pools receive a 42% reduction after all shared floors/multipliers. Native solo Furious total: 6,521 HP. Blacksteel remains the alternate. |
| Arrows and shields | Stage 6 incoming/above-unit arrows and Stage 5/6 miniboss directional arrows are suppressed. FOV and warning sounds remain. Enemy shield silhouettes fit their hulls instead of drawing oversized bubbles. |
| Stage X | Surviving rebels unlock individual central-core encounters; defeating them during Stage 6 prevents those side quests. The corrected title asset is a transparent framed stage plaque, not the rejected poster. Terrain has transparent water channels over an independently animated ocean reel. |
| Stage 7 enemies/vents | The clipped lamprey has a new complete sprite. Vent hardware holds a fixed frame while only the toxin stream animates. Toxic ordnance no longer reuses a construction barricade plate. |
| Stage 7 escape | The boss stays ground-anchored while the sewer/camera advances. Existing explosion reels are palette-swapped green; repeated blasts use explosion samples, not a repeating scream. A generated corridor cap removes the baked ground portal and extends the sewer. A centered vortex holds its open frame, the pilot enters, then it contracts/dissipates; toxic blasts fill the screen before fade/stats. |
| Stage 8 | Mike clarified that the **mutated alien vessel belongs to Stage 8's first boss form**, not Stage 6. The realm scrolls, its authored music plays, portal entry releases controls, and the alien family fires binary bolts, bursting data bombs and dark matter with committed tells. The new first vessel has cannon/core targets and binary attack patterns. Later forms retain their existing designs. |
| Shared terrain | Cached atlas canvases have `height` rather than reliable `naturalHeight`. `levelScrollRange()` now uses that height, fixing zero-range scrolling/encounter stalls. |
| Campaign unlock | Cole4u stays active for the open game session through death, new runs and old-save loads. Saved campaign data can preserve the unlock; a fresh process without a saved unlock starts locked. |
| Audio/package | Stage 2/3 minibosses have separate formerly unused tracks. Stage 8 uses `stage8_furious_death.mp3`. The Windows loopback launcher supports range requests and avoids silent `file://` WebAudio playback. Source PNG/audio files are preserved. |

## Where the implementation lives

`assets/game.js` remains the main engine. The late repair hooks in `assets/furious_review_0927.js` intentionally wrap the existing owners. `index.html` loads this addon after the combat, modular-roster, Stage 7, and HAMMER scripts, before the widescreen HUD and online scripts. Reordering it can silently reinstate older behavior.

| File | Responsibility |
| --- | --- |
| `assets/game.js` | Shared collision, Retina, spawning/HP floors, carrier hull pools, scroll range, explosions, vent composition, base controls and core engine. |
| `assets/furious_review_0927.js` | Dedicated Y scan, Furious armor/healing counters, missile flanks, route pause/rebels, Stage X, toxic escape, alien entry/AI/ordnance/first form, late renderer overrides. |
| `assets/encounters_0926.js` | Encounter patterns, difficulty movement and upgraded boss/miniboss attack routing. |
| `assets/combat_polish_0927b.js` | Missile lanes, bombing, Siege Bomber timing and directional-arrow suppression. |
| `assets/modular_roster_0927.js` | Current authored enemy/part ownership and bomber setup. |
| `assets/hammer_time_0927.js` | Password encounter, sound-cue locking and continues. |
| `assets/stage7_modular_0927.js` | Warden/tank module state and original fight renderer; escape delegates through the late addon. |
| `assets/vile_finale_0924.js` | Existing alien form construction/takeover/later phases; its entry now reveals the new first vessel plate. |
| `assets/rival_fight_0924.js` | Rival encounter ownership/persistence used by the newer Stage 6/Stage X hooks. |

Generated runtime art is in `assets/game/furious_review_0927/` (eight plates/sheets), `assets/game/stage6_fleet_0927/` (two south-facing hulls), and `assets/game/stage678_repair_0928/` (sewer connector, complete lamprey, mutated vessel). Preserve each generation manifest. The fleet source/import script is under `_BUILD_SOURCE/stage6_fleet_0927/`.

## Next work for Opus — prioritized, with acceptance criteria

These are **pending validation/polish**, not claims that every listed feature is currently broken. Reproduce before changing values, and retain the approved behavior above.

### Priority 0: sustained gameplay and regression traps

1. **Play a complete Furious campaign naturally**, plus targeted Normal/Hard runs. Start from a fresh profile, earn equipment normally, continue after death, finish levels and reload saves. Record actual input footage with game audio. Most probes jump directly to encounter states; that leaves wave-to-boss scheduling and long-session pacing less well exercised. Record pilot, difficulty, weapon levels, element, missile tier, timestamp and exact reproduction for each issue.
2. **Stage 6 density and fairness.** Test the opening with no premature enemy waves; verify allies remain near the player's lower formation and obey maneuver cooldowns. Check offscreen enemies do not shoot unreadable/upward attacks. Re-test both routes from actual miniboss completion, the 30-second decision, uninterrupted sky outside the explicit choice pause, and route banking. Acceptance: the player can read warning lanes, target exposed aircraft, replenish supplies and survive with skill without permanent lock/audio spam.
3. **Harrier/Ace damage and pacing.** Test guns, beams, orbs, single Retina, Y volleys and special abilities on every live module and hull, then the real carrier-to-Ace handoff. Check HP bar/music ownership on normal entry and debugging paths. Re-measure the reduced Stage 6 miniboss with naturally earned loadouts; the older bomber damage-window measurements predate this reduction. Avoid simply raising all HP again.
4. **Hammer full-fight counters.** Verify ordinary Stage 5 and HAMMER on Hard/Furious through activation, half armor, underlying 75/50/35/15% checkpoints, twirl, critical stun, rage jumps and continues. Test manual missiles, passive volley and direct weapons against the healing hammer. Acceptance: a correctly selected counter interrupts recovery; the body wall still deflects frontal fire; damage and health-bar layers stay honest. Preserve `ht27CombatSequence` and the flank route rather than bypassing the shield globally.
5. **Stage 7 → stats → Stage 8 continuity.** Play the entire escape at ordinary render cadence, then advance stats/rewards in Campaign and Arcade. Check the boss's ground anchor, explosion timing/audio, pilot-following camera, sewer joins, full dialogue readability, center portal entry, closure and black fade. Ensure reward/autosave happens once and the new stage has music, movement and firing. The latest native entry test moved 105 pixels and fired six shots; it is not a full transition playthrough with every pilot.
6. **Stage 8 subsequent forms.** This pass only redesigns the first mutated vessel. Review/build the later forms as a coherent alien progression rather than silently retaining mixed visual language forever. Test first-form cannon destruction, core hits, data-bomb warning/burst windows, each morph and eventual clear. Preserve the nonfightable takeover robot and Mike's approved blue shield/sword where those assets are used. Do not mistake the first shell for the whole completed boss.
7. **Stage 4 long-session stability.** Repeat heavy fights with hit flashes, missiles, pickups, helpers, deaths and camera release on every difficulty. Assert balanced Canvas save/restore and inspect actual pixels. Never use a zoom/camera workaround to conceal a renderer stack leak. Verify destroyed helper/turret targets do not intercept shots invisibly.

### Priority 1: weapon completeness, UI, audio and authored frames

8. **Weapon/element matrix.** Reconcile actual gameplay, icon, projectile, unlock announcement, preview and loadout entry for all nine weapon types × nine elements × levels 1–5. Earlier work found 405 tier icons on disk and tested broad level-1 previews; that is not proof of all 405 combat behaviors. Reuse existing art and `assets/data/FORGE_TEMPLATES_0916.json` before generating duplicates. Fire Whip is already implemented: ship-anchored alternating sweep with shared render/hit curve and +25% laser damage. Verify it naturally, along with Magma Orb impact shards, Ice Lance tap/delay, Dark Void absorption/collapse, Eradicator, Chromium immobilization/shrapnel, Prism splitting and cast-stream variants. Never replace every orb with the same behavior.
9. **Rewards/loadout budgets.** Natural boss defeat must grant one element license and two upgrades, not one usable upgrade. Exercise A to select a main weapon, left/right base variant, up/down element and A to equip; controller paging and RE-SPEC must be usable. Preserve crafted forms after switching to bare weapons and campaign save/load. The current element map is Stage 1 kinetic/Sonic, 2 fire, 3 ice, 4 lightning, 5 chrome, 6 dark, 7 toxic, 8 prism, **9 water**. Some older docs have a different order; do not copy it back.
10. **Pilot-specific progression.** Test Freezer's Stage 2 Ice Breath default/lock, subsequent Flamethrower choice, orb choice and Stage 3 Thermoshock default. Test Maverick's exclusive homing-laser/regular beam selection and bounded homing lifetime/damage at higher tiers. Test Yuri's post-Stage-4 blue lightning upgrade, tap/charge Thunder Storm, ship charging, sky strikes and dimmed background. Verify actual elemental +50% / −50% messages agree with damage; do not infer from a catalog label.
11. **UI timing and fit.** Mike repeatedly reported slow stats. Measure the complete debrief on low and high frame rates, check independent label/bar reveals and sounds, rank/full-image layout, skip/confirm behavior, Fury conversion and notices. Re-test full campaign-map scaling, top bar plus connected clock, nine horizontal bottom-left stage boxes, centered right-panel text and the portrait fitting its box without a name/dossier label. Verify Armory is separate from Achievements, free/unlock-only, and has honest locked icons/categories. These older requests have implementations; refresh current evidence before rebuilding the UI.
12. **Physical pad and saves.** Test Mike's actual 8BitDo wireless pad after relaunch, rebind/apply and another relaunch; synthetic Gamepad API checks are not hardware proof. Test 24 manual slots plus one autosave, fresh-pilot campaign isolation, death/reload semantics, Cole session unlock and two-player independence.
13. **Audio audition.** Listen to real output for enemy guns/boats, warnings, missiles, tank movement, Harrier/mechanical thrust, firewall/geyser hazards, explosions, every forged attack and boss music handoffs. Counted calls and decoded files do not establish audible output or a pleasant mix. Test the localhost launcher, first user gesture and cold audio pools. Do not route `file://` media through a WebAudio filter that outputs silence. Avoid fixing missing effects by globally replacing muzzle flashes or removing retrigger gates.
14. **Direction/frame audit.** The new Stage 6 hull replacements are idle art, not a newly generated complete maneuver library. Review exact roll/pitch/bank frames for every remaining jet/tank/rebel, consistent anchors and south-facing idle orientation. Generate missing poses against approved source art, with enough transparent margin and reviewed cell boundaries. Do not invent aerobatics by squashing or arbitrarily rotating a hull without the required frames. Modular turret pivots remain appropriate when their art is authored for them.
15. **Stage 1–3 fairness and Stage 9 weapons.** Revisit furious warning/projectile contrast, sonic horizontal/vertical wave variants and escape gaps, helicopter barrage/safe lanes, large ice-ball readability and the laser-eye gap. Test Stage 5/9 single locks and rockets on distant modules/objects after target destruction. Preserve real stage ecology and avoid enemy pop-in from late sprite loading.

### Priority 2: older backlog, only after reconciliation

`docs/REQUEST_CHECKLIST_0914.md` still contains partial/pending entries for warning-family coverage, full vehicle frame audits, campaign cinematics, hazard readability, Stage 2 death/head sequences, Stage 3 Hard behavior, Stage 4 optional Dark Chromium helper attacks, no-continue trophy art, and playable Boss Rush/Time Attack. Treat it as a source of requests, not a current certification list. Several items now have later implementations. Inspect owners and newest native evidence, update statuses, then complete only real omissions.

Cockpit portraits should face the pilot from inside the canopy, with **one central joystick**, including relaxed/not-gripping poses where useful. Reuse the approved nine-pilot portrait pack rather than generating redundant avatars. Preserve authored terrain, stage-card family, bitmap fonts, rectangular shield fill wells and standard modular explosion/debris deaths. The older `ANIMATION_NEEDS.md` favors some runtime rotations; Mike's later pose/frame corrections take precedence where a vehicle turn looks wrong.

## Reproduce verification

Run from the repository root:

```powershell
node --check assets/game.js
node --check assets/furious_review_0927.js
node _BUILD_SOURCE/test_fl.js
git -c core.whitespace=cr-at-eol diff --check

python _BUILD_SOURCE/probe_controls_fleet_0927.py
python _BUILD_SOURCE/probe_furious_0927.py
python _BUILD_SOURCE/probe_hammer_repair_0928.py
python _BUILD_SOURCE/probe_stage678_repair_0928.py
python _BUILD_SOURCE/probe_stage6_opening_0927.py
python _BUILD_SOURCE/probe_stagex_water_0928.py
python _BUILD_SOURCE/probe_boss_warnings_0927.py
python _BUILD_SOURCE/probe_cole_session_0927.py
python _BUILD_SOURCE/probe_space_boats_0927.py
```

Use the focused probe corresponding to the change; do not run every old probe blindly. Some historical probes encode retired encounters. Python probes use Playwright/Chromium and `_BUILD_SOURCE/shoot.py`. If required art is absent in a sparse checkout, restore that named dependency before interpreting a missing-file failure as a gameplay regression. The full suite needs `_ART_SOURCES/stage1_ai_fx/spaced_v2`.

For the release:

```powershell
python _BUILD_SOURCE/collect_release_0927.py
python _BUILD_SOURCE/build_playable_0927.py
python _BUILD_SOURCE/probe_stage678_repair_0928.py ../release_0927/BulletsOfFury
python _BUILD_SOURCE/probe_hammer_repair_0928.py ../release_0927/BulletsOfFury
```

Output is relative to the checkout's parent. Keep the base ZIP at or below **500,000,000 bytes**, not 500 MiB. Current headroom is only **987,639 bytes**. New art/audio requires a new size audit. Scenery uses high-quality WebP at original size; combat sprites/projectiles/icons/fonts remain lossless where the builder specifies it. `.png` URL rewriting happens only in the release copy. Collect runtime registries after all nine stage setups; otherwise space-ship parts and late registrations can disappear from the package. Check ZIP CRC, runtime-script equivalence and native compressed-build rendering.

## Working rules that prevent repeat regressions

- One writer at a time for `assets/game.js`; keep its LF and `test_fl.js`'s CRLF.
- Identify the live owner before editing. The boss seen as Harrier is `warhive`; Stage 6's miniboss is `siegebomber`; the new vessel is Stage 8 `vileexistence` form 0. Retired Tempest/Chaos Harrier docs are not assignment authority.
- Shared HP floors must scale every private pool and the public gauge together. A native hit should remove the number shown by the bar. Apply the Stage 6 reduction after the floors, not before.
- Touch lazy art, wait for decoding, then inspect it. `XART.get` can return a canvas without a stable identity or `.src`. Wrap the game's own `ctx.drawImage` if measuring draw calls; prototype traps can miss it.
- A completed green suite proves state, not pixels or survival. Record the assertion count and final banner. Preserve meaningful tests instead of changing their expectations merely to obtain green.
- Do not restore arrow spam to satisfy a blanket warning rule. Preserve the current FOV/Retina/audio tells and their safe lanes.
- Portal frame 7 is dissipating residue. Hold an open mid-reel frame, then play the closing tail; do not hold the last frame as the portal.
- Preserve source art, existing saves, expansion separation and protected trailer work. Keep secret keys and signed service URLs out of Git and logs.

## Supporting repair notes

- `docs/REPAIR_0927_RELEASE.md`: initial repair/download/package, boats, space death/Shadow Orb, Cole session, warnings and stealth fly-in.
- `docs/FURIOUS_REPAIR_0927.md`: the large full-game Furious request and focused verification limits.
- `docs/HAMMER_REPAIR_0928.md`: activation cue and healing missile counter.
- `docs/STAGE_X_CARD_0928.md` and `docs/STAGE_X_WATER_0928.md`: approved replacement card and layered ocean.
- `docs/STAGE_678_REPAIR_0928.md`: latest Harrier/miniboss/vent/escape/alien pass.
- `docs/GAMEPLAY_REPAIRS_0926.md` and `docs/REPAIR_PASS_0922_FLIGHT_BOSSES_ARSENAL.md`: earlier weapon, flight and encounter implementations; their old suite failures are historical.

The next useful deliverable is a short, reproducible list from real sustained play, with footage and measured fixes. Continue Mike's approved systems; do not spend another generation pass recreating assets that already ship.
