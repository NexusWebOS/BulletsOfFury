"""Palette-swap the approved Furnace laser plate for the Furious Frost Cruiser.

The source pixels and alpha are retained. Only RGB is mapped through a dark-blue
to icy-white ramp; no sprite geometry is generated or mirrored.
"""
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/game/bosses/furnace/fzt_fire_laser_0920.png"
TARGET = ROOT / "assets/game/bosses/frost/frost_furious_beam_0920.png"


def main() -> None:
    source = np.asarray(Image.open(SOURCE).convert("RGBA"), dtype=np.uint8)
    rgb = source[..., :3].astype(np.float32)
    red, green, blue = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    # Green tracks the source's red -> orange -> yellow heat bands, while blue
    # distinguishes the bright core. Red retains variation in the dark rim.
    heat = np.clip(0.62 * red + 0.92 * green + 0.34 * blue, 0, 430)
    stops = np.array([45, 90, 130, 185, 245, 310, 365, 430], dtype=np.float32)
    palette = np.array([
        (4, 9, 30), (8, 19, 59), (15, 35, 107), (22, 59, 167),
        (29, 102, 213), (58, 163, 240), (112, 193, 241), (187, 228, 253),
    ], dtype=np.float32)
    mapped = np.stack([np.interp(heat, stops, palette[:, c]) for c in range(3)], axis=-1)
    # Do not flatten source value variation within each band.
    grain = (np.clip((red - 170) / 210, -0.16, 0.16)
             * np.clip((430 - heat) / 150, 0, 1))[..., None]
    mapped = np.clip(mapped * (1 + grain), 0, 255).astype(np.uint8)
    out = np.concatenate((mapped, source[..., 3:4]), axis=-1)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(out, "RGBA").save(TARGET, optimize=True)
    print(f"{TARGET.relative_to(ROOT)} {Image.open(TARGET).size}")


if __name__ == "__main__":
    main()
