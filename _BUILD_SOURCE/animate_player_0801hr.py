#!/usr/bin/env python3
"""
DROP 0801hr - THE PLAYER'S PROJECTILES GET THE SAME TREATMENT

Mike: "now, similar treatment witih all other projectiles in the game including our
players laser beams. machine guns and spread do not get this treatment, but we do
black edge and make their sprites easier to see on screen."

DIRECTION, from the same message:
  "since the projecticle are going toward the player, animations go top to bottom
   if its a glow projectile, thrusters you animate bottom to top."

The player's shots travel the OTHER WAY - up the screen, away from the ship. So the
rule inverts for them: a glow on a player beam travels UP with the shot, and a
muzzle/exhaust effect trails DOWN behind it. The principle is the same one Mike
stated - the glow rides with the projectile, the exhaust trails behind it - only
the direction of travel differs.

WHAT GETS ANIMATED
  nlz_<lv>_b*    the beam tiers          glow, up
  nfb_orb*       the fire orb             glow, up
  nfb_fl*        the detached flames      flicker
  nts_orb*       thermoshock orb          glow, up
  nts_shard*     thermoshock shards       flicker
  aorb / alaser  Axel's orb and beam      glow, up
  nhxb_*         Maverick's helix ball    pulse

WHAT DOES NOT
  mfx_mg_*       machine gun
  mfx_spr_*      spread
Mike is explicit that these two are excluded. They get a black edge instead so they
read against terrain - which is the actual complaint, that they are hard to see.
"""
import os
import re
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CACHE = os.path.join(ROOT, '_BUILD_SOURCE/_pfx_src')
PHASES = 6

# family prefix -> (motion, strength). Player shots fly UP, so 'glow' rides up.
ANIMATE = [
    ('nlz_1_b',   'glow',    0.34), ('nlz_2_b', 'glow', 0.34), ('nlz_3_b', 'glow', 0.34),
    ('nlz_4_b',   'glow',    0.34), ('nlz_5_b', 'glow', 0.34),
    ('nfb_orb1_', 'glow',    0.40), ('nfb_orb2_', 'glow', 0.40), ('nfb_orb3_', 'glow', 0.40),
    ('nfb_orb4_', 'glow',    0.40), ('nfb_orb5_', 'glow', 0.40),
    ('nfb_fl1_',  'flicker', 0.46), ('nfb_fl2_', 'flicker', 0.46), ('nfb_fl3_', 'flicker', 0.46),
    ('nfb_fl4_',  'flicker', 0.46), ('nfb_fl5_', 'flicker', 0.46),
    ('nts_orb_',  'glow',    0.42), ('nts_shard_', 'flicker', 0.44),
    ('nhxb_g_',   'pulse',   0.40), ('nhxb_p_',   'pulse',   0.40),
]
EDGE_ONLY = ['mfx_mg_', 'mfx_spr_']


def lit_region(a):
    """The bright, saturated matter - the beam core and its glow, not the outline."""
    op = a[..., 3] > 16
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = np.maximum(np.maximum(r, g), b)
    outline = (r < 60) & (g < 60) & (b < 70) & op
    body = op & ~outline
    if not body.any():
        return body
    # A UNIFORM SPRITE DEFEATS A PERCENTILE. The beam plates are near-solid colour,
    # so percentile(mx, 46) equals almost every pixel's value and a strict `>`
    # selected NOTHING - 14 frames reported no lit region while carrying 12,491 lit
    # pixels each. Falling back to the whole body when the split finds too little
    # (drop 0801hr).
    sel = body & (mx > np.percentile(mx[body], 46))
    if sel.sum() < body.sum() * 0.12:
        sel = body
    return sel


def animate(a, mask, motion, amt, phase):
    out = a.copy()
    H, W = a.shape[:2]
    yy = np.mgrid[0:H, 0:W][0] / max(1, H)
    ph = phase / float(PHASES)
    if motion == 'glow':
        # the player's shots fly UP, so a glow that rides WITH the round runs up
        w = np.sin((yy * 2.0 + ph) * 2 * np.pi) * 0.5 + 0.5
    elif motion == 'trail':
        w = np.sin((yy * 2.0 - ph) * 2 * np.pi) * 0.5 + 0.5
    elif motion == 'pulse':
        w = np.full_like(yy, np.sin(ph * np.pi) ** 2)
    else:  # flicker
        rng = np.random.RandomState(500 + phase * 11)
        base = np.sin((yy * 3.0 + ph * 1.6) * 2 * np.pi) * 0.5 + 0.5
        w = np.clip(base * 0.62 + rng.rand(H, W) * 0.38, 0, 1)
    lift = 1.0 + (w - 0.5) * 2 * amt
    for c in range(3):
        out[..., c] = np.where(mask, np.clip(a[..., c] * lift, 0, 255), a[..., c])
    return out


def edge(a):
    """1px black rim so the sprite reads against terrain."""
    a = np.pad(a, ((1, 1), (1, 1), (0, 0)))
    al = a[..., 3] > 16
    e = ndimage.binary_dilation(al, iterations=1) & ~al
    a[..., 0][e] = 0
    a[..., 1][e] = 0
    a[..., 2][e] = 0
    a[..., 3][e] = 255
    return a, int(e.sum())


def main():
    man = open(os.path.join(ROOT, 'assets/manifest.js'), encoding='utf-8').read()
    os.makedirs(CACHE, exist_ok=True)
    keyed = dict(re.findall(r'"([a-zA-Z0-9_]+)":"(assets/[^"]+\.png)"', man))
    done = {}

    for pre, motion, amt in ANIMATE:
        keys = sorted(k for k in keyed if k.startswith(pre))
        if not keys:
            continue
        # a pristine copy so re-running cannot compound the lift
        srcs = []
        for k in keys:
            c = os.path.join(CACHE, k + '.png')
            if not os.path.exists(c):
                Image.open(os.path.join(ROOT, keyed[k])).convert('RGBA').save(c)
            srcs.append((k, np.array(Image.open(c).convert('RGBA')).astype(float)))
        n = 0
        for i, (k, a) in enumerate(srcs):
            m = lit_region(a)
            if m.sum() < 20:
                print('   !! %s: no lit region found, left alone' % k)
                continue
            b = animate(a, m, motion, amt, i % PHASES)
            Image.fromarray(np.clip(b, 0, 255).astype(np.uint8), 'RGBA').save(
                os.path.join(ROOT, keyed[k]))
            n += 1
        done[pre] = (motion, n)

    edged = 0
    for pre in EDGE_ONLY:
        for k in sorted(k for k in keyed if k.startswith(pre)):
            p = os.path.join(ROOT, keyed[k])
            c = os.path.join(CACHE, k + '.png')
            if not os.path.exists(c):
                Image.open(p).convert('RGBA').save(c)
            a = np.array(Image.open(c).convert('RGBA')).astype(float)
            a, n = edge(a)
            Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(p)
            edged += 1

    print('  animated:')
    for pre, (mo, n) in sorted(done.items()):
        print('   %-12s %-8s %d frames' % (pre, mo, n))
    print('  black-edged (no animation, per Mike): %d frames across %s'
          % (edged, ', '.join(EDGE_ONLY)))


if __name__ == '__main__':
    main()
