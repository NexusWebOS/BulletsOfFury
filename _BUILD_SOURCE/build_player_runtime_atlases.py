#!/usr/bin/env python3
"""Build and register the three production player-art atlases.

The atlases are deliberately named by what the game reads from them:

* ``bof_player_weapon_special_icons.png``
* ``bof_player_ordnance_projectiles.png``
* ``bof_player_ships_barrel_rolls.png``

Every runtime cell keeps its authored natural canvas.  Projectile cells are restored at their
original dimensions and ship cells preserve the original canvas plus trim offset, so moving the
art into a sheet cannot move a muzzle, thruster, bank pivot, or barrel-roll anchor.
"""
from __future__ import annotations

import importlib.util
import json
import math
import re
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "manifest.js"
RUNTIME_DIR = ROOT / "assets" / "game" / "atlas"
DOCS_DIR = ROOT / "docs" / "atlases"

ICON_ATLAS_KEY = "bof_player_weapon_special_icons_atlas"
PROJECTILE_ATLAS_KEY = "bof_player_ordnance_projectiles_atlas"
SHIP_ATLAS_KEY = "bof_player_ships_barrel_rolls_atlas"

ICON_ATLAS = RUNTIME_DIR / "bof_player_weapon_special_icons.png"
PROJECTILE_ATLAS = RUNTIME_DIR / "bof_player_ordnance_projectiles.png"
SHIP_ATLAS = RUNTIME_DIR / "bof_player_ships_barrel_rolls.png"

ICON_META = RUNTIME_DIR / "bof_player_weapon_special_icons.json"
PROJECTILE_META = RUNTIME_DIR / "bof_player_ordnance_projectiles.json"
SHIP_META = RUNTIME_DIR / "bof_player_ships_barrel_rolls.json"

PROJECTILE_PREVIEW = DOCS_DIR / "Bullets_of_Fury_Player_Ordnance_and_Projectiles_Atlas_Labeled.png"
SHIP_PREVIEW = DOCS_DIR / "Bullets_of_Fury_Player_Ships_and_Barrel_Rolls_Atlas_Labeled.png"

PILOTS = ("axel", "cole", "decker", "falva", "freezer", "juggernaut", "lizzie", "maverick", "yuri")
SHIP_SUFFIX_ORDER = ("", "_nf", "_l", "_r", "_pv0", "_pv1", "_pv2", "_pv3", "_pv4",
                     "_br0", "_br1", "_br2", "_br3", "_br4", "_br5", "_br6", "_br7")

ICON_ALIASES = {
    "spicon_axel": "special_icon_axel_mega_shield",
    "spicon_cole": "nsw_icon_cole",
    "spicon_decker": "special_icon_decker_cloaking_system",
    "spicon_falva": "special_icon_falva_roller_ball",
    "spicon_freezer": "special_icon_freezer_time_freeze",
    "spicon_juggernaut": "special_icon_juggernaut_wrecking_ball",
    "spicon_lizzie": "special_icon_lizzie_atom_bomb",
    "spicon_maverick": "special_icon_maverick_helix_beam",
    "spicon_yuri": "special_icon_yuri_chain_lightning",
}

# These keys were packed beside the old ship sheet.  Migrating them lets nca_4.png disappear
# instead of retaining an eleven-megabyte sheet just to keep a warning plate or one beam alive.
NCA4_SUPPORT = (
    "enemy_approaching", "alert_up", "nba_boxpill", "ngm_shock_7",
    "laserbeam_0", "laserbeam_1", "laserbeam_2", "laserbeam_3", "laserbeam_4",
)

PILOT_MISSILES = (
    "msl_2_0", "msl_2_1", "msl_2_2", "msl_2_3", "msl_2_4", "msl_2_5", "mslB_2_2",
    "msl_0_0", "msl_0_1", "msl_0_2", "msl_0_3", "msl_1_1", "msl_1_2", "mslB_0_2",
    "msl_falva", "msl_lizzie",
)

# First-choice art only.  Dead or decode-only fallbacks are intentionally not carried into the
# production sheet: an atlas of bogus alternatives is exactly the sprawl this migration removes.
PLAYER_PROJECTILE_PATTERNS = (
    r"^mgcf_[1-5]_[0-5]$",
    r"^mavlaser_lance_[1-5]$",
    r"^nlz_[1-5]_b[0-5]$",
    r"^nfw_wall_[0-7]$",
    r"^nibr_[0-7]$",
    r"^nts_(?:orb|rel|burst|shard)_\d+$",
    r"^nfb_launch_[0-3]$",
    r"^nfb_orb[1-5]_[0-7]$",
    r"^nfb_fl[1-5]_[0-7]$",
    r"^fireshard_[0-3]$",
    r"^nhxs_[gp]_[smlh]$",
    r"^nhxsb_[gp]_[0-2]$",
    r"^nhxb_[gp]_[0-4]$",
    r"^nhxv_[gp]_[smlh]_\d{2}$",
    r"^nadb_(?:[0-9]|1[01])$",
    r"^fllaser_[0-7]$",
    r"^flspread_[0-7]$",
    r"^chain_bolt_[0-6]$",
    r"^ndk_ang_[0-6]$",
    r"^ndk_trail_[0-3]$",
    r"^nsw_ring_[0-3]$",
    r"^nfrb_[0-3]$",
)

PLAYER_PROJECTILE_EXACT = {
    "nca_87", "fx0825_ice_orb", "fx0825_ice_shard", "lz_bomb", "cole_warhead_A",
    "nlz_slug", "fburst", "eglaser_0", "eglaser_2", *PILOT_MISSILES,
    *NCA4_SUPPORT,
}
PLAYER_PROJECTILE_EXACT.update(f"lz_nuke_{index}" for index in range(4))


def load_icon_builder():
    path = ROOT / "_BUILD_SOURCE" / "build_weapon_special_icon_atlas.py"
    spec = importlib.util.spec_from_file_location("bof_icon_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_manifest() -> tuple[str, dict]:
    text = MANIFEST.read_text(encoding="utf-8")
    match = re.search(r"^window\.BOFX=(.*);$", text, re.MULTILINE)
    if not match:
        raise RuntimeError("window.BOFX assignment not found")
    return text, json.loads(match.group(1))


def save_manifest(container: str, bofx: dict) -> None:
    line = "window.BOFX=" + json.dumps(bofx, separators=(",", ":")) + ";"
    updated, count = re.subn(r"^window\.BOFX=.*;$", lambda _match: line,
                             container, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError("manifest BOFX replacement failed")
    MANIFEST.write_text(updated if updated.endswith("\n") else updated + "\n", encoding="utf-8")


def font(size: int, bold: bool = False):
    for name in (("consolab.ttf", "arialbd.ttf") if bold else ("consola.ttf", "arial.ttf")):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


class SourceBank:
    def __init__(self, bofx: dict):
        self.bofx = bofx
        self.cache: dict[Path, Image.Image] = {}

    def open_path(self, rel: str) -> Image.Image:
        path = ROOT / rel
        if path not in self.cache:
            if not path.exists():
                raise FileNotFoundError(path)
            self.cache[path] = Image.open(path).convert("RGBA")
        return self.cache[path]

    def sheet_key(self, key: str) -> Image.Image:
        rel = self.bofx.get("img", {}).get(key)
        if not rel:
            raise KeyError(f"unregistered sheet key: {key}")
        return self.open_path(rel)

    def xart(self, key: str) -> Image.Image:
        player = self.bofx.get("playercells", {}).get(key)
        if player:
            sheet_key, sx, sy, width, height, dx, dy, canvas_w, canvas_h = player
            crop = self.sheet_key(sheet_key).crop((sx, sy, sx + width, sy + height))
            frame = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
            frame.alpha_composite(crop, (dx, dy))
            return frame

        cell = self.bofx.get("cells", {}).get(key)
        if cell:
            index, sx, sy, width, height = cell[:5]
            sheet = self.open_path(f"assets/game/atlas/nca_{index}.png")
            return sheet.crop((sx, sy, sx + width, sy + height))

        rel = self.bofx.get("img", {}).get(key)
        if rel:
            return self.open_path(rel).copy()

        code_owned = {
            **{f"mgcf_{level}_{frame}": f"assets/game/fx_0825/mg_bullet_{level}_{frame}.png"
               for level in range(1, 6) for frame in range(6)},
            "fx0825_ice_orb": "assets/game/fx_0825/ice_orb.png",
            "fx0825_ice_shard": "assets/game/fx_0825/ice_shard.png",
        }
        if key in code_owned:
            return self.open_path(code_owned[key]).copy()
        for folder in ("assets/game/maverick_laser_icons", "assets/game/special_icons", "assets/game"):
            path = ROOT / folder / f"{key}.png"
            if path.exists():
                return Image.open(path).convert("RGBA")
        raise KeyError(f"unresolved runtime art key: {key}")

    def ship_trim(self, key: str) -> tuple[Image.Image, list[int]]:
        rect = self.bofx.get("ships", {}).get(key)
        if not rect or len(rect) < 8:
            raise KeyError(key)
        sx, sy, width, height, dx, dy, canvas_w, canvas_h = rect[:8]
        sheet_key = self.bofx.get("shipAtlas", "nsa_ships")
        sheet = self.sheet_key(sheet_key)
        return sheet.crop((sx, sy, sx + width, sy + height)), [dx, dy, canvas_w, canvas_h]


def pack_shelves(items: list[tuple[str, Image.Image]], width: int = 4096, pad: int = 4):
    """Deterministic height-sorted shelf pack with transparent safety borders."""
    if not items:
        raise ValueError("cannot pack an empty atlas")
    ordered = sorted(items, key=lambda row: (-row[1].height, -row[1].width, row[0]))
    placements: dict[str, list[int]] = {}
    x = pad
    y = pad
    row_h = 0
    used_w = 0
    for key, image in ordered:
        if image.width + pad * 2 > width:
            raise ValueError(f"{key} is {image.width}px wide and cannot fit a {width}px atlas")
        if x + image.width + pad > width:
            x = pad
            y += row_h + pad * 2
            row_h = 0
        placements[key] = [x, y, image.width, image.height]
        used_w = max(used_w, x + image.width + pad)
        row_h = max(row_h, image.height)
        x += image.width + pad * 2
    used_h = y + row_h + pad
    atlas = Image.new("RGBA", (max(1, used_w), max(1, used_h)), (0, 0, 0, 0))
    lookup = dict(items)
    for key, (sx, sy, _, _) in placements.items():
        atlas.alpha_composite(lookup[key], (sx, sy))
    return atlas, placements


def category_for_projectile(key: str) -> str:
    if key in NCA4_SUPPORT:
        return "runtime_support" if not key.startswith("laserbeam_") else "laser_beams"
    if key == "nca_87" or key.startswith("mgcf_"):
        return "machine_gun_spread"
    if key.startswith("msl"):
        return "pilot_missiles_bombs"
    if key.startswith(("lz_bomb", "lz_nuke_", "cole_warhead")):
        return "pilot_missiles_bombs"
    if key.startswith(("mavlaser_", "nhx", "nlz_", "laserbeam_", "eglaser_", "lzr_")):
        return "laser_helix_projectiles"
    if key.startswith(("nfw_", "nibr_", "nts_", "nfb_", "fireshard_", "fx0825_ice_")):
        return "flame_ice_thermoshock"
    return "pilot_special_projectiles"


def build_icon_runtime(icon_builder, bofx: dict) -> list[dict]:
    source = Image.open(icon_builder.RAW).convert("RGBA")
    source.save(ICON_ATLAS)
    meta = json.loads(icon_builder.META.read_text(encoding="utf-8"))
    entries = []
    by_key = {}
    for row in meta["entries"]:
        key = row["source_key"]
        rect = list(row["content"])
        by_key[key] = rect
        entries.append({"key": key, "id": row["id"], "category": row["category"],
                        "label": row["label"], "rect": rect})

    bofx.setdefault("img", {})[ICON_ATLAS_KEY] = "assets/game/atlas/bof_player_weapon_special_icons.png"
    icons = bofx.setdefault("icons", {})
    for row in entries:
        rect = row["rect"] + [ICON_ATLAS_KEY]
        icons[row["key"]] = rect
        icons[row["id"]] = rect
    for alias, target in ICON_ALIASES.items():
        icons[alias] = by_key[target] + [ICON_ATLAS_KEY]

    # No active icon may fall back to the two old icon-sheet locations.
    bofx.get("cells", {}).pop("nia_icons", None)
    bofx.get("img", {}).pop("nia_icons", None)
    bofx.get("img", {}).pop("nia_icons2", None)
    for key in set(by_key) | set(ICON_ALIASES):
        if key != ICON_ATLAS_KEY:
            bofx.get("img", {}).pop(key, None)

    ICON_META.write_text(json.dumps({
        "format": "coleforge.player-icon-atlas.v1",
        "atlas_key": ICON_ATLAS_KEY,
        "atlas": ICON_ATLAS.name,
        "size": list(source.size),
        "count": len(entries),
        "aliases": ICON_ALIASES,
        "entries": entries,
    }, indent=2), encoding="utf-8")
    return entries


def projectile_keys(bofx: dict) -> list[str]:
    known = set(bofx.get("img", {})) | set(bofx.get("cells", {})) | set(bofx.get("playercells", {}))
    known.update(PLAYER_PROJECTILE_EXACT)
    known.update(f"mgcf_{level}_{frame}" for level in range(1, 6) for frame in range(6))
    known.update(f"mavlaser_lance_{level}" for level in range(1, 6))
    patterns = [re.compile(pattern) for pattern in PLAYER_PROJECTILE_PATTERNS]
    return sorted(key for key in known if key in PLAYER_PROJECTILE_EXACT or any(p.match(key) for p in patterns))


def build_projectile_runtime(bank: SourceBank, bofx: dict) -> list[dict]:
    images = []
    missing = []
    for key in projectile_keys(bofx):
        try:
            image = bank.xart(key)
        except (KeyError, FileNotFoundError):
            missing.append(key)
            continue
        if image.getchannel("A").getbbox() is None:
            missing.append(key)
            continue
        images.append((key, image))
    if missing:
        raise RuntimeError("active player projectile art missing: " + ", ".join(missing))

    # 3840 is the smallest-area legal layout for the current 505-frame production set while
    # remaining below the 4096px texture-height gate (about 1.7% less decoded surface than 4096).
    atlas, placements = pack_shelves(images, width=3840, pad=4)
    if atlas.height > 4096:
        raise RuntimeError(f"projectile atlas is {atlas.size}; active set exceeds the 4096px texture gate")
    atlas.save(PROJECTILE_ATLAS)

    bofx.setdefault("img", {})[PROJECTILE_ATLAS_KEY] = "assets/game/atlas/bof_player_ordnance_projectiles.png"
    playercells = bofx.setdefault("playercells", {})
    entries = []
    for key, image in images:
        sx, sy, width, height = placements[key]
        playercells[key] = [PROJECTILE_ATLAS_KEY, sx, sy, width, height, 0, 0, width, height]
        bofx.setdefault("img", {})[key] = "assets/game/atlas/bof_player_ordnance_projectiles.png"
        bofx.get("cells", {}).pop(key, None)
        entries.append({"key": key, "category": category_for_projectile(key),
                        "rect": [sx, sy, width, height], "canvas": [width, height]})

    counts = {name: sum(1 for row in entries if row["category"] == name)
              for name in sorted({row["category"] for row in entries})}
    PROJECTILE_META.write_text(json.dumps({
        "format": "coleforge.player-ordnance-projectile-atlas.v1",
        "atlas_key": PROJECTILE_ATLAS_KEY,
        "atlas": PROJECTILE_ATLAS.name,
        "size": list(atlas.size),
        "count": len(entries),
        "counts": counts,
        "entries": entries,
    }, indent=2), encoding="utf-8")
    build_contact_preview("BULLETS OF FURY — PLAYER ORDNANCE + PROJECTILES",
                          atlas, entries, PROJECTILE_PREVIEW, exclude_categories={"runtime_support"})
    return entries


def restore_ship(trim: Image.Image, frame_meta: list[int]) -> Image.Image:
    dx, dy, canvas_w, canvas_h = frame_meta
    frame = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    frame.alpha_composite(trim, (dx, dy))
    return frame


def build_ship_runtime(bank: SourceBank, bofx: dict) -> list[dict]:
    trims = []
    frame_meta = {}
    for pilot in PILOTS:
        for suffix in SHIP_SUFFIX_ORDER:
            key = f"ship_{pilot}{suffix}"
            trim, meta = bank.ship_trim(key)
            if trim.getchannel("A").getbbox() is None:
                raise RuntimeError(f"empty ship frame: {key}")
            trims.append((key, trim))
            frame_meta[key] = meta

    # The 3584-wide shelf packs to 3530x1605, 11.5% less decoded surface than the naive
    # 4096-wide layout while
    # retaining six transparent pixels around every trimmed frame.
    atlas, placements = pack_shelves(trims, width=3584, pad=6)
    if atlas.height > 4096:
        raise RuntimeError(f"ship atlas is {atlas.size}; frames exceed the 4096px texture gate")
    atlas.save(SHIP_ATLAS)

    bofx.setdefault("img", {})[SHIP_ATLAS_KEY] = "assets/game/atlas/bof_player_ships_barrel_rolls.png"
    bofx["shipAtlas"] = SHIP_ATLAS_KEY
    new_ships = {}
    entries = []
    for key, trim in trims:
        sx, sy, width, height = placements[key]
        dx, dy, canvas_w, canvas_h = frame_meta[key]
        new_ships[key] = [sx, sy, width, height, dx, dy, canvas_w, canvas_h]
        entries.append({"key": key, "pilot": key.split("_")[1],
                        "kind": "barrel_roll" if "_br" in key else "flight",
                        "rect": [sx, sy, width, height], "offset": [dx, dy],
                        "canvas": [canvas_w, canvas_h]})
    bofx["ships"] = new_ships
    # Keep the historical preload key as an alias while the runtime names the sheet explicitly.
    bofx.setdefault("img", {})["nsa_ships"] = "assets/game/atlas/bof_player_ships_barrel_rolls.png"

    SHIP_META.write_text(json.dumps({
        "format": "coleforge.player-ship-barrel-roll-atlas.v1",
        "atlas_key": SHIP_ATLAS_KEY,
        "atlas": SHIP_ATLAS.name,
        "size": list(atlas.size),
        "count": len(entries),
        "pilots": len(PILOTS),
        "frames_per_pilot": len(SHIP_SUFFIX_ORDER),
        "entries": entries,
    }, indent=2), encoding="utf-8")
    build_ship_preview(atlas, entries)
    return entries


def build_contact_preview(title: str, atlas: Image.Image, entries: list[dict], path: Path,
                          exclude_categories: set[str] | None = None) -> None:
    exclude_categories = exclude_categories or set()
    rows = [row for row in entries if row.get("category") not in exclude_categories]
    cols, cell_w, cell_h, title_h = 8, 180, 158, 58
    canvas = Image.new("RGBA", (cols * cell_w, title_h + math.ceil(len(rows) / cols) * cell_h),
                       (12, 14, 20, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((16, 12), title, fill=(255, 211, 107), font=font(22, True))
    draw.text((16, 38), f"{len(rows)} ACTIVE FRAMES — RUNTIME ATLAS CELLS",
              fill=(148, 170, 198), font=font(12))
    for index, row in enumerate(rows):
        col, r = index % cols, index // cols
        x, y = col * cell_w, title_h + r * cell_h
        draw.rectangle((x + 4, y + 4, x + cell_w - 5, y + cell_h - 5),
                       fill=(18, 22, 31), outline=(68, 118, 174), width=1)
        sx, sy, width, height = row["rect"]
        image = atlas.crop((sx, sy, sx + width, sy + height))
        image.thumbnail((cell_w - 22, cell_h - 42), Image.Resampling.NEAREST)
        canvas.alpha_composite(image, (x + (cell_w - image.width) // 2, y + 10))
        label = row["key"] if len(row["key"]) <= 25 else row["key"][:24] + "…"
        draw.text((x + 7, y + cell_h - 23), label, fill=(230, 236, 247), font=font(10))
    canvas.convert("RGB").save(path, quality=94)


def build_ship_preview(atlas: Image.Image, entries: list[dict]) -> None:
    by_pilot = defaultdict(list)
    for row in entries:
        by_pilot[row["pilot"]].append(row)
    cols, cell_w, cell_h, heading_h, title_h = 9, 150, 168, 30, 58
    rows_per_pilot = math.ceil(len(SHIP_SUFFIX_ORDER) / cols)
    width = cols * cell_w
    height = title_h + len(PILOTS) * (heading_h + rows_per_pilot * cell_h)
    canvas = Image.new("RGBA", (width, height), (12, 14, 20, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((16, 12), "BULLETS OF FURY — PLAYER SHIPS + BARREL ROLLS",
              fill=(255, 211, 107), font=font(22, True))
    draw.text((16, 38), "9 PILOTS • 17 FULL-CANVAS FRAMES EACH • PADDED ATLAS CELLS",
              fill=(148, 170, 198), font=font(12))
    y = title_h
    for pilot in PILOTS:
        draw.text((12, y + 7), pilot.upper(), fill=(116, 202, 255), font=font(15, True))
        y += heading_h
        lookup = {row["key"]: row for row in by_pilot[pilot]}
        for index, suffix in enumerate(SHIP_SUFFIX_ORDER):
            row = lookup[f"ship_{pilot}{suffix}"]
            col, rr = index % cols, index // cols
            x, cy = col * cell_w, y + rr * cell_h
            draw.rectangle((x + 4, cy + 4, x + cell_w - 5, cy + cell_h - 5),
                           fill=(18, 22, 31), outline=(55, 72, 96), width=1)
            sx, sy, width2, height2 = row["rect"]
            trim = atlas.crop((sx, sy, sx + width2, sy + height2))
            full = restore_ship(trim, row["offset"] + row["canvas"])
            full.thumbnail((cell_w - 18, cell_h - 34), Image.Resampling.NEAREST)
            canvas.alpha_composite(full, (x + (cell_w - full.width) // 2, cy + 8))
            label = "idle" if not suffix else suffix[1:]
            draw.text((x + 7, cy + cell_h - 21), label, fill=(226, 232, 244), font=font(10))
        y += rows_per_pilot * cell_h
    canvas.convert("RGB").save(SHIP_PREVIEW, quality=94)


def prune_superseded_runtime_files() -> list[str]:
    exact = [
        ROOT / "assets" / "game" / "nia_icons2.png",
        *(ROOT / "assets" / "game" / f"micon_thermoshock_{tier}.png" for tier in range(1, 6)),
        *(ROOT / "assets" / "game" / "maverick_laser_icons" / f"micon_maverick_laser_{tier}.png" for tier in range(1, 6)),
        *(ROOT / "assets" / "game" / "maverick_laser_icons" / f"mavlaser_lance_{tier}.png" for tier in range(1, 6)),
        *(ROOT / "assets" / "game" / "special_icons" / f"{key}.png" for key in (
            "special_icon_axel_mega_shield", "special_icon_freezer_time_freeze",
            "special_icon_freezer_thermoshock", "special_icon_juggernaut_wrecking_ball",
            "special_icon_maverick_helix_beam", "special_icon_lizzie_atom_bomb",
            "special_icon_falva_roller_ball", "special_icon_cole_nuclear_warheads",
            "special_icon_decker_cloaking_system", "special_icon_yuri_chain_lightning",
        )),
        ROOT / "assets" / "game" / "fx_0825" / "ice_orb.png",
        ROOT / "assets" / "game" / "fx_0825" / "ice_shard.png",
    ]
    removed = []
    for path in exact:
        if path.exists():
            path.unlink()
            removed.append(str(path.relative_to(ROOT)))
    return removed


def nca4_is_unreferenced(bofx: dict) -> bool:
    old = "assets/game/atlas/nca_4.png"
    if any(value == old for value in bofx.get("img", {}).values()):
        return False
    if any(row and row[0] == 4 for row in bofx.get("cells", {}).values()):
        return False
    return True


def main() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    icon_builder = load_icon_builder()
    icon_builder.main()

    container, bofx = load_manifest()
    bank = SourceBank(bofx)
    icon_entries = build_icon_runtime(icon_builder, bofx)
    projectile_entries = build_projectile_runtime(bank, bofx)
    ship_entries = build_ship_runtime(bank, bofx)

    # The direct runtime maps win before BOFX.cells, so old cell registrations can now go.
    for key in (*NCA4_SUPPORT, "nsa_ships"):
        bofx.get("cells", {}).pop(key, None)
    bofx.get("img", {}).pop("nca_4", None)
    save_manifest(container, bofx)

    # Only prune after all three atlases, their metadata, and the rewritten manifest exist.
    removed = prune_superseded_runtime_files()
    old_nca4 = ROOT / "assets" / "game" / "atlas" / "nca_4.png"
    if old_nca4.exists() and nca4_is_unreferenced(bofx):
        old_nca4.unlink()
        removed.append(str(old_nca4.relative_to(ROOT)))

    print(f"icons: {len(icon_entries)} -> {ICON_ATLAS.relative_to(ROOT)}")
    print(f"projectiles/support: {len(projectile_entries)} -> {PROJECTILE_ATLAS.relative_to(ROOT)}")
    print(f"ships: {len(ship_entries)} -> {SHIP_ATLAS.relative_to(ROOT)}")
    print(f"removed superseded runtime files: {len(removed)}")
    for path in removed:
        print(f"  removed {path}")


if __name__ == "__main__":
    main()
