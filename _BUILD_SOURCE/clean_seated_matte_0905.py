#!/usr/bin/env python3
"""
clean_seated_matte_0905.py - strip the leftover white matte from the seated HQ poses.

    python _BUILD_SOURCE/clean_seated_matte_0905.py            # report + preview, write nothing
    python _BUILD_SOURCE/clean_seated_matte_0905.py --apply    # clear it

Mike, 0905, on the seated poses: "remove the white stuck under their arms and stuff."

WHAT IT IS. `cinematic_campaign/seated_poses/*_seated_rgba.png` are nine cut-outs whose background
removal missed the ENCLOSED gaps - the space between an arm and a torso, between two legs - because
those regions are not reachable from the image border. So each figure carries flat near-white
blobs exactly where Mike says: under the arms.

⚠ A FLAT "DELETE WHITE" RULE WOULD EAT REAL ART, and this project has already paid for that once:
   the 0904h caption rule fired on 21 units and deleted 13,313 pixels of which only 6,861 were
   text - the rest was muzzle flash and ejected shells. Falva's boots are cream, Decker's tablet
   screen is lit, and several pilots have white highlights on leather.

   The matte separates from art on THREE measurements taken together, and all three are needed:

     near-white and desaturated   min channel >= 210, max-min <= 26
     FLAT                         per-component RGB std <= 9.5  (art whites are shaded; measured
                                  std 5.0-6.7 on matte against 8.0-10.6 on genuine highlights)
     BIG                          >= 150 px  (a real highlight is a speck; the matte blobs measure
                                  675 to 9,229)

   Verified by rendering the mask in magenta over each figure BEFORE applying it - the regions land
   on underarm gaps and the space between Falva's legs, and Axel, who has no matte, is untouched.

⚠ LIZZIE IS EXCLUDED, AND HER POSE IS DAMAGED RATHER THAN DIRTY. Her alpha is hard 0/255 like the
   others, but her gloves, belt and sleeve panels are washed out to pale opaque GREY - the matte
   removal that produced her file ate into the art instead of stopping at it. Nothing here can fix
   that: deleting those pixels would punch holes in her gloves and vest. She needs regenerating.
   She is listed in SKIP so a later run cannot quietly damage her further.
"""
import io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'assets', 'game', 'cinematic_campaign', 'seated_poses')
SKIP = ('lizzie_seated_rgba.png',)          # damaged art, not matte - see the header
MIN_CH, MAX_SAT, MAX_STD, MIN_PX = 210, 26, 9.5, 150

import numpy as np
from PIL import Image
from scipy import ndimage


def matte_mask(a):
    r, g, b, al = a[:, :, 0], a[:, :, 1], a[:, :, 2], a[:, :, 3]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    cand = (al > 40) & (mn >= MIN_CH) & ((mx - mn) <= MAX_SAT)
    lab, n = ndimage.label(cand)
    out = np.zeros_like(cand)
    hits = []
    for i in range(1, n + 1):
        m = lab == i
        sz = int(m.sum())
        if sz < MIN_PX:
            continue
        v = np.stack([r[m], g[m], b[m]], 1)
        if v.std() > MAX_STD:
            continue
        out |= m
        hits.append((sz, round(float(v.mean()), 1), round(float(v.std()), 2)))
    return out, hits


def main():
    apply = '--apply' in sys.argv
    tot = 0
    print('%-28s %-9s %s' % ('file', 'cleared', 'regions (size, meanRGB, std)'))
    for f in sorted(os.listdir(DIR)):
        if not f.endswith('.png'):
            continue
        if f in SKIP:
            print('%-28s %-9s SKIP - washed-out art, needs regenerating, not cleaning' % (f, '-'))
            continue
        p = os.path.join(DIR, f)
        im = Image.open(p).convert('RGBA')
        a = np.array(im).astype(int)
        m, hits = matte_mask(a)
        tot += int(m.sum())
        print('%-28s %-9d %s' % (f, int(m.sum()), hits if hits else ''))
        if apply and m.any():
            out = np.array(im)
            out[m] = [0, 0, 0, 0]              # the gap is background: clear it, do not paint it
            Image.fromarray(out, 'RGBA').save(p)
    print()
    print('%s  %d px' % ('APPLIED' if apply else 'DRY RUN (pass --apply)', tot))


if __name__ == '__main__':
    main()
