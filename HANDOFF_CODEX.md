# Handoff to Codex — 2026-09-13 (from Claude)

Read `CLAUDE.md` in this folder first. Its tail has notes for every drop below.

## Status
- **Nothing is committed or pushed.** All of the work below is local in the working tree.
- **origin/main is ahead** by two Tempest-staging commits from another session, labelled 0912u and 0912v. My local drops also use the labels 0912u–0912z, so the labels clash.
  - Before committing: `git fetch`, rebase or merge, and relabel the local drops.
  - Commit only when Mike asks.
- **Test suite** (`node _BUILD_SOURCE/test_fl.js`, a CRLF file): 3,626 checks pass and 61 fail. All 61 failures already existed before these drops; don't chase them as regressions.
  - To spot a new failure, compare the list of failing check names against the previous run, with the numbers in them masked.
- **C: drive has about 5 GB free.** Don't make worktrees or full copies of the repo.

## How to verify changes
- The suite has missed real bugs before. Check anything visible with `_BUILD_SOURCE/shoot.py`, which runs the game in real Chromium; the probe scripts are listed below.
- `assets/game.js` is about 64.7k lines with LF endings. Have only one writer editing it at a time.

## Changes in the working tree
| Drop | What changed | Probe |
|---|---|---|
| 0912x | Stage-3 boss laser warning: FOV cones (`L23_FOV`, `l23FovDraw`) go green, then yellow, then red; alert frames use `bmfx_alert_<col>_danger` | `probe_fov_telegraph_0912x.py` |
| 0912y | Every hit now flashes the enemy through `markHit(t,f)`, which runs before shields and part routing: enemies, `hitBoss`, `hitSubBoss` and the Furnace Tyrant (`fztFlashSprite`, plus a nearest-part fallback in `furnaceHit`). The sealed quad-laser is exempt and keeps its shield pulse. Six enemy draw functions gained hit tints | `probe_hitflash_0912y.py` |
| 0912z | Juggernaut's two wrecking balls: the chains are anchored under the hull (`WB_CHAIN0=14`, `wreckPos`/`wreckSync`) and cleared on special end, death and the attract demo. His charge dash is easier to see: launch ring, afterimages, bigger wake, landing ring, sound | `probe_wreckdash_0912z.py` |
| 0913a | The spaceship is used in every space scene (`spaceShipActive()`, `gravityModeRetain`) with per-pilot palettes. The transformation is fixed (no shrink or black frame; doesn't replay after returning from stage 9). Also a spaceship death spin and somersault frames. The weapons atlas gained 16 cells | `probe_spaceship_0913a.py` |
| 0913b | Tempest Leviathan is now stage 6's miniboss (`SUBBOSS[6]`), with the Blacksteel Raptor as the alternate (`ALTBOSS[6]`). Art is in `assets/game/bosses/tempest/`; the patch was applied by `patch_tempest_0913b.py` | `probe_tempest_0913b.py` |

New suite sections are §289–§293.

## Open decisions for Mike
1. Once the spaceship is earned, re-entering stage 5 from the map skips the transformation. Should it play every time?
2. Tempest Leviathan:
   - Hitting a laser port flashes the whole hull. On the quad-laser, only the hit turret lights.
   - Its frenzy lasers draw over the MINI BOSS bar.
   - Its needles are the fastest enemy round at 7.49 px/frame.
   - A ram from the right edge can park half hidden behind the EQUIPPED box.
   - The pursuer can't clear a player hugging the bottom edge.
3. Razorback pellet collision and exposed-gun laser hits resolved by Codex on
   2026-09-13; see `docs/BUGFIX_0913.md`.
4. Older open items:
   - End-card copy resolved by Mike on 2026-09-13; see the Codex update below.
   - Cole's silent middle nuke resolved by Codex on 2026-09-13; see `docs/BUGFIX_0913.md`.
   - Stage-5 laser cannon loudness.

## Trailer
- **Outputs:** v7 is on the Desktop as `BulletsOfFury_Trailer.mp4`. Older versions are kept as `_v2`–`_v6`, and Mike has seen v7.
- **Pipeline scripts:** `capture3.py`, `edit3.py`, `mix3.py`, `render_v7.sh`. They live in Claude's temp scratchpad, `%LOCALAPPDATA%\Temp\claude\...\scratchpad\trailer\`, which uses about 20 GB.
  - Ask Mike before deleting anything there.
  - That folder can vanish, so don't depend on it.
- **Mike's trailer rules:**
  - One file, with the game's own sounds, and sound is never silent.
  - Only live in-game footage.
  - Pilots get equal screen time, with no repeated shots and no pilot twice in a row.
  - No boss name cards.
  - No stage-6 bosses, except the Tempest Leviathan duel.
  - Full-size view; zoom only on intense moments.

## Rules
- Don't echo SpriteCook signed URLs.
- Don't delete user data.
- A PostToolUse `validate_antipatterns.py` hook error comes from a broken plugin and can be ignored.

## Codex update — 2026-09-13: trailer end-card resolved

- Mike approved replacing the closing credit with **BUILT WITH THE ASSISTANCE OF AI & HUMAN TOOLS.**
- Updated `edit3.py` and `edl3.json` in `_BUILD_SOURCE/trailer_v7/` and rendered trailer v8.
- Output: `C:/Users/Mdogg/Desktop/BulletsOfFury_Trailer_v8.mp4`; v7 remains at its original Desktop path.
- Verified 9,900 frames at 1920×1080 / 60 fps, duration 2:45, full decode with zero duplicate or dropped frames.
  The full AAC soundtrack and the first 9,566 video frames match v7 by SHA-256.
- The updated encoded end-card was inspected. The 44px credit fits on one line with safe margins.
- Validation: `docs/qa/trailer_endcard_0913_validation.json`. Reusable range renderer:
  `_BUILD_SOURCE/trailer_v7/render_endcard_0913.py`.

## Codex update — 2026-09-13: Stage 6 Tempest duo integrated

- Mike approved the black/gray duo integration and the MINI BOSS laser visibility fix.
- `SUBBOSS[6]` now selects `tempestbrothers`; Blacksteel remains stored in `ALTBOSS[6]`.
  Other stage assignments were preserved. The original solo Tempest remains spawnable.
- Reviewed source is pinned to GitHub main `f936f106d85d935aaf518fbac5ab34756bc26724`.
  Native adapter/source notes: `docs/TEMPEST_BROTHERS_0913.md`.
- Independent ship/aperture damage, combined gauge, coordinated pincer/ram timing,
  offscreen gray holds, survivor AI and one ordinary final slot release are wired into BOF.
  Gray's return/counterattack and visible regroup now also defer black's ram warning.
- Forward lasers stop below the gauge; duo drawing clips below its band and the gauge draws last.
- Real in-game recording with game SFX: `_shots/tempest_duo_0913/BulletsOfFury_Stage6_TempestBrothers.mp4`.
  58 seconds, 960×1024, 30 fps. The demonstration uses an invincible pilot and accelerated native
  damage gates; gameplay code contains neither capture behavior.
- Validation: syntax checks passed; full suite **3,647 passed / 60 failed**, exit 1,
  with **zero new failure names** against the takeover baseline. All 20 new native duo checks pass.
  Real Chromium **16 passed / 0 failed**, with zero page or console errors.
- Results: `docs/qa/tempest_brothers_0913.json`; complete log:
  `_shots/tempest_duo_0913/test_fl_final.log`. Nothing committed or pushed.

## Codex update — 2026-09-13: Mike's revised fighter flight

- After viewing the duo, Mike requested south-facing jets, rapid turns/slides,
  red-to-green flashes and charged thrusts toward the pilot with sounds. This
  supersedes the earlier fixed nose-up/one-axis direction for the active duo.
- Both authored hulls now bank, slide twice, aim red, lock green, thrust along a
  fixed committed vector, brake and turn back to the upper arena. Only one
  brother owns a pass at a time. Independent damage, disabled apertures,
  phase/death cancellation, survivor behavior and campaign slot release remain.
- Hull art, hardpoints, hit geometry, gunfire and laser lanes rotate together.
  The existing authored engine flames follow each tail. Charge, ready, turn,
  booster, engine-loop and braking cues use the game's own sound samples.
- Source and notes: `_BUILD_SOURCE/tempest_source_0913/fighter.js`, `adapter.js`
  and `docs/TEMPEST_FIGHTER_0913.md`. The source builder embeds them in the actual
  `assets/game.js` runtime; stored solo Tempest remains original.
- Video: `_shots/tempest_fighter_0913/BulletsOfFury_Tempest_FighterPasses.mp4`.
  Thirty seconds, 960×1024 at 30 fps, 900 fully decoded frames with game SFX.
  The recording uses real movement/fire input and an invincible demo pilot;
  health gates are not accelerated. Capture behavior is confined to the probe.
- Syntax checks passed. All 12 new fighter tests pass; real Chromium passed
  **10 / 0**, with zero page or console errors. Two full suite runs each finish
  **3,658 passed / 61 failed**, exit 1. Sixty failure names match the takeover
  baseline. The additional Stage 1 sand-wave sampling failure also exists in the
  earlier duo log from before fighter flight; no unexplained failure names remain.
- Results and comparison evidence: `docs/qa/tempest_fighter_0913.json`.
  Complete logs: `_shots/tempest_fighter_0913/test_fl_final.log` and
  `test_fl_confirm.log`. Silent video/WAV intermediates removed; final recordings
  and user data retained. Nothing committed or pushed.

## Codex update — 2026-09-13: complete thrust exit and physical return

- Mike requested that each jet turn into its thrust direction, fly offscreen,
  and then fly back onscreen. The charge now waits for nose alignment before
  ignition; thrust stays aligned and continues until the entire rotated hull
  and exhaust clear a camera edge. The old onscreen timer brake is removed.
- The jet turns fully offscreen, then flies back at 560 world pixels/second
  facing the inbound path. It reaches its visible upper-arena position before
  releasing its pass. No teleport or early timed return completion. Existing
  damage, phase/death cancellation, duo coordination and red/green cues remain.
- Notes: `docs/TEMPEST_RETURN_0913.md`. Source remains `fighter.js` in
  `_BUILD_SOURCE/tempest_source_0913/`, embedded in `assets/game.js`.
- Video: `_shots/tempest_return_0913/BulletsOfFury_Tempest_ExitAndReturn.mp4`.
  Thirty seconds, 960×1024 at 30 fps, 900 fully decoded frames with game sounds.
  Both brothers complete two exits and two returns. Real movement input,
  invincible demo pilot, unchanged health gates. Prior videos remain intact.
- Syntax checks passed. All eight new section-296 tests pass. Full suite:
  **3,666 passed / 61 failed**, exit 1, zero new failure names against the prior
  fighter baseline. Real Chromium **14 passed / 0 failed**, zero page/console
  errors, zero thrust/return heading mismatches or position jumps.
- Validation: `docs/qa/tempest_return_0913.json`. Run the actual-game probe with
  `python _BUILD_SOURCE/probe_tempest_fighter_0913.py --return-pass`.
  Nothing committed or pushed.

## Codex update — 2026-09-13: collision, laser reach and nuclear audio fixes

- Mike asked Codex to continue improving and bugfixing the game. Three reproduced
  bug groups were fixed; notes and reproduction details: `docs/BUGFIX_0913.md`.
- Razorback ordinary shots now use exposed-part collision, so sealed armor,
  destroyed guns and invulnerable transitions do not swallow pellets.
- Held lasers now intersect finite beam widths/endpoints with exposed Razorback
  guns and rotated Tempest geometry. The duo's combined center no longer blocks
  a reachable target, and targets beyond the endpoint remain unhittable.
  Tempest laser damage routes to the nearest intersected brother/live aperture.
- Cole's 1.8-second nuclear sound gate rejected the middle impact in a three-nuke
  sequence. The gate is now 120ms, with the same sample, volume, filters and pool.
  Actual before/after sound acceptance: true/false/true -> true/true/true.
  The three-cue game-mixer render has peak 0.3684, no clipping or errors.
- Readable sources: `_BUILD_SOURCE/bugfix_0913/beam.js`, `tests.js`, and the existing
  Tempest adapter/fighter sources. The actual self-contained runtime is `assets/game.js`.
  Rebuild with the Tempest integration script followed by `bugfix_0913/integrate.py`.
- Syntax checks passed. All 14 new section-297 tests pass. Full suite:
  **3,680 passed / 61 failed**, exit 1, zero new failure names against the prior
  return-pass baseline. Targeted Chromium **11 / 0**; original live Razorback
  attack/progression probe **19 / 0**; zero page or console errors.
- Validation: `docs/qa/game_bugfix_0913.json`. Actual before/after screenshots,
  archived before-runtime and sound proof are under `_shots/game_bugfix_0913/`.
  Existing dirty work and previous recordings preserved. Nothing committed or pushed.

## Codex update — 2026-09-13: four weapon graphics and sound

- Mike requested improvements to Cole Sonic Boom, Juggernaut charge dash and wrecking balls, and Laser Mist. Details: docs/WEAPON_FEEDBACK_0913.md.
- Authored compression fronts and wakes scale with sonic charge. Juggernaut has aft exhausts, clear ram plates, a solid dash hull and independent mechanical audio. Two opposite flails keep their original contact rules and ship anchors, with full steel art, visual recoil, stationary contact flashes and gated metal cues. Laser Mist has three blue launch flashes, readable lance echoes, split pulses and one sound per split beat per wave. Sixteen authored WAV mixes are registered through seventeen explicitly tamed runtime sound routes.
- Fixed duplicated generic ram explosions and dead-pilot charge ownership. Laser Mist now honors exposed miniboss geometry; sealed Razorback armor no longer consumes lances with fake wet impacts, while live rotated guns take damage.
- Syntax passes. All 23 new section-298 assertions pass. Full suite: 3,703 passed / 61 failed, exit 1, no new failing assertion names against game_bugfix_0913. Focused Chromium 27/0, original wreck/dash probe 23/0, zero page/console errors. Runtime LF and suite CRLF preserved.
- Video: _shots/weapon_feedback_0913/video/BulletsOfFury_Weapon_Feedback_0913.mp4. Forty seconds / 1,200 fully decoded frames / 960x1024 at 30fps, frame-aligned game sounds, protected demo pilot, unchanged target health gates. Cole 0–10s, dash 10–20s, flails 20–28s, mist 28–40s. All four mixer renders stay below clipping with zero cut voices.
- Sources and probes: _BUILD_SOURCE/weapon_feedback_0913/. They reproduce the runtime byte-for-byte. Proof and complete baseline failure names: docs/qa/weapon_feedback_0913.json. Prior dirty work, videos and trailer scratch preserved. Nothing committed or pushed.

## Codex update — 2026-09-14: stage 1–5 encounter corrections

- Mike clarified that surviving stage-1 fodder should burn at half health, and
  space Volley Missiles should be the passive homing upgrade in its space style.
  All requested stage 1–5 corrections are implemented. Details:
  `docs/STAGE_1_5_CORRECTIONS_0914.md`.
- Stage 1 uses clean plates plus animated half-health fire/smoke; Razorback and
  Overlord have dedicated weapon and rotor sounds. Stage 2 uses reviewed stable
  projectile flight poses. Stage 3 boats are stored with their assets/controllers
  preserved; ice-drone shots are larger, and every Rime Wall laser originates at
  an actual cannon with authored FOV warning and center charge.
- Olive Warden has mounted spread guns, centered dual straight guns, mounted
  rocket salvos and anchored flashes/sounds. Sovereign helpers fit outside its
  shield above the generator columns. A held laser pierces both nodes per column.
  Its unpowered dive clears the screen, flies overhead with a frame-shaped shadow
  and returns through the opposite edge without an invisible ground-plane hit.
- Stage 5 extends the scrolling sky to five seconds, uses the finished authored
  spaceship, keeps three passive homing volleys independent, reduces cannon gain
  to 0.30 and raises Shadow Orb damage 35%. Regent stays centered with charged
  escort fire and warnings for each new grid opening. Dense combat effects use
  0.40 encounter gain; voices and player volume preferences remain intact.
- Syntax passes. Full suite: **3,724 passed / 61 failed, exit 1**, final summary
  reached; all 61 failure names match `docs/qa/weapon_feedback_0913.json` after
  normalizing dynamic numeric observations. All 21 section-299 assertions pass.
  Real Chromium **42 / 0**, zero page, console or controlled-loop errors.
  Actual held input, authored source pixels and screenshots were checked.
- Preview: `_shots/stage_1_5_0914/video/BulletsOfFury_Stages_1_to_5_0914.mp4`,
  **76 seconds / 2,280 decoded frames / 960×1024 at 30 fps**, native game sounds,
  protected demo pilot and selected debug attack windows. Sovereign's demo has
  1-HP nodes after its 75/50% gates; runtime health gates are unchanged. All ten
  sound-effect renders stay below clipping; rapid-fire voice-pool reuse is
  retained. Music is not included. The recorder pins the buffer-source overload
  to fix inherited noise scheduling, without export-only normalization.
- Proof and current measured baseline: `docs/qa/stage_1_5_0914.json`. Sources:
  `_BUILD_SOURCE/stage_1_5_0914/`; exact archived dirty baselines and verification
  output remain under ignored `_shots/stage_1_5_0914/`. `integrate.py --dry-run`
  reconstructs the comparison byte-for-byte; mutation refuses subsequent edits.
  Do not run older integration workflows over this newer runtime. Runtime LF
  and suite CRLF preserved. No atlas changes, GitHub integration, commit or push.
  Prior staged/unstaged/untracked work and user/trailer recordings are preserved.

## Codex update — 2026-09-14: readable attacks and overnight work

Mike authorized autonomous work until morning. Full scope:
docs/OVERNIGHT_REQUESTS_0914.md. Thread heartbeat every 30 minutes through 8 AM
EDT September 14; quiet unless meaningful verified progress or required access.

Verified batch: docs/READABLE_ATTACKS_0914.md. Stage-1 jets lose their second
generic volley; Stage-3 blue side beams and finite central pulse; Furnace head
aim/pose commitment; Regent mounted-port warnings; six ordinary space impact
decorations; player flame shrinks 25%, boss flame widens 25%; Backspace pause
protection. Shared warning/gliding helpers ready. Full encounter migration,
dark-blue refinement, pause menu and new progression remain pending.

Syntax passes. Full suite **3,734 / 60, exit 1**, no new failing assertion names
against stage_1_5_0914; one prior randomized sand-tank assertion passed this run.
Section 300 9/0; Chromium 47/0, zero errors.
Proof: docs/qa/encounter_cleanup_0914.json.
Video: _shots/encounter_cleanup_0914/video/BulletsOfFury_Readable_Attacks_0914.mp4,
37 seconds/1,110 decoded frames, native sounds, protected debug pilot, no music.
Sources: _BUILD_SOURCE/encounter_cleanup_0914/. Do not run older integration
workflows over this runtime. LF/CRLF preserved. Nothing committed/pushed.

SpriteCook's Claude plugin exists but no authenticated callable SpriteCook MCP
is exposed to this task; ElevenLabs is likewise unavailable. Specified art is
pending. Do not extract OAuth credentials or substitute ImageGen for Mike's
specified SpriteCook work. Existing authored assets remain usable.

## Codex update — 2026-09-14: missile supplies

Verified details: docs/MISSILE_SUPPLIES_0914.md. Boss/miniboss supply clock
7-second first allowance/18-second restock, one shared live ammo box, Hard/Furious
25% faster restocking. Stages 1–7 x5/x10/x20; stage 8 x50/x100. Stage 9 retains
small x5/x10 pending Mike's quantities. x5 grants five (formerly three); x2
migrates to x5. Fodder-only one/two spinning projectile pickups, bounded scatter,
one roll per death, native one-round collect. Bosses/minibosses/props excluded.
Tier upgrades/caps remain pending SpriteCook art.

Syntax pass; full suite **3,745 / 61, exit 1**, final summary reached, names
match stage_1_5_0914. Section301 12/0; Chromium11/0, zero errors.
Proof: docs/qa/missile_supplies_0914.json. Sources:
_BUILD_SOURCE/missile_supplies_0914/. Prior runtime archived under ignored
_shots/missile_supplies_0914/. Do not run older integrators over this runtime.
LF/CRLF preserved, nothing committed/pushed.

## Codex update — 2026-09-14: green pause menu

Verified details: docs/PAUSE_MENU_0914.md. Drop-in Resume/Return to Main Menu/
Restart/Options/Help/Quit rows, authored green cursor/fonts and existing chrome
helpers. Grayscale playfield via one reusable offscreen composite. Music ducks
to 28% without altering the preference. Real Options/Help return to frozen combat;
Backspace cannot abandon the stage. Restart resets the same level.

Campaign Return/quit: verify rotating Autosav01/02/03.json localStorage records
(separate from manual slots), native anchored death spin/crash, game-over cues/
over voice, fade and title/exited state. SAVED only after identical readback.
Continue recovers latest campaign record after session loss; controls reset
preserves autosaves. These are browser JSON records, not Windows files.

Syntax pass. Full suite **3,756 / 61, exit 1**, final summary reached, all names
match stage_1_5_0914. Section302 11/0; Chromium14/0, zero errors.
Proof: docs/qa/pause_menu_0914.json. Sources: _BUILD_SOURCE/pause_menu_0914/.
Runtime SHA256 2fd799df3f07d58042ee5093e1e2ea935c772d12da6ee44f426a1541867f4bdd.
LF/CRLF preserved. No commits/push or user-data deletion. Bitmap button production
and remaining overnight scope stay pending in docs/OVERNIGHT_REQUESTS_0914.md.

## 0914 shared laser warnings
Shared laser families now inherit the same three-second authored green/yellow/red FOV. Stage-3 cannons use dark-blue bodies and a narrow light core. Full suite 3759 pass / 61 baseline failures, exit 1; Chromium 7/0, no errors. Proof: docs/qa/shared_laser_warnings_0914.json. Combined pause/laser video is pending a clipping correction for overlapping death explosions. Retina target eligibility is next.

## 0914 Retina component target pass
Read docs/RETINA_TARGETS_0914.md and docs/qa/retina_targets_0914.json. Runtime SHA256 95b659ac2bd4327f292e4197fdb56bf8aa6449baa7ca3632ea471373c8123e53; suite 3771/60 exit 1, no new failure names, historical random sand-tank check passed. Chromium12/0. Component targets and manual missile damage verified. Native pause/blue-laser video now fully decoded with unclipped audio: _shots/shared_laser_warnings_0914/video/BulletsOfFury_Pause_and_Blue_Lasers_0914.mp4. Current source: _BUILD_SOURCE/retina_targets_0914. Do not run old integrators over this newer runtime. Next: directional multi-lock upgrade and five-second sequential missile firing; universal no-one-shot rule, Hard/Furious variants and achievements remain pending. Preserve all dirty work; no commits/pushes/deletions authorized.

## 0914 directional Retina Scan verified
Read docs/RETINA_SCAN_0914.md and docs/qa/retina_scan_0914.json. Four-target directional scan, five-second expiry, 50ms sequential manual missiles, exact ammo, invalid-target skips, pause/death cleanup and campaign equipment persistence. Native13/0; section30516/0; full suite3787/60 exit1, no new assertion names (historical random sand-tank check passed). Runtime SHA256 3e8159683cba3b65b344244e50de5ee300e0f7371e2119eb5b30bd9511a14212. Current source _BUILD_SOURCE/retina_scan_0914; older integrators must not overwrite this runtime. Native14sec preview _shots/retina_scan_0914/video/BulletsOfFury_Retina_MultiLock_0914.mp4, 420 frames decoded, 60% in-game SFX, no export normalization. Universal no-one-shot rule and remaining Hard/Furious/achievement/missile-tier work are still pending. Mike explicitly resumed development after the overnight schedule ended with "continue on lad!". No new recurring automation was created.


## 0914 Arcade credit rules and request tally
Mike asked to continue unfinished work and maintain a tally. Read docs/REQUEST_CHECKLIST_0914.md: 135 entries, 44 complete / 11 partial / 80 pending. Its editable source is docs/REQUEST_CHECKLIST_0914.json; regenerate with python _BUILD_SOURCE/update_request_checklist.py. Do not count partial encounter passes as finished designs.
Arcade stocks now match Easy/Normal/Hard/Furious lives 7/5/3/3, continues 7/5/3/1, including a run-wide bank in Stage 9. Campaign/co-op tuning stays separate; campaign loads refresh DIFF. Native difficulty and credit prompts verified with real Enter input; the Stage-9 retreat cannot refund Arcade credits. Proof and limits: docs/ARCADE_RULES_0914.md and docs/qa/arcade_rules_0914.json.
Full suite 3804/60, exit 1, final summary reached, no new failing assertion names; section306 17/0. Native Chromium 22/0 with no page/console/loop errors. Runtime SHA256 41ee9c77220592dc818374cd5a1fba54d870ac22036c113c38284d48c9b15835. Runtime LF and test CRLF preserved. Current patch sources _BUILD_SOURCE/arcade_rules_0914; do not apply older integrators over this build. No commits, pushes or user-data deletion.
Next shared foundations remain universal no-one-shot damage and elemental/shield behavior; encounter variants, production assets and achievements remain on the checklist. The overnight schedule expired; this was Mike's resumed interactive request, not a new background automation.


## 0914 easiest-to-hardest queue — first two entries verified
Mike asked for the full list in chat and work ordered easiest to hardest. Current queue is docs/WORK_ORDER_0914.md, generated from workOrder/difficulty fields in docs/REQUEST_CHECKLIST_0914.json. Tally: 135 entries, 46 complete / 11 partial / 78 pending (89 unfinished). Follow ascending ready work; respect dependencies and skip unavailable external assets. This replaces the earlier foundation-first ordering.
Completed SPACE-15: eight supplied Space Fighter model announcements; Decker currently displays SPACE FIGHTER DECKER pending Mike's requested naming response (SPACE-16). Completed MODE-06: Hard/Furious Life Up chance +25% on both midpoint and ordinary death routes, without stealing ammo/shield outcomes. Midpoint pickups use visible camera bounds. New ship and Life Up replacement art remain pending.
Proof docs/EASY_QUEUE_0914.md and docs/qa/easy_queue_0914.json. Native Chromium25/0, no page/console/loop errors; section30715/0; full suite3818/61 exit1, final summary reached, no new failure names. Historical random sand-tank assertion failed this time. Runtime SHA256 e2e95dfbd9e0d65bfe55ac40d4989f3be1aba6d3ad4f33c9c89efe5f57674533. Sources _BUILD_SOURCE/easy_queue_0914; LF/CRLF preserved. No commits/pushes, new atlas art, data deletion or background automation.
Next ready item: MSL-09 remaining missile-supply frequency audit, then SPACE-11 source-ship inspection, S4-02 screenshot review and S2-05 actual flame shield from the opening frame. Decker naming is independently pending; do not invent a model.


## 0914 Draven and complete missile supply frequency
Mike named Decker's Space Fighter Draven and asked to continue. SPACE-16 and MSL-09 are now complete. Read docs/SUPPLY_AUDIT_0914.md and docs/qa/supply_audit_0914.json. Hard/Furious boss opening/repeat times 5.6/14.4s; fodder loose chance 12.5%; legacy single-ammo chance 7.75%; scheduled/scripted boxes receive one 25% bonus roll with a two-second, existing-box-clear queue. No recursive bonus or double bonus on the boss clock. Forced scripted x10 stays guaranteed.
Native27/0, real crate shooting/collection and real player death, zero page/console/loop errors. Full suite3839/61 exit1, final summary, section30821/0, no new failure names; historical random sand-tank assertion failed. One section307 fixture now allows the extra ammo interval above its life boundary. Current runtime SHA256 41a0790603c5e4d8320839e1083b19a6e123e9075fce334a744825dea888d7d5. Sources _BUILD_SOURCE/supply_audit_0914; LF/CRLF preserved. No commits/pushes/atlas edits/user-data deletion.
Tally 135: 48 complete / 10 partial / 77 pending. Follow docs/WORK_ORDER_0914.md. Next SPACE-11: distinct new SpriteCook ship concept not yet identified; current ledger contains Warden/map assets and the known active ship traces to _ART_SOURCES/gravity_mode_v2. Do not select the already-shipped ship or GPT component master as the new concept without evidence. Then S4-02 screenshot review and S2-05 actual flame shield opening.


## Codex update — September 14: Furyship source selected

Mike approved `assets/game/gravity_mode/furyship_somersault_13.png` as the top-down replacement reference. Actual PNG and the existing sixteen-frame reel were inspected. SPACE-11 is complete; new parts, perspective frames, transformation and speed effects remain pending. See `docs/FURYSHIP_REFERENCE_0914.md`. SpriteCook is unavailable; tool-choice clarification is pending. No runtime or atlas change in this pass.


## Codex update — September 14: Furyship generated candidates

Mike approved built-in image generation for the ship. Eight master sheets and 70 normalized transparent candidate frames are saved with prompts/build metadata. Native Chromium rendered 71 assets including the approved reference with zero browser errors. Interactive preview also checked. See `docs/FURYSHIP_ASSETS_0914.md`. Exact assembly fit, intermediate animation/palettes and gameplay integration remain; SPACE-12/13 are partial. Runtime unchanged, no gameplay-suite rerun.


## Codex update — September 14: somersault and nine palettes

Added 12 generated somersault candidate frames (82 total frames) and 50 blue/cyan masks. Verified all 450 pilot/frame palette combinations and preserved all unmasked pixels. Native render: 83 assets including reference, no browser errors. See `docs/FURYSHIP_SOMERSAULT_0914.md`. Runtime integration/assembly fit and some frame-width drift remain. SPACE-14 is now partial; runtime unchanged, no gameplay-suite rerun.


## Codex update — September 14: Furyship installed in the game

Read docs/FURYSHIP_LIVE_0914.md and docs/qa/furyship_live_0914.json. The approved frame-13 hull, six-part assembly, 12 somersault poses, both eight-frame rolls, transition/speed effects and all nine palettes now run in the game. SPCBOY selects the preserved original fighter; campaign snapshots save/restore the selection. New cannon anchors and space death/Stage 9 rendering verified. Sources _BUILD_SOURCE/furyship_live_0914; no atlas repack or shipping-manifest changes in this batch.

Native Chromium 26/0, no page/console/loop errors. Full suite 3,849 passed / 61 failed, exit 1, final summary reached; failure names exactly match docs/qa/supply_audit_0914.json. Section309 10/0; two older replacement-sensitive assertions updated with separate legacy checks. Runtime SHA256 3fc67f9238c635ee3367f574a2a57bd2a1094ffadcf52aae1b7e76de59a02e45. LF/CRLF preserved.

Video: _shots/furyship_live_0914/video/BulletsOfFury_Furyship_0914.mp4 (26 seconds, actual game sound events, export gain prevents clipping, full decode passed). Capture skips completed HQ dialogue/entrance and uses fixture-only invincibility; this is not a full balance run. SPACE-13/14 complete; SPACE-12 partial for wingspan/silhouette drift and smoother component turns/fit. Tally 135: 51 complete / 11 partial / 73 pending, 84 unfinished. Preserve docs/WORK_ORDER_0914.md; the larger encounter requests are still open. No commits/pushes/deletion/background automation.


## Codex update — September 14: cloud-flight intro revision

Mike rejected the small six-piece assembly and slow sweep. Read docs/FURYSHIP_CLOUD_INTRO_0914.md and docs/qa/furyship_cloud_intro_0914.json. The new Stage-5 intro now stays at 420px/s through sky, clouds, clearing, assembly, white fade and countdown. Twelve independent pieces use the existing authored kit; full-size loose cells draw at 194.7px around a 118px cinematic hull. The local energy ring is smaller. Space replaces sky only under opaque white, which also covers HQ and scanlines. Latest request explicitly supersedes the old no-fade rule for this intro. Retained new fighters skip rebuilding and stay 48px; other stages/legacy route unchanged.

Native full launch from t=0 including all HQ dialogue: 11/0; separate retained/animated-exhaust probe passed; zero page/console/loop errors. Full suite 3,850/60 exit1, final summary, no new failure names. Historical random sand-tank assertion passed; no fix claimed. Test file unchanged. Runtime SHA256 3d55604968cc2af62926ed8ef7ed296a03cf051c57d87686ad6434d9405e2978. LF/CRLF preserved. Video _shots/furyship_cloud_0914/BulletsOfFury_Cloud_Transformation_0914.mp4 (26 seconds, game sound effects, fully decoded). Sources _BUILD_SOURCE/furyship_cloud_0914; do not reapply prior integrators over this build.

Tally still 135: 51 complete / 11 partial / 73 pending. SPACE-12 retains art consistency/fit/perspective refinement; SPACE-13 evidence updated for the revised staging. No commit/push/atlas edits/user-data deletion/background automation.


## Codex update — September 14: solid parts, individual arrivals and faster sky

Mike rejected part fades, perspective flips and travelling top/bottom clouds. Read docs/FURYSHIP_SOLID_ASSEMBLY_0914.md and docs/qa/furyship_solid_assembly_0914.json. Parts now use opaque top plates only, rotated in evenly spaced orbits. Twelve individual bottom entrances begin in the cloud section, 0.54s apart, each with the new game-engine furyPartArrival sound. Incoming kit draws above clouds, plane beneath the holes. Entire kit stays opaque until the full white transition hides the completed-hull substitution. No per-part fade or mirrored transform. Side banks hold fixed positions; the central cloud deck passes once and does not wrap. Intro speed 1,000px/s, no braking. Flight roll/somersault frames unchanged.

Native full-launch checks 17/0, actual draw opacity/key/transform and twelve sound-cue timing audit passed; zero page/console/loop errors. Video _shots/furyship_solid_0914/BulletsOfFury_Solid_Assembly_0914.mp4 (26 seconds, game sound, full decode passed). Full suite 3,849/61 exit1, final summary, exact failure names from furyship_live_0914 baseline. Historical random sand-tank assertion failed. Test file unchanged; LF/CRLF preserved. Runtime SHA256 5150c9c4134da494bec2d2789b9e7fecfd4c022f8647302a470945f4072109b5. Sources _BUILD_SOURCE/furyship_solid_0914. Do not reapply old integrators over this build.

Checklist remains 51 complete / 11 partial / 73 pending. SPACE-12's assembly perspective blending is superseded by the opaque top-view rotation requirement; flight silhouette consistency and exact fit remain. No new bitmap/atlas/manifest changes, commit, push, user-data deletion or automation.


## 0914 - Solid space hazards and shared dialogue frame

See docs/DIALOGUE_HAZARDS_0914.md and docs/qa/dialogue_hazards_0914.json. Generated pilot-tinted rectangular dialogue plate, centered stable typewriter text, no decorative asteroid/comet ghosts, physical shootable hazards and real contact checks. Native 12/12, no browser errors. Full suite 3852 pass / 58 inherited failures, exit 1, no new failing assertion names. Preserve all working changes; no commit or push. Checklist updated.


## 0914 - Static projectile cells and pixel glow

Read docs/PROJECTILE_PIXEL_GLOW_0914.md and docs/qa/projectile_glow_0914.json. Stage-5 CFX rows now hold column 1; Stage-2 saws already held that column. Shared fixed-frame shots get stepped pixel lighting without blur or growing sprites. Spin/trajectory/collision unchanged. Native 19/19, zero browser errors. Full suite 3853/57, exit1, no new failure names. No atlas/test changes or commit/push.


## 0914 - New Yuri and readable typography

Read docs/READABLE_TYPE_YURI_0914.md and docs/qa/readable_type_yuri_0914.json. Legacy Yuri portrait routes now use the approved seven new expressions; talking holds the approved idle pose. All nine pilots have compact dialogue portraits. Added uppercase Command Signal dialogue/TrueType, Command Alloy game labels and nine biome stage font variants. In-play panels clear the bottom HUD. Native 9/9, zero browser errors. Full suite 3852 pass / 58 inherited failures, exit 1; no new failure names against recorded baselines. Font/portrait source assets retained, no existing atlases changed. Harness loads current font registrations and updated obsolete font/portrait expectations. Checklist: 57 complete, 11 partial, 70 pending (81 unfinished). No commit or push.


## 0914 - Pilot name flair

See docs/PILOT_NAME_FLAIR_0914.md and docs/qa/pilot_name_flair_0914.json. Shared bitmap nameplates now have pilot-colored edges, white highlights, dark keylines and a slow three-second halo in dialogue, cinematic dialogue, comms and pilot selection. Authored portraits/body lettering preserved. Native 11/11, no browser errors. Full suite 3853 pass / 57 inherited failures, exit 1; no new failing names. One obsolete source-call assertion now checks pilotNameDraw. No atlas changes, commit or push. Tally remains 57 complete / 11 partial / 70 pending.


## 0914 - Stage-4 visual audit and Furnace flame shield

Read docs/ENCOUNTER_VISUAL_0914.md and docs/qa/encounter_visual_0914.json. S4-02 closed by native visual review: the apparent orange beams are road markings; Warden emits short machine rounds at its mapped mounts and upper racks are part of the whole authored plate. S2-05 fixed: actual Magma Ward flame shield now draws throughout Furnace assembly; the intro-only overload-wave substitute is removed. Lazy cells hold a decoded flame frame; break, core rearm and vulnerable head lifecycle verified. Native 16/16, no browser errors; two silent gameplay clips under _shots/encounter_visual_0914. Syntax passed; full suite 3853 pass / 57 inherited failures, exit 1, no new names. No atlas/test edits or commit/push. Tally 59 complete / 10 partial / 69 pending (79 unfinished). Next ready item is S1-04 Razorback baseline speeds, then S3-07 Hard/Furious size/palette.


## 0914 - Razorback baseline speed

See docs/RAZORBACK_SPEED_0914.md and docs/qa/razorback_speed_0914.json. S1-04 done: travel +30%, turn +20%, shots and rocket acceleration/cap +20%, Sonic Hammer/Nova expansion +25%. Warning/attack timing, HP and authored art unchanged. Native 12/12, zero browser errors; standing-hit versus post-release keyboard escape verified. Syntax passed; suite 3852/58, exit 1, no new failure names against recorded baselines. No test/atlas edits or commit/push. Tally 60 complete / 10 partial / 68 pending (78 unfinished). Next S3-07: Hard/Furious miniboss royal-dark-blue/black palette and +35% size.


## 0914 - Frost Cruiser Hard/Furious hull variant

Read docs/FROST_CRUISER_VARIANT_0914.md and docs/qa/frost_cruiser_variant_0914.json. S3-07 complete: the actual stage-3 miniboss is Frost Cruiser, not alternate Cryo Spear. Hard/Furious hull dimensions increase 168 to 226.8 (+35%) and use cached black/royal-dark-blue armor, preserving alpha, linework and protected emitters. Actual mounts, ordnance origins, collision bounds and damage/enrage rendering verified; Easy/Normal and other encounters excluded. Native 12/12, zero browser errors. Syntax passed; full suite 3851/59, exit 1: 58 recorded failures plus one intermittent road-tank heading failure reproduced identically against the pre-change backup (nine controlled cases). No newly introduced failure found. Silent seven-second native preview under _shots/cryo_variant_0914. No source-art, atlas or test-harness edits; no commit/push. Tally 61 complete / 10 partial / 67 pending (77 unfinished). Next UI-09: pilot-select letter reveal and stat-bar fill, followed by UI-08 fullscreen presentation.


## 0914 - Three new boss music tracks stored

Mike supplied minderaser (Boss 1), Hazardous-Death (Boss 2), and Lie Down or Stay Down (Boss 3). Original WAV copies are in assets/game/music/newboss/; see docs/NEW_BOSS_MUSIC_0914.md and the folder inventory.json. SHA-256 verified against Desktop originals. Stored only: no existing music replaced, no runtime registration or encounter music assignments changed. Boss numbers are inventory labels pending future direction.


## 0914 - Frost Cruiser nose laser correction

Mike clarified the wing pods are missile turrets and the nose must shoot Falva-style black/blue lasers. Read docs/FROST_NOSE_LASER_0914.md and docs/qa/frost_nose_laser_0914.json. Nose now launches fixed-frame fllaser_0 bolts at 24x112 and 0.34s cadence, with cached black/blue palette, four-step pixel lighting, laser muzzle/audio, nose-tail launch anchoring, committed aim and oriented shaft collision. Wing missiles and shared Jungle Cruiser nose remain unchanged. Full-tail culling and lazy-ready release guard verified. Native15/15, zero browser errors; nine-second silent native preview under _shots/frost_nose_laser_0914. Syntax passed; full suite 3852/58, exit1, no new names. No source-art/atlas/test-harness/music changes or commit/push. Checklist S3-14 added complete: 139 entries, 62 complete / 10 partial / 67 pending (77 unfinished). The charged sweeping beam and new difficulty attacks remain pending; next queue item UI-09.


## 0914 - GitHub integration and publication

Mike authorized committing and pushing the complete current build. Local build commit 45174735 collects game changes, art, new boss music storage and verification notes. Integrated origin/main through f936f106, preserving the Stage-6 duo and both stored ALTBOSS6/ALTBOSS8 encounters; Stage 8 now has no miniboss as requested in the incoming commit. Both sets of development notes are retained. Post-merge syntax passed, native15/15 with no browser errors; suite 3850/58, exit1, no new names. Read docs/GITHUB_BUILD_0914.md and docs/qa/github_build_0914.json. Unrelated nested projects and ignored scratch remain local.


## 0914 - Pilot text and stat reveal (UI-09)

Read docs/PILOT_REVEAL_0914.md and docs/qa/pilot_reveal_0914.json. The composed drawPilot screen now consumes the existing pcard reveal state for names, subtitle, biography, special and stat labels, then fills each bar from its left edge. Layout uses full strings; styled names keep one cached plate. Screen re-entry resets the reveal; Enter skips without same-press confirmation. Nine-pilot VM checks pass. Native controlled-time screenshots cover partial text, intermediate bars, skip and roster layouts; ordinary intro path not completed, and a review tab crashed during a large synchronous render batch before recovery with bounded steps. Full suite 3850/58, exit 1, no new failure names. UI-09 complete; tally 63 complete / 10 partial / 66 pending (76 unfinished). Next UI-08 fullscreen pilot screen, then ACH-09 boss fight timer. No commit/push.

## 2026-09-14 — generated input prompts / B is Back

Implemented Mike's consistent generated D-pad/action/Start prompts and logical B navigation; Backspace is deletion only. See docs/CONTROL_HINTS_0914.md and docs/qa/control_hints_0914.json. Final focused checks 25/0; full suite 3851/57, exit 1, no new failure names. Campaign-hub native proof is limited by the pre-existing missing CAMPHUB_ITEMS definition. AGENTS.md preserves the convention. Existing UI-08 and later work remain queued; nothing committed or pushed.

## 0914 — Pilot fullscreen desktop pass (UI-08 partial)

Read docs/PILOT_FULLSCREEN_0914.md and docs/qa/pilot_fullscreen_0914.json. Pilot now owns a proportional browser-sized buffer; card/roster expand and pointer mapping follows. Desktop Axel/Lizzie five-stat layouts and B return verified. Portrait bounds and backing pixels are valid, but resize screenshots remain black; fresh default tabs recover. Keep UI-08 partial and first in queue until this is resolved. Viewport override reset. Syntax passes, reveal9/0, controls25/0, full suite3851/57 exit1 with no new names. No commit/push.

## 0914 — UI-08 complete and ACH-09 boss timer

Pilot resize verified in a real game iframe at 390x844 and 1100x620, both directions; earlier native viewport capture gap closed. Read docs/PILOT_FULLSCREEN_0914.md follow-up. Added upper-right unit-owned boss/miniboss timer: excludes initial entry/pause, includes respawns/later transforms, freezes on defeat. Read docs/BOSS_TIMER_0914.md and QA. Focused12/0, full3851/57 exit1 with no new names; native timer review no errors. 66 complete / 10 partial / 64 pending; 74 unfinished. Next ENG-03 shared gliding/follow integration, then S3-05 miniboss movement and S1-07 chopper movement. No commit/push.

## 0914 — Shared glide and two encounter movement fixes

ENG-03, S3-05 and S1-07 complete. Read docs/MOVEMENT_BATCH_0914.md and docs/qa/movement_batch_0914.json. Frost tracks sampled player X, returns vertically on a committed lane and follows 1.15s before beam charge. Chopper orbit phase latches once; pursuit and orbit-entry speeds are bounded. Weapon patterns retained. Focused23/0, suite3850/58 exit1, no new names; native both encounters no errors. 69 complete / 9 partial / 62 pending, 71 unfinished. Next S1-08 rotor audio, UI-10 ship frame alignment, UI-07 title silhouettes. No commit/push.


## 2026-09-14 Overlord rotor audio
Dedicated original helicopter rotor WAV replaces the servo placeholder. Native loop/release verified; syntax passes; full suite 3850 passed / 58 known failures, exit 1, no new names. See docs/ROTOR_AUDIO_0914.md. Checklist: 70 complete, 8 partial, 62 pending; UI-10 ship-frame alignment next. No commit or push.


## 2026-09-14 Pilot ship alignment
UI-10 complete: menu-only alpha-bound centers and shared reel scale. Native 72 stock frames, nine onion pairs, Axel/Decker menu verified. See docs/SHIP_ALIGNMENT_0914.md. Syntax passed; suite 3850/58 known failures, exit 1, no new names. 71 complete / 8 partial / 61 pending, 69 unfinished. UI-07 next. No commit or push.


## 2026-09-15 Opener pilot pairs
UI-07 complete: nine frontal bodies beside ships, Cole-first 12s sweep. Corrected Lizzie to current ship. Native nine pairs and Enter-to-title verified; full suite 3850/58 known failures, exit 1, no new names. See docs/OPENER_LINEUP_0915.md. 72 complete / 8 partial / 60 pending; 68 unfinished. No commit/push.


## 2026-09-15 Generated pause-button art
UI-06 complete, six rows share generated plate with preserved endcaps and bitmap labels. Native selection/resume verified; suite 3851/57 known failures, exit 1, no new names. See docs/PAUSE_ART_0915.md. SpriteCook spent 16, balance 118. 73 complete / 8 partial / 59 pending, 67 unfinished. MODE-08 Life/Continue Up art next. No commit/push.


## 2026-09-15 Stage 4 death / Stage 5 transformer
Read docs/BOSS_BATCH_0915.md and docs/BOSS_DESIGNS_0915.md. New Easy/Normal Stage 5 chrome hammer transformer, authored SpriteCook reels, distinct manual missile knockback, 15-second ball and warned hammer leaps. Stage 4 cinematic cookoff and regenerated reflected-edge highway loop. Stage 2 identity question unanswered; do not replace its boss or generate the wrong head. Full natural-play balance remains SPACE-06. QA in docs/qa/boss_designs_0915.json. Preserve all dirty work; no commit/push.
Final 0915 boss QA: syntax pass; focused 20/0; full suite 3850 pass / 58 recorded failures, exit 1, no new names. Checklist 148 total: 79 complete / 8 partial / 61 pending (69 unfinished). SpriteCook balance 22.

## 2026-09-15 Overnight gameplay continuation

Chrome Hammer now has its one-hand vertical boomerang, Hard/Furious difficulty aces are injected across all nine stages, and Olive Warden Hard/Furious has both its warned assault cycle and difficulty-only two/three-escort formations. Read docs/CHROME_HAMMER_BOOMERANG_0915.md, docs/DIFFICULTY_ELITE_ACES_0915.md, docs/OLIVE_WARDEN_HARD_ASSAULT_0915.md and docs/OLIVE_WARDEN_ESCORTS_0915.md. Final focused sections 304e and 321-323 pass. Latest full suite has only the established 57 named failures; latest native proofs are 50-frame/zero-error hammer capture, 28/28 Warden assault, 42/42 nine-stage aces and 15/15 Warden escorts. Checklist 149: 114 complete / 9 partial / 26 pending, 35 unfinished. Mike explicitly authorized committing and pushing the completed overnight batch to GitHub.

## Codex update — 2026-09-15: Continue Up rewards

- MODE-07 is complete: deathless miniboss/boss encounters and Hard/Furious authored aces drop a physical Continue Up exactly once.
- Either co-op seat dying blocks the deathless reward. The collected credit extends the shared finite bank, survives campaign save/load, and is shown on the Continue screen.
- Current art is a clearly marked composition of the authored Life Up; MODE-08 still owns the dedicated SpriteCook pickup art.
- Verification: focused 18/18, Chromium 18/18 with zero errors, full suite exact 57-name recorded baseline. Evidence: docs/CONTINUE_UP_REWARDS_0915.md.

## Codex update — 2026-09-15: Sovereign helper blockade

- S4-11 is complete: Hard/Furious Sovereign helpers get 50% more shield capacity, faster attack handling and a timed forward blocking row that follows the player before returning to its generator stations.
- Normal remains unchanged. S4-12 and S4-13 still own the generator-hit enrage and side-stream follow-up.
- Verification: focused 14/14, Chromium 17/17 with zero errors, and the exact established 57-name full-suite baseline. Evidence: docs/SOVEREIGN_HELPER_BLOCKADE_0915.md.

## Codex update — 2026-09-15: Sovereign helper enrage

- S4-12 is complete: real Hard/Furious generator damage sends surviving helpers red to opposite edges with glowing asterisks, inward hull aim, and staggered six-round streams separated by recurring dodge gaps.
- The dedicated phase lasts 5.6s on Hard and 6.8s on Furious; unrelated boss orb/final-gun pressure pauses so the intended route remains visible. Normal is unchanged, and S4-13 still owns the later spider-walk tracking response.
- Verification: focused 12/12, Chromium 19/19 with zero errors, repeat full suite exact 57-name baseline. Evidence: docs/SOVEREIGN_HELPER_ENRAGE_0915.md.

## Codex update — 2026-09-15: Sovereign helper spider walk

- S4-13 is complete: generator damage during the red side phase makes both helpers walk upward and back within explicit 58px Hard / 72px Furious limits, while preserving the edge route, separated streams, and pause windows.
- Different nodes are recognized, repeated damage cannot pin the motion at its start, and a new response can begin after the pair returns. Normal is unchanged.
- Verification: focused 9/9, Chromium 13/13 with zero errors, full suite no new failure names. Evidence: docs/SOVEREIGN_HELPER_SPIDER_WALK_0915.md.
