"""Compose Overdrive roster faces with the existing 0919 pilot avatar frame.

This mirrors rebuild_pilot_avatars_0919.py's frame recolor and 202x212
portrait placement without touching the current nine pilots.
"""

from colorsys import hsv_to_rgb, rgb_to_hsv
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
EXPANSION = Path(__file__).resolve().parents[1]
FRAME_PATH = ROOT / "assets/game/pilot_avatars/avatar_frame_template_0919.png"
SOURCE_DIR = EXPANSION / "concept"
OUTPUT_DIR = EXPANSION / "pilot_avatars"
PILOTS = {"hotwire": 0.52, "phoenix": 0.06}


def recolor_frame(frame: Image.Image, hue: float) -> Image.Image:
    pixels = []
    for r, g, b, a in frame.get_flattened_data():
        h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)
        if a and 0.48 < h < 0.71 and s > 0.22 and b > r + 10:
            nr, ng, nb = hsv_to_rgb(hue, s, v)
            r, g, b = round(nr * 255), round(ng * 255), round(nb * 255)
        pixels.append((r, g, b, a))
    result = Image.new("RGBA", frame.size)
    result.putdata(pixels)
    return result


def main() -> None:
    frame = Image.open(FRAME_PATH).convert("RGBA")
    assert frame.size == (256, 256)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for pilot, hue in PILOTS.items():
        face = Image.open(SOURCE_DIR / f"{pilot}_avatar_inner.png").convert("RGBA")
        # The inner art is deliberately borderless. The same nearest-neighbor
        # placement as the existing avatar builder keeps the family's scale.
        face = face.resize((202, 212), Image.Resampling.NEAREST)
        panel = Image.new("RGBA", (256, 256), (7, 11, 19, 255))
        panel.alpha_composite(face, (27, 27))
        panel.alpha_composite(recolor_frame(frame, hue))
        panel.save(OUTPUT_DIR / f"{pilot}-idle.png")


if __name__ == "__main__":
    main()
