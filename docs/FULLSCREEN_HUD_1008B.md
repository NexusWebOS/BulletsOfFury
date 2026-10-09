# Fullscreen and HUD readability — October 8, 2026

Score follow-up: numbers enlarged 7px → 12px with comma grouping; solo/co-op
now reserve 104/208 logical rows (backing 960×208 / 960×416). Sidebar and
leaderboard scores are larger too. Final captures: `_shots/fullscreen_hud_1008/score_final`.

Mike requested a full-height browser/fullscreen presentation and a clearer live
player HUD. Installed in the GitHub Coding checkout; local changes, not published.

## Result

- The ordinary browser bay and fullscreen bay use all available height whenever
  width permits, while keeping the 480:512 playfield aspect. Width-constrained
  portrait windows fit the whole playfield to the available width without cropping.
- The HUD, divider and playfield share one pixel-height budget. Independent
  rounding previously exceeded a 1366×768 viewport by one pixel. The divider now
  takes two logical pixels instead of six. Hidden fullscreen menu HUD rows consume
  no height; menus keep their original aspect. Campaign/cinematic viewports retain
  their existing owners. Hidden mobile credit rails reserve no horizontal space.
- F enters/exits native fullscreen. Browsers rejecting/unavailable fullscreen
  use the browser-fill fallback, which F can also exit.
- HUD backing and cached authored housing now render at 2× density: 960×208 for
  solo, 960×416 for co-op. Logical rows are 480×104, so encounters/resource drains
  do not resize the shell or alter movement/collision/gameplay coordinates.
- Bitmap letters round on the denser HUD grid; equipment icons and metal trim
  retain more detail. Larger special names and an opaque status strip improve
  readability. Corrected label-erasure regions remove the baked concept Roll and
  Somersault fragments that were visible behind their live replacements.
- Authored continuous glowing green/red tracks, ship/missile icons, stage themes,
  boss/miniboss/shield bars and all live values remain installed. Derived caches
  still retire with their stage. No generated artwork, atlas or expansion edit.
- Side portraits use their pilot-owned paths. Changed runtime script URLs carry
  a version stamp to prevent a cached old script from accompanying the new page.
- The main-loop HUD clear now covers its actual backing dimensions, including
  both co-op rows; returning to a menu cannot leave stale lower HUD pixels.

## Verification

- Required base suite `_BUILD_SOURCE/test_fl.js`: exit 0 and final
  `FALVA/LIZZIE BUILD OK, 0 ERRORS` summary. Gameplay controllers are unchanged.
- Syntax: `assets/game.js`, `assets/player_hud_1008.js`, and
  `assets/widescreen_hud_0918.js` pass `node --check`.
- Existing native HUD probe: 205/205, zero page/console errors. Its pixel reads
  now account for the denser backing; logical size and gameplay assertions remain.
  Covers all ten themes, all pilots/native weapons, co-op, empty/draining fills,
  locks, equipment, cache retirement and finale health pools.
- New fullscreen probe: 51/51 across Chromium, Firefox and WebKit, zero browser
  or missing-asset errors. Includes actual Chromium F/native fullscreen, rejected
  API fallback enter/exit, 1920×1080, 1366×768, 2560×1440, 3440×1440 and 390×844,
  aspect/edge/crop checks, narrow browser width, menu aspect and full HUD clearing.
- Inspected real renderer captures for Rebel fullscreen, boss/shield assembly,
  stage themes, co-op and menus. Captures are controlled fixtures, not balance tests.

Portable fullscreen checks: `docs/qa/fullscreen_hud_1008b.json`.
Screenshots: `_shots/fullscreen_hud_1008/{before,after,final,acceptance}` and
`_shots/player_hud_1008`. Final Rebel/HUD captures are in the `final` folder.

Reproduce from repository root:

```
node --check assets/game.js
node --check assets/player_hud_1008.js
node --check assets/widescreen_hud_0918.js
node _BUILD_SOURCE/test_fl.js
python _BUILD_SOURCE/probe_player_hud_1008.py
python _BUILD_SOURCE/probe_fullscreen_hud_1008b.py
```

## Expanded status strip follow-up

The non-playable footer is now 34 logical pixels tall (previously 20). Score,
high score and special values share a padded 12px number/status line with 7px
labels. Fullscreen still fills the available height while preserving playfield
aspect; the taller reserved HUD slightly reduces its physical display size.
A floating-point epsilon prevents a 1px budget shortfall at 1366×768.

Native HUD checks: 205/205. Three-browser fullscreen checks: 51/51.
Focused footer checks: 12/12, with real glyph pixel bounds for nuke/A-bomb
counts, 100% ball/charge states, large scores and co-op; zero errors.
Screenshots inspected in `_shots/fullscreen_hud_1008/footer_status`.
Reproduce with `python _BUILD_SOURCE/probe_hud_footer_1008d.py`.

Published follow-up: the authored crosshair now remains silver in NO LOCK and
turns red with LOCK-ON; each label has separate room beside the icon. Both
real renderer states were captured and inspected with zero browser errors.
