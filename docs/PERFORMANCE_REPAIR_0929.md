# Stage 6–8 rendering and Stage 7 vent repair — September 29

The incoming engine is preserved, including HAMA, campaign ownership, the Stage 6
jet gates, Stage 7 cinematic portal and authored beam reels. This pass changes
rendering cost and hazard registration, not encounter health, weapon damage or
wave density.

## Owners and fixes

- `assets/game.js`: `lateSpriteBake` holds small rendered sprite layers in a
  192-entry / 8 MiB LRU cache. P87 machine-gun/spread round halos and Cole's
  gold/black trident glows/filters now use cached layers. Positions, rotations,
  source cells, palettes and separate halo/body alpha remain with their callers.
- Main-context pickup/icon shadows use the same bounded cache; other contexts
  and unshadowed draws retain the direct path. No generated art or atlas changed.
- `bakeGlow` and `glowBlob` evict old entries when full. They no longer return
  null solely because their lifetime bake counter reached the cap, which silently
  restored per-projectile live blur. Their explicit cap=0 diagnostic remains.
- `bg6RainDraw`: unchanged 382 drops at maximum rain, with the same positions,
  lengths, depths and widths, batched into three canvas strokes.
- `stage7SluiceDraw`: fixed pipe/outlet plate, with exhaust cells aligned to it.
  The last sheet column is offset -33 source pixels in X; the lower row is
  offset -31 in Y. Buildup frame 2 precedes alternating flow frames 3/4 and
  withdrawal frames 5/6. The crop no longer animates the metal edge of the pipe.
  Outlet is centered on its event row. Collision begins at its visible mouth;
  the initial short puff has a shorter hit region. Existing warning timing and
  harmless withdrawal window remain.
- `enemyWarningOwner` removes floating warning triangles from regular enemies
  and their attack-lane wrappers. `assets/combat_polish_0927b.js` also suppresses
  its second arrow overlay for those owners. Ordinary enemy edge arrows are
  suppressed in Stages 6–8. Boss/miniboss symbols, FOV lanes, ground reticles and
  Stage 6 ordered row asterisks remain.

## Verification

Syntax and the full `_BUILD_SOURCE/test_fl.js` suite are required after the final
edit. Native QA and captures live under ignored `_shots/performance_0929/`.

`_BUILD_SOURCE/performance_repair_0929/verify_performance.py` serves the actual
index in Chromium. It reverses only this pass's guarded edits in an intercepted
engine response to obtain the exact incoming engine (SHA-256 starts
`bd466181ffb2`), without reverting files on disk or discarding earlier work.
Matched rendering workloads enforce SS=2, 100 projectiles, 180 authored particles
and four pickups. Rendering runs on native requestAnimationFrame. This is a
rendering stress comparison, not a full-stage survival or balance test.

Nine native checks cover live main-canvas blur/filter removal, cache bounds and
eviction past capacity, diagnostic bypass, full rain density, regular-enemy
triangle removal, retained boss warning art and the vent's authored phases.
The actual mirrored vent frames are captured into `vent_repaired.gif`; review
them, rather than trusting frame-number assertions alone.

`profile_late_stages.py` also samples actual gameplay simulation and firing in
Stages 1/6/7/8. Its detailed instrumentation affects timings and random encounters
change object counts; do not use those samples as a matched before/after result.
Headless Chromium timings are local observations, not a universal FPS promise.

Changes remain local until Mike requests a commit or upload.

## Measured results
Local Chromium, identical fixed scene counts, high-quality SS=2.
| Stage | Before FPS | After FPS | After render p95 |
|---|---:|---:|---:|
| 6 | 4.7 | 53.6 | 15.1 ms |
| 7 | 5.1 | 60.0 | 9.1 ms |
| 8 | 5.0 | 60.0 | 2.1 ms |

Native checks: 9 passed, no browser errors. Reviewed authored bullet/pickup
visuals against the incoming renderer and the captured vent animation phases.

Final syntax checks pass; full suite reaches its final banner: 5,817 passing
checks, zero errors. Engine SHA-256: `0d3e6e4aacdee8ba660c863f90783e0e75a798140faa4ecaeb341ff09f131b94`.

The warmed live simulation sample (without individual draw-call profiling)
observed Stage 6: 42.6 FPS, Stage 7: 59.0 FPS, Stage 8: 56.1 FPS.
Stage 6 remains the heaviest live scene, especially with the allied wing and
storm. These short, immune-player observations verify runtime execution;
they do not establish a constant 60 FPS across a full level or all machines.
