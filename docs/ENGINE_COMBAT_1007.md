# October 7 combat engine pass

The game now retains readable warning symbols, warns the nearest real incoming rounds across stages, attaches the final arena architecture to world space, and uses simulation time for the repaired projectile and chaingun paths.

## Diagnosed defects and changes

- The final arena centered its background and architectural ribs on `camLeftX()` every draw. Both sides followed the player. `aa5ArenaDraw` now places those two layers at the world center; the existing camera alone determines what part is visible. Code/void motion remains independent.
- The generic enemy movement path added velocity once per rendered update without using `dt`. Identical tracers traveled different distances at 30/60/120 FPS. It now applies `dt * 60`, preserving the established 60 FPS speed.
- Ordinary hostile collision selected `targetShip` again inside each co-op seat's damage pass. This could test a nearby P2 projectile against P2's position while charging P1 for the hit. Collision now uses the current seat's physical player. A swept expanded-box test catches a fast round that passes completely through a ship between updates.
- The ordinary player projectile path now scales displacement by `dt * 60`. Fast MG/spread/incendiary/ice-lance rounds sample the path at no more than four-pixel intervals before the existing collision/damage owner runs. Thin fighters and modular boss geometry can no longer be skipped simply because the endpoint is beyond them. Existing beam/special collision owners remain separate.
- Generic static-frame projectile glow/spin previously used wall time. They now use the projectile's age; held static frames remain static, and approved authored flight reels remain animated. Generic MG/spread rounds receive their own age.
- Both the original and repair chaingun renderers advanced barrel animation during draws, sharing `run._chainSpinT` across seats, and `drawWorld` decayed muzzle flashes. The new renderer reads `player._chainSpinT`; simulation advances it independently for each ship. Pausing/repeated captures cannot accelerate barrels. Actual chaingun pickup warms that pilot's two mounts and barrel, and retries a premature cached-null lookup. Player reset clears stale death-spin/muzzle state that could continue suppressing mounts.
- Ready-cache pickup switching did not reproduce the user's intermittent missing-mount report. This pass fixes the concrete reset/cache/clock defects and verifies five actual weapon-to-chaingun pickup transitions for each of all nine pilots, rather than claiming an unobserved root cause.

## Shared warning contract

`combatWarningTick(owner, id, elapsed, duration, silent)` still owns the warning sound/timing state. `combatWarningDraw(owner, q)` keeps its existing geometry and `fieldOnly`/`alertOnly` options. New optional `laneShape: 'line'` draws an authored constant-width beam corridor using `q.width` and the committed `x,y,ex,ey` endpoints. Ordinary FOV warnings remain available.

The original authored green/yellow/red symbol stays visible with a small brightness pulse, is kept within the visible field, and draws at most once per owner per world render. Stage 6 now uses it too. The warning collector considers relative approach, prioritizes at most two imminent rounds per seat, and ignores dead rounds, receding/parallel safe rounds, helpers and beams with their own lane warnings. Small authored impact asterisks no longer add a second glow-tracer overlay.

Attack controllers must commit their target and cancel their own released shots/warnings when the emitter dies. The warning renderer does not invent a new target or extend an attack's collision.

## Integration

Load `assets/engine_combat_1007.js` after `assets/finale_ai_1006.js` and before the October 7 encounter layers. Require `_BUILD_SOURCE/test_engine_combat_1007.cjs` after the existing finale AI test. No new art or atlas is needed. `assets/game.js` preserves LF endings.

Changed files: `assets/game.js`, `assets/alien_arena_1005.js`, `assets/pellet_warnings_1005.js`, and new `assets/engine_combat_1007.js`.

## Verification

- Required existing full suite completed with **7,485 passing assertions**, final success banner, exit **0**, after the game/arena/collector changes.
- Native Chromium: **34 checks**, zero page/console/missing-asset errors. Actual pickup transitions across nine pilots, roll/somersault/reset, independent co-op barrel clocks, paused native projectile pixels, retained comet flight animation, equal linear tracer travel at 30/60/120 FPS, a P2-only swept hostile hit, a fast player round crossing a thin fighter, warning priorities, and final arena world anchors passed.
- Native screenshots inspected: all nine current hulls/mounts, committed warning corridor and arena camera positions. Source probe `_BUILD_SOURCE/probe_engine_combat_1007.py`; captures/review `_shots/engine_combat_1007/`; portable evidence `docs/qa/engine_combat_1007.json`.

These are controlled native fixtures, not a full campaign clear or human balance approval. Timestep repairs cover the shared generic travel paths; specialized authored/homing controllers retain their existing owners. The new regression module must also run in the final combined upgrade suite.

No commit or push performed. Existing dirty work and archived assets retained.
