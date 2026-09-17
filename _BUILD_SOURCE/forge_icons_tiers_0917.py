#!/usr/bin/env python3
"""
forge_icons_tiers_0917.py - slice the tier II..V sheets (edit_asset_id edits of each weapon's tier-I
sheet) into micon_forge_<elem>_<slot>_<tier>.png, and lay every slot's five tiers on one card.

Mike, 0917: "All icons here should get their level 1-5 upgrade generated variants."

The tier-I badges are already on disk as micon_forge_<elem>_<slot>.png (forge_icons_slice_0917.py);
tiers II..V are the same sheet EDITED (edit_asset_id, never a fresh generation - a fresh generation
redraws the emblem), with the tag numeral and N gems on the frame the only change. Same cut: gutters
from the sheet, a border flood per cell, the rim fringe to a dark edge, FAMILY height.

    python _BUILD_SOURCE/forge_icons_tiers_0917.py            # slice everything present, build the cards
"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import forge_icons_slice_0917 as S

ROOT = S.ROOT; OUT = S.OUT; ELEMS = S.ELEMS; FAMILY_H = S.FAMILY_H
D = os.path.join(ROOT, 'docs', 'proofs', 'forge_icons_0917')
SHEETS = {0: ('gen_mg', 'mg'), 1: ('gen_spread', 'sp'), 2: ('gen_missile', 'ms'), 3: ('gen_laser', 'lz'), 5: ('gen_orb', 'orb'), 7: ('gen_cg', 'cg')}

def slice_sheet(path, slot, tier):
    im = Image.open(path).convert('RGB')
    cols, rows = S.find_cells(im)
    if len(cols) != 3 or len(rows) != 3:
        cols, rows = S.find_cells(im, 200)   # the tier-V glow tints the gutters; a lower floor separates the rows
    if len(cols) != 3 or len(rows) != 3:
        print('  REFUSED %s: %dx%d content runs' % (path, len(cols), len(rows))); return False
    k = 0
    for (y0, y1) in rows:
        for (x0, x1) in cols:
            cell = im.crop((max(0, x0 - 2), max(0, y0 - 2), min(im.width, x1 + 2), min(im.height, y1 + 2)))
            cell, fringe = S.punch(cell)
            bb = cell.getbbox()
            if not bb: print('  REFUSED: empty cell', k); return False
            cell = cell.crop(bb)
            sc = FAMILY_H / cell.height
            cell = cell.resize((max(1, round(cell.width * sc)), FAMILY_H), Image.LANCZOS)
            cell.save(os.path.join(OUT, 'micon_forge_%s_%d_%d.png' % (ELEMS[k], slot, tier)))
            k += 1
    return True

def main():
    os.makedirs(OUT, exist_ok=True)
    done = []
    for slot, (d, pfx) in SHEETS.items():
        for tier in (2, 3, 4, 5):
            p = os.path.join(D, d, '%s_t%d_raw.png' % (pfx, tier))
            if not os.path.exists(p): print('  missing', p); continue
            if slice_sheet(p, slot, tier): done.append((slot, tier)); print('  sliced slot %d tier %d' % (slot, tier))
        # the card: five tiers down, nine elements across
        rows = []
        for tier in (1, 2, 3, 4, 5):
            tiles = []
            for e in ELEMS:
                f = os.path.join(OUT, 'micon_forge_%s_%d%s.png' % (e, slot, '' if tier == 1 else '_%d' % tier))
                tiles.append(Image.open(f).convert('RGBA') if os.path.exists(f) else None)
            rows.append((tier, tiles))
        W = 9 * 124 + 60; H = 5 * (FAMILY_H + 26) + 30
        card = Image.new('RGB', (W, H), (14, 14, 20)); dr = ImageDraw.Draw(card)
        for r, (tier, tiles) in enumerate(rows):
            y = 20 + r * (FAMILY_H + 26); dr.text((6, y + FAMILY_H // 2), ['I', 'II', 'III', 'IV', 'V'][tier - 1], fill=(255, 230, 120))
            for c, t in enumerate(tiles):
                x = 40 + c * 124
                if r == 0: dr.text((x, 4), ELEMS[c], fill=(235, 220, 150))
                if t is not None: card.paste(t, (x, y), t)
                else: dr.rectangle((x, y, x + 100, y + FAMILY_H), outline=(120, 40, 40))
        cp = os.path.join(D, 'slot%d_tiers.png' % slot); card.save(cp); print('  card ->', cp)
    print('%d sheets sliced' % len(done))

if __name__ == '__main__':
    main()
