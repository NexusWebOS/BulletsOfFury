# Reference art pack — October 24

## Superseded: modular interpretation rejected

Mike rejected the source-cut 170 layers as destruction/breakup pieces. The
replacement complete-base + complete-module art kit is documented in
RAIDEN_COMPONENT_FOUNDRY_1024.md and delivered in art-packs/raiden-components-1024/.
The following records are historical and do not establish his approval.

## Rejected breakup-layer prototype

Mike explicitly required all enemies to be modular and requested minibosses and
large boss types based on the supplied Raiden roster. The current pack contains
16 ordinary enemies, four minibosses and four large bosses, all modular.
170 independent registered parts, each in master/native plus white-hit variants.
The 36 existing weapon/effect designs remain in the collection.

New minibosses: Olive Assault Tank, Quad Battery Fortress, Orange Heavy Bomber,
Missile Corvette. Large bosses: Iron Bastion Landship, Dreadnought Battleship,
Stormwing Sky Carrier, Quad Laser Citadel. Two new image_gen source sheets and
exact prompts retained beside the initial three. No live campaign boss was split.

Measured source-preserving polygon masks, attachment cleanup and per-module
pivots own separate visible hardware. No duplicate whole plate backs the parts.
Both master and native part unions reconstruct the original displayed source
exactly. These are visible-surface modules; hidden/occluded faces are not painted
in. Fixed even 384/512/768 master canvases per tier, common proportional scale
per family; every native canvas is half its master.

The gallery now exposes assembled/exploded inspection, per-part selection,
visibility, hit flash/expiry, pivot markers, individual PNG downloads and module
sheets. Owning build: build_raiden_pack_1024.py + raiden_modular_1024.py. Current
QA owner: probe_raiden_modular_1024.py, evidence _shots/raiden_modular_1024/.

Final native Chromium verification: 25 checks passed / 0 failed; all 858 PNGs
decoded/drawn, every module's normal/white alpha matches, all 48 master/native
assemblies reconstruct exactly without overlapping module pixels, all 58 sheets
decode, selected gun flashes white and returns to its exact original raster,
hide/restore/explode/reset and wide/mobile layouts pass. All 24 exploded
assemblies visually inspected after attachment cleanup. No browser page,
console or request errors. Final ZIP: 868 matching files / 37,037,912 bytes.
Game.js, test_fl.js, shipping index and ART_TAXONOMY retain this turn's starting
hashes. Gameplay suite not run for this standalone art-only change.

## Initial pack — historical

Mike requested projectiles, lasers, shmup weaponry, and an enemy roster based
specifically on his three attached Raiden-style reference sheets. Delivered a
standalone static art collection under `art-packs/raiden-reference-1024/` and a
complete `art-packs/raiden-reference-1024.zip` (13,716,025 bytes).

24 projectiles, 12 beam/special columns, 16 distinct enemies. Enemies include
eight aircraft/drone designs, four armored ground units, two emplacements, one
patrol boat and one whole siege aircraft. Names and weapon pairings are working
design suggestions. The terrain reference supplied palette context.

Built-in image_gen generated three RGBA sources using all three references.
Original sources, reference copies and exact prompts are retained under
`_ART_SOURCES/raiden_reference_1024/`. No SpriteCook or PixelLab generation was
used. `_BUILD_SOURCE/build_raiden_pack_1024.py` owns source measurement, export,
sheet registration, manifest, roster CSV and ZIP together.

Projectiles use 288-square master cells / 144-square native cells; beams use
256x512 / 128x256; enemies use 384-square / 192-square. Shared cell-center pivots,
source scale 1, native scale 0.5, nearest sampling, original alpha retained.
The generated projectile source did not honor its requested grid: the first
browser review caught neighboring fragments at nominal cell edges. Measured
silhouette separation and common padded cells corrected those exports. The
original source remains unchanged.

Real Chromium verification using shoot.py's local server: 15 checks passed,
0 failed. All 104 individual PNGs decoded and drew to actual canvas; even
dimensions, transparent margins, and no alpha>=64 edge pixels. All six sheets
decode at their registered dimensions; exporter checks every sheet cell against
its loose PNG. Every sprite was inspected in gallery screenshots. Detail
downloads, five backgrounds and mobile overflow passed, with no page, console
or request errors. ZIP has 118 files matching the local pack byte-for-byte.
Evidence: `_shots/raiden_reference_1024/`.

This is an art pack, with one frame per sprite. No live game integration or
animation/combat/audio behavior is claimed. `assets/game.js`, test_fl.js,
index.html and ART_TAXONOMY.json retain their starting hashes. Required gameplay
suite was not run because gameplay was unchanged. Nothing committed or pushed.
