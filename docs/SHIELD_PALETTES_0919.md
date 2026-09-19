# Boss shield palettes

The original 881×82 rectangular `SHIELD` frame remains the default. `shield_frame_volcano_red.png` and four matching red fill states are selected automatically for any boss with `_mwBarrier` (the volcanic barrier). `shield_frame_level5_steel.png` and four matching dark gray/white fills are registered for the future Level 5 shield form; set `boss._shieldGaugeStyle = 'level5_steel'` when that form becomes active. Both variants preserve the original frame's alpha, label placement, and fill geometry.

Regenerate the exact-size palette variants with `python _BUILD_SOURCE/shield_palette_0919.py`. Check the three game-rendered bars with `python _BUILD_SOURCE/probe_shield_palette_0919.py`; its preview is written under `_shots/shield_palette_0919/all_three.png`.
