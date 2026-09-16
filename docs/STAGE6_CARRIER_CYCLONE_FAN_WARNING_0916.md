# Stage 6 Doomsday Carrier twin-cyclone warning — September 16, 2026

The Doomsday Carrier Mk II no longer releases its opening six-tracer cyclone rake without warning. Both physical rotary batteries now commit their three original aimed paths before a 0.62-second shared green/yellow/red warning. Player movement after the warning begins cannot redirect the six promised lanes.

The original attack geometry and pressure remain intact: the left and right `MG` hardpoints each retain their mirrored `-0.15`, `0` and `0.15` offsets, all six rounds remain authored `s6cyclone` tracers with base speed `4.1`, and phases one and three retain their original 1.35-second and 1.12-second total cadences. The warnings follow the physical hardpoints if the carrier shifts, while their angles remain committed. Both authored cyclone muzzle reels and the existing fire sound release with the rounds.

Focused section 348 passes **10/10**. The full suite reaches its final summary with **4,421 passing assertions / 57 failures**: the established 56-name baseline plus the known intermittent Stage-1 sand-tank fixture, with no new failure name. Real Chromium passes **16/16** with zero page, console or game-loop errors. Four native 960×1024 frames were inspected from green through release; the six fields remain behind the carrier, the matching alert clears the boss gauge, and warning art is gone before the tracers appear.

Machine-readable proof: [qa/stage6_carrier_cyclone_fan_warning_0916.json](qa/stage6_carrier_cyclone_fan_warning_0916.json).
