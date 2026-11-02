# Stage2 volcanic sprite prompt set

Generation used the built-in `image_gen` tool with transparent background. The
original generated files are retained next to this document; the bank manifest
records source hashes and measured source rectangles. No SpriteCook credits or
PixelLab generation credits were spent.

Shared aircraft sheet prompt: detailed NeoGeo arcade vertical-shooter pixel art,
metallic highlights, black outlines, upper-left light. Fixed 256×256 cells,
4 columns ×6 rows, shared fuselage center, one proportional scale, transparent
margins, no scenery, labels, grid or detached projectile effects. Row1 south idle,
recoil, left/right drift; rows2–3 eight top-view headings; row4 four barrel-roll
poses; row5 four forward-somersault poses; row6 four sequential charge/weapon
poses. Complete strips were generated together. The exporter corrects generated
grid drift using connected authored hulls, fixed padding and common scale.

| Source | Subject and required identity |
| --- | --- |
| interceptor_source.png | Large fire-red/black jet; exactly four machine-gun mounts, two wing and two forward; molten orange cores and white metal highlights. |
| skimmer_source.png | Larger broad twin-boom obsidian/bronze fighter; two long gun rails, two turbofans and swept wings. |
| wasp_source.png | Narrow amber/black/copper mechanical Cinderwasp; four short swept wings and twin aft fire engines. |
| thunder_source.png | Large black/fire-red/cobalt Thunderlance; blue electric cores and wing edges, paired gun rails and visible missile racks. |
| crucible_source.png | Black medium gunship; two large fire cores and two matching forward orb apertures; no baked shield. |
| minelayer_source.png | Distinct rectangular mine-magazine craft, black/rust-orange armor, ventral deployment hatch, two large escape boosters. |
| carrier_source.png | Broad volcanic Harrier hangar, four lift engines, central bay and sliding two-piece door. Final four frames closed→open; no child jets baked into the hull. |
| elite_source.png | New black/red carrier-launched jet, scimitar wings, two forward fire cannons and ventral furnace emitter. |

Separate whole-object prompts:

- `snake_source.png`: connected long lava mechanical snake, obsidian segments,
  orange molten gaps, hinged jaw and silver spikes; sixteen poses in4×4 fixed
  cells: eastward eruption/crossing, westward crossing, south bite windup, open
  bite, miss recovery and rest. No disjoint body pieces or terrain.
- `maw_source.png`: mechanically braced basalt mini volcano, actual top crater,
  sixteen idle/heat/erupt/cool poses, stable base and no forward cannon.
- `pod_source.png`: distinct six-petal black/copper floating mechanical pod,
  sixteen closed/open/erupt/close poses with a molten central core.
- `disc_source.png`: black radial saw-disc, glowing orange core and red laser
  apertures;16 spin poses. The generator supplied seven spikes. The exporter
  corrects this using its actual authored core and one complete source spike,
  assembled into exactly nine fixed weapon sockets and32 registered spin poses.
- `ordnance_source.png`:4×8 effect sheet with four loop frames per row: solid fire
  slug, black/blue/orange thunderfire slug, physical thunderfire missile, spinning
  magma orb, proximity air mine, seamless red/white laser segment, forward fire
  muzzle and flame thruster. No floating warnings, UI or background. Directional
  exports and a nozzle-free flamethrower derive from these actual source pixels.

Ash uses the complete approved BF22 Magma Dart idle/attack/drift/roll/somersault
banks. Basalt uses the complete BF22 Forge banks with the requested gray/black
steel palette, preserving hot fire cores, neutral highlights and dark seams.
