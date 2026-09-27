# Stage 5: full-size Retina row across the entire map

Mike clarified that the original Retina size must remain, and scrolling into off-screen space must not bypass the attack. This supersedes the viewport-sized row in `HAMMER_RANDOM_SPIKES_0926.md`.

The measured Stage 5 world is **680 logical pixels wide**, versus a **480-pixel camera view**. Restored Retina draw width: **96 pixels**. Five Retina widths fit one view; the attack now extends across the entire world instead of stopping at the camera edges.

The current map uses **eight world-fixed positions: x = 4, 100, 196, 292, 388, 484, 580, 676**. The outer positions deliberately sit at the map edges, preventing the player from parking beyond the first or last spike. Their graphics naturally extend past the viewport at those edges; they are not resized. About five Retina widths are visible at once, and scrolling reveals the others. The count is calculated from the authoritative world width and the fixed 96-pixel footprint, rather than a hardcoded camera count.

The row's positions, activation order and timers do not follow the camera. Off-screen columns continue their normal warning and eruption sequence. The randomized order, green/yellow/red Retina glow, full second of red warning, matching red damage-zone preview, 75%-height spike reel and harmless residual sparks remain. Spike radius returns to its original 20 pixels. Ordinary hammer throws remain free of extra warning overlays.

## Verification

- Syntax check passed. Full suite: **5,021 passing, zero failures**, exit 0 and final success banner. No failing names compared with the prior 5,012/0 baseline. Log: `_shots/test_fl_world_spikes_0926.log`.
- Real Chromium: measured world/view/Retina dimensions **680/480/96**. The exact same row was rendered at left, center and right camera positions, and screenshots were inspected.
- Six native movement cases: Normal/Hard/Furious, both directions. Each starts in the center and holds movement to the map edge. The camera reaches x=0 or x=200; the row's world positions, sizes and delays remain unchanged. The player at x=10 or x=670 is hit when that edge spike rises. Scrolling therefore does not move or remove the hazard.
- Existing three-difficulty phase loops, all nine ordinary/space/Retina hammer counters, red-window escape checks, visible-shaft collision, generated sprite edges and rendered red-zone coverage pass. **Zero page or console errors.** Durable report: [qa/hammer_world_row_0926.json](qa/hammer_world_row_0926.json).
- The first edge simulation omitted the camera update normally called by rendering, so its camera-travel assertion failed even though edge damage already passed. The fixture now calls the real camera update, and passes. Logs preserved as `_shots/probe_world_spikes_0926.log`, `_shots/probe_world_spikes_0926_recheck.log`, and `_shots/probe_world_spikes_0926_final.log`. A paused impact flash was cleared in the three static camera-comparison fixtures; gameplay is unchanged.

Preview: `_shots/hammer_world_row_0926/review.html`, with a new scrolling encounter recording and separate counter-throw clips. These are native canvas recordings from controlled invulnerable, muted fixtures, with the unrelated asteroid stream suppressed only in the preview. They do not claim an unassisted campaign balance run.

No new assets, resized source images, atlas changes, commits or pushes. Game LF and test harness CRLF retained; existing unrelated work preserved.
