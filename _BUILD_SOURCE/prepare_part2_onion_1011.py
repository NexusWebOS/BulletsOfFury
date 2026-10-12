"""Measured source crops for Mike's onion correction; no painted sprite pixels."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / '_ART_SOURCES/part2_1010'
OUT = ROOT / '_ART_SOURCES/part2_1011'
OUT.mkdir(parents=True, exist_ok=True)
im = Image.open(SRC / 'atom_raw.png').convert('RGBA')
# Actual seven rows, separated by fully transparent horizontal gutters.
rows = [(62, 197), (223, 434), (447, 675), (691, 914), (933, 1159), (1190, 1419), (1477, 1737)]
poses = []
for i in range(28):
    row, col = divmod(i, 4)
    rect = [round(col * im.width / 4), rows[row][0] - 4, round((col + 1) * im.width / 4), rows[row][1] + 4]
    cell = im.crop(rect)
    p = np.asarray(cell).copy()
    # The source has unowned near-transparent gutters from neighboring poses.
    # Discard only <=20/255 alpha contamination; all visible authored RGB and
    # all stronger smoke/sparks remain unchanged.
    p[p[:, :, 3] <= 20, 3] = 0
    cell = Image.fromarray(p)
    ys, xs = np.nonzero(p[:, :, 3] >= 24)
    # The ground ridge is the lowest authored pixel; late smoke rises above it.
    ground = int(ys.max()) + 1
    base = np.nonzero((p[:, :, 3] >= 24) & (np.indices(p.shape[:2])[0] >= ground - 7))[1]
    cx = (float(base.min()) + float(base.max()) + 1) / 2
    c = Image.new('RGBA', (384, 576))
    k = 1.5
    scaled = cell.resize((round(cell.width * k), round(cell.height * k)), Image.Resampling.NEAREST)
    move = [round(192 - cx * k), round(480 - ground * k)]
    c.alpha_composite(scaled, move)
    c.save(OUT / f'atom_source_{i:02d}.png')
    assert c.getbbox()[1] >= 8 and c.getbbox()[3] <= 568, (i, c.getbbox())
    poses.append(dict(source_rect=rect, source_pivot=[cx, ground], scale=k, translation=move, opaque_bounds=c.getbbox()))
(OUT / 'atom_source_crops.json').write_text(json.dumps(poses, indent=2), encoding='utf-8')
# Four true intermediate poses are requested between these pairs. Original
# twenty-eight authored poses are retained, rather than inventing cropped cells.
pairs = [(3, 4), (6, 7), (15, 16), (23, 24)]
for n, (left, right) in enumerate(pairs):
    c = Image.new('RGBA', (768, 576))
    c.alpha_composite(Image.open(OUT / f'atom_source_{left:02d}.png'), (0, 0))
    c.alpha_composite(Image.open(OUT / f'atom_source_{right:02d}.png'), (384, 0))
    c.save(OUT / f'atom_pair_{n}.png')
print(json.dumps(dict(source_poses=len(poses), pairs=pairs, rows=rows)))
