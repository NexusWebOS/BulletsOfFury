"""Build the Furious Razorback's authored neon-red-panel sprite family.

Only green paint is changed. Neutral steel, black outlines, highlights, damage,
and ordnance luminance remain byte-for-byte where the source pixel is not green.
"""
from pathlib import Path
import colorsys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets/game/bosses/razorback"
DST = ROOT / "assets/game/bosses/razorback_furious"


def swap_green_to_neon_red(src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGBA")
    out = []
    for r, g, b, a in im.getdata():
        if not a:
            out.append((r, g, b, a))
            continue
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        # Authored green paint and glow only. Warm ordnance and neutral steel stay intact.
        if 0.18 <= h <= 0.47 and s >= 0.23 and v >= 0.055:
            nr, ng, nb = colorsys.hsv_to_rgb(0.985, max(0.88, s), min(1.0, v * 1.08))
            out.append((round(nr * 255), round(ng * 255), round(nb * 255), a))
        else:
            out.append((r, g, b, a))
    im.putdata(out)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, optimize=True)


def main() -> None:
    for src in sorted(SRC.glob("rzb_*.png")):
        swap_green_to_neon_red(src, DST / src.name.replace("rzb_", "rzbf_", 1))
    print(f"wrote {len(list(DST.glob('rzbf_*.png')))} Furious Razorback plates to {DST}")


if __name__ == "__main__":
    main()
