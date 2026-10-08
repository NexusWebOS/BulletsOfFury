"""fusion_beam_1002 - the Fusion beam as a SOLID pink-purple plasma column (Mike, 1002).

    python3 _BUILD_SOURCE/fusion_beam_1002.py

"the fusion cannon beams. they should not be spikey lasers, that makes no sense at all. solid pink beams like
falva's laser beams, but more 'Fusion' energy like while still pinkishpurple."

Source: _BUILD_SOURCE/fusion_beam_spritecook_1002.png - a SpriteCook EDIT of Falva's own laser plate (fllaser_0),
so it keeps her solid capsule: a pink-violet sheath, a white-hot core and a contained double helix of plasma.
Output: assets/game/shared/player_weapons/fusion_1002/beam.png, an 8-frame horizontal strip (one cell per frame, tight to the ink).

The animation is the helix FLOWING up the beam: one period of the helix (measured by autocorrelation) is tiled
down the interior (inside the 3 px sheath, between the two caps), offset by one eighth of a period per frame. The
sheath, the caps and the alpha are never touched, so the silhouette is identical on all eight frames (0906s:
an animation must not move the silhouette) and the loop is seamless because it scrolls by exactly one period.
Never reads its own output.
"""
import os
import numpy as np
from PIL import Image
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = os.path.join(ROOT, '_BUILD_SOURCE/fusion_beam_spritecook_1002.png')
OUT = os.path.join(ROOT, 'assets/game/shared/player_weapons/fusion_1002/beam.png')
N = 8


def main():
    im = np.array(Image.open(SRC).convert('RGBA'))
    a = im[..., 3]; ys, xs = np.where(a > 20)
    im = im[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; a = im[..., 3]
    h, w = a.shape
    full = [y for y in range(h) if (a[y] > 20).sum() >= w - 1]
    top, bot = full[0] + 2, full[-1] - 2                        # the body, inside both caps
    x0, x1 = 3, w - 3                                          # inside the sheath
    lum = im[top:bot, x0:x1, :3].astype(float).mean(axis=(1, 2))
    lum -= lum.mean()
    lags = range(10, min(70, (bot - top) // 2))
    corr = [float((lum[:-L] * lum[L:]).mean()) for L in lags]
    P = list(lags)[int(np.argmax(corr))]
    body = bot - top
    print('cell %dx%d body rows %d..%d (%d) helix period %d px' % (w, h, top, bot, body, P))
    sheet = np.zeros((h, w * N, 4), np.uint8)
    for k in range(N):
        f = im.copy()
        shift = int(round(k * P / N))
        seg = im[top:bot, x0:x1].copy()
        # tile ONE measured helix period down the body, offset by `shift`: every frame is the same continuous
        # helix (a roll inside a non-multiple span left a hard cut that showed on half the frames)
        block = seg[(body - P) // 2:(body - P) // 2 + P]
        moved = np.stack([block[(y + shift) % P] for y in range(body)])
        keep = a[top:bot, x0:x1] > 0
        f[top:bot, x0:x1][keep] = moved[keep]
        f[..., 3] = a                                          # the silhouette is the source's, always
        sheet[:, k * w:(k + 1) * w] = f
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    Image.fromarray(sheet).save(OUT)
    print('wrote', OUT, sheet.shape[1], 'x', sheet.shape[0], 'frames', N, 'cell', w, 'x', h)


if __name__ == '__main__':
    main()
