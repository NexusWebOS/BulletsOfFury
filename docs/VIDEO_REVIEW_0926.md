# September 26 gameplay video review

Source recordings: `11-48-32.mp4`, `11-49-38.mp4`, and `11-55-56.mp4` in Mike's Videos folder. Review frames and local Chromium captures are in ignored `_shots/`.

## Repaired in this pass

- Player-position jumps: the modular ground-turret renderer restored the canvas state twice after one save, which could remove the world/camera transform for everything drawn afterward. Its save/restore stack is balanced; turrets retain a map position, reproject with terrain scroll, and cannot be displaced by enemy separation. Camera shake now follows a continuous wave rather than a new random offset each frame.
- Missiles: manual gmiss impacts deal direct damage to bosses, minibosses, and enemies even without a retina lock. Space-volley lock range reaches distant Stage 5/9 targets. Launch and routine impact shake were removed.
- Stage 6 crowding: ally-assisted spawn pressure, the simultaneous random-enemy cap, and allied missile/special cadence were reduced. Stage 6 and 9 ordinary death-smoke rings are smaller and shorter. Scripted squadrons can still overlap, so the battle needs a deliberate encounter/composition pass.
- Stage 5/6/9 hit legibility: ordinary full-white enemy flashes now use a shaded blue pulse, retaining the hull's colors and outlines. A Chromium trace confirmed that Stage 6 hulls no longer request full-white hit tints; remaining white tint calls there were small explosion/spark effects. Event Horizon uses separate warned fork, fan, and ring volleys. Twin sentinels start staggered and fire less often. The Tidal Sovereign's ordinary volleys have longer, committed warning paths; its final radial volley leaves three adjacent safe directions. Its hit pulse also leaves the hull visible.
- Stage 5 Chromium beam: the flat rectangle now uses the authored two-cell energy column from `arch_effects`, anchored at the boss's core. Its active duration is shorter and bomb cadence less dense; both side lanes remain open. The whirlwind warning follows its horizontal sweep.

## Evidence

- `node --check assets/game.js` and the full `_BUILD_SOURCE/test_fl.js` suite reached the final zero-error summary after these edits.
- `_shots/probe_video_regressions_0926.json`: ordinary boss missile damage without retina, Stage 9 space-volley lock and damage, stationary turret and preserved canvas transform; no page/console errors.
- `_shots/stage9_boss_warning_0926/` and `_shots/stage9_boss_phase3_0926/`: warning positions and angles match released projectiles; no page/console errors.
- `_shots/stage9_boss_hit_0926/` and `_shots/stage9_hit_pulse_0926/`: visible Stage 9 hull detail during hits; no page/console errors.
- `_shots/hammer_beam_0926/`: authored beam rendered and boss advanced from the active beam into its next phase; no page/console errors.
- `_shots/stage6_white_tint_log_0926.json` and `_shots/visual_0926_stage6_tints_after/`: the Stage 6 hull flash trace and a post-change battle frame; no page/console errors.

## Still open

- The HQ screenshot does not establish that the pilot source art contains a white matte. The cited source atlas cells contain few white pixels. A specific affected cinematic frame is needed to distinguish an art issue from an on-hit overlay or compositing issue; do not recolor all pilots on guesswork.
- Stage 5 whirlwind still rotates a single composite pose. It needs a proper authored frame sequence and another visual gameplay pass. The Chromium attack now reads better, but its overall phase choreography and fairness need manual play on each difficulty.
- Stage 6 remains visually busy when multiple ally attacks and enemy deaths coincide. Its opening pacing, encounter spacing, and large FX need a full manual playthrough, not just fixed-time captures.
- Stage 9 encounter pacing and both boss fights need a full manual playthrough on Normal, Hard, and Furious. The present Chromium checks verify attack geometry, not overall difficulty or enjoyment.
- Cinematics need a separate editing pass for movement, character identity/poses, and dialogue-to-action continuity. Existing timing edits in `assets/campaign_story_0924.js` predate this review and were preserved.
