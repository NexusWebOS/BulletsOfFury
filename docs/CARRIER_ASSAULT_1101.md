# Stage6 carrier assault / November1

Mike requested two paired-carrier action sequences, with one approach from the top and another from below. Both hulls must stay protected until all their turrets are destroyed. Passing over the carriers must be harmless and cast aircraft shadows onto the decks. He then requested a massive nuclear-warhead carrier and a different massive laser-warhead carrier, including new effects and timed hazards. His later visual correction asks for larger hulls and guns, staggered slow arrivals, engine shaking, stronger exhaust animation and removal of floating HP bars.

## Current owners and art

`assets/cloud_carrier_1101.js` / `CC111` own the paired hulls and five circular gun modules per hull. The later `assets/carrier_assault_1101.js` / `CA111` owns the four-wave campaign sequence, two new strategic carriers, physical warheads and generated hazards. These registries remain separate from the existing Siege Console `SC12` and shared audio `CA15` registries.

The paired hulls retain their original authored identity. `_BUILD_SOURCE/build_cloud_carrier_1101.py` exports north/south whole plates from the same source pixels, preserving512x1024 cells and the same measured deck wells. Current world height is470, approximately38% taller than the first340-unit pass. Cannon cells remain192 square/32 headings; world size rises from48 to68, approximately42% larger. Their native hit rectangles grow to44 square to match the visible45.3-unit circular rims.

`_BUILD_SOURCE/build_carrier_assault_1101.py` owns ten newly generated built-in image_gen originals, copied verbatim under `_BUILD_SOURCE/carrier_assault_1101/`. Original filenames, tool attribution, SHA256 values, crop rectangles, shared scales and physical pivots are retained in `assets/game/levels/stage_06/enemies/carrier_assault_1101/manifest.json`. The builder writes13 banks plus `assets/carrier_assault_art_1101.js`:

- Two distinctly shaped512x512 whole carrier hulls: a navy/gunmetal nuclear silo fortress with amber warning rails, and a swept-prong black/chrome laser carrier with cyan cores. Neither hull uses generated whole-body attack animation.
- Eight authored mechanical launch-door poses for each carrier, with fixed rims, common pivots and proportional canvases:256x512 nuclear shutter cells and256x256 laser-iris cells.
- Eight axial-roll poses per new heavy warhead, normalized to256x256. Nuclear flight has32 registered heading cells; the southbound laser body has8. Nuclear rise, apex rotation and descent select these real cells, with measured tails and first-frame geometry matching the following native update. The nuclear body follows its actual velocity; lateral catch-up steering eases as it approaches its committed lane. Laser warheads launch from two measured offsets inside the same circular aperture and travel south rather than strafing sideways.
- Eight strong blue-white exhaust poses, with a fixed measured root and an alpha-preserving amber derivative. These new plumes replace the weak paired-carrier exhaust and also serve the new giant carriers and warheads. Each outlet uses an independent phase at26 source-frame steps per second.
- Eight newly generated nuclear shockwave frames. The blast grows within its fixed canvas, then breaks into authored fragments. Its visible80th-percentile hot radius grows from15.65 to95.68 source pixels; the gameplay effect uses a fixed460-unit canvas. There is no HTML/CSS fade or scale-based substitute for the expansion.
- Twelve newly generated laser-tornado frames, including growth, a cyclic full vortex and pixel breakup, plus eight new animated blue-white laser shaft segments with registered directional cells.

The native player craft is not regenerated. Its current authored directional frame supplies a black alpha silhouette, clipped against the actual carrier hull. This projection is drawn over receiving deck/door/gun surfaces, below weapon light, and below the actual player aircraft. Both seats use their own real craft frames. There are no procedural ship/shadow sprites and no live rotation of a static hull.

## Paired action sequences

Pairs enter slowly along both cloud edges,1.8s apart. The top-entry pair uses the south-facing whole plate; the lower-entry pair uses the north-facing whole plate. Root movement, gun sockets, physical targets and warnings share the same measured transforms. Engine vibration is a small coherent translation of the whole assembly, increased while a gun recoils. Existing1015 source-pixel light remains. Floating HP bars are removed.

All ten native gun actors must be destroyed before either hull target enters the native collision/Retina list. The protected hull objects retain their complete health pools while absent from targeting; a direct protected hit can still flash the armor without reducing its budget. Destroying only one carrier's five guns cannot expose that hull early. Once both batteries are exhausted, exactly two native hull targets appear and the authored shared SHOOT! objective identifies them. No full-health invisible parent duplicates the live component budget.

Each gun has `EHP(38)*4`, and each hull has `EHP(110)*5`. This is950 total for the verified low-arsenal Furious QA fixture; adaptive native pressure yields1100 in the level5 recording loadout. These are actual live pools, not recording substitutions. A complete pair gives two native kills and two8000-point rewards. Gun breaks stop that gun's beam immediately. Every gun and exposed hull retains native visible white hit feedback and expiry.

All paired components and hulls have `_noBodyContact`. Aircraft can fly across the decks safely; only the warned weapons can hit them. Unlike the first pass, the pair does not disappear after a23s timeout. It remains an actual turret-then-hull objective.

## Strategic carriers and warheads

The nuclear and laser carriers are different large solid hulls, approximately470/460 world units square, each with one real native hull pool of `EHP(180)*32` and one native16000-point complete defeat. Both are safe deck-overflight surfaces and have no added floating HP bar. Launch doors open, charge and release through the shared native player-lock Retina/beep owner. Carrier defeat cancels its pending locks and callbacks. Already launched physical warheads own their finite flight/fuse independently; the wave waits for them and their hazards to resolve.

Nuclear warheads rise, shrink with depth, visibly turn through registered frames at the apex, then descend and grow as they catch up. Descent steering eases toward a committed lane; the final1.5s uses a fixed impact Retina and a readable side-mounted fuse counter. A missed warhead releases the new expanding nuclear shockwave.

Laser warheads travel south with axial casing animation. Four measured visible lens pairs supply eight registered rays. Each burst commits a0.72s warning, fires for0.40s and has finite recovery. Beam reach increases with warhead age and is fixed during each committed burst. In the final1.6s, beams stop and the impact Retina/fuse counter commits the upcoming tornado. The tornado grows, loops its authored full-volume frames and breaks into source-pixel fragments.

Both warheads have physical `*Warhead` kinds from their birth frame. Their offensive hit route explicitly uses `enemyOrdnanceCanIntercept`; ordinary bullets retain the engine-wide prohibition. Warheads remain real native shootable/Retina actors with their own HP. Successful interception produces a small harmless authored break effect instead of the dangerous timed detonation. Nuclear warheads use `EHP(65)*3`; laser warheads use `EHP(65)*2`.

Warhead collision is in front of the deck. A scoped native primary-round hook lets a shot in the visible warhead's lane reach that missile instead of being swallowed by the larger carrier below it. Warheads paint after their parents. No unrelated aircraft or projectile is reordered. Physical contact becomes dangerous when the nuclear missile returns to the player's plane or the laser missile leaves its launch phase; carrier contact remains harmless.

Generated blast/tornado contact is measured from the current authored frame's actual opaque hot pixels, sampled around each native player hit point. Empty space remains safe. Native `playerHit` owns shields, rolls, somersaults, invulnerability and death. Supplementary harmless carrier death effects remain attached to the native once-only death/reward owner; they do not replace it.

## Campaign integration and audio

The four added stage-plan callbacks are18s `pair-top`,35s `pair-bottom`,51s `nuclear`, and66s `laser`. Each callback queues once, including co-op's repeated dispatch route. While an assault is active, native stage progress and ordinary dispatch pause; attack, input, projectile, weather and effect clocks continue. The normal Stage6 boss warning additionally requires all four actual completion keys. Thus these sequences extend the level instead of being skipped by the original75s end gate.

Existing boss/miniboss warnings, active encounters and protected story scenes keep a queued assault from starting. Native CP22 crossing pressure cannot start a new wave during the assault. Existing wind units, helper identities, the opening stealth sequence, the two Tempest ships and the Carrier/Nightwing boss remain separate owners. StageX is excluded. Stage changes clear controllers, pending pairs, locks, hazards and all holds.

The only core-engine changes are the explicit owned-actor update branch, native progress/dispatch/boss gates and scoped warhead-over-deck primary-contact hook. No player weapon progression, save ledger or boss pools are changed.

Approved audio uses the shared mixer/retrigger gates: `combatServo0927`, `bossWeaponCharge`, `atomicLaunch`, `nuclearDetonate`, `enemyHeavyLaser`, `combatEnergy0927`, `combatModule0927`, plus native Retina warning cues and native full-death feedback. One launcher/burst speaks once; eight parallel rays do not trigger eight duplicate release sounds. There are no detached timeout-based attack/audio callbacks.

## Verification and current review

- `_BUILD_SOURCE/probe_carrier_assault_1101.py`:39/39 focused real Chromium checks. These include warning interlock, full paired budget/target gate, actual travelling rounds, actual deck-shadow pixels, safe direct overflight, native damaged pixels and expiry, physical-warhead shared interception, both timed hazards, growing beam reach, exact hot-pixel damage, native player death, launcher cleanup and stage cleanup. Screenshots and JSON evidence live under `_shots/carrier_assault_1101/`.
- `_BUILD_SOURCE/probe_carrier_campaign_1101.py`:4/4 integration checks. All four real stage-plan callbacks execute in order and are defeated with native movement/fire inputs, four paired hulls plus two strategic hulls receive real native defeats, and progression/boss gates release. Regular pressure/crew are isolated in this QA fixture; no enemy HP/phase/attack-clock writes are used.
- `_BUILD_SOURCE/probe_stage6_airframe_1101.py`:66/66 preserved-aircraft checks, including stable hulls, existing native flight, hit pixels/expiry, exhausts, sky turret exclusion and original stealth entrance preservation.
- All13 new bank dimensions match their registered even cells. All ten raw generated originals remain available. `assets/game.js` retains LF line endings; syntax checks pass. The full `node _BUILD_SOURCE/test_fl.js` still exits1 before assertions/final summary because ignored `UNUSED_ASSETS/retired_art_1022/manifest.json` is missing, matching the recorded baseline blocker.

`_BUILD_SOURCE/record_carrier_assault_1101.py` records four complete native-input Furious demonstrations with an explicitly labelled invulnerable observer, no enemy health/form/phase/attack-clock writes, full decoding and shared-mixer audio. The recordings show both ten-turret-to-hull handoffs, nuclear sky-return and expanding explosion, laser growth/tornado, successful warhead interception and complete takedowns.

The final clips are27.37s (top pair),26.90s (bottom pair),33.87s (nuclear) and31.82s (laser),119.96s total. All source hashes match the final runtime. All four fights complete; both strategic films include an ignored timed detonation and successful interceptions. `_BUILD_SOURCE/verify_carrier_assault_preview_1101.py` passes24/24 installed guide/player checks, including decoded chapter seeks, actual browser AAC playback, un-clipped audio and the clickable detonation chapter. Expected interrupted-playback promises are handled when switching/pausing clips. There are no game or preview page/console errors.

`_BUILD_SOURCE/publish_carrier_assault_1101.py --install` updates the existing cloud-carrier review URL and adds `/current/stage6-carrier-assault-1101.html`. Its four players include direct chapter buttons for firing, exposed hulls, launches and detonations. The full guide gets four current carrier cards; all160 unrelated cards and previous film files remain. No commit or push was requested or performed.
