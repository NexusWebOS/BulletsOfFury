# CF_ToxicSewerPortal-Lvl7

Complete Bullets of Fury Level 7 toxic-sewer scroll and animated sewer-side gateway.

## Indoor layer contract

- Exterior space beyond the physical sewer walls is opaque pure `#000000`.
- Inner toxic-sludge channels and the portal aperture remain exact `#FF00FF` in `Edited/Master Edit` files.
- Runtime alpha files make only those inner regions fully transparent for animated sludge and portal energy.
- Connector cutouts stay transparent so all five boards retain their jagged 96px interlocking overlaps.
- Alpha is binary; there is no gray fill, partial translucency, or hidden RGB.

## Runtime order

1. Animated sludge behind the relevant transparent inner channels.
2. Sewer background with solid black indoor exterior.
3. `sewerportal` energy behind the final aperture.
4. Physical gate rim, player, and foreground effects.

The full scroll is `680x4716`. The portal animation is eight `512x512` frames at 12 FPS.
