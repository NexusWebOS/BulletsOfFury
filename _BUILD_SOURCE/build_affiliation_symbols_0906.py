#!/usr/bin/env python3
"""build_affiliation_symbols_0906.py - the faction emblems for the pilot cards.

    python _BUILD_SOURCE/build_affiliation_symbols_0906.py --write

Mike, 0906: "there affiliation symbols should be regenerated and used on the cards."

⚠ THERE ARE SIX AFFILIATIONS ACROSS NINE PILOTS, NOT NINE. Two pilots fly for AIRFORCE, two are
INDEPENDENT, two are PRINCESSES OF THE SKY. A faction badge is worn by its members, so the emblem
is keyed by AFFILIATION and the card looks it up - generating nine would have produced two
different Airforce badges and made the roster read as nine loners rather than six factions.

⚠ AND THE TWO AFFILIATION TABLES IN THE GAME DISAGREE ABOUT TWO PILOTS. `BOFX.pilotcard[].affil`
says lizzie PRINCESSES OF THE SKY and cole THE RIGHT HAND MAN; `AINTRO_AFFIL` says STRATEGIC
ORDNANCE and FURY FOUNDER. This follows the pilotcard table because that is the one the CARD draws
and the card is what Mike asked to change - but the disagreement is real, it is Mike's to settle,
and it is why AFFIL_KEY is a table rather than a string comparison.

⚠ THE WHITE IS FLOOD-KEYED AT THE ANTI-ALIASING BAND, NOT AT PURE WHITE. Measured: each plate is
44-71% pure white with a further 100-800 px sitting in the 232..249 band, which is the soft edge
between badge and background. Keying only >=250 leaves that band behind as a white halo ring around
every emblem - the exact artefact the standing halo rule exists to prevent, arriving from the other
direction. The flood is CONNECTIVITY-based from the border, so a light highlight enclosed by the
badge (the steel rim, the star) cannot be reached and cannot be eaten - which is what makes a
threshold this generous safe here, where a global sweep at the same value would not be.
"""
import os, sys
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(ROOT, '_BUILD_SOURCE/sc_out_0906')
OUT = os.path.join(ROOT, 'assets/game/affiliations')
SIZE = 128
WHITE = 232        # min-channel at or above this, and reachable from the border, is background

# affiliation -> the generated plate. Keyed by the string the CARD carries.
AFFIL_KEY = {
    'AIRFORCE':              'airforce',
    'ORDER OF THE MATRIX':   'matrix',
    'INDEPENDENT':           'independent',
    'BROTHERHOOD OF FURY':   'brotherhood',
    'PRINCESSES OF THE SKY': 'princesses',
    'THE RIGHT HAND MAN':    'forge',
}
PILOT_AFFIL = {
    'axel': 'AIRFORCE', 'freezer': 'AIRFORCE',
    'decker': 'ORDER OF THE MATRIX',
    'maverick': 'INDEPENDENT', 'yuri': 'INDEPENDENT',
    'juggernaut': 'BROTHERHOOD OF FURY',
    'lizzie': 'PRINCESSES OF THE SKY', 'falva': 'PRINCESSES OF THE SKY',
    'cole': 'THE RIGHT HAND MAN',
}


def is_bg(p):
    return min(p[0], p[1], p[2]) >= WHITE


def key_white(im):
    """flood the background in from the border; anything enclosed by the badge survives"""
    im = im.convert('RGBA')
    w, h = im.size
    px = im.load()
    seen = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_bg(px[x, y]) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg(px[x, y]) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    n = 0
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and is_bg(px[nx, ny]):
                seen[ny][nx] = True; q.append((nx, ny))
    for y in range(h):
        for x in range(w):
            if seen[y][x]:
                px[x, y] = (0, 0, 0, 0); n += 1
    return im, n


def fit(im):
    """trim to ink and letterbox into a square, so every emblem shares one drawn scale"""
    bb = im.getbbox()
    if bb:
        im = im.crop(bb)
    s = min(SIZE / im.width, SIZE / im.height)
    t = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    cv = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    cv.alpha_composite(t, ((SIZE - t.width) // 2, (SIZE - t.height) // 2))
    return cv


def main():
    write = '--write' in sys.argv
    made, rows = {}, []
    for affil, slug in AFFIL_KEY.items():
        src = os.path.join(GEN, 'af_%s.png' % slug)
        if not os.path.exists(src):
            rows.append((slug, 'MISSING', '-', '-')); continue
        im = Image.open(src)
        before = '%dx%d' % im.size
        keyed, n = key_white(im)
        out = fit(keyed)
        px = out.load()
        ink = sum(1 for y in range(SIZE) for x in range(SIZE) if px[x, y][3] > 8)
        made[slug] = out
        rows.append((slug, before, '%d px keyed' % n, '%.0f%% ink' % (100.0 * ink / (SIZE * SIZE))))

    print('%-13s %-11s %-15s %s' % ('emblem', 'source', 'background', 'result'))
    print('-' * 56)
    for r in rows:
        print('%-13s %-11s %-15s %s' % r)

    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 14)
    except Exception:
        F = ImageFont.load_default()
    T = 150
    # on a mid-grey so a leftover white halo would be obvious - proving the key on black hides it
    proof = Image.new('RGB', (T * 6, T + 40), (86, 90, 98))
    d = ImageDraw.Draw(proof)
    for i, (affil, slug) in enumerate(AFFIL_KEY.items()):
        if slug not in made:
            continue
        proof.paste(made[slug].resize((T - 10, T - 10), Image.LANCZOS), (i * T + 5, 5), made[slug].resize((T - 10, T - 10), Image.LANCZOS))
        d.text((i * T + 4, T + 2), slug, font=F, fill=(255, 255, 255))
        who = ', '.join(k for k, v in PILOT_AFFIL.items() if v == affil)
        d.text((i * T + 4, T + 20), who[:22], font=F, fill=(210, 214, 224))
    proof.save(os.path.join(ROOT, 'docs/AFFILIATIONS_0906.png'))
    print(os.linesep + 'wrote docs/AFFILIATIONS_0906.png (on mid-grey: a white halo would show)')

    if not write:
        print('DRY RUN - nothing written. Re-run with --write.')
        return 0
    os.makedirs(OUT, exist_ok=True)
    for slug, im in made.items():
        im.save(os.path.join(OUT, 'affil_%s.png' % slug))
    print('wrote %d emblems to assets/game/affiliations/' % len(made))
    return 0


if __name__ == '__main__':
    sys.exit(main())
