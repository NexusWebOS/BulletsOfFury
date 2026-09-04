# Bullets of Fury - Cutscene Wiring and Full-Game Playtest Passover

Date: 2026-09-02

## Delivered in this pass

- Registered the dedicated `07_center_rear.png` cinematic aircraft for all nine pilots.
- Routed the centered rear aircraft into HQ approaches, jungle approaches, departure traffic, and the pilot-specific ending ascent.
- Kept two-pilot approach formations separated while they scale into the shot.
- Prewarms the final ending during the last campaign results screen.
- Holds the ending timeline until its HQ plate, selected aircraft, sequel plates, and dialogue font are ready. Dialogue can no longer begin over an undecoded blank backdrop.
- Extended the ending QA to pin the seventh view, straight flight, approach separation, prewarm, and readiness gate.

## Test scope

The production browser page was run in real Chromium with Lizzie as the observation pilot. The pass included:

- Stage 1-9 visual combat smoke captures.
- Stage 1 jet formation and tank brake/fire behavior.
- Stage 2 Inferno Reaver shield, pause/resume, Laser Mist, Stage 9 failure return, and reward unlock.
- Stage 3 and Stage 4 live waves.
- Stage 5 Xeno Regent shield/fairness and stage-resource timing.
- Stage 6 live wave and Doomsday Carrier bay-window mechanics.
- Stage 7 Warden cores, stun, hyper phase, cripple, escape, and Stage 8 helix-rift handoff.
- Stage 8 live wave.
- Stage 9 opening wave, specialist roster, destructible water rocks, fusion twins, and Tidal Sovereign cascade.
- Ground/space death weapon reset and passive volley missile behavior.
- Campaign prologue skip/routing and all nine pilot opening branches.
- Ending readiness and centered rear-flight proof.

This was an invulnerable visual/mechanical observation pass, not a score-attack balance run. Chromium was muted, so sound files and trigger paths were exercised but mix, loudness, fatigue, and timing by ear still need a live listening pass.

## Verified passes

- All nine pilot openings start the correct branch, select the correct cast/destination, fit their dialogue windows, use the dialogue font, and report no missing assets or runtime errors.
- Ending static QA passes 64 checks.
- Campaign prologue routes and skips correctly.
- Pause applies grayscale and lowers music, then restores both.
- Death resets all ground and space weapon tiers to Level 1 without deleting the equipped weapon identity.
- Stage 2 boss shield/body ownership and attack cancellation on shield break pass.
- Stage 5 boss can be killed; the mother shield takes damage without body bleed-through.
- Stage 6 reflected-warhead shield break and exposed bay damage window work.
- Stage 7 cores, stun, hyper/cripple escalation, escape, and Stage 8 entry pass.
- Stage 9 Tidal Cascade exposes a two-lane safe door, moves it by one lane, and releases the expected projectile row.
- Stage 9 water-rock spawn/break scenario completes without a runtime error.

## Findings, highest priority first

### P1 - Stage loading and frame pacing are the release blocker

Reproduction: run the Stage 5 boss/loading browser proof on a cold page.

- 28 Stage 5 roots took **50.865 seconds** to report ready.
- The combat render sample measured **100 ms median** and **133.3 ms p95** frame time.
- Two other stage-art suites timed out at 10 and 30 seconds while waiting for required art.
- The current asset tree is **4,853 files / 1,148 MB**. The largest groups are `atlas` (356 MB), `generated_cinematic` (175.2 MB / 1,355 files), and `cinematic_campaign` (88.5 MB).
- The runtime loader is deliberately capped at three concurrent roots. Large multi-megabyte atlases are still decoded during transitions.

Player impact: long pre-stage waits, visible asset pop-in if a path bypasses a loading gate, and slow-motion combat on the target laptop.

Likely owner: asset packaging plus stage-loader scheduling.

Recommended change:

1. Establish a hard per-stage compressed/decode budget.
2. Remove raw generation/source duplicates from the shipping tree and keep them in `_BUILD_SOURCE` or archival storage.
3. Audit boot ownership: the page currently requests every pilot portrait family, warp reels, and the full music bank before the selected stage is known.
4. Split the largest 6-14 MB atlases by actual stage use and preload the next stage during results/campaign-map time.
5. Benchmark loader concurrency at 4-6 roots on the laptop; keep the value adaptive rather than globally fixed at three.

Evidence: `docs/proofs/stage5_boss_loading_0901/report.json`.

### P1 - Stage 8 composition is visually overloaded and violates unit spacing

Reproduction: start Stage 8, let the opening wave run for roughly eight gameplay seconds.

Multiple shielded ships, a large central hostile, and the terrain-scale symbiote mass occupy the same central lane. Several silhouettes overlap, one unit is clipped at the top, and the player sits against the lower edge of the mass.

Player impact: hostile identities and attack origins cannot be read; collision ownership becomes ambiguous.

Likely owner: Stage 8 wave layout, enemy separation bounds, and large-unit safe margins.

Recommended change: give large/mega units lane reservations based on visual alpha bounds, cap small escorts around them, and prevent any non-boss unit from occupying the player's bottom safe band.

Evidence: `docs/proofs/playtest_0902/stage8/shot_0003.png`.

### P1 - Stage 9 still ships visibly procedural orange X projectiles

Reproduction: run `_BUILD_SOURCE/scenario_stage9_void_roster.js` for approximately three seconds.

The orange/pink X projectiles are clear to dodge, but they read as debug geometry beside the finished violet/green ships, shield art, and Tidal Sovereign arsenal. The runtime confirms Stage 9 standard families still route through `procSpace` drawings.

Player impact: Stage 9 loses its premium final/bonus-stage finish at the exact moment its combat should look best.

Likely owner: hostile projectile art/runtime atlas.

Recommended change: replace `s9gold`, `s9warp`, `s9turbo`, `s9needle`, `s9comet`, and `s9pair` procedural routes with padded authored animation cells and matching impacts. Keep procedural geometry only as a debug fallback.

Evidence: `docs/proofs/playtest_0902/stage9_roster/shot_0006.png`.

### P1 - Stage 9 fusion twins are not framed as a two-boss encounter

Reproduction: run `_BUILD_SOURCE/scenario_stage9_fusion.js` and inspect the first ten seconds.

The left twin remains partially outside the viewport while the right twin owns the readable center. Grey terrestrial smoke also covers both hulls.

Player impact: one boss feels missing/cut off and its attack origin is harder to learn.

Likely owner: fusion boss formation and boss-damage overlay system.

Recommended change: clamp each twin's visual bounds to a 10% viewport gutter, reserve symmetrical anchors until the actual merge, and use void-water damage overlays rather than generic grey smoke.

Evidence: `docs/proofs/playtest_0902/stage9_fusion/shot_0010.png`.

### P2 - Stage 9 opening formations become a wall of overlapping units

Reproduction: run Stage 9's opening wave for 10-16 seconds.

Ring drones, towers, tanks, pickups, and a very large rift-rock obstacle share the upper half. Some units are only partly visible at the right edge; the large obstacle can dominate the playable width.

Player impact: individual patterns and collectible priorities become difficult to parse.

Likely owner: Stage 9 wave director and enemy/pickup occupancy rules.

Recommended change: stagger each role by depth band, cap one large obstacle per screen, enforce pickup separation, and reserve 25-30% of the playfield as an always-readable maneuver corridor.

Evidence: `docs/proofs/playtest_0902/stage9_opening/shot_0013.png`.

### P2 - Stage 3 aircraft enter too large and clip before their formation reads

Reproduction: start Stage 3 and observe the first eight seconds.

The authored ice aircraft look good, but the largest units approach at near-boss scale; left and right entries are partly clipped and their arrangement competes with the background islands. The damage smoke is also the same generic grey used elsewhere.

Player impact: the opening is dramatic but less readable than Stage 1 and Stage 6.

Likely owner: Stage 3 wave scale/entry anchors and engine-wide damage overlays.

Evidence: `docs/proofs/playtest_0902/stage3/shot_0003.png`.

### P2 - The Stage 2 support-wave fire assertion is consistently late/empty

Reproduction: run `_BUILD_SOURCE/qa_ai_curve_0901.js` in isolation. The sampled Stage 2 ash/cinder squad produced zero bullets in both runs at the established 1.5-second observation point.

This does not prove the units never fire; the live Stage 3/4/6/8 captures do show hostile bullets. It does show that the intended early pressure contract is no longer deterministic.

Player impact: early Stage 2 may feel softer or less responsive than its configured difficulty curve suggests.

Likely owner: Stage 2 entry delay/fire cadence and the QA timing contract.

Recommended change: decide the intended first-shot deadline, then make the wave and test share that explicit contract rather than relying on random cooldown timing.

Evidence: `docs/proofs/ai_curve_0901/report.json`.

### P2 - Damage overlays need stage ownership

Generic grey smoke and occasional ordinary orange fire remain visible on void-water/alien bosses. The same overlay language is acceptable on Stage 1-4 machinery but clashes with Stage 8-9 materials.

Recommended change: make the engine damage-overlay rule select a stage/material family: mechanical smoke, cryo vapor, magma venting, toxic fumes, symbiote ooze, and void-water mist/electrical breakup.

## What should be removed or consolidated

- Procedural production projectile fallbacks for Stages 2, 5, 7, 8, and 9 once their authored atlases are complete.
- Loose duplicate runtime frames that are already represented in an atlas.
- Unreferenced generated cinematic variants from the shipping asset directory.
- Terrestrial grey-smoke/orange-fire overlays on Stage 8-9 enemies and bosses.

## What should be added

- An automated visual-occupancy check that fails a wave when two live enemy alpha bounds overlap by more than 35% for multiple frames.
- An off-screen boss check that fails when more than 10% of a boss visual bound remains outside the viewport after entry.
- Per-stage asset budgets and cold-load benchmarks in QA.
- A final real-speaker/headphone mix pass for alerts, rapid-fire weapons, boss loops, and the ending mechanical scream.
- Stage-specific projectile/impact atlas completeness checks so procedural fallback art cannot silently return.

## Recommended next order

1. Asset/load budget and laptop frame pacing.
2. Stage 8 and Stage 9 overlap/off-screen composition.
3. Replace Stage 9 procedural X projectile family.
4. Reframe fusion twins and retheme their damage overlays.
5. Stage 3 entry scale plus Stage 2 deterministic first-shot cadence.
6. Live audio mix pass.

## Proof locations

- Rear-view contact sheet: `docs/proofs/ending_cinematic_0902_center_rear/center_rear_9pilot_contact.png`
- Corrected Freezer/Axel approach: `docs/proofs/pilot_openings_0901/action_08_freezer_jungle_approach.png`
- Ending rear ascent after readiness gate: `docs/proofs/playtest_0902/ending_center_rear_ready/`
- Stage 3/4/6/8 smoke captures: `docs/proofs/playtest_0902/stage3/`, `stage4/`, `stage6/`, `stage8/`
- Stage 9 opening/roster/fusion/water-rock captures: `docs/proofs/playtest_0902/stage9_opening/`, `stage9_roster/`, `stage9_fusion/`, `stage9_waterrock/`
- Stage 9 final-boss cascade: `docs/proofs/shmup_reference_0831/05_stage9_tidal_cascade_tell.png` and `06_stage9_tidal_cascade_release.png`
