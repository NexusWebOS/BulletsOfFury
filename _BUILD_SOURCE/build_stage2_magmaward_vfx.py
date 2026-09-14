"""Normalize the generated MAGMA WARD VFX into runtime-ready sprite frames.

The source generations are retained under _BUILD_SOURCE/stage2_magmaward_vfx/raw.
This script only derives transparent, consistently anchored game assets and QA
previews from those originals.
"""

from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "_BUILD_SOURCE" / "stage2_magmaward_vfx" / "raw"
OUT = ROOT / "assets" / "game" / "stage2_magmaward"
PROOF = ROOT / "docs" / "proofs" / "stage2_magmaward_vfx"


def alpha_bbox(im: Image.Image):
    return im.getchannel("A").getbbox()


def remove_edge_checker(im: Image.Image) -> Image.Image:
    """Remove the baked neutral checker using an edge-connected flood fill.

    The projectile's isolated white-hot core is deliberately preserved because
    only background-like pixels connected to an image edge are removed.
    """
    src = im.convert("RGBA")
    px = src.load()
    w, h = src.size

    def is_background(x: int, y: int) -> bool:
        r, g, b, _ = px[x, y]
        return min(r, g, b) >= 205 and max(r, g, b) - min(r, g, b) <= 42

    q = deque()
    seen = bytearray(w * h)

    def enqueue(x: int, y: int):
        idx = y * w + x
        if not seen[idx] and is_background(x, y):
            seen[idx] = 1
            q.append((x, y))

    for x in range(w):
        enqueue(x, 0)
        enqueue(x, h - 1)
    for y in range(h):
        enqueue(0, y)
        enqueue(w - 1, y)

    while q:
        x, y = q.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h:
                enqueue(nx, ny)

    data = list(src.getdata())
    for idx, flagged in enumerate(seen):
        if flagged:
            r, g, b, _ = data[idx]
            data[idx] = (r, g, b, 0)
    src.putdata(data)
    return src


def split_equal(im: Image.Image, count: int):
    frames = []
    w, h = im.size
    for i in range(count):
        x0 = round(i * w / count)
        x1 = round((i + 1) * w / count)
        frames.append(im.crop((x0, 0, x1, h)))
    return frames


def split_alpha_runs(im: Image.Image, expected: int, min_column_pixels=5, min_width=8):
    """Slice a generated strip at its actual transparent gaps.

    Image generation does not always honor mathematically equal cells. Using
    alpha runs prevents a wide pose from donating fragments to its neighbor.
    """
    alpha = im.getchannel("A")
    w, h = im.size
    counts = [sum(1 for y in range(h) if alpha.getpixel((x, y)) > 16) for x in range(w)]
    runs = []
    start = None
    for x, count in enumerate(counts + [0]):
        if count >= min_column_pixels and start is None:
            start = x
        elif count < min_column_pixels and start is not None:
            if x - start >= min_width:
                runs.append((start, x))
            start = None
    if len(runs) != expected:
        raise RuntimeError(f"Expected {expected} alpha runs, found {len(runs)}: {runs}")
    frames = []
    for x0, x1 in runs:
        frames.append(im.crop((max(0, x0 - 2), 0, min(w, x1 + 2), h)))
    return frames


def fit_frame(frame: Image.Image, size, mode="center", crop_top=0, shared_scale=None):
    if crop_top:
        frame = frame.crop((0, crop_top, frame.width, frame.height))
    box = alpha_bbox(frame)
    if not box:
        return Image.new("RGBA", size)
    frame = frame.crop(box)
    pad_x, pad_y = 4, 3
    if shared_scale is None:
        scale = min((size[0] - pad_x * 2) / frame.width, (size[1] - pad_y * 2) / frame.height)
    else:
        scale = shared_scale
    nw = max(1, round(frame.width * scale))
    nh = max(1, round(frame.height * scale))
    frame = frame.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size)
    x = (size[0] - nw) // 2
    if mode == "top":
        y = 0
    elif mode == "bottom":
        y = size[1] - nh
    else:
        y = (size[1] - nh) // 2
    canvas.alpha_composite(frame, (x, y))
    return canvas


def save_frames(frames, stem: str):
    paths = []
    for i, frame in enumerate(frames):
        path = OUT / f"{stem}_{i:02d}.png"
        frame.save(path, optimize=True)
        paths.append(path)
    return paths


def make_preview(groups):
    bg = (34, 10, 7, 255)
    cell_w, cell_h = 150, 292
    rows = len(groups)
    cols = max(len(frames) for _, frames in groups)
    sheet = Image.new("RGBA", (cols * cell_w, rows * cell_h), bg)
    draw = ImageDraw.Draw(sheet)
    for row, (name, frames) in enumerate(groups):
        y0 = row * cell_h
        draw.text((6, y0 + 5), name, fill=(255, 226, 158, 255), stroke_width=1, stroke_fill=(0, 0, 0, 255))
        for col, frame in enumerate(frames):
            thumb = frame.copy()
            scale = min(132 / thumb.width, 252 / thumb.height, 1.0)
            if scale < 1:
                thumb = thumb.resize(
                    (max(1, round(thumb.width * scale)), max(1, round(thumb.height * scale))),
                    Image.Resampling.LANCZOS,
                )
            x = col * cell_w + (cell_w - thumb.width) // 2
            y = y0 + 31 + (252 - thumb.height) // 2
            sheet.alpha_composite(thumb, (x, y))
            draw.rectangle((col * cell_w, y0, col * cell_w + cell_w - 1, y0 + cell_h - 1), outline=(92, 46, 28, 255))
            draw.text((col * cell_w + 6, y0 + cell_h - 20), f"{col:02d}", fill=(255, 156, 62, 255))
    sheet.save(PROOF / "magmaward_vfx_contact_sheet.png", optimize=True)


def make_gif(frames, name, size=(320, 320), duration=72):
    rendered = []
    for frame in frames:
        bg = Image.new("RGBA", size, (19, 7, 6, 255))
        draw = ImageDraw.Draw(bg)
        for y in range(0, size[1], 32):
            draw.line((0, y, size[0], y), fill=(43, 19, 13, 255), width=1)
        x = (size[0] - frame.width) // 2
        y = max(10, (size[1] - frame.height) // 2)
        bg.alpha_composite(frame, (x, y))
        rendered.append(bg.convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
    rendered[0].save(
        PROOF / name,
        save_all=True,
        append_images=rendered[1:],
        loop=0,
        duration=duration,
        disposal=2,
        optimize=False,
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PROOF.mkdir(parents=True, exist_ok=True)

    flame_src = Image.open(RAW / "raw_flamethrower.png").convert("RGBA")
    authored_flame = split_alpha_runs(flame_src, 11)
    # The generator authored eleven clean poses. Duplicate one central turbulent
    # beat to expose a 12-frame runtime loop without inventing a broken tween.
    flame_cells = authored_flame[:6] + [authored_flame[5].copy()] + authored_flame[6:]
    flame = [fit_frame(f, (128, 256), mode="top") for f in flame_cells]

    laser_src = Image.open(RAW / "raw_flame_laser.png").convert("RGBA")
    laser_cells = split_alpha_runs(laser_src, 12)
    # The generation included a repeated cannon housing. The runtime already
    # owns the real barrel, so retain only the lance below its muzzle.
    laser = [fit_frame(f, (96, 256), mode="top", crop_top=100) for f in laser_cells]

    shield_src = Image.open(RAW / "raw_fire_shield.png").convert("RGBA")
    # Keep the common generated cell scale instead of fitting every ring up to
    # the canvas independently. That guarantees a fixed collision silhouette.
    shield_cells = split_equal(shield_src, 8)
    shield = []
    common_y0, common_y1 = 154, 474
    for cell in shield_cells:
        cell = cell.crop((0, common_y0, cell.width, common_y1))
        shield.append(fit_frame(cell, (288, 288), mode="center", shared_scale=0.91))

    fireball_src = remove_edge_checker(Image.open(RAW / "raw_fireball.png"))
    # This generation contains fourteen evenly spaced poses: seven growth/
    # charge beats followed by seven stable travel beats. Resample each section
    # to the requested eight-frame runtime sequences.
    fb_cells = split_alpha_runs(fireball_src, 14)
    charge_src = fb_cells[:7]
    travel_src = fb_cells[7:]
    charge_indices = [round(i * (len(charge_src) - 1) / 7) for i in range(8)]
    travel_indices = [round(i * (len(travel_src) - 1) / 7) for i in range(8)]

    # Preserve the authored growth during charge by fitting all charge poses to
    # a shared scale derived from the largest pose.
    charge_crops = []
    max_w = max_h = 1
    for cell in charge_src:
        box = alpha_bbox(cell)
        crop = cell.crop(box) if box else Image.new("RGBA", (1, 1))
        charge_crops.append(crop)
        max_w = max(max_w, crop.width)
        max_h = max(max_h, crop.height)
    charge_scale = min(88 / max_w, 88 / max_h)
    charge = [fit_frame(charge_src[idx], (96, 96), mode="center", shared_scale=charge_scale) for idx in charge_indices]
    travel = [fit_frame(travel_src[idx], (96, 96), mode="center") for idx in travel_indices]

    save_frames(flame, "magmaward_flamethrower")
    save_frames(laser, "magmaward_flame_laser")
    save_frames(charge, "magmaward_fireball_charge")
    save_frames(travel, "magmaward_fireball")
    save_frames(shield, "magmaward_fire_shield")

    groups = [
        ("FLAMETHROWER — MOUTH / TOP-CENTER ANCHOR", flame),
        ("TWIN FLAME LANCES — BARREL / TOP-CENTER ANCHOR", laser),
        ("CHARGED FIREBALL — CHARGE", charge),
        ("CHARGED FIREBALL — TRAVEL LOOP", travel),
        ("FIRE BUBBLE SHIELD — CENTER ANCHOR", shield),
    ]
    make_preview(groups)
    make_gif(flame, "magmaward_flamethrower.gif", size=(320, 320), duration=70)
    make_gif(laser[2:10], "magmaward_flame_laser.gif", size=(260, 320), duration=68)
    make_gif(charge + travel, "magmaward_charged_fireball.gif", size=(240, 240), duration=88)
    make_gif(shield, "magmaward_fire_shield.gif", size=(340, 340), duration=82)
    print(f"Wrote {sum(len(g[1]) for g in groups)} frames to {OUT}")
    print(f"Wrote previews to {PROOF}")


if __name__ == "__main__":
    main()
