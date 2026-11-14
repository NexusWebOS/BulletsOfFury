# BOF hammer animation recovery — November 11, 2026

Chronos and Dracodia copied Chronos use complete character-and-held-hammer drawings. Both downward strikes pass over and behind the head. Faces stay forward; original helmet/horn designs remain. Normal has one down strike; Hard has two; Furious adds left/right sweeps. Follow-ups stay planted after the initial jump.

The recovered .75 export enlarged the overhead bank relative to the established .63 whole-attack source scale and clipped the high pose in native views. These final exports come directly from the original full generated drawings at .63, with 640×640 cells, common 320,320 pivot, and 474 boot baseline. They retain the existing side, throw and catch owners.

Editable Aseprite projects, lossless textures, accepted original drawings, exact generation prompts, canonical references, landmarks and reproducible exporter are included. No head stamping or separately assembled held weapon. Only released flight uses a separate weapon.

Rebuild: run build.py with Python, Pillow, NumPy and Aseprite installed; ASEPRITE may override the executable path. It writes the same fixed-cell exports and registration metadata. source-index.json uses local package paths for the accepted drawings. Historical source paths are provenance only.

Final browser checks and live recordings are in verification/. The clips are attack demonstrations with an invulnerable observer, not full-fight or campaign evidence. Each boss runs in a separate closed browser process. A loading checkpoint was added before pixel capture so a hidden actor cannot pass a flash test.

The game's broad test suite previously exited 1 on the existing missing difficultyHealthBaseline15 helper before its final summary. That unrelated baseline is preserved in verification/full-suite-baseline.txt; this is not a full-suite-green claim.

Installed in C:/Users/Mike/Desktop/Github Coding/BulletsOfFury: assets/overhead_slam_art_1111.js and ten overhead_slam_1111 lossless textures. Core gameplay and native attack owners were not changed by this recovery. No installer, commit or push.
