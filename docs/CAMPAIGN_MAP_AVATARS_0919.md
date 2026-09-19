# Fullscreen campaign map and pilot avatars

The campaign map keeps the native 480 x 512 game canvas for its controls and draws the same camera, ocean, islands, shadows, and clouds across the widescreen viewport in `assets/wide_map_world_0919.js`. Outlying unlocked islands remain clickable. The stage row has a dark backing for readability over the world.

All nine compact pilot avatars use one approved 256 x 256 frame template at `assets/game/pilot_avatars/avatar_frame_template_0919.png`. Their faces come from `assets/game/pilot_portraits/<pilot>-idle.png`; the generator applies pilot accent colors and writes `pav_<pilot>.png`. The pilot select cells and widescreen dossiers load these same avatar files. When an idle portrait changes, run:

```powershell
python _BUILD_SOURCE/rebuild_pilot_avatars_0919.py
```

Verify the fullscreen map and an out-of-canvas island click with:

```powershell
python _BUILD_SOURCE/probe_wide_map_0919.py
```
