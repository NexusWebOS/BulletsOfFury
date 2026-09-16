# Stage 8 FURIOUS DEATH straight-missile warning — September 16, 2026

FURIOUS DEATH no longer launches its four-missile vertical salvo without warning. The final Vile form now commits all four original launch columns before a 0.58-second shared green/yellow/red warning and releases only after red. Player movement cannot shift the promised lanes.

The original missile behavior remains intact: four launch attempts use the existing enemy-missile budget, the same `-0.30`, `-0.10`, `0.10` and `0.30` hull offsets, the original armored-gunship muzzle art and the 0.78-second total cadence. Each surviving missile remains shootable and flies straight down with the existing velocity. No Retina or homing state is added, preserving the engine rule that bosses after Stage 1 do not receive default homing missiles.

Focused section 347 passes **9/9**. The full suite reaches its final summary with **4,412 passing assertions / 56 established failures**, with no new failure name. Real Chromium passes **16/16** with zero page, console or game-loop errors. Four native 960×1024 frames were inspected from green through release.

Machine-readable proof: [qa/stage8_vile_missile_salvo_warning_0916.json](qa/stage8_vile_missile_salvo_warning_0916.json).
