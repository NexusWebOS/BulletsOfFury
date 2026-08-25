from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parent
PROJECTILES = BASE / "candidates" / "projectiles"
DAMAGE = BASE / "candidates" / "damage_effects"
ROOT = BASE.parents[1]


def visible_magenta(image: Image.Image) -> int:
    return sum(1 for r, g, b, a in image.convert("RGBA").getdata() if a and r >= 250 and b >= 250 and g <= 5)


projectile_families = 0
projectile_frames = 0
atlas_mismatches = []
magenta_pixels = 0
for family in sorted(path for path in PROJECTILES.iterdir() if path.is_dir()):
    metadata_paths = list(family.glob("*.json"))
    if not metadata_paths:
        continue
    metadata = json.loads(metadata_paths[0].read_text(encoding="utf-8"))
    atlas_path = family / metadata["atlas"]["file"]
    if not atlas_path.exists():
        atlas_mismatches.append(f"{family.name}:missing_atlas")
        continue
    atlas = Image.open(atlas_path).convert("RGBA")
    projectile_families += 1
    for frame_name, rect in metadata["atlas"]["rects"].items():
        x, y, width, height = rect
        standalone = Image.open(family / f"{frame_name}.png").convert("RGBA")
        cut = atlas.crop((x, y, x + width, y + height))
        projectile_frames += 1
        magenta_pixels += visible_magenta(standalone)
        if standalone.tobytes() != cut.tobytes():
            atlas_mismatches.append(f"{family.name}:{frame_name}")

damage_reels = 0
damage_frames = 0
damage_failures = []
alpha_motion_reels = 0

js = r'''
global.window={}; require('./assets/manifest.js');
const c=window.BOFX.cells||{}, i=window.BOFX.img||{}, out={};
for(const key of Object.keys(c).filter(k=>/_(damaged|critical)(?:_idle)?$/.test(k))){
  const candidates=[key.replace(/_(damaged|critical)(_idle)?$/, '_intact$2'),key.replace(/_(damaged|critical)(_idle)?$/, '$2'),key.replace(/_(damaged|critical)(_idle)?$/, '')];
  const intactKey=candidates.find(candidate=>c[candidate]);
  if(intactKey) out[key]={damagedCell:c[key],damagedImg:i[key]||null,intactCell:c[intactKey],intactImg:i[intactKey]||null};
}
process.stdout.write(JSON.stringify(out));
'''
manifest_defs = json.loads(subprocess.run(["node", "-e", js], cwd=ROOT, check=True, capture_output=True, text=True).stdout)


def crop_manifest(cell, image_path):
    atlas_index, x, y, width, height = [int(value) for value in cell]
    atlas = Image.open(ROOT / (image_path or f"assets/game/atlas/nca_{atlas_index}.png")).convert("RGBA")
    return atlas.crop((x, y, x + width, y + height))


for reel in sorted(path for path in DAMAGE.iterdir() if path.is_dir()):
    frames = [Image.open(path).convert("RGBA") for path in sorted(reel.glob("*.png"))]
    if len(frames) != 8:
        damage_failures.append(f"{reel.name}:frame_count={len(frames)}")
        continue
    damage_reels += 1
    damage_frames += len(frames)
    first_size = frames[0].size
    first_alpha = frames[0].getchannel("A").tobytes()
    if any(frame.size != first_size for frame in frames):
        damage_failures.append(f"{reel.name}:dimension_drift")
    if len({frame.tobytes() for frame in frames}) < 2:
        damage_failures.append(f"{reel.name}:no_animation")
    if len({frame.getchannel("A").tobytes() for frame in frames}) > 1:
        alpha_motion_reels += 1
    definition = manifest_defs.get(reel.name)
    if not definition:
        damage_failures.append(f"{reel.name}:missing_manifest_definition")
    else:
        damaged_source = crop_manifest(definition["damagedCell"], definition.get("damagedImg"))
        intact_source = crop_manifest(definition["intactCell"], definition.get("intactImg"))
        if damaged_source.size != frames[0].size or damaged_source.tobytes() != frames[0].tobytes():
            damage_failures.append(f"{reel.name}:frame01_not_exact_source")
        if intact_source.size == frames[0].size:
            intact_alpha = intact_source.getchannel("A")
            damaged_alpha = damaged_source.getchannel("A")
            for index, frame in enumerate(frames[1:], start=2):
                holes = sum(
                    1
                    for ia, da, fa in zip(intact_alpha.getdata(), damaged_alpha.getdata(), frame.getchannel("A").getdata())
                    if ia and da and not fa
                )
                if holes:
                    damage_failures.append(f"{reel.name}:frame{index:02d}_hull_alpha_holes={holes}")
                    break
    magenta_pixels += sum(visible_magenta(frame) for frame in frames)

result = {
    "projectile_families": projectile_families,
    "projectile_frames": projectile_frames,
    "projectile_atlas_mismatches": atlas_mismatches,
    "damage_reels": damage_reels,
    "damage_frames": damage_frames,
    "damage_reels_with_effect_alpha_motion": alpha_motion_reels,
    "damage_failures": damage_failures,
    # Informational only: several approved cosmic/energy assets intentionally use
    # saturated magenta as part of their palette, so its presence is not a failure.
    "visible_magenta_palette_pixels": magenta_pixels,
    "passed": not atlas_mismatches and not damage_failures,
}
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["passed"] else 1)
