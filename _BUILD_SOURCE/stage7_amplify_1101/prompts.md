# Stage7 modular source prompts — November1

Tool: built-in image_gen; true transparent background. Original PNGs retained
beside this file; source SHA256 and generated-bank hashes live in generation.json
and the runtime manifest. No CLI/API fallback was used.

All requests included: even frame dimensions, one proportional scale, fixed
physical pivot, transparent safety margins, crisp arcade pixel clusters, dark
outlines, metallic highlights, no text, labels, scene, UI or surrounding bubble.
Actual generated dimensions were normalized by the owning builder without
per-frame fitting. Runtime headings are baked source-preserving direction cells.

- **brood_source.png:** One512x512 top-down south-facing terrifying mechanical
  Brood Sentinel. Anthracite/dirty bronze chitin armor, toxic-green vents, broad
  abdomen, serrated metal maw and two clearly jointed inward-curving scythe arms.
  Clear alpha gaps between body and claws; no wings or separate glow circle.
- **face_source.png:** Reference the actual generated Brood source. Eight256px
  cells in4x2; same skull pivot and scale. Clenched jaw, slightly open, half open,
  fully open, glowing throat spit, open recoil, closing, closed. Face only.
- **fly_source.png:** Eight128px cells in4x2. One south-facing black/bronze toxic
  robot fly, green eye/reactor, silver razor wings performing a rapid wingbeat.
  Identical body/eye pivot; no asterisks, halo or loose sparks.
- **relay_source.png:** One512px top-down south-facing heavy sewer aircraft.
  Steel-gray/black industrial hull, green reactor strips, twin rear engines,
  two huge six-barrel rotary miniguns on clearly isolated circular trunnions.
- **relay_roll_source.png:** Use relay identity. Eight256px cells in4x2; complete
  longitudinal barrel roll, nose always south. Dorsal,45 bank, edge-on, underside,
  opposite bank, opposite edge,315 bank, upright. Shared scale/pivot, full volume.
- **slime_source.png:** One512px medium/large swept bat-wing toxic jet, weathered
  gray/green camouflage, green liquid reactor, twin independent chainguns on
  clear swivels and two north exhausts. No missiles, slime clouds or balls.
- **slime_roll_source.png:** Reference slime source. Eight256px longitudinal
  roll cells, same jet/reactor/palette/guns and shared center pivot. Nose south,
  actual bank/edge-on/underside/dorsal poses, no heading spin substitute.
- **missilejet_source.png:** One512px black/green wide toxic missile jet, chunky
  reverse-swept wings, green recessed seams, two independent round-swivel pods,
  each with two physical black/green missiles and silver south-facing points.
  Rear twin engines; no chainguns, ball or bubble.
- **barge_source.png:** One512px heavy rectangular industrial toxic hoverbarge.
  Blunt south bow, black iron/bronze plates, central open sludge reservoir,
  two rear propulsion fans, four distinct dual-barrel deck guns on swivels.
  Green emissive seams, no insect/jet silhouette, no surrounding shield circle.
- **crescent_source.png:** One512px distinct mechanical south-facing aircraft.
  Forward-curved crescent wing, bronze/black/green armor, dagger nose, three
  rear engines, two slim energy-cannon modules near outer wings. No creature,
  Brood anatomy, claws or shield bubble.
- **crawler_source.png:** One512px south-facing pipe-side mechanical crawler.
  Three interlocking bronze/black cylindrical abdomen sections, jointed piston
  gripping legs, clear alpha gaps, green head lens and two slim south guns.
  No surrounding scenery, valve, jet or round projectiles.

Preserved native sources: toxic mini-tank, Stage7 ground base and MG/laser/sonic
heads. Projectile, muzzle and thruster variants derive from the approved Stage2
ordnance; sonic waves derive from the actual native sonic sprite. Toxic palette
retains source alpha and white-core/luminance hierarchy.1015 spill derives only
from the actual source pixels and articulated module outlines.
