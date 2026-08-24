# FURY cinematic character poses

This pack contains six full-body cinematic poses for each of the nine supplied heroes: **54 native-resolution RGBA PNGs** total.

## Pose order

1. Front neutral
2. Front-left three-quarter action/character pose
3. Front-right three-quarter action/character pose
4. True back neutral
5. Back-left three-quarter over-shoulder pose
6. Back-right three-quarter action/character pose

Each character folder contains:

- `poses/`: the six isolated native-scale frames
- `*_poses_master_rgba.png`: the unsized six-pose master sheet
- `*_edge_qa_preview.png`: dark/red/blue/green compositing checks

No pose frame was resampled. Only transparent outer padding was cropped. Empty pixels are true straight-alpha RGBA with zeroed RGB, transparent corners, and no bright checker matte or halo.

## Generation prompt set

Built-in ImageGen was used in reference-image mode, one character per supplied intro card. Each prompt locked face, age, body, hair, costume construction, insignia, palette, equipment, proportions, and high-resolution Neo-Geo/arcade pixel rendering across a six-pose horizontal master. The prompt required complete head-to-toe figures, a common ground line, true front and rear construction, no environment, no UI, no labels, no props not present in the identity design, and zero-alpha empty space.

Because ImageGen returned an opaque checker preview despite the alpha request, the sprite pipeline removed the connected bright-neutral matte deterministically, discarded isolated generator specks, split the six largest connected silhouettes, and verified the edges over four saturated/dark backdrops. See `manifest.json` for source crops, native dimensions, hashes, corner-alpha checks, and exposed-matte counts.

## Recommended use

Composite these masters directly into the FURY HQ plates, then resize the finished shot for the target display. This keeps the character pixel detail available for camera pushes, parallax, and alternate crops.
