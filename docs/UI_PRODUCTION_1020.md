# Command Armor HUD, pilot dialogue and reusable UI kit â€” October 20

Mike selected Command Armor (A) for the main game and asked to retain all three HUD/dialogue designs for expansions. His later feedback rejected the cropped Cole actors and their facial drift. The final Cole bank has four complete head-to-boots frames derived from one corrected full-body identity master and the user-approved portrait sheet. The approved existing talking portraits are preserved.

## In the game

- Left: Roll and Somersault solid fill/readiness, real pilot ship/lives, missiles, primary ability and its current duration/charge, separate secondary ability/count/status.
- Right: Actual pilot portrait, pilot-colored name tab, score, high score, equipped weapon/level, solid Speed and Armor meters.
- All nine pilot colors come directly from PILOTS. Dynamic labels, counts and meters are not baked into concept art. Cole's Sonic Boom and nuclear warheads, Lizzie's atom bombs/turret, Decker's cloak/shotgun, Freezer's Thermoshock equipment and Juggernaut's charge remain represented separately.
- Narrow windows use a compact instrument panel. Co-op has independent seat readouts. Existing boss bars remain owned by their encounter HUD.
- Command Armor dialogue uses current animated comm portraits and the dedicated Dracodia portrait. Speaker names use actual alpha-colored glyphs. Original typewriter timing, dialogue ticks and director callbacks are retained. Stage 4/6 radio pages stay in the side HUD alongside secondary ability status; compact mode retains a small score/comms compartment. Their timing owners remain unchanged and the playfield receives no additional radio overlay.
- Cole's new full-body neutral/reporting/worried/speaking masters are 512 Ã— 1024 with one common scale and pivot. The ending frames the upper 512 Ã— 704 region as a camera crop; complete boots/hands remain available in the actual source assets and gallery. His facial likeness is for Mike's visual review; a programmatic check cannot certify a personal likeness.

## Expansion templates

27 pilot/style combinations: A Command Armor, B Cartridge Classic and C Fury Broadcast, each with blank and named portrait versions. B's nameplate AND interior use that pilot's color. 54 HUD rails, 27 blank dialogue frames, 54 named HUD/dialogue plates, nine neutral bases, layout rectangles and extracted portrait/body components. The main game loads only A; B/C live in the source/template library.

Review: http://127.0.0.1:8794/docs/previews/ui_production_1020/index.html

Download: `_ART_SOURCES/ui_production_1020/BOF_UI_Expansion_Templates_1020.zip`

Runtime UI: `assets/command_ui_1020.js`, `assets/game/shared/ui/command_1020/`.
Cole: `assets/game/pilots/cole/body_frames/front_identity_1020/`.
Sources/prompts: `_ART_SOURCES/ui_production_1020/`. Built-in image_gen was used, with no PixelLab calls. Rejected facial/cropped candidates are recorded in provenance and excluded from the playable bank.

## Verification

Native Edge checks cover all nine named/color-matched HUDs/dialogues, actual colored glyph pixels, dual abilities, depleted states, nine-digit score, co-op, 390/1366/2560 viewport bounds, ending shots, Cole aliases, director callback, all 27 library combinations, even dimensions and transparent margins. See `docs/qa/ui_production_1020.json`. The full Falva/Lizzie integrity/behavior harness completed its final BUILD OK with 0 errors. These are UI/state/asset checks, not a new whole-campaign balance claim.

HUD drawing stays in the existing console's scheduled refresh; no new animation loop. Rail redraw signatures quantize meters to visible pixels; static text/icon products are cached. Expansion textures and rejected frames are not preloaded into gameplay. Changes are local; no commit or push.

## Centered dialogue correction â€” October 20

The live dialogue and ending caption owners now share one source-coordinate aperture
map. Nine-slice artwork and content use identical rounded edges. The pilot tint is
a polygon inset within the actual authored nameplate, and the name is centered
using its visible glyph bounds. Body rows are centered horizontally and vertically
from the full sentence before typewriter reveal. Automatic height uses the real
text aperture; the bounded existing UI cache retains the fitted height. Portraits
are contained proportionally and centered in the portrait opening, including
non-square Falva sources. The right HUD portrait uses proportional containment too.
No new artwork or gameplay changes. Native Edge:37/37 checks, zero page/draw/console
or missing-asset errors, at390Ã—844,1366Ã—768 and1920Ã—1080. All nine pilots, Dracodia,
long text, portrait-free messages, typing stability and ending captions covered.
Reviewed native screenshots; full campaign regression was not rerun for this UI-only
layout correction. Probe: `_BUILD_SOURCE/probe_dialogue_fit_1020.py`; report:
`docs/qa/dialogue_fit_1020.json`; review: `_shots/dialogue_fit_1020/review.html`.
Cache version: `command-centered-dialogue-3`. Local only; no commit or push.

### Full inner nameplate fill correction

Mike requested that the color reach the entire inner shape, including the angled
end. The earlier polygon stopped short of the plate edges. The source contour
now follows the full inner plate at top/bottom/left shoulder and angled nose.
Its portrait-side section uses the portrait nine-slice map, and all tint is
clipped inside the plate; the original lamp and bolts remain visible through
holes in the tint. Centered content and proportional portraits are unchanged.
Installed native Edge:38/38 checks, no browser errors; explicit edge samples cover
the formerly unfilled areas. Cache:command-full-nameplate-4. No gameplay edits.

## Military/digital font update

Dialogue/cinematic copy now uses PixelLab BOF Iron Signal. See
docs/IRON_SIGNAL_1020.md for the font builder, sources, corrected punctuation,
small runtime payload and native checks. Existing HUD/names/pilot colors remain.
