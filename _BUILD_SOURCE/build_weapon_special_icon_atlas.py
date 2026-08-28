#!/usr/bin/env python3
"""Build the complete active weapon/special icon atlas and a labelled review sheet.

Outputs:
  docs/atlases/Bullets_of_Fury_Player_Weapon_and_Special_Icon_Atlas.png
  docs/atlases/Bullets_of_Fury_Player_Weapon_and_Special_Icon_Atlas.json
  docs/atlases/Bullets_of_Fury_Player_Weapon_and_Special_Icon_Atlas_Labeled.png

Only active production icon families are included. The special-ability section uses the
original animated ``sp_<pilot>_<frame>`` icons, not the smaller ``spicon_<pilot>`` glyphs
extracted from inside the newer power-up boxes.
"""
import json
import math
import os
import re
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "manifest.js"
OUT = ROOT / "docs" / "atlases"
RAW = OUT / "Bullets_of_Fury_Player_Weapon_and_Special_Icon_Atlas.png"
META = OUT / "Bullets_of_Fury_Player_Weapon_and_Special_Icon_Atlas.json"
PREVIEW = OUT / "Bullets_of_Fury_Player_Weapon_and_Special_Icon_Atlas_Labeled.png"
GEN_REF = ROOT / "docs" / "proofs" / "Special_Icon_Generation_Reference.png"
SPECIAL_DIR = ROOT / "assets" / "game" / "special_icons"
MAVERICK_LASER_DIR = ROOT / "assets" / "game" / "maverick_laser_icons"

SPECIAL_MASTERS = {
    "special_icon_axel_mega_shield": "special_axel_mega_shield_v2.png",
    "special_icon_freezer_time_freeze": "special_freezer_time_freeze_v2.png",
    "special_icon_freezer_thermoshock": "special_freezer_thermoshock_v2.png",
    "special_icon_juggernaut_wrecking_ball": "special_juggernaut_wrecking_ball_v2.png",
    "special_icon_maverick_helix_beam": "special_maverick_helix_beam_v2.png",
    "special_icon_lizzie_atom_bomb": "special_lizzie_atom_bomb_v2.png",
    "special_icon_falva_roller_ball": "special_falva_roller_ball_v2.png",
    "special_icon_cole_nuclear_warheads": "special_cole_nuclear_warheads_v2.png",
    "special_icon_decker_cloaking_system": "special_decker_cloaking_system_v2.png",
    "special_icon_yuri_chain_lightning": "special_yuri_chain_lightning_v2.png",
}

MAVERICK_ICON_MASTERS = {
    tier: f"maverick_icon_tier{tier}_master_v2.png" for tier in range(1, 6)
}
MAVERICK_ICON_MASTERS[5] = "maverick_icon_tier5_master_v3.png"
MAVERICK_LANCE_MASTERS = {
    tier: f"mavlaser_lance_tier{tier}_master.png" for tier in range(1, 6)
}

CELL = 128
INNER = 112
COLS = 8


def load_manifest():
    text = MANIFEST.read_text(encoding="utf-8")
    match = re.search(r"^window\.BOFX=(.*);$", text, re.MULTILINE)
    if not match:
        raise RuntimeError("window.BOFX assignment not found in manifest")
    return json.loads(match.group(1))


BOFX = load_manifest()
_cache = {}


def open_rgba(rel):
    path = ROOT / rel
    if path not in _cache:
        _cache[path] = Image.open(path).convert("RGBA")
    return _cache[path]


def xart_source(key):
    """Resolve one XART key, including a named sheet nested inside nca_N.png."""
    playercells = BOFX.get("playercells", {})
    cells = BOFX.get("cells", {})
    images = BOFX.get("img", {})
    if key in playercells:
        sheet_key, x, y, w, h, dx, dy, canvas_w, canvas_h = playercells[key]
        sheet = open_rgba(images[sheet_key])
        frame = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        frame.alpha_composite(sheet.crop((x, y, x + w, y + h)), (dx, dy))
        return frame
    if key in cells:
        sheet_index, x, y, w, h = cells[key][:5]
        sheet = open_rgba(f"assets/game/atlas/nca_{sheet_index}.png")
        return sheet.crop((x, y, x + w, y + h))
    if key in images:
        return open_rgba(images[key]).copy()
    raise KeyError(f"unresolved XART source: {key}")


def source_icon(key):
    """Resolve a key through the same priority as the live icon/XART paths."""
    # Generated production plates win over a previously-built runtime atlas.  This makes a
    # rebuild pick up a changed master immediately instead of reading yesterday's packed cell.
    generated = SPECIAL_DIR / f"{key}.png"
    if generated.exists():
        return Image.open(generated).convert("RGBA")
    maverick_laser = MAVERICK_LASER_DIR / f"{key}.png"
    if maverick_laser.exists():
        return Image.open(maverick_laser).convert("RGBA")
    loose = ROOT / "assets" / "game" / f"{key}.png"
    if loose.exists() and (key.startswith("micon_thermoshock_") or key.startswith("special_icon_")):
        return Image.open(loose).convert("RGBA")
    icons = BOFX.get("icons", {})
    if key in icons:
        rect = icons[key]
        sheet_key = rect[4] if len(rect) > 4 else "nia_icons"
        sheet = xart_source(sheet_key)
        x, y, w, h = rect[:4]
        return sheet.crop((x, y, x + w, y + h))
    try:
        return xart_source(key)
    except KeyError:
        pass
    loose = ROOT / "assets" / "game" / f"{key}.png"
    if loose.exists():
        return Image.open(loose).convert("RGBA")
    raise KeyError(f"unresolved icon source: {key}")


def entries():
    out = []
    families = [
        ("MACHINE GUN", "micon_mg", 8),
        ("SPREAD FIRE", "micon_spread", 5),
        ("AUTO MISSILES", "micon_missile", 5),
        ("LASER BEAM", "micon_laser", 5),
        ("MAVERICK HOMING LASER", "micon_maverick_laser", 5),
        ("FLAMETHROWER", "micon_firewall", 5),
        ("ICE BREATH", "micon_icebreath", 5),
        ("ICE ORB", "micon_iceorb", 5),
        ("FIRE ORB", "micon_fireorb", 5),
        ("THERMOSHOCK", "micon_thermoshock", 5),
    ]
    for label, prefix, count in families:
        for level in range(1, count + 1):
            out.append({"id": f"{prefix}_{level}", "source_key": f"{prefix}_{level}",
                        "category": "weapon", "label": f"{label} L{level}"})

    for ident, key, pilot, label, kind in [
        ("special_axel_mega_shield", "special_icon_axel_mega_shield", "axel", "AXEL — MEGA SHIELD", "generated_powerup"),
        ("special_freezer_time_freeze", "special_icon_freezer_time_freeze", "freezer", "FREEZER — TIME FREEZE", "generated_powerup"),
        ("special_freezer_thermoshock", "special_icon_freezer_thermoshock", "freezer", "FREEZER — THERMOSHOCK", "generated_powerup"),
        ("special_juggernaut_wrecking_ball", "special_icon_juggernaut_wrecking_ball", "juggernaut", "JUGGERNAUT — WRECKING BALL", "generated_powerup"),
        ("special_maverick_helix_beam", "special_icon_maverick_helix_beam", "maverick", "MAVERICK — HELIX BEAM", "generated_powerup"),
        ("special_lizzie_atom_bomb", "special_icon_lizzie_atom_bomb", "lizzie", "LIZZIE — ATOM BOMB", "generated_powerup"),
        ("special_falva_roller_ball", "special_icon_falva_roller_ball", "falva", "FALVA — ROLLER BALL", "generated_powerup"),
        ("special_cole_nuclear_warheads", "special_icon_cole_nuclear_warheads", "cole", "COLE — NUCLEAR WARHEADS", "generated_powerup"),
        ("special_decker_cloaking_system", "special_icon_decker_cloaking_system", "decker", "DECKER — CLOAKING SYSTEM", "generated_powerup"),
        ("special_yuri_chain_lightning", "special_icon_yuri_chain_lightning", "yuri", "YURI — CHAIN LIGHTNING", "generated_powerup"),
        ("special_cole_sonic_boom", "nsw_icon_cole", "cole", "COLE — SONIC BOOM", "approved_powerup"),
        ("special_decker_shotgun", "nsw_icon_decker", "decker", "DECKER — INCENDIARY SHOTGUN", "approved_powerup"),
        ("special_lizzie_heavy_gun", "nsw_icon_lizzie", "lizzie", "LIZZIE — HEAVY MACHINE GUN / TURRET", "approved_powerup"),
    ]:
        out.append({"id": ident, "source_key": key, "category": "special",
                    "kind": kind, "pilot": pilot, "label": label})
    return out


def fit_icon(im):
    im = im.copy()
    im.thumbnail((INNER, INNER), Image.Resampling.LANCZOS)
    return im


def font(size, bold=False):
    names = ["consolab.ttf" if bold else "consola.ttf", "arialbd.ttf" if bold else "arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def wrapped(text, width=24):
    words, lines, cur = text.split(), [], ""
    for word in words:
        nxt = word if not cur else cur + " " + word
        if len(nxt) <= width:
            cur = nxt
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines[:3]


def write_generation_reference():
    """Export exact approved icon anchors plus the live Thermoshock orb for image generation."""
    keys = ("nsw_icon_cole", "nsw_icon_decker", "nsw_icon_lizzie", "nts_orb_0")
    cell = 240
    ref = Image.new("RGBA", (cell * len(keys), cell), (0, 0, 0, 0))
    for index, key in enumerate(keys):
        im = source_icon(key).copy()
        im.thumbnail((200, 200), Image.Resampling.LANCZOS)
        ref.alpha_composite(im, (index * cell + (cell - im.width) // 2, (cell - im.height) // 2))
    GEN_REF.parent.mkdir(parents=True, exist_ok=True)
    ref.save(GEN_REF)


def normalize_generated_specials():
    """Keep generation masters, but ship compact 160px plates beside them."""
    SPECIAL_DIR.mkdir(parents=True, exist_ok=True)
    for key, master_name in SPECIAL_MASTERS.items():
        master_path = SPECIAL_DIR / master_name
        if not master_path.exists():
            raise FileNotFoundError(master_path)
        im = Image.open(master_path).convert("RGBA")
        alpha = im.getchannel("A")
        box = alpha.getbbox()
        if box:
            im = im.crop(box)
        im.thumbnail((152, 152), Image.Resampling.LANCZOS)
        plate = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        plate.alpha_composite(im, ((160 - im.width) // 2, (160 - im.height) // 2))
        plate.save(SPECIAL_DIR / f"{key}.png")


def clear_edge_neutral_background(image):
    """Remove an edge-connected generated white/checkerboard field without touching the badge.

    Some generated masters arrived with a flattened transparency preview.  Flood-filling only
    neutral bright pixels reachable from the canvas edge preserves enclosed white energy cores,
    Roman numerals and metal highlights while restoring an actual transparent exterior.
    """
    image = image.convert("RGBA")
    if image.getchannel("A").getextrema()[0] < 255:
        return image
    width, height = image.size
    pixels = image.load()
    seen = set()
    queue = deque()

    def neutral_bright(x, y):
        r, g, b, _ = pixels[x, y]
        return min(r, g, b) >= 205 and max(r, g, b) - min(r, g, b) <= 20

    for x in range(width):
        for y in (0, height - 1):
            if neutral_bright(x, y):
                seen.add((x, y)); queue.append((x, y))
    for y in range(height):
        for x in (0, width - 1):
            if neutral_bright(x, y) and (x, y) not in seen:
                seen.add((x, y)); queue.append((x, y))
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in seen and neutral_bright(nx, ny):
                seen.add((nx, ny)); queue.append((nx, ny))
    for x, y in seen:
        r, g, b, _ = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)
    return image


def normalize_maverick_laser_icons():
    """Normalize five complete, original Maverick badges—no borrowed tier shells."""
    MAVERICK_LASER_DIR.mkdir(parents=True, exist_ok=True)
    for tier, master_name in MAVERICK_ICON_MASTERS.items():
        master_path = MAVERICK_LASER_DIR / master_name
        if not master_path.exists():
            raise FileNotFoundError(master_path)

        master = clear_edge_neutral_background(Image.open(master_path))
        alpha_box = master.getchannel("A").getbbox()
        if alpha_box:
            master = master.crop(alpha_box)

        master.thumbnail((154, 154), Image.Resampling.LANCZOS)
        plate = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        plate.alpha_composite(master, ((160 - master.width) // 2, (160 - master.height) // 2))
        plate.save(MAVERICK_LASER_DIR / f"micon_maverick_laser_{tier}.png")


def normalize_maverick_projectiles():
    """Normalize one isolated lance per tier; composite volley art is UI-only."""
    for tier, master_name in MAVERICK_LANCE_MASTERS.items():
        master = Image.open(MAVERICK_LASER_DIR / master_name).convert("RGBA")
        alpha_box = master.getchannel("A").getbbox()
        if alpha_box:
            master = master.crop(alpha_box)
        master.thumbnail((96, 144), Image.Resampling.LANCZOS)
        sprite = Image.new("RGBA", (112, 160), (0, 0, 0, 0))
        sprite.alpha_composite(master, ((112 - master.width) // 2, (160 - master.height) // 2))
        sprite.save(MAVERICK_LASER_DIR / f"mavlaser_lance_{tier}.png")


def rebuild_thermoshock_tiers():
    """Replace the broken split-sphere centers with the exact live radial Thermoshock orb."""
    orb = source_icon("nts_orb_0").copy()
    box = orb.getchannel("A").getbbox()
    if box:
        orb = orb.crop(box)
    orb.thumbnail((72, 72), Image.Resampling.LANCZOS)
    for tier in range(1, 6):
        path = ROOT / "assets" / "game" / f"micon_thermoshock_{tier}.png"
        # Start from a clean tier-matched hex plate.  The former Thermoshock loose files were
        # flattened composites and left UI/debug pixels around the orb even after its center
        # was repaired.  Reusing only the authored Fire Orb rim gives Thermoshock the same
        # progression language while the live radial orb remains its own unmistakable art.
        rim = source_icon(f"micon_fireorb_{tier}").copy()
        rim.thumbnail((152, 152), Image.Resampling.LANCZOS)
        plate = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        plate.alpha_composite(rim, ((160 - rim.width) // 2, (160 - rim.height) // 2))
        draw = ImageDraw.Draw(plate)
        draw.polygon(((80, 34), (120, 56), (120, 100), (106, 109),
                      (54, 109), (40, 100), (40, 56)), fill=(2, 7, 18, 255))
        plate.alpha_composite(orb, ((160 - orb.width) // 2, 39 + (72 - orb.height) // 2))
        plate.save(path)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    write_generation_reference()
    normalize_generated_specials()
    normalize_maverick_projectiles()
    normalize_maverick_laser_icons()
    rebuild_thermoshock_tiers()
    rows = entries()
    nrows = math.ceil(len(rows) / COLS)
    atlas = Image.new("RGBA", (COLS * CELL, nrows * CELL), (0, 0, 0, 0))
    packed = []
    for index, row in enumerate(rows):
        im = fit_icon(source_icon(row["source_key"]))
        col, r = index % COLS, index // COLS
        x, y = col * CELL, r * CELL
        atlas.alpha_composite(im, (x + (CELL - im.width) // 2, y + (CELL - im.height) // 2))
        packed.append({**row, "rect": [x, y, CELL, CELL], "content": [
            x + (CELL - im.width) // 2, y + (CELL - im.height) // 2, im.width, im.height
        ]})
    atlas.save(RAW)

    counts = {kind: sum(1 for row in packed if row["category"] == kind)
              for kind in ("weapon", "special")}
    counts["pilots"] = len({row["pilot"] for row in packed if row["category"] == "special"})
    counts["generated_powerups"] = sum(1 for row in packed if row.get("kind") == "generated_powerup")
    counts["approved_powerups"] = sum(1 for row in packed if row.get("kind") == "approved_powerup")
    META.write_text(json.dumps({
        "atlas": RAW.name, "cell_size": CELL, "columns": COLS, "rows": nrows,
        "counts": counts, "entries": packed
    }, indent=2), encoding="utf-8")

    pw, ph = 176, 184
    title_h = 72
    preview = Image.new("RGBA", (COLS * pw, title_h + nrows * ph), (12, 14, 20, 255))
    draw = ImageDraw.Draw(preview)
    draw.text((18, 13), "BULLETS OF FURY — COMPLETE WEAPON + SPECIAL ICON ATLAS",
              fill=(255, 211, 107), font=font(23, True))
    draw.text((18, 43), f"{counts['weapon']} WEAPON TIERS  •  {counts['special']} WEAPON-READABLE SPECIAL POWERUPS  •  {counts['pilots']} PILOTS",
              fill=(150, 170, 198), font=font(14))
    category_color = {"weapon": (85, 126, 174), "special": (202, 122, 42)}
    for index, row in enumerate(packed):
        col, r = index % COLS, index // COLS
        x, y = col * pw, title_h + r * ph
        edge = category_color[row["category"]]
        draw.rectangle((x + 5, y + 5, x + pw - 6, y + ph - 6), fill=(18, 22, 31), outline=edge, width=2)
        sx, sy, sw, sh = row["rect"]
        cell = atlas.crop((sx, sy, sx + sw, sy + sh))
        preview.alpha_composite(cell, (x + (pw - CELL) // 2, y + 9))
        for li, line in enumerate(wrapped(row["label"], 20)):
            box = draw.textbbox((0, 0), line, font=font(12, li == 0))
            tw = box[2] - box[0]
            draw.text((x + (pw - tw) // 2, y + 137 + li * 14), line,
                      fill=(236, 240, 248), font=font(12, li == 0))
    preview.convert("RGB").save(PREVIEW, quality=95)

    print(f"packed {len(packed)} icons -> {RAW.relative_to(ROOT)}")
    print(f"metadata -> {META.relative_to(ROOT)}")
    print(f"labelled preview -> {PREVIEW.relative_to(ROOT)}")
    print("counts", counts)


if __name__ == "__main__":
    main()
