# Crossed Fate source art — November 15, 2026

Original BOF. Storm Cannon is the current internal Thunderhead/FB112/TC119 modular rig, renamed only for display. Both headings were captured from its actual native renderer, including the real module placement and exhaust. HF28's current closed/broken Harrier plates were captured as the actual Harrier references. No replacement aircraft were generated.

The two achievement medals were generated with the built-in imagegen tool against the existing general-family medal, expansion/topdown/art/menu_1011/od_general_0.png. Generation brief: two separate gold/laurel/navy 16-bit achievement medals, a blue-steel cannon core with crossed lightning and forked paths for Crossed Fate, and exactly five rust-red fighters over a forked flight trail for the alternate Rebel victory. No lettering inside the medals. This is a provenance brief, not a verbatim generation transcript. Original imagegen output is retained as generated-medals.png (1774x887 RGBA).

Each generated tile is 887x887. Both share one alpha crop [0,4,887,887] and one proportional nearest-neighbor scale fitting 228 pixels, centered on even 256x256 cells at pivot128,128. No per-tile fitting. Native aircraft cells retain 800x800 source canvas/pivot400,400. Each whole bank shares one even alpha-union crop and adjusted common pivot. Native Storm NW/west animations have16 frames each, shadows retain27% alpha. The Harrier crash uses48 registered authored poses over720 degrees; straight-flight hulls retain one actual plate. No runtime flat-plane rotation for these overlays. Lossless WebP pages pack at most16 cells with no scale changes.

manifest.json owns all crop, pivot, timing-bank cell, page and content-hash contracts. Source *-NN.png files preserve full800 cells. storm-native-* and harrier-*.png preserve direct native exports. The shipping registry is assets/crossed_fate_art_1115.js.

Run python _BUILD_SOURCE/crossed_fate_1115_pack_saved.py to reproduce every shipping page, both medal PNGs and the registry in memory and compare exact hashes without writing shipping art. The build recipe can regenerate from retained project sources; inventory.py can recapture current native references via the local game server. Do not re-run an old capture against a different approved aircraft revision without reviewing the result.

Runtime owner: assets/crossed_fate_1115.js. Native combat, protection, hit, death, rewards, results and city encounter owners remain intact. See docs/CROSSED_FATE_1115.md for branch behavior and verification scope.
