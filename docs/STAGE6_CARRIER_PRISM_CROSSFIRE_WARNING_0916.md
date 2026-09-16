# Stage 6 Doomsday Carrier prism-crossfire warning — September 16, 2026

The Doomsday Carrier Mk II no longer releases its Phase 5 upper-barrel prism crossfire without warning. All four physical barrel paths now commit before a 0.62-second shared green/yellow/red warning. The field origins continue to follow the moving hull, while player movement cannot bend the promised angles.

The original attack remains intact. The authored `upper_left_outer`, `upper_left_inner`, `upper_right_inner` and `upper_right_outer` hardpoints retain their alternating `22`, `8`, `-8`, `-22` and reversed `-22`, `-8`, `8`, `22` degree layouts. All four bolts remain authored `s6prism` rounds at base speed `4.3`; the three existing prism muzzle reels, cannon sound and 1.25-second total cadence release on the same beat. Phase changes now cancel a pending crossfire warning along with the other Carrier warning controllers.

Focused section 350 passes **12/12**. The full suite reaches its final summary with **4,443 passing assertions / 58 failures**: the established 56-name baseline plus the previously documented intermittent Stage-1 sand-tank and road-tank fixtures, with no new failure name. Real Chromium passes **16/16** with zero page, console or game-loop errors. Four native 960×1024 frames were inspected from green through release; the four fields remain behind the authored hull, the alert clears the boss gauge, and warning art is gone before the prism bolts appear.

Machine-readable proof: [qa/stage6_carrier_prism_crossfire_warning_0916.json](qa/stage6_carrier_prism_crossfire_warning_0916.json).
