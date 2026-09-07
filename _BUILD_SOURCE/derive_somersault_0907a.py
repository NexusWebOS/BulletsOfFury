#!/usr/bin/env python3
"""derive_somersault_0907a.py - the eight somersault frames, from four authored VIEWS.

    python _BUILD_SOURCE/derive_somersault_0907a.py decker
    python _BUILD_SOURCE/derive_somersault_0907a.py decker --write

Mike, 0906: "even get everyone somersault frames too!" -> "they all need regenerated replacing."

A somersault is a PITCH rotation, so it is the barrel roll's transform turned ninety degrees:
the roll foreshortens HORIZONTALLY about the nose-to-tail axis, and this foreshortens VERTICALLY
about the wing axis. What it cannot do is collapse to a sliver at 90 degrees the way the roll does,
because an aircraft seen nose-on still has a full wingspan - which is exactly why it needs authored
views at the quarter points rather than a squash of the top plate.

FOUR VIEWS, ALL OF WHICH THE GENERATOR CAN ACTUALLY DRAW (0906y/0906z):
    0 deg   TOP      the ship's own hull plate
    90 deg  NOSE-ON  seen from the front, wings spread wide, short
    180 deg BELLY    the underside
    270 deg TAIL-ON  seen from behind, engine bell face-on

⚠ THE FRAMES ARE A SQUASH OF THE NEAREST VIEW, NOT A CROSS-FADE BETWEEN TWO. Blending two
different pictures gives a ghosted double image - two canopies, two sets of wings - which reads as
a rendering fault rather than as motion. Each 45-degree frame takes the view it is closest to and
foreshortens it toward the next one, so every frame is one clean picture.

⚠ AND THE TARGET HEIGHTS COME OFF MAVERICK'S AUTHORED REEL, NOT OFF cos(). Measured on his eight
frames as a fraction of his 228px top view: 1.00 / 0.73 / 0.51 / 0.77 / 0.99 / 0.77 / 0.49 / 0.73.
A pure cosine would put 0.71 at 45 degrees and 0.00 at 90; the authored reel sits slightly above
the cosine at 45 and nowhere near zero at 90. Driving the derivation off the authored numbers means
a derived reel and a hand-drawn one are the same manoeuvre at the same speed.

⚠ MAVERICK'S AND LIZZIE'S OWN `so` FRAMES ARE HAND-DRAWN AND STAY. Cole's are a barrel roll wearing
the wrong name (his so2 is a 31px knife-edge) and Yuri's barely move at all - those two are rebuilt.
"""
import os, sys, json, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEWS = os.path.join(ROOT, '_BUILD_SOURCE/sc_hero_0906x')
OUT = os.path.join(ROOT, 'assets/game/ships_derived')

# maverick's authored reel, as a fraction of his top view's height - the cadence to match
SO_H = [1.000, 0.732, 0.513, 0.772, 0.987, 0.772, 0.491, 0.732]
# which view each 45-degree step is a foreshortening OF
SO_VIEW = ['top', 'top', 'noseon', 'belly', 'belly', 'belly', 'tailon', 'top']


def flat(rgba, bg=(20, 20, 26)):
    """⚠ COMPOSITE, never .convert('RGB') - that discards alpha and paints the old key back (0906v)"""
    o = Image.new('RGB', rgba.size, bg)
    o.paste(rgba, (0, 0), rgba)
    return o


def load(pilot, name):
    for suf in ('_%s.png' % name,):
        f = os.path.join(VIEWS, pilot + suf)
        if os.path.exists(f):
            im = Image.open(f).convert('RGBA')
            b = im.getbbox()
            return im.crop(b) if b else im
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pilot = sys.argv[1]
    write = '--write' in sys.argv

    views = {}
    for v in ('hero', 'noseon', 'belly', 'tailon'):
        views['top' if v == 'hero' else v] = load(pilot, v)
    missing = [k for k, v in views.items() if v is None]
    if missing:
        print('%s is missing view(s): %s - generate them first' % (pilot, ', '.join(missing)))
        return 1
    for k, v in views.items():
        print('   %-8s %dx%d' % (k, v.width, v.height))

    TH = views['top'].height
    frames = {}
    for i in range(8):
        src = views[SO_VIEW[i]]
        target_h = max(4, int(round(TH * SO_H[i])))
        # ⚠ WIDTH IS THE SOURCE VIEW'S OWN, NOT THE TOP VIEW'S. A nose-on aircraft is WIDER than a
        # top-down one (maverick: 215 against 187) because the wings are seen at full span with no
        # sweep foreshortening. Forcing the top view's width would pinch the wings back in and undo
        # the pose.
        if src.height == target_h:
            im = src.copy()
        else:
            sc = target_h / float(src.height)
            # only the VERTICAL axis foreshortens in a pitch; width is the view's own
            im = src.resize((src.width, target_h), Image.LANCZOS)
        frames['_so%d' % i] = im
        print('   so%d  %-8s %dx%d  (%.3f of the top view height)'
              % (i, SO_VIEW[i], im.width, im.height, target_h / float(TH)))

    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 13)
    except Exception:
        F = ImageFont.load_default()
    T = 150
    proof = Image.new('RGB', (T * 8, T + 20), (18, 18, 24))
    d = ImageDraw.Draw(proof)
    for i in range(8):
        im = frames['_so%d' % i]
        sc = min((T - 10) / im.width, (T - 26) / im.height)
        t = flat(im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.NEAREST))
        proof.paste(t, (i * T + (T - t.width) // 2, 20 + (T - 20 - t.height) // 2))
        d.text((i * T + 4, 3), 'so%d %dx%d' % (i, im.width, im.height), font=F, fill=(238, 238, 248))
    proof.save(os.path.join(ROOT, 'docs/SOMERSAULT_%s_0907A.png' % pilot.upper()))
    print('wrote docs/SOMERSAULT_%s_0907A.png' % pilot.upper())

    if not write:
        print('DRY RUN - nothing written.')
        return 0
    d2 = os.path.join(OUT, pilot)
    os.makedirs(d2, exist_ok=True)
    for k, im in frames.items():
        im.save(os.path.join(d2, 'ship_%s%s.png' % (pilot, k)))
    print('wrote 8 somersault frames to assets/game/ships_derived/%s/' % pilot)
    return 0


if __name__ == '__main__':
    sys.exit(main())
