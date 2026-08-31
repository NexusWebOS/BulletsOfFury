"""Build the Bullets of Fury Gravity Mode v2 runtime atlas.

Source masters live in _ART_SOURCES/gravity_mode_v2.  The build removes the
generation mattes, crops the authored cells, normalizes runtime scale, packs a
single texture atlas, and emits a labelled proof sheet for visual QA.
"""

from __future__ import annotations

import json
import math
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "_ART_SOURCES" / "gravity_mode_v2"
OUT = ROOT / "assets" / "game" / "atlas"
PROOF = ROOT / "docs" / "proofs"
ATLAS_PNG = OUT / "bof_gravity_mode_space_weapons.png"
ATLAS_JSON = OUT / "bof_gravity_mode_space_weapons.json"
ATLAS_JS = OUT / "bof_gravity_mode_space_weapons.js"
PROOF_PNG = PROOF / "Gravity_Mode_v2_Asset_Atlas_Labeled.png"
REVIEW_PNG = PROOF / "Gravity_Mode_v3_Blue_Mask_Weapons_Review.png"


def rgba(name: str) -> Image.Image:
    return Image.open(SRC / name).convert("RGBA")


def magenta_key(im: Image.Image) -> Image.Image:
    a = np.asarray(im.convert("RGBA")).copy()
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    bg = (r > 160) & (g < 125) & (b > 160) & (np.abs(r - b) < 120)
    a[..., 3] = np.where(bg, 0, a[..., 3])
    return Image.fromarray(a, "RGBA")


def neutralize_ship_edge_purple(im: Image.Image, passes: int = 8) -> Image.Image:
    """Turn transparency-adjacent purple key spill into the ship's dark outline.

    The recovered rotation sheet was antialiased against hot magenta.  Removing only the
    background key leaves a two-to-four pixel violet rind around every pose, especially after
    the runtime pilot-palette overlay.  Purple inside the opaque hull is not selected: this is a
    boundary-distance operation, and the selected pixels retain alpha so the silhouette cannot
    fray or shrink.
    """
    a = np.asarray(im.convert("RGBA")).copy()
    alpha = a[..., 3]
    opaque = alpha > 0
    near_clear = ~opaque
    for _ in range(max(1, passes)):
        expanded = near_clear.copy()
        expanded[1:] |= near_clear[:-1]
        expanded[:-1] |= near_clear[1:]
        expanded[:, 1:] |= near_clear[:, :-1]
        expanded[:, :-1] |= near_clear[:, 1:]
        near_clear = expanded

    rgb = a[..., :3].astype(int)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    purple = (r > g + 10) & (b > g + 18) & (r > 35) & (b > 35)
    rim = opaque & near_clear & purple
    # Five restrained steel-outline steps preserve the original edge contrast without replacing
    # the halo with a flat black sticker.
    shades = np.asarray(
        ((6, 9, 13), (12, 16, 22), (19, 24, 32), (27, 33, 43), (38, 45, 56)),
        dtype=np.uint8,
    )
    lum = (r * 21 + g * 72 + b * 7) // 100
    band = np.clip(lum * len(shades) // 96, 0, len(shades) - 1)
    a[rim, :3] = shades[band[rim]]
    # Transparent RGB must be neutral as well; otherwise linear texture sampling can reintroduce
    # a colored fringe even though the source pixel's alpha is zero.
    a[~opaque, :3] = 0
    return Image.fromarray(a, "RGBA")


def neutral_edge_key(im: Image.Image) -> Image.Image:
    """Flood only the light neutral checkerboard connected to a crop edge."""
    a = np.asarray(im.convert("RGBA")).copy()
    rgb = a[..., :3].astype(int)
    neutral = ((rgb.max(2) - rgb.min(2)) < 22) & (rgb.min(2) > 172)
    h, w = neutral.shape
    seen = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        if neutral[0, x]: q.append((0, x)); seen[0, x] = True
        if neutral[h - 1, x]: q.append((h - 1, x)); seen[h - 1, x] = True
    for y in range(h):
        if neutral[y, 0] and not seen[y, 0]: q.append((y, 0)); seen[y, 0] = True
        if neutral[y, w - 1] and not seen[y, w - 1]: q.append((y, w - 1)); seen[y, w - 1] = True
    while q:
        y, x = q.popleft()
        for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= yy < h and 0 <= xx < w and neutral[yy, xx] and not seen[yy, xx]:
                seen[yy, xx] = True
                q.append((yy, xx))
    a[..., 3] = np.where(seen, 0, a[..., 3])
    return Image.fromarray(a, "RGBA")


def gradient_key(im: Image.Image, radius: int = 28, threshold: int = 18) -> Image.Image:
    """Remove a smooth generated backdrop while retaining luminous FX."""
    src = im.convert("RGB")
    base = src.filter(ImageFilter.GaussianBlur(radius))
    s = np.asarray(src).astype(int)
    b = np.asarray(base).astype(int)
    delta = np.max(np.abs(s - b), axis=2)
    lum = s.mean(axis=2)
    base_lum = b.mean(axis=2)
    score = delta + np.maximum(0, lum - base_lum) * 0.75
    alpha = np.clip((score - threshold) * 10, 0, 255).astype(np.uint8)
    # Keep bright cores even where the local blur is also bright.
    alpha = np.maximum(alpha, np.clip((lum - 185) * 5, 0, 255).astype(np.uint8))
    out = np.dstack((s.astype(np.uint8), alpha))
    return Image.fromarray(out, "RGBA")


def trim(im: Image.Image, pad: int = 3) -> Image.Image:
    alpha = im.getchannel("A")
    box = alpha.getbbox()
    if not box:
        return Image.new("RGBA", (4, 4))
    x0, y0, x1, y1 = box
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(im.width, x1 + pad), min(im.height, y1 + pad)
    return im.crop((x0, y0, x1, y1))


def largest_alpha_component(im: Image.Image, cutoff: int = 44) -> Image.Image:
    """Keep one connected authored projectile from a generated formation cell."""
    a = np.asarray(im.convert("RGBA")).copy()
    mask = a[..., 3] > cutoff
    h, w = mask.shape
    seen = np.zeros((h, w), dtype=bool)
    best: list[tuple[int, int]] = []
    for sy in range(h):
        for sx in range(w):
            if not mask[sy, sx] or seen[sy, sx]:
                continue
            q: deque[tuple[int, int]] = deque([(sy, sx)])
            seen[sy, sx] = True
            comp: list[tuple[int, int]] = []
            while q:
                y, x = q.popleft()
                comp.append((y, x))
                for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = True
                        q.append((yy, xx))
            if len(comp) > len(best):
                best = comp
    keep = np.zeros((h, w), dtype=bool)
    for y, x in best:
        keep[y, x] = True
    # Retain antialias pixels immediately around the chosen hard-alpha body.
    halo = keep.copy()
    for _ in range(2):
        halo[1:] |= halo[:-1]; halo[:-1] |= halo[1:]
        halo[:, 1:] |= halo[:, :-1]; halo[:, :-1] |= halo[:, 1:]
    a[..., 3] = np.where(halo, a[..., 3], 0)
    return Image.fromarray(a, "RGBA")


def contain(im: Image.Image, max_w: int, max_h: int) -> Image.Image:
    scale = min(max_w / im.width, max_h / im.height, 1.0)
    if scale >= 0.999:
        return im
    return im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.Resampling.LANCZOS)


def crop_grid(im: Image.Image, cols: int, rows: int, col: int, row: int) -> Image.Image:
    x0 = round(im.width * col / cols)
    x1 = round(im.width * (col + 1) / cols)
    y0 = round(im.height * row / rows)
    y1 = round(im.height * (row + 1) / rows)
    return im.crop((x0, y0, x1, y1))


def pulse(im: Image.Image, scale: float, brightness: float) -> Image.Image:
    p = ImageEnhance.Brightness(im).enhance(brightness)
    p = p.resize((max(1, round(p.width * scale)), max(1, round(p.height * scale))), Image.Resampling.LANCZOS)
    return p


def blue_mask(im: Image.Image) -> Image.Image:
    """Return only Axel's authored blue/cyan pixels as a luminance mask.

    Runtime tints this small layer and composites it back over the untouched source frame.  Steel,
    black linework, white speculars and orange UI trim never enter the mask, so changing pilot
    colour cannot repaint the whole ship.
    """
    a = np.asarray(im.convert("RGBA")).copy()
    rgb = a[..., :3].astype(np.float32) / 255.0
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    delta = mx - mn
    sat = np.where(mx > 0.001, delta / np.maximum(mx, 0.001), 0.0)
    hue = np.zeros_like(mx)
    nz = delta > 0.001
    rr, gg, bb = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    rm = nz & (mx == rr)
    gm = nz & (mx == gg)
    bm = nz & (mx == bb)
    hue[rm] = ((gg[rm] - bb[rm]) / delta[rm]) % 6.0
    hue[gm] = ((bb[gm] - rr[gm]) / delta[gm]) + 2.0
    hue[bm] = ((rr[bm] - gg[bm]) / delta[bm]) + 4.0
    hue /= 6.0
    # Blue through cyan only.  The modest saturation floor retains pale blue energy fringes while
    # excluding neutral steel and white highlights.
    pick = (a[..., 3] > 0) & (sat > 0.22) & (mx > 0.16) & (hue >= 0.47) & (hue <= 0.72)
    lum = np.clip(rr * 0.22 + gg * 0.62 + bb * 0.16, 0.0, 1.0)
    out = np.zeros_like(a)
    out[..., 0] = out[..., 1] = out[..., 2] = np.clip(lum * 255, 0, 255).astype(np.uint8)
    out[..., 3] = np.where(pick, a[..., 3], 0).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def square_canvas(im: Image.Image, side: int = 124) -> Image.Image:
    src = contain(trim(im, 6), side - 14, side - 14)
    out = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    out.alpha_composite(src, ((side - src.width) // 2, (side - src.height) // 2))
    return out


def piece_motion_frames(im: Image.Image, side: int = 124) -> tuple[list[Image.Image], list[Image.Image]]:
    """Eight in-plane turns plus eight perspective card flips, all on a no-clip fixed canvas."""
    base = square_canvas(im, side)
    turns: list[Image.Image] = []
    flips: list[Image.Image] = []
    for i in range(8):
        angle = i * 45
        turns.append(base.rotate(-angle, resample=Image.Resampling.NEAREST, expand=False))
        c = math.cos(math.radians(angle))
        src = ImageOps.mirror(base) if c < 0 else base
        fw = max(6, round(side * max(0.08, abs(c))))
        squeezed = src.resize((fw, side), Image.Resampling.NEAREST)
        card = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        card.alpha_composite(squeezed, ((side - fw) // 2, 0))
        flips.append(card)
    return turns, flips


frames: dict[str, Image.Image] = {}


def add(key: str, im: Image.Image, max_w: int = 220, max_h: int = 220) -> None:
    prepared = contain(trim(im), max_w, max_h)
    # LANCZOS normalization can pull a few key-colored RGB values back into low-alpha boundary
    # pixels. Run the same silhouette-preserving cleanup on the final runtime-sized ship cell,
    # not only on the large source sheet.
    if key == "ship_base" or key.startswith("ship_bank_") or key.startswith("ship_roll_"):
        prepared = neutralize_ship_edge_purple(prepared, passes=10)
    frames[key] = prepared


# Canonical Fury ship: first clean top-down frame from the user's recovered sheet.
ship_master = neutralize_ship_edge_purple(
    magenta_key(rgba("canonical_fury_ship_rotations.png"))
)
add("ship_base", ship_master.crop((374, 60, 532, 225)), 150, 162)
# The middle authored row is the missing ordinary left/right turn set.  These are not generated
# approximations and they are not the somersault cycle below: three progressively harder poses on
# each side preserve the Fury hull's perspective as the player banks during regular movement.
ship_bank_boxes = {
    "ship_bank_l3": (137, 282, 300, 474),
    "ship_bank_l2": (314, 282, 475, 474),
    "ship_bank_l1": (490, 282, 658, 474),
    "ship_bank_r1": (862, 282, 1034, 474),
    "ship_bank_r2": (1042, 282, 1212, 474),
    "ship_bank_r3": (1218, 282, 1392, 474),
}
for key, box in ship_bank_boxes.items():
    add(key, ship_master.crop(box), 150, 162)
# The bottom two authored rows are the complete top-down rotation/barrel-roll cycle.
ship_roll_boxes = [
    (51, 550, 179, 688), (250, 554, 318, 688), (409, 550, 465, 684),
    (544, 550, 632, 688), (711, 546, 827, 688), (909, 550, 978, 688),
    (1075, 550, 1131, 683), (1221, 556, 1282, 688), (1354, 550, 1483, 688),
    (1295, 806, 1424, 930), (1146, 803, 1260, 930), (985, 806, 1091, 927),
    (795, 800, 898, 928), (644, 795, 742, 927), (445, 805, 563, 926),
    (269, 795, 380, 927), (95, 806, 221, 928),
]
for i, box in enumerate(ship_roll_boxes):
    x0, y0, x1, y1 = box
    add(f"ship_roll_{i:02d}", ship_master.crop((x0 - 7, y0 - 7, x1 + 7, y1 + 7)), 150, 162)

# Twelve authored assembly pieces, one per generated 4x3 presentation cell.  Piece 07 is the
# corrected dual-laser module: the source's one-sided pod was mirrored and mechanically joined so
# both laser turrets exist throughout the transformation.
parts = rgba("gpt_gravity_ship_components_master.png")
piece_sources: list[Image.Image] = []
for row in range(3):
    for col in range(4):
        index = row * 4 + col
        piece = crop_grid(parts, 4, 3, col, row)
        if index == 7:
            piece = neutral_edge_key(rgba("gpt_dual_laser_component_master.png"))
        piece = contain(trim(piece), 124, 114)
        piece_sources.append(piece)
        add(f"piece_{index:02d}", piece, 124, 114)
        turns, flips = piece_motion_frames(piece)
        for fi, frame in enumerate(turns):
            frames[f"piece_{index:02d}_turn_{fi:02d}"] = frame
        for fi, frame in enumerate(flips):
            frames[f"piece_{index:02d}_flip_{fi:02d}"] = frame

# A canonical thruster plume, duplicated at the ship's two engine ports and
# pulsed into four animation frames.  (The source sheet presents single plumes
# at several authored sizes; runtime needs the actual twin-engine arrangement.)
thr_master = magenta_key(rgba("canonical_fury_thrusters_blue.png"))
thr_single = trim(thr_master.crop((824, 196, 894, 410)))
thr_pair = Image.new("RGBA", (thr_single.width * 2 + 16, thr_single.height), (0, 0, 0, 0))
thr_pair.alpha_composite(thr_single, (0, 0))
thr_pair.alpha_composite(thr_single, (thr_single.width + 16, 0))
for i, (sc, br) in enumerate(((0.78, 0.82), (0.90, 0.95), (1.00, 1.10), (0.88, 0.98))):
    add(f"thruster_{i}", pulse(thr_pair, sc, br), 78, 116)

# Laser Cannon I-V icons.
laser_icons = rgba("gpt_laser_cannon_icons_master.png")
for i in range(5):
    icon = neutral_edge_key(crop_grid(laser_icons, 5, 1, i, 0))
    add(f"laser_icon_{i + 1}", icon, 112, 112)

# Laser Cannon FX: five tier rows, with muzzle, two pulse lengths and four impacts.
laser_fx = rgba("gpt_laser_cannon_fx_master.png")
for tier in range(5):
    row = crop_grid(laser_fx, 1, 5, 0, tier)
    cells = [
        ("muzzle_0", 0.00, 0.12), ("muzzle_1", 0.12, 0.24),
        ("muzzle_2", 0.24, 0.36), ("muzzle_3", 0.36, 0.48),
        ("pulse_short", 0.45, 0.56), ("pulse_long", 0.53, 0.65),
        ("impact_0", 0.63, 0.73), ("impact_1", 0.72, 0.82),
        ("impact_2", 0.81, 0.91), ("impact_3", 0.90, 1.00),
    ]
    for name, xa, xb in cells:
        piece = row.crop((round(row.width * xa), 0, round(row.width * xb), row.height))
        piece = gradient_key(piece, radius=20, threshold=14)
        add(f"laser_{tier + 1}_{name}", piece, 92 if "pulse" not in name else 48, 112)

# Shadow Orb I-V icons and tier-specific generated FX.  Each FX row is:
# charge spark, charge medium, charge full, flight, impact ring, implosion.
shadow_icons = rgba("gpt_shadow_orb_icons_i_v_master.png")
shadow_fx = rgba("gpt_shadow_orb_fx_i_v_master.png")
for tier in range(5):
    add(f"shadow_icon_{tier + 1}", neutral_edge_key(crop_grid(shadow_icons, 5, 1, tier, 0)), 112, 112)
    cells = [neutral_edge_key(crop_grid(shadow_fx, 6, 5, col, tier)) for col in range(6)]
    for fi, src in enumerate(cells[:3]):
        add(f"shadow_{tier + 1}_charge_{fi}", src, 104, 104)
    # The authored flight cell is one projectile pose.  Six subtle squash/pulse frames keep that
    # individual orb animated in motion without turning it into one solid beam graphic.
    flight = contain(trim(cells[3]), 96, 76)
    for fi, (sc, br) in enumerate(((0.90,0.82),(0.96,0.94),(1.00,1.08),(1.04,1.15),(1.00,1.03),(0.95,0.90))):
        add(f"shadow_{tier + 1}_flight_{fi}", pulse(flight, sc, br), 102, 82)
    impact_sources = [cells[4], cells[5]]
    for fi in range(6):
        src = impact_sources[0 if fi < 3 else 1]
        scale = (0.65,0.84,1.00,1.05,0.86,0.60)[fi]
        bright = (0.82,1.00,1.18,1.15,0.94,0.72)[fi]
        add(f"shadow_{tier + 1}_impact_{fi}", pulse(src, scale, bright), 124, 124)

# Volley Missiles I-V.  Every generated tier row is split flash, three independent missiles,
# curved trail, crossing spark, first impact and final impact.
volley_icons = rgba("gpt_volley_missile_icons_i_v_master.png")
volley_fx = rgba("gpt_volley_missile_fx_i_v_master.png")
for tier in range(5):
    add(f"volley_icon_{tier + 1}", neutral_edge_key(crop_grid(volley_icons, 5, 1, tier, 0)), 112, 112)
    cells = [gradient_key(crop_grid(volley_fx, 8, 5, col, tier), 22, 13) for col in range(8)]
    add(f"volley_{tier + 1}_split", cells[0], 128, 112)
    for mi in range(3):
        add(f"volley_{tier + 1}_missile_{mi}", cells[1 + mi], 54, 84)
    for fi, src in enumerate((cells[4], cells[5], cells[4], cells[5])):
        add(f"volley_{tier + 1}_trail_{fi}", pulse(src, 0.88 + fi * 0.055, 0.86 + fi * 0.09), 80, 92)
    for fi in range(6):
        src = cells[6 if fi < 3 else 7]
        add(f"volley_{tier + 1}_impact_{fi}", pulse(src, 0.58 + fi * 0.11, 0.82 + fi * 0.08), 112, 112)


# Add one compact monochrome mask beside every pilot-colourable frame.  The original remains the
# Axel source; runtime overlays only this mask for every other pilot.  This is deliberately done
# after all motion frames exist so turns/flips cannot reveal an untinted blue edge.
palette_keys = [k for k in list(frames) if k == "ship_base" or k.startswith("ship_bank_")
                or k.startswith("ship_roll_")
                or k.startswith("piece_") or k.startswith("thruster_")]
for key in palette_keys:
    mask = blue_mask(frames[key])
    if mask.getchannel("A").getbbox():
        frames[key + "_blue"] = mask


def pack(items: dict[str, Image.Image], atlas_w: int = 4096, pad: int = 4):
    entries: dict[str, dict[str, int]] = {}
    x = y = pad
    shelf_h = 0
    for key, im in sorted(items.items(), key=lambda kv: (-kv[1].height, kv[0])):
        if x + im.width + pad > atlas_w:
            x = pad
            y += shelf_h + pad
            shelf_h = 0
        entries[key] = {"x": x, "y": y, "w": im.width, "h": im.height}
        x += im.width + pad
        shelf_h = max(shelf_h, im.height)
    # Canvas drawImage supports non-power-of-two sources.  Keeping the packed height instead of
    # rounding it to the next power of two avoids allocating several empty megabytes in memory.
    height = max(256, y + shelf_h + pad)
    atlas = Image.new("RGBA", (atlas_w, height), (0, 0, 0, 0))
    for key, rect in entries.items():
        atlas.alpha_composite(items[key], (rect["x"], rect["y"]))
    return atlas, entries


OUT.mkdir(parents=True, exist_ok=True)
PROOF.mkdir(parents=True, exist_ok=True)
atlas, metadata = pack(frames)
atlas.save(ATLAS_PNG, optimize=True)
ATLAS_JSON.write_text(
    json.dumps({"image": ATLAS_PNG.name, "frames": metadata}, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)
ATLAS_JS.write_text(
    "window.BOF_GRAVITY_ATLAS="
    + json.dumps({"image": ATLAS_PNG.name, "frames": metadata}, separators=(",", ":"))
    + ";\n",
    encoding="utf-8",
    newline="\n",
)

# Labelled proof sheet, grouped by atlas order, on a neutral checker for alpha QA.
thumb_w, thumb_h = 184, 168
cols = 6
rows = math.ceil(len(frames) / cols)
proof = Image.new("RGB", (cols * thumb_w, rows * thumb_h + 54), "#10131c")
pd = ImageDraw.Draw(proof)
for y in range(0, proof.height, 16):
    for x in range(0, proof.width, 16):
        if ((x // 16) + (y // 16)) % 2 == 0:
            pd.rectangle((x, y, x + 15, y + 15), fill="#171c28")
pd.rectangle((0, 0, proof.width, 48), fill="#080b12")
pd.text((16, 15), "BULLETS OF FURY - GRAVITY MODE V2 / SPACE WEAPONS ATLAS", fill="#f2b84b")
for idx, key in enumerate(sorted(frames)):
    col, row = idx % cols, idx // cols
    x, y = col * thumb_w, 54 + row * thumb_h
    tile = Image.new("RGBA", (thumb_w, thumb_h - 25), (0, 0, 0, 0))
    item = contain(frames[key], thumb_w - 24, thumb_h - 42)
    tile.alpha_composite(item, ((tile.width - item.width) // 2, (tile.height - item.height) // 2))
    proof.paste(tile.convert("RGB"), (x, y))
    pd.rectangle((x + 4, y + thumb_h - 28, x + thumb_w - 4, y + thumb_h - 5), fill="#080b12")
    pd.text((x + 8, y + thumb_h - 24), key[:27], fill="#e8edf7")
proof.save(PROOF_PNG, optimize=True)

# Compact decision proof: exact blue-only palette contract plus all ten new level icons and one
# representative effect row from each family.  The live browser proof supplies per-pilot colours.
review_keys = (["ship_base", "ship_base_blue"] +
               [f"ship_bank_{side}{i}" for side in ("l", "r") for i in range(1, 4)] +
               ["piece_07", "piece_07_blue"] +
               [f"piece_07_turn_{i:02d}" for i in range(8)] +
               [f"piece_07_flip_{i:02d}" for i in range(8)] +
               [f"shadow_icon_{i}" for i in range(1, 6)] +
               [f"volley_icon_{i}" for i in range(1, 6)] +
               [f"shadow_5_charge_{i}" for i in range(3)] +
               [f"shadow_5_flight_{i}" for i in range(6)] +
               [f"shadow_5_impact_{i}" for i in range(6)] +
               ["volley_5_split"] + [f"volley_5_missile_{i}" for i in range(3)] +
               [f"volley_5_trail_{i}" for i in range(4)] +
               [f"volley_5_impact_{i}" for i in range(6)])
rw, rh, rcols = 160, 154, 6
rrows = math.ceil(len(review_keys) / rcols)
review = Image.new("RGB", (rw * rcols, 48 + rh * rrows), "#10131c")
rd = ImageDraw.Draw(review)
rd.rectangle((0, 0, review.width, 45), fill="#080b12")
rd.text((14, 15), "GRAVITY MODE V3 - BLUE MASK / DUAL LASERS / SHADOW + VOLLEY I-V", fill="#f2b84b")
for idx, key in enumerate(review_keys):
    im = frames.get(key)
    if im is None: continue
    x, y = (idx % rcols) * rw, 48 + (idx // rcols) * rh
    tile = contain(im, rw - 22, rh - 38)
    bg = Image.new("RGBA", (rw, rh - 24), (17, 22, 32, 255))
    bg.alpha_composite(tile, ((rw - tile.width) // 2, (rh - 24 - tile.height) // 2))
    review.paste(bg.convert("RGB"), (x, y))
    rd.rectangle((x + 3, y + rh - 25, x + rw - 3, y + rh - 3), fill="#080b12")
    rd.text((x + 7, y + rh - 22), key[:24], fill="#e8edf7")
review.save(REVIEW_PNG, optimize=True)

print(f"Built {len(frames)} frames")
print(ATLAS_PNG)
print(ATLAS_JSON)
print(ATLAS_JS)
print(PROOF_PNG)
print(REVIEW_PNG)
