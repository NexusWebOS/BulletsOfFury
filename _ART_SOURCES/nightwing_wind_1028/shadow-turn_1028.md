# Nightwing — persistent shadows and banked turns, October 28

Mike requested a shadow beneath the wind Nightwing and actual rotational turn/swerve frames. The earlier owner drew shadows only for a few depth banks; cruising, normal banking, rolls and directional entry had no shadow. The old24-frame drift also switched abruptly between a flat plate and one fixed bank attitude.

## Changes

The owning `_ART_SOURCES/nightwing_wind_1028/build.py` now exports exact-pose silhouette shadows for the whole hull, clean body, both aiming/recoil guns, heading, flyover, left/right drift and return. Static stored-alpha shadows use RGB(2,7,14) and56% source alpha. Fixed authored cells only; no runtime tint, opacity animation, filter or generated shape. Runtime draws one complete shadow before exhaust/hull: clean body plus its two actual aimed gun shadows in modular gun flight, otherwise the exact whole pose. Offset[18,76] follows each pre-authored depth unit; hidden offscreen phases leave no shadow. Damage flashes stay white and never recolor the shadow. Native death/crash rules remain.

The directional bank now has64 yaw angles ×3 bank attitudes (192 cells). Each drift has48 frames: the same canonical aircraft gradually banks to28 degrees and back while making the tangent-aligned half-turn and shrinking through its original depth curve. Roll projections and direction/size variants are source-pixel authored offline. Shared body pivots, matching measured thruster anchors and white hit masks remain. `nf29Art` lets native frame timing/collision use the actual updated metadata, retaining the old source outside the Stage6 wind encounter. No runtime sprite rotation or scaling substitutes for these frames.

`assets/nightwing_wind_1028.js` owns the single aircraft/shadow draw; `assets/nightwing_flight_1027.js` owns the native path and cell selection. New `_flight_1028c.png` URLs and script versions avoid stale art. Canonical cruise hull, weapons, wind gusts/muzzles, charge, dash rings and exhaust PNGs remain byte-identical. One HP/target, native attack/dodge timing, health, flight trajectory, protection and ordinary-bullet rules are unchanged. No game.js/test_fl.js edits, commit or push.

Both `drift_left-48.aseprite` and `drift_right-48.aseprite` are editable48-frame timelines,432×432 with fixed216px pivot. CLI re-export reconstructs each bank pixel-identically. Owning recipe, manifest, source hashes and turn contact are retained.

