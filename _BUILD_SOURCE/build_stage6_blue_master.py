"""Build Stage 6's single continuous blue-sky master and five 1000px sections.

The approved launch plate is the source of truth.  Alternating vertically mirrored
copies meet on identical edge rows, eliminating a visible tile seam without
inventing another sky.  Clouds are composited into the master once, so they scroll
with the terrain and never animate or drift independently.
"""

from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SKY = ROOT / "docs" / "proofs" / "stage6_sky_plate.png"
CLOUD = ROOT / "assets" / "game" / "bg6" / "bg6_cloud_day_0.png"
OUT = ROOT / "assets" / "game" / "stage6_blue"
MASTER = ROOT / "assets" / "game" / "stage6_blue_master.png"
PROOF = ROOT / "docs" / "proofs" / "stage6_blue_master_contact.png"

WIDTH = 680
HEIGHT = 5000
SECTION_H = 1000


def clean_cloud(image: Image.Image) -> Image.Image:
    """Remove the magenta key/outline without soft alpha halos."""
    rgba = image.convert("RGBA")
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            if a and r > 105 and b > 105 and g < min(r, b) * 0.72:
                px[x, y] = (r, g, b, 0)
    return rgba


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PROOF.parent.mkdir(parents=True, exist_ok=True)

    src = Image.open(SKY).convert("RGB")
    tile_h = round(src.height * WIDTH / src.width)
    tile = src.resize((WIDTH, tile_h), Image.Resampling.NEAREST)
    master = Image.new("RGB", (WIDTH, HEIGHT), "#071a55")
    y = 0
    flip = False
    while y < HEIGHT:
        plate = tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM) if flip else tile
        master.paste(plate, (0, y))
        y += tile_h
        flip = not flip

    cloud = clean_cloud(Image.open(CLOUD))
    # (centre x, top y, width, mirrored). These are scenery positions in the
    # 5000px world, not animation frames; some deliberately enter from an edge.
    placements = [
        (105, 250, 300, False), (555, 690, 390, True),
        (330, 1190, 450, False), (35, 1660, 350, True),
        (590, 2125, 330, False), (285, 2590, 400, True),
        (70, 3100, 310, False), (520, 3550, 430, True),
        (350, 4110, 380, False), (100, 4630, 410, True),
    ]
    for cx, top, w, mirrored in placements:
        h = round(cloud.height * w / cloud.width)
        still = cloud.resize((w, h), Image.Resampling.NEAREST)
        if mirrored:
            still = still.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        master.paste(still, (round(cx - w / 2), top), still)

    master.save(MASTER, optimize=True)
    for i in range(HEIGHT // SECTION_H):
        part = master.crop((0, i * SECTION_H, WIDTH, (i + 1) * SECTION_H))
        part.save(OUT / f"stage6_blue_{i + 1:02d}.png", optimize=True)

    # Compact QA contact sheet: all five sections side by side at 20% scale.
    proof = Image.new("RGB", (WIDTH, SECTION_H), "black")
    for i in range(5):
        part = master.crop((0, i * SECTION_H, WIDTH, (i + 1) * SECTION_H))
        part = part.resize((WIDTH // 5, SECTION_H // 5), Image.Resampling.NEAREST)
        proof.paste(part, (i * (WIDTH // 5), 0))
    proof.save(PROOF, optimize=True)

    print(MASTER)
    print(f"sections={len(list(OUT.glob('stage6_blue_*.png')))} size={WIDTH}x{SECTION_H}")
    print(PROOF)


if __name__ == "__main__":
    main()
