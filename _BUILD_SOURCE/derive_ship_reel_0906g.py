#!/usr/bin/env python3
"""derive_ship_reel_0906g.py - build a pilot's 17 ship frames from ONE hero plate.

    python _BUILD_SOURCE/derive_ship_reel_0906g.py juggernaut <hero.png>
    python _BUILD_SOURCE/derive_ship_reel_0906g.py juggernaut <hero.png> --write

WHY THIS EXISTS INSTEAD OF ANOTHER GENERATED ROTATION SHEET.

The generated sheet for Juggernaut's new hull came back unusable, and it is the SECOND time:
0906b already recorded the generator ignoring a requested layout (Lizzie's 7x4). Measured on this
one - 8x3 was asked for and 7x3 returned, row 2 came back with the nose pointing LEFT rather than
up, row 1 is 3/4 perspective rather than top-down bank, and connected-component analysis found
**20 components for 21 frames** because two pairs are drawn touching and merge into single 870px
blobs against a ~360px ship. Slicing that on a grid would have cut ships in half.

A BARREL ROLL ABOUT THE NOSE AXIS IS A HORIZONTAL COSINE SCALE, so it can be derived exactly
rather than drawn approximately. That is the geometry, not an approximation of it: at roll angle t
the ship's projected width is |cos t| of its level width and its height is unchanged, which is
precisely why the authored reels have two edge-on slivers a quarter turn apart. Deriving it gives
frames that are correctly ordered, correctly symmetric and consistently lit by construction - three
things the generated sheet was not.

⚠ THE SECOND HALF OF THE ROLL NOW USES A REAL BELLY PLATE (0906y). This docstring used to say the
belly was "the MIRRORED plate darkened by UNDER_DIM ... if Mike wants a true underside the answer is
an authored plate for it, not a better transform." That plate now exists: pass it as the third
argument and the roll interpolates between two authored views instead of one and a mirror. Without
it the old mirror+dim path still runs, so every existing reel is unaffected.

⚠ AND THE BELLY IS THE ONE POSE THE GENERATOR CAN ACTUALLY DRAW. Measured on Decker: asked for a
27-degree BANK it returned the ship YAWED in the image plane - principal axis -49.1 degrees against
the +90.0 of a nose-north hull - and saying "do NOT rotate the image, the nose must point to the
top" three times made it WORSE, -64.4. Asked for a knife-edge it returned a 39px-wide narrowed top
view with the canopy still visible, against the 18px a true edge-on measures. But asked for the
UNDERSIDE - which is just another nose-north top-down view, no roll involved - it came back at
+90.0 with real pylons, gear doors and belly plating. So: generate the two VIEWS, derive the
rotation between them.

⚠ AND THE BANK FRAMES ARE SAMPLED FROM THE ROLL, NOT INVENTED SEPARATELY. pv0..pv4 and _l/_r are
partial rolls, so taking them off the same curve guarantees the bank and the roll agree with each
other. Two independent approximations would drift and the ship would change shape mid-manoeuvre.
"""
import os, sys, math
from PIL import Image, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets/game/ships_derived')
EDGE_MIN = 0.10          # the edge-on frame keeps this fraction of width, never zero
UNDER_DIM = 0.72         # how much darker the belly reads than the topside


def roll_frame(plate, deg, belly=None):
    """the plate at roll angle `deg`, as a canvas the size of the level plate"""
    t = math.radians(deg)
    f = abs(math.cos(t))
    w = max(1, int(round(plate.width * max(EDGE_MIN, f))))
    src = plate
    under = 90 < (deg % 360) < 270
    if under:
        if belly is not None:
            # a real underside, mirrored because rolling past 90 shows it reversed left-to-right
            src = belly.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            src = src.transpose(Image.FLIP_LEFT_RIGHT)
            src = ImageEnhance.Brightness(src).enhance(UNDER_DIM)
    sq = src.resize((w, plate.height), Image.LANCZOS)
    cv = Image.new('RGBA', plate.size, (0, 0, 0, 0))
    cv.alpha_composite(sq, ((plate.width - w) // 2, 0))
    return cv


def main():
    if len(sys.argv) < 3:
        print(__doc__); return 2
    pilot, hero = sys.argv[1], sys.argv[2]
    write = '--write' in sys.argv
    extra = [a for a in sys.argv[3:] if not a.startswith('--')]
    plate = Image.open(hero).convert('RGBA')
    bb = plate.getbbox()
    if bb:
        plate = plate.crop(bb)
    belly = None
    if extra:
        belly = Image.open(extra[0]).convert('RGBA')
        b2 = belly.getbbox()
        if b2:
            belly = belly.crop(b2)
        # ⚠ THE BELLY MUST BE THE SAME SIZE AS THE TOP OR THE SHIP CHANGES SHAPE MID-ROLL. The
        # generator returns its own dimensions whatever is asked (size_behavior is a "hint"), so
        # Decker's came back 172x192 against a 176x218 top. Fitted here, not trusted.
        belly = belly.resize(plate.size, Image.LANCZOS)
        print('%s belly plate supplied, fitted to %dx%d' % (pilot, plate.width, plate.height))
    print('%s hero plate %dx%d' % (pilot, plate.width, plate.height))

    frames = {}
    frames[''] = plate.copy()
    frames['_nf'] = plate.copy()          # the flameless variant is the same hull; the plume is drawn separately
    # the eight roll steps, 45 degrees apart, starting level
    for i in range(8):
        frames['_br%d' % i] = roll_frame(plate, i * 45, belly)
    # banks are partial rolls off the SAME curve, so they cannot disagree with it
    # MEASURED OFF THE AUTHORED SHIPS, not chosen: Cole's pv frames are 0.94-1.00 of his hull
    # width (17-20 degrees) and Freezer's are 0.89-0.99 (19-27). So the authored convention is a
    # 17-27 degree bank, and these sit inside it - a derived ship that banks harder than every
    # hand-drawn one would read as a different aircraft rather than as the same fleet.
    BANK = {'_l': -20, '_r': 20, '_pv0': -27, '_pv1': -17, '_pv2': 0, '_pv3': 17, '_pv4': 27}
    for k, d in BANK.items():
        frames[k] = roll_frame(plate, d, belly)

    order = ['', '_nf', '_l', '_r', '_pv0', '_pv1', '_pv2', '_pv3', '_pv4'] + ['_br%d' % i for i in range(8)]
    print('%d frames derived' % len(frames))
    ws = [(k, frames[k].getbbox()) for k in order]
    print('roll widths (the two edge-on frames are br2 and br6):')
    print('   ' + '  '.join('%s %d' % (k.lstrip('_') or 'hull', (b[2] - b[0]) if b else 0)
                            for k, b in ws if k.startswith('_br') or k == ''))

    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 13)
    except Exception:
        F = ImageFont.load_default()
    T = 140
    cols = 9
    rows = (len(order) + cols - 1) // cols
    proof = Image.new('RGB', (T * cols, (T + 18) * rows), (24, 24, 30))
    d = ImageDraw.Draw(proof)
    for i, k in enumerate(order):
        im = frames[k]
        b = im.getbbox()
        c = im.crop(b) if b else im
        s = min((T - 8) / c.width, (T - 8) / c.height)
        t = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
        x, y = (i % cols) * T, (i // cols) * (T + 18)
        proof.paste(t, (x + (T - t.width) // 2, y + (T - t.height) // 2), t)
        d.text((x + 3, y + T + 2), k.lstrip('_') or 'hull', font=F, fill=(238, 240, 250))
    proof.save(os.path.join(ROOT, 'docs/SHIP_REEL_%s_0906G.png' % pilot.upper()))
    print('wrote docs/SHIP_REEL_%s_0906G.png' % pilot.upper())

    if not write:
        print('DRY RUN - nothing written. Re-run with --write.')
        return 0
    d2 = os.path.join(OUT, pilot)
    os.makedirs(d2, exist_ok=True)
    for k, im in frames.items():
        im.save(os.path.join(d2, 'ship_%s%s.png' % (pilot, k)))
    print('wrote %d frames to assets/game/ships_derived/%s/' % (len(frames), pilot))
    return 0


if __name__ == '__main__':
    sys.exit(main())
