#!/usr/bin/env python3
"""Normalize the generated Stage-8 symbiote boss, entrance, and six weapon families."""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "_BUILD_SOURCE" / "stage8_symbiote_generated"
BOSS = ROOT / "assets" / "game" / "stage8_symbiote_boss"
FLEET = ROOT / "assets" / "game" / "stage8_symbiote_fleet"
PROOF = ROOT / "docs" / "proofs" / "stage8_symbiote_boss"

SLUGS = [
    "armored_gunship", "needle_interceptor", "scout_drone",
    "solar_corvette", "spread_wing_fighter", "stealth_crescent",
]

# The generated 6x8 plate obeys row/column order but leaves asymmetric outer padding.  These
# measured centers preserve every complete projectile instead of slicing the last column.
WEAPON_X = [112, 292, 462, 633, 812, 972, 1130, 1288]
WEAPON_Y = [112, 280, 448, 616, 786, 958]


def neutral_backdrop(image: Image.Image) -> Image.Image:
    """Flood the pale checker from the border, preserving enclosed white hot cores."""
    a = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    rgb = a[..., :3]
    candidate = ((rgb.max(2).astype(np.int16) - rgb.min(2).astype(np.int16)) <= 16) & (rgb.min(2) >= 205)
    h, w = candidate.shape
    seen = np.zeros((h, w), dtype=np.uint8)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        if candidate[0, x]: seen[0, x] = 1; q.append((x, 0))
        if candidate[h - 1, x]: seen[h - 1, x] = 1; q.append((x, h - 1))
    for y in range(h):
        if candidate[y, 0] and not seen[y, 0]: seen[y, 0] = 1; q.append((0, y))
        if candidate[y, w - 1] and not seen[y, w - 1]: seen[y, w - 1] = 1; q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h and candidate[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = 1
                q.append((nx, ny))
    a[seen.astype(bool), 3] = 0
    # Any pale antialias fringe immediately touching the removed checker is matte, not artwork.
    transparent = a[..., 3] == 0
    for _ in range(3):
        near = np.zeros_like(transparent)
        near[1:] |= transparent[:-1]
        near[:-1] |= transparent[1:]
        near[:, 1:] |= transparent[:, :-1]
        near[:, :-1] |= transparent[:, 1:]
        chroma = rgb.max(2).astype(np.int16) - rgb.min(2).astype(np.int16)
        fringe = near & (a[..., 3] > 0) & (rgb.min(2) >= 172) & (chroma <= 24)
        a[fringe, 3] = 0
        transparent |= fringe
    return Image.fromarray(a, "RGBA")


def normalize_cell(cell: Image.Image, side: int, fill: int) -> Image.Image:
    alpha = np.asarray(cell.getchannel("A"))
    ys, xs = np.where(alpha > 0)
    if not len(xs):
        return Image.new("RGBA", (side, side))
    crop = cell.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
    scale = min(fill / crop.width, fill / crop.height)
    size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
    crop = crop.resize(size, Image.Resampling.NEAREST)
    out = Image.new("RGBA", (side, side))
    out.alpha_composite(crop, ((side - size[0]) // 2, (side - size[1]) // 2))
    return out


def black_rim_key_spill(frame: Image.Image, passes: int = 4) -> Image.Image:
    """Turn only saturated magenta pixels on the alpha perimeter into dark organic rim ink."""
    a = np.asarray(frame.convert("RGBA"), dtype=np.uint8).copy()
    opaque = a[..., 3] > 0
    frontier = ~opaque
    band = np.zeros_like(opaque)
    for _ in range(passes):
        near = np.zeros_like(opaque)
        near[1:] |= frontier[:-1]
        near[:-1] |= frontier[1:]
        near[:, 1:] |= frontier[:, :-1]
        near[:, :-1] |= frontier[:, 1:]
        new = near & opaque & ~band
        band |= new
        frontier |= new
    r, g, b = (a[..., c].astype(np.int16) for c in range(3))
    spill = band & (r > 175) & (b > 175) & (g < 105) & (np.abs(r - b) < 85)
    lum = np.clip((r * 54 + g * 183 + b * 19) // 256, 4, 30).astype(np.uint8)
    a[..., 0][spill] = lum[spill]
    a[..., 1][spill] = np.maximum(2, lum[spill] // 5)
    a[..., 2][spill] = np.maximum(4, lum[spill] // 3)
    return Image.fromarray(a, "RGBA")


def fixed_cell(cell: Image.Image, side: int) -> Image.Image:
    """Resize a complete atlas cell; never normalize individual effect silhouettes."""
    return cell.resize((side, side), Image.Resampling.NEAREST)


def keep_center_components(cell: Image.Image) -> Image.Image:
    """Drop generation spill from neighbouring atlas cells, retaining center-owned FX only."""
    a = np.asarray(cell.convert("RGBA"), dtype=np.uint8).copy()
    mask = a[..., 3] > 0
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=np.uint8)
    keep = np.zeros_like(mask, dtype=bool)
    cx, cy = (w - 1) / 2, (h - 1) / 2
    for sy in range(h):
        for sx in range(w):
            if not mask[sy, sx] or seen[sy, sx]:
                continue
            q = deque([(sx, sy)])
            seen[sy, sx] = 1
            pts = []
            closest = 1e9
            while q:
                x, y = q.popleft()
                pts.append((x, y))
                closest = min(closest, (x - cx) ** 2 + (y - cy) ** 2)
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1),
                               (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)):
                    if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = 1
                        q.append((nx, ny))
            if closest <= (min(w, h) * .34) ** 2:
                for x, y in pts: keep[y, x] = True
    a[~keep, 3] = 0
    return Image.fromarray(a, "RGBA")


def clear_entrance_matte(cell: Image.Image, frame_index: int) -> Image.Image:
    """Remove checker trapped inside closed black rings; late central fusion cores remain."""
    a = np.asarray(cell.convert("RGBA"), dtype=np.uint8).copy()
    rgb = a[..., :3]
    neutral = ((rgb.max(2).astype(np.int16) - rgb.min(2).astype(np.int16)) <= 24) & (rgb.min(2) >= 168)
    if frame_index < 10:
        a[neutral, 3] = 0
    else:
        h, w = neutral.shape
        seen = np.zeros_like(neutral, dtype=np.uint8)
        preserve = np.zeros_like(neutral, dtype=bool)
        cx, cy = (w - 1) / 2, (h - 1) / 2
        for sy in range(h):
            for sx in range(w):
                if not neutral[sy, sx] or seen[sy, sx]:
                    continue
                q = deque([(sx, sy)])
                seen[sy, sx] = 1
                pts = []
                while q:
                    x, y = q.popleft(); pts.append((x, y))
                    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                        if 0 <= nx < w and 0 <= ny < h and neutral[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = 1; q.append((nx, ny))
                mx = sum(p[0] for p in pts) / len(pts)
                my = sum(p[1] for p in pts) / len(pts)
                if abs(mx - cx) <= w * .18 and abs(my - cy) <= h * .18 and len(pts) < w * h * .20:
                    for x, y in pts: preserve[y, x] = True
        a[neutral & ~preserve, 3] = 0
    return Image.fromarray(a, "RGBA")


def dark(frame: Image.Image, side: int | None = None) -> Image.Image:
    if side is None: side = frame.width
    bg = Image.new("RGB", (side, side), (9, 8, 13))
    f = frame if frame.size == bg.size else frame.resize(bg.size, Image.Resampling.NEAREST)
    bg.paste(f, (0, 0), f)
    return bg


def build_boss() -> list[Image.Image]:
    sheet = Image.open(SRC / "boss_forms_master.png").convert("RGBA")
    BOSS.mkdir(parents=True, exist_ok=True)
    frames = []
    for i in range(4):
        x0 = round(i * sheet.width / 4)
        x1 = round((i + 1) * sheet.width / 4)
        frame = black_rim_key_spill(normalize_cell(sheet.crop((x0, 0, x1, sheet.height)), 384, 344))
        frame.save(BOSS / f"form_{i + 1}.png")
        frames.append(frame)
    return frames


def build_entrance() -> list[Image.Image]:
    sheet = neutral_backdrop(Image.open(SRC / "entrance_fx_master.png"))
    frames = []
    for i in range(16):
        row, col = divmod(i, 4)
        x0, x1 = round(col * sheet.width / 4), round((col + 1) * sheet.width / 4)
        y0, y1 = round(row * sheet.height / 4), round((row + 1) * sheet.height / 4)
        cell = clear_entrance_matte(sheet.crop((x0, y0, x1, y1)), i)
        frame = fixed_cell(cell, 384)
        frame.save(BOSS / f"entrance_{i + 1:02d}.png")
        frames.append(frame)
    return frames


def build_weapons() -> dict[str, list[Image.Image]]:
    sheet = neutral_backdrop(Image.open(SRC / "fleet_weapon_fx_master.png"))
    rows: dict[str, list[Image.Image]] = {}
    for row, slug in enumerate(SLUGS):
        unit = FLEET / slug
        unit.mkdir(parents=True, exist_ok=True)
        row_frames = []
        for col in range(8):
            half = 90
            x0, x1 = WEAPON_X[col] - half, WEAPON_X[col] + half + 1
            y0, y1 = WEAPON_Y[row] - half, WEAPON_Y[row] + half + 1
            cell = keep_center_components(sheet.crop((x0, y0, x1, y1)))
            frame = fixed_cell(cell, 96)
            name = ("muzzle" if col < 4 else "projectile") + f"_{(col % 4) + 1:02d}.png"
            frame.save(unit / name)
            row_frames.append(frame)
        rows[slug] = row_frames
    return rows


def make_proofs(forms, entrance, weapons) -> None:
    PROOF.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    boss_board = Image.new("RGB", (4 * 404, 440), (6, 5, 9))
    draw = ImageDraw.Draw(boss_board)
    for i, f in enumerate(forms):
        tile = dark(f, 384)
        x = i * 404 + 10
        boss_board.paste(tile, (x, 10))
        draw.text((x + 8, 402), f"FORM {i + 1} — 25% TOTAL HP", fill=(255, 98, 71), font=font)
    boss_board.save(PROOF / "four_forms_contact.png")

    ent_board = Image.new("RGB", (4 * 256, 4 * 256), (7, 6, 10))
    for i, f in enumerate(entrance):
        ent_board.paste(dark(f, 256), ((i % 4) * 256, (i // 4) * 256))
    ent_board.save(PROOF / "entrance_16f_contact.png")
    gif = [dark(f, 256).convert("P", palette=Image.Palette.ADAPTIVE, colors=128) for f in entrance]
    gif[0].save(PROOF / "entrance_16f_preview.gif", save_all=True, append_images=gif[1:], duration=85, loop=0, disposal=2)

    fx = Image.new("RGB", (8 * 112, 6 * 128), (8, 8, 13))
    fd = ImageDraw.Draw(fx)
    for row, slug in enumerate(SLUGS):
        for col, f in enumerate(weapons[slug]):
            fx.paste(dark(f, 96), (col * 112 + 8, row * 128 + 4))
        fd.text((8, row * 128 + 103), slug.replace("_", " ").upper(), fill=(224, 228, 240), font=font)
    fx.save(PROOF / "fleet_weapon_fx_contact.png")


def main() -> None:
    forms = build_boss()
    entrance = build_entrance()
    weapons = build_weapons()
    make_proofs(forms, entrance, weapons)
    prompt_record = {
        "boss_mode": "imagegen new four-form horizontal master; deterministic fixed-pivot split",
        "entrance_mode": "imagegen sixteen-frame 4x4 master; deterministic row-major split",
        "weapon_mode": "imagegen six-family 6x8 master; deterministic fixed-cell split",
        "form_count": 4, "form_hp_share": [0.25, 0.25, 0.25, 0.25],
        "entrance_frames": 16, "muzzle_frames_per_unit": 4, "projectile_frames_per_unit": 4,
    }
    (BOSS / "build.json").write_text(json.dumps(prompt_record, indent=2), encoding="utf-8")
    print(json.dumps(prompt_record, indent=2))


if __name__ == "__main__":
    main()
