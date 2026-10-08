"""Bake the ground pack's three tank families in all eleven pilot paints for the top-down levels.

The recolour is the pack's own rule, ported verbatim from expansion/ground/preview.html `tint()`:
only cobalt-blue paint changes (b > r+23, b > g*1.08, g > b*.14), luminance carried through and
scaled by the pilot's `lum`. Baked offline so the game never reads pixels at runtime (getImageData
throws on a file:// page).

    python expansion/topdown/_research/bake_ground_tanks.py          (from the BulletsOfFury folder)
"""
import json, os
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
GROUND = os.path.join(ROOT, 'ground')
OUT = os.path.join(os.path.dirname(__file__), '..', 'art', 'tanks')
PARTS = ['hull', 'turret', 'damaged_hull', 'wreck']

def tint(im, color, lum):
    rgb = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    target = .2126 * rgb[0] + .7152 * rgb[1] + .0722 * rgb[2]
    px = im.load(); n = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and b > r + 23 and b > g * 1.08 and g > b * .14:
                L = (.2126 * r + .7152 * g + .0722 * b) * lum
                px[x, y] = tuple(min(255, round(c * L / target)) for c in rgb) + (a,); n += 1
    return n

def main():
    man = json.load(open(os.path.join(GROUND, 'manifest.json')))
    os.makedirs(OUT, exist_ok=True)
    for pilot, p in man['pilots'].items():
        for part in PARTS:
            im = Image.open(os.path.join(GROUND, 'tanks', f"{p['family']}_{part}.png")).convert('RGBA')
            n = tint(im, p['color'], p['lum'])
            im.save(os.path.join(OUT, f'{pilot}_{part}.png'))
            print(pilot, p['family'], part, 'repainted', n)
    json.dump({k: {'family': v['family'], 'color': v['color']} for k, v in man['pilots'].items()},
              open(os.path.join(OUT, 'pilots.json'), 'w'), indent=1)

main()
