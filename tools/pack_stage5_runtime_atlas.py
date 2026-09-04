"""Pack every Stage-5 combat reel used at runtime into one 4096px texture.

The original PNGs remain editable source assets.  This emits the shipping atlas plus the exact
cell table consumed by XART, eliminating 159 independent browser image decodes.
"""
from pathlib import Path
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "assets" / "game"
OUT = GAME / "atlas" / "stage5_runtime_atlas.png"
MAP = GAME / "atlas" / "stage5_runtime_atlas.js"
WIDTH = 4096
PAD = 4

items = []
for unit_dir in sorted((GAME / "stage5_enemy_attacks").iterdir()):
    if not unit_dir.is_dir():
        continue
    for i, src in enumerate(sorted(unit_dir.glob("*.png"))):
        items.append((f"s5atk_{unit_dir.name}_{i}", src))
for i, src in enumerate(sorted((GAME / "stage5_fracture_halo").glob("*.png"))):
    items.append((f"s5fracture_{i}", src))
for src in sorted((GAME / "chaos_harrier").glob("*.png")):
    items.append((src.stem, src))

opened = []
for key, src in items:
    im = Image.open(src).convert("RGBA")
    opened.append((key, src, im))
opened.sort(key=lambda row: (-row[2].height, -row[2].width, row[0]))

x = y = PAD
shelf_h = 0
placed = []
for key, src, im in opened:
    if x + im.width + PAD > WIDTH:
        x = PAD
        y += shelf_h + PAD
        shelf_h = 0
    placed.append((key, src, im, x, y))
    x += im.width + PAD
    shelf_h = max(shelf_h, im.height)
height = y + shelf_h + PAD

atlas = Image.new("RGBA", (WIDTH, height), (0, 0, 0, 0))
cells = {}
for key, _src, im, px, py in placed:
    atlas.alpha_composite(im, (px, py))
    cells[key] = ["stage5_runtime_atlas", px, py, im.width, im.height]

OUT.parent.mkdir(parents=True, exist_ok=True)
atlas.save(OUT, optimize=True, compress_level=9)
MAP.write_text("window.BOF_STAGE5_CELLS=" + json.dumps(cells, separators=(",", ":")) + ";\n", encoding="utf-8")
print(f"packed {len(cells)} cells -> {OUT.relative_to(ROOT)} {atlas.width}x{atlas.height}")
print(f"map -> {MAP.relative_to(ROOT)}")
