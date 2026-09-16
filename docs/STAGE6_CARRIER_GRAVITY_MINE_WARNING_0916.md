# Stage 6 Doomsday Carrier gravity-mine warning — September 16, 2026

The Doomsday Carrier Mk II no longer releases its Phase 5 paired gravity mines without warning. Both mine paths now commit before a 0.72-second shared green/yellow/red warning. The field origins continue to follow the moving left and right mounts, while player movement cannot alter the promised angles.

The original attack remains intact. The left and right mines keep their `π/2 - 0.20` and `π/2 + 0.20` trajectories, authored `s6gravity` art, base speed `1.35`, acceleration `0.16`, maximum speed `2.15` and scale `1.05`. The existing prism muzzles, cannon/space-volley sound route and 1.72-second total cadence release on the same beat. Phase changes cancel a pending gravity warning with the Carrier's other attack controllers.

Focused section 351 passes **11/11**. The full suite reaches its final summary with **4,455 passing assertions / 57 failures**: the established 56-name baseline plus the previously documented intermittent Stage-1 sand-tank fixture, with no new failure name. Real Chromium passes **16/16** with zero page, console or game-loop errors. Four native 960×1024 frames were inspected from green through release; both fields remain behind the authored hull, the alert clears the boss gauge, and warning art is gone before the two solid gravity mines appear.

Machine-readable proof: [qa/stage6_carrier_gravity_mine_warning_0916.json](qa/stage6_carrier_gravity_mine_warning_0916.json).
