#!/usr/bin/env python3
"""Extract the shipped Stage-2 enemy seed frames from the packed XART atlases."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "manifest.js"
OUT = ROOT / "_BUILD_SOURCE" / "stage2_enemy_redesign" / "seeds"
ARTS = ["ash", "skim", "eye", "disc", "lance", "cruc", "carrier", "miner", "maw", "crawl", "pod", "golem"]


def cells() -> dict[str, tuple[int, int, int, int, int]]:
    source = MANIFEST.read_text(encoding="utf-8")
    found: dict[str, tuple[int, int, int, int, int]] = {}
    for match in re.finditer(
        r'"(nvl_[a-z]+_[0-5])":\[(\d+),(\d+),(\d+),(\d+),(\d+)\]', source
    ):
        key = match.group(1)
        found[key] = tuple(int(match.group(i)) for i in range(2, 7))
    return found


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    packed = cells()
    seeds: list[tuple[str, Image.Image]] = []
    atlases: dict[int, Image.Image] = {}
    for art in ARTS:
        key = f"nvl_{art}_0"
        atlas_no, x, y, w, h = packed[key]
        atlas = atlases.setdefault(
            atlas_no, Image.open(ROOT / "assets" / "game" / "atlas" / f"nca_{atlas_no}.png").convert("RGBA")
        )
        crop = atlas.crop((x, y, x + w, y + h))
        path = OUT / f"{art}_seed.png"
        crop.save(path)
        seeds.append((art, crop))

    slot = 288
    sheet = Image.new("RGBA", (slot * 4, slot * 3), (8, 13, 23, 255))
    draw = ImageDraw.Draw(sheet)
    for index, (name, sprite) in enumerate(seeds):
        col, row = index % 4, index // 4
        thumb = sprite.copy()
        thumb.thumbnail((240, 230), Image.Resampling.NEAREST)
        px = col * slot + (slot - thumb.width) // 2
        py = row * slot + 18 + (230 - thumb.height) // 2
        sheet.alpha_composite(thumb, (px, py))
        draw.text((col * slot + 10, row * slot + 258), name.upper(), fill=(255, 170, 55, 255))
    sheet.save(OUT.parent / "stage2_enemy_seed_contact.png")


if __name__ == "__main__":
    main()
