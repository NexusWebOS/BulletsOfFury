# Stage 5: round warning columns and asterisks

Mike rejected the red warning that narrowed toward the top. The chromium eruption now has a constant **96-pixel diameter**, matching the original Retina footprint, with rounded top and bottom caps. The existing authored red warning plate supplies the fill and curved caps through runtime slicing; no new sprites or atlas edits were needed.

Each position displays the shared **impact-imminent asterisk**, using `bmfx_alert_<color>_impact_imminent` (the star, not the triangular danger symbol). It sits at the column's crown, below the boss gauge, progresses green/yellow/red with the Retina, and clears when eruption starts. Edge asterisks stay inside the world's bounds. They are preloaded with the hammer encounter and drawn after its body and spike art.

The full-world row still has eight fixed positions across the 680-pixel Stage 5 map, with about five full Retina widths in a 480-pixel view. The shuffled sequence, three-second countdown with a full second of red, difficulty cadence, 75%-height spike animation, damage boundaries and counterable hammer throws are unchanged. The red column is a conservative danger preview; its width includes safe margin around the narrower damaging shaft.

## Verification

- `node --check assets/game.js` passed.
- Full suite completed with **5,033 passing assertions, zero failures**, exit 0 and final success banner. Previous baseline: 5,021/0. No new or remaining failing names. Log: `_shots/test_fl_round_zones_0926.log`.
- Real Chromium measured **96 pixels** of warning width near the top, center and bottom, with transparent rounded corners. All **3,233** sampled damaging shaft points are covered by warning pixels.
- Actual asterisk pixels were verified in all three colors. Both-edge movement/damage, fixed row geometry across camera views, Normal/Hard/Furious phase loops, all nine hammer-counter routes and the one-second sidestep check pass. **Zero page/console errors.** Durable report: [qa/hammer_round_zones_0926.json](qa/hammer_round_zones_0926.json).
- The first pixel probe found one uncovered lower-boundary point at the rounded foot. Added four pixels of bottom margin, then reran successfully. Initial and final logs are preserved in `_shots/probe_round_zones_0926.log` and `_shots/probe_round_zones_0926_final.log`.
- Inspected screenshots and a contact sheet from the updated native Chromium recording. Preview: `_shots/hammer_round_zones_0926/review.html`. Controlled invulnerable, muted inspection fixture with unrelated asteroids suppressed; not a full campaign balance run.

Existing work preserved. Game LF and test harness CRLF retained. No commit or push.
