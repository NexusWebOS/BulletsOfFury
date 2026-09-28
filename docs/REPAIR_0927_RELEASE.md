# September 27 download, repair pass and playable release

Downloaded `NexusWebOS/BulletsOfFury` main at `4ad8549de9e49cbef2d4b10ccce638ba7081c500`.
The working source is `C:/Users/Mike/Documents/New project/bof-repair-0927`.
The Overdrive art is also available separately at `C:/Users/Mike/Documents/New project/expansion`.
It contains Hotwire/Phoenix concepts, portraits and special-effect assets. The incoming expansion README states it is an art package for future integration. This pass does not integrate it into gameplay or include it in the base release ZIP.

## Repairs

- Retina: C retains the selected target on space stages instead of the scan controller replacing it with a nearer module. Directional multi-target marks persist across volleys while the lock key is held; they refresh their lifetime. Held missile fire repeats at a controlled cadence. Empty ammunition no longer generates a fail sound every frame.
- Stage 4: encounter scroll resumes over a short ramp, rather than jumping immediately to full speed. Ordinary kills have a much smaller camera impulse. Kill diagnostics show unchanged player position and zoom, continuous 40 px/s map advance and a gradual encounter release.
- Stage 5: space bomber core/module durability increased 80%; Hammer durability increased 70% over the incoming balance. The first attack cycles include whirlwind, including when health is pushed rapidly below half. Body damage no longer disarms a campaign whirlwind; strikes on the hammer still do. The chaingun arsenal now enters the existing Chromium restoration sequence, retaining its visible healing and interruptible core.
- Stage 6: initial Harrier-bay jets launch north, grow from 28 to 61 px high and roll out to the sides. New authored south-facing interceptor/bomber sprites replace six inconsistent aircraft idle hulls. They retain their authored gunmetal/red scheme; the frenzy palette still applies. After the miniboss and full wing formation, a large Harrier crosses diagonally left and five Rebel ships cross diagonally right. The central arrow prompt follows this flyover, allows 30 seconds and chooses a fallback if ignored. Final boss spawning waits for a choice and at least 15 seconds of the selected route.
- Bombing encounters: shorter mortar cycles, faster/more frequent siege bombs and missile lanes; Furious retains a safe lane. Space bomber bombs now use the same south-facing orientation as other bombers.
- Music: Stage 2 miniboss uses `unused5 - stage2mb-stage2b.mp3`; Stage 3 miniboss uses `unused6 - stage3b.mp3`. They decode successfully as separate stereo tracks, about 175 and 140 seconds respectively.

## Release

`C:/Users/Mike/Documents/New project/release_0927/BulletsOfFury-playable-2026-09-27.zip`

Extract the entire ZIP and run `PLAY_BULLETS_OF_FURY.bat`. The bundled PowerShell/.NET loopback server requires no Python installation. It supports concurrent requests and byte-range audio streaming. It binds only to localhost and rejects paths outside the extracted folder. The launcher opens the game; leave its window open while playing.

The ZIP is under **500,000,000 bytes**. Exact size and SHA-256 are in the adjacent `build-report.json`. Runtime assets are collected after all nine stage setups, including the lazily registered modular space ship. Source archives, development tools, recordings, unused music and the separate expansion are excluded.

Images retain their original dimensions. Fonts, icons and projectile art use lossless WebP. Large scenery/cinematic plates use quality 90; high-detail enemy/boss texture plates use quality 98. This is high-quality lossy compression on those selected textures, not a claim of pixel-identical output. Source PNGs and audio are unchanged. Runtime `.png` URL strings are rewritten only in the release copy.

Rebuild with:

```powershell
python _BUILD_SOURCE/collect_release_0927.py
python _BUILD_SOURCE/build_playable_0927.py
```

## Verification and limits

- `node --check` for the three edited engine modules; `git diff --check`.
- Full `_BUILD_SOURCE/test_fl.js` suite: 5,545 passing checks, final `FALVA/LIZZIE BUILD OK, 0 ERRORS` banner. An initial source-strip failure was caused by omitting `_ART_SOURCES/stage1_ai_fx/spaced_v2` from the sparse checkout; restoring that test dependency resolved it.
- Native Chromium release probe: selected locks survive repeat launches on stages 1â€“9, multi-target marks persist, Harrier jet movement is northbound, the post-miniboss route is reachable and does not spawn the final boss immediately, Stage 4 kill/scroll invariants hold, Hammer healing and counter routing work, and both music files decode. No page, console or HTTP errors. Captured frames were inspected. Fixtures are controlled diagnostics, not recorded campaign victories.
- Windows launcher returned HTTP 200 for the page and HTTP 206 with the correct Content-Range and 128-byte body for a music-range request.
- ZIP CRC and source/runtime game-script consistency checked after final packaging.
- Native aiming-bot damage windows (Cole space laser III, automatic missiles II, no manual missiles/elements/specials; immunity removes survival from this diagnostic): space miniboss about 34/43/53 seconds and Hammer about 79/113/152 seconds on Normal/Hard/Furious. Hammer reaches actual whirlwind and restoration in all three. These measurements do not prove subjective difficulty or a full campaign playthrough.

Probe commands and evidence:

```powershell
python _BUILD_SOURCE/probe_repair_0927.py ../release_0927/BulletsOfFury
python _BUILD_SOURCE/benchmark_encounters_0927.py siegebomber chromehammer
```

Reports/screenshots live in `_shots/repair_0927`; damage-window data is in `_shots/overnight_0927/damage-windows/report.json`. Focused native checks cover the repaired sequences, not every possible menu, pilot, save state or full campaign route.

## September 27 boat and space-weapon follow-up

- Removed the extra hull-centred volley layer from Stage 1 boats. Patrol turrets now launch three-shot spreads from the live modular turret muzzle; corvettes keep their authored alternating broadside fan and missile boats keep their rack launches.
- Overlord sonic-wave windup uses the shared FOV field, flashing asterisk and warning audio before wave release. The existing 2.1-second tell remains.
- Shadow Orb shows a graphical-font charge percentage and meter above the ship, with a minimum-charge marker and READY at full charge. Its charge and release use the shipped warp-charge/void-orb samples.
- Real death clears Akimbo, selects Laser Cannon level 0, resets Volley Missiles to base level 1 and cancels Shadow Orb charging. Shield absorption does not trigger this reset.
- Native Chromium follow-up probe: `_BUILD_SOURCE/probe_space_boats_0927.py`, including Stage 5 and 9, decoded audio, turret origins, warning-before-release and death equipment state. Screenshots/reports are under `_shots/repair_0927`.

## Cole4u session unlock

Entering Cole4u remains valid across new campaign runs, deaths/game over and loading older campaign checkpoints until the game closes. Campaign snapshots still save the unlock. A new game process starts locked, and loading a campaign carrying Cole restores him; another save without Cole stays locked unless the password was entered in that session. Native Chromium regression: `_BUILD_SOURCE/probe_cole_session_0927.py`.

## Boss warning follow-up

Upgraded Stage 2â€“4 attacks now announce their real turret fans, rocket racks, radial volleys and centre emitters through the shared FOV system. Warning audio is enabled on these attacks, helper guns and incoming missile lanes. Destroyed modules no longer announce attacks. Rime Wall/Glacier Press commit their escape opening for the whole barrage. Travelling burst orbs announce their split, and the Siege Bomber's laser windup uses the warning sound clock.

Stage 7 tank orb spreads and Warden bounce impacts now show warning fields and alerts. Shield retaliation queues a committed 1.05-second tell before firing; shield destruction, stun or death cancels it. Existing Stage 5/6/8/9 attack-specific warning systems remain in use.

Native regression: `_BUILD_SOURCE/probe_boss_warnings_0927.py`, covering the upgraded Stage 2â€“4 attack books, Stage 7 gun/orb/laser/melee/bounce tells and counter release timing. The full regression suite also checks delayed shield retaliation.

## Fleet generation

Built-in `image_gen` produced the shared south-facing fleet source. Saved runtime sprites:

- `assets/game/stage6_fleet_0927/interceptor.png`
- `assets/game/stage6_fleet_0927/bomber.png`

The source, full generation prompt and reproducible alpha-crop/nearest-neighbor import are in `_BUILD_SOURCE/stage6_fleet_0927/`. No hull rotations or artificial recoloring were baked into these idle sprites.

## Stage 6 stealth fly-in

The opening now enters the same live sky and ship renderer as gameplay. The pilot glides in during the first dialogue, with movement locked until the fighters reveal and both HUD canvases fading in over 2.4 seconds. Cole’s warning starts the lock alert and rapid Retina beeps; a targeting Retina descends from the sky onto the pilot before Maverick’s cloaking question. Fighters uncloak, pass north continuously and launch upward-facing missiles which curl back toward the player under the real lock system. Rolls/somersaults still break the lock. Gun, beam and Retina interceptions use the existing authored explosion, shock ring, smoke and debris pipeline. The twelve-jet carrier pass remains intact.

Native regression: `_BUILD_SOURCE/probe_stage6_opening_0927.py`, including continuous rendered scrolling, fly-in pose steps, dialogue order, warning audio calls, upward launch and live curving trajectories, and intercepted-missile effects. Audio timing is measured by calls to the shipped SFX; this does not substitute for listening on the user’s speakers.
