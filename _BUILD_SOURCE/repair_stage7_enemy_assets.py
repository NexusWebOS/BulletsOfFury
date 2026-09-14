#!/usr/bin/env python3
"""Rebuild the active Stage-7 enemy reels with stable anchors and clean black rims.

The combat-pack source is a labelled 4x3 preview GIF.  The previous extractor cropped each
256px cell to 200px, then erased another ten rows and re-centred every attack frame separately.
That clipped low muzzle art and made the hull anchor move between frames.  This repair keeps the
complete hull plus vivid attack FX below the label line, anchors every frame to frame 01, rejects
detached preview fragments, and converts only transparency-edge purple to black without changing
alpha.
"""

from __future__ import annotations

from collections import Counter, deque
import json
from pathlib import Path
import shutil

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "_BUILD_SOURCE" / "review_combat_packs_2026-08-24" / \
    "CF_EnemyCombatPatterns-Vol.1" / "Level-7" / "Documentation" / \
    "CF_EnemyCombatSystems-Lvl7-preview.gif"
OUT = ROOT / "assets" / "game" / "stage7_enemy_attacks"
PROOF = ROOT / "_BUILD_SOURCE" / "stage7_enemy_cleanup"
BACKUP = PROOF / "original_active"

NAMES = [
    "armored_lamprey", "armored_sludge_barge", "dual_scoop_dredger", "pipe_crawler",
    "piston_pump_walker", "sampling_drone", "sewer_serpent", "sludge_mine",
    "toxic_canister", "toxic_mini_tank", "toxic_skimmer", "valve_turret",
]


def clear_preview_backdrop(cell: Image.Image) -> Image.Image:
    """Flood-clear only the dominant edge-connected navy checker colours."""
    rgba = cell.convert("RGBA")
    colors = Counter(rgba.getdata())
    backdrop = {px for px, count in colors.most_common(12) if count > 300 and max(px[:3]) < 80}
    pix = rgba.load()
    w, h = rgba.size
    seen: set[tuple[int, int]] = set()
    todo: deque[tuple[int, int]] = deque()
    for x in range(w):
        todo.extend(((x, 0), (x, h - 1)))
    for y in range(h):
        todo.extend(((0, y), (w - 1, y)))
    while todo:
        x, y = todo.popleft()
        if (x, y) in seen or pix[x, y] not in backdrop:
            continue
        seen.add((x, y))
        pix[x, y] = (0, 0, 0, 0)
        if x: todo.append((x - 1, y))
        if x + 1 < w: todo.append((x + 1, y))
        if y: todo.append((x, y - 1))
        if y + 1 < h: todo.append((x, y + 1))
    return rgba


def components(image: Image.Image) -> list[tuple[list[tuple[int, int]], tuple[int, int, int, int]]]:
    alpha = image.getchannel("A")
    ap = alpha.load()
    unseen = {(x, y) for y in range(image.height) for x in range(image.width) if ap[x, y] >= 40}
    found = []
    while unseen:
        start = unseen.pop()
        points = [start]
        todo = [start]
        while todo:
            x, y = todo.pop()
            for nx, ny in (
                (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1),
                (x - 1, y - 1), (x + 1, y - 1),
                (x - 1, y + 1), (x + 1, y + 1),
            ):
                if (nx, ny) in unseen:
                    unseen.remove((nx, ny))
                    todo.append((nx, ny))
                    points.append((nx, ny))
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        found.append((points, (min(xs), min(ys), max(xs) + 1, max(ys) + 1)))
    return found


def keep_unit_and_fx(image: Image.Image) -> Image.Image:
    """Discard labels and detached preview debris while keeping nearby muzzle/charge FX."""
    rgba = image.convert("RGBA")
    px = rgba.load()
    # The row labels overlap y=190 onward by a few pixels in some cells. The hulls end above
    # that line; vivid green toxic muzzle/charge pixels are the only authored art allowed below.
    for y in range(190, rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            toxic_fx = a >= 40 and g >= 85 and g > r * 1.10 and g > b * 0.88
            if not toxic_fx:
                px[x, y] = (0, 0, 0, 0)

    comps = components(rgba)
    if not comps:
        raise RuntimeError("empty Stage-7 source cell")
    main_points, main_box = max(comps, key=lambda item: len(item[0]))
    mx0, my0, mx1, my1 = main_box
    keep = set(main_points)
    for points, (x0, y0, x1, y1) in comps:
        if points is main_points:
            continue
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        close_to_hull = mx0 - 24 <= cx <= mx1 + 24 and my0 - 18 <= cy <= my1 + 28
        authored_fx = len(points) >= 4 and close_to_hull
        if authored_fx:
            keep.update(points)

    out = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
    src, dst = rgba.load(), out.load()
    for x, y in keep:
        dst[x, y] = src[x, y]
    return out


def blacken_purple_rim(image: Image.Image) -> tuple[Image.Image, int]:
    """Convert saturated purple on the transparent boundary to black; preserve alpha."""
    out = image.copy()
    src = image.load()
    dst = out.load()
    changed = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = src[x, y]
            if not (a >= 40 and r > 90 and b > 90 and g < min(r, b) * 0.62):
                continue
            boundary = False
            for nx, ny in (
                (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1),
                (x - 1, y - 1), (x + 1, y - 1),
                (x - 1, y + 1), (x + 1, y + 1),
            ):
                if nx < 0 or ny < 0 or nx >= image.width or ny >= image.height or src[nx, ny][3] < 40:
                    boundary = True
                    break
            if boundary:
                dst[x, y] = (0, 0, 0, a)
                changed += 1
    return out, changed


def anchored(image: Image.Image, offset: tuple[int, int]) -> Image.Image:
    out = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    out.alpha_composite(image, offset)
    return out


def checker(size: tuple[int, int]) -> Image.Image:
    out = Image.new("RGBA", size, (17, 23, 29, 255))
    draw = ImageDraw.Draw(out)
    for y in range(0, size[1], 16):
        for x in range(0, size[0], 16):
            if (x // 16 + y // 16) & 1:
                draw.rectangle((x, y, x + 15, y + 15), fill=(29, 37, 44, 255))
    return out


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    OUT.mkdir(parents=True, exist_ok=True)
    PROOF.mkdir(parents=True, exist_ok=True)
    BACKUP.mkdir(parents=True, exist_ok=True)

    source = Image.open(SOURCE)
    source_frames = []
    for frame_index in range(source.n_frames):
        source.seek(frame_index)
        source_frames.append(source.convert("RGBA"))

    before = checker((8 * 280, len(NAMES) * 300))
    after = checker((8 * 280, len(NAMES) * 300))
    before_draw = ImageDraw.Draw(before)
    after_draw = ImageDraw.Draw(after)
    font = ImageFont.load_default()
    report = []

    for unit_index, name in enumerate(NAMES):
        col, row = unit_index % 4, unit_index // 4
        recovered = []
        for frame in source_frames:
            cell = frame.crop((col * 256, row * 256, col * 256 + 256, row * 256 + 256))
            recovered.append(keep_unit_and_fx(clear_preview_backdrop(cell)))

        idle_bbox = recovered[0].getbbox()
        if not idle_bbox:
            raise RuntimeError(f"{name}: empty idle frame")
        idle_cx = (idle_bbox[0] + idle_bbox[2]) // 2
        idle_cy = (idle_bbox[1] + idle_bbox[3]) // 2
        offset = (128 - idle_cx, 128 - idle_cy)
        unit_out = OUT / name
        unit_out.mkdir(parents=True, exist_ok=True)
        halo_total = 0
        frames_report = []

        for frame_index, recovered_frame in enumerate(recovered):
            source_path = unit_out / f"{frame_index + 1:02d}.png"
            backup_path = BACKUP / name / source_path.name
            if source_path.is_file() and not backup_path.exists():
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, backup_path)

            cleaned, changed = blacken_purple_rim(recovered_frame)
            final = anchored(cleaned, offset)
            final_bbox = final.getbbox()
            if not final_bbox:
                raise RuntimeError(f"{name} frame {frame_index + 1}: empty output")
            if final_bbox[0] <= 2 or final_bbox[1] <= 2 or final_bbox[2] >= 254 or final_bbox[3] >= 254:
                raise RuntimeError(f"{name} frame {frame_index + 1}: unsafe canvas bbox {final_bbox}")
            final.save(source_path, optimize=True)
            halo_total += changed
            frames_report.append({"frame": frame_index + 1, "bbox": final_bbox, "blackened": changed})

            old_path = BACKUP / name / source_path.name
            if old_path.is_file():
                old = Image.open(old_path).convert("RGBA")
                old_tile = checker((256, 256))
                old_tile.alpha_composite(old)
                before.alpha_composite(old_tile, (frame_index * 280 + 12, unit_index * 300 + 26))
            new_tile = checker((256, 256))
            new_tile.alpha_composite(final)
            after.alpha_composite(new_tile, (frame_index * 280 + 12, unit_index * 300 + 26))

        label = name.upper()
        before_draw.text((12, unit_index * 300 + 6), label, font=font, fill=(161, 255, 123, 255))
        after_draw.text((12, unit_index * 300 + 6), f"{label}  BLACK RIM {halo_total}px", font=font,
                        fill=(161, 255, 123, 255))
        report.append({"unit": name, "anchor_offset": offset, "blackened": halo_total,
                       "frames": frames_report})

    before.save(PROOF / "stage7_enemy_before_repair.png", optimize=True)
    after.save(PROOF / "stage7_enemy_after_repair.png", optimize=True)
    (PROOF / "stage7_enemy_repair.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("unit\tblackened\tanchor_offset\toutput_union")
    for row in report:
        boxes = [frame["bbox"] for frame in row["frames"]]
        union = (min(b[0] for b in boxes), min(b[1] for b in boxes),
                 max(b[2] for b in boxes), max(b[3] for b in boxes))
        print(f"{row['unit']}\t{row['blackened']}\t{row['anchor_offset']}\t{union}")


if __name__ == "__main__":
    main()
