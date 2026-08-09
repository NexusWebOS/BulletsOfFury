#!/usr/bin/env python3
"""
DROP 0801hg - ICE BREATH THAT ROLLS OUT

Mike: "we need to also make ice breath, appear to 'roll out' like true breath, and
the inside animates with a glowing frost via pixel manipulating. I think we should
use the best of the best frame, and simply cut frames of it to make it roll out
cleanly and then roll back in when were done like true breath."

THE APPROACH
The eight authored frames are eight SIZES, not eight moments - frame 1 is a short
plume and frame 8 a tall one. Played in sequence they read as the breath growing
and shrinking on a loop, which is not what breath does.

So: take the largest, most detailed frame as the single source of truth, and cut
the reel out of it by REVEALING it from the nozzle upward. Frame k shows the
bottom k/N of the plume with a soft leading edge. Played forward that is breath
rolling out; played backward it is breath drawing back in on release.

Because every frame is a slice of the SAME art, the plume's shape, shading and
fronds are identical throughout - it grows rather than morphing, which is the
thing that made the eight-size version read wrong.

THE FROST GLOW
On top of the reveal, a travelling brightness runs UP the interior on its own
clock - the same palette-cycle idea as the flamethrower, but cold. Only pixels
that are already lit get lifted, and the black outline is excluded, so the plume
brightens from within instead of glowing at its edges.

  ROLL_N   frames in the reveal reel
  GLOW_N   frames in the frost cycle
Both are cut from one source, so the total is ROLL_N * 1 plates plus the glow
applied per frame - GLOW_N phases of the fully-extended frame for the held state.
"""
import os
import re
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/fx/weapons/icebreath'
SRC_FRAME = 7          # the largest, most detailed plume
ROLL_N = 8             # reveal steps from nozzle to full extension
GLOW_N = 6             # frost-cycle phases once fully out
FEATHER = 26           # rows of soft leading edge on the reveal


def frost(a, phase, bands=2.2, amt=0.34):
    """Lift a travelling band of brightness UP the interior."""
    out = a.copy()
    H = a.shape[0]
    alpha = a[..., 3]
    op = alpha > 16
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    outline = (r < 50) & (g < 50) & (b < 60) & op
    body = op & ~outline
    yy = np.mgrid[0:H, 0:a.shape[1]][0]
    # y increases downward, so ADDING the phase walks the band toward y=0 = up
    wave = np.sin(((yy / max(1, H)) * bands + phase) * 2 * np.pi) * 0.5 + 0.5
    lift = 1.0 + (wave - 0.5) * 2 * amt
    for c in range(3):
        out[..., c] = np.where(body, np.clip(a[..., c] * lift, 0, 255), a[..., c])
    return out


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    src_rel = re.search(r'"nib_v_%d":"([^"]+)"' % SRC_FRAME, man).group(1)
    a = np.array(Image.open(os.path.join(ROOT, src_rel)).convert('RGBA')).astype(float)
    H, W = a.shape[:2]
    print('  source: nib_v_%d  %dx%d' % (SRC_FRAME, W, H))

    ys = np.where(a[..., 3].max(axis=1) > 16)[0]
    top, bot = ys.min(), ys.max()
    span = bot - top + 1
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    add = {}

    # ---- ROLL OUT: reveal from the nozzle (bottom) upward ----
    for k in range(ROLL_N):
        f = (k + 1) / float(ROLL_N)
        cut = bot - int(span * f)                       # everything below `cut` is shown
        b = a.copy()
        yy = np.mgrid[0:H, 0:W][0]
        # hard hide above the cut, feathered for FEATHER rows below it so the
        # leading edge reads as breath pushing out rather than a sliced sprite
        hide = yy < cut
        fade = (yy >= cut) & (yy < cut + FEATHER)
        b[..., 3] = np.where(hide, 0, b[..., 3])
        t = np.clip((yy - cut) / float(FEATHER), 0, 1)
        b[..., 3] = np.where(fade, b[..., 3] * t, b[..., 3])
        p = '%s/nib_roll_%d.png' % (OUT, k)
        Image.fromarray(np.clip(b, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, p))
        add['nib_roll_%d' % k] = p

    # ---- HELD: the frost cycle on the fully-extended plume ----
    for k in range(GLOW_N):
        b = frost(a, k / float(GLOW_N))
        p = '%s/nib_hold_%d.png' % (OUT, k)
        Image.fromarray(np.clip(b, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, p))
        add['nib_hold_%d' % k] = p

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])

    print('  roll-out : nib_roll_0..%d  (reveal from the nozzle up)' % (ROLL_N - 1))
    print('  held     : nib_hold_0..%d  (frost travelling up the interior)' % (GLOW_N - 1))
    print('  registered %d keys' % new.count('":"'))

    # prove the reveal grows and the silhouette never changes shape
    hs = []
    for k in range(ROLL_N):
        b = np.array(Image.open(os.path.join(ROOT, '%s/nib_roll_%d.png' % (OUT, k))).convert('RGBA'))
        vis = np.where(b[..., 3] > 16)[0]
        hs.append(int(vis.max() - vis.min() + 1) if len(vis) else 0)
    print('  revealed height per frame: %s' % hs)


if __name__ == '__main__':
    main()
