# Stage 5: bottom-row chromium sweep

Mike's September 26 correction supersedes the spike layout and throw-warning behavior in `HAMMER_STORM_0926.md`.

## Behavior

- Ordinary hammer throws and angry spiral retaliation use the visible overhead wind-up alone. Their FOV cones, ground Retina markers, alert symbols and warning beeps are removed. Spin audio, wind-up timing, projectile counters, magnetic catch and random left/right spiral remain.
- Charged hammer slams reveal one committed row of Retina markers across the bottom. Normal/Hard/Furious retain 3/4/5 columns. The first slam sweeps left to right; the next reverses. Glow/eruption starts are spaced 0.40/0.36/0.32 seconds apart by difficulty.
- The regenerated 16-frame chromium needle rises from the marker into a peak **384 logical pixels high: 75% of the 512-pixel game canvas**. At the standard view its foot is at y=430 and tip at y=46. Frames include ground glow, rising shaft, electric pulses, breaking/retraction and fading residue.
- Damage follows the visible shaft's current frame, height and taper. Unrisen space, gaps between columns, decorative foot sparks and the final residue are safe. This replaces the old small damage circle at the base.
- Retina markers remain visible where the right-hand LOCK/radar overlaps the ground row. A narrowly clipped redraw uses the exact world camera/zoom/shake transform after the HUD; the HUD's position and ordinary behavior are unchanged. Special ability overlays remain above it.

## Art

Generated with the built-in `image_gen` tool. Installed unchanged RGBA PNG:

`assets/game/stage5_archmage_0916/combat_0926/chromium_spike_tall_v2.png`

Exact initial/revision prompts, source path, frame dimensions and measured anchors: [hammer_bottom_row_art_0926.json](hammer_bottom_row_art_0926.json). Sixteen frames, eight columns, measured row boundary y=576. Original short sheet preserved. Runtime registration and ART_TAXONOMY updated together. No atlas repack or generated manifest edits.

## Verification

- `node --check assets/game.js`: passed.
- Full `_BUILD_SOURCE/test_fl.js`: **4,997 passing, zero failures**, exit 0, final `FALVA/LIZZIE BUILD OK, 0 ERRORS` banner reached. `_shots/test_fl_bottom_row_0926_final.log`.
- Initial full run exited 1 only on `Chrome Hammer leap warning: boomerang`, an older assertion requiring the warning Mike explicitly removed. Updated that requirement while preserving leap warnings and throw timing. Initial log retained as `_shots/test_fl_bottom_row_0926.log`. The final run has no failures, including the previously intermittent road-tank/drone assertions.
- Real Chromium, `_BUILD_SOURCE/probe_hammer_storm_0926.py --record`: Normal, Hard and Furious native phase loops; all nine ordinary/space/Retina counter routes; visible upper-shaft damage, harmless warning and safe outside area; single row; measured maximum height 384; zero throw warning/Retina/clock calls; all sixteen spike cells clear at their opaque edges; original charge/throw/overhead pose edges clear. **Zero page or console errors.** Durable result: [qa/hammer_bottom_row_0926.json](qa/hammer_bottom_row_0926.json).
- Inspected real canvas frames of the row, sequential growth and warning-free wind-up, plus extracted video contact sheet. Three new real-canvas recordings and review page: `_shots/hammer_bottom_row_0926/review.html`. Earlier review links to the revision.
- Game LF and test harness CRLF preserved. Existing unrelated staged/unstaged/untracked work retained. Nothing committed or pushed.

The clips use controlled invulnerable fixtures with muted sound; the unrelated asteroid stream is suppressed only in the preview. Counter clips inject a native player bullet and select each available spiral side. These are focused behavior/visual checks, not complete unassisted campaign playthroughs or a claim of final balance approval.
