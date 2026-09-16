# Stage 7 DUAL SCOOP DREDGER minefield warning — September 16, 2026

The DUAL SCOOP DREDGER's late-phase minefield now commits one safe column before it attacks. Five shared fields preview the five dangerous trajectories through green, yellow and red for 0.86 seconds, while the sixth column remains open. Player movement after the tell begins cannot move that opening.

The original attack remains a five-mine spread from the center launcher. Its old condition required a nonexistent third Dredger phase, so the minefield could never occur in natural play; it now runs every fourth attack in the real damaged phase. The warning controller owns the attack channel until release, launches the same five slow shootable mines down the previewed paths, preserves the authored toxic muzzle, and then returns control to the miniboss cadence. Fields render below the authored hull and one matching alert remains visible above it, including during cold-load fallback art.

Focused section 343 passes **10/10**. The full suite reaches its final summary with **4,375 passing assertions / 56 established failures**; the failure names match the previous 56-name baseline exactly and the intermittent Stage-1 sand-tank fixture passed this run. Real Chromium passes **16/16** with zero page, console or game-loop errors. Four native 960×1024 frames were pixel-reviewed from green through release.

Machine-readable proof: [qa/stage7_dredger_mine_warning_0916.json](qa/stage7_dredger_mine_warning_0916.json).
