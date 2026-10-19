#!/usr/bin/env python3
"""mr27_hull_mask_1017.py - measure the modular roster's hull plates (MR27_ART cells[0]) into a coarse
occupancy grid, written to assets/mr27_hull_mask_1017.js as MR27_HULL_MASK.

Why (Mike, 1017: "I cant destroy modular pieces with my bullets"): mr27At's core test was a box
|dx|<w*.37, |dy|<h*.44, which reaches far below the gun turrets - a round coming up from the player
struck "core" on bare road before it ever reached the turret it was aimed at. The core must be the
hull that is actually painted. getImageData cannot be used at runtime (file:// taints the canvas),
so the silhouette is measured here, offline, from the same PNG and the same cell rect the draw uses.

    python _BUILD_SOURCE/mr27_hull_mask_1017.py           # write the mask
    python _BUILD_SOURCE/mr27_hull_mask_1017.py --check   # also save a proof render per skin

Grid: N x N cells over the plate's own rect. A cell is solid when at least FILL of its pixels have
alpha >= ALPHA. Each row is stored as a hex string, bit (N-1-i) of the row = column i.
"""
import os, sys, json, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART_JS = os.path.join(ROOT, 'assets', 'modular_roster_art_0927.js')
OUT_JS = os.path.join(ROOT, 'assets', 'mr27_hull_mask_1017.js')
N = 48
ALPHA = 96
FILL = 0.30
SKINS = ('iron', 'rime', 'storm')

def load_art():
    src = open(ART_JS, encoding='utf-8').read()
    m = re.search(r'const MR27_ART=(\{.*\});', src, re.S)
    return json.loads(m.group(1))

def grid(im):
    w, h = im.size
    a = im.getchannel('A').load()
    rows = []
    for gy in range(N):
        y0, y1 = gy * h // N, max(gy * h // N + 1, (gy + 1) * h // N)
        bits = 0
        for gx in range(N):
            x0, x1 = gx * w // N, max(gx * w // N + 1, (gx + 1) * w // N)
            tot = on = 0
            for y in range(y0, y1):
                for x in range(x0, x1):
                    tot += 1
                    if a[x, y] >= ALPHA: on += 1
            if tot and on / tot >= FILL:
                bits |= 1 << (N - 1 - gx)
        rows.append(bits)
    return rows

def frost_plate():
    # Same two transforms as pt11Plate(hull) and pt11Part(core), before any
    # skin assignment/draw. No runtime pixel reads and no synthetic hit box.
    src = open(os.path.join(ROOT, 'assets', 'playthrough_art_1011.js'), encoding='utf-8').read()
    art = json.loads(re.search(r'const PT11_ART=(\{.*?\});', src, re.S).group(1))['ice_parts']
    hull, core = art[0], art[3]
    im = Image.open(os.path.join(ROOT, hull['path'])).convert('RGBA')
    chip = Image.open(os.path.join(ROOT, core['path'])).convert('RGBA')
    relative = .145 / (300 / 806)
    chip = chip.resize((round(core['w'] * relative), round(core['h'] * relative)), Image.Resampling.NEAREST)
    at = (round(hull['pivot'][0] - core['pivot'][0] * relative), round(hull['pivot'][1] - core['pivot'][1] * relative))
    im.alpha_composite(chip, at)
    return im


def main():
    art = load_art()
    out = {}
    for sk in SKINS:
        d = art[sk]
        r = d['cells'][0]
        im = Image.open(os.path.join(ROOT, d['path'])).convert('RGBA').crop((r[0], r[1], r[0] + r[2], r[1] + r[3]))
        rows = grid(im)
        out[sk] = ['%012x' % v for v in rows]
        solid = sum(bin(v).count('1') for v in rows)
        print('%-6s plate %dx%d  solid %d/%d cells (%.1f%%)' % (sk, r[2], r[3], solid, N * N, 100.0 * solid / (N * N)))
        if '--check' in sys.argv:
            sc = 4
            pr = Image.new('RGBA', (r[2], r[3]), (40, 40, 40, 255)); pr.paste(im, (0, 0), im)
            ov = Image.new('RGBA', pr.size, (0, 0, 0, 0)); px = ov.load()
            for gy, v in enumerate(rows):
                for gx in range(N):
                    if v >> (N - 1 - gx) & 1:
                        for y in range(gy * r[3] // N, (gy + 1) * r[3] // N):
                            for x in range(gx * r[2] // N, (gx + 1) * r[2] // N):
                                if (x + y) % sc == 0: px[x, y] = (0, 255, 0, 150)
            pr = Image.alpha_composite(pr, ov)
            dst = os.path.join(ROOT, '_shots', 'modular_1017'); os.makedirs(dst, exist_ok=True)
            pr.save(os.path.join(dst, 'hullmask_%s.png' % sk))
    frost = frost_plate()
    rows = grid(frost)
    out['pt11_frost'] = ['%012x' % v for v in rows]
    print('pt11_frost hull+core %dx%d solid %d/%d cells' % (*frost.size, sum(bin(v).count('1') for v in rows), N * N))
    if '--check' in sys.argv:
        proof = Image.new('RGBA', frost.size, '#182333'); proof.alpha_composite(frost)
        from PIL import ImageDraw
        pen = ImageDraw.Draw(proof)
        for gy, row in enumerate(rows):
            for gx in range(N):
                if row >> (N - 1 - gx) & 1:
                    pen.rectangle((gx * frost.width / N, gy * frost.height / N, (gx + 1) * frost.width / N - 1, (gy + 1) * frost.height / N - 1), outline='#36c383')
        proof.save(os.path.join(ROOT, '_shots', 'modular_1017', 'hullmask_pt11_frost.png'))
    js = ('"use strict";\n'
          '/* Generated by _BUILD_SOURCE/mr27_hull_mask_1017.py - do not edit by hand.\n'
          '   Current modular hulls, including the mounted Frost carrier core, on a %dx%d grid.\n'
          '   one hex string per row, most significant bit = leftmost column. mr27At reads it so a round\n'
          '   only strikes the core where hull is actually painted (Mike 1017). */\n'
          'const MR27_HULL_MASK={n:%d,rows:%s};\n') % (N, N, N, json.dumps(out, separators=(',', ':')))
    open(OUT_JS, 'w', encoding='utf-8', newline='\n').write(js)
    print('wrote', OUT_JS)

if __name__ == '__main__':
    main()
