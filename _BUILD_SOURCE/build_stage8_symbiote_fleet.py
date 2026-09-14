#!/usr/bin/env python3
"""Build the six user-supplied Stage-8 drones without altering their silhouettes.

The source plates are high-resolution pixel art on an opaque magenta key.  This builder:
  * removes only the connected matte family;
  * converts the surviving magenta edge spill to the project's required black rim;
  * applies luminance-preserving OUTER/INNER palette ramps;
  * normalizes every hull to a fixed 256x256 pivot without inventing idle frames; and
  * writes a contact sheet plus machine-readable hardpoint metadata.
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "_BUILD_SOURCE" / "stage8_symbiote_generated" / "fleet_sources"
OUT = ROOT / "assets" / "game" / "stage8_symbiote_fleet"
PROOF = ROOT / "docs" / "proofs" / "stage8_symbiote_fleet"


UNITS = {
    "armored_gunship": {
        "source": "Armored_Gunship_Front_Source.png",
        "outer": None,
        "inner": None,
        "label": "ORIGINAL STEEL / RUBY",
        "mounts": [[-.34, .27], [.34, .27], [0, .43]],
    },
    "needle_interceptor": {
        "source": "Needle_Interceptor_Front_Source.png",
        "outer": [(5, 6, 13), (24, 20, 53), (65, 48, 112), (127, 105, 174), (212, 197, 235)],
        "inner": [(2, 18, 29), (0, 70, 96), (0, 172, 209), (73, 244, 255), (228, 255, 255)],
        "label": "OBSIDIAN VIOLET / CYAN",
        "mounts": [[-.25, .22], [.25, .22], [0, .44]],
    },
    "scout_drone": {
        "source": "Scout_Drone_Front_Source.png",
        "outer": [(3, 9, 17), (15, 36, 70), (34, 78, 139), (80, 133, 197), (176, 219, 255)],
        "inner": [(7, 22, 4), (35, 79, 9), (84, 155, 20), (163, 224, 47), (239, 255, 170)],
        "label": "ROYAL BLUE / ACID GREEN",
        "mounts": [[-.31, .25], [.31, .25], [0, .34]],
    },
    "solar_corvette": {
        "source": "Solar_Corvette_Front_Source.png",
        "outer": [(14, 9, 3), (58, 37, 9), (113, 75, 18), (178, 135, 49), (247, 225, 149)],
        "inner": [(10, 6, 27), (48, 20, 94), (116, 49, 170), (190, 110, 235), (255, 224, 255)],
        "label": "BURNISHED GOLD / VIOLET",
        "mounts": [[-.40, .20], [.40, .20], [0, .42]],
    },
    "spread_wing_fighter": {
        "source": "Spread_Wing_Fighter_Front_Source.png",
        "outer": [(13, 3, 6), (59, 10, 19), (116, 22, 31), (181, 56, 62), (247, 164, 151)],
        "inner": [(2, 12, 33), (7, 47, 103), (12, 112, 201), (63, 190, 255), (210, 247, 255)],
        "label": "CRIMSON ARMOR / COBALT",
        "mounts": [[-.25, .23], [.25, .23], [0, .39]],
    },
    "stealth_crescent": {
        "source": "Stealth_Crescent_Front_Source.png",
        "outer": [(2, 10, 11), (8, 42, 44), (15, 83, 83), (49, 137, 132), (163, 225, 210)],
        "inner": [(17, 3, 27), (57, 11, 91), (116, 23, 176), (190, 80, 244), (255, 216, 255)],
        "label": "DARK TEAL / ULTRAVIOLET",
        "mounts": [[-.18, .23], [.18, .23], [0, .35]],
    },
}


def is_key(px: np.ndarray) -> np.ndarray:
    r, g, b = px[..., 0], px[..., 1], px[..., 2]
    return (r > 175) & (b > 175) & (g < 145) & (np.abs(r.astype(np.int16) - b.astype(np.int16)) < 105)


def connected_matte(candidate: np.ndarray) -> np.ndarray:
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
    return seen.astype(bool)


def edge_band(alpha: np.ndarray, passes: int = 5) -> np.ndarray:
    opaque = alpha > 0
    band = np.zeros_like(opaque)
    frontier = ~opaque
    for _ in range(passes):
        near = np.zeros_like(opaque)
        near[1:] |= frontier[:-1]
        near[:-1] |= frontier[1:]
        near[:, 1:] |= frontier[:, :-1]
        near[:, :-1] |= frontier[:, 1:]
        new = near & opaque & ~band
        band |= new
        frontier |= new
    return band


def clean(path: Path) -> Image.Image:
    src = np.asarray(Image.open(path).convert("RGBA"), dtype=np.uint8).copy()
    matte = connected_matte(is_key(src))
    src[matte, 3] = 0
    band = edge_band(src[..., 3], 6)
    r, g, b = src[..., 0], src[..., 1], src[..., 2]
    spill = band & (r > g * 1.35) & (b > g * 1.35) & (np.minimum(r, b) > 72)
    lum = (r.astype(np.uint16) * 54 + g.astype(np.uint16) * 183 + b.astype(np.uint16) * 19) // 256
    ink = np.clip(lum // 5, 3, 26).astype(np.uint8)
    for c in range(3): src[..., c][spill] = ink[spill]
    return Image.fromarray(src, "RGBA")


def sample_ramp(ramp: list[tuple[int, int, int]], value: np.ndarray) -> np.ndarray:
    pos = np.clip(value.astype(np.float32) / 255.0 * (len(ramp) - 1), 0, len(ramp) - 1)
    lo = np.floor(pos).astype(np.int16)
    hi = np.minimum(lo + 1, len(ramp) - 1)
    t = (pos - lo)[..., None]
    pal = np.asarray(ramp, dtype=np.float32)
    return np.clip(pal[lo] * (1 - t) + pal[hi] * t, 0, 255).astype(np.uint8)


def palette_swap(image: Image.Image, outer, inner) -> Image.Image:
    if outer is None:
        return image.copy()
    a = np.asarray(image, dtype=np.uint8).copy()
    rgb = a[..., :3]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    lum = np.clip((r.astype(np.uint16) * 54 + g.astype(np.uint16) * 183 + b.astype(np.uint16) * 19) // 256, 0, 255).astype(np.uint8)
    opaque = a[..., 3] > 0
    energy = opaque & (r > 66) & (r.astype(np.int16) > g.astype(np.int16) * 1.24) & (r.astype(np.int16) > b.astype(np.int16) * 1.16)
    body = opaque & ~energy & (lum > 12)
    outer_rgb = sample_ramp(outer, lum)
    inner_rgb = sample_ramp(inner, lum)
    rgb[body] = outer_rgb[body]
    rgb[energy] = inner_rgb[energy]
    return Image.fromarray(a, "RGBA")


def normalize(image: Image.Image, side: int = 256, fill: int = 220) -> tuple[Image.Image, list[int]]:
    alpha = np.asarray(image.getchannel("A"))
    ys, xs = np.where(alpha > 0)
    box = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    crop = image.crop(tuple(box))
    scale = min(fill / crop.width, fill / crop.height)
    size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
    crop = crop.resize(size, Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", (side, side))
    x = (side - size[0]) // 2
    y = (side - size[1]) // 2
    canvas.alpha_composite(crop, (x, y))
    return canvas, [x, y, x + size[0], y + size[1]]


def make_contact(frames: dict[str, Image.Image]) -> None:
    board = Image.new("RGB", (3 * 304, 2 * 336), (8, 9, 15))
    draw = ImageDraw.Draw(board)
    font = ImageFont.load_default()
    for i, (slug, frame) in enumerate(frames.items()):
        x = (i % 3) * 304 + 24
        y = (i // 3) * 336 + 18
        # neutral checkerboard proves transparency without hiding the dark rim
        tile = Image.new("RGB", (256, 256), (28, 31, 40))
        td = ImageDraw.Draw(tile)
        for yy in range(0, 256, 16):
            for xx in range(0, 256, 16):
                if (xx // 16 + yy // 16) & 1: td.rectangle((xx, yy, xx + 15, yy + 15), fill=(39, 43, 54))
        tile.paste(frame, (0, 0), frame)
        board.paste(tile, (x, y))
        draw.text((x, y + 265), slug.replace("_", " ").upper(), fill=(245, 245, 250), font=font)
        draw.text((x, y + 280), UNITS[slug]["label"], fill=(255, 102, 82), font=font)
    PROOF.mkdir(parents=True, exist_ok=True)
    board.save(PROOF / "stage8_new_fleet_contact.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    built: dict[str, Image.Image] = {}
    report = {"canvas": [256, 256], "anchor": [0.5, 0.5], "units": {}}
    for slug, spec in UNITS.items():
        src = SOURCE / spec["source"]
        if not src.exists():
            raise FileNotFoundError(src)
        cleaned = clean(src)
        swapped = palette_swap(cleaned, spec["outer"], spec["inner"])
        frame, bounds = normalize(swapped)
        unit_dir = OUT / slug
        unit_dir.mkdir(parents=True, exist_ok=True)
        frame.save(unit_dir / "idle.png")
        built[slug] = frame
        report["units"][slug] = {
            "source": str(src), "palette": spec["label"], "bounds": bounds,
            "muzzles": spec["mounts"], "idle_frames": 1,
        }
    (OUT / "fleet.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    make_contact(built)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
