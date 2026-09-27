# Stage 5: framed warning signs, difficulty speed and recovery

Mike requested the existing warning signs instead of bare asterisks, much faster Hard/Furious spike rises, and a smoother return to the boss's area. This supersedes the bare symbols and shared rise speed in `HAMMER_ROUND_ZONES_0926.md`.

## Warning signs and spike timing

The row uses the authored, metal-framed triangular `bmfx_badge_green`, `bmfx_badge_yellow` and `bmfx_badge_red` signs. These are the existing hazard-sign plates, including their central warning mark; no new symbols were drawn. The frame was inspected, then verified through the real game's `XART.get` and canvas rendering. Signs stay beneath the boss gauge, respect their full aspect ratio at the world edges, and share the Retina's absolute release timestamp.

| Difficulty | Rise rate | Full-height rise | Gap between eruptions |
|---|---:|---:|---:|
| Normal | 1× | 0.380 s | 0.50 s |
| Hard | 1.8× | 0.211 s | 0.30 s |
| Furious | 2.8× | 0.136 s | 0.20 s |

The rise rate is committed to each spike when the row is created. Only the rise accelerates; the authored peak hold, collapse and harmless residual sparks retain their timing. Rendering, visible-shaft collision, red-zone disappearance and cleanup use the same adjusted reel clock. Every difficulty retains the three-second green/yellow/red countdown, including a full second of red before eruption.

The full-width round columns, 96px Retinas, eight world-fixed positions, off-screen coverage, newly shuffled order each slam and 75%-height peak remain.

## Recovery

Previously the post-slam recovery moved linearly toward the current camera center, so scrolling could change his destination mid-return. The charged-hammer phase now owns a fixed world-space home at **(340, 174.08)** on the current Stage 5 map.

After impact, five existing authored poses play in order: impact, follow-through, lifting the hammer free, lowering it, and settled idle. Retreat begins after 0.62 seconds, with zero-speed endpoints and a quintic easing curve. Its duration accounts for travel distance. The destination is captured once; the return does not chase the camera, overshoot or switch attacks before reaching home. The hammer remains lowered during return and the following idle. Existing source art and measured chest/head anchors are reused.

## Verification

- `node --check assets/game.js` passed. LF retained; `_BUILD_SOURCE/test_fl.js` CRLF retained.
- Final full suite: **5,048 passing assertions / 0 failures**, exit 0 and final success banner. Previous baseline: 5,033/0. Log: `_shots/test_fl_sign_recovery_0926_final.log`.
- Initial full suite exited 1 with **5,047 passing / 1 failing**: `Archmage storm recovery: normal asterisk ends at eruption`. Subtraction roundoff could keep the sign visible at an exact release timestamp. It now compares the same absolute timestamp as the Retina. The final full-suite rerun and native probe pass. Initial log retained at `_shots/test_fl_sign_recovery_0926.log`.
- Native Chromium measured peak rises of **0.381 / 0.212 / 0.136 seconds** in 1ms sampling. All authored rising frames remained present, and the red warning is still one second on all difficulties.
- Six return cases (both sides × three difficulties) play poses **7, 8, 9, 10, 11**, reach the exact fixed home, remain within their start/end bounds and settle while the camera repeatedly changes sides. Maximum displacement is **6.873 logical pixels per 60Hz step** on the longest tested return; no destination snap.
- Full row/camera-edge tests, actual sidestep escape, warning pixel coverage, all three phase loops and all nine counter routes pass. **Zero page or console errors.** Durable evidence: [qa/hammer_sign_recovery_0926.json](qa/hammer_sign_recovery_0926.json). Initial and final native logs: `_shots/probe_sign_recovery_0926.log`, `_shots/probe_sign_recovery_0926_final.log`, `_shots/probe_sign_recovery_0926_recheck.log`.
- Inspected screenshots and native-video contact sheets for all difficulties. The review page loads three 24-second clips and its images without browser errors: `_shots/hammer_sign_recovery_0926/review.html`. These are muted, invulnerable inspection fixtures with unrelated asteroids suppressed, not complete campaign playthroughs.

No new asset generation, atlas edits, commits or pushes. Existing work preserved.
