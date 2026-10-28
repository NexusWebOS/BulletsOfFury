# Biome fleet — October22,2026

Stage2 now uses Cinder Dart small magma craft and Obsidian Forge heavy craft.
Stage6 uses Zephyr Needle, Gale Sabre and Stratus Bastion in teal/white/gray.
Stage9 uses Abyss Skate, Tidal Manta, Pelagic Leviathan and Undertow Core water-tech
spacecraft/drone designs. Mike explicitly chose to retain its void/space arena.

Nine PixelLab masters,45 complete idle/attack/drift/roll/somersault banks:365
fixed128x128 cells. Twelve projectile/muzzle banks add60 fixed64x64 cells.
Shipping art is57 lossless WebP sheets,539240 bytes. Source candidates, normalized
masters, prompts/job receipts, sockets, exact module-union and frame/export audits
are archived in `_ART_SOURCES/biome_fleet_1022`. The owning builder is
`_BUILD_SOURCE/build_biome_fleet_1022.py`; rerun with `--install` to rebuild.

The runtime `assets/biome_fleet_1022.js` uses the native AF21 bank renderer with
temporary stage-scoped aliases. It restores every alias after drawing. A complete
new hull can render while a retired texture is unavailable. The Stage2 and Stage6
units both named lance resolve independently. Live Stage6 bomber-flight aliases
and the retired golem's firejet1002 replacement are included.

Native health, controller cadence, entry protection, collision boxes, shields,
warning directors, sound assignments and death/explosion owners are retained.
Generated stray firing effects are clipped out of the hull banks. Weapon-owned
effects follow measured cannon sockets, deduplicate volley partners and cancel
with their launcher; intentional noMuzzle options remain effective. Projectile
art is centered and fitted to its existing collision dimensions. Existing boss,
rebel, environmental comet/rock, ground-fixture and other-stage art is retained.

Validation:73/73 real Chromium checks, no renderer errors. These cover nine native
hulls and hit flashes, all45 bank selectors, missile/launcher ownership, single
muzzles and follow callbacks, shared-name scope, all three native encounters,
flash expiry and native destruction. The full core suite reached its final
summary:8943 passes,0 errors. All three runtime JS files pass syntax checks.
Native results/captures: `_shots/biome_fleet_1022/report.json`. Review:
`docs/previews/biome_fleet_1022/index.html`.

The PixelLab pass completed. Its balance reported -$0.01 with two daily bonus
generations remaining at the final check; no further generation was queued.
This is a local change. No commit or push was requested for this pass.
