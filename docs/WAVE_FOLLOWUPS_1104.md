# Wave follow-ups (November 4)

Mike picked three open items from the wave audit (docs/WAVE_AUDIT_1103.md). Layer
`assets/wave_followups_1104.js` (WF14), loaded last. `window.WF14_OFF=1` disables all three.

1. **Stage 6 story scene skip** (`WF14_TALK_OFF`). The team-argument scene (fb2Talk,
   feedback_claude_1003.js) freezes combat. feedback_1003h.js replaced fb2TalkTick with an
   auto-advance-only version, so it could not be skipped: 87 s for Cole (Callisto + demo), ~58 s
   otherwise. WF14 wraps fb2TalkTick: FIRE or confirm finishes the typing, a second press advances.
   A press counts only after the scene is 0.35 s old and the line 0.25 s old, so mashing cannot
   blank-skip. Callisto/demo beats ignore presses. Measured: 87 s untouched, 24 s pressing every 0.5 s.
2. **Stage 5 rammer wind-up** (`WF14_RAM_OFF`). S511's rammer (stage5_amplify_1101.js) warns with a
   lane .64/.42/.30 s (N/H/F) then charges 440/650/850 px/s. WF14 wraps s5SpaceTick: during the tell
   it blinks white twice (45%/80%) and eases ~10 px back against the charge line, returning by the
   end so the charge starts on the warned lane (all difficulties). Normal only: tell .90 s, charge
   capped at 360 px/s. Hard/Furious timing and speed unchanged (verified against the switch).
3. **Below-screen units and the wave cap** (`WF14_CAP_OFF`). game.js's dispatcher counted units that
   had scrolled fully past the bottom edge until they were culled. `probe_cap_offscreen_1104.py`
   measured this holding a due wave 0-2.5 s per stage (longest 1.1 s): turrets on Stages 2-3, Stage 4
   convoy units, drones, s8deathorb, cometsm. One hook line in game.js after the naval exclusion calls
   `wf14BelowScreen(e)` (top edge > VH); the rule and switch live in WF14.

**Verification:** `_BUILD_SOURCE/probe_wave_followups_1104.py` 14/14, zero page errors. test_fl stops
at the same pre-existing `difficultyHealthBaseline15 is not defined` (combat_polish_0927b.js).

**Density, for reference:** `DIFF.density` (1.0/1.25/1.5) looks like a "more enemies per wave" dial
but buildStagePlan reads it and never uses it. Left alone.
