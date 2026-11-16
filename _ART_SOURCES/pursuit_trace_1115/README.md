> Historical source: rejected simplified contour. Use _ART_SOURCES/pursuit_trace_exact_1115 and docs/PURSUIT_TRACE_EXACT_1115.md.

# Pursuit card perimeter markers

Mike requested tracing each new pursuit card and flashing its frame alongside the existing arrow. Four manually registered eight-vertex contours follow the metal chamfers on Hard/Furious left/right cards; paths.json retains the original912x512 image-space points. Current menu masters retain their typography and aircraft.

Native source canvas456x256; one1/2 proportional registration to the source-image grid. Three layers in each16-frame .aseprite: hidden locked reference, visible rim, visible pulse.16 distinct authored RGB palettes and opaque stroke pixels. Fixed crop/origin per bank, transparent safety margins, even206x158 or204x158 native cells. Four8x2 PNG pages fit4096 texture limits; all64 source cels remain separate.

The recorded Aseprite executable is not installed on this host. No GUI/CLI use is claimed. Layered .aseprite files were authored to the official RGBA file format with sRGB profile, compressed/linked cels and a selected-green-white tag. An independent source decoder checks all16 visible composites and timings against export. Source-format reference: https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md

Retained .aseprite sources are authoritative. Default python _BUILD_SOURCE/pursuit_trace_1115_build.py exports their visible layers. --author explicitly recreates sources from the original hand-trace recipe and palette; use it only to replace source edits intentionally. Hidden reference layers never enter runtime PNGs. The decoder supports the current normal RGBA layer/compressed-and-linked-cel subset, not all Aseprite features.

Registry assets/pursuit_trace_art_1115.js loads immediately before assets/city_rescue_1115.js. city16Trace chooses difficulty/side at16fps from the same native menu clock as the retained arrow. Native cell blits use static origins with no runtime outline drawing, scaling, glow, rotation, opacity animation or filters. Native pixel isolation compares with/without only the new marker and requires all changed pixels to remain inside the selected perimeter mask. No new menu input, route, dialogue, gameplay or camera rules.
