"""Pack modern per-stage loose combat reels into bounded 4096x4096 runtime atlases.

Editable source PNGs remain untouched. The emitted JS table lets XART resolve every logical frame
to a stage-owned sheet and release that sheet when the next mission begins.
"""
from pathlib import Path
import json
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "assets" / "game"
OUTDIR = GAME / "atlas" / "stage_runtime"
MAP = GAME / "atlas" / "stage_runtime_atlases.js"
MAX = 4096
PAD = 4


def numbered(directory, prefix):
    out = []
    for unit in sorted(directory.iterdir()):
        if not unit.is_dir():
            continue
        for i, src in enumerate(sorted(unit.glob("*.png"))):
            out.append((f"{prefix}{unit.name}_{i}", src))
    return out


def stage_items(stage):
    out = []
    if stage == 2:
        out += numbered(GAME / "stage2_enemy_attacks", "s2atk_")
        for src in sorted((GAME / "stage2_magmaward").glob("*.png")):
            m = re.match(r"magmaward_(.+)_(\d+)$", src.stem)
            if m:
                out.append((f"mwfx_{m.group(1)}_{int(m.group(2))}", src))
        for src in sorted((GAME / "boss_projectiles_stage2_stage3").glob("*.png")):
            m = re.match(r"(.+)_(\d+)$", src.stem)
            if m:
                out.append((f"l23fx_{m.group(1)}_{int(m.group(2))}", src))
    elif stage == 3:
        out += numbered(GAME / "stage3_enemy_attacks", "s3atk_")
        for unit in sorted((GAME / "stage3_enemy_damage").iterdir()):
            if not unit.is_dir():
                continue
            for state in sorted(unit.iterdir()):
                if not state.is_dir():
                    continue
                for i, src in enumerate(sorted(state.glob("*.png"))):
                    out.append((f"s3dmg_{unit.name}_{state.name}_{i}", src))
    elif stage == 4:
        out += numbered(GAME / "stage4_enemy_attacks", "s4atk_")
        for src in sorted((GAME / "stage4_warfare").glob("s4w_*.png")):
            m = re.match(r"(.+)_([0-9]+)$", src.stem)
            out.append(((f"{m.group(1)}_{int(m.group(2))}" if m else src.stem), src))
    elif stage == 6:
        out += numbered(GAME / "stage6_enemy_attacks", "s6atk_")
        for src in sorted((GAME / "stage6_mega_boss").glob("*.png")):
            m = re.match(r"(.+)_f(\d+)-frame_\d+$", src.stem)
            if m:
                out.append((f"s6mb_{m.group(1)}_{int(m.group(2))-1}", src))
        out += [(src.stem, src) for src in sorted((GAME / "l6_fleet").glob("n6v*.png"))]
    elif stage == 7:
        out += numbered(GAME / "stage7_enemy_attacks", "s7atk_")
        out += [(f"s7spore_{i}", src) for i, src in enumerate(sorted((GAME / "stage7_spore_crown").glob("*.png")))]
    elif stage == 8:
        for unit in sorted((GAME / "stage8_mega_enemies").iterdir()):
            if not unit.is_dir():
                continue
            for mode, prefix in (("attack", "s8atk_"), ("roll", "s8roll_")):
                for i, src in enumerate(sorted(unit.glob(f"{mode}_*.png"))):
                    out.append((f"{prefix}{unit.name}_{i}", src))
        for unit in sorted((GAME / "stage8_symbiote_fleet").iterdir()):
            if not unit.is_dir():
                continue
            idle = unit / "idle.png"
            if idle.exists():
                out.append((f"s8nf_{unit.name}_idle", idle))
            for mode in ("muzzle", "projectile"):
                for i, src in enumerate(sorted(unit.glob(f"{mode}_*.png"))):
                    out.append((f"s8nf_{unit.name}_{mode}_{i}", src))
        out += [(f"s8symboss_entrance_{i}", src) for i, src in enumerate(sorted((GAME / "stage8_symbiote_boss").glob("entrance_*.png")))]
        out += [(f"s8symboss_form_{i}", src) for i, src in enumerate(sorted((GAME / "stage8_symbiote_boss").glob("form_*.png")))]
        out += [(f"s8rift_{i}", src) for i, src in enumerate(sorted((GAME / "stage8_furious_rift").glob("[0-9][0-9].png")))]
        hd = GAME / "herald_of_death"
        for action, count in (("idle", 6), ("movement", 7), ("primary_attack", 6),
                              ("special_attack", 6), ("hit_reaction", 4),
                              ("damage_transition", 6), ("destruction", 8)):
            for i in range(count):
                f = i + 1
                out.append((f"nhd_{action}_{i}", hd / "Frames" / action /
                            f"hellwing_death_carrier_{action}_f{f:02d}.png"))
        for action, count in (("primary_muzzle_overlay", 6), ("special_charge_overlay", 6),
                              ("destruction_fx_overlay", 8)):
            for i in range(count):
                f = i + 1
                out.append((f"nhd_{action}_{i}", hd / "Overlay_Frames" / action /
                            f"hellwing_death_carrier_{action}_f{f:02d}.png"))
        for kind in ("primary", "special"):
            for i in range(6):
                f = i + 1
                out.append((f"nhd_{kind}_projectile_{i}", hd / "Projectile_Frames" /
                            f"{kind}_projectile" / f"hellwing_death_carrier_{kind}_projectile_f{f:02d}_64.png"))
        out += [(f"nfx_l7portal_{i}", src) for i, src in enumerate(sorted(GAME.glob("nfx_l7portal_*.png")))]
        env = GAME / "stage8_environment_crimson"
        out += [(f"nl8c_lg_{i}", src) for i, src in enumerate(sorted(env.glob("nl8_lg_*.png")))]
        out += [(f"nl8c_rim_{i}", src) for i, src in enumerate(sorted(env.glob("nl8_rim_*.png")))]
        out += [(f"nl8c_prop_{i}", src) for i, src in enumerate(sorted(env.glob("nl8_prop_*.png"), key=lambda p: int(p.stem.rsplit('_',1)[1])))]
    elif stage == 9:
        out += numbered(GAME / "stage9_enemy_attacks", "s9atk_")
        out += [(f"s9lattice_{i}", src) for i, src in enumerate(sorted((GAME / "stage9_warp_lattice").glob("*.png")))]
    return out


def pack_stage(stage, source_items):
    opened = []
    seen = set()
    for key, src in source_items:
        if key in seen:
            raise RuntimeError(f"duplicate runtime key {key}")
        seen.add(key)
        opened.append((key, src, Image.open(src).convert("RGBA")))
    opened.sort(key=lambda row: (-row[2].height, -row[2].width, row[0]))

    pages = []
    current = []
    x = y = PAD
    shelf_h = 0
    for row in opened:
        key, src, im = row
        if im.width + PAD * 2 > MAX or im.height + PAD * 2 > MAX:
            raise RuntimeError(f"{src} exceeds atlas page")
        if x + im.width + PAD > MAX:
            x = PAD
            y += shelf_h + PAD
            shelf_h = 0
        if y + im.height + PAD > MAX:
            pages.append(current)
            current = []
            x = y = PAD
            shelf_h = 0
        current.append((key, src, im, x, y))
        x += im.width + PAD
        shelf_h = max(shelf_h, im.height)
    if current:
        pages.append(current)

    cells = {}
    roots = {}
    for page_i, placed in enumerate(pages):
        sheet = f"stage{stage}_runtime_{page_i}"
        root_key = "nca_" + sheet
        page_h = max(py + im.height + PAD for _k, _s, im, _px, py in placed)
        atlas = Image.new("RGBA", (MAX, page_h), (0, 0, 0, 0))
        for key, _src, im, px, py in placed:
            atlas.alpha_composite(im, (px, py))
            cells[key] = [sheet, px, py, im.width, im.height]
        rel = Path("assets/game/atlas/stage_runtime") / f"{sheet}.png"
        dest = ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        atlas.save(dest, optimize=True, compress_level=9)
        roots[root_key] = rel.as_posix()
        print(f"stage {stage} page {page_i}: {len(placed)} cells, {atlas.width}x{atlas.height}")
    return roots, cells


all_roots = {}
all_cells = {}
for stage in (2, 3, 4, 6, 7, 8, 9):
    roots, cells = pack_stage(stage, stage_items(stage))
    all_roots.update(roots)
    all_cells.update(cells)

payload = {"roots": all_roots, "cells": all_cells}
MAP.write_text("window.BOF_STAGE_RUNTIME_ATLASES=" + json.dumps(payload, separators=(",", ":")) + ";\n", encoding="utf-8")
print(f"mapped {len(all_cells)} runtime cells across {len(all_roots)} texture pages")
