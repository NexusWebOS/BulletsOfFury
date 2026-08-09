#!/usr/bin/env python3
"""
key_crates_0801km.py — turn the four magenta-backed crate sheets into game sprites

THE KEY IS NOT A FLAT COLOUR. Measured across the four sheets the background runs
(224,3,233) (225,3,233) (217,1,231) (205,2,224) ... — compressed and noisy, so an
exact-RGB match (which is what worked for the crackle bolts) drops most of it and
leaves a magenta rind.

Passover trap #5 is exactly this case: "Thresholds tuned to one sample generalise
badly. Magenta needed three attempts; the right invariant was the RATIO (green
collapses, red and blue stay high), not any absolute brightness."

So the test is ratio-based:
    green collapses:  G < 0.55 * min(R,B)
    both ends high:   R > 70 and B > 70
    and magenta, not red: |R-B| < 0.55 * max(R,B)
That last clause is what protects the art. These crates are full of RED — missile
stripes, the x35 body, the ELITE stamp. Red is high-R / low-G / LOW-B, so it fails
the "B > 70" and the |R-B| test. Magenta is high-R / low-G / HIGH-B.

BACKGROUND-CONNECTED ONLY. Even a good colour test can hit a magenta-ish pixel
inside the artwork. Only the region flood-connected to the border is removed, so
an interior pixel that happens to look magenta is kept.

DESPILL. Edge pixels blend crate into background, leaving a violet rim. Any
surviving pixel that still reads magenta-ward has its blue and red pulled toward
green in proportion to how magenta it is, which kills the rim without touching
saturated reds (they never read magenta in the first place).
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd

SRC = '/home/claude/work/newart'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets/pickups/crates')
CRATES = {'x20': 'nmc_20', 'x35': 'nmc_35', 'x50': 'nmc_50', 'x100': 'nmc_100'}
TARGET_H = 128        # stored height; drawn far smaller, this keeps it crisp


def magentaness(a):
    """0..1 how magenta a pixel reads. Ratio-based, never absolute brightness."""
    R = a[:, :, 0].astype(np.float32)
    G = a[:, :, 1].astype(np.float32)
    B = a[:, :, 2].astype(np.float32)
    lo = np.minimum(R, B)
    hi = np.maximum(R, B)
    green_gap = np.clip((lo - G) / np.maximum(lo, 1), 0, 1)      # how far green has collapsed
    balanced = 1 - np.clip(np.abs(R - B) / np.maximum(hi, 1), 0, 1)
    bright = np.clip(np.minimum(R, B) / 70.0, 0, 1)
    return green_gap * balanced * bright


def key(path):
    im = Image.open(path).convert('RGB')
    a = np.array(im)
    m = magentaness(a)
    bg = (m > 0.45)

    # keep only what touches the border — an interior magenta-ish pixel is ART
    lab, n = nd.label(bg)
    if n:
        border = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
        border.discard(0)
        keepbg = np.isin(lab, list(border)) if border else np.zeros_like(bg)
    else:
        keepbg = np.zeros_like(bg)

    out = np.dstack([a, np.where(keepbg, 0, 255).astype(np.uint8)])

    # despill the rim: only pixels that still read magenta-ward, scaled by how much
    solid = out[:, :, 3] > 0
    spill = (m > 0.18) & solid
    if spill.any():
        f = np.clip((m - 0.18) / 0.5, 0, 1)[spill][:, None]
        rgb = out[:, :, :3].astype(np.float32)
        G = rgb[:, :, 1:2]
        tgt = np.dstack([np.minimum(rgb[:, :, 0:1], G * 1.15),
                         rgb[:, :, 1:2],
                         np.minimum(rgb[:, :, 2:3], G * 1.15)])
        out[:, :, :3][spill] = (rgb[spill] * (1 - f) + tgt[spill] * f).astype(np.uint8)
        # a fully-magenta leftover is background the flood missed: drop it
        out[:, :, 3][(m > 0.72) & solid] = 0

    img = Image.fromarray(out)
    bb = img.getbbox()
    if bb:
        img = img.crop(bb)
    return img


def main(apply=False):
    os.makedirs(OUT, exist_ok=True)
    man_p = os.path.join(ROOT, 'assets/manifest.js')
    rows = []
    for stem, keyname in CRATES.items():
        img = key(os.path.join(SRC, stem + '.png'))
        w, h = img.size
        nw = max(1, int(round(w * TARGET_H / h)))
        small = img.resize((nw, TARGET_H), Image.LANCZOS)
        # LANCZOS can leave near-transparent halo; harden it
        al = np.array(small)[:, :, 3]
        arr = np.array(small)
        arr[:, :, 3] = np.where(al < 26, 0, al)
        small = Image.fromarray(arr)
        opaque = int((np.array(small)[:, :, 3] > 128).sum())
        rows.append((keyname, (w, h), small.size, opaque))
        if apply:
            small.save(os.path.join(OUT, keyname + '.png'))
    print(f"{'key':10s} {'keyed src':>14s} {'stored':>12s} {'opaque px':>10s}")
    for k, s, d, o in rows:
        print(f'{k:10s} {str(s):>14s} {str(d):>12s} {o:>10d}')
    print('APPLIED -> ' + OUT if apply else 'DRY RUN — pass --apply')


if __name__ == '__main__':
    main('--apply' in sys.argv)
