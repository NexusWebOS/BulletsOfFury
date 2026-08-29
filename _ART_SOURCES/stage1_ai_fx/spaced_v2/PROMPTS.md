# Stage 1 Jungle VFX — spaced v2 sources

These four source strips were generated with the built-in GPT image generator, one
effect family per image. Each prompt required exactly six frames in one horizontal
row, extremely wide empty gutters, generous outer padding, complete silhouettes,
and no fragments between frames. The earlier four-row contact sheet is retained as
a style/source reference but is no longer sliced into the production atlas.

The production builder additionally rejects any source frame that enters a 20px
edge guard and rejects any packed frame that enters a 20px atlas-cell edge guard.
This makes clipped crescents, rings, impacts, and neighboring-frame leakage a hard
build failure instead of a visual regression.

Families:

- `green_laser_spaced.png`: six-frame emerald vertical jungle laser pulse.
- `wind_blade_spaced.png`: six-frame rotating emerald crescent wind blade.
- `wind_vortex_spaced.png`: six-frame expanding/contracting emerald vortex.
- `green_impact_spaced.png`: six-frame expanding/contracting emerald impact.
