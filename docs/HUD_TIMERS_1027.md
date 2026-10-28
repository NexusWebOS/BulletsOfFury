# Square pilot bay and live stage/encounter clocks — October 27, 2026

The Fury R has a complete double-row top/bowl across all twelve display banks and eight palettes. Its spacing, baseline and all other glyphs are retained. The bank version is solid-r-square-hud-1027d.

A new generated right-HUD portrait bezel has straight inner edges and a fixed 228x228 square aperture. Full native pilot boxes fit without corner clipping or aspect distortion. The lower 640 pixels of the original right HUD are unchanged. The name strip has its own narrower measured text limit.

Stage Completion counts active native simulation time across waves and encounters; it does not reuse the wave-progression timer, which pauses during boss fights. The right header starts a fresh Miniboss/Boss clock on each new actor, includes its entrance, continues across the same actor's phases and holds on defeat. Pause and menus stop both clocks. A new stage/retry resets both. The result screen snapshots full completion time; existing rank/reward formulas and the original internal fight clocks are untouched.

Both clocks use fixed authored steel housings and bitmap text. Wide layouts put them above the left and right HUD columns, clear of the fullscreen control. Compact layouts put the pair immediately above the compact HUD. Co-op shares the stage/encounter clocks above its two native HUD rows.

Verification: 41 native browser checks pass, including ordinary waves, pause/resume, miniboss→boss reset, result snapshot, retry, all nine full portraits, names, four viewport sizes, fullscreen clearance, co-op and menu cleanup. No final page, console or HTTP errors. 96 source top-bar checks pass. Actual native screenshots were inspected. Syntax checks pass. The full 389-case suite reaches its summary and exits1 with the same five prior failures: hit-flash hold, Chronos opening dialogue/jump order (two), and StageX route persistence/launch (two). The existing result snapshot assertion now verifies the frozen result value without pinning the retired time source.

Generated raw source, precise aperture cleanup, fixed header variants, manifest, builder and editable Aseprite exports are under _ART_SOURCES/hud_timers_1027. No paid PixelLab credits, commit or push.
