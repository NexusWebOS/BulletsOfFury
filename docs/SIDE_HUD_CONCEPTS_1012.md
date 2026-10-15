# Side HUD concepts — October 12, 2026

**Selected and installed:** Mike approved the vented **Siege Console (4)**
with his attached plate and “this looks good. continue.” See
[the installed HUD notes](SIEGE_CONSOLE_1012.md) and native verification.
The original concept-only pass below is retained for provenance.

Mike requested side HUDs matching the current Armored Command style, with
square instrument boxes and side bars, and a consistent large playfield
across gameplay, intro fly-ins and continue screens. He requested concepts
for selection before installation. These are review-only candidates.

[Open the five-concept review](previews/side_hud_1012/index.html).

| Option | Direction |
|---|---|
| 1 — Command Bastion | Closest to Armored Command: connected heavy frames and amber indicators |
| 2 — Split Batteries | Separate maneuver, stock and instrument pods |
| 3 — Tactical Rails | Uniform rails with broad display wells |
| 4 — Siege Console | Vented military armor and fewer illuminated seams |
| 5 — Command Glass | Compact beveled frames and recessed illuminated meter strips |

The left column carries score/high score, Roll, Somersault, equipped weapon,
and retained speed/shield bars. The right carries radar, special ability,
lives, missiles and retina lock-on. The latest explicit radar request
supersedes the earlier no-radar direction for this proposed replacement.
Stock digits are large and paired with the native game icons.

## Viewport evidence and proposed layout

`export_side_hud_refs_1012.py` captured the actual game in Chromium through
`shoot.py`, at a 1920 × 1080 browser viewport. The game backing store remained
960 × 1024 (480 × 512 logical), while the visible gameplay/fly-in field was
692 × 738 and the continue field was 984 × 1050. This is a display-fit change,
not a change to the logical gameplay resolution. The live fitter budgets
visible top/bottom HUD bands; other cinematic owners also have dedicated
fullscreen viewports. Details are in the review's `native-references.json`.

Each concept uses a 2048 × 1152 review canvas and one fixed field rectangle
`[484, 0, 1080, 1152]`. The native 480:512 playfield aspect is retained without
cropping or stretching. HUDs sit outside it, and no top or bottom HUD band
consumes its height. On a fullscreen 1920 × 1080 display, the field therefore
uses all 1080 vertical pixels, roughly 46% taller than the measured 738-pixel
gameplay field in that browser capture. This illustrates the proposed layout;
it does not claim the shipping viewport has already changed.

Scene buttons use separate native gameplay, fly-in and continue captures.
They demonstrate a constant field rectangle and HUD placement. Example
stocks, bars and the animated radar are review data, not a live game session.
Normal, low and empty stocks, fullscreen preview, gallery comparison and PNG
download are available. The review page fits desktop/mobile; narrow-screen
and co-op game installation details follow Mike's choice.

## Generated assets and ownership

Built-in `image_gen` generated five new paired side HUD plates using the
approved `_ART_SOURCES/hud_concepts_1011/armored-command.png` as the material
reference. Every returned source is 1024 × 1536 RGBA. Sources are copied
unchanged into `_ART_SOURCES/side_hud_1012/`; original generated images remain
in the Codex image folder. No recoloring, stretching or alpha removal was used.

- Exact prompt set: `_ART_SOURCES/side_hud_1012/prompts.json`.
- Original output paths: `_ART_SOURCES/side_hud_1012/generation-record.json`.
- Measured wells: `_ART_SOURCES/side_hud_1012/well-measurements.json`.
- SHA-256, source dimensions and well registration: `registration.json` there.
- Owner: `_BUILD_SOURCE/build_side_hud_concepts_1012.py`.
- Review and five 2048 × 1152 populated PNGs: `docs/previews/side_hud_1012/`.

Each source column is displayed at one proportional scale. Text uses the
authored Command Alloy bitmap face; weapon, special, life, missile and lock
graphics reuse the game's native HUD exports. Meter strips also use authored
HUD art. Radar contacts and its sweep are drawn as UI data in the generated
square radar housing.

## Verification and status

`node --check` passes for the review script. The native reference capture
reports no page/console errors. `_BUILD_SOURCE/probe_side_hud_1012.py` reports
**16 passes, 0 failures**, including all five choices, scene switching without
resizing, fullscreen coverage, stock states, motion, PNG download and mobile
overflow. No browser or missing-asset errors. All five populated mockups,
the fly-in reference, low-stock display and mobile review were inspected.
Portable report: `docs/qa/side_hud_1012.json`; scratch captures: `_shots/side_hud_1012/`.

The live HUD, gameplay logic, viewport fitter, game entrypoint and atlas were
not edited in this concept pass. The full gameplay suite was not rerun because
no shipping game code or data changed. Implementation awaits Mike's concept
selection, as requested. No commit or push was made.
