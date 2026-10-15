"""Register the rebuilt Warrior's six even, padded module canvases together.

The generated master stays intact. No per-frame fitting or atlas edits.
"""
from pathlib import Path
import hashlib, json
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'expansion/topdown/art/warrior_1011'


def main():
    source = OUT / 'source/warrior.png'
    im = Image.open(source).convert('RGBA')
    assert im.size == (1536, 1024), im.size
    keys = ['warrior_hull', 'warrior_helmet', 'warrior_arm_l',
            'warrior_arm_r', 'warrior_damaged', 'warrior_wreck']
    anchors = [[256, 270], [268, 315], [450, 170],
               [60, 170], [256, 270], [256, 270]]
    assets = {}
    for i, (key, anchor) in enumerate(zip(keys, anchors)):
        x, y = (i % 3) * 512, (i // 3) * 512
        # The helmet's shoulder extends into the neighboring cell's empty
        # left gutter. Extract the arm's measured source region, then restore
        # that shared transparent gutter without moving its physical mount.
        pad_left = 48 if key == 'warrior_arm_l' else 0
        frame = Image.new('RGBA', (512, 512))
        frame.paste(im.crop((x + pad_left, y, x + 512, y + 512)), (pad_left, 0))
        frame.save(OUT / (key + '.png'))
        # Measured visible bounds for the native camera/geometry review. Alpha
        # is preserved in the exported frame; the threshold only measures it.
        bounds = frame.getchannel('A').point(lambda a: 255 if a >= 80 else 0).getbbox()
        assets[key] = {'file': f'expansion/topdown/art/warrior_1011/{key}.png',
                       'size': [512, 512], 'anchor': anchor,
                       'bounds': list(bounds),
                       'sourceCell': [x, y, 512, 512],
                       'sourceCrop': [x + pad_left, y, 512 - pad_left, 512],
                       'transparentPadding': [pad_left, 0, 0, 0]}
    rig = {
        'hull': {'key': 'warrior_hull', 'x': 0, 'y': 0, 'hx': 0, 'hy': 0,
                 'r': 108, 'scale': .56},
        'helmet': {'key': 'warrior_helmet', 'x': 0, 'y': 20, 'hx': 0, 'hy': -52,
                   'r': 54, 'scale': .42, 'mx': 0, 'my': -40},
        'armL': {'key': 'warrior_arm_l', 'x': -92, 'y': -38,
                 'hx': -164, 'hy': 27, 'r': 43, 'scale': .34,
                 'mx': -184, 'my': 64},
        'armR': {'key': 'warrior_arm_r', 'x': 92, 'y': -38,
                 'hx': 164, 'hy': 27, 'r': 43, 'scale': .34,
                 'mx': 184, 'my': 64},
    }
    doc = {'tool': 'built-in image_gen', 'master': 'source/warrior.png',
           'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
           'frameFormat': '512x512, fixed pivot and common scale per module bank',
           'assets': assets, 'rig': rig}
    (OUT / 'manifest.json').write_text(json.dumps(doc, indent=2), encoding='utf-8', newline='\n')
    (OUT / 'manifest.js').write_text('(function(root){root.TD_WARRIOR_ART=' +
                                  json.dumps(doc, separators=(',', ':')) +
                                  ';})(window);\n', encoding='utf-8', newline='\n')
    print('6 Warrior modules registered: even 512x512 frames, original alpha retained')


if __name__ == '__main__':
    main()
