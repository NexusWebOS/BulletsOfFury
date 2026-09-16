# Stage 6 Thunderhead shared row warnings — September 16, 2026

ENG-02 advances across the Doomsday Carrier Mk II's live `THUNDERHEAD` attack. Each of its four rows now owns a complete 0.66-second shared green/yellow/red warning. Six fields show the exact lightning columns while two adjacent columns remain open. The opening commits when each row begins, moves one column only after release, and cannot chase late player movement.

The fields render behind the authored carrier and its storm nodes. The matching alert renders afterward at the top of the enormous hull, below the boss gauge, so it remains visible. The original pair of authored Stage-6 projectiles per dangerous column, muzzle flashes, acceleration, four-row count and bouncing gap direction remain intact: twelve rounds per row and 48 across the full sequence.

Focused section 341 passes **12/12**. After rebasing onto GitHub commit `02f38a6b`, the complete suite reaches its final summary with **4,359 passing assertions** and the **56 established failure names**; the incoming build removed the prior intermittent Stage-1 sand-tank failure and Thunderhead added no new failures. Real Chromium passes **19/19** with zero page, console or game-loop errors. Five native 960×1024 frames were pixel-reviewed across green, yellow, red, first release and the next row's restarted green warning.

Machine-readable proof: [qa/stage6_thunderhead_warning_0916.json](qa/stage6_thunderhead_warning_0916.json).
