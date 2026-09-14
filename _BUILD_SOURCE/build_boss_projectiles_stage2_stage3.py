"""Normalize generated Inferno Reaver / Cryo Spear / Rime Wall projectile strips.

Raw ImageGen outputs stay under _BUILD_SOURCE/boss_projectiles_stage2_stage3/raw.
This derives fixed-box, shared-scale, transparent runtime frames plus QA previews.
"""

from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "_BUILD_SOURCE" / "boss_projectiles_stage2_stage3" / "raw"
OUT = ROOT / "assets" / "game" / "boss_projectiles_stage2_stage3"
PROOF = ROOT / "docs" / "proofs" / "boss_projectiles_stage2_stage3"


FAMILIES = {
    "inferno_mg": (8, (40, 64)),
    "inferno_shotgun": (8, (56, 76)),
    "inferno_laser": (12, (96, 256)),
    "cryo_ball": (8, (64, 64)),
    "rime_orb": (8, (104, 104)),
    "rime_laser": (12, (96, 256)),
}


def checker_to_alpha(im: Image.Image) -> Image.Image:
    """Remove ImageGen's baked neutral checker without keying blue-white ice."""
    src = im.convert("RGBA")
    data = []
    for r, g, b, a in src.getdata():
        neutral = max(r, g, b) - min(r, g, b) <= 5
        if neutral and min(r, g, b) >= 228:
            data.append((r, g, b, 0))
        else:
            data.append((r, g, b, a))
    src.putdata(data)
    return src


def split_equal(im: Image.Image, count: int):
    frames = []
    for i in range(count):
        x0 = round(i * im.width / count)
        x1 = round((i + 1) * im.width / count)
        frames.append(im.crop((x0, 0, x1, im.height)))
    return frames


def split_runs(im: Image.Image, minimum_pixels=8, minimum_width=5):
    """Split vertical effects at their actual transparent gutters.

    ImageGen keeps the requested ordering but does not promise mathematically
    equal slot widths. Run detection prevents one beam donating its edge to the
    neighboring frame.
    """
    alpha = im.getchannel("A")
    counts = [sum(alpha.getpixel((x, y)) > 24 for y in range(im.height)) for x in range(im.width)]
    runs, start = [], None
    for x, count in enumerate(counts + [0]):
        if count >= minimum_pixels and start is None:
            start = x
        elif count < minimum_pixels and start is not None:
            if x - start >= minimum_width:
                runs.append(im.crop((max(0, start - 2), 0, min(im.width, x + 2), im.height)))
            start = None
    return runs


def normalize(frames, target):
    crops = []
    max_w = max_h = 1
    for frame in frames:
        box = frame.getchannel("A").getbbox()
        crop = frame.crop(box) if box else Image.new("RGBA", (1, 1))
        crops.append(crop)
        max_w, max_h = max(max_w, crop.width), max(max_h, crop.height)
    scale = min((target[0] - 6) / max_w, (target[1] - 6) / max_h)
    result = []
    for crop in crops:
        size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
        crop = crop.resize(size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", target)
        # Beams are top-center muzzle anchored; travelling rounds are center anchored.
        y = 0 if target[1] >= 200 else (target[1] - size[1]) // 2
        canvas.alpha_composite(crop, ((target[0] - size[0]) // 2, y))
        result.append(canvas)
    return result


def save_family(stem, frames):
    for i, frame in enumerate(frames):
        frame.save(OUT / f"{stem}_{i:02d}.png", optimize=True)


def preview(groups):
    cell_w, cell_h = 128, 282
    cols = max(len(v) for v in groups.values())
    sheet = Image.new("RGBA", (cols * cell_w, len(groups) * cell_h), (8, 12, 22, 255))
    draw = ImageDraw.Draw(sheet)
    for row, (name, frames) in enumerate(groups.items()):
        y0 = row * cell_h
        draw.text((6, y0 + 5), name.upper(), fill=(215, 240, 255), stroke_width=1, stroke_fill=(0, 0, 0))
        for col, frame in enumerate(frames):
            thumb = frame.copy()
            scale = min(112 / thumb.width, 238 / thumb.height, 1)
            if scale < 1:
                thumb = thumb.resize((round(thumb.width * scale), round(thumb.height * scale)), Image.Resampling.NEAREST)
            x = col * cell_w + (cell_w - thumb.width) // 2
            y = y0 + 28 + (238 - thumb.height) // 2
            sheet.alpha_composite(thumb, (x, y))
            draw.rectangle((col * cell_w, y0, col * cell_w + cell_w - 1, y0 + cell_h - 1), outline=(35, 78, 112))
            draw.text((col * cell_w + 6, y0 + cell_h - 18), f"{col:02d}", fill=(114, 218, 255))
    sheet.save(PROOF / "boss_projectiles_contact_sheet.png", optimize=True)


def gif(frames, name, bg, duration=72):
    rendered = []
    for frame in frames:
        canvas = Image.new("RGBA", (240, 300), bg)
        canvas.alpha_composite(frame, ((240 - frame.width) // 2, max(8, (300 - frame.height) // 2)))
        rendered.append(canvas.convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
    rendered[0].save(PROOF / name, save_all=True, append_images=rendered[1:], loop=0,
                     duration=duration, disposal=2, optimize=False)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PROOF.mkdir(parents=True, exist_ok=True)
    groups = {}
    for stem, (count, target) in FAMILIES.items():
        src = Image.open(RAW / f"{stem}_raw.png")
        if "A" not in src.getbands():
            src = checker_to_alpha(src)
        else:
            src = src.convert("RGBA")
        if stem.endswith("laser"):
            cells = split_runs(src)
            # The ice generation authored eleven clean beats. Duplicate one
            # central sustain pose to expose the requested twelve-frame timing
            # without inventing a mismatched tween or fading the beam early.
            if stem == "rime_laser" and len(cells) == 11:
                cells = cells[:6] + [cells[5].copy()] + cells[6:]
            if len(cells) != count:
                raise RuntimeError(f"{stem}: expected {count} alpha runs, found {len(cells)}")
        else:
            cells = split_equal(src, count)
        frames = normalize(cells, target)
        save_family(stem, frames)
        groups[stem] = frames
    preview(groups)
    gif(groups["inferno_mg"], "inferno_mg.gif", (31, 8, 3, 255), 62)
    gif(groups["inferno_shotgun"], "inferno_shotgun.gif", (31, 8, 3, 255), 70)
    gif(groups["inferno_laser"], "inferno_laser.gif", (31, 8, 3, 255), 68)
    gif(groups["cryo_ball"], "cryo_ball.gif", (9, 27, 50, 255), 72)
    gif(groups["rime_orb"], "rime_orb.gif", (9, 27, 50, 255), 72)
    gif(groups["rime_laser"], "rime_laser.gif", (9, 27, 50, 255), 68)
    print(f"Wrote {sum(len(v) for v in groups.values())} normalized frames and six previews")


if __name__ == "__main__":
    main()
