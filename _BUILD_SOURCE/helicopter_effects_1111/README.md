# Dracodia helicopter weapon effects — November11,2026

Mike requested the helicopter equivalent of the Phoenix/Neural Archon effect upgrade: better animated gunfire, missiles and explosions.

The copied helicopter now uses new eight-pose gold muzzle flashes and animated pointed tracers. Actual current pod recoil/aim sockets own each flash. New red/chromium missiles retain a stable metallic body with eight exhaust/smoke phases and64 authored headings. Larger launch bursts reuse the same hot flame sequence. New16-pose fuel explosions replace the copied helicopter's missile impact/interception effect and its old purple pod-break bursts. A broken pod gets one160px blast plus two delayed112px secondary blasts; missile impacts use72px blasts. Smoke, metal fragments, hot lobes and empty end frames are authored into the source.

## Preserved behavior

HC79 still owns all movement, rotor poses, weapon pods, recoil, aiming, committed gun corridors, native player locks, difficulty counts, physical homing, interception, damage, HP and parts. Gunfire stays non-interceptible. The2/3/4 missiles per living pod remain shootable. Destroying a pod cancels its queued callbacks and removes its target; the other pod keeps fighting. Native sonic fronts, warned charge, hit flash, copy return and death owners remain. No body redesign or extra HP was added. D124's Phoenix/brain effects and game.js are unchanged.

## Authored source and runtime

- Owners: assets/helicopter_effects_art_1111.js and assets/helicopter_effects_1111.js, appended after D124.
- Pages: assets/game/levels/stage_08/effects/helicopter_1111/.
- Source archive: _BUILD_SOURCE/helicopter_effects_1111/.
- Four raw generated masters, exact prompts, actual helicopter reference and source hashes are retained. Sprite-sheet adaptation uses fixed source cells and proportional exports. The missile's lower metallic body is held from one approved source pose so only its exhaust changes.
- Seven tagged Aseprite timelines hold2096 frames, including64 offline directions for muzzle, launch, tracer and missile banks. timeline.json maps editor frames to runtime frame indices. Twenty-one representative Aseprite exports match integrated pixels exactly, including empty timed frames.
- Five lossless packed PNG pages. Even logical cells and packed rectangles; shared bank pivots; binary alpha. Runtime uses ordinary fixed source blits and frame selection. No runtime rotation, scaling, additive blending, filters or animated alpha are added.
- New decorative explosions do not add damage. Effects cap at24, expire after800ms plus any authored delay, freeze with game time and clear with the native owner. Legacy trail emission is suppressed only at a tracked helicopter missile's exact native exhaust point; other trails remain native.

## Observed verification

55 scoped checks pass across native gameplay and source export. Native evidence covers both pod emitters at their current recoil sockets, ordinary player gunfire intercepting actual homing missiles, exactly one burst per intercepted missile, difficulty counts, independent native locks, an input-only non-GOD gun-corridor dodge, pod callback cancellation, visible hit flash and expiry, finite explosions, pause, clear, reduced flashing, sonic/charge compatibility, decoded gun/rocket/blast cues, complete preload, bounded effect lists, and unchanged earlier owners. No page or console errors in completed captures.

The reduced-flashing check initially stopped at95 ticks, before the last queued missile pair. Its corrected130-tick check observes all8 launches; no runtime change was required. An initial capture failed under system memory pressure. The successful capture uses a16-worker HTTP server to limit asset-loader memory; this is capture infrastructure only.

Required game.js and new-script syntax checks pass. The required full test suite still exits1 at the recorded missing difficultyHealthBaseline15 helper (combat_polish_0927b.js:151 / test_fl.js:4537), before its final summary. That existing failure was not changed.

## Finished review

helicopter-upgraded.mp4 shows native gunfire, missile volleys, actual player-fired interceptions, and native pod destruction. Chapters start at selected form/attack checkpoints. The presentation pilot is invulnerable; intercepted missiles use ordinary fire inputs, and the pod-destruction chapter begins through native modularHit. Separate safe-corridor verification uses normal movement, no GOD and zero invulnerability. No HP/phase/clock edits occur during each recorded chapter. Source only; no commit, push or installer.
