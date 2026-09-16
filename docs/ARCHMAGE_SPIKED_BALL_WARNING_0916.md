# Stage 5 Archmage spiked-ball warning — September 16, 2026

The Chrome Hammer Archmage no longer curls into its 15-second spiked-ball phase and launches on an unwarned random vector. When the curl begins, it now commits a left or right launch direction and exact first wall-impact point. A 1.25-second shared green/yellow/red corridor previews that path before the physical ball can move.

The committed impact remains stable when the player moves far enough to shift the Stage 5 camera. The first reflection uses the bounds captured at warning start, so its wall contact matches the visible corridor; after that first bounce, the existing dynamic screen-edge reflections resume. The authored spiked-ball reel, base velocity `150/165`, 15-second duration, missile knockback, weapon-triggered rage behavior and later attack flow remain intact. Interrupting the curl cancels its pending warning.

Focused section 357 passes **10/10**. The full suite reaches its final summary with **4,521 passing assertions / 56 failures**, the exact established baseline with no new failure name. Real Chromium passes **18/18** with zero page, console or game-loop errors. Five native 960×1024 frames were inspected from green through the first bounce; the warning remains fixed after opposite player movements, clears before launch, and the authored ball reflects at the promised wall.

Machine-readable proof: [qa/archmage_spiked_ball_warning_0916.json](qa/archmage_spiked_ball_warning_0916.json).
