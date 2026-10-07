# Rebel air encounter upgrade — October 7, 2026

`assets/rebel_air_1007.js` extends the deployed RA4/RG4 Rebel Squadron and WHV blue-ace controllers. Load it after `pellet_warnings_1005.js` and the other existing boss layers. It does not replace `assets/game.js` or the shared warning renderer. All new warning lanes use `combatWarningTick`/`combatWarningDraw` and their real committed trajectories.

## Rookhook

Rook's natural ability cycle is grapple, slugs, ram. The grapple first gives a 1.65/1.40/1.20/1.20 second warning on Easy/Normal/Hard/Furious. Its aim stops tracking before the halfway mark. The open hook then travels from the visible rotating winch on a chain of independently positioned chrome links. A connected hook closes, reels the chosen jet inward over 0.70 seconds, swings it over 0.42 seconds, releases it toward a bounded screen edge over 0.45 seconds, and recovers for 1.05 seconds.

The open or connected hook has its own HP and Retina target. Ordinary rounds and beam fire can cut it; a barrel roll, somersault or charge dash escapes it. Only the selected co-op seat moves. Rook's death, target loss, stage change and encounter clear all release the captured ship. The source encounter pauses competing special attacks and ordinary squad gunfire during capture; forced motion cannot deliver incidental contact damage. The edge impact still uses normal player damage, shielding and invulnerability rules. A stationary unshielded positive control dies on impact; a Juggernaut can sidestep the committed cast using ordinary right movement at every visible difficulty.

## Nyx

Ghostknife now uses an authored cyan/indigo corkscrew with eight phases. The same reel is drawn behind the ship and clipped across three front turns, giving above/below occlusion around the faint whole hull. It is present during charge, combat cloak, reveal and the opening showcase. Nyx's earlier diamond/glow showcase is suppressed. Her missile-acquisition hiding and blind-hit white silhouette are preserved.

During cloak, Nyx commits a three-round ambush from a visible nozzle warning. The warning lasts 1.05/0.85/0.72 seconds across Easy/Normal/Hard-or-Furious, followed by a repositioning gap. The original cloak duration and recovery remain in the deployed special-attack system.

## Blue elite jet

The actual Stage 6 blue ace adds a paired wing-battery sequence between its existing evasions and missiles. It moves to a position captured above the pilot, settles, warns both batteries, fires two six-round salvos on Easy or three on other modes, and leaves an explicit recovery window. The rounds diverge away from the center, preserving a visible central corridor. Copied Stage 8 donor controllers are excluded from this source-specific motif.

## Destruction

Rebel wrecks use the pilot's constants: 1.25 seconds of anchored burning spin, 540–900 degrees of turn, crash, shock rings and explosions, then the 0.55 second aftermath. The old GP4 second wreck is retired; the authored whole hull remains opaque until impact. Owner projectiles and attached hooks clear on death. The all-dead squad still resolves the real boss reward exactly once.

The blue ace uses the same clock and anchored bursts. Death cancels living dash, crossing, roll and somersault states so a crossing warning cannot hide its wreck. It has no delayed full-screen white death flash.

## Authored assets

- Shipping sheet: `assets/game/rebel_air_1007/rebel_air.png`, 1,150,786 bytes.
- Native source: `_ART_SOURCES/rebel_air_1007/rebel_air.png`; prompt retained beside it.
- Native RGBA size: 1448 × 1086. Four columns, three rows, 362 × 362 cells.
- Cells 0–3: winch, open hook, chain link, closed hook. Cells 4–11: Nyx spiral phases.
- Runtime key: `ra7_air`.
- SHA256: `5090844963aec3d25c2a8a5f70355a569dfaf457389b7b6728ed5852910cc045`.

The source and shipping files are exact byte copies, retaining native transparency. `_BUILD_SOURCE/build_rebel_air_1007.py` verifies dimensions, alpha, cell bounds, source and shipping hashes; `--write` emits the matching manifest. No color-keying, synthetic pixels, or procedural sprite replacement is used. Runtime rotation, module placement, depth clipping and energy-frame blending are animation/composition operations.

## Verification and limits

Run `node --check assets/rebel_air_1007.js`, `python _BUILD_SOURCE/build_rebel_air_1007.py`, and the integrated `node _BUILD_SOURCE/test_fl.js`. The dedicated `_BUILD_SOURCE/test_rebel_air_1007.cjs` adds 36 assertions when called by the shared suite. A full pre-integration suite run with the initial 35 additions reached 7,520 assertions and its final zero-error summary. That run preceded the final Nyx showcase consistency and blue-ace dead-warning fixes; the root integration run must verify the final combined build.

`python _BUILD_SOURCE/probe_rebel_air_1007.py` captures actual Chromium `drawWorld` pixels and controller outcomes under `_shots/rebel_air_1007`. It tests Rook's full state sequence, cut/roll/death/clear escapes, real edge damage, co-op ownership, all four ordinary-movement Juggernaut dodges, Nyx's authored depth layers/committed rounds/white contact/showcase, single opaque death, ace center corridor, and death during a crossing warning. It records page/console errors and the real asset draw counters.

The probe is a focused set of controlled combat states, not a full campaign clear or exhaustive multiplayer balance pass. Its ordinary-movement dodge fixtures and edge-impact damage control have no shield or invulnerability. Other visual captures hold the pilot safe to inspect specific behavior. Audio dispatch uses existing authored effects; this work does not claim an audible mix review.
