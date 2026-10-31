# Corrupted Phoenix turbo cannons and chest core — October 30

PH82 replaces the Phoenix/volcano copy's former aimed feather fan and twin-pod lasers during its cannon stage. It keeps the approved whole Phoenix silhouette, exact native parts/HP dependency, intact/damaged cannon ownership, later corner swoons, copied-life return and final progression.

| Action | Tell / commitment | Active / recovery | Player response |
|---|---|---|---|
| Twin turbo guns |1.65/1.50/1.35/1.20s Easy/Normal/Hard/Furious; body settles halfway through |1.25s; paired left/right cannon reports every140/115/95/80ms, alternating each pod's two physical barrels;0.45s recovery |Leave the narrow parallel straight-south lanes, then track the moving pods |
| Chest-core laser |2.00/1.80/1.60/1.45s;1015 chest charge, metal warning and green/yellow/red field; aim commits halfway through |One32px warm white-hot beam grows outward over0.16s;0.85s active,0.65s recovery with harmless0.32s dissipation |Read the held final lane and move laterally; no tracking after commitment |
| Evasive recovery |One bounded waypoint from visible incoming northbound player fire/current player position, never future input |85–121px/s lateral,48px/s vertical, subtle7px hover;0.8–1.1s cooldown and first-half windup |Chase and aim at the cannon pods while their original vulnerability rules remain |

Both pods alternate their two measured visible barrel-mouth sockets. The two simultaneous reports share one gun cue; there is no shotgun fan or lateral/homing acceleration. Physical rounds use approved authored gun tracer and recoil-muzzle art from HC79, with native collision and explicit non-interception before the first update. Breaking a pod cancels its remaining launches. Every beam now originates exclusively at the measured orange chest-core pixel cluster. Selection uses a private seeded generator, bounded to at most three gun attacks between beams.13 authored7.5-degree directions cover45–135 degrees; warning, actual emitting pose, beam pixels and exact source-alpha damage agree. Body position holds during commitment/fire. Damage retains native white body/part flash and expiry, with the warm core still readable.

The old lava arena's centered transparent architecture plate is replaced with the existing8-frame lava floor at half brightness. Two48px side strips come from the original outer metal edges and use8 pre-authored ember/code-light phases. Their x positions follow the visible left/right viewport boundaries, preventing camera movement from bringing them into the arena interior. Lava scrolls at8px/s, edges at18px/s; the palette frames run at10fps. Native arena download curtains remain. Brain night clouds, helicopter digital jungle, space/main arenas and Stage2's original arena remain unchanged.

## Artwork and rendering scope

467 fixed authored frames:92 whole-body plates across23 source poses/four cannon damage combinations;115 source-locked chest-light frames;260 directional launch/flow/recovery/warning cells. Common logical canvases and pivots are retained, with even unrotated atlas crops and1024px pages. Appearance changes, core glow, direction changes, hit versions, palette darkening and wall light phases are baked offline. No new runtime image rotation/scaling, tint, compositing glow, animated alpha or generated decoration. Sources are existing approved Phoenix BI24 plates, NB80 warm optics, native lava and mechanical-edge art; no new paid generation. Exact hashes, metadata, builder and seven editable Aseprite source documents are in `_ART_SOURCES/phoenix_turbo_core_1030/`.

This pass migrates the cannon station and its scenery. The later native corner-swoon controller and its prior rotating/scaling/blended renderer remain unchanged. It is not a claim of a whole-boss rendering migration. Existing camera easing can continue briefly when paused, while gameplay/body/charge and both arena animation clocks freeze; side strips continue to follow the actual visible edges. The full replay exposed a last-copy handoff bug: surviving Phoenix wing/claw IDs reached the main-body final renderer. The covered native final handoff now uses its native zero-HP core/left/right anatomy, preserving every depleted life pool and final destruction. No changes to core engine bytes, native health budgets or score/reward ownership.

## Verification and footage

49 focused checks pass: rapid twin reports through all four muzzles, straight/non-interceptible physical rounds, both ordinary-movement escape routes without GOD on Normal/Hard/Furious for guns and core beam, actual beam death, core-only beam ownership, pose-specific1015 charge, real damage flash/expiry, single/both cannon breaks and native swoon, visible-fire evasion and bounded motion, clear/pause, timed live-copy return and native copied-life defeat/download home. Actual viewport edge anchoring, independent wall/lava animation, dark palette, even cells and preserved brain/helicopter owners were checked in real Chromium. Native screenshots and decoded footage were inspected. No page, console or asset errors.

Fresh native Furious4100HP checkpoint film: other copied/main lives were cleared before filming. An invulnerable input-only observer uses native guns/Retina and reacts to the visible core warning; there are no recorder HP/phase/clock writes during capture. This is a checkpoint review, not a whole-game or non-GOD full-fight victory claim. Duration101.63s; defeat94.30s; cannon stage55.91FPS / combat53.90FPS / overall53.03FPS. Recorded224 turbo rounds,5 core beams and15 evasive decisions. Decoded audio mean-20.1dB, peak-4.1dB. Prior first-visit film remains archived.

Required full suite finishes with the same five pre-existing failures, no new failures, exit1. `assets/game.js` remains byte-identical. No commit/push requested.

[Turbo cannon chapter](http://127.0.0.1:51046/?phoenix=turbo-core-lava-1030#clip=stage8-phoenix-turbo-cannons)

[Core-beam chapter](http://127.0.0.1:51046/?phoenix=turbo-core-lava-1030#clip=stage8-phoenix-core-beam)

[Full updated Phoenix fight](http://127.0.0.1:51046/?phoenix=turbo-core-lava-1030#clip=s8-phoenix-volcano)

Rebuild `_BUILD_SOURCE/build_phoenix_turbo_core_1030.py`; verify `_BUILD_SOURCE/probe_phoenix_turbo_core_1030.py`; record `_BUILD_SOURCE/record_phoenix_turbo_core_1030.py`.
