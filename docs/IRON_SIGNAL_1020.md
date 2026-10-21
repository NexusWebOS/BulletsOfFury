# BOF Iron Signal — October20

Mike requested a better dialogue/cinematic font: militant meets digital. The new
PixelLab-generated BOF Iron Signal Bold uses squared block capitals, heavy stems,
clipped corners and restrained stencil gaps. The selected generation is job
cfa58012-3393-419d-acf3-3b3de1b398e5 / asset521976eb-4e8a-5749-b840-40a1b347c86c,
seed10202026,16px/Bold, reported15 generations or$0.115credits. No additional
font generations were used. Prompt and untouched source atlas/TTF are archived
in _ART_SOURCES/iron_signal_1020/request.json.

The source is128×160:8columns×10rows, despite the tool description's10×8 wording.
Character order was visually verified. Runtime uses73 visible glyphs in a200×160
white-alpha sheet with20-square padded cells, a14px line height and13px baseline.
Generated minus/plus strokes were malformed and the dollar exceeded the shared
line; those three and supplemental punctuation use existing Command art at one
uniform2x scale. Other generated glyph pixels retain their original proportions.
All printable ASCII, smart quotes/dashes, arrows and supported dialogue symbols
resolve. Runtime is caps-only; lowercase input maps to uppercase.

New standalone font registration runs after command_0914/fonts.js and before
game.js, replacing only the dialogue/cutscene BMF aliases. Existing layout and
typewriter owners continue to measure and draw the same face. HUD/menu/stage
display faces, pilot names/colors, portrait geometry and full-shaped nameplates
retain their current owners. The game core and full regression harness are
byte-identical to the prior passing build. No gameplay modifications.

The browser loads just the generated fonts.js plus the PNG:11,034bytes; no system
font, font service, text-image request, CSS font swap or additional animation loop.
The optional corrected BOFIronSignal-Bold.ttf mirrors the accepted runtime masks
for future UI/template use. Original generated TTF remains archived separately.

Builder:_BUILD_SOURCE/build_iron_signal_1020.py emits the sheet, metrics, font
registration, audit and corrected TTF together. Runtime:assets/game/shared/fonts/
fonts/iron_signal_1020/. Role registered in assets/data/ART_TAXONOMY.json.
No existing atlas is repacked.

Verification:41/41 native Edge checks and4/4 artifact checks pass, no page, console,
draw or missing-asset errors. All9 pilots/Dracodia;390×844,1366×768,1920×1080;
long messages, portrait-free messages, color glyphs, typewriter stability and
ending captions. Native glyph specimen and actual dialogue/cinematic screenshots
visually inspected. Even cells, clear margins,14px line containment, TTF ASCII
coverage and protected file hashes checked. Full campaign regression was not
rerun for this font-only change. Probe:_BUILD_SOURCE/probe_iron_signal_1020.py;
report:docs/qa/iron_signal_1020.json; review:_shots/iron_signal_1020/review.html.
Cache:iron-signal-1020. Local only; no commit/push requested.

## October20 alignment correction

Mike correctly identified uneven letters in the actual sentence screenshot. The
generator supplied13px A-H/several digits but12px remaining capitals. Merely
sharing a line box did not align their visible caps, and independent destination
rounding made that mismatch visible at small sizes. The builder now normalizes
cap bodies proportionally to12px, places them at top1/baseline13, and retains Q's
1px tail. Digits, exclamation/question marks and cap-height symbols follow the
same rule. Small punctuation and the currency bar retain their appropriate
bearings/overhangs. No independent horizontal/vertical stretch or new generation.

The corrected atlas/embedded map/optionalTTF are regenerated together. Source
20-square cells,200x160 sheet and14px line remain. Previous exports and builder
are archived under _ART_SOURCES/iron_signal_1020/exports_before_alignment_1020/.
The playable folder now uses iron-signal-aligned-alpha.png and its matching map.
Both the registration URL and atlas filename change to prevent stale caches:
fonts.js?v=iron-signal-aligned-1020 / map revision aligned-2.

Native Edge76/76, zero browser errors. In addition to the prior dialogue fit/color/
portrait/typing checks, actual top/bottom pixels are compared through bmfDraw and
bmfDrawOn at17 sizes8..28px (including9.6,13.75,16.384,23.04) and3 fractional
origins. All capital/digit raster cap lines and baselines agree; Q's tail is
checked separately.4 artifact checks verify bitmap metrics, even cells, matching
TTF bounds and exact unchanged hashes for game.js/test_fl.js/command_ui_1020.js.
Full campaign suite not rerun for this font-only correction.
Probe:_BUILD_SOURCE/probe_iron_signal_alignment_1020.py;
report:docs/qa/iron_signal_alignment_1020.json;
review:_shots/iron_signal_align_1020/review.html. The earlier review URL redirects
to this current review. No new generation charge. Local only, no commit/push.
