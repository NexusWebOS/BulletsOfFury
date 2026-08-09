#!/usr/bin/env python3
"""
DROP 0801hl - THE 12 BOSS FIRE FX SETS

Mike: "all projecticles must be rotated to face verticall south. clean all purple
halo's. black edge all projecticles or blue or green or red depending on what the
projectile is. magma - thesee all actually look good to me. they can go with the
enemies they state, our red tanks can get the legion command sprites."

WHAT THIS IS
CF_BossFireFX-Vol_2 carries a projectile, a muzzleflash and an impact burst for
each of twelve bosses - 216 frames - and not one of them was registered. Every
boss has been firing the generic mfx_ round instead of its own authored ammunition.

THREE CORRECTIONS PER FRAME

1. ROTATE TO SOUTH. Every frame is authored pointing EAST - measured on magma:
   241px wide against 95px tall. The game fires down the screen, so each is turned
   90 degrees clockwise. Muzzleflash and impact are radial and do not care, but
   they are turned too so a set stays internally consistent if anyone ever aligns
   one to a barrel.

2. PURPLE HALO -> BLACK. The alpha key leaves a magenta cast on the anti-aliased
   rim - 926px on magma's first frame alone. Darkened, never deleted: deleting the
   halo eats the outline and the sprite frays. Mike's standing rule from the chroma
   work.

3. EDGE BY COLOUR, not uniformly. Mike: "black edge all projecticles or blue or
   green or red depending on what the projectile is." The edge is picked from the
   frame's own dominant hue so a green acid round gets a deep green rim and a blue
   cryo round a deep blue one - the outline reads as part of the shot rather than
   a black sticker on it. Neutral and pale rounds fall back to black.

NAMING
  bfx_<slug>_p_<n>   projectile
  bfx_<slug>_m_<n>   muzzleflash
  bfx_<slug>_i_<n>   impact
Twelve slugs, three kinds, six frames.
"""
import os
import re
import glob
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PACK = '/tmp/bfx'
OUT = 'assets/fx/bossfire'

# slug -> the short key used in the manifest, and which unit fields it
UNITS = {
    'magma-colossus':             ('magma',   'stage 2 boss'),
    'cryo-behemoth':              ('cryo',    'stage 3 boss'),
    'storm-sovereign':            ('storm',   'stage 6 boss'),
    'toxic-leviathan':            ('toxic',   'stage 7 boss'),
    'rampart-zero':               ('rampart', 'stage 5 boss'),
    'warhawk-arsenal':            ('warhawk', 'stage 4 boss'),
    'obsidian-drill-tank':        ('obsid',   'stage 2 miniboss'),
    'glacier-rail-fortress':      ('glacier', 'stage 3 miniboss'),
    'legion-command-tank':        ('legion',  'the RED TANKS - Mike'),
    'mirv-stalker':               ('mirv',    'missile fodder'),
    'sludge-crawler':             ('sludge',  'stage 7 crawler'),
    'cyclone-interceptor-carrier':('cyclone', 'stage 6 carrier'),
}
KINDS = {'projectile': 'p', 'muzzleflash': 'm', 'impact': 'i'}


def edge_colour(px):
    """Pick the rim from the frame's own dominant hue."""
    r, g, b = px[:, 0].mean(), px[:, 1].mean(), px[:, 2].mean()
    mx = max(r, g, b)
    if mx < 70:
        return (0, 0, 0)
    if r > g + 26 and r > b + 26:
        return (96, 10, 6)       # deep red for the fire rounds
    if g > r + 22 and g > b + 12:
        return (10, 74, 20)      # deep green for the acid rounds
    if b > r + 26:
        return (10, 26, 96)      # deep blue for the cryo and storm rounds
    return (0, 0, 0)


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    add = {}
    stats = {'rot': 0, 'halo': 0, 'edge': 0}
    per_unit = {}

    for slug, (short, who) in UNITS.items():
        edges = []
        for kind, kc in KINDS.items():
            files = sorted(glob.glob('%s/**/%s-%s-alpha-*.png' % (PACK, slug, kind), recursive=True))
            files = [f for f in files if 'atlas' not in f]
            for n, f in enumerate(files[:6]):
                a = np.array(Image.open(f).convert('RGBA')).astype(float)

                # 1. face SOUTH
                a = np.rot90(a, k=-1).copy()
                stats['rot'] += 1

                # trim to the art
                op = a[..., 3] > 16
                if not op.any():
                    continue
                ys, xs = np.where(op)
                a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
                op = a[..., 3] > 16

                # 2. purple halo -> black, never deleted
                r, g, b = a[..., 0], a[..., 1], a[..., 2]
                pur = op & (b > g + 25) & (r > g + 15)
                for c in range(3):
                    a[..., c] = np.where(pur, a[..., c] * 0.10, a[..., c])
                stats['halo'] += int(pur.sum())

                # 3. edge in the frame's own colour
                px = a[..., :3][op]
                ec = edge_colour(px)
                edges.append(ec)
                a = np.pad(a, ((1, 1), (1, 1), (0, 0)))
                alpha = a[..., 3] > 16
                edge = ndimage.binary_dilation(alpha, iterations=1) & ~alpha
                a[..., 0][edge], a[..., 1][edge], a[..., 2][edge] = ec
                a[..., 3][edge] = 255
                stats['edge'] += int(edge.sum())

                k = 'bfx_%s_%s_%d' % (short, kc, n)
                rel = '%s/%s.png' % (OUT, k)
                Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))
                add[k] = rel
        if edges:
            from collections import Counter
            per_unit[short] = (Counter(edges).most_common(1)[0][0], who)

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])

    print('  registered %d frames across %d bosses' % (len(add), len(UNITS)))
    print('  rotated to south : %d' % stats['rot'])
    print('  purple -> black  : %d px' % stats['halo'])
    print('  edge drawn       : %d px' % stats['edge'])
    print()
    NAME = {(0, 0, 0): 'black', (96, 10, 6): 'red', (10, 74, 20): 'green', (10, 26, 96): 'blue'}
    for short, (ec, who) in sorted(per_unit.items()):
        print('   %-9s %-6s edge   %s' % (short, NAME.get(ec, '?'), who))


if __name__ == '__main__':
    main()
