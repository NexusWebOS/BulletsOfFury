"""Build the Stage-9 Laser Mist reward atlas from the approved GPT source sheets.

The generated sources deliberately use a flat magenta production matte and very
large gutters.  This builder keys the matte, trims each frame independently,
and repacks the results with fixed empty padding so no animation cell can borrow
pixels from its neighbour at runtime.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path(r"C:\Users\Mike\.codex\generated_images\01a0356a-5a7c-7601-aba6-43bc3b493520")
SOURCES = {
    "icons": GENERATED / "exec-965608db-1c98-467d-88a4-4a8b6dde6473.png",
    "beams": GENERATED / "exec-edf43061-8b5d-4c1f-ad43-600b0a723816.png",
    "effects": GENERATED / "exec-b96b53b9-7197-4f7c-a1fc-ac699b660f66.png",
}
OUT_DIR = ROOT / "assets" / "game" / "laser_mist"
ATLAS_PATH = OUT_DIR / "bof_laser_mist_weapon_atlas.png"
MAP_PATH = OUT_DIR / "bof_laser_mist_weapon_atlas.json"
SOURCE_DIR = OUT_DIR / "sources"


def remove_matte(src: Image.Image) -> Image.Image:
    """Remove generated magenta while retaining cyan water glow and white cores."""
    rgba = src.convert("RGBA")
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            # The generated matte varies slightly around #e20dde.  Water art is
            # cyan (G/B dominant), so requiring both R and B to outrun G makes
            # the key safe for the authored glow, white cores, and tier rims.
            magenta = r > g + 42 and b > g + 42 and abs(r - b) < 105
            if magenta:
                px[x, y] = (0, 0, 0, 0)
            else:
                # Remove only red matte spill from otherwise blue/cyan edges.
                if b > r and b > g and r > g:
                    r = g
                px[x, y] = (r, g, b, 255)
    return rgba


def grid_cells(src: Image.Image, cols: int, rows: int) -> list[Image.Image]:
    cells: list[Image.Image] = []
    for row in range(rows):
        y0 = round(row * src.height / rows)
        y1 = round((row + 1) * src.height / rows)
        for col in range(cols):
            x0 = round(col * src.width / cols)
            x1 = round((col + 1) * src.width / cols)
            cells.append(src.crop((x0, y0, x1, y1)))
    return cells


def _projection(alpha: Image.Image, axis: str, lo: int, hi: int) -> list[int]:
    """Count visible pixels per source line inside one band."""
    px = alpha.load()
    if axis == "x":
        return [sum(px[x, y] > 8 for y in range(lo, hi)) for x in range(alpha.width)]
    return [sum(px[x, y] > 8 for x in range(lo, hi)) for y in range(alpha.height)]


def _low_runs(values: list[int], threshold: int, edge_pad: int = 3) -> list[tuple[int, int]]:
    runs: list[tuple[int, int]] = []
    start = None
    for i, value in enumerate(values + [threshold + 1]):
        if value <= threshold and start is None:
            start = i
        elif value > threshold and start is not None:
            if i - start >= 3 and start > edge_pad and i < len(values) - edge_pad:
                runs.append((start, i - 1))
            start = None
    return runs


def _blank_line(values: list[int], run: tuple[int, int]) -> int:
    """Use the emptiest line nearest the middle of the selected gutter."""
    a, b = run
    mid = (a + b) / 2
    return min(range(a, b + 1), key=lambda i: (values[i], abs(i - mid)))


def _row_separators(alpha: Image.Image, rows: int) -> list[int]:
    values = _projection(alpha, "y", 0, alpha.width)
    # Generated rows are not equally spaced: choose the widest real transparent valleys.
    runs = sorted(_low_runs(values, 8), key=lambda q: (q[1] - q[0] + 1), reverse=True)[: rows - 1]
    if len(runs) != rows - 1:
        raise RuntimeError(f"Could not locate {rows - 1} clean row gutters")
    return sorted(_blank_line(values, run) for run in runs)


def _column_separators(alpha: Image.Image, y0: int, y1: int, cols: int) -> list[int]:
    values = _projection(alpha, "x", y0, y1)
    runs = _low_runs(values, 2)
    step = alpha.width / cols
    selected: list[tuple[int, int]] = []
    for k in range(1, cols):
        nominal = k * step
        candidates = [run for run in runs if abs(((run[0] + run[1]) / 2) - nominal) <= step * 0.48]
        if not candidates:
            raise RuntimeError(f"Could not locate clean column gutter {k}/{cols} in y={y0}:{y1}")
        # Prefer a broad empty gutter, with a small penalty for drifting away from the expected slot.
        choice = max(candidates, key=lambda run: (run[1] - run[0] + 1) - abs(((run[0] + run[1]) / 2) - nominal) * 0.25)
        if choice in selected:
            raise RuntimeError(f"Column gutter reused at {choice} in y={y0}:{y1}")
        selected.append(choice)
    lines = [_blank_line(values, run) for run in selected]
    if lines != sorted(lines):
        raise RuntimeError(f"Column gutters are not ordered in y={y0}:{y1}: {lines}")
    return lines


def adaptive_grid_cells(src: Image.Image, cols: int, rows: int) -> tuple[list[Image.Image], dict]:
    """Slice generated strips at real transparent valleys instead of mathematical fractions."""
    alpha = src.getchannel("A")
    ys = _row_separators(alpha, rows)
    ybounds = [0, *ys, src.height]
    cells: list[Image.Image] = []
    columns: list[list[int]] = []
    for row in range(rows):
        y0, y1 = ybounds[row], ybounds[row + 1]
        xs = _column_separators(alpha, y0, y1, cols)
        xbounds = [0, *xs, src.width]
        columns.append(xs)
        for col in range(cols):
            cell = src.crop((xbounds[col], y0, xbounds[col + 1], y1))
            # A crop edge containing visible source pixels proves a frame was sliced, so fail loudly.
            ca = cell.getchannel("A")
            edge = list(ca.crop((0, 0, ca.width, 1)).getdata())
            edge += list(ca.crop((0, ca.height - 1, ca.width, ca.height)).getdata())
            edge += list(ca.crop((0, 0, 1, ca.height)).getdata())
            edge += list(ca.crop((ca.width - 1, 0, ca.width, ca.height)).getdata())
            if any(v > 8 for v in edge):
                raise RuntimeError(f"Visible source pixels touch adaptive cell edge row={row} col={col}")
            cells.append(cell)
    return cells, {"rowSeparators": ys, "columnSeparators": columns}


def trim(cell: Image.Image, safety: int = 3) -> Image.Image:
    alpha = cell.getchannel("A")
    box = alpha.getbbox()
    if not box:
        return Image.new("RGBA", (1, 1))
    l, t, r, b = box
    return cell.crop((max(0, l - safety), max(0, t - safety),
                      min(cell.width, r + safety), min(cell.height, b + safety)))


def place_fit(atlas: Image.Image, cell: Image.Image, box: tuple[int, int, int, int], pad: int = 6) -> dict:
    x, y, w, h = box
    cell = trim(cell)
    scale = min((w - pad * 2) / max(1, cell.width), (h - pad * 2) / max(1, cell.height))
    nw = max(1, round(cell.width * scale))
    nh = max(1, round(cell.height * scale))
    cell = cell.resize((nw, nh), Image.Resampling.LANCZOS)
    dx = x + (w - nw) // 2
    dy = y + (h - nh) // 2
    atlas.alpha_composite(cell, (dx, dy))
    return {"x": x, "y": y, "w": w, "h": h, "content": [dx, dy, nw, nh], "padding": pad}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    # The first build reads Codex's generated matte sheets.  The keyed source copies below are
    # checked into the project, so another workstation can reproduce the atlas without depending
    # on this machine's generated-image cache.
    keyed = {}
    for name, path in SOURCES.items():
        portable = SOURCE_DIR / f"laser_mist_{name}_keyed.png"
        if path.exists():
            keyed[name] = remove_matte(Image.open(path))
        elif portable.exists():
            keyed[name] = Image.open(portable).convert("RGBA")
        else:
            raise FileNotFoundError(f"Missing both generated and portable Laser Mist source: {name}")
    for name, image in keyed.items():
        image.save(SOURCE_DIR / f"laser_mist_{name}_keyed.png", optimize=True)

    icons = grid_cells(keyed["icons"], 5, 1)
    beams, beam_slices = adaptive_grid_cells(keyed["beams"], 4, 5)
    effects, effect_slices = adaptive_grid_cells(keyed["effects"], 8, 3)

    atlas = Image.new("RGBA", (1024, 896), (0, 0, 0, 0))
    frames: dict[str, dict] = {}

    # Fixed padded cells make the atlas auditable by eye and keep filtering from
    # sampling adjacent frames at small HUD/gameplay scales.
    for tier, cell in enumerate(icons, 1):
        frames[f"micon_lasermist_{tier}"] = place_fit(atlas, cell, ((tier - 1) * 160, 0, 152, 152), 10)

    for tier in range(1, 6):
        for frame in range(4):
            idx = (tier - 1) * 4 + frame
            frames[f"lmfx_beam_{tier}_{frame}"] = place_fit(
                atlas, beams[idx], (frame * 72, 160 + (tier - 1) * 96, 64, 88), 7
            )

    for frame in range(8):
        frames[f"lmfx_impact_{frame}"] = place_fit(atlas, effects[frame], (frame * 112, 648, 104, 104), 8)
        frames[f"lmfx_decal_{frame}"] = place_fit(atlas, effects[8 + frame], (frame * 112, 760, 104, 104), 8)
        frames[f"lmfx_bubble_{frame}"] = place_fit(atlas, effects[16 + frame], (296 + frame * 88, 160, 80, 80), 8)

    # Hard QA: every atlas cell must retain a fully transparent safety ring.
    for name, meta in frames.items():
        x, y, w, h = meta["x"], meta["y"], meta["w"], meta["h"]
        a = atlas.getchannel("A")
        edge = list(a.crop((x, y, x + w, y + 1)).getdata())
        edge += list(a.crop((x, y + h - 1, x + w, y + h)).getdata())
        edge += list(a.crop((x, y, x + 1, y + h)).getdata())
        edge += list(a.crop((x + w - 1, y, x + w, y + h)).getdata())
        if any(edge):
            raise RuntimeError(f"Atlas safety ring is not transparent: {name}")

    atlas.save(ATLAS_PATH, optimize=True)
    MAP_PATH.write_text(json.dumps({
        "image": ATLAS_PATH.name,
        "size": [atlas.width, atlas.height],
        "source": "GPT ImageGen sources, chroma-keyed and gutter-packed by build_laser_mist_assets.py",
        "frames": frames,
        "sourceSlices": {"beams": beam_slices, "effects": effect_slices},
    }, indent=2), encoding="utf-8")

    # Review sheet: every runtime rect on a checkerboard, with no neighboring cell available to
    # hide a bad crop. This is the approval surface for the slice pass, not another game asset.
    proof_dir = ROOT / "docs" / "proofs" / "laser_mist_slices_0902"
    proof_dir.mkdir(parents=True, exist_ok=True)
    preview = Image.new("RGB", (1000, 1030), (12, 16, 23))
    draw = ImageDraw.Draw(preview)

    def checker(box: tuple[int, int, int, int], tile: int = 8) -> None:
        x, y, w, h = box
        for yy in range(y, y + h, tile):
            for xx in range(x, x + w, tile):
                c = (46, 52, 62) if ((xx - x) // tile + (yy - y) // tile) % 2 else (28, 33, 41)
                draw.rectangle((xx, yy, min(x + w - 1, xx + tile - 1), min(y + h - 1, yy + tile - 1)), fill=c)

    def cell_preview(key: str, x: int, y: int, w: int, h: int) -> None:
        checker((x, y, w, h))
        m = frames[key]
        cut = atlas.crop((m["x"], m["y"], m["x"] + m["w"], m["y"] + m["h"]))
        scale = min((w - 8) / cut.width, (h - 8) / cut.height)
        cut = cut.resize((max(1, round(cut.width * scale)), max(1, round(cut.height * scale))), Image.Resampling.NEAREST)
        preview.paste(cut, (x + (w - cut.width) // 2, y + (h - cut.height) // 2), cut)
        draw.rectangle((x, y, x + w - 1, y + h - 1), outline=(94, 112, 132))

    draw.text((18, 12), "LASER MIST - CLEAN SLICE REVIEW", fill=(198, 232, 255))
    draw.text((18, 38), "PICKUP ICONS I-V", fill=(92, 220, 255))
    for tier in range(1, 6):
        cell_preview(f"micon_lasermist_{tier}", 18 + (tier - 1) * 188, 58, 170, 150)
    draw.text((18, 222), "PROJECTILES - 5 TIERS x 4 COMPLETE FRAMES", fill=(92, 220, 255))
    for tier in range(1, 6):
        for frame in range(4):
            cell_preview(f"lmfx_beam_{tier}_{frame}", 18 + frame * 120, 244 + (tier - 1) * 116, 104, 104)
    for label, prefix, py in [("IMPACTS", "lmfx_impact", 836), ("RIPPLE DECALS", "lmfx_decal", 914)]:
        draw.text((18, py - 18), label, fill=(92, 220, 255))
        for frame in range(8):
            cell_preview(f"{prefix}_{frame}", 18 + frame * 120, py, 104, 68)
    preview_path = proof_dir / "laser_mist_clean_slice_preview.png"
    preview.save(preview_path, optimize=True)
    print(f"wrote {ATLAS_PATH} ({atlas.width}x{atlas.height})")
    print(f"wrote {MAP_PATH} ({len(frames)} frames)")
    print(f"wrote {preview_path}")


if __name__ == "__main__":
    main()
