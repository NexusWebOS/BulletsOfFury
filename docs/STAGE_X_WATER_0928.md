# Stage X animated ocean

Removed the painted ocean from `assets/game/furious_review_0927/stagex_terrain.png` using built-in image generation. The transparent industrial foreground now renders over the existing four-frame authored ocean reel (`nlq2_water` -> `nwl_water`), at 5 fps with independent flow. A subdued ocean backing preserves projectile contrast. Stage X takes precedence over the regular stage background.

Native Chromium verification: `_BUILD_SOURCE/probe_stagex_water_0928.py` checks four decoded water frames, zero alpha in the former water channel, changing water pixels with stationary terrain, and Stage X encounter persistence. Actual screenshots are under `_shots/stagex_water_0928`.

Original output: `C:/Users/Mike/.codex/generated_images/01a0c9fd-a6cc-73a3-8dca-3e0f7a90a956/exec-210f4793-4ef9-4f5e-a665-f352e550f3c4.png`

## Final prompt

Edit the supplied exact game terrain tile: REMOVE ALL WATER to true transparency. This is a precision background extraction for a layered 16-bit game. Keep ALL solid industrial platforms, walkways, buildings, pipework, support pylons, reactor structures and their cyan/amber lights exactly in the same positions, same scale and same pixel art design. Remove the entire blue ocean, waves and white/cyan foamy water surrounding every pylon, including all narrow water channels and small gaps between platforms. Those regions must be fully transparent alpha=0, not black, not gray, not a checkerboard painted into the image. Preserve crisp opaque solid metal silhouettes and pillars down to their bases; do not erase cyan machinery lights. No new objects, no redesign, no layout changes, no camera changes, no crop. Output same portrait 2:3 full tile composition with transparent empty middle water lane and transparent former water gaps. Opaque terrain foreground only, to be composited over animated water.
