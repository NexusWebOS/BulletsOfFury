# ColeForge style foundation — 2026-10-23

## Confirmed user direction

ColeForge should have a recognizable design identity across UI, menus and games, support 2D
and 3D sidescrollers/platformers/shmups, use authored game graphics rather than HTML-modified
effects, and keep future ports feasible within actual platform limits and applicable rights.
The installed authored-graphics contract is the current detailed rule. BOF I/II are references,
not a reason to repeat every historical implementation choice.

## Inspected reference material

Local asset library: `C:/Users/Mike/Desktop/ColeForge-Packs/`.
Inspected preview images: `HUD_Preview.png`, `Fonts1_Preview.png`,
`BOF2Projectiles_Preview.png`. These are production/showcase sheets, not approved screen layouts.

Observed HUD traits: discrete framed icons and compact segmented/radial gauges; dark panel
surfaces with blue/silver edge accents; bright state/resource colors; pixel glyphs and explicit
state frames. The font sheet includes metal, military, electric, elemental and other families:
choose a coherent project family rather than mixing the entire catalogue. Projectile bodies
have strong bright cores and distinct color/silhouette families. Some sheets include soft glow
layers labelled additive: that historical packaging does not authorize additive runtime blending.

Useful local source packs: `HUD.zip`, `Fonts1.zip`, `Fonts2.zip`, `ImpactFX.zip`, `MuzzleFX.zip`,
`WeaponFX.zip`, `BOF2Projectiles.zip`, `SmokeDust.zip`, `MEGA_Interface.zip` and themed effects.
Inspect per-pack metadata/license files and actual frames before reuse. Several inspected packs
include AI disclosure and game-use terms; do not generalize those terms to unrelated assets.

Inspected archive: `BulletsOfFury_0810a.zip`, including `BulletsOfFury/docs/ART_STANDARDS.md`,
enemy roster, boss roster and animation notes. Useful evidence: declared enemy classes/cells,
damage-state families, component-based bosses, distinct component vocabulary per boss type,
and muzzle origins tied to visible weapons. Historical docs also recommend runtime rotation
and per-enemy display scaling; those conflict with the current authored-frame contract and
must not be adopted as current studio policy.

A newer BOF OnlineBeta Windows/source package is present under
`C:/Users/Mike/Documents/Codex/2026-10-21/fo/outputs/` but was not visually playtested for this
skill design. No complete BOF II game build or approved final UI reference was inspected here.

## Provisional direction, not an invented approval

Use crisp authored silhouettes, a clear gameplay value hierarchy, deliberate material/pixel
detail, readable bright cues and coherent modular UI families as a starting point. Preserve
each game's theme. Exact signature palette, logo treatment, universal font, component sizes,
spacing scale and final menu composition are not established by these previews alone.
For a design task extract them from the current approved game/reference, build a concrete
native-scale representative screen, and record what Mike actually approves.


## Adopted retro-reference extension — November 6, 2026

Mike explicitly extended the selected art styles to all his 16-bit and retro games. Use [the standing retro art direction](retro-art-direction.md) for the adopted visual defaults and genre/camera routing. This approves the reference influence and broad visual qualities; it does not establish exact universal colors, fonts, dimensions, gameplay rules or a sound signature. Earlier provisional palette/layout caveats remain valid.
