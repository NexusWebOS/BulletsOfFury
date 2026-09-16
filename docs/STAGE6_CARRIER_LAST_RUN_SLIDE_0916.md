# Stage 6 Doomsday Carrier Last Run slide repair — September 16, 2026

The Doomsday Carrier Mk II now traverses continuously during its sixth and final phase. Its sine-driven horizontal flight previously sat after controller and cooldown returns, so the hull froze during warnings, cannon/beam ownership and nearly every cooldown frame. The same authored 0.85-radian-per-second motion and bounded amplitude now run once per frame before those exits.

The repair keeps the complete boss plate, hardpoints, fields, muzzle effects and attack controllers in the same moving coordinate system. It is scoped to Phase 6, keeps the existing attack cadence intact and uses the original bound of `max(60, worldWidth/2 - max(150, hullWidth/2))`. Other Carrier phases retain their existing movement.

Focused section 352 passes **7/7**. The full suite reaches its final summary with **4,463 passing assertions / 56 failures**, exactly matching the established failure-name baseline. Real Chromium passes **12/12** with zero page, console or game-loop errors. Four native 960×1024 frames were inspected across ordinary cooldown, beam-owned, cannon-owned and return motion; the authored Carrier and its effects remain together throughout the traverse.

Machine-readable proof: [qa/stage6_carrier_last_run_slide_0916.json](qa/stage6_carrier_last_run_slide_0916.json).
