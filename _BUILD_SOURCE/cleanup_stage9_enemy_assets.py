#!/usr/bin/env python3
"""Remove leaked preview-caption islands from live Stage-9 enemy reels.

The operation is deliberately conservative: it keeps every connected hull, engine flare and
muzzle spark, changes no canvas dimensions or pivots, and only removes tiny glyph-like components
that sit in a detached caption band below the primary silhouette.
"""

from __future__ import annotations

import json
import shutil
from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets" / "game" / "stage9_enemy_attacks"
PROOF_ROOT = ROOT / "_BUILD_SOURCE" / "stage9_enemy_cleanup"
BACKUP_ROOT = PROOF_ROOT / "original_active"
CAPTION_UNITS = {"hyperspace_prism", "ring_drone", "singularity_mine"}


def components(alpha: Image.Image, cutoff: int = 8) -> list[dict[str, object]]:
    width, height = alpha.size
    source = alpha.load()
    seen = bytearray(width * height)
    found: list[dict[str, object]] = []
    for y0 in range(height):
        for x0 in range(width):
            index = y0 * width + x0
            if seen[index] or source[x0, y0] <= cutoff:
                continue
            seen[index] = 1
            queue: deque[tuple[int, int]] = deque([(x0, y0)])
            points: list[tuple[int, int]] = []
            while queue:
                x, y = queue.popleft()
                points.append((x, y))
                for nx in range(max(0, x - 1), min(width, x + 2)):
                    for ny in range(max(0, y - 1), min(height, y + 2)):
                        ni = ny * width + nx
                        if not seen[ni] and source[nx, ny] > cutoff:
                            seen[ni] = 1
                            queue.append((nx, ny))
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            found.append({
                "points": points,
                "pixels": len(points),
                "bbox": (min(xs), min(ys), max(xs) + 1, max(ys) + 1),
            })
    found.sort(key=lambda group: int(group["pixels"]), reverse=True)
    return found


def main() -> None:
    PROOF_ROOT.mkdir(parents=True, exist_ok=True)
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    report: list[dict[str, object]] = []
    total_removed = 0

    for unit in sorted(path for path in ASSET_ROOT.iterdir() if path.is_dir()):
        backup_dir = BACKUP_ROOT / unit.name
        backup_dir.mkdir(parents=True, exist_ok=True)
        for path in sorted(unit.glob("*.png")):
            backup = backup_dir / path.name
            if not backup.exists():
                shutil.copy2(path, backup)

            image = Image.open(path).convert("RGBA")
            groups = components(image.getchannel("A"))
            if not groups:
                continue
            main_bottom = groups[0]["bbox"][3]
            removed: list[dict[str, object]] = []
            pixels = image.load()
            if unit.name == "hyperspace_prism":
                alpha = image.getchannel("A")
                counts = [sum(alpha.getpixel((x, y)) > 8 for x in range(image.width))
                          for y in range(image.height)]
                for caption_y in range(int(image.height * 0.72), image.height):
                    if counts[caption_y] > 110 and counts[caption_y - 1] < 80:
                        count = 0
                        for y in range(caption_y, image.height):
                            for x in range(image.width):
                                if pixels[x, y][3] > 8:
                                    count += 1
                                pixels[x, y] = (0, 0, 0, 0)
                        removed.append({"pixels": count,
                                        "bbox": [0, caption_y, image.width, image.height]})
                        total_removed += count
                        break
            for group in groups[1:]:
                x0, y0, x1, y1 = group["bbox"]
                if (unit.name in CAPTION_UNITS and y0 >= main_bottom + 1 and
                        y1 - y0 <= 7 and group["pixels"] <= 100):
                    for x, y in group["points"]:
                        pixels[x, y] = (0, 0, 0, 0)
                    removed.append({"pixels": group["pixels"], "bbox": list(group["bbox"])})
                    total_removed += int(group["pixels"])

            # Transparent texels carry black RGB so browser filtering cannot resurrect a fringe.
            for y in range(image.height):
                for x in range(image.width):
                    if pixels[x, y][3] == 0:
                        pixels[x, y] = (0, 0, 0, 0)
            image.save(path, optimize=True)
            if removed:
                report.append({"unit": unit.name, "frame": path.name, "removed": removed})

    # Publish the complete delta from the recoverable originals, not just changes made by this run.
    verified: list[dict[str, object]] = []
    verified_removed = 0
    verified_added = 0
    for backup in sorted(BACKUP_ROOT.glob("*/*.png")):
        active = ASSET_ROOT / backup.parent.name / backup.name
        before = Image.open(backup).convert("RGBA")
        after = Image.open(active).convert("RGBA")
        bp, ap = before.load(), after.load()
        removed_count = added_count = 0
        for y in range(before.height):
            for x in range(before.width):
                was, now = bp[x, y][3] > 8, ap[x, y][3] > 8
                removed_count += int(was and not now)
                added_count += int(now and not was)
        if removed_count or added_count:
            verified.append({"unit": backup.parent.name, "frame": backup.name,
                             "removed_pixels": removed_count, "added_pixels": added_count})
            verified_removed += removed_count
            verified_added += added_count

    (PROOF_ROOT / "stage9_enemy_cleanup.json").write_text(
        json.dumps({"removed_pixels": verified_removed, "added_pixels": verified_added,
                    "changed_frames": len(verified), "frames": verified}, indent=2),
        encoding="utf-8",
    )
    print(f"removed {total_removed} pixels this run; verified {verified_removed} leaked pixels "
          f"removed and {verified_added} added across {len(verified)} Stage-9 frames")


if __name__ == "__main__":
    main()
