# Live top HUD and enemy bars — October 8, 2026

Mike requested wiring the generated player HUD, boss bars and miniboss bars into
the game. All nine stage themes and the Stage X theme now use the compact authored
five-panel top assembly, with live game values replacing the concept examples.

Readability/fullscreen follow-up: [October 8 browser/HUD pass](FULLSCREEN_HUD_1008B.md).
Score follow-up: solo/co-op reserve 104/208 logical rows with a 2× dense backing canvas.
Score/high score use separate 12px lines, comma grouping and no leading-zero padding.
The non-playable footer is 34px tall, with 7px labels and equally legible 12px
special status values; all three lanes have vertical padding.

## Installed behavior

- Roll and somersault tracks show actual cooldown availability and refill as the
  maneuvers recover. Lizzie's docked Heavy MG still disables roll.
- Weapon slots use the existing native weapon resolver, including forged variants,
  space weapons and Cole's actual animated yellow/black/Fusion reels. Tier changes
  update the equipped display.
- The center panel shows the pilot's special name and actual remaining resource.
  Rollerball/ram charge and nuclear stock remain available in the short status row.
  Timed borrowed weapons retain icons and independent resource strips. Lizzie's
  mount readout cannot leak to another pilot.
- Radar uses real world targets, camera bounds and player positions. Cloaked/dead
  Rebels are suppressed. The incoming-lock capsule reads the existing lock states
  and uses their warning cadence; lock timing, targeting and audio are unchanged.
  The authored crosshair stays visible in silver for NO LOCK and turns red on lock.
- Lives, missiles, five speed/shield equipment pips, score and high score remain
  live. Existing encounter clocks and widescreen side panels are retained.
- Solo reserves 104 logical pixels before assets decode; co-op reserves two complete
  104-pixel rows, reading each seat independently and restoring the main seat.
  Showing a boss or draining a meter never resizes the shell.
- Previous bottom equipment/radar/maneuver/special panels are replaced by the top
  assembly. Gameplay effects, Cole's world-space overcharge gauge and alerts,
  dialogue, world collision bounds and combat controllers remain intact.
- Existing authored enemy frames remain installed. Complete miniboss nameplates
  now sit immediately below the player assembly, clear of the obsolete tab offset.
  Optional cyan enemy shields remain distinct from player equipment pips.
- Rebel health bars retain five individual pools and cloak/death visibility.
  Finale bars retain each actual pool without healing during drawing; the eight
  successive coronation fills and current form colors remain visible in the new
  housing, using the existing authored palette fill.

## Art and memory

The ten compact 269-pixel-high source crops total 6,528,923 bytes. Their original
pixels and alpha are unchanged. Source images, crop rectangles and SHA-256 hashes
are recorded in `_ART_SOURCES/player_hud_1008/manifest.json`; the owning reproducible
builder is `_BUILD_SOURCE/build_player_hud_1008.py`.

`assets/player_hud_art_1008.js` registers the crops. The runtime caches each selected
assembly at 960×140 backing (480×70 logical) and composites native bitmap letters, existing icons and clipped
authored strip samples. It does not load all ten concept sheets. Stage ownership
retires outgoing source textures and derived canvases; Stage X's row is explicitly
owned by Stage 6. Repeated drawing reuses the static cache and does not advance
combat clocks or change HP/resource values.

No shared atlas or `assets/game.js` edit. The base game SHA-256 remains
`0413d3cd1e0f92703986a67d7966e740dd44b3fd421586292e2c824e4bfc91ca`.
`index.html` retains its existing CRLF line endings and reserves the HUD geometry
before asynchronous loading. The existing CRLF test harness is unchanged.

## Verification

The required full game suite completed with **7,952 passing assertions, zero
errors**, exit 0 and the final success banner. JavaScript syntax checks passed.
The suite remains a base-game regression check; native Chromium covers the newly
installed layers and actual rendered pixels.

The dedicated native player probe passes **205 checks** with zero page/console errors.
[Portable results](qa/player_hud_1008.json) preserve the final assertions.

Native evidence is in `_shots/player_hud_1008/validation.json`, its captures and
review. The dedicated probe covers all stage themes, HP/resource fill pixels,
texture retirement, every pilot, equipment changes, incoming locks, borrowed
weapons, co-op, fullscreen/narrow geometry, stable rendering and all finale pools
and colored coronation refills. The existing enemy HUD probe additionally passes
**245 checks**, including all four health/shield housings at five fractions and
Rebel ownership/visibility across all four difficulties and both routes.

Reproduce:

```powershell
node --check assets/game.js
node --check assets/player_hud_1008.js
node --check assets/player_hud_art_1008.js
node _BUILD_SOURCE/test_fl.js
python _BUILD_SOURCE/probe_player_hud_1008.py
python _BUILD_SOURCE/probe_enemy_hud_1007c.py
```

Captures use controlled rendering/encounter fixtures, selected HP/resources and
protected pilots. They verify HUD ownership and rendering, not unassisted clears
or a new balance sign-off. This verification preceded publication; Mike authorized the GitHub update on October 8.
