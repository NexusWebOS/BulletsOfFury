# Attached clock and stats rework â€” 2026-09-22

The campaign clock now takes its vertical position from the actual map bar bottom, with a five-logical-pixel overlap. It reads as an attached lower module and follows the bar entrance position; it still hides during Save/Load so it cannot cover the dropdown title.

Stage-clear results retain the authored panel and graphical stage font. Each of the eight stat bays now separates its label from a right-aligned value, sized independently against reserved widths. Typing uses fixed anchors so letters do not shift sideways. The portrait is contained within its bay, the complete rank plate remains intact, and its adjacent box spells out the rank name. Score and clear time have separate labels above their values.

The old 0.8-second forced finish interrupted the row sequence. Results now progress through eight 0.16-second row reveals, score tally, rank stamp and password, with a 2.6-second completion ceiling. A finishes the reveal immediately; a second confirmation advances. Score ticks are deterministic rather than random, and character sound tracking resets for every debrief.

Verification:
- Syntax checks passed for both changed scripts.
- Chromium: eight label/value pairs fit, including 987654 shots, 1234 upgrades and THERMOSHOCK BALL; sequential row progression, score/rank completion and A-to-finish verified; no page or console errors.
- 90 stat-tick invocations observed during the scripted normal reveal. This validates sound triggers, not a listening evaluation.
- Clock is visible and overlaps the bar by 9.1 screen pixels at 1600 x 900. Screenshots inspected.
- Full test_fl.js suite completed with exit 1 and 75 failures; no new normalized failure names compared with the preceding map run. Two source-shape checks were updated for the new score/time layout. Log: _shots/stats_rework_suite_final_0922.log.
- Probe: _BUILD_SOURCE/probe_stats_rework_0922.py. Evidence: _shots/stats_rework_0922/.

No generated artwork was replaced. No commit or push performed.
