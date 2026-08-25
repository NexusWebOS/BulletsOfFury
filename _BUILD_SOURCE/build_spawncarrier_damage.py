"""Build the complete Spawn Carrier and registration-locked damage plates.

The original intact plate is missing its starboard wing.  The source master is the
regenerated, complete two-wing carrier.  It is normalized onto the game's 256px
registration canvas before damage is added.  The shipped damage alternates fused
smoke/explosion FX into the hull; these plates add structural damage only.
"""
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "_ART_SOURCES" / "SpawnCarrier" / "nsb_spawncarrier_complete_master.png"
OUT_INTACT = ROOT / "assets" / "game" / "nsb_spawncarrier_intact_v2.png"
OUT_DAMAGED = ROOT / "assets" / "game" / "nsb_spawncarrier_damaged_v2.png"
OUT_CRITICAL = ROOT / "assets" / "game" / "nsb_spawncarrier_critical_v2.png"


def normalized_master() -> Image.Image:
    """Remove generator-edge noise and fit the real silhouette with safe padding."""
    src = Image.open(SRC).convert("RGBA")
    alpha = src.getchannel("A")
    solid = alpha.point(lambda a: 255 if a >= 8 else 0)
    bbox = solid.getbbox()
    if not bbox:
        raise SystemExit("generated source has no visible alpha")
    pad = 4
    bbox = (
        max(0, bbox[0] - pad), max(0, bbox[1] - pad),
        min(src.width, bbox[2] + pad), min(src.height, bbox[3] + pad),
    )
    ship = src.crop(bbox)
    # 12px minimum breathing room prevents either wing or forward claw being cut.
    scale = min(232 / ship.width, 232 / ship.height)
    size = (max(1, round(ship.width * scale)), max(1, round(ship.height * scale)))
    ship = ship.resize(size, Image.Resampling.LANCZOS).filter(
        ImageFilter.UnsharpMask(radius=0.7, percent=105, threshold=2)
    )
    # Clear only near-invisible resampling noise; retain the antialiased silhouette.
    a = ship.getchannel("A").point(lambda value: 0 if value < 4 else value)
    ship.putalpha(a)
    out = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    out.alpha_composite(ship, ((256 - ship.width) // 2, (256 - ship.height) // 2))
    return out


def clipped_overlay(base: Image.Image, painter) -> Image.Image:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    painter(ImageDraw.Draw(layer))
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), base.getchannel("A")))
    return Image.alpha_composite(base, layer)


def scars(base: Image.Image, critical: bool) -> Image.Image:
    out = base.copy()

    # Localized scorches: opaque enough to read at game scale, never a smoke cloud.
    patches = [
        (73, 91, 104, 123, 72),
        (151, 122, 181, 153, 82),
        (99, 172, 126, 203, 68),
    ]
    if critical:
        patches += [
            (126, 52, 160, 89, 104),
            (53, 165, 86, 205, 112),
            (166, 182, 201, 221, 116),
        ]

    def paint_scars(d: ImageDraw.ImageDraw) -> None:
        for x0, y0, x1, y1, a in patches:
            d.ellipse((x0, y0, x1, y1), fill=(3, 3, 8, a))

        # Deep cracked plates. Black under-line gives every fracture a hard arcade edge;
        # the one-pixel violet interior reads as exposed powered conduit.
        cracks = [
            [(80, 90), (88, 99), (83, 109), (95, 119), (90, 131)],
            [(166, 124), (156, 133), (163, 145), (151, 158)],
            [(111, 177), (119, 185), (113, 195), (125, 205)],
        ]
        if critical:
            cracks += [
                [(139, 55), (132, 66), (143, 76), (135, 89), (148, 101)],
                [(65, 168), (75, 176), (68, 188), (80, 198), (75, 210)],
                [(183, 185), (173, 194), (181, 203), (170, 214), (177, 225)],
                [(121, 111), (132, 120), (124, 132), (137, 144)],
            ]
        for pts in cracks:
            d.line(pts, fill=(2, 2, 5, 245), width=3, joint="curve")
            d.line(pts, fill=(173, 52, 231, 220), width=1, joint="curve")

        # Recessed ruptured panels and exposed conduits, all clipped inside the hull.
        panels = [
            [(88, 112), (101, 108), (105, 120), (94, 130), (84, 124)],
            [(151, 151), (169, 149), (172, 163), (158, 172), (147, 165)],
        ]
        if critical:
            panels += [
                [(123, 68), (144, 63), (153, 77), (143, 91), (122, 87)],
                [(59, 181), (78, 173), (88, 188), (80, 205), (62, 207)],
                [(171, 194), (195, 188), (202, 205), (188, 221), (169, 214)],
            ]
        for poly in panels:
            d.polygon(poly, fill=(5, 4, 10, 218), outline=(38, 28, 46, 255))
            xs = [p[0] for p in poly]
            ys = [p[1] for p in poly]
            cx = (min(xs) + max(xs)) // 2
            cy = (min(ys) + max(ys)) // 2
            # Two broken, non-parallel conductor fragments.  Avoid full-width neon bars:
            # those read as pasted UI marks instead of torn internal machinery.
            d.line([(cx - 7, cy - 3), (cx - 2, cy), (cx + 3, cy - 4)],
                   fill=(191, 65, 239, 220), width=1)
            d.line([(cx - 4, cy + 4), (cx + 1, cy + 1), (cx + 5, cy + 4)],
                   fill=(76, 25, 116, 220), width=1)

        # Small hard-edged impact chips; no particles or atmospheric FX.
        chips = [(93, 84), (172, 116), (119, 158), (80, 139)]
        if critical:
            chips += [(145, 105), (63, 194), (193, 205), (137, 47), (108, 215)]
        for x, y in chips:
            d.rectangle((x - 2, y - 1, x + 2, y + 1), fill=(0, 0, 0, 245))
            d.point((x, y), fill=(235, 104, 255, 255))

    out = clipped_overlay(out, paint_scars)
    return out


def main() -> None:
    base = normalized_master()
    base.save(OUT_INTACT, optimize=True)
    scars(base, critical=False).save(OUT_DAMAGED, optimize=True)
    scars(base, critical=True).save(OUT_CRITICAL, optimize=True)
    print(OUT_INTACT)
    print(OUT_DAMAGED)
    print(OUT_CRITICAL)


if __name__ == "__main__":
    main()
