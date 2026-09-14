#!/usr/bin/env python3
"""Extract the approved non-drone Stage-3 hulls from the packed XART atlas."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "manifest.js"
OUT = ROOT / "_BUILD_SOURCE" / "stage3_enemy_redesign" / "seeds"
ARTS = {
    "mine": "nef_s3_shard_mine",
    "interceptor": "nef_s3_elite_ice_interceptor",
    "sled": "nef_s3_aa_sled",
    "snowmobile": "nef_s3_snowmobile_gunner",
    "crawler": "nef_s3_ice_crawler",
    "tank": "nef_s3_snow_tank",
    "barge": "nef_s3_cryo_barge",
    "artillery": "nef_s3_tracked_frost_artillery",
}


def cells() -> dict[str, tuple[int, int, int, int, int]]:
    source = MANIFEST.read_text(encoding="utf-8")
    found: dict[str, tuple[int, int, int, int, int]] = {}
    for match in re.finditer(
        r'"(nef_s3_[a-z0-9_]+_intact_idle)":\[(\d+),(\d+),(\d+),(\d+),(\d+)\]',
        source,
    ):
        found[match.group(1)] = tuple(int(match.group(i)) for i in range(2, 7))
    return found


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    packed = cells()
    atlas_cache: dict[int, Image.Image] = {}
    seeds: list[tuple[str, Image.Image]] = []
    for name, base in ARTS.items():
        key = f"{base}_intact_idle"
        atlas_no, x, y, w, h = packed[key]
        atlas = atlas_cache.setdefault(
            atlas_no,
            Image.open(ROOT / "assets" / "game" / "atlas" / f"nca_{atlas_no}.png").convert("RGBA"),
        )
        crop = atlas.crop((x, y, x + w, y + h))
        crop.save(OUT / f"{name}_seed.png")
        seeds.append((name, crop))

    slot_w, slot_h = 300, 282
    sheet = Image.new("RGBA", (slot_w * 4, slot_h * 2), (7, 15, 28, 255))
    draw = ImageDraw.Draw(sheet)
    for index, (name, sprite) in enumerate(seeds):
        col, row = index % 4, index // 4
        thumb = sprite.copy()
        thumb.thumbnail((260, 228), Image.Resampling.NEAREST)
        px = col * slot_w + (slot_w - thumb.width) // 2
        py = row * slot_h + 12 + (228 - thumb.height) // 2
        sheet.alpha_composite(thumb, (px, py))
        draw.text((col * slot_w + 12, row * slot_h + 250), name.upper(), fill=(146, 226, 255, 255))
    sheet.save(OUT.parent / "stage3_enemy_seed_contact.png")


if __name__ == "__main__":
    main()
