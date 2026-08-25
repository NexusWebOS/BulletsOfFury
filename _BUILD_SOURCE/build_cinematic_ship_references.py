from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "game" / "atlas" / "nca_4.png"
MANIFEST = ROOT / "assets" / "manifest.js"
OUT = ROOT / "_BUILD_SOURCE" / "cinematic_ship_inputs"
PILOTS = ("axel", "freezer", "falva", "lizzie", "yuri", "maverick", "juggernaut", "decker", "cole")
VARIANTS = ("", "_nf", "_l", "_r", "_pv2", "_br0")
SLOT = (400, 400)
SHEET = (1200, 800)


def read_rect(key: str, source: str) -> list[int]:
    match = re.search(rf'"{re.escape(key)}":\[([^\]]+)\]', source)
    if not match:
        raise KeyError(key)
    return json.loads("[" + match.group(1) + "]")


def restore_frame(atlas: Image.Image, rect: list[int]) -> Image.Image:
    sx, sy, width, height, dx, dy, canvas_w, canvas_h = rect
    frame = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    frame.alpha_composite(atlas.crop((sx, sy, sx + width, sy + height)), (dx, dy))
    bbox = frame.getbbox()
    if not bbox:
        raise ValueError(f"empty frame: {rect}")
    return frame.crop(bbox)


def fit(frame: Image.Image, bounds: tuple[int, int]) -> Image.Image:
    copy = frame.copy()
    copy.thumbnail(bounds, Image.Resampling.NEAREST)
    return copy


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source = MANIFEST.read_text(encoding="utf-8")
    atlas = Image.open(SOURCE).convert("RGBA")
    previews: list[tuple[str, Path]] = []

    for pilot in PILOTS:
        canvas = Image.new("RGBA", SHEET, (0, 0, 0, 0))
        for index, suffix in enumerate(VARIANTS):
            frame = restore_frame(atlas, read_rect(f"ship_{pilot}{suffix}", source))
            frame = fit(frame, (330, 330))
            col, row = index % 3, index // 3
            x = col * SLOT[0] + (SLOT[0] - frame.width) // 2
            y = row * SLOT[1] + (SLOT[1] - frame.height) // 2
            canvas.alpha_composite(frame, (x, y))
        path = OUT / f"{pilot}_canonical_ship_reference_rgba.png"
        canvas.save(path)
        previews.append((pilot, path))

    font = ImageFont.truetype(r"C:\Windows\Fonts\bahnschrift.ttf", 20)
    overview = Image.new("RGB", (1200, 930), (8, 10, 15))
    draw = ImageDraw.Draw(overview)
    for index, (pilot, path) in enumerate(previews):
        with Image.open(path) as image:
            thumb = image.convert("RGBA").resize((400, 267), Image.Resampling.LANCZOS)
        x = index % 3 * 400
        y = index // 3 * 310
        overview.paste(thumb, (x, y), thumb)
        draw.text((x + 10, y + 276), pilot.upper(), font=font, fill=(118, 220, 255))
    overview.save(OUT / "canonical_ship_references_contact.jpg", quality=94, optimize=True)
    print(f"PASS: built {len(previews)} canonical ship reference canvases from {SOURCE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
