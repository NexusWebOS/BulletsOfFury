# Rotation, shield and Stage 2 repair — 0918

This batch moves pickup and Furnace Tyrant turning away from live canvas rotation. Twelve-frame pickup turn strips and sixteen-frame Furnace direction strips are generated under `assets/game/rotation_frames_0918`; runtime code chooses a finished frame. The Furnace arms use the same quantized body angle and retain their mount pivot, recoil and part-specific damage state.

Pickup acquisition notices now use the graphical dialogue face through the letter-by-letter arcade banner. Life/continue, infusion, Fury/Time bombs, score bullets and Fury HQ space rewards use authored turn strips. The additive disc under the new bombs and score bullets was removed.

The boss shield gauge now uses a distinct rectangular cyan energy frame with a straight rectangular fill well and an attached `SHIELD` label box centered in the art. The label is baked once; runtime does not draw a second copy.

Hard-mode Razorback Duo draws one independent miniboss bar for each tank. The targetable center turret flashes on any registered turret hit, including the opening gun phase.

Stage 2 hostile fire geysers spawn only inside 10–42 pixel lava gutters at the left or right camera edge and rise from the bottom edge. They have dedicated warning and eruption cues. Firewalls now play their registered pass cue when the wall crosses the player's row.

The remaining vehicle-wide direction-frame audit is tracked separately because it covers every tank and jet family rather than this repair's pickup and Stage 2 scope.
