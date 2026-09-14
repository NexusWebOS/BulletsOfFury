#!/usr/bin/env python3
"""Recover the approved Level-7 sewer roster and spore-crown reels from previews."""

from __future__ import annotations

from collections import Counter, deque
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "_BUILD_SOURCE" / "review_combat_packs_2026-08-24" / \
    "CF_EnemyCombatPatterns-Vol.1" / "Level-7"
SOURCE = PACK / "Documentation" / "CF_EnemyCombatSystems-Lvl7-preview.gif"
SPORE_SOURCE = PACK / "Elite-Previews" / "VFX-Elite-spore-crown" / \
    "lvl7-elite-spore-crown-preview.gif"
OUT = ROOT / "assets" / "game" / "stage7_enemy_attacks"
SPORE_OUT = ROOT / "assets" / "game" / "stage7_spore_crown"
PROOF = ROOT / "_BUILD_SOURCE" / "stage7_enemy_redesign"

NAMES = [
    "armored_lamprey", "armored_sludge_barge", "dual_scoop_dredger", "pipe_crawler",
    "piston_pump_walker", "sampling_drone", "sewer_serpent", "sludge_mine",
    "toxic_canister", "toxic_mini_tank", "toxic_skimmer", "valve_turret",
]


def edge_clear(cell: Image.Image) -> Image.Image:
    rgba = cell.convert("RGBA")
    colors = Counter(rgba.getdata())
    background = {px for px, _ in colors.most_common(8) if max(px[:3]) < 75}
    w, h = rgba.size
    pix = rgba.load()
    seen: set[tuple[int, int]] = set()
    todo: deque[tuple[int, int]] = deque()
    for x in range(w):
        todo.extend(((x, 0), (x, h - 1)))
    for y in range(h):
        todo.extend(((0, y), (w - 1, y)))
    while todo:
        x, y = todo.popleft()
        if (x, y) in seen or pix[x, y] not in background:
            continue
        seen.add((x, y)); pix[x, y] = (0, 0, 0, 0)
        if x: todo.append((x - 1, y))
        if x + 1 < w: todo.append((x + 1, y))
        if y: todo.append((x, y - 1))
        if y + 1 < h: todo.append((x, y + 1))
    return rgba


def keep_hull(cell: Image.Image, floor: int = 190) -> Image.Image:
    w, h = cell.size
    px = cell.load()
    for y in range(floor, h):
        for x in range(w):
            px[x, y] = (0, 0, 0, 0)
    alpha = cell.getchannel("A"); ap = alpha.load()
    unseen = {(x, y) for y in range(h) for x in range(w) if ap[x, y]}
    comps = []
    while unseen:
        start = unseen.pop(); points = [start]; todo = [start]
        while todo:
            x, y = todo.pop()
            for q in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if q in unseen:
                    unseen.remove(q); todo.append(q); points.append(q)
        xs = [p[0] for p in points]; ys = [p[1] for p in points]
        comps.append((points, (min(xs), min(ys), max(xs) + 1, max(ys) + 1)))
    if not comps:
        return cell
    main_points, main_box = max(comps, key=lambda c: len(c[0]))
    mx0, my0, mx1, my1 = main_box; keep = set(main_points)
    for points, (x0, y0, x1, y1) in comps:
        if points is main_points:
            continue
        cx = (x0 + x1) / 2
        if len(points) >= 5 and mx0 - 14 <= cx <= mx1 + 14 and y0 <= my1 + 8 and y1 >= my0 - 8:
            keep.update(points)
    out = Image.new("RGBA", cell.size, (0, 0, 0, 0)); src, dst = cell.load(), out.load()
    for x, y in keep:
        dst[x, y] = src[x, y]
    return out


def stable_canvas(cleaned: Image.Image) -> Image.Image:
    bbox = cleaned.getbbox()
    if not bbox:
        raise RuntimeError("empty recovered frame")
    canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    # Keep the preview cell's original pivot. Per-frame tight crops made muzzle flashes shift
    # the hull and the old 190px floor clipped low weapon art.
    canvas.alpha_composite(cleaned, (0, 0))
    return canvas


def clear_checker(frame: Image.Image) -> Image.Image:
    rgba = frame.convert("RGBA")
    colors = Counter(rgba.getdata())
    # The supplied preview uses two exact navy checker colours. They account for roughly
    # 48k of 65k pixels, so selecting only dominant colours avoids eating dark hull pixels.
    checker = {px for px, count in colors.most_common(8) if count > 1000}
    pix = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            if pix[x, y] in checker:
                pix[x, y] = (0, 0, 0, 0)
    return rgba


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True); SPORE_OUT.mkdir(parents=True, exist_ok=True)
    PROOF.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE); frames = []
    for i in range(source.n_frames):
        source.seek(i); frames.append(source.convert("RGBA"))
    contact = Image.new("RGBA", (4 * 280, 3 * 270), (7, 15, 28, 255))
    draw = ImageDraw.Draw(contact)
    for index, name in enumerate(NAMES):
        col, row = index % 4, index // 4
        unit_out = OUT / name; unit_out.mkdir(parents=True, exist_ok=True)
        recovered = []
        for fi, frame in enumerate(frames):
            cell = frame.crop((col * 256, row * 256, col * 256 + 256, row * 256 + 200))
            canvas = stable_canvas(keep_hull(edge_clear(cell)))
            canvas.save(unit_out / f"{fi + 1:02d}.png", optimize=True); recovered.append(canvas)
        thumb = recovered[3].copy(); thumb.thumbnail((228, 220), Image.Resampling.NEAREST)
        contact.alpha_composite(thumb, (col * 280 + (280 - thumb.width) // 2,
                                        row * 270 + 4 + (220 - thumb.height) // 2))
        draw.text((col * 280 + 10, row * 270 + 236), name.upper(), fill=(161, 255, 123, 255))
    contact.save(PROOF / "stage7_recovered_roster.png")

    spore = Image.open(SPORE_SOURCE)
    strip = Image.new("RGBA", (12 * 128, 128), (7, 15, 28, 255))
    for fi in range(spore.n_frames):
        spore.seek(fi); cleaned = clear_checker(spore.convert("RGBA"))
        cleaned.save(SPORE_OUT / f"{fi + 1:02d}.png", optimize=True)
        thumb = cleaned.copy(); thumb.thumbnail((120, 120), Image.Resampling.NEAREST)
        strip.alpha_composite(thumb, (fi * 128 + (128 - thumb.width) // 2, (128 - thumb.height) // 2))
    strip.save(PROOF / "stage7_spore_crown_strip.png")

    # The labelled roster GIF needs a second pass for shared pivots, label rejection and the
    # project's black-edge halo rule. Keep this call here so rerunning the extractor cannot
    # silently restore the old cropped/haloed enemy plates.
    from repair_stage7_enemy_assets import main as repair_stage7_enemy_assets
    repair_stage7_enemy_assets()


if __name__ == "__main__":
    main()
