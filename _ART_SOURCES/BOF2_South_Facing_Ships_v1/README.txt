BOF2 SOUTH-FACING SHIP REMAKES v1
Author: ColeForge Productions

CONTENTS
- 6 full-resolution cleaned source sprites in Source/
- 6 engine-ready runtime sprites in Frames/
- 1 dark-background fleet contact preview in Previews/
- 1 machine-readable manifest.json

RUNTIME CONTRACT
- Camera: strict top-down orthographic vertical-shooter view
- Facing: South; nose/front at bottom, engines/rear at top
- Cell: 256 x 256 pixels
- Pivot: (128, 128)
- Color: indexed PNG, maximum 64 used colors per sprite
- Transparency: binary alpha only (fully opaque or fully transparent)
- Filtering: nearest-neighbor / point filtering only
- Lighting: upper/front key light with dark selective outlines

SHIP FILES
- BOF2_Ship_Cryo_Spear_South.png
- BOF2_Ship_Blacksteel_Raptor_South.png
- BOF2_Ship_Inferno_Reaver_South.png
- BOF2_Ship_Olive_Siegecarrier_South.png
- BOF2_Ship_Thorn_Cruiser_South.png
- BOF2_Ship_Void_Bat_South.png

IMPORT NOTES
- Use the Frames/ versions directly for runtime use.
- Disable bilinear/trilinear texture filtering and mipmap smoothing for crisp pixels.
- Keep the source aspect ratio and scale by integer multiples when possible.
- The Source/ versions retain the larger cleaned render for future edits.

QA
- All ships face vertically south.
- No frame is clipped.
- All runtime images are exactly 256 x 256.
- Every runtime PNG has genuine transparency with exactly two alpha levels.
- Baked checkerboards, chroma-key magenta, pink fringe, and colored background halos were removed.
- Runtime sprites use 60 to 64 colors.

GENERATION SUMMARY
Each supplied ship was used as its own identity reference. The approved Cryo Spear remake established the shared south-facing camera, scale, padding, and late-16-bit/arcade pixel technique. The other five ships were remade independently against that production standard so their silhouettes and palettes did not blend together.

