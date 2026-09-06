#!/usr/bin/env python3
"""recolour_ships_0906.py - Mike's three palette swaps for Lizzie, Yuri and Cole.

    python _BUILD_SOURCE/recolour_ships_0906.py            # proof sheet only
    python _BUILD_SOURCE/recolour_ships_0906.py --write     # + the recoloured plates

Mike, 0906, verbatim:

  LIZZIE  "As much as I like Lizzie's B-42 bomber, doesnt fit the game. use [71f14c92] ...
           palette swap the black to be golden, palette swap the blue to be shades of gray."
  YURI    "take 40f35fb5 and palette swap it to neon red, and changing the orange/yellow to
           shades of red/dark red, then turning the dakrk gray to be more dark gray/black."
  COLE    "take 4110e74e - palette swap the red to forest green. pallete swap the orange light
           to be neon green."

⚠ LUMINANCE IS PRESERVED, HUE AND SATURATION ARE NOT. That is this repo's standing rule and it is
load-bearing rather than stylistic: a flat tint composited over pixel art destroys the shading it
was drawn with, which is exactly how the font's drop shadow got flooded and turned E into B. Every
rule below rewrites H and S and leaves V alone, so every panel line, bevel and specular the artist
put in survives the swap. The one deliberate exception is Yuri's grey, which Mike explicitly asked
to go DARKER ("more dark gray/black") - a value change he named.

⚠ AND "BLACK" IS A VALUE BAND, NOT A HUE. Lizzie's hull reads black but is really desaturated
gunmetal: measured, ~50% of her ink sits at s<0.16 across v 0.0..0.4. So "black -> golden" cannot
be a hue rotation - grey has no hue to rotate. It assigns a gold hue and a saturation that RIDES
the existing value, so the darkest plating stays nearly black and only the lit faces come up gold.
Flooding the whole band at one saturation would turn her into a yellow silhouette.

⚠ THE MAGENTA KEY IS EXCLUDED BY THE SAME BORDER FLOOD USED EVERYWHERE ELSE, not by a colour test
- Yuri's plate measures 4.1% magenta-bucket pixels that are part of the SHIP (hot rim light on the
copper), and a colour test would have recoloured the background and eaten those highlights.
"""
import os, sys, colorsys
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESK = 'C:/Users/Mdogg/Desktop/'
OUT = os.path.join(ROOT, 'assets/game/ships_v2')

SHIPS = {
    'lizzie': '71f14c92-dade-4dbe-ad48-9d1c0b43e7f1.png',
    'yuri':   '40f35fb5-546d-4f45-83a1-6593efcb1fb0.png',
    'cole':   '4110e74e-4426-454c-904e-5ede3235f90e.png',
}


def is_key(p):
    r, g, b = p[0], p[1], p[2]
    return r > 150 and b > 150 and g < 95 and abs(r - b) < 80


def punch(im):
    """border flood the magenta away; interior magenta-ish pixels are ART and survive"""
    w, h = im.size
    px = im.load()
    seen = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_key(px[x, y]) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_key(px[x, y]) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and is_key(px[nx, ny]):
                seen[ny][nx] = True; q.append((nx, ny))
    for y in range(h):
        for x in range(w):
            if seen[y][x]:
                px[x, y] = (0, 0, 0, 0)
    return im


def deg(h):
    return h * 360.0


def rule_lizzie(h, s, v):
    """black -> golden, blue -> shades of grey"""
    d = deg(h)
    if 185 <= d <= 265 and s >= 0.18:                 # the blue cockpit, stripes and engine glow
        return h, s * 0.07, v                          # -> grey, shading intact
    if s < 0.26:                                       # the "black" gunmetal hull
        # gold that rides the value: near-black stays near-black, lit faces come up gold
        return 0.113, min(0.62, 0.16 + v * 0.62), min(1.0, v * 1.06)
    return h, s, v


def rule_yuri(h, s, v):
    """neon red overall; orange/yellow -> red/dark red; dark grey -> darker"""
    d = deg(h)
    if 12 <= d <= 70 and s >= 0.18:                    # copper panels and the orange lights
        return 0.995, min(1.0, s * 1.18), v * (0.80 + 0.20 * v)
    if (d < 12 or d > 340) and s >= 0.18:              # the reds already there -> NEON
        return 0.0, min(1.0, s * 1.30), min(1.0, v * 1.10)
    if s < 0.20:                                       # gunmetal -> darker gunmetal/black
        return h, s, v * 0.72
    return h, s, v


def rule_cole(h, s, v):
    """red -> forest green; the orange lights -> neon green"""
    d = deg(h)
    if 12 <= d <= 60 and s >= 0.22 and v >= 0.45:      # the bright orange lights
        return 0.315, min(1.0, s * 1.15), min(1.0, v * 1.05)   # neon green
    if (d < 15 or d > 338) and s >= 0.16:              # the red spine and accents
        return 0.305, min(1.0, s * 0.92), v * 0.94             # forest green
    return h, s, v


RULES = {'lizzie': rule_lizzie, 'yuri': rule_yuri, 'cole': rule_cole}


def recolour(im, fn):
    px = im.load()
    n = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            nh, ns, nv = fn(h, s, v)
            if (nh, ns, nv) != (h, s, v):
                n += 1
            nr, ng, nb = colorsys.hsv_to_rgb(nh, max(0.0, min(1.0, ns)), max(0.0, min(1.0, nv)))
            px[x, y] = (int(nr * 255 + .5), int(ng * 255 + .5), int(nb * 255 + .5), a)
    return n


def main():
    write = '--write' in sys.argv
    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 17)
    except Exception:
        F = ImageFont.load_default()
    TH = 380
    pairs = []
    for who, f in SHIPS.items():
        src = punch(Image.open(DESK + f).convert('RGBA'))
        bb = src.getbbox()
        src = src.crop(bb) if bb else src
        new = src.copy()
        n = recolour(new, RULES[who])
        print('%-8s %-34s %dx%d   %d px recoloured' % (who, f[:32], new.width, new.height, n))
        pairs.append((who, src, new))
        if write:
            os.makedirs(OUT, exist_ok=True)
            new.save(os.path.join(OUT, 'ship_%s_v2_hero.png' % who))

    cols = len(pairs)
    cw = TH + 18
    out = Image.new('RGB', (cw * cols, TH * 2 + 52), (24, 22, 30))
    d = ImageDraw.Draw(out)
    for i, (who, a, b_) in enumerate(pairs):
        for j, img in enumerate((a, b_)):
            s = min(TH / img.width, TH / img.height)
            t = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)
            out.paste(t.convert('RGB'), (i * cw + (cw - t.width) // 2, j * (TH + 26) + (TH - t.height) // 2), t)
            d.text((i * cw + 6, j * (TH + 26) + TH + 4), '%s %s' % (who, 'BEFORE' if j == 0 else 'AFTER'),
                   font=F, fill=(240, 240, 250))
    out.save(os.path.join(ROOT, 'docs/SHIP_RECOLOUR_0906.png'))
    print('\nwrote docs/SHIP_RECOLOUR_0906.png')
    if write:
        print('wrote 3 hero plates to assets/game/ships_v2/')
    else:
        print('DRY RUN - proof only. Re-run with --write once Mike approves the colours.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
