> Historical: Mike rejected this eight-vertex approximation. Current implementation traces original metal-frame pixels; see [PURSUIT_TRACE_EXACT_1115.md](PURSUIT_TRACE_EXACT_1115.md). Evidence below describes the superseded pass.

# Traced pursuit-card frame flash - November15

Mike requested tracing each new selection box and adding its flashing outline alongside the existing arrow. Both Hard/Furious menus now have their selected card's complete chamfered metal perimeter pulsing green/white in16 authored phases. The arrow remains and uses the exact same menu clock/phase. Changing left/right immediately moves both markers. Aircraft, typography, footer and unselected card pixels remain unchanged.

Four manually traced contours follow the original card frames. Native source canvas456x256; static crop/origin per bank; even206x158 and204x158 cells,16 separate phases each, four8x2 PNG pages below4096. Runtime uses native-size pre-authored frame blits, not canvas paths, glow/filter/opacity/scale effects. Load registry assets/pursuit_trace_art_1115.js immediately before the existing assets/city_rescue_1115.js owner. Native inputs, confirm briefings and actual encounters remain owners; no gameplay/camera/resolution/dialogue changes in this pass.

Editable layered Aseprite-format sources, traces/palette/timing and manifest are retained under _ART_SOURCES/pursuit_trace_1115. Aseprite executable was unavailable on this host; no GUI/CLI use is claimed. Official-format source authoring plus independent decode verifies all64 visible RGBA composites and source timing. Hidden locked reference layers stay out of runtime exports. Default _BUILD_SOURCE/pursuit_trace_1115_build.py exports retained source layers; --author deliberately recreates sources from the trace recipe. The exact export of all4 atlas pages and registry is reproduced byte-for-byte. See the source README for this decoder's supported subset and format reference.

150/150 native/GIF/name checks pass, with no page/console/HTTP errors. Tests exercise actual left/right keyboard events on both menus, all16 matching arrow/outline phases, real pointer confirmation and the actual5-member Rough Riders encounter. At each of the four card states, a native with/without marker comparison proves every changed pixel lies inside its registered perimeter; the other card, aircraft, text and footer are byte-identical. All5166 sampled current/fallback dialogue lines retain Rough Riders naming. No physical8BitDo test or campaign win is claimed.

Full suite8,969 passed/0 failures/exit0; failing-name comparison stays empty against the previous pass. Syntax checks pass. assets/game.js is unchanged LF, test_fl.js unchanged CRLF. Rough Riders naming, Bulletalica, the mandatory StageX/Stage7 flow and all other prior work remain. No commit, push, installer or release.

Three native912x512 GIFs show actual menu input:4s Hard,4s Furious and8s combined (Hard then Furious). Shared-palette export and transparent changed-rectangle compaction preserve every decoded timing tick pixel-for-pixel.5/5 actual GIF browser checks pass, including changing composited screenshots and no page/console/HTTP errors. Combined GIF is968,069 bytes. Older arrow-only GIFs and previews remain intact.

Review: http://127.0.0.1:8766/_shots/pursuit_trace_1115/review.html

Native capture/pixel/GIF recipe: _BUILD_SOURCE/pursuit_trace_1115_capture.py. Temporary evidence: _shots/pursuit_trace_1115. Durable receipt: docs/qa/pursuit_trace_1115.json. Assets: assets/game/shared/ui/pursuit_trace_1115; source recipe/metadata: _ART_SOURCES/pursuit_trace_1115.
