#!/usr/bin/env python3
"""Audit live Stage-9 enemy reels for clipping, chroma spill and stray pixel islands."""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets" / "game" / "stage9_enemy_attacks"
PROOF_ROOT = ROOT / "_BUILD_SOURCE" / "stage9_enemy_cleanup"


def components(alpha: Image.Image, cutoff: int = 8) -> list[dict[str, object]]:
    """Return 8-connected alpha components, largest first."""
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
                "pixels": len(points),
                "bbox": [min(xs), min(ys), max(xs) + 1, max(ys) + 1],
                "points": points,
            })
    found.sort(key=lambda component: int(component["pixels"]), reverse=True)
    return found


def edge_mask(alpha: Image.Image, cutoff: int = 8) -> Image.Image:
    width, height = alpha.size
    source = alpha.load()
    edge = Image.new("L", alpha.size, 0)
    output = edge.load()
    for y in range(height):
        for x in range(width):
            if source[x, y] <= cutoff:
                continue
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                output[x, y] = 255
                continue
            if any(source[nx, ny] <= cutoff for nx, ny in (
                (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1),
                (x - 1, y - 1), (x + 1, y - 1),
                (x - 1, y + 1), (x + 1, y + 1),
            )):
                output[x, y] = 255
    return edge


def is_magenta_spill(pixel: tuple[int, int, int, int]) -> bool:
    red, green, blue, alpha = pixel
    return bool(alpha >= 24 and red > 78 and blue > 78 and green < min(red, blue) * 0.58)


def checker(size: tuple[int, int]) -> Image.Image:
    output = Image.new("RGBA", size, (10, 14, 24, 255))
    draw = ImageDraw.Draw(output)
    for y in range(0, size[1], 16):
        for x in range(0, size[0], 16):
            if (x // 16 + y // 16) & 1:
                draw.rectangle((x, y, x + 15, y + 15), fill=(28, 34, 50, 255))
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="before")
    args = parser.parse_args()
    PROOF_ROOT.mkdir(parents=True, exist_ok=True)
    units = sorted(path for path in ASSET_ROOT.iterdir() if path.is_dir())
    font = ImageFont.load_default()
    sheet = checker((8 * 268, len(units) * 280))
    draw = ImageDraw.Draw(sheet)
    report: list[dict[str, object]] = []

    for row_index, unit in enumerate(units):
        frames: list[dict[str, object]] = []
        for frame_index, path in enumerate(sorted(unit.glob("*.png"))):
            image = Image.open(path).convert("RGBA")
            alpha = image.getchannel("A")
            bbox = alpha.point(lambda value: 255 if value > 8 else 0).getbbox()
            groups = components(alpha)
            edge = edge_mask(alpha)
            ep = edge.load()
            px = image.load()
            magenta = sum(
                1 for y in range(image.height) for x in range(image.width)
                if ep[x, y] and is_magenta_spill(px[x, y])
            )
            transparent_rgb = sum(
                1 for red, green, blue, a in image.getdata()
                if a == 0 and (red or green or blue)
            )
            touches: list[str] = []
            if bbox:
                if bbox[0] == 0: touches.append("left")
                if bbox[1] == 0: touches.append("top")
                if bbox[2] == image.width: touches.append("right")
                if bbox[3] == image.height: touches.append("bottom")
            frames.append({
                "frame": path.name,
                "size": list(image.size),
                "bbox": list(bbox) if bbox else None,
                "touches_canvas": touches,
                "magenta_edge_pixels": magenta,
                "transparent_rgb_pixels": transparent_rgb,
                "components": [
                    {"pixels": group["pixels"], "bbox": group["bbox"]}
                    for group in groups[:24]
                ],
            })

            tile = checker((256, 256))
            tile.alpha_composite(image)
            td = ImageDraw.Draw(tile)
            if bbox:
                td.rectangle((bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1), outline=(255, 201, 54, 255))
            stray_count = sum(1 for group in groups[1:] if int(group["pixels"]) <= 24)
            td.text((5, 5), f"F{frame_index + 1} C{len(groups)} S{stray_count} M{magenta}",
                    font=font, fill=(255, 255, 255, 255), stroke_width=2,
                    stroke_fill=(0, 0, 0, 255))
            x0, y0 = frame_index * 268 + 6, row_index * 280 + 20
            sheet.alpha_composite(tile, (x0, y0))

        report.append({"unit": unit.name, "frames": frames})
        draw.text((8, row_index * 280 + 4), unit.name.upper(), font=font,
                  fill=(112, 239, 255, 255), stroke_width=2,
                  stroke_fill=(0, 0, 0, 255))

    (PROOF_ROOT / f"stage9_enemy_audit_{args.tag}.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    sheet.save(PROOF_ROOT / f"stage9_enemy_{args.tag}_contact.png", optimize=True)

    print("unit\tframes\ttouches\tmagenta-edge\ttransparent-rgb\tsmall-islands")
    for row in report:
        frames = row["frames"]
        touches = sorted({side for frame in frames for side in frame["touches_canvas"]})
        magenta = sum(frame["magenta_edge_pixels"] for frame in frames)
        transparent = sum(frame["transparent_rgb_pixels"] for frame in frames)
        islands = sum(
            1 for frame in frames for group in frame["components"][1:]
            if group["pixels"] <= 24
        )
        print(f"{row['unit']}\t{len(frames)}\t{','.join(touches) or '-'}\t{magenta}\t{transparent}\t{islands}")


if __name__ == "__main__":
    main()
