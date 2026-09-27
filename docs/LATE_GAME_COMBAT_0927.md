# September 27 combat pass

Stage 7 already had a Dredger miniboss and a Portal Warden, including its entrance and ending. This pass keeps those identities and replaces their live combat sequencing. Stage 9 uses the existing authored Horizon, Sentinel and Sovereign hulls. No raster generation or atlas repacking was needed.

## What changed

- **Stage 7 Dredger:** alternating cannon crossfire, a committed scoop rush with the actual impact circle shown from the start, toxic spore rings with an opening, and shootable mine gates. Mines fly continuously from their mounts into position rather than snapping there. Normal leaves a wider gate; Hard/Furious tighten tempo and openings. A killed miniboss cannot complete a queued landing hit.
- **Stage 7 Warden:** planted-leg stalking, warned leaps, alternating cannon bursts, rail spreads, and mine placement with recovery between attacks. Below half health, the rotation includes extra leaps and chain fire. The portal arrival/chase, 75% exposed-core stun, 50% hyper transition, 25% leg destruction/cripple attack, defeat and escape remain owned by the existing encounter. Interrupted leap markers are cancelled.
- **Stage 9 Horizon:** needle relay, prism gates, orbiting volleys with a committed escape opening, and crystal-lance sweeps. Its existing black damaged hull and core hit routing remain.
- **Stage 9 boss:** Sentinels release in alternating turns. Once both are defeated the existing intact fusion plays, followed by the Sovereign's crossing cutters, shootable accelerating torpedoes, lane gates, crown rings and broad sweeps. Launch angles are committed before release. Authored cached-canvas projectiles now use real image dimensions instead of assuming naturalWidth exists. New energy ordnance does not inherit the oversized chemical-rocket smoke trail.
- **Field enemies:** shared visibility grace, brief damage flinches that interrupt a release, and predictive lateral avoidance with a readable reaction delay and cooldown. Neighbor/edge checks prevent a dodge into a crowded lane. Existing special routes and ground anchors retain ownership. Boss scripts are not globally replaced by this field layer. Direct drone fire is included in the release gate.
- **Missing drones:** the native drone constructor now initializes sine-flight amplitude even for reinforcements. Previously Cinderwasp and Sharddart reinforcements could get NaN x positions when their movement controller selected that path.
- **Stage 6:** allies reduce field pressure instead of multiplying it. Extra reinforcement traffic waits for a quiet field. Friendly guns fire less often and heavy weapons share a 0.70-second release window. Allies cannot fire through an active evasion. Rolls last 0.46 seconds followed by 5 seconds of recharge; somersaults last 0.62 seconds followed by 7 seconds, matching player constants. These are independent cooldowns, with no overlapping maneuvers.
- **Stage 6 Rival squad:** coordinated attack turns, a 0.90-second committed dash lane using the shared warning sign/cone, longer roll recharge, and stun clocks that decrement rather than being erased. The dash no longer also triggers an unrelated lightning strike. Existing Tempest/Harrier/Carrier authored encounter designs remain.

## Ownership

`assets/combat_ai_0927.js` owns field reactions, wing recharge and release scheduling. `assets/late_encounters_0927.js` owns the new late encounter books. `index.html` loads both after the existing encounter/muzzle scripts. Narrow hooks in `assets/game.js` preserve damage, story, rewards, endings, custom editor scenes and authored rendering.

The enemy loop restores its firing context through a finally block, including early returns/continues. Offscreen field suppression cannot spill into boss releases or detached midair splits. Main game LF and test harness CRLF are retained.

## Verification

Final full suite: **5,190 passed, 0 failed**, exit 0, with the final `FALVA/LIZZIE BUILD OK` banner. Immediate baseline was 5,159/0; no new failing names. Syntax checks passed for game.js and both new modules. The first development suite stopped on a duplicate local variable in the new test file; this was repaired, not counted as a passing run.

Native Chromium evidence:

- Twelve 75-second encounter fixtures: four encounter types across Normal, Hard and Furious. All new attack modes were reached; Warden core/hyper/cripple gates and Sentinel fusion were exercised. No nonfinite projectiles, page errors or console errors.
- Rendered field traffic on all nine stages, covering **75 field enemy types**. No invalid enemy coordinates after the constructor repair; no stationary-player position jumps. The first diagnostic pass caught the missing amplitude on two reinforcement types.
- Actual predictive dodge displacement: 31.5 / 38.1 / 44.7 pixels on Normal / Hard / Furious, with delayed starts and visible hit-reaction state.
- Native space missiles damaged the Horizon (1936 → 1903), a Sentinel (4420 → 4398), and the fused Sovereign (4400 → 4367). Separate regression checks passed for manual ground missiles, space lock acquisition and stationary turret bases with rotating heads.
- Warden defeat completed its escape and reached the arcade results state. Mine placement's maximum sampled frame step was 4.54 pixels, ending exactly on the anchor.
- Ten Stage 9 projectile families rendered through the game context with finite draw dimensions; the toxic spore art was also rendered and inspected.
- Five real-time canvas recordings with keyboard flight, plus refreshed Dredger/Sovereign/Warden clips after final visual changes. These fixtures use invulnerability and forced health gates for inspection, not campaign-win evidence.

The seeded 38-second Stage 6 field comparison with eight allies measured these peak hostile bullet counts:

| Difficulty | Before | After |
| --- | ---: | ---: |
| Normal | 35 | 26 |
| Hard | 42 | 34 |
| Furious | 61 | 48 |

Peak allied bullet counts and evasion counts also declined; see the JSON report. These are controlled windows, not predicted player clear rates. Full mortal controller playthroughs are still needed to judge final difficulty and sustained campaign flow.

## Review and reproduction

- Local review: `_shots/late_game_0927/review.html`
- Durable results: `docs/qa/late_game_combat_0927.json`
- Native matrix: `_BUILD_SOURCE/probe_late_game_0927.py`
- Field comparison: `_BUILD_SOURCE/probe_field_ai_0927.py` (the before comparison uses the saved ignored `_shots/late_game_0927/game-before.js`)
- Damage/behavior/art contracts: `_BUILD_SOURCE/probe_combat_contracts_0927.py`
- Clips: `_BUILD_SOURCE/record_late_game_0927.py`
- Assertions: `_BUILD_SOURCE/test_late_game_0927.cjs`, loaded at the end of the full suite; the native probes exercise the fully loaded browser build.

Existing staged, unstaged and untracked work was preserved. Nothing was committed or pushed.
