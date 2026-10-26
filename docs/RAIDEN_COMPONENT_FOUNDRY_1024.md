Current matched-set correction: see docs/RAIDEN_MATCHED_SETS_1025.md.
The 24 hulls now have 144 individual matched hardware modules plus 33 running-gear
modules. Earlier counts and generic shared-family fitouts below are historical.

# Correct modular asset contract — October 24

Mike rejected the 170 source-cut layers: those were breakup/destruction pieces,
not his intended modular art. That delivery does not satisfy his request and
must not be described or reintroduced as the finished modular roster.

Modular means complete independently usable authored objects. The chassis has
continuous armor/deck/skin beneath attachments; a turret has its complete rotating
base and barrels; engines, wings and racks have finished mounting interfaces.
Hardware overlaps a complete base and can be swapped, aimed or omitted while
the underlying hull remains intact. Do not partition a finished unit into masks
or claim pixel-perfect source reconstruction proves modularity.

The replacement is art-packs/raiden-components-1024/, with its own ZIP. The original
eight sheets plus new hull/track/wheel sheets supply 24 complete bare bases and 59 complete
reusable modules, with 16 enemy / four miniboss / four large boss example fitouts.
All generated sources/prompts retained in _ART_SOURCES/raiden_components_1024/.

Air kits supply complete wing pairs, engine pairs and two weapon pods; ground
kits have complete gearless mobile hulls / stationary foundations and independent turret/rack/radar
and generator choices; naval kits have complete decks and gun/bridge/drive/radar
modules. The loadout builder changes components at compatible hardpoints and
aims complete cannon/turret objects around recorded pivots. Its Bare chassis view
exposes the actual uninterrupted base layer.

Every component exports on a fixed 512-square master / 256-square native canvas.
Example assembly frames are 512/768/1024 per tier. Each kit keeps one source
normalization scale; instance scales are scalar and recorded. Source components
are extracted as whole pre-separated objects, never partitioned assembled units.
Hardpoint anchors are measured on solid base pixels with interior clearance.

Owner: _BUILD_SOURCE/build_raiden_components_1024.py. Native Chromium QA owner:
_BUILD_SOURCE/probe_raiden_components_1024.py. 54 checks passed / 0 failed after the running-gear correction:
all 83 complete components decode, all 24 bases have uninterrupted central armor,
all mounts have painted backing, no fitted assembly clips, actual loadout swaps
and independent turret aiming change hardware while preserving the bare-base
raster, empty mounts and reset work, desktop/mobile layouts pass. Actual bare,
fitted and swapped pixels inspected. No browser page/console errors. Evidence:
_shots/raiden_components_1024/. Shipping game files retain starting hashes.

This delivery is a static reusable component art kit and preview, not a claim of
live combat, animation or audio integration. Earlier projectile/laser artwork is
retained in the original armory. No commit, push, user-data deletion or worktree.

## Running gear correction

Mike explicitly requires the tank wheels to be modular too. Seven mobile ground
bases now use newly generated fully surfaced hulls WITHOUT baked tracks or
wheels: Scout Tank, Twin-Cannon Tank, Rocket Carrier, Wheeled Flak, Olive Assault
Tank, Iron Bastion Landship and Quad Laser Citadel. Never restore the old
tracked/wheeled plates as their bare chassis.

The ninth kit contains 11 whole generated running-gear objects: two track
cassettes, rubber and armored tires, road wheel, drive sprocket, idler, twin
wheel bogie, suspension arm, steel roller and wide roller. Six tracked machines
have independently registered left/right belts, ten wheels and six suspension
arms. Flak has six separate wheels and six suspension arms. Default draw order:
suspension, wheels, track cassettes, complete hull, weapons.

Track belts can be hidden while the wheels remain, and all running gear can be
hidden while weapons remain. Removing one wheel changes only its module pixels;
replacing it restores them. All seven wheel hit flashes visibly light damaged
pixels and expire. Browser checks preserve the bare hull through these edits.
Prompts and selected source filenames: running-gear-prompts.json. This remains
a static art kit and interactive assembly preview, not a gameplay refit.
