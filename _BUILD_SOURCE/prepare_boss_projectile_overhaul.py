"""Prepare generated boss projectile/muzzle atlases for runtime use.

The image generator returns a baked neutral checkerboard.  This script removes
only edge-connected neutral light pixels, so enclosed white-hot projectile cores
remain opaque, then exports stable 128x128 cells with a shared center pivot.
"""

from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "game" / "boss_projectile_overhaul"
ROWS = ("kinetic", "laser", "missile", "void")
CELL = 128


def is_background(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, _ = pixel
    return min(r, g, b) >= 218 and max(r, g, b) - min(r, g, b) <= 18


def clear_edge_background(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    px = rgba.load()
    width, height = rgba.size
    seen: set[tuple[int, int]] = set()
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(height):
        queue.append((0, y))
        queue.append((width - 1, y))

    while queue:
        x, y = queue.popleft()
        if (x, y) in seen or not (0 <= x < width and 0 <= y < height):
            continue
        seen.add((x, y))
        if not is_background(px[x, y]):
            continue
        px[x, y] = (0, 0, 0, 0)
        queue.extend(((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)))
    return rgba


def remove_generated_socket(cell: Image.Image) -> Image.Image:
    """Remove the gray locator dot ImageGen drew above each muzzle flash."""
    rgba = cell.copy()
    px = rgba.load()
    colored_rows: list[int] = []
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            spread = max(r, g, b) - min(r, g, b)
            if spread >= 42 and max(r, g, b) >= 110:
                colored_rows.append(y)
                break
    if colored_rows:
        first_color = min(colored_rows)
        # The locator has a short neutral stem that overlaps the first colored
        # ignition pixels, so clear neutral pixels slightly into the flash while
        # preserving the saturated flame/plasma underneath it.
        for y in range(min(rgba.height, first_color + 14)):
            for x in range(rgba.width):
                r, g, b, a = px[x, y]
                if a and max(r, g, b) - min(r, g, b) < 42:
                    px[x, y] = (0, 0, 0, 0)
    return rgba


def normalize_cell(cell: Image.Image, *, projectile: bool) -> Image.Image:
    if projectile:
        # Native runtime projectile art faces down. ImageGen supplied upward art.
        cell = cell.rotate(180)
    bbox = cell.getbbox()
    canvas = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    if not bbox:
        return canvas
    sprite = cell.crop(bbox)
    limit_w, limit_h = (88, 112) if projectile else (112, 104)
    scale = min(limit_w / sprite.width, limit_h / sprite.height, 1.0)
    if scale < 1:
        sprite = sprite.resize(
            (max(1, round(sprite.width * scale)), max(1, round(sprite.height * scale))),
            Image.Resampling.NEAREST,
        )
    x = (CELL - sprite.width) // 2
    y = (CELL - sprite.height) // 2
    canvas.alpha_composite(sprite, (x, y))
    return canvas


def export_atlas(source_name: str, prefix: str, *, projectile: bool) -> None:
    source = clear_edge_background(Image.open(OUT / source_name))
    src_w, src_h = source.size
    master = Image.new("RGBA", (CELL * 8, CELL * 4), (0, 0, 0, 0))
    for row, family in enumerate(ROWS):
        y0, y1 = round(row * src_h / 4), round((row + 1) * src_h / 4)
        for frame in range(8):
            x0, x1 = round(frame * src_w / 8), round((frame + 1) * src_w / 8)
            cell = source.crop((x0, y0, x1, y1))
            if not projectile:
                cell = remove_generated_socket(cell)
            cell = normalize_cell(cell, projectile=projectile)
            cell.save(OUT / f"{prefix}_{family}_{frame}.png", optimize=True)
            master.alpha_composite(cell, (frame * CELL, row * CELL))
    master.save(OUT / f"{prefix}_master_clean.png", optimize=True)


def export_preview(prefix: str, name: str, duration: int) -> None:
    proof = ROOT / "docs" / "proofs" / "boss_projectile_overhaul"
    proof.mkdir(parents=True, exist_ok=True)
    frames: list[Image.Image] = []
    for frame in range(8):
        board = Image.new("RGBA", (640, 188), (4, 8, 18, 255))
        draw = ImageDraw.Draw(board)
        for column, family in enumerate(ROWS):
            x = 16 + column * 156
            sprite = Image.open(OUT / f"{prefix}_{family}_{frame}.png").convert("RGBA")
            board.alpha_composite(sprite, (x + 14, 28))
            draw.text((x + 56, 164), family.upper(), fill=(220, 235, 255, 255), anchor="mm")
        frames.append(board.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(
        proof / name,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        disposal=2,
        optimize=False,
    )


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    export_atlas("projectile_master_4x8.png", "bpfx_proj", projectile=True)
    export_atlas("muzzle_master_4x8.png", "bpfx_muzzle", projectile=False)
    export_preview("bpfx_proj", "projectile_families.gif", 75)
    export_preview("bpfx_muzzle", "muzzle_families.gif", 60)
    print(f"Prepared 64 frames in {OUT}")
