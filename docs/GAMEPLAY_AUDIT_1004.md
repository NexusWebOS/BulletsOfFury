# Gameplay repair pass — October 4, 2026

## Evidence and scope

Source: Mike's local `2026-10-04 00-46-51.mp4`, 61:29, 1280×720/30fps.
Initial review covers the entire recording through timestamped frames every two
seconds (1,845 frames, 77 contact sheets). This is a sampled visual review, not a
claim to have watched every frame or listened to the complete audio. Targeted
full-size/more frequent frames and live Chromium reproductions follow below.
The recording starts on the Stage 1 completion screen; Stage 1 combat is absent.
Contact sheets and incident captures live in ignored `_shots/gameplay_audit_1004/`.

## Observed timeline

| Video time | Observation / follow-up |
|---|---|
| 00:00 | Stage 1 complete; no Stage 1 fight in supplied recording. |
| 00:56–01:02 | Campaign reveal ends with a tiny/dark map; replace with island assembly and arrival zoom. |
| 01:50–03:22 | Stage 2 Reaver fights through modular destruction; many full-white hit silhouettes. |
| 03:50–06:52 | Furnace fight; shield flash and impact glare often obscure the boss. |
| 08:20–09:18 | Stage 3 miniboss has long exposed intervals with sparse attacks. |
| 09:50–10:56 | Stage 3 boss also has low sustained pressure; improve recognizable patterns. |
| 12:36–13:16 | Stage 4 miniboss: limited fan attacks and movement. |
| 13:50–16:48 | Stage 4 boss: shield stays up through sustained attacks; smaller gray form becomes near-continuous white silhouette; run ends in game over. Reproduce shield lifecycle. |
| 16:56–17:00 | Player bypasses Stage 4 with Stage 5 password. |
| 17:56–18:10 | Stage 5 mini dies quickly; check beam direction/placement. |
| 19:04–23:02 | Hammer fight: check emergency regeneration crossing, armor break and rage transition. |
| 23:04 | Abrupt switch to still cutscenes without requested modular in-engine death. |
| 23:28–24:04 | Earth occupies foreground; replace with return to in-engine aftermath and distant Earth flight. |
| 24:08–25:06 | Forge navigation, unexpected element availability and preview/selection mismatch; reproduce Up navigation. |
| 25:34, 27:06, 51:32 | Opening stealth fighters establish the approved source silhouette. |
| 25:46–26:14, 27:06–27:50, 51:46–52:30 | Bomber runs use the rejected different green/gold plane. Use red/green variants of opening stealth fighter. |
| 26:26, 51:08 | Explosions/pickup text leak from previous run into fresh Stage 6 intro. |
| 28:34–29:30 | Stage 6 Eclipse mini; many full-white hit silhouettes. |
| 29:56–30:54, 58:18–59:16 | Cole's protected dialogue: world scrolls but unrelated enemies and pickups remain visible. |
| 32:08–33:54 | Rebel fight. Gang Mode at 32:34; Decker rescue 32:48–33:24. Nine friendly ships instead of five. |
| 33:40–33:50 | Rebel deaths use small radio/quick explosion; need burning spin, crash and large shocked portrait fade. Preserve individual HP bars. |
| 34:56 | Stage 6 completion goes straight to Stage 7 instead of campaign map. |
| 35:40–36:08 | Stage 7 mini drops quickly under upgraded weapons; balance against normal entry loadouts too. |
| 37:24–39:52 | Stage 7 boss: opaque gas hides player/projectiles, frequent white hull flashing. |
| 40:48–42:18 | Stage 8 new enemies mostly ram or fire weak trickles and disappear quickly. |
| 41:20–41:48 | Herald miniboss: modest cones, quickly destroyed. |
| 42:22–43:10 | Mutated drone fight has code wall and intermittent attacks. |
| 43:12–44:52 | Ghost fight; art is hidden by full-white damage silhouette through most attacks. |
| 44:54–50:28 | Dracula/transform fight: base shape frequently white, imitation phases use very sparse common attacks; several only last ~10–20s. Actual donor boss patterns and sustained form state required. |
| 50:32–50:54 | Finale portal/ending, then returns to menu. |
| 51:00–54:50 | Stage 6 password replay with Lizzie; low weapon power creates a very different difficulty spike. |
| 55:00–59:18 | Maverick replay through Stage 6, then chooses Harrier. |
| 59:52–61:02 | Harrier platform fight, frequent white flashes and nine friendly ships. |
| 61:04–61:24 | Escaping elite switches between blue and gray/black art as it banks. |
| 61:26–61:29 | Recording ends at game over. |

## Requested implementation checklist

- [x] Fix Stage 4 boss shield/progression; verify defeat through ordinary weapon damage in a controlled fixture.
- [x] Fix forge Up navigation and earned-only combo availability.
- [x] Revamp fire and other orb damage, targeting and authored impact feedback.
- [x] Strengthen Stage 3 encounters and Stage 4 miniboss with readable patterns.
- [x] Hammer: guaranteed 8% failsafe to 38%, active armor/rage recovery.
- [x] Hammer: modular in-game death before cutscenes, in-engine Earth homecoming after.
- [x] Stage 6: approved red/green stealth bomber palette variants and consistent elite art.
- [x] Stage 6: five versus five, individual Rebel HP, cinematic death expressions/sequence.
- [x] Clear cross-run effects and unrelated objects during protected live dialogue.
- [x] Stage 6 completion returns to campaign map.
- [x] Stage 9 password; separate Stage X Harrier and Rebel passwords.
- [x] Stage 8 new enemies: ranged projectiles and signature specials.
- [x] Finale: donor-boss pattern reuse, upgraded mechanics, eight persistent form HP pools, Dracula base pressure.
- [x] Review SotN true-final Dracula gameplay reference.
- [x] Regenerate connected modular campaign islands and middle city; hover lift and arrival zoom.
- [x] Improve hit readability without hiding authored boss art.
- [x] Native Chromium checks, screenshots, console/page errors, full regression suite final summary.

## Implementation and validation

Runtime additions are `assets/gameplay_repair_1004.js` and
`assets/finale_donors_1004.js`, loaded after Rebel Gang. Supporting edits preserve
existing local work. No commit or push. Starting recorded baseline: 7,022 assertions.

### Combat and progression

- Stage 4 shield now overloads after 18 seconds and exposes the hull for eight
  seconds even with surviving generators. Breaking generators still opens it sooner.
  A native Furious fixture defeated it in 126 seconds using ordinary Level 3 MG
  rounds and the normal collision/damage path. This fixture auto-aims and grants
  player invulnerability; it proves progression, not human survival/balance.
- Stage 3 and Stage 4 batteries retain their authored patterns with shorter recovery,
  tighter Furious cadence and an active central battery after side guns break.
  Forty-five-second native samples: Frost Cruiser 140 projectiles / seven modes;
  Cryospear 213 / seven modes; Olive Warden 302 / six modes. Beams were also active.
- Hammer cannot be overkilled past the first 8% threshold. It recovers to 38% over
  three seconds, removes the interrupted Chromium barrier and resumes rage attacks.
  This reserve fires once. Ordinary interrupted recovery no longer leaves a long stun.
- The approved separate body/head/arm death plays for eight seconds in the game
  engine with electrical bursts, smoke rings and an explosion flash before the stills.
  After the monochrome sequence, the engine returns with fading explosions, a distant
  Earth, welcome dialogue and a shrinking ship flying toward the planet.
- Rebel battles keep five fixed HP readouts, four NPC allies plus the player, whole
  ship art, 720-degree burning deaths, crash explosions and queued large shocked
  portraits fading white. Victory waits for the last crash and portrait. Existing
  Gang Mode, personal abilities and the live Decker scene remain.
- Fresh blue ace keys bypass conflicting old atlas aliases, including modular
  damaged wings and bank/somersault frames. Stage 6 bombers use red/green palettes
  of the opening stealth fighter. No replacement bomber silhouette.
- Stage 6 completion opens the campaign map at Stage 7. Both Stage X routes use
  `LevelX.mp3`, confirmed through the actual playing audio element.

| Password | Destination |
|---|---|
| `RIFT9` | Stage 9 |
| `XHARR` | Stage X Harrier encounter |
| `XREBEL` | Stage X Rebel encounter |

### Finale and weapons

The outer sequence remains mutated drone → ghost → Dracula with eight persistent
form health pools. Borrowed attacks now execute actual campaign controllers:

| Alien form | Live donor controller |
|---|---|
| Helicopter | `updateOverlordX`: sweep, charge/re-entry, sonic combo, rockets |
| Furnace | `furnaceCombat`: arms, reactor and eye phases |
| Cryo | `er26Tick`: battery, relay, crossfire, glacier press |
| Storm | `er26Tick`: battery, escorts, lance, siege weapons |
| Knight | original `hammerBossTick`: leaps, chaining, guns, spells, rage; powered sword follows real arm geometry |
| Harrier | `whvAceTick` plus carrier cannon/beam/shot controllers |
| Warden | current `s7mTick`: pursuit, swipes, jumps, stomps and later gun/toxic patterns |

Proxies own attack state only. They cannot award a second victory or run a donor's
campaign ending. Live modules supply muzzle/collision positions; broken guns,
missile racks and beam emitters stop firing. Delayed locks cancel on transformation.
Form HP, broken parts and controller state persist across returns. Each form gets
up to 32 seconds before returning home, with an additional telegraphed alien volley.
Dracula gets three base attack beats, including flanking orb casts. The design reference
was [SotN True Dracula and Shaft gameplay](https://www.youtube.com/watch?v=6rXONPQvoTw),
particularly its throne/heart silhouette, curling limbs and flanking attacks.

Blue Hybrid, Hexpyre, Imp Harrow and Furnace Maw release distinct multi-shot sequences
(20/16/8/12 rounds in the controlled burst fixtures). Existing Rifle Locust guns,
demon cannons and Hellhugger's intended fast melee role remain.

Orb motion and timers are initialized and frame-rate consistent. Fire/kinetic/water/
toxic impact orbs have stronger level-scaled bodies, splash damage and authored bursts;
other orbs retain their status/area roles with stronger ticks. Dark wells form sooner
and last longer. A real Level 3 Fire Orb dealt 36 primary and 23.52 nearby splash
damage in the native two-target test. Forge previews restore their canvas state after
errors, and malformed modular rotations no longer corrupt previews. All weapon/element
previews and repeated Up presses completed without errors. Global historical element
discovery no longer unlocks every run's combos; explicit purchased recipes remain.

### Readability and map

Boss hit flashes are short and throttled, modular overlays reduced, overlapping toxic
cloud opacity normalized, and cross-run explosions/beams/clouds cleared. Protected Stage
6 dialogue keeps the world moving but clears unrelated enemies and pickups.

Nine generated pieces make eight distinct biome islands and a central city, joined by
authored bridge art. Original source/prompt/crop records are under
`_ART_SOURCES/gameplay_1004`; normalization belongs to `repair_assets_1004.py`.
The complete map assembles, then zooms toward the selected island; hover lift and
camera movement work at 1920×1080 and 1000×900. Existing expansion map art remains.

### Verification and limits

- `node --check assets/game.js`, both new runtime modules: pass.
- `node _BUILD_SOURCE/test_fl.js`: exit 0; **7,038 passing assertions**, final
  `FALVA/LIZZIE BUILD OK, 0 ERRORS` summary reached.
- The first full run exited nonzero with four obsolete Forge/profile expectations:
  legacy paid levels, duplicate detection, second-element selection, and global arcade
  recipe preservation. Fixtures now explicitly discover required elements and assert
  the requested isolation. The complete rerun passes; no assertions were removed.
- Native Chromium probes: `probe_gameplay_repair_1004.py`, `probe_repair_routes_1004.py`,
  `probe_repair_polish_1004.py`, `probe_repair_map_1004.py`,
  `probe_repair_modules_1004.py`, `probe_repair_cinematic_1004.py`.
  Completed reports contain zero page/console errors. Screenshots were inspected.
- All seven donors exercised at full and 24% HP with finite movement/projectiles;
  specific disarm and delayed-lock checks pass. Knight warning exists during the tell
  and disappears during recovery. Hammer death renders before the still transition.
- Review: `_shots/gameplay_audit_1004/review.html`. Portable results:
  `docs/qa/gameplay_repair_1004.json`. Probe fixtures are not full human campaign clears,
  all-pilot balance certification, or a complete audio review of the recording.
