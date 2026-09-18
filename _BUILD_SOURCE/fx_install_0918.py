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

def degrey(im, lo=0.27, hi=0.78, smax=0.14):
    px = im.load(); n = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a: continue
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            if s < smax and lo <= v <= hi:
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

# 0918b: THE BURSTS WERE CUT OFF. An explosion grows to fill its animation cell, so on the middle frames the
# ink runs into the cell's edge and ends in a straight line - "spliced incorrectly and cut off" (Mike).
# Re-animating with the widest margin the tool allows (edge_margin 25) still touches the edge on frames 2-4,
# so the edge is SOFTENED here: every burst frame's alpha fades to nothing across the outer ring of its
# cell (a circle, so the burst reads round, never square), and the last two frames fade out so a burst
# dissolves rather than stopping on its final grey speck.
VIGNETTE = (0.36, 0.5)      # radius (share of the cell) where the fade starts / reaches zero
TAIL = {6: 0.62, 7: 0.28}   # alpha kept on the tail frames

def burst_soften(im, fw, fh):
    px = im.load(); cx, cy = (fw - 1) / 2.0, (fh - 1) / 2.0; r0, r1 = VIGNETTE
    for i in range(N):
        tk = TAIL.get(i, 1.0)
        for y in range(fh):
            for x in range(fw):
                r, g, b, a = px[i*fw + x, y]
                if not a: continue
                d = (((x - cx) / fw) ** 2 + ((y - cy) / fh) ** 2) ** 0.5
                k = 1.0 if d <= r0 else max(0.0, (r1 - d) / (r1 - r0))
                k = k * k * (3 - 2 * k)   # smoothstep
                px[i*fw + x, y] = (r, g, b, int(a * k * tk))

# 0918b: THE GEYSER'S BOTTOM WAS A ROCK VENT, and Mike: "remove the geyser bottom effect and just use the fire
# animation". The vent rows are cut off each strip (measured per kind on the rendered strips) and the new base
# fades in over VENT_FADE rows so the column rises out of nothing.
VENT = {'fire': 20, 'water': 6, 'lightning': 12}
VENT_FADE = 18

def main(src):
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
        # chrome's silver IS low-saturation grey; only the matte's own mid-band is punched there
        n = degrey(im, 0.40, 0.62, 0.06) if 'chrome' in a else degrey(im)
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
        if kind == 'burst': burst_soften(im, fw, fh)
        if kind == 'geyser':
            k = a[3:-4]; cut = VENT[k]; fh -= cut
            im = im.crop((0, 0, im.width, fh)); px = im.load()
            for y in range(fh - VENT_FADE, fh):
                kk = (fh - 1 - y) / float(VENT_FADE)
                for x in range(im.width):
                    r, g, b2, a2 = px[x, y]
                    if a2: px[x, y] = (r, g, b2, int(a2 * kk))
        im.save(os.path.join(OUT, b))
        print('  %-24s %dx%d cells, %d matte px punched' % (b, fw, fh, n))

if __name__ == '__main__':
    main(sys.argv[1])
