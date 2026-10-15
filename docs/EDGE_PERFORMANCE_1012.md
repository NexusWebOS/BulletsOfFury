# Main-game Edge performance — October 12, 2026

Mike reported stuttering while moving, firing and exploding enemies in Edge on
an unplugged Ryzen 7 7000-series/Radeon laptop with 16 GB RAM.

## Installed changes

- Siege Console retains its authored housings and repaints only wells whose
  displayed data changes. Radar and animated equipment still update each frame;
  readiness, pilot/theme changes and co-op seats invalidate the appropriate wells.
- The frame loop skips the hidden old HUD under the Siege Console. Its hidden
  split canvases also stop copying. Explicit recording retains the previous path.
- Retiring the sprite cache now resets its byte counter with its plates; old
  stages could otherwise leave the next stage evicting useful plates repeatedly.
- Explosion sparks resolve each shared sprite/colour once per draw. Their count,
  positions, colours, durations and authored frames remain unchanged.
- Updated runtime cache stamps ensure the installed files reload.

No simulation clock, collision, projectile limit, gameplay or art changes.

## Evidence and limits

The paired headless Edge HUD measurement at 1366x768 is sequential, with the
published renderer and installed renderer in the same browser session. Mean HUD
submission time fell from 1.03 to 0.43 ms at normal CPU speed and from 3.67 to
1.69 ms under 4x CPU throttling (about 54-58% less HUD CPU work). These are HUD
measurements, not a claim that whole-game FPS doubled.

For 224 explosion particles, sprite/tint calls fell from 224 to 2 with zero
changed framebuffer bytes. HUD dirty/full repaint differs only by less than one
premultiplied colour unit at translucent bezel edges. Cache retirement, hidden
HUD skipping and menu round trips pass. Final Siege Console native probe: 51/51.
Final full base regression reaches its zero-error banner and exits 0; all four
changed runtime scripts pass syntax checks.

Two short protected live Edge runs exercise actual loop updates, movement,
weapon firing and repeated explosions. Stage 1 peaked at 83 player shots and
714 effects; Stage 6 at 12 player shots, four hostile shots and 364 effects.
Both remained in play with finite coordinates and no browser errors. Their
observed rAF rates were about 55 and 60 FPS on this host at SS=2. The user laptop,
battery throttling, all stages and sustained thermals remain unmeasured.

Earlier frozen combat screens included first-use effect warmup and overlapping
QA runs. Their aggregate FPS is not used as before/after evidence. Edge's favicon
request receives 204 in the verification server; it is not a game asset.

Portable results: [performance QA](qa/performance_1012.json).
Screenshots inspected in `_shots/performance_1012/live` and `paired`.

```powershell
python _BUILD_SOURCE/probe_edge_performance_1012.py
python _BUILD_SOURCE/probe_edge_live_1012.py
python _BUILD_SOURCE/probe_siege_console_1012.py
node _BUILD_SOURCE/test_fl.js
```

Run timing probes alone. They require installed Microsoft Edge and Playwright.
The 4c3f7b269 reference functions ship beside the probe for repeatable comparisons.
Changes are local only; no commit or push was requested.
