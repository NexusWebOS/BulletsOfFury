# Readable attacks — September 14, 2026

Mike's screenshots exposed a second generic volley on stage-1 jets, reused green
player beams on stage 3, and excessive curtains/impact decoration on stage 5.

## Verified changes

- Stage-1 jets retain authored straight twin guns/rocket sequences. Generic
  fan/rake/salvo volleys cannot stack over their own controller.
- Stage-3 beams release from side cannon exits using blue authored laser art.
  The center charges with FOV and releases a finite ice pulse from its forward
  hull exit. Stronger dark-blue palette refinement remains pending.
- Shared warning helpers synchronize green/yellow/red FOV and overhead alerts.
  Furnace head acquisition lasts 0.70 seconds; its pose/aim then lock until two
  eye beams release after 1.65 seconds. Every dangerous encounter has not yet
  migrated to the helper.
- Regent's curtain becomes three mounted-port warnings of three seconds each,
  releasing two projectiles per port. Mother/escort charge starts are serialized.
- Space impacts use one authored atlas reel, with at most six ordinary visible
  impact decorations and no duplicated generic explosions. Damage is unchanged.
  This does not claim stages 5–9 are fully balanced.
- Player fire plume/collision span shrink 25%, retaining the plane nozzle anchor
  and Fire Orb hue. Ice Breath is unchanged. Furnace flame width grows 25%.
- Backspace cannot abandon a paused level; basic shortcut text is removed.
  Full pause menu remains pending. A bounded horizontal gliding helper is ready;
  adoption across encounters remains pending.

Stage-4 rendering diagnosis found no long narrow weapon paths. Gun rounds and
muzzle art were reviewed; a background-only comparison is still required before
conclusively identifying the apparent orange stripes as road art.

## Measured verification

Syntax passes. Full suite: **3,734 passed / 60 failed, exit 1**, final summary
reached. No new failing assertion names against docs/qa/stage_1_5_0914.json.
One prior randomized sand-tank assertion passed this run, not claimed as a fix.
Nine section-300 assertions pass. Generic volley tests exercise armed stage-4
context; the old head-tracking assertion now verifies aim commitment, supported
by a native late-dodge test. Chromium **47 / 0**, zero page/console/loop errors.
Actual input, authored source pixels, warnings and screenshots inspected.

Preview: _shots/encounter_cleanup_0914/video/BulletsOfFury_Readable_Attacks_0914.mp4.
**37 seconds / 1,110 decoded frames / 960×1024 / 30 fps / H.264 + stereo AAC.**
Native sound events/loops aligned to frames; no music. Selected debug attacks
with a protected demo pilot. No export-only normalization; maximum peak 0.9178.

Sources: _BUILD_SOURCE/encounter_cleanup_0914/. integrate.py --dry-run reproduces
runtime bytes; later mutations reject subsequent edits. Proof:
docs/qa/encounter_cleanup_0914.json. Runtime LF/test CRLF preserved.
No atlas changes, Git integration, commit, push or user-data deletion.
