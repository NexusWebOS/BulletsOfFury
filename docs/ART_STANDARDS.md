# Bullets of Fury — Enemy Sprite Scale Standard (v1)

**For incoming artists.** Every enemy, vehicle, turret, and destructible ships on a fixed canvas so the game never has to re-scale per unit.

## Canvas
- **Standard units:** 128 × 128 px, transparent (RGBA PNG).
- **Mini-boss / huge units:** 192 × 192 px.
- One sprite per canvas, **centered**.

## Silhouette fill (how much of the canvas the art occupies, by class)
| Class  | Examples                         | Fill of canvas (longest edge) | ~pixels |
|--------|----------------------------------|-------------------------------|---------|
| small  | drones, mines, darts             | 62%                           | ~80px   |
| medium | fighters, gunships, tanks, boats | 78%                           | ~100px  |
| large  | heavy tanks, turrets, naval guns | 88%                           | ~113px  |
| huge   | mini-boss craft (192 canvas)     | 88%                           | ~169px  |

## Orientation
- Enemies face **DOWN-SCREEN** (toward the player). Nose/guns point to the **bottom** of the canvas.
- Top-down or 3/4 view to match existing art.

## State columns (author left→right, one row per unit)
1. **idle** — resting/flying
2. **fire** — muzzle flash / firing pose
3. **hurt** — damaged, smoke
4. **death** — debris/explosion frame
(Optional extra columns for wreck / palette-variant are welcome; the pipeline reads the first 4 by default.)

## Edges & background
- Author on a solid **magenta (#FF00FF)** or **green (#00FF00)** chroma key. The pipeline removes it by hue (handles dark anti-aliased halo rings too).
- The pipeline adds a **2px near-black outline** at export — don't paint your own outline.

## In-game behavior (why this matters)
- The engine draws the whole canvas at the enemy's hitbox width `e.w`; scale is always `e.w / canvasSize`. Because every sprite shares the canvas size and fill fraction, **no per-enemy scale multipliers are needed** — footprints stay consistent and hitboxes line up with the art.

## Pipeline
`_BUILD_SOURCE/extract_enemies.py` slices atlas rows → despills key → places on class canvas → outlines → `assets/enemies/<prefix>_<name>_<state>.png` + `_keys.json`.
