"""Extract the organic boss FX family and author a purple Spawn Carrier set.

Outputs 18 loose PNGs: six projectile, six muzzle, six impact frames. Geometry,
timing and registration stay identical to the approved source family. A transparent
safety gutter is added because the atlas cells are content-tight and several authored
glow pixels touch their cell boundary; loose runtime FX must never look clipped.
"""
from __future__ import annotations

import colorsys
import math
import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "manifest.js"
OUT = ROOT / "assets" / "game" / "boss_fx_spawncarrier"


def cell_for(text: str, key: str) -> tuple[int, int, int, int, int]:
    m = re.search(r'"' + re.escape(key) + r'":\[(\d+),(\d+),(\d+),(\d+),(\d+)\]', text)
    if not m:
        raise KeyError(key)
    return tuple(map(int, m.groups()))


def purple_pixel(px: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    r, g, b, a = px
    if a == 0:
        return px
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    # Organic family accent runs yellow -> acid green. Shift only saturated warm/green
    # energy; neutral metal, black outlines and white-hot cores remain authored.
    if s > 0.22 and 0.08 <= h <= 0.48:
        # yellow becomes hot magenta, green becomes electric violet.
        t = (h - 0.08) / 0.40
        nh = 0.88 - 0.13 * t
        ns = min(1.0, s * 1.08)
        nr, ng, nb = colorsys.hsv_to_rgb(nh, ns, v)
        return (round(nr * 255), round(ng * 255), round(nb * 255), a)
    return px


def main() -> None:
    text = MANIFEST.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    atlases: dict[int, Image.Image] = {}
    try:
        for role in ("p", "m", "i"):
            for frame in range(6):
                src_key = f"bfx_toxic_{role}_{frame}"
                atlas, x, y, w, h = cell_for(text, src_key)
                if atlas not in atlases:
                    atlases[atlas] = Image.open(ROOT / "assets" / "game" / "atlas" / f"nca_{atlas}.png").convert("RGBA")
                im = atlases[atlas].crop((x, y, x + w, y + h))
                im.putdata([purple_pixel(px) for px in im.getdata()])
                pad = max(8, math.ceil(max(w, h) * 0.06))
                loose = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
                loose.alpha_composite(im, (pad, pad))
                loose.save(OUT / f"bfx_spawn_{role}_{frame}.png", optimize=True)
    finally:
        for im in atlases.values():
            im.close()
    print(f"wrote 18 frames to {OUT}")


if __name__ == "__main__":
    main()
