# Installed Siege Console — October 12, 2026

Mike selected the vented Siege Console plate with “this looks good. continue.”
The selected side HUD is now loaded by the game entrypoint and reads live
game state. The earlier five-concept review remains available for provenance.

## Live layout

Left: score and shared high score, Roll, Somersault, equipped weapon, speed,
shield and pilot/stage identification. Right: radar, special ability/resource,
lives, missiles and retina lock-on. The full authored 1024 × 1536 RGBA plate
is copied byte-for-byte to `assets/game/shared/ui/siege_console_1012/frame.png`.
The owner is `_BUILD_SOURCE/build_siege_console_1012.py`; registration and
`assets/siege_console_art_1012.js` record columns, measured wells, SHA-256 and
compact module rectangles. All delivered/backing frame dimensions are even.

`assets/siege_console_1012.js` draws the selected plate through native XART
and the HUD contexts, using the game's Command Alloy face and existing icons.
It reads each seat through `withSeat`/`ph8Values`, retaining special timers,
loan resources, weapon variants and active enhanced-special icon routing.
Maverick's bare homing lances display **FIXED / LEVEL 01**; his separate
Laser Beam shows its equipped level. This changes the display only.
Weapon icons reuse their measured native alpha crops with a larger allowed
display size. Long special names use two readable lines. Both co-op score
panels show the same highest live score, while each seat retains its own
stocks, cooldowns, weapon and signature resource.

Radar maps actual visible enemies, bosses and player ships through the
current camera bounds. Cloaked actors remain hidden. Its sweep uses the
gameplay clock and freezes in pause; drawing does not advance combat.

## Consistent display fit

The existing `index.html` fitter calls the new layout owner for intro,
launch, play, pause, continue, game-over, outbound, warp-entry, rival and
flyover states. At wide display sizes it fits one proportional **480 × 512**
field using the full window height, with the two HUD columns outside it.
Top/bottom strips, credit rails and older operations panels consume no space
in this mode. Native fullscreen follows the same layout and field size.
The gameplay backing store remains 960 × 1024; actor scales, camera behavior
and combat coordinates remain owned by the game.

If the side space cannot support readable columns, the selected art supplies
a compact 480 × 176 dock per seat under the field. Its modules are cropped
from the same plate and proportionally contained in the dock. This layout
also stays constant across the corresponding gameplay/intro/continue states.
Co-op stacks both seat readouts without shrinking the wide gameplay field.
Returning to menus releases the new owner; campaign maps and authored
widescreen story/results presentations retain their existing viewport owners.

`assets/siege_console_1012.css` supplies the layout visibility rules. The old
operations-panel ticker respects the new owner. No gameplay canvas is resized
or cleared by a HUD draw. Input still maps against the actual canvas rectangle.

## Verification

- `node --check`: game.js, generated HUD registry and the new renderer pass.
- Full `_BUILD_SOURCE/test_fl.js`: **8,700 passes, 0 failures**, final summary,
  exit 0. The final run follows the completed implementation.
- `_BUILD_SOURCE/probe_siege_console_1012.py`: **51 passes, 0 failures**, exit 0.
  Covers exact art identity, live counters/cooldowns/special resources, radar
  and cloaking, scene geometry, pause, native fullscreen, seven window sizes,
  real mouse mapping, all nine pilots' icons, fixed homing-lance display,
  co-op stocks/shared high score/seat restoration, compact mode and menu return.
- Existing `_BUILD_SOURCE/probe_playthrough_finale_1011.py`: **14 passes,
  0 failures**, exit 0; the boss/portal transition remains intact.
- No page, console or missing-asset errors. Native captures of the installed
  HUD, active special, continue, fixed lances, co-op and compact layouts were
  visually inspected.

Portable verification: `docs/qa/siege_console_1012.json`.
Captures/logs: `_shots/siege_console_1012/`.
The concept builder also corrected its original Roll/Somersault trough
ordering by matching horizontal position rather than the one-pixel difference
between their measured top edges.

No edits were made to `assets/game.js` or `_BUILD_SOURCE/test_fl.js` in this
pass; their preexisting work and LF/CRLF endings are preserved. The atlas and
earlier concept/source files remain available. No commit or push was made.
