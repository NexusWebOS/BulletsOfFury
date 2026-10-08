"""Normalize authored Overdrive ground masters; no runtime art is drawn here.

Source PNGs and exact generation prompts stay in art/ground_1008/source.
This workflow owns only loose expansion assets, never the base-game atlases.
"""
from pathlib import Path
import json
from PIL import Image

BASE = Path(__file__).resolve().parents[1] / 'art/ground_1008'
SRC = BASE / 'source'


def cell(im, box, size):
    frame = im.crop(box).convert('RGBA').resize(size, Image.Resampling.NEAREST)
    # Remove only near-invisible generated lighting outside the physical pixels.
    frame.putdata([(r, g, b, a) if a >= 28 else (0, 0, 0, 0)
                   for r, g, b, a in frame.get_flattened_data()])
    return frame


def main():
    records = {}
    def save(key, image, anchor=None):
        image.save(BASE / (key + '.png'))
        records[key] = {'file': key + '.png', 'size': list(image.size),
                        'anchor': anchor or [image.width / 2, image.height / 2]}

    boss = Image.open(SRC / 'bastion_huntsman.png')
    for i, key in enumerate(['huntsman_hull', 'huntsman_turret', 'huntsman_pod_l',
                              'huntsman_pod_r', 'huntsman_damaged', 'huntsman_wreck']):
        x, y = (i % 3) * 512, (i // 3) * 512
        anchors = [[137, 148], [128, 184], [120, 136], [137, 126], [137, 148], [137, 148]]
        save(key, cell(boss, (x, y, x + 512, y + 512), (256, 256)), anchors[i])

    warrior = Image.open(SRC / 'warrior.png')
    warrior_cells = [
        ('warrior_hull', (0, 0, 512, 512), [127, 156]),
        ('warrior_helmet', (510, 0, 1100, 515), [126, 226]),
        ('warrior_arm_l', (1100, 0, 1536, 512), [225, 96]),
        ('warrior_arm_r', (0, 512, 512, 1024), [32, 60]),
        ('warrior_damaged', (512, 512, 1024, 1024), [127, 128]),
        ('warrior_wreck', (1024, 512, 1536, 1024), [127, 128]),
    ]
    for key, box, anchor in warrior_cells:
        save(key, cell(warrior, box, (256, 256)), anchor)

    buildings = Image.open(SRC / 'destructible_buildings.png')
    for i, key in enumerate(['warehouse_intact', 'warehouse_damaged', 'warehouse_rubble', 'roof_fragment',
                              'relay_intact', 'relay_damaged', 'relay_rubble', 'wall_fragment']):
        x0, y0 = round((i % 4) * buildings.width / 4), round((i // 4) * buildings.height / 2)
        x1, y1 = round((i % 4 + 1) * buildings.width / 4), round((i // 4 + 1) * buildings.height / 2)
        save(key, cell(buildings, (x0, y0, x1, y1), (256, 256)))

    fx = Image.open(SRC / 'tank_weapon_fx.png')
    for row, (y0, y1) in enumerate([(0, 330), (330, 700), (700, 1086)]):
        keys = ([f'tank_charge_{i}' for i in range(4)] if row == 0 else
                [f'tank_missile_{i}' for i in range(4)] if row == 1 else
                ['tank_laser_gold', 'tank_laser_silver', 'tank_laser_crimson', 'tank_ap'])
        for col, key in enumerate(keys):
            x0, x1 = round(col * fx.width / 4), round((col + 1) * fx.width / 4)
            save(key, cell(fx, (x0, y0, x1, y1), (128, 128)))

    concrete = Image.open(SRC / 'concrete_break.png')
    for row, (y0, y1) in enumerate([(0, 452), (452, 817), (817, 1086)]):
        keys = ([f'concrete_break_{i}' for i in range(4)] if row == 0 else
                [f'concrete_dust_{i}' for i in range(4)] if row == 1 else
                ['barrier_intact', 'barrier_damaged', 'barrier_rubble', 'concrete_fragment'])
        for col, key in enumerate(keys):
            x0, x1 = round(col * concrete.width / 4), round((col + 1) * concrete.width / 4)
            size = (256, 192) if row == 2 else (192, 192)
            save(key, cell(concrete, (x0, y0, x1, y1), size))

    # Repeat whole authored sectors. Alternating vertical mirrors gives exact
    # matching pixels at each seam without synthesizing terrain or recoloring it.
    sector = Image.open(SRC / 'compound_sector.png').convert('RGB').resize((800, 800), Image.Resampling.NEAREST)
    ground = Image.new('RGB', (800, 3600))
    for row in range(5):
        tile = sector if row % 2 == 0 else sector.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        ground.paste(tile, (0, row * 800))
    arena = Image.open(SRC / 'warrior_arena.png').convert('RGB').resize((800, 800), Image.Resampling.NEAREST)
    ground.paste(arena, (0, 0))
    save('compound_ground', ground)
    (BASE / 'manifest.json').write_text(json.dumps({'tool': 'built-in image_gen', 'assets': records}, indent=2), encoding='utf-8', newline='\n')
    registration = '(function(root){root.TD_GROUND_ART=' + json.dumps(records, separators=(',', ':')) + ';})(window);\n'
    (BASE / 'manifest.js').write_text(registration, encoding='utf-8', newline='\n')
    print(f'{len(records)} authored ground assets registered')


if __name__ == '__main__':
    main()
