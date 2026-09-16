# Stage 6 Doomsday Carrier chrome-flak warning — September 16, 2026

The Doomsday Carrier Mk II no longer launches its Last Run chrome-flak shells without warning. Both shell paths now commit before a 0.62-second shared green/yellow/red warning. Their origins follow the continuously sliding lower-inner hardpoints, while their angles cannot shift after commitment.

The attack now alternates the authored outer `-18°/+18°` pair and inner `+10°/-10°` pair. The previous `%4` indexing always selected the inner pair because this attack only runs on step 2 of each four-step rotation, leaving the outer pair unreachable. Both variants retain authored `s6flak` shells, speed `3.75`, the 0.64-second fuse, twin cyclone muzzles and a 1.08-second total cadence. Each shell still detonates through the authored flak-burst reel into five short-lived fragments. Phase changes cancel a pending flak warning with the Carrier's other attack controllers.

Focused section 355 passes **13/13**. The full suite reaches its final summary with **4,497 passing assertions / 57 failures**: the established 56-name baseline plus the previously documented intermittent Stage-1 sand-tank fixture, with no new failure name. Real Chromium passes **19/19** with zero page, console or game-loop errors. Five native 960×1024 frames were inspected from green through airburst; both fields stay behind the authored hull, the alert clears the boss gauge, and the warnings disappear before the solid shells and authored burst appear.

Machine-readable proof: [qa/stage6_carrier_flak_warning_0916.json](qa/stage6_carrier_flak_warning_0916.json).
