#!/usr/bin/env python3
"""
chaingun_icons_0916.py - THE CHAINGUN GETS ICONS IN THE HOUSE STYLE.

    python3 _BUILD_SOURCE/chaingun_icons_0916.py [--check]

Mike, 0916, with a strip of four weapon icons in which the chaingun is the odd one out: "generatre
new chaingun icons to match our current style of icons."

Rendered side by side, the style is unmistakable and the chaingun has none of it. Every weapon icon
in `bof_player_weapon_special_icons.png` is a FRAMED BADGE: a bevelled ring - RED for the gun
family (mg, spread, missile), green for the specials - around a dark field holding the weapon's
emblem, with a metal tag at the bottom carrying the tier in Roman numerals. The chaingun's are five
loose 64x64 sprites with a small blue number under them and no frame at all.

⚠ SO THE ICON IS NOT DRAWN FROM SCRATCH - IT IS TWO PIECES OF AUTHORED ART COMPOSITED. CLAUDE.md's
first standing rule is never to create a placeholder or procedural sprite and to search the existing
art first; both halves already exist and are already Mike's:
  * the FRAME and its tier tag come from `micon_icebreath_N` - the SPECIAL family's green hex, which
    is the badge the chaingun's own neighbours wear in the strip he sent (thermoshock, ice breath,
    lightning orb). Taking tier N's own badge means the Roman numeral, the tag and the frame are the
    authored ones rather than something re-invented per tier.
  * the EMBLEM is the chaingun art already shipping as `chaingun_icon_N` - the part of those files
    that was always fine. It is cut out, fitted to the frame's interior and re-seated.

⚠ THE GUN FAMILY'S BADGE WAS THE FIRST CHOICE AND IT WAS WRONG, WHICH ONLY THE RENDER SHOWED.
`micon_mg_N` is colour-coded PER TIER (orange, blue, green, silver, red - the machine gun's own tier
colours from 0812d) and its interior FIELD is saturated, not dark. So a chaingun built on it would
change colour every tier for reasons that have nothing to do with the chaingun, and the
flood-from-the-centre below escaped through the field on three of the five tiers. The specials are
green at every tier over a DARK field, which is both the right neighbourhood and the tractable one.

⚠ THE INTERIOR IS A PER-ROW SPAN, NOT THE FLOOD ITSELF. Flooding from the centre stops at the
EMBLEM as well as at the ring - the crystal in the donor badge is bright and saturated - so the
flood alone leaves the old emblem's own pixels unmasked and they survive into the new icon. Taking,
for each row, everything BETWEEN the leftmost and rightmost flooded pixel fills the emblem back in
and gives the hexagon the art actually has, without a hexagon being assumed anywhere.

⚠ AND THE FIELD IS SAMPLED PER ROW. The interior is not flat: it carries a vignette. Each row is
refilled with the median of that row's own field pixels, so a cleared interior keeps the shading the
badge already had instead of becoming a flat slab.
"""
import os, sys, argparse, colorsys
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ATLAS = os.path.join(ROOT, 'assets', 'game', 'atlas', 'bof_player_weapon_special_icons.png')
ARCH = os.path.join(ROOT, 'assets', 'game', 'stage5_archmage_0916')
OUT = os.path.join(ROOT, 'docs', 'proofs', 'chaingun_icons_0916')

# the SPECIAL family's badges, tier by tier, straight out of the manifest (micon_icebreath_1..5)
MG = {1: (144, 520, 96, 112), 2: (271, 520, 97, 112), 3: (399, 520, 98, 112),
      4: (527, 520, 97, 112), 5: (654, 520, 99, 112)}


def chroma(px):
    r, g, b, a = px
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    return s * v


def near_black(p):
    """the badge's FIELD: pure black, measured - 0..12 across the donor's middle row"""
    return p[3] > 8 and (p[0] + p[1] + p[2]) <= 40 and chroma(p) <= 0.12


def interior_mask(im):
    """The badge's interior, found by walking the layers the art actually has.

       ⚠ THREE CUTS FAILED BEFORE THIS ONE AND EACH TAUGHT SOMETHING:
       1. flood from the centre - the centre is the EMBLEM, so it flooded nothing;
       2. largest enclosed black island - the ring is SEGMENTED and its joints are near-black, so
          the field and the outer outline are one connected region and this returned 7x3px pockets;
       3. bounded by the GREEN ring - only tier 3 is green. The badges are colour-coded per TIER
          (orange, blue, green, silver, red), which is also why every icon in the strip Mike sent is
          green: they are all tier 3. A hue-specific rule found no ring at all on four of five.
       Brightness alone does not work either: tier 2's ring is a DARK blue that reads as field.

       What every tier does have is the same LAYER ORDER across a row - outline, ring, field - so
       the interior starts at the first near-black pixel AFTER the first non-near-black run. Rows
       are limited to the hex by width: the tier tag hangs below and is ~45% of the hex's span, so
       rows narrower than 62% of the widest are left alone and the Roman numeral is untouched."""
    w, h = im.size
    px = im.load()
    widths = [sum(1 for x in range(w) if px[x, y][3] > 8) for y in range(h)]
    mx = max(widths) or 1
    out = Image.new('L', (w, h), 0)
    op = out.load()
    spans = {}
    # 1. the ring's THICKNESS, from the rows where the walk is unambiguous
    ts, us = [], []
    rows = [y for y in range(h) if widths[y] >= 0.62 * mx]
    for y in rows:
        xs = [x for x in range(w) if px[x, y][3] > 8]
        if not xs:
            continue
        lo, hi = min(xs), max(xs)
        i = lo
        while i <= hi and near_black(px[i, y]):
            i += 1
        while i <= hi and not near_black(px[i, y]):
            i += 1
        j = hi
        while j >= lo and near_black(px[j, y]):
            j -= 1
        while j >= lo and not near_black(px[j, y]):
            j -= 1
        if j - i >= 6:
            ts.append(i - lo)
            us.append(hi - j)
    if not ts:
        return out
    ts.sort(); us.sort()
    tl, tr = ts[len(ts) // 2], us[len(us) // 2]

    # 2. ⚠ THE SPAN IS THE RING'S THICKNESS INSET FROM THE ALPHA EDGE, NOT THE PER-ROW WALK. Where
    #    the donor's emblem TOUCHES the ring - the crystal's rays do, low on tiers 4 and 5 - the walk
    #    runs straight through it and the ray outside the landing point survives into the new icon.
    #    It showed as blue streaks in the badge's lower corners. The ring is a constant width on a
    #    hex, so the median inset measured above holds for every row and no row depends on its own
    #    pixels being clean.
    # 3. ⚠ AND THE TIER TAG IS PROTECTED BY ITS OWN GEOMETRY, NOT BY "anything bright down low".
    #    The first guard protected every non-field pixel in the bottom 38% - which is where the
    #    DONOR'S EMBLEM also is, so the crystal survived below a hard horizontal edge across the
    #    badge. The tag is the narrow tail below the hex: measured, rows 99..111 and x 19..79, about
    #    58-61% of the width on every tier. Only its own columns, and only from a little above where
    #    it starts, are held back - so the field clears and the Roman numeral is untouched.
    narrow = [y for y in range(h) if 0 < widths[y] < 0.62 * mx and y > h * 0.6]
    tag = [[False] * h for _ in range(w)]
    if narrow:
        txs = [x for y in narrow for x in range(w) if px[x, y][3] > 8]
        tx0, tx1 = min(txs) - 2, max(txs) + 2
        ttop = min(narrow) - 10
        for y in range(max(0, ttop), h):
            for x in range(max(0, tx0), min(w, tx1 + 1)):
                if px[x, y][3] > 8 and not near_black(px[x, y]):
                    tag[x][y] = True
    for y in rows:
        xs = [x for x in range(w) if px[x, y][3] > 8]
        if not xs:
            continue
        lo, hi = min(xs), max(xs)
        a, b = lo + tl, hi - tr
        if b - a < 6:
            continue
        spans[y] = (a, b)
    for y, (i, j) in spans.items():
        for x in range(i, j + 1):
            if px[x, y][3] > 8 and not tag[x][y]:
                op[x, y] = 255
    return out


def field_colour(im, mask):
    """kept for the proof print: the interior's median brightness"""
    px, mp = im.load(), mask.load()
    vals = []
    for y in range(im.height):
        for x in range(im.width):
            if mp[x, y]:
                vals.append(px[x, y][:3])
    if not vals:
        return (12, 12, 16)
    vals.sort(key=lambda c: c[0] + c[1] + c[2])
    return vals[len(vals) // 2]


def clear_interior(im, mask, flood_hint):
    """Refill the interior with ITS OWN field, row by row, so the vignette survives."""
    out = im.copy()
    px, mp, op = im.load(), mask.load(), out.load()
    rows = []
    for y in range(im.height):
        band = [px[x, y][:3] for x in range(im.width)
                if mp[x, y] and near_black(px[x, y])]
        if band:
            band.sort(key=lambda c: c[0] + c[1] + c[2])
            rows.append((y, band[len(band) // 2]))
    if not rows:
        return out
    lut = dict(rows)
    ys = sorted(lut)
    for y in range(im.height):
        if y in lut:
            c = lut[y]
        else:                                   # rows the emblem filled entirely: nearest field row
            c = lut[min(ys, key=lambda q: abs(q - y))]
        for x in range(im.width):
            if mp[x, y]:
                op[x, y] = c + (255,)
    return out


def trim(im):
    b = im.getbbox()
    return im.crop(b) if b else im


def drop_tag(im):
    """Cut the old icon's own tier tag off before anything else.

       ⚠ TAKING THE LARGEST CONNECTED ISLAND IS NOT ENOUGH: on tiers 3, 4 and 5 the tag TOUCHES the
       gun, so the island is both and the tag rode into the badge - a second, smaller numeral above
       the authored one. Measured on the row profile, every one of the five files has the same
       shape: the gun tapers, a gap of 1-3 inked pixels per row, then the tag as a solid band. The
       cut is that gap, found from the bottom up, so it is the art's own boundary rather than a
       fraction picked to fit."""
    w, h = im.size
    px = im.load()
    prof = [sum(1 for x in range(w) if px[x, y][3] > 16) for y in range(h)]
    inked = [y for y in range(h) if prof[y]]
    if not inked:
        return im
    low = max(prof[int(h * 0.55):] or [0])
    y = inked[-1]
    while y > 0 and prof[y] >= 0.45 * low:
        y -= 1
    return im.crop((0, 0, w, max(1, y + 1)))


def emblem(im):
    """The gun alone.

       ⚠ THE OLD ICON FILES CARRY THEIR OWN LITTLE BLUE TIER TAG under the sprite, and trimming to
       the bounding box brings it along - the first render had a second, smaller 'I' sitting inside
       the badge above the authored one. The gun is the largest connected island of ink in the file
       and the tag is a separate one, so the emblem is that island's box and nothing else."""
    w, h = im.size
    px = im.load()
    seen = [[False] * h for _ in range(w)]
    best, bestbox = 0, None
    for sy in range(h):
        for sx in range(w):
            if seen[sx][sy] or px[sx, sy][3] <= 16:
                continue
            st = [(sx, sy)]
            n = 0
            x0 = x1 = sx
            y0 = y1 = sy
            while st:
                x, y = st.pop()
                if x < 0 or y < 0 or x >= w or y >= h or seen[x][y] or px[x, y][3] <= 16:
                    continue
                seen[x][y] = True
                n += 1
                x0, x1 = min(x0, x), max(x1, x)
                y0, y1 = min(y0, y), max(y1, y)
                st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
                       (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]
            if n > best:
                best, bestbox = n, (x0, y0, x1 + 1, y1 + 1)
    return im.crop(bestbox) if bestbox else trim(im)


def build(tier, atlas):
    r = MG[tier]
    badge = atlas.crop((r[0], r[1], r[0] + r[2], r[1] + r[3])).copy()
    mask = interior_mask(badge)
    mask = mask.filter(ImageFilter.MinFilter(3))       # keep off the ring's inner bevel
    cleared = clear_interior(badge, mask, None)

    gun = emblem(drop_tag(Image.open(os.path.join(ARCH, 'chaingun_icon_%d.pre0916.png' % tier)
                          if os.path.exists(os.path.join(ARCH, 'chaingun_icon_%d.pre0916.png' % tier))
                          else os.path.join(ARCH, 'chaingun_icon_%d.png' % tier)).convert('RGBA')))
    bb = mask.getbbox()
    iw, ih = bb[2] - bb[0], bb[3] - bb[1]
    tw, th = int(iw * 0.88), int(ih * 0.88)
    k = min(tw / gun.width, th / gun.height)
    gw, gh = max(1, int(gun.width * k)), max(1, int(gun.height * k))
    gun = gun.resize((gw, gh), Image.LANCZOS)
    layer = Image.new('RGBA', badge.size, (0, 0, 0, 0))
    layer.alpha_composite(gun, (bb[0] + (iw - gw) // 2, bb[1] + (ih - gh) // 2))
    # ⚠ CLIPPED TO THE INTERIOR: a sprite fitted by its bounding box still pokes a corner over the
    # bevel of a HEX interior, which no rectangle fits inside.
    layer.putalpha(Image.composite(layer.getchannel('A'), Image.new('L', badge.size, 0), mask))
    cleared.alpha_composite(layer)
    return cleared, mask


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    atlas = Image.open(ATLAS).convert('RGBA')
    made = []
    for t in (1, 2, 3, 4, 5):
        ic, mask = build(t, atlas)
        made.append((t, ic, mask))
        print('tier %d  %dx%d  interior %s' % (t, ic.width, ic.height, mask.getbbox()))

    if a.check:
        Z = 3; pad = 10
        rows = []
        for t, ic, mask in made:
            _p = os.path.join(ARCH, 'chaingun_icon_%d.pre0916.png' % t)
            old = Image.open(_p if os.path.exists(_p) else os.path.join(ARCH, 'chaingun_icon_%d.png' % t)).convert('RGBA')
            rows.append((t, old, ic, atlas.crop((MG[t][0], MG[t][1], MG[t][0] + MG[t][2], MG[t][1] + MG[t][3]))))
        W = 150 + (max(r[2].width for r in rows) * 3 + 20) * Z
        H = sum(max(r[1].height, r[2].height) * Z + pad for r in rows) + pad
        card = Image.new('RGBA', (W, H), (28, 30, 38, 255))
        d = ImageDraw.Draw(card); y = pad
        for t, old, ic, mg in rows:
            x = 150
            for lab, im in (('was', old), ('donor', mg), ('now', ic)):
                im2 = im.resize((im.width * Z, im.height * Z), Image.NEAREST)
                card.alpha_composite(im2, (x, y)); x += im2.width + 16
            d.text((8, y + 20), 'chaingun %d' % t, fill=(255, 210, 140, 255))
            y += max(old.height, ic.height) * Z + pad
        p = os.path.join(OUT, '01_new_icons.png')
        card.save(p); print('--check: wrote', os.path.relpath(p, ROOT))
        return

    for t, ic, _ in made:
        dst = os.path.join(ARCH, 'chaingun_icon_%d.png' % t)
        bak = os.path.join(ARCH, 'chaingun_icon_%d.pre0916.png' % t)
        if not os.path.exists(bak):
            os.rename(dst, bak)          # the old sprite is kept, never overwritten
        ic.save(dst)
        print('wrote %s (old kept as %s)' % (os.path.relpath(dst, ROOT), os.path.basename(bak)))


if __name__ == '__main__':
    main()
