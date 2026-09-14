#!/usr/bin/env python3
"""Audit active Stage-7 enemy reels for clipped silhouettes and magenta edge spill."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets" / "game" / "stage7_enemy_attacks"
PROOF_ROOT = ROOT / "_BUILD_SOURCE" / "stage7_enemy_cleanup"


def edge_mask(alpha: Image.Image) -> Image.Image:
    """Return opaque pixels directly adjacent to transparency or the canvas edge."""
    w, h = alpha.size
    ap = alpha.load()
    edge = Image.new("L", (w, h), 0)
    ep = edge.load()
    for y in range(h):
        for x in range(w):
            if not ap[x, y]:
                continue
            if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                ep[x, y] = 255
                continue
            if any(
                not ap[nx, ny]
                for nx, ny in (
                    (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1),
                    (x - 1, y - 1), (x + 1, y - 1),
                    (x - 1, y + 1), (x + 1, y + 1),
                )
            ):
                ep[x, y] = 255
    return edge


def is_magenta_spill(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    # Project standing rule: only the saturated purple family on the OUTER rim is a halo.
    # Interior purple armor remains authored colour.
    return bool(a >= 40 and r > 90 and b > 90 and g < min(r, b) * 0.62)


def checker(size: tuple[int, int]) -> Image.Image:
    out = Image.new("RGBA", size, (17, 23, 29, 255))
    draw = ImageDraw.Draw(out)
    step = 16
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) & 1:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill=(28, 36, 43, 255))
    return out


def main() -> None:
    PROOF_ROOT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    units = sorted(path for path in ASSET_ROOT.iterdir() if path.is_dir())
    sheet = checker((8 * 280, len(units) * 300))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for row_index, unit in enumerate(units):
        union: tuple[int, int, int, int] | None = None
        unit_rows = []
        for frame_index, path in enumerate(sorted(unit.glob("*.png"))):
            image = Image.open(path).convert("RGBA")
            bbox = image.getbbox()
            if bbox:
                union = bbox if union is None else (
                    min(union[0], bbox[0]), min(union[1], bbox[1]),
                    max(union[2], bbox[2]), max(union[3], bbox[3]),
                )
            edge = edge_mask(image.getchannel("A"))
            ep = edge.load()
            px = image.load()
            magenta_edge = sum(
                1
                for y in range(image.height)
                for x in range(image.width)
                if ep[x, y] and is_magenta_spill(px[x, y])
            )
            touches = []
            if bbox:
                if bbox[0] == 0: touches.append("left")
                if bbox[1] == 0: touches.append("top")
                if bbox[2] == image.width: touches.append("right")
                if bbox[3] == image.height: touches.append("bottom")
            unit_rows.append({
                "frame": path.name,
                "bbox": bbox,
                "touches_canvas": touches,
                "magenta_edge_pixels": magenta_edge,
            })

            tile = checker((256, 256))
            tile.alpha_composite(image)
            tile_draw = ImageDraw.Draw(tile)
            if bbox:
                tile_draw.rectangle((bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1), outline=(255, 202, 56, 255))
            x0, y0 = frame_index * 280 + 12, row_index * 300 + 26
            sheet.alpha_composite(tile, (x0, y0))
            draw.text((x0 + 4, y0 + 4), f"{frame_index + 1}: M{magenta_edge}", font=font,
                      fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))

        rows.append({"unit": unit.name, "union_bbox": union, "frames": unit_rows})
        draw.text((12, row_index * 300 + 6), unit.name.upper(), font=font,
                  fill=(161, 255, 123, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))

    (PROOF_ROOT / "stage7_enemy_audit.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    sheet.save(PROOF_ROOT / "stage7_enemy_before_contact.png", optimize=True)

    print("unit\tunion_bbox\tcanvas_touches\tmagenta_edge_pixels")
    for row in rows:
        touches = sorted({side for frame in row["frames"] for side in frame["touches_canvas"]})
        magenta = sum(frame["magenta_edge_pixels"] for frame in row["frames"])
        print(f"{row['unit']}\t{row['union_bbox']}\t{','.join(touches) or '-'}\t{magenta}")


if __name__ == "__main__":
    main()
