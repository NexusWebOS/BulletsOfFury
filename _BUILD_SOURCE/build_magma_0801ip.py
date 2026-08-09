#!/usr/bin/env python3
"""
DROP 0801ip - THE MAGMA COLOSSUS, BUILT FROM ITS POSE SHEET

Mike: "the mega boss, your using the wrong graphics. wire up the ones including the
one where his head and torsa were one piece, each piece needs to be scaled down to
where the bosses total size is 192x256 or 256x256, not each piece. and no purple
halo's no magenta."

WHAT WAS WRONG
The game draws the boss from mbg2_p_* - eight SEPARATE limb plates, each on its own
384x384 canvas, assembled by mechDraw. Mike wants the mbg2_pose_* set instead:
eight whole-body poses with head and torso as one piece.

  aim-left   aim-right   dual-wide   neutral
  recoil-left  recoil-right  twist-left  twist-right

THE SIZE RULE
"the bosses TOTAL size is 192x256 or 256x256, not each piece." The source poses are
384x384 with the figure filling most of it. Each is trimmed to its own art, then
scaled so the WHOLE BOSS fits 256x256 - not each plate scaled independently, which
would make the limbs disagree.

All eight are scaled by ONE factor, derived from the largest pose, so they stay in
proportion with each other. A boss that changed size between poses would read as
breathing in and out.

NO PURPLE, NO MAGENTA
Both are stripped: the magenta key is cut to alpha, and the purple halo the key
leaves on the anti-aliased rim is darkened to black rather than deleted, which is
Mike's standing rule - deleting the halo eats the outline and the sprite frays.
"""
import os
import re
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma'
TARGET = 256          # the whole boss, per Mike


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)

    keys = sorted(set(re.findall(r'"(mbg2_pose_[a-z-]+)":', man)))
    if not keys:
        print('  no pose keys'); return

    # PASS 1 - trim every pose and find the largest, so one scale serves them all
    trimmed = {}
    for k in keys:
        m = re.search(r'"%s":"([^"]+)"' % k, man)
        p = os.path.join(ROOT, m.group(1))
        if not os.path.exists(p):
            continue
        a = np.array(Image.open(p).convert('RGBA')).astype(float)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]

        # magenta key -> alpha
        key = (r > 190) & (g < 90) & (b > 190)
        a[..., 3] = np.where(key, 0, a[..., 3])
        op = a[..., 3] > 16
        if not op.any():
            continue

        # purple halo -> black, never deleted
        pur = op & (b > g + 22) & (r > g + 14)
        for c in range(3):
            a[..., c] = np.where(pur, a[..., c] * 0.10, a[..., c])

        ys, xs = np.where(op)
        trimmed[k] = (a[ys.min():ys.max() + 1, xs.min():xs.max() + 1], int(pur.sum()))

    if not trimmed:
        print('  nothing usable'); return
    maxW = max(v[0].shape[1] for v in trimmed.values())
    maxH = max(v[0].shape[0] for v in trimmed.values())
    scale = min(TARGET / float(maxW), TARGET / float(maxH))
    print('  largest pose %dx%d  ->  scale %.3f  so the WHOLE boss fits %d'
          % (maxW, maxH, scale, TARGET))

    add = {}
    halo = 0
    for k, (a, pur) in sorted(trimmed.items()):
        halo += pur
        h, w = a.shape[:2]
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
        im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)

        # CLEAN AFTER THE RESIZE TOO (drop 0801ip). LANCZOS blends neighbouring
        # pixels, so a red edge next to a keyed-out magenta pixel lands back in
        # purple - 1 to 11 px per pose survived a pre-resize clean. Doing it again
        # on the scaled result catches what interpolation reintroduces.
        b2 = np.array(im).astype(float)
        op2 = b2[..., 3] > 16
        rr, gg, bb = b2[..., 0], b2[..., 1], b2[..., 2]
        pur2 = op2 & (bb > gg + 22) & (rr > gg + 14)
        for c in range(3):
            b2[..., c] = np.where(pur2, b2[..., c] * 0.10, b2[..., c])
        im = Image.fromarray(np.clip(b2, 0, 255).astype(np.uint8), 'RGBA')

        # centre on one common canvas so a pose change never shifts the boss
        canvas = Image.new('RGBA', (TARGET, TARGET), (0, 0, 0, 0))
        canvas.alpha_composite(im, ((TARGET - im.width) // 2, (TARGET - im.height) // 2))

        nk = k.replace('mbg2_pose_', 'mgx_')
        rel = '%s/%s.png' % (OUT, nk)
        canvas.save(os.path.join(ROOT, rel))
        add[nk] = rel

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])

    print('  %d poses at %dx%d, one common canvas' % (len(add), TARGET, TARGET))
    print('  purple halo darkened: %d px' % halo)

    # prove it: no magenta, no purple, and every pose the same size
    man2 = open(man_path, encoding='utf-8').read()
    bad = 0
    for k in add:
        p = os.path.join(ROOT, re.search(r'"%s":"([^"]+)"' % k, man2).group(1))
        a = np.array(Image.open(p).convert('RGBA')).astype(int)
        op = a[..., 3] > 16
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        mag = int((op & (r > 190) & (g < 90) & (b > 190)).sum())
        pur = int((op & (b > g + 22) & (r > g + 14)).sum())
        if mag or pur:
            print('   %s: magenta %d  purple %d' % (k, mag, pur)); bad += 1
    print('  magenta / purple remaining: %s' % ('none' if bad == 0 else '%d poses still dirty' % bad))


if __name__ == '__main__':
    main()
