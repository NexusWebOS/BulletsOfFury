# Pilot Cinematic Ship Frames

Production-ready cinematic views for all nine Fury pilots, generated from the canonical runtime ship atlas rather than redesigned from memory.

## Delivery

- 9 pilot ships
- 6 cinematic views per pilot
- 54 fixed frames total
- 512x512 RGBA per fixed frame
- Tight native-resolution RGBA cutout for every view
- 1536x1024 RGBA six-view master for every pilot
- Clean decontaminated alpha with zero RGB beneath fully transparent pixels
- No background, matte, drop shadow, fringe or chroma halo

## View order

1. Strict top-down neutral
2. Front-left three-quarter pseudo-3D
3. Front-right three-quarter pseudo-3D
4. Rear-left three-quarter
5. Rear-right three-quarter
6. Dramatic hard-bank upper-side

## Folder layout

Each pilot folder contains:

- `<pilot>_cinematic_views_master_rgba.png` - all six views on a transparent 1536x1024 canvas
- `frames_512/` - fixed 512x512 compositing frames with consistent slot anchors
- `cutouts_native/` - tightly cropped native-resolution cutouts for free cinematic placement
- `<pilot>_edge_qa_checker.jpg` - transparency review image

`manifest.json` records every file, view description, cutout size, checksum, reference source and alpha-edge metric. The combined review sheet is `previews/cinematic_ships_9pilots_contact.jpg`.

## Tail continuity repair

Eight frames were selectively regenerated after the full-pack audit removed invented rear-end geometry:

- Falva: front-left three-quarter, front-right three-quarter and hard-bank
- Decker: front-left three-quarter, front-right three-quarter and hard-bank
- Lizzie: rear-left and rear-right three-quarter

Falva and Decker now end in canonical engine nozzles with short gaseous exhaust instead of solid second nose cones. Lizzie now has a plain gold tailplane with no rear bulb or light. The corrected-frame review sheet is `previews/cinematic_ships_tail_repairs_contact.jpg`; retained keyed repair sources live in `_BUILD_SOURCE/cinematic_ship_repairs/`.

Rebuild from the retained chroma masters with `_BUILD_SOURCE/build_cinematic_ship_pack.py`. Validate the package with `_BUILD_SOURCE/verify_cinematic_ship_pack.py`.
