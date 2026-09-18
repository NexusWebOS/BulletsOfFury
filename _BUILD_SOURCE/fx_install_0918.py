#!/usr/bin/env python3
"""
fx_install_0918.py - install the 0918 generated effect animations as 8-frame horizontal strips.

Mike, 0918: "We [need] fire effects in game like burst fire decals for our new upgrades, same with the other
elements. We also need actual fire effects that animate and we need flaming laser beam geysers that take up
sections of the screen. These should all be generated effects."

SpriteCook (generate_game_art -> animate_game_art, spritesheet output, 8 frames each):
  efx_burst_<elem>   the on-hit burst per infusion element (9)       one-shot
  efx_burn           the fire that rides a burning unit               loop
  efx_geyser_<kind>  fire / water / lightning geyser columns          loop

Two repairs, both measured on the returned sheets:
  1. MATTE SPECKS. The animator composites on a #808080 matte and some tail frames keep a few grey pixels
     (and one whole grey disc on the lightning burst's 4th frame). Low-saturation mid-grey pixels are punched
     to alpha - NOT on the chrome burst, whose silver IS low-saturation grey; chrome was re-animated on a
     magenta matte instead.
  2. SQUARE GEYSER FRAMES. The 1:2 geyser sources came back framed in 256x256 cells, mostly empty. Each
     strip is cropped to the UNION of its frames' ink columns so every frame keeps one shared anchor (a
     per-frame crop would make the column jitter sideways).

    python _BUILD_SOURCE/fx_install_0918.py <folder with a_*.png>
"""
import os, sys, colorsys
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(ROOT, 'assets', 'game', 'fx_0918')
N = 8

def degrey(im):
    px = im.load(); n = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a: continue
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            if s < 0.14 and 0.27 <= v <= 0.78:
                px[x, y] = (0, 0, 0, 0); n += 1
    return n

def chrome_strip(src):
    """THE CHROME BURST, ASSEMBLED. Both renders turned the scattering shards into a solid silver DISC from frame
    4 on (the first on the grey matte, the retry on magenta with Pro removal) - the model's reading of 'reflective
    core', not a matte fault. Its first three frames are good (flash, burst, full scatter), so the strip is those
    three plus the scatter frame flung outward and fading - generated pixels, only re-timed."""
    im = Image.open(os.path.join(src, 'a_chrome_grey.png')).convert('RGBA'); fw, fh = im.width // N, im.height
    frames = [im.crop((i*fw, 0, (i+1)*fw, fh)) for i in range(3)]
    last = frames[2]
    for k, (sc, al) in enumerate([(1.10, .80), (1.20, .60), (1.30, .42), (1.40, .25), (1.50, .10)]):
        big = last.resize((int(fw*sc), int(fh*sc)), Image.NEAREST)
        cx = (big.width - fw)//2; big = big.crop((cx, cx, cx+fw, cx+fh))
        a = big.split()[3].point(lambda v, al=al: int(v*al)); big.putalpha(a); frames.append(big)
    out = Image.new('RGBA', (fw*N, fh), (0, 0, 0, 0))
    for i, f in enumerate(frames): out.paste(f, (i*fw, 0))
    out.save(os.path.join(src, 'a_chrome.png'))

def main(src):
    if os.path.exists(os.path.join(src, 'a_chrome_grey.png')): chrome_strip(src)
    os.makedirs(OUT, exist_ok=True)
    jobs = [('a_%s.png' % e, 'efx_burst_%s.png' % e, 'burst') for e in
            ['fire', 'ice', 'lightning', 'prism', 'toxic', 'kinetic', 'water', 'chrome', 'dark']]
    jobs += [('a_burn.png', 'efx_burn.png', 'burn')]
    jobs += [('a_g%s.png' % k, 'efx_geyser_%s.png' % k, 'geyser') for k in ['fire', 'water', 'lightning']]
    for a, b, kind in jobs:
        p = os.path.join(src, a)
        if not os.path.exists(p): print('  missing', a); continue
        im = Image.open(p).convert('RGBA')
        assert im.width % N == 0, (a, im.size)
        fw, fh = im.width // N, im.height
        n = 0 if 'chrome' in a else degrey(im)
        if kind == 'geyser':
            x0, x1 = fw, 0
            for i in range(N):
                bb = im.crop((i*fw, 0, (i+1)*fw, fh)).getbbox()
                if bb: x0 = min(x0, bb[0]); x1 = max(x1, bb[2])
            x0 = max(0, x0 - 2); x1 = min(fw, x1 + 2); cw = x1 - x0
            out = Image.new('RGBA', (cw*N, fh), (0, 0, 0, 0))
            for i in range(N): out.paste(im.crop((i*fw + x0, 0, i*fw + x1, fh)), (i*cw, 0))
            im = out; fw = cw
            # the source frame CUT the crown flat (the fire column's dark smoke ends in a hard line - seen in
            # the first in-game frame); the top 22% of every frame fades to nothing so the column dissolves
            fade = int(fh*0.22); px = im.load()
            for y in range(fade):
                k = y/float(fade)
                for x in range(im.width):
                    r, g, b2, a2 = px[x, y]
                    if a2: px[x, y] = (r, g, b2, int(a2*k))
        im.save(os.path.join(OUT, b))
        print('  %-24s %dx%d cells, %d matte px punched' % (b, fw, fh, n))

if __name__ == '__main__':
    main(sys.argv[1])
