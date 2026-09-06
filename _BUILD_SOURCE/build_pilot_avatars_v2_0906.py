#!/usr/bin/env python3
"""build_pilot_avatars_v2_0906.py - the nine square bordered avatars, generated per pilot.

    python _BUILD_SOURCE/build_pilot_avatars_v2_0906.py --write

Mike, 0906: "now use spritecook and get me bordered avatars of each pilot."

This REPLACES build_pilot_avatars_0906.py, which composited one lifted frame over nine portraits
because only 66 credits remained. Mike topped the account up to 1,066, so the reason that script
existed is gone and each pilot now gets a real generation: `edit_asset_id` on their own authored
portrait, so the likeness is theirs and not a lookalike.

⚠ YURI IS NOT REGENERATED, AND THAT IS THE POINT RATHER THAN AN OMISSION. His authored plate IS
the reference every other avatar was generated to match - the gunmetal frame, the corner bolt
plates, the accent bars, the dark interior and the rim light are all described FROM it. Running it
back through the generator would replace authored art with an imitation of itself.

⚠ THE ACCENT COLOUR IS EACH PILOT'S OWN `PILOTS[].tint`, NOT A GUESS. Yuri's plate accents measure
red and his tint is #e23a3a; the rest follow the same rule, so the roster reads as one set and each
slot still says whose it is. That table already drives the card, the HUD and the ship, so the
avatar cannot drift from them.

⚠ AND THERE IS NO PALETTE LOCK HERE, DELIBERATELY - THE RULE IN CLAUDE.md IS FOR A DIFFERENT ART
CLASS. That note ("pixel:true does NOT give you pixel art", snap to the reference's own palette)
was measured on the Cryo Spear, an authored BOSS at 61 colours, where a 19,063-colour generation
swapping in at 62% HP changes art style mid-fight. Measured here instead: the authored portraits
run 19,815 to 37,168 colours on opaque pixels and Yuri's own authored avatar is 120,327. They are
continuous-tone illustrated plates, not low-colour sprites, and the generations land at ~60,000 -
inside that range. Locking them would flatten art that is meant to be smooth and would make the new
avatars LESS like the authored ones, which is the opposite of what the rule is for.
"""
import os, sys, collections
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(ROOT, '_BUILD_SOURCE/sc_out_0906')
OUT = os.path.join(ROOT, 'assets/game/pilot_avatars')
YURI_PLATE = 'C:/Users/Mdogg/Desktop/new yuri.png'
SIZE = 256
PILOTS = ['axel', 'decker', 'maverick', 'freezer', 'juggernaut', 'yuri', 'lizzie', 'falva', 'cole']
TINT = {'axel': '#3a8aff', 'decker': '#ffd24a', 'maverick': '#8de23a', 'freezer': '#6fd0ff',
        'juggernaut': '#c08a3a', 'yuri': '#e23a3a', 'lizzie': '#ffc21a', 'falva': '#ff2a8f',
        'cole': '#7ad63a'}


def opaque_colours(im):
    px = im.convert('RGBA').load()
    c = set()
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y][3] > 8:
                c.add(px[x, y][:3])
    return len(c)


def square(im):
    """centre-crop to square, then resize. The frame reaches all four edges, so a crop that is not
    centred would eat one side's accent bar - measured square already on every generation, but the
    crop is here because `size_behavior` is a HINT and the next batch may not be."""
    w, h = im.size
    if w != h:
        s = min(w, h)
        im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
    return im.resize((SIZE, SIZE), Image.LANCZOS)


def main():
    write = '--write' in sys.argv
    made, rows = {}, []
    for p in PILOTS:
        if p == 'yuri':
            src, note = YURI_PLATE, 'authored (the reference plate)'
        else:
            src, note = os.path.join(GEN, 'av_%s.png' % p), 'generated'
        if not os.path.exists(src):
            rows.append((p, 'MISSING', '-', '-', note)); continue
        im = Image.open(src).convert('RGBA')
        before = '%dx%d' % im.size
        n = opaque_colours(im)
        out = square(im)
        made[p] = out
        rows.append((p, before, '%dx%d' % out.size, '%d' % n, note))

    print('%-11s %-11s %-9s %-8s %s' % ('pilot', 'generated', 'normalised', 'colours', 'source'))
    print('-' * 68)
    for r in rows:
        print('%-11s %-11s %-9s %-8s %s' % r)

    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    T = 200
    proof = Image.new('RGB', ((T + 6) * 5, (T + 22) * 2), (18, 16, 22))
    d = ImageDraw.Draw(proof)
    for i, p in enumerate(PILOTS):
        if p not in made:
            continue
        x, y = (i % 5) * (T + 6), (i // 5) * (T + 22)
        proof.paste(made[p].resize((T, T), Image.LANCZOS).convert('RGB'), (x, y))
        d.text((x + 3, y + T + 4), '%s %s' % (p, TINT[p]), font=F, fill=(240, 240, 250))
    proof.save(os.path.join(ROOT, 'docs/PILOT_AVATARS_V2_0906.png'))
    print(os.linesep + 'wrote docs/PILOT_AVATARS_V2_0906.png')

    if not write:
        print('DRY RUN - no avatars written. Re-run with --write.')
        return 0
    os.makedirs(OUT, exist_ok=True)
    for p, im in made.items():
        im.convert('RGBA').save(os.path.join(OUT, 'pav_%s.png' % p))
    print('wrote %d avatars to assets/game/pilot_avatars/ (same keys, so nothing needs rewiring)'
          % len(made))
    return 0


if __name__ == '__main__':
    sys.exit(main())
