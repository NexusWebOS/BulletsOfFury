# Stage 6 Doomsday Carrier omega-bomb warning — September 16, 2026

The Doomsday Carrier Mk II no longer drops either Last Run omega-bomb variant without warning. The center corridor now commits before a 0.66-second shared green/yellow/red warning. Its origin follows the moving center cannon throughout the warning, while the downward angle cannot change.

Both original variants remain intact. The primary bomb retains base speed `1.1` and a 1.45-second total cadence; the later pressure beat retains base speed `1.25` and a 1.20-second cadence. Both use authored `s6omega` art, acceleration `1.05`, maximum speed `5.2`, scale `1.15`, the center prism muzzle and the existing boss-cannon/space-volley sound route. Phase changes cancel a pending omega warning with the Carrier's other attack controllers.

Focused section 353 passes **11/11**. The full suite reaches its final summary with **4,473 passing assertions / 57 failures**: the established 56-name baseline plus the previously documented intermittent Stage-1 sand-tank fixture, with no new failure name. Real Chromium passes **16/16** with zero page, console or game-loop errors. Four native 960×1024 frames were inspected from green through release; the corridor remains behind the authored hull, the alert clears the boss gauge, and warning art is gone before the solid omega bomb appears.

Machine-readable proof: [qa/stage6_carrier_omega_warning_0916.json](qa/stage6_carrier_omega_warning_0916.json).
