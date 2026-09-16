#!/usr/bin/env python3
"""
chaingun_badges_0916.py - THE CHAINGUN ICONS, GENERATED WHOLE.

    python3 _BUILD_SOURCE/chaingun_badges_0916.py <src_dir> [--check]

Mike, 0916, on the composited first attempt: *"you have to generate those chaingun icons by scratch,
they look clearly edited."* He was right - that version was a generated barrel dropped into another
weapon's badge with its interior cleared, and it read exactly like what it was.

These are generated COMPLETE: frame, field, barrel and the Roman-numeral tier plate, one job per
tier, with three authored badges (`micon_icebreath_3/4/5`) uploaded as the style reference so the
segmented bevelled ring, the black field and the tag come back in the family's own language.
SpriteCook, `gemini-3.1-flash-image`, two variations per tier; the pick per tier is the one whose
muzzle face reads clearest at icon size.

⚠ THE NUMERALS CAME BACK CORRECT AND THAT IS NOT GUARANTEED - generated text usually is not.
Every tier was rendered and read before selection (I, II, III, IV, V), and one rejected variation had
a GOLD V where the frame is red. Read the numeral on any regeneration; do not assume it.

What this file does after the generation is only what the art needs to sit in the game:

⚠ SIZE. `size_behavior` is "hint": 112x112 was requested and the jobs returned 100, 106 and 200.
The icons are drawn by HEIGHT beside the other weapon badges, so each is scaled to the family's own
112 and its aspect kept - a badge scaled to a square would draw narrower than its neighbours.

⚠ NO PALETTE LOCK, AND THAT IS A MEASUREMENT RATHER THAN AN OVERSIGHT. 0905's rule is that
`pixel:true` does not give pixel art and a generated plate must be snapped to the reference's own
palette - it was written against a boss plate whose authored counterpart is **61 colours**. These
badges are not that: measured on opaque pixels only, `icebreath_3` is **6,329** colours,
`icebreath_1` 4,977, `mg_5` 4,775, `thermoshock_3` 2,875. They are rich anti-aliased art. The
generated badges come back at 4,600-5,600, which is INSIDE that range, so a snap would only flatten
them - it would be a fix for a problem this family does not have. The snap is kept in the file
behind --snap for the day a flatter family needs it, with the measurement recorded here so the next
person does not have to re-derive it.
⚠ AND IT WOULD HAVE TO SNAP TO THE WHOLE FAMILY, NOT ONE BADGE: snapping an ORANGE tier to a green
badge's palette repaints the tier, which is the opposite of the point.
"""
import os, sys, argparse, collections
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ATLAS = os.path.join(ROOT, 'assets', 'game', 'atlas', 'bof_player_weapon_special_icons.png')
DST = os.path.join(ROOT, 'assets', 'game', 'stage5_archmage_0916')
OUT = os.path.join(ROOT, 'docs', 'proofs', 'chaingun_icons_0916')

# the pick per tier, chosen by reading the render: clearest muzzle face, correct numeral
PICK = {1: 'b1a', 2: 'b2a', 3: 'b3b', 4: 'b4b', 5: 'b5a'}   # b4b keeps the family's aspect; b4a came back wider than its siblings
FAMILY_H = 112

# every authored weapon badge, for the palette
AUTHORED = [(144, 520, 96, 112), (271, 520, 97, 112), (399, 520, 98, 112), (527, 520, 97, 112),
            (654, 520, 99, 112), (35, 31, 58, 66), (162, 31, 60, 66), (280, 16, 79, 96),
            (408, 16, 79, 96), (536, 16, 80, 96)]


def opaque_colours(im):
    px = im.convert('RGBA').load()
    return len({px[x, y][:3] for y in range(im.height) for x in range(im.width) if px[x, y][3] > 8})


def family_palette(atlas):
    c = collections.Counter()
    for r in AUTHORED:
        crop = atlas.crop((r[0], r[1], r[0] + r[2], r[1] + r[3]))
        px = crop.load()
        for y in range(crop.height):
            for x in range(crop.width):
                p = px[x, y]
                if p[3] > 8:
                    c[p[:3]] += 1
    return [k for k, _ in c.most_common()]


def snap(im, pal):
    out = im.copy().convert('RGBA')
    px = out.load()
    cache = {}
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a <= 96:
                px[x, y] = (0, 0, 0, 0)
                continue
            k = (r, g, b)
            if k not in cache:
                cache[k] = min(pal, key=lambda c: (c[0] - r) ** 2 + (c[1] - g) ** 2 + (c[2] - b) ** 2)
            c = cache[k]
            px[x, y] = (c[0], c[1], c[2], 255)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--snap', action='store_true', help='palette-lock to the authored family (see the header)')
    a = ap.parse_args()
    atlas = Image.open(ATLAS).convert('RGBA')
    pal = family_palette(atlas)
    print('family palette: %d colours from %d authored badges' % (len(pal), len(AUTHORED)))

    made = []
    for t in (1, 2, 3, 4, 5):
        src = Image.open(os.path.join(a.src, PICK[t] + '.png')).convert('RGBA')
        b = src.getbbox()
        if b:
            src = src.crop(b)
        w = max(1, int(round(src.width * FAMILY_H / src.height)))
        fit = src.resize((w, FAMILY_H), Image.LANCZOS)
        before = opaque_colours(fit)
        out = snap(fit, pal) if a.snap else fit
        made.append((t, out))
        print('  tier %d  %s  %dx%d -> %dx%d  colours %d -> %d'
              % (t, PICK[t], src.width, src.height, out.width, out.height, before, opaque_colours(out)))

    os.makedirs(OUT, exist_ok=True)
    if a.check:
        Z = 3; pad = 10
        W = pad + len(made) * (max(m[1].width for m in made) * Z + pad)
        H = FAMILY_H * Z + pad * 2 + 16
        card = Image.new('RGBA', (W, H), (28, 30, 38, 255))
        from PIL import ImageDraw
        d = ImageDraw.Draw(card); x = pad
        for t, im in made:
            card.alpha_composite(im.resize((im.width * Z, im.height * Z), Image.NEAREST), (x, pad))
            d.text((x + 4, pad + FAMILY_H * Z + 2), 'tier %d' % t, fill=(255, 220, 150, 255))
            x += im.width * Z + pad
        p = os.path.join(OUT, '07_final_badges.png')
        card.save(p); print('--check: wrote', os.path.relpath(p, ROOT))
        return

    for t, im in made:
        p = os.path.join(DST, 'chaingun_icon_%d.png' % t)
        im.save(p)
        print('wrote', os.path.relpath(p, ROOT))


if __name__ == '__main__':
    main()
