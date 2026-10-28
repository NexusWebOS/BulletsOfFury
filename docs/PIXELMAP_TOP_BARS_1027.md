# Complete R and 5 top bars — October 27, 2026

Mike identified missing top edges in the Fury28px READY50/50 specimen. The authoring defect was the sequential upper-left corner scoring in build_fonts.py: after clearing a pixel, its next neighbor was tested against the newly cleared pixel and was also erased. The entire first face scanline could disappear. Thin R/5 top bars showed the loss most clearly.

The scoring pass is removed. Capital and numeral top silhouettes now come entirely from the authored HEAVY masters. Native font PNG/JSON/FNT exports, Aseprite sources, compiled runtime banks and the downloadable font pack were rebuilt. The glyph inspection sheet has non-overlapping rows, so Command labels no longer paint over the enlarged Fury sample. Runtime source/asset version is glyph-tops-1027c.

Validation:288 source capital/numeral top rows across8 palettes,192 compiled R/5 top-thickness checks across12 Fury sizes and8 palettes, and192 checks through the actual game renderer all pass. The27-bank R/r connectivity,0/8 counters, bounds and digit-spacing checks remain green. Refreshed native menu/HUD/dialogue screenshots have no browser/console errors. Syntax check passed. This correction changes authored font assets and review layout; no gameplay behavior was changed. The previous full game suite's five known failures are not reclassified or claimed fixed.

Preview: http://127.0.0.1:50240/_shots/pixelmap_fix_1027/index.html?rev=glyph-tops-1027c#r5-tops

No paid generation, commit or push.
