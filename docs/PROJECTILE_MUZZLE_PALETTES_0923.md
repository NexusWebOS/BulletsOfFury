# Projectile muzzle palettes — 2026-09-23

Mike approved the rounded green player muzzle as the common style and requested
palette variants for the other players and enemy projectiles.

The existing eight generated frames now supply kinetic, missile, laser, fire,
ice, lightning, toxic, water, dark, chrome, prism, thermo and sonic palettes.
`PROJECTILE_MUZZLE_PALETTES` defines the colors; cached canvas palette swaps keep
the authored luminance, transparent silhouette and white core. No new generation
credits were used. `palette_reels.png` and `palette_preview.png` beside the source
frames are exports of the actual runtime palette cache.

Integration covers the shared player firing flash for all nine pilots, held and
space lasers, forged elements, naval/jet/tank enemy flashes, ship bosses, custom
minibosses and paired Stage 9 guns. Quad-Laser, Razorback and Furnace have separate
rendering paths and now use circular muzzles too. Moving hardpoint callbacks,
projectile sprites, attack timing and damage are preserved. Held beams suppress
the extra player flash to avoid drawing two muzzles on the same nozzle.

Verification uses `_BUILD_SOURCE/probe_muzzle_variants_0923.py` in real Chromium:
five laser tiers, all nine pilots, nine forge elements, eleven enemy families,
both spaceship guns and a moving enemy mount. Palette previews are captured
through the engine's real cached art. Both existing laser/Harrier probes remain
applicable. Evidence is in `_shots/muzzle_variants_0923/`.

The expanded Chromium probe also verifies all four Quad-Laser muzzle locations
and the Razorback/Furnace rendering paths. It passes with no page or console
errors; screenshots and palette previews were inspected. Syntax validation passes.
The full suite completed with 4,898 passing checks and 81 failures (exit 1),
matching the established 81-name baseline. The intermittent Stage 1 sand-tank
spawn check failed this time; there are no new failure names. Final suite log:
`_shots/muzzle_variants_verified_suite_0923.log`.

The existing source assertion counted two legacy muzzle fallback guards. There
are now three because the old player pack also yields to the approved circular
flash; the assertion was updated to require all three guards. Test-file CRLF and
game-file LF endings are preserved.

No commit or push performed.
