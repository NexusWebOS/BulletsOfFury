# Dracodia downloaded arenas

Each named folder contains the accepted PixelLab terrain and its matching PixelLab wireframe. All eight plates are512x512 with fixed256,256 pivots. Lava is a transparent72.26percent terrain overlay; the original native nlq3_lava_0..7 animation is rendered below it, not copied into this folder. Other plates are opaque.

download-curtain-32.webp:32 genuine PixelLab PixMiniMax phases,256x256 cells,128,128 pivot,20fps,1560x1560 sheet with2px edge extrusion. Input reference0 is excluded. manifest.json and assets/arena_download_art_1020.js are built together by _BUILD_SOURCE/build_arena_download_1020.py.

Runtime: assets/arena_download_1020.js. Helicopter=jungle, Phoenix=lava, Hammer=space, Harrier=sky. Main Dracodia retains the native void. World-fixed architecture, separate far/near data particles and moving sky clouds. All clocks use native simulation time. See docs/ARENA_DOWNLOAD_1020.md for proof and generation provenance.
