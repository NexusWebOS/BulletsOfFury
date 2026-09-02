"""Normalize generated combat atlases into real transparent PNG assets.

The image service previews alpha over a pale checkerboard and may flatten that
preview into RGB.  This removes only the connected pale-neutral matte while
retaining bright weapon cores that are enclosed by colored/dark sprite pixels.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = ROOT / "assets" / "game" / "combat_final"


def is_matte(rgb: tuple[int, int, int]) -> bool:
    lo = min(rgb)
    hi = max(rgb)
    return lo >= 224 and hi - lo <= 18


def normalize(path: Path) -> None:
    rgba_src = Image.open(path).convert("RGBA")
    existing_alpha = rgba_src.getchannel("A")
    if existing_alpha.getextrema()[0] == 0:
        # A second pass on an already-normalized sheet: walk outward from every transparent
        # pixel through pale neutral preview-matte. This removes checker remnants trapped in
        # enclosed gaps between a hull and its legs without touching bright cores enclosed by
        # saturated energy pixels.
        width, height = rgba_src.size
        pixels = rgba_src.load()
        seen = bytearray(width * height)
        queue: deque[tuple[int, int]] = deque()
        for y in range(height):
            for x in range(width):
                if pixels[x, y][3] == 0:
                    seen[y * width + x] = 1
                    queue.append((x, y))
        while queue:
            x, y = queue.popleft()
            for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if xx < 0 or yy < 0 or xx >= width or yy >= height:
                    continue
                offset = yy * width + xx
                if seen[offset]:
                    continue
                px = pixels[xx, yy]
                if px[3] == 0 or is_matte(px[:3]):
                    seen[offset] = 1
                    if px[3] != 0:
                        pixels[xx, yy] = (0, 0, 0, 0)
                    queue.append((xx, yy))
        rgba_src.save(path, optimize=True)
        transparent = sum(1 for value in rgba_src.getchannel("A").getdata() if value == 0)
        print(f"{path.name}: {width}x{height}, transparent={transparent / (width * height):.1%} (alpha cleanup)")
        return

    src = rgba_src.convert("RGB")
    width, height = src.size
    pixels = src.load()
    outside = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def enqueue(x: int, y: int) -> None:
        offset = y * width + x
        if not outside[offset] and is_matte(pixels[x, y]):
            outside[offset] = 1
            queue.append((x, y))

    for x in range(width):
        enqueue(x, 0)
        enqueue(x, height - 1)
    for y in range(height):
        enqueue(0, y)
        enqueue(width - 1, y)

    while queue:
        x, y = queue.popleft()
        if x:
            enqueue(x - 1, y)
        if x + 1 < width:
            enqueue(x + 1, y)
        if y:
            enqueue(x, y - 1)
        if y + 1 < height:
            enqueue(x, y + 1)

    rgba = Image.new("RGBA", src.size, (0, 0, 0, 0))
    out = rgba.load()
    for y in range(height):
        row = y * width
        for x in range(width):
            rgb = pixels[x, y]
            if outside[row + x]:
                continue
            # Clear enclosed checker cells (shield interiors and circular holes)
            # unless a colored/dark sprite edge is within two pixels.
            if is_matte(rgb):
                keep = False
                for yy in range(max(0, y - 2), min(height, y + 3)):
                    for xx in range(max(0, x - 2), min(width, x + 3)):
                        near = pixels[xx, yy]
                        if min(near) < 205 or max(near) - min(near) > 28:
                            keep = True
                            break
                    if keep:
                        break
                # Generated weapon cores are deliberately white and can match
                # the preview matte exactly. Retain compact white cores when
                # they are surrounded by a dense ring of saturated energy.
                if not keep and min(rgb) >= 250:
                    saturated = 0
                    for yy in range(max(0, y - 12), min(height, y + 13), 2):
                        for xx in range(max(0, x - 12), min(width, x + 13), 2):
                            near = pixels[xx, yy]
                            if max(near) - min(near) > 42 and max(near) > 150:
                                saturated += 1
                    keep = saturated >= 12
                if not keep:
                    continue
            out[x, y] = (*rgb, 255)

    rgba.save(path, optimize=True)
    alpha = rgba.getchannel("A")
    transparent = sum(1 for value in alpha.getdata() if value == 0)
    print(f"{path.name}: {width}x{height}, transparent={transparent / (width * height):.1%}")


def main() -> None:
    for path in sorted(ASSET_DIR.glob("*.png")):
        normalize(path)


if __name__ == "__main__":
    main()
