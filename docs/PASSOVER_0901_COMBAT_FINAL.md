# Bullets of Fury — Combat Final Passover (2026-09-01)

This pass upgrades the shared boss/miniboss damage presentation and completes the requested Stage 5–7 encounter work. It does not push or merge the repository.

## Implemented

### Shared encounter rules

- Bosses and minibosses emit authored smoke and rupture overlays below 50% health.
- Below 25% health, the damage presentation escalates with a third vent and periodic explosive ruptures.
- The overlay is drawn over the live unit; defeated encounters do not fade into generic canvas-circle effects.
- Existing all-stage unit separation remains active, including category-aware plane, boat, and ground-unit spacing.

### Stage 5 — Xeno Regent and warp route

- Warp-gate x positions now follow the supplied alternating route sketch: `28%, 54%, 76%, 23%, 54%, 29%, 69%, 18%` of the 680-wide playfield.
- Gates remain one connected continuous scroll; a dashed navigation line exposes the intended route.
- Alien carrier attack reels now select their full authored animation range instead of remaining on frame zero.
- Carrier lances, split darts, chaos charges, halo shots, mines, and impacts now use the new dedicated projectile atlas.

### Stage 6 — Doomsday Carrier MkII

- The giant shield starts with three reflected-warhead hits and absorbs ordinary player fire.
- Only a reflected giant missile can remove a shield hit. Each hit produces an electrical shield-impact effect.
- Breaking the shield opens a 30-second bay-destruction window.
- During that window, each surviving bay has its own health and can be destroyed independently.
- If either bay remains after 30 seconds, the shield reforms at full strength around the surviving launcher configuration.
- A reflected missile can inflict a large bonus hit on an exposed bay.
- The carrier core remains protected until both bays are destroyed.
- The cannon hull reel is cropped to the launcher assembly; the existing separate beam atlas is now the sole animated laser beam.
- A local encounter readout displays reflected shield hits, the bay timer, and both bay health values.

### Stage 7 — Toxic Portal Warden

- The former Stage 7 boss slot now presents **TOXIC PORTAL WARDEN** while preserving the internal runtime ID for save/stage compatibility.
- New grounded mechanical-walker art includes a true leg gait driven by horizontal travel rather than hover or side-to-side wobble.
- The gait is an articulated eight-pose crawl: four legs alternate recovery and planted power strokes, with forward movement weighted to each foot plant and only a small vertical suspension compression under load.
- Crawl targets extend far enough into the sewer walls for a genuine edge-to-edge traverse; teleport arrivals still use fully visible safe anchors.
- The original generated crawl poses were replaced after motion review because their leg silhouettes changed too sharply between frames. The runtime now uses SpriteCook asset `7e8870d9-7875-4197-8b71-82b22a7d83b0`, an eight-frame horizontal strip with a locked chassis and consistent articulated leg geometry.
- The Warden was reduced from `338×258` to `300×230` so the complete gait remains readable inside the central sewer lane.
- Its burst, minefield, and rail states now select dedicated SpriteCook body reels. Burst uses alternating cannon recoil; minefield and rail use a contained reactor-charge sequence with no baked projectile or beam.
- Its pressure shell, portal mine, and rift-rail spear are separate clean SpriteCook assets and separate runtime projectile kinds. The rail spear is faster and taller than the standard pressure shell.
- Portal mines fan outward, phase-lock into distinct target lanes, remain destructible, and expire after 4.8 seconds so formations cannot accumulate indefinitely.
- Its controller has five committed states: slow patrol, fast aimed cannon burst, destructible minefield, toxic rail/fan, and opposite-side teleport.
- Teleport invulnerability exists only during the displaced middle phase; the generated exit/entry shell is rendered directly with the boss.
- The existing miniboss gains a late-health portal-mine formation with a deliberate player escape lane.
- The stage-end gate is now a cyan/cobalt/hot-magenta helix rift seated inside the authored sewer portal rim. An opaque black-violet rift seal completely occludes the old green slime inside the rim throughout the finale. The helix expands to the aperture's exact circular mask, closes, and reforms for the escape.
- The Warden's teleport reel expands inside that same masked aperture—there is no second floating teleport circle—and the walker scales and travels out from its center before walking forward on the articulated gait, rearing up, and performing its mechanical roar.
- The fight reverses the same continuous Stage 7 master scroll while the Warden advances; it does not cut or teleport the player into another section.
- At 75% health the Warden is knocked back and stunned. Its two toxic canister cores become independently targetable, gain explicit bright hit rings, and take critical damage during the vulnerability window.
- At 50% health a bottom-to-top white pixel scan introduces the cyan/magenta Hyper palette and faster attack cadence.
- At 25% health any surviving cores are force-broken, the rear assembly detonates in a readable one-by-one chain, and the Warden switches to a damaged front-leg crawl with frantic single and dual rail fire.
- At zero health the chassis remains present as an intact wreck. Pilot dialogue calls the escape, the helix gate reopens, the player ship flies into it, and limb/internal explosions build into a full-screen explosion chase and whiteout.
- Campaign completion unlocks Stage 8 and returns to the campaign map. Selecting the newly unlocked stage starts directly on white, opens the matching helix rift over the live Stage 8 background, ejects the correct pilot ship, plays the reader warnings, and then runs a non-overlapping `3…2…1…GO!` countdown.

## New production assets

- `assets/game/combat_final/stage5_xeno_projectiles_atlas.png`
- `assets/game/combat_final/stage6_carrier_shield_atlas.png`
- `assets/game/combat_final/stage7_toxic_portal_warden_walk_atlas.png`
- `assets/game/combat_final/stage7_toxic_portal_warden_crawl_spritecook.png` (active crawl strip)
- `assets/game/combat_final/stage7_warden_cannon_barrage_spritecook.png`
- `assets/game/combat_final/stage7_warden_rail_charge_spritecook.png`
- `assets/game/combat_final/stage7_warden_toxic_pressure_shell_spritecook.png`
- `assets/game/combat_final/stage7_warden_portal_mine_spritecook.png`
- `assets/game/combat_final/stage7_warden_rift_rail_spear_spritecook.png`
- `assets/game/combat_final/stage7_toxic_portal_teleport_atlas.png`
- `assets/game/combat_final/stage7_toxic_portal_projectiles_atlas.png`
- `assets/game/combat_final/stage7_warden_rear_roar_spritecook.png`
- `assets/game/combat_final/stage7_warden_crippled_crawl_spritecook.png`
- `assets/game/combat_final/stage7_warden_last_stand_spritecook.png`

The bitmap sheets were generated with GPT image generation, then normalized with `_BUILD_SOURCE/combat_final_0901/normalize_generated_atlases.py`. The cleanup converts flattened checker backgrounds to alpha while preserving enclosed white energy cores and removes pale matte fragments around articulated legs.

## Verification

- `node --check assets/game.js` — passes.
- `_BUILD_SOURCE/qa_combat_final_0901.js` — passes in the production browser page with Lizzie.
- All five new atlases report loaded and ready.
- Stage 6 proof: shield hit count decreases only from a reflected warhead; exposed bay HP changes from `320` to `205`; the shield remains down with approximately 29 seconds on the window.
- Browser console errors: none.
- Missing assets: none.
- `_BUILD_SOURCE/qa_stage7_finale_helix_0901.js` — passes the full phase/handoff proof: both exposed cores are destroyed, Stage 8 unlocks, campaign returns to `stagesel`, the pending rift handoff is consumed, and Stage 8 reaches live play.
- Stage 7/8 finale proof: no browser errors, no missing requests, all six Warden/teleport assets ready. Screenshots and Lizzie footage are under `docs/proofs/stage7_finale_helix_0901/`.

Proofs and footage are under `docs/proofs/combat_final_0901/`.

The broad legacy test runner currently ends with 65 failures. These include older assertions that explicitly expect the removed `SLUDGE EMPEROR`, the old baked Stage 6 beam presentation, and the old reflected-only exposed-bay rule, plus unrelated existing baseline failures. The focused production-browser combat proof is green; the legacy expectations should be reconciled separately rather than used to revert the new requested behavior.
