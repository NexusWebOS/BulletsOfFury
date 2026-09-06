#!/usr/bin/env python3
"""build_pilot_bodies_0906.py - the eight front-facing standing figures.

    python _BUILD_SOURCE/build_pilot_bodies_0906.py --write

Mike, 0906: "front facing frames of each pilot like Yuri is facing forward."

Yuri already had one - `yuri_body_0`, authored, and it is the pose every other pilot was generated
to match: square to camera, symmetrical, arms relaxed at the sides, head up. So he is the REFERENCE
and is not regenerated; the other eight are `edit_asset_id` runs on their own `pose_<pilot>_0`
cinematic frame, which keeps each pilot's face and outfit and changes only the stance.

⚠ TAKE THE `pixel_url`, NOT THE `raw_url`, FOR THESE - THE OPPOSITE OF THE RULE FOR THE AVATARS.
CLAUDE.md says to prefer raw because pixel is crushed to the size hint, and that is right when the
plate is opaque. It is wrong here: measured, the raw comes back RGB with NO ALPHA AT ALL and a flat
white background, while the alpha SpriteCook computed lives only on the pixel version. A standing
figure needs its cutout, and re-keying the white myself is the worse option - Falva's suit is white
and Lizzie's is near-white, so a border flood at the threshold the emblems needed would eat into
their clothing. The size cost is real and acceptable: the crushed plates are 228-320px against a
bay that draws them at 95x212.

⚠ AND THE HEIGHT IS NORMALISED, NOT THE CANVAS. The eight come back at eight different sizes
(228, 240, 240, 280, 282, 284, 308, 320), which is `size_behavior: "hint"` again. Scaling each
canvas to one size would leave every pilot a different height on screen, because the figure fills
a different fraction of each. They are trimmed to ink and scaled so the FIGURE is one height -
which is what the eye reads - and Yuri's authored 273px ink sets that height so the new eight
stand level with him rather than the other way round.
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(ROOT, '_BUILD_SOURCE/sc_out_0906')
OUT = os.path.join(ROOT, 'assets/game/pilot_bodies')
YURI = os.path.join(ROOT, 'assets/game/yuri_v2/yuri_body_0.png')
PILOTS = ['axel', 'decker', 'maverick', 'freezer', 'juggernaut', 'lizzie', 'falva', 'cole']


def ink(im):
    bb = im.getbbox()
    return im.crop(bb) if bb else im


def main():
    write = '--write' in sys.argv
    ref = ink(Image.open(YURI).convert('RGBA'))
    H = ref.height
    print('reference: yuri_body_0 ink %dx%d - every figure is scaled to %dpx tall'
          % (ref.width, ref.height, H))
    print()
    made, rows = {}, []
    for p in PILOTS:
        src = os.path.join(GEN, 'bd_%s.png' % p)
        if not os.path.exists(src):
            rows.append((p, 'MISSING', '-', '-')); continue
        im = Image.open(src).convert('RGBA')
        before = '%dx%d' % im.size
        fig = ink(im)
        s = H / fig.height
        out = fig.resize((max(1, round(fig.width * s)), H), Image.LANCZOS)
        made[p] = out
        rows.append((p, before, '%dx%d' % fig.size, '%dx%d' % out.size))

    print('%-11s %-10s %-11s %s' % ('pilot', 'returned', 'ink', 'normalised'))
    print('-' * 48)
    for r in rows:
        print('%-11s %-10s %-11s %s' % r)
    ws = [im.width for im in made.values()] + [ref.width]
    print(os.linesep + 'widths at a common height: %d..%d px (yuri %d) - a natural build spread,'
          % (min(ws), max(ws), ref.width))
    print('not a scaling error: juggernaut is meant to be the widest and falva the slightest.')

    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    TH = 300
    order = ['axel', 'decker', 'maverick', 'freezer', 'juggernaut', 'yuri', 'lizzie', 'falva', 'cole']
    cw = 150
    proof = Image.new('RGB', (cw * 9, TH + 26), (28, 30, 36))
    d = ImageDraw.Draw(proof)
    for i, p in enumerate(order):
        im = ref if p == 'yuri' else made.get(p)
        if im is None:
            continue
        s = min((cw - 14) / im.width, (TH - 10) / im.height)
        t = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
        proof.paste(t, (i * cw + (cw - t.width) // 2, TH - 5 - t.height), t)
        d.text((i * cw + 6, TH + 5), p + ('  (authored)' if p == 'yuri' else ''), font=F,
               fill=(255, 236, 160) if p == 'yuri' else (238, 240, 248))
    proof.save(os.path.join(ROOT, 'docs/PILOT_BODIES_0906.png'))
    print(os.linesep + 'wrote docs/PILOT_BODIES_0906.png (all nine, standing on one baseline)')

    if not write:
        print('DRY RUN - nothing written. Re-run with --write.')
        return 0
    os.makedirs(OUT, exist_ok=True)
    for p, im in made.items():
        im.save(os.path.join(OUT, '%s_body_0.png' % p))
    print('wrote %d figures to assets/game/pilot_bodies/' % len(made))
    return 0


if __name__ == '__main__':
    sys.exit(main())
