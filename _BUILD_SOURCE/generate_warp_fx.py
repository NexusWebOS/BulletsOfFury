"""Build the deterministic Neo-Geo warp-distortion reel used by Stages 5 and 9.

The reel stays on one 512x512 transparent canvas with a fixed centre/pivot.  It is
generated rather than hand-resized so every frame has identical registration and
the game can rotate/scale it without shimmer.
"""
from __future__ import annotations

from pathlib import Path
from math import cos, pi, sin
import random

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "game" / "warp_fx"
PREVIEW = ROOT / "_BUILD_SOURCE" / "warp_fx_preview"
SIZE = 512
FRAMES = 16
PALETTE = ((55, 238, 255), (80, 126, 255), (153, 64, 255), (224, 102, 255))


def frame(index: int) -> Image.Image:
    random.seed(0xF00D + index)
    phase = index / FRAMES
    hi = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    bloom = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(hi)
    b = ImageDraw.Draw(bloom)
    cx = cy = SIZE // 2

    # Elliptical tunnel rings, broken into rotating arcs so the transparent playfield remains readable.
    for ring in range(12):
        travel = (ring / 12 + phase) % 1.0
        eased = travel * travel
        rx = 22 + eased * 238
        ry = 14 + eased * 178
        col = PALETTE[(ring + index // 3) % len(PALETTE)]
        alpha = int(40 + 150 * (1 - travel))
        width = 2 + (ring % 3)
        start = (index * 17 + ring * 37) % 360
        gap = 28 + (ring % 4) * 7
        box = (cx - rx, cy - ry, cx + rx, cy + ry)
        for arm in range(4):
            a0 = start + arm * 90 + gap / 2
            a1 = start + (arm + 1) * 90 - gap / 2
            d.arc(box, a0, a1, fill=(*col, alpha), width=width)
            b.arc(box, a0, a1, fill=(*col, max(12, alpha // 3)), width=width * 4)

    # Curved radial filaments create apparent lensing without white speed lines.
    for filament in range(24):
        a = filament * (2 * pi / 24) + phase * 2 * pi
        col = PALETTE[(filament + index) % len(PALETTE)]
        pts = []
        for step in range(9):
            r = 35 + step * 30
            bend = a + sin(phase * 2 * pi + step * .47 + filament) * .12 + step * .018
            pts.append((cx + cos(bend) * r, cy + sin(bend) * r * .73))
        d.line(pts, fill=(*col, 54 + filament % 4 * 18), width=1 + filament % 2)

    # Chunky pixel motes travel toward the viewer. They are square on purpose.
    for mote in range(54):
        a = random.random() * 2 * pi
        travel = (random.random() + phase * (1.2 + mote % 3 * .17)) % 1
        r = 26 + travel * 310
        x = int(cx + cos(a) * r)
        y = int(cy + sin(a) * r * .73)
        if 0 <= x < SIZE and 0 <= y < SIZE:
            z = 1 + int(travel * 3)
            col = PALETTE[mote % len(PALETTE)]
            d.rectangle((x - z, y - z, x + z, y + z), fill=(*col, int(70 + travel * 150)))

    # Dark transparent eye in the middle leaves the portal/ship readable.
    eye = Image.new("L", (SIZE, SIZE), 0)
    ed = ImageDraw.Draw(eye)
    ed.ellipse((cx - 62, cy - 42, cx + 62, cy + 42), fill=225)
    eye = eye.filter(ImageFilter.GaussianBlur(18))
    combined = Image.alpha_composite(bloom.filter(ImageFilter.GaussianBlur(7)), hi)
    alpha = combined.getchannel("A")
    alpha = Image.eval(Image.composite(Image.new("L", alpha.size, 0), alpha, eye), lambda v: v)
    # Composite() above gives zero in the eye and preserves the exterior via inverted mask logic below.
    exterior = Image.eval(eye, lambda v: 255 - v)
    alpha = Image.composite(combined.getchannel("A"), Image.new("L", alpha.size, 0), exterior)
    combined.putalpha(alpha)
    return combined


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PREVIEW.mkdir(parents=True, exist_ok=True)
    imgs = []
    for i in range(FRAMES):
        im = frame(i)
        path = OUT / f"warp_tunnel_{i:02d}.png"
        im.save(path, optimize=True)
        imgs.append(im)
    imgs[0].save(PREVIEW / "warp_tunnel_preview.gif", save_all=True,
                 append_images=imgs[1:], duration=58, loop=0, disposal=2)
    sheet = Image.new("RGBA", (SIZE * 4, SIZE * 4), (7, 5, 18, 255))
    for i, im in enumerate(imgs):
        sheet.alpha_composite(im, ((i % 4) * SIZE, (i // 4) * SIZE))
    sheet.save(PREVIEW / "warp_tunnel_contact_sheet.png", optimize=True)
    print(f"wrote {FRAMES} frames to {OUT}")


if __name__ == "__main__":
    main()
