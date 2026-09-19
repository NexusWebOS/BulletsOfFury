# Yuri portraits and campaign row — 0919

The nine map stage cells now form one horizontal row at the bottom-left of the fullscreen side area; the rank plate remains above each element icon. The left-side background and the right-side pilot dossier remain as before.

Yuri's 12 square portraits now use his current short mohawk, beard, black scarf and red flight suit. The generated source sheet is `assets/game/pilot_portraits/yuri_expression_sheet_0919.png`; run `python _BUILD_SOURCE/build_yuri_portraits_0919.py` to extract the separate idle, anger, crash, happy, laugh, sad, victory and five talking-mouth portraits. The old black-haired images at the same `pilot_portraits/yuri-*.png` paths were replaced. `pilotPortrait()` and legacy `port_yuri_*` requests now resolve to this new set; the older seven-expression `yuri_v2_*` keys also point to these files. The current mohawk `comm_portraits_0914` and pilot-body references remain available.

Verify with `python _BUILD_SOURCE/probe_yuri_portraits_0919.py` and `python _BUILD_SOURCE/probe_widescreen_0918.py`.
