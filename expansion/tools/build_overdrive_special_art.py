"""Package generated Overdrive special art as loose, consistently anchored PNGs.

The source masters stay unchanged in expansion/specials/source.
This builder does not touch the game atlas or runtime manifest.
"""

import json
from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parents[1] / "specials"
SOURCE = BASE / "source"
FRAMES = BASE / "frames"
UI = BASE / "ui"
PREVIEWS = BASE / "previews"

SHEETS = {
    "hotwire_whip": ("hotwire_whip_snap_sheet.png", 4, 2, (384, 384)),
    "hotwire_hit": ("hotwire_hit_spread_sheet.png", 3, 2, (128, 128)),
    "hotwire_chain": ("hotwire_chain_sheet.png", 4, 2, (256, 256)),
    "phoenix_retina": ("phoenix_retina_sheet.png", 4, 2, (128, 128)),
    "phoenix_mortar": ("phoenix_mortar_sheet.png", 3, 2, (128, 128)),
    "phoenix_volley": ("phoenix_volley_sheet.png", 4, 2, (256, 256)),
}

TIMING_MS = {
    # Wind up deliberately, then accelerate through release and contact.
    "hotwire_whip": [90, 110, 140, 55, 45, 45, 70, 110],
    "hotwire_hit": [40, 45, 50, 60, 70, 100],
    "hotwire_chain": [45, 50, 55, 55, 65, 65, 70, 90],
}

UI_ART = {
    "special_hotwire_box": ("special_hotwire_box_source.png", (360, 400)),
    "special_phoenix_box": ("special_phoenix_box_source.png", (360, 400)),
    "spicon_hotwire": ("special_hotwire_icon_source.png", (112, 112)),
    "spicon_phoenix": ("special_phoenix_icon_source.png", (112, 112)),
    "phoenix_charge_tether": ("phoenix_charge_tether.png", (64, 256)),
}


def clean_alpha(image: Image.Image) -> Image.Image:
    """Discard only near-invisible generation haze and transparent RGB fringes."""
    image = image.convert("RGBA")
    pixels = []
    for r, g, b, a in image.get_flattened_data():
        pixels.append((0, 0, 0, 0) if a < 16 else (r, g, b, a))
    result = Image.new("RGBA", image.size)
    result.putdata(pixels)
    return result


def alpha_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A").point(lambda a: 255 if a > 24 else 0)
    return alpha.getbbox() or (0, 0, image.width, image.height)


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    UI.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    manifest = {"format": "bof.overdrive.special-art.v1", "runtime_registered": False, "effects": {}, "ui": {}}

    for key, (filename, cols, rows, size) in SHEETS.items():
        source = Image.open(SOURCE / filename).convert("RGBA")
        files = []
        for row in range(rows):
            for col in range(cols):
                box = (
                    round(col * source.width / cols),
                    round(row * source.height / rows),
                    round((col + 1) * source.width / cols),
                    round((row + 1) * source.height / rows),
                )
                # Keep every cell's shared anchor while leaving a transparent
                # guard band, so effect pixels cannot meet the final frame edge.
                pad = 8 if min(size) >= 256 else 4
                inner = (size[0] - pad * 2, size[1] - pad * 2)
                cell = clean_alpha(source.crop(box)).resize(inner, Image.Resampling.LANCZOS)
                frame = Image.new("RGBA", size)
                frame.alpha_composite(cell, (pad, pad))
                frame = clean_alpha(frame)
                dest = FRAMES / f"{key}_{len(files):02d}.png"
                frame.save(dest)
                files.append(dest.relative_to(BASE).as_posix())
        effect = {"source": f"source/{filename}", "grid": [cols, rows], "size": list(size), "frames": files}
        if key in TIMING_MS:
            effect["frame_duration_ms"] = TIMING_MS[key]
            # Review-only animation on a dark game-like field. The PNG frames
            # remain the transparent assets intended for the eventual runtime.
            preview = PREVIEWS / f"{key}.gif"
            preview_frames = []
            for name in files:
                plate = Image.new("RGBA", size, (6, 10, 18, 255))
                plate.alpha_composite(Image.open(BASE / name).convert("RGBA"))
                preview_frames.append(plate.convert("RGB"))
            preview_frames[0].save(
                preview,
                save_all=True,
                append_images=preview_frames[1:],
                duration=TIMING_MS[key],
                loop=0,
                optimize=False,
            )
            effect["preview"] = preview.relative_to(BASE).as_posix()
        manifest["effects"][key] = effect

    for key, (filename, size) in UI_ART.items():
        source = clean_alpha(Image.open(SOURCE / filename))
        source = source.crop(alpha_bounds(source))
        # Special boxes are intentionally 360x400 like their current pickup
        # siblings. Icons retain a square 112x112 cell. The tether has a fixed
        # top and bottom endpoint on a 64x256 canvas.
        art = clean_alpha(source.resize(size, Image.Resampling.LANCZOS))
        dest = UI / f"{key}.png"
        art.save(dest)
        manifest["ui"][key] = {"source": f"source/{filename}", "file": dest.relative_to(BASE).as_posix(), "size": list(size)}

    with (BASE / "manifest.json").open("w", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
