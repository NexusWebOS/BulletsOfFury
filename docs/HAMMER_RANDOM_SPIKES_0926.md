# Stage 5: eight randomized chromium spikes

Mike's follow-up replaces the 3/4/5 sequential columns from `HAMMER_BOTTOM_ROW_0926.md`.

Eight evenly spaced positions now span the visible arena on every difficulty. Retina markers are fitted to their spacing, so all eight remain distinct. A new shuffled order is committed once per hammer impact: each position erupts exactly once, and consecutive slams cannot reuse the identical order. Movement after the warning does not redirect a marked column.

Each lane runs the shared green → yellow → red sequence for three seconds, with the final **one full second red on every difficulty**. An authored red warning plate marks the whole future shaft during that red second and remains during the eruption. The plate is cropped/scaled to cover the shaft's taper, with a small safety margin. It causes no damage. The generated ground spark is also harmless; damage starts as the shaft visibly rises. The 75%-height art, visible-shaft collision, harmless residue and warning-free hammer throws remain.

Difficulty changes the gap between queued eruptions: Normal **0.50 s**, Hard **0.42 s**, Furious **0.34 s**. The sequence fills all eight positions over time, while leaving gaps and keeping the escape warning intact. Right-side warning graphics remain visible over the overlapping LOCK/radar footprint.

No new artwork was needed: the installed 16-frame spike reel and the engine's authored `bmfx_fov_red_tall` warning plate are reused. The green/yellow/red Retina colors follow `l23FovPhase`, keeping them synchronized with the warning clock. No throw cones or throw alert sounds were reintroduced.

## Verification

- Syntax check passed. Final full suite: **5,012 passing, zero failures**, exit 0 and final success banner. `_shots/test_fl_random_spikes_0926_final.log`; no failing names against the previous 4,997/0 baseline. The initial full run also passed.
- Real Chromium, all three difficulties: eight distinct positions and unique delays, changed orders across slams, green/yellow/red phases, the harmless red window, growing-shaft damage and all nine hammer-counter routes passed. Zero page/console errors. Durable results: [qa/hammer_random_spikes_0926.json](qa/hammer_random_spikes_0926.json).
- Native player input: staying in the first warned column causes one hit **1.15 seconds after red begins**; a 0.35-second sidestep moves 73.71 logical pixels and avoids damage on Normal, Hard and Furious. The first escape fixture accidentally placed the player against the boss's body; that probe failed and was corrected to start below the body, then passed. Logs retained as `_shots/probe_random_spikes_0926_final.log` and `_shots/probe_random_spikes_0926_escape_recheck.log`. No runtime change was needed for that fixture repair.
- Sampled **3,233 lethal points against the actual rendered red warning pixels**: zero unwarned points. The warning covers the tapered shaft and slightly exceeds its boundaries.
- Inspected the real screenshots and recorded animation; review media load check passes. Game LF and test harness CRLF retained; whitespace check passes.

Preview: `_shots/hammer_random_spikes_0926/review.html`. Three native canvas recordings show the charged phase and the two counter/spiral routes. The spike recording holds the player/camera centrally so all eight positions remain visible. These are controlled invulnerable, muted inspection recordings, with unrelated asteroids suppressed in the fixture; they are not unassisted campaign playthroughs.

The original shorter spike sheet, earlier reviews, prior work and music remain. Nothing committed or pushed.
