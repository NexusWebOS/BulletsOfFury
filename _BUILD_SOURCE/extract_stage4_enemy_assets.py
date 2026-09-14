#!/usr/bin/env python3
"""Recover the approved 8-frame Level-4 combat reels from the pack preview.

The supplied Patterns archive carries lossless combat metadata and an animated
contact preview, but not the loose atlases named by that metadata.  This script
extracts the twelve 256px preview cells, removes only edge-connected checkerboard
pixels, and normalizes every frame to a stable 256px pivot for runtime use.
"""

from __future__ import annotations

from collections import Counter, deque
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "_BUILD_SOURCE"
    / "review_combat_packs_2026-08-24"
    / "CF_EnemyCombatPatterns-Vol.1"
    / "Level-4"
    / "Documentation"
    / "CF_EnemyCombatSystems-Lvl4-preview.gif"
)
OUT = ROOT / "assets" / "game" / "stage4_enemy_attacks"
PROOF = ROOT / "_BUILD_SOURCE" / "stage4_enemy_redesign"

NAMES = [
    "airfield_tank",
    "armored_tractor",
    "blacksite_interceptor",
    "command_plane",
    "explosive_barrel",
    "fuel_tanker",
    "gunship_bomber",
    "heavy_attack_jet",
    "missile_vehicle",
    "rocket_plane",
    "runway_mini_tank",
    "sam_carrier",
]


def edge_clear(cell: Image.Image) -> Image.Image:
    """Clear checkerboard reachable from the cell edge; preserve dark hull pixels."""
    rgba = cell.convert("RGBA")
    colors = Counter(rgba.getdata())
    # The preview checker consists of the two dominant opaque dark colours.
    background = {px for px, _ in colors.most_common(5) if max(px[:3]) < 60}
    w, h = rgba.size
    pix = rgba.load()
    seen: set[tuple[int, int]] = set()
    todo: deque[tuple[int, int]] = deque()
    for x in range(w):
        todo.append((x, 0))
        todo.append((x, h - 1))
    for y in range(h):
        todo.append((0, y))
        todo.append((w - 1, y))
    while todo:
        x, y = todo.popleft()
        if (x, y) in seen or pix[x, y] not in background:
            continue
        seen.add((x, y))
        pix[x, y] = (0, 0, 0, 0)
        if x:
            todo.append((x - 1, y))
        if x + 1 < w:
            todo.append((x + 1, y))
        if y:
            todo.append((x, y - 1))
        if y + 1 < h:
            todo.append((x, y + 1))
    return rgba


def keep_hull_components(cell: Image.Image) -> Image.Image:
    """Drop disconnected preview captions while retaining attached exhaust sparks."""
    w, h = cell.size
    px = cell.load()
    # All preview captions begin in this reserved strip. No authored hull reaches it; a few
    # detached exhaust sparks stop just above it.
    for y in range(190, h):
        for x in range(w):
            px[x, y] = (0, 0, 0, 0)
    alpha = cell.getchannel("A")
    ap = alpha.load()
    unseen = {(x, y) for y in range(h) for x in range(w) if ap[x, y]}
    comps: list[tuple[list[tuple[int, int]], tuple[int, int, int, int]]] = []
    while unseen:
        start = unseen.pop()
        points = [start]
        todo = [start]
        while todo:
            x, y = todo.pop()
            for q in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if q in unseen:
                    unseen.remove(q)
                    todo.append(q)
                    points.append(q)
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        comps.append((points, (min(xs), min(ys), max(xs) + 1, max(ys) + 1)))
    if not comps:
        return cell
    main_points, main_box = max(comps, key=lambda c: len(c[0]))
    mx0, my0, mx1, my1 = main_box
    keep = set(main_points)
    for points, (x0, y0, x1, y1) in comps:
        if points is main_points:
            continue
        # Engine flames and weapon sparks sit directly against the hull footprint.  Preview
        # captions sit lower and/or well outside it, so they are excluded without colour keys.
        cx = (x0 + x1) / 2
        if len(points) >= 5 and mx0 - 10 <= cx <= mx1 + 10 and y0 <= my1 + 5 and y1 >= my0 - 5:
            keep.update(points)
    out = Image.new("RGBA", cell.size, (0, 0, 0, 0))
    src, dst = cell.load(), out.load()
    for x, y in keep:
        dst[x, y] = src[x, y]
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PROOF.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE)
    frames: list[Image.Image] = []
    for i in range(source.n_frames):
        source.seek(i)
        frames.append(source.convert("RGBA"))

    contact = Image.new("RGBA", (4 * 280, 3 * 270), (7, 15, 28, 255))
    draw = ImageDraw.Draw(contact)
    for index, name in enumerate(NAMES):
        col, row = index % 4, index // 4
        unit_out = OUT / name
        unit_out.mkdir(parents=True, exist_ok=True)
        recovered: list[Image.Image] = []
        for fi, frame in enumerate(frames):
            # The label strip starts at y=200 inside each 256px tile.
            cell = frame.crop((col * 256, row * 256, col * 256 + 256, row * 256 + 200))
            cleaned = keep_hull_components(edge_clear(cell))
            bbox = cleaned.getbbox()
            if not bbox:
                raise RuntimeError(f"empty recovered cell: {name} frame {fi}")
            sprite = cleaned.crop(bbox)
            canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
            x = (256 - sprite.width) // 2
            # Keep the lower hardpoint stable and leave room for forward muzzle art.
            y = min(244 - sprite.height, (256 - sprite.height) // 2)
            canvas.alpha_composite(sprite, (x, y))
            canvas.save(unit_out / f"{fi + 1:02d}.png", optimize=True)
            recovered.append(canvas)

        thumb = recovered[3].copy()
        thumb.thumbnail((228, 220), Image.Resampling.NEAREST)
        px = col * 280 + (280 - thumb.width) // 2
        py = row * 270 + 4 + (220 - thumb.height) // 2
        contact.alpha_composite(thumb, (px, py))
        draw.text((col * 280 + 10, row * 270 + 236), name.upper(), fill=(148, 226, 255, 255))

    contact.save(PROOF / "stage4_recovered_roster.png")


if __name__ == "__main__":
    main()
