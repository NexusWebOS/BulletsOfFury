"""stealth_jets_1002 - the Stage 6 stealth flight sheets (Mike, 1002).

    python3 _BUILD_SOURCE/stealth_jets_1002.py

"Use the stealth fighter jets that are blue, palette swap them to red, and another new enemy to green
... make an orange one with machine gun turrets ... generate this one entirely with spritecook using
the ship its based off of as reference."

Inputs (never this script's own output):
  assets/game/mission_repair_0929/bluejets.png   the authored blue stealth jet, frames east/west/south
  _BUILD_SOURCE/stealth_orange_spritecook_1002.png  SpriteCook edit of the blue jet's south frame
                                                    (orange paint, wing gatlings, chin gun)
Outputs assets/game/stealth_1002/{red,green,orange}.png - 4 cells of 128x128: east, west, south, north.

RED/GREEN are a hue ROTATION of the blue paint only (palette rule: hue moves, saturation and value -
i.e. the shading - stay); the silver metal, black outlines and orange ordnance accents are untouched.
NORTH (nose up) is the south cell turned 180 degrees and the orange east/west are the south cell turned
90 - a heading change of a top-down hull, not a bank, so rotation is the correct derivation.
"""
import colorsys, os
from PIL import Image
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = os.path.join(ROOT, 'assets/game/mission_repair_0929/bluejets.png')
ORANGE = os.path.join(ROOT, '_BUILD_SOURCE/stealth_orange_spritecook_1002.png')
OUT = os.path.join(ROOT, 'assets/game/stealth_1002')
TARGET = {'red': 0.995, 'green': 0.33}


def is_blue(r, g, b):
    return b > r * 1.35 and b > g * 1.12 and b > 40


def recolor(im, hue):
    im = im.copy(); px = im.load(); n = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a or not is_blue(r, g, b): continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            rr, gg, bb = colorsys.hsv_to_rgb(hue, s, v)
            px[x, y] = (round(rr * 255), round(gg * 255), round(bb * 255), a); n += 1
    return im, n


def cell128(im):
    c = Image.new('RGBA', (128, 128), (0, 0, 0, 0)); c.paste(im, ((128 - im.width) // 2, (128 - im.height) // 2), im); return c


def main():
    os.makedirs(OUT, exist_ok=True)
    blue = Image.open(SRC).convert('RGBA')
    cells = [blue.crop((i * 128, 0, i * 128 + 128, 128)) for i in range(3)]
    for name, hue in TARGET.items():
        sheet = Image.new('RGBA', (512, 128), (0, 0, 0, 0)); total = 0
        for i, c in enumerate(cells):
            rc, n = recolor(c, hue); total += n; sheet.paste(rc, (i * 128, 0))
        sheet.paste(recolor(cells[2], hue)[0].rotate(180), (384, 0))
        assert total > 1500, name + ': too few blue pixels recoloured (%d)' % total
        sheet.save(os.path.join(OUT, name + '.png')); print(name, 'recoloured px', total)
    o = cell128(Image.open(ORANGE).convert('RGBA'))
    sheet = Image.new('RGBA', (512, 128), (0, 0, 0, 0))
    for i, c in enumerate([o.rotate(90), o.rotate(-90), o, o.rotate(180)]): sheet.paste(c, (i * 128, 0))
    sheet.save(os.path.join(OUT, 'orange.png')); print('orange sheet written')


if __name__ == '__main__':
    main()
