# Overdrive Retina, shoulder aim and Warrior fit — October 12, 2026

Mike reported that Retina and shoulder aiming were still unusable, requested
BOF's Retina system and A-button menu selection, and asked for a slightly smaller
Warrior with centered text inside its frames.

## Controls and lock behavior

- **R shoulder / Z / I:** tap to acquire the nearest visible hostile; tap again
  to cycle. The original BOF seeker travels and shrinks over 0.45 seconds.
- The lock survives release for **five seconds** and flashes before expiry.
  Holding Retina maintains that window. Solid cover and target destruction
  invalidate a lock. The old 320-pixel range and forward-cone restriction are
  removed; candidates must remain inside the visible playfield.
- **C charge/release / K / standard B:** fire the cannon at an acquired target.
  **Hold Retina + A:** fire guided missiles alongside the primary gun. Missiles
  spend the actual rack and retain the exact enemy or modular boss part.
- **L shoulder + D-pad:** capture the direction already being driven, keep
  cruising in it, and aim the turret with the D-pad. A alone fires along that
  turret aim. Explicit directional face-button combinations retain their firing
  directions. A new mouse movement can take aim over, and a new D-pad direction
  can take it back. Standard-pad right-stick aim remains independent.
- **A or Start** confirms title, difficulty, pilot, briefing, pause, password,
  controller setup and the boss dossier's Continue action. As in BOF, menus
  accept face/shoulder reports that are not mapped to Back, Mode or movement;
  the printed A can arrive as browser button 5. B remains Back.

Saved user mappings remain intact. Rebinding and volume controls still use the
original Options renderer; its owner builder regenerated the input adapter.

## Authored art and layout

Retina uses the existing `retm_0..3`, `retmb_0..3` and nine `nbret_*` cells through
BOF's manifest. Pilot colors and the original multiply/mask/specular tint path
are retained; new pilots use the same masters with their expansion colors.
Seeker/ordinary-lock frames animate; boss retinas retain their original art.
The stage-three nuclear targeting graphic is no longer used for Retina.

The live Warrior is uniformly scaled to **85%**. Drawing, mounts, muzzle
positions, hit radii, blast/ram collisions, fragments and wrecks share that
factor. HP, armor and attack timing are retained. The arena stays at **640x480**
with normal **1:1** camera zoom.

Dossier text is measured against its assigned rectangles and centered. Target
rows combine part name and HP, attack lines fit the right pane, and A/Start
Continue prompts sit inside the card. Pilot titles, descriptions, stats,
controller instructions, setup prompts, achievement text and briefing headings
also fit their allotted regions. Menu prompt groups use actual glyph widths.

## Verification

Native Chromium using `_BUILD_SOURCE/shoot.py`, isolated saves, actual keyboard
and pointer events and synthetic Gamepad reports:

| Probe | Passing checks |
| --- | ---: |
| Retina/shoulders/menu A/text/smaller boss | 40 |
| Existing mouse and directional input | 28 |
| Warrior introduction | 42 |
| Original frontend and Options | 55 |
| Warrior combat, collisions and breakoffs | 22 |
| Total | **187** |

Zero page, console, asset or audio errors. Inspected actual seeker, ordinary
lock, boss lock, shoulder aim, boss-card, smaller-arena, Hotwire-pilot and Help
captures. Physical hardware was not connected; synthetic reports exercise the
same Gamepad polling and saved-binding path.

Syntax checks pass. Required base suite reaches its final summary with **8,700
passing assertions, zero errors and exit 0**. The older September baseline is
historical. Results: `docs/qa/overdrive_retina_1012.json`; ignored evidence:
`_shots/overdrive_retina_1012/`.

Module/launcher stamp: `overdrive1012-retina-r1`. Local only; no commit or push.
