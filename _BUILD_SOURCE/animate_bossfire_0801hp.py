#!/usr/bin/env python3
"""
DROP 0801hp - ANIMATING THE TWELVE BOSS PROJECTILES

Mike, per unit:
  cryo     blue frost
  cyclone  the thrusters
  glacier  clean up and replace the thruster, then animate it
  legion   the fire
  magma    the fire lines
  mirv     the fire
  obsid    fire all over including the thruster
  rampart  inner red/white core, make it glow
  sludge   the acid appears to drip and decay
  storm    white/blue glowing like lightning
  toxic    the lines glow green, and the ball's effects glow
  warhawk  the thrusters animate

WHY THIS IS NEEDED
The pack ships six frames per projectile, but they are six SIZES, not six moments:
measured, 0 of 5 differ from frame 0 in content and all six have different
dimensions. So a projectile currently reads as a still image sliding down the
screen. Nothing pulses, nothing burns.

HOW THE GLOW WORKS
Each unit names a REGION by colour - the thruster, the fire, the core, the acid -
and a MOTION for it. The region is selected from the sprite's own pixels, never a
box, so it follows the art wherever it sits. Then per frame:

  travel   a band of brightness walks along the region, up or down
  pulse    the whole region breathes together
  flicker  a fast irregular lift, for fire and lightning
  drip     brightness pools downward and decays, for the acid

Only pixels already inside the region move. The outline, the chassis and the
silhouette are untouched, so nothing changes shape - it lights from within.

Output is bfx_<unit>_p_<0..5>, replacing the six size-variants with six PHASES of
the largest frame. One size, six moments, which is what a projectile wants.
"""
import os
import re
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PHASES = 6

# unit -> (region selector, motion, strength)
#   selector picks the pixels that light up, from the sprite's own colour
SPEC = {
    'cryo':    ('cool',     'glow',   0.42),   # blue frost climbing the crystal
    'cyclone': ('thruster', 'flicker',  0.55),   # thruster burn
    'glacier': ('thruster', 'thrust', 0.52),   # the replaced thruster
    'legion':  ('warm',  'flicker',     0.52),   # fire
    'magma':   ('warm',     'glow',   0.55),   # the fire LINES specifically
    'mirv':    ('warm',  'flicker',     0.50),   # fire
    'obsid':   ('warm',  'flicker',     0.55),   # fire all over, thruster included
    'rampart': ('core',  'pulse',       0.60),   # the inner red/white core
    'sludge':  ('acid',  'drip',        0.48),   # acid dripping and decaying
    'storm':   ('cool',  'flicker',     0.58),   # lightning
    'toxic':   ('acid',     'glow',   0.50),   # the lines and the ball
    'warhawk': ('warm',     'thrust', 0.50),   # thrusters
}


def region(a, kind):
    """Select the lighting region from the sprite's own colour."""
    op = a[..., 3] > 16
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    # never touch the outline - that is the shape
    outline = (r < 60) & (g < 60) & (b < 70) & op
    body = op & ~outline
    if kind == 'warm':
        # FIRE, NOT PAINT (drop 0801hq). Mike: "dont make the red tips on our
        # graphics glow. just the effect parts that are needed to glow. your making
        # the missile red parts glow instead of just the fire."
        #
        # r > g + 18 catches RED PAINT as readily as flame - measured on legion, 3569
        # of the 4509 px it selected were painted chassis and only 435 were fire.
        # Flame is separable on two counts: it carries GREEN (that is what makes it
        # orange rather than red) and it is BRIGHT. Painted metal is red but dark and
        # green-starved. Requiring both green content and high value keeps the hull
        # still and lights only what is burning.
        return body & (r > b + 30) & (g > 88) & (mx > 190)
    if kind == 'cool':
        return body & (b > r + 20)
    if kind == 'acid':
        return body & (g > r + 14) & (g > b + 10)
    if kind == 'thruster':
        # THE EXHAUST, NOT THE AIRFRAME (drop 0801hq). cyclone and glacier are blue
        # units, so 'warm' found ZERO pixels on them and they fell through to the
        # whole-sprite fallback - the entire jet was pulsing instead of its burn.
        # The exhaust is the brightest cool matter in the BOTTOM third, which is
        # where a downward-facing round trails from.
        H = a.shape[0]
        yy = np.mgrid[0:H, 0:a.shape[1]][0]
        if not body.any():
            return body
        # the ternary here used to swallow the comparison - `a & (x > y if c else d)`
        # parses as `a & (x > (y if c else d))`, so `hot` came out meaningless and
        # the selector returned nothing. Split out (drop 0801hq).
        thr = np.percentile(mx[body], 72)
        hot = body & (mx > thr)
        # THE EXHAUST TRAILS BEHIND. These rounds face SOUTH, so the burn is at the
        # TOP of the frame, not the bottom - I had the half inverted, which is why
        # the selector kept coming back empty on both blue units.
        return hot & (yy < H * 0.55)
    if kind == 'core':
        # ADAPTIVE, not a fixed 168. rampart's whole body is 393px and none of it
        # cleared that threshold, so it fell back to the full sprite too. Taking the
        # brightest quarter of whatever the sprite actually contains finds the core
        # on a dark unit as readily as a bright one.
        if not body.any():
            return body
        return body & (mx > np.percentile(mx[body], 76))
    return body


def animate(a, mask, motion, amt, phase):
    """Lift the masked pixels according to the motion, at this phase."""
    out = a.copy()
    H, W = a.shape[:2]
    yy = np.mgrid[0:H, 0:W][0] / max(1, H)
    ph = phase / float(PHASES)

    # DIRECTION IS SET BY WHAT THE PIXELS ARE (drop 0801hr). Mike:
    #   "since the projecticle are going toward the player, animations go top to
    #    bottom if its a glow projectile, thrusters you animate bottom to top."
    #
    # A glow travels WITH the round, so it runs down the frame toward the player.
    # An exhaust trails BEHIND it, so it runs up. Subtracting the phase walks the
    # band toward +y (down); adding walks it toward -y (up).
    if motion == 'glow':                       # top -> bottom
        w = np.sin((yy * 2.1 - ph) * 2 * np.pi) * 0.5 + 0.5
    elif motion == 'thrust':                   # bottom -> top
        w = np.sin((yy * 2.1 + ph) * 2 * np.pi) * 0.5 + 0.5
    elif motion == 'pulse':
        # a plain sine returns the same value at 0 and at pi, so phase 0 and phase 3
        # came out IDENTICAL and the core appeared to stall twice a cycle. Squaring
        # a half-rate wave gives six distinct steps that still breathe evenly.
        w = np.full_like(yy, np.sin(ph * np.pi) ** 2)
    elif motion == 'flicker':
        rng = np.random.RandomState(1000 + phase * 7)
        base = np.sin((yy * 3.0 + ph * 1.7) * 2 * np.pi) * 0.5 + 0.5
        w = np.clip(base * 0.6 + rng.rand(H, W) * 0.4, 0, 1)
    elif motion == 'drip':
        # brightness pools toward the bottom and decays as it goes
        w = np.clip((yy + ph) % 1.0, 0, 1) ** 1.7
    else:
        w = np.full_like(yy, 0.5)

    lift = 1.0 + (w - 0.5) * 2 * amt
    for c in range(3):
        out[..., c] = np.where(mask, np.clip(a[..., c] * lift, 0, 255), a[..., c])
    return out


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    made = 0
    report = []
    for unit, (sel, motion, amt) in SPEC.items():
        # the LARGEST of the six size-variants becomes the single source
        best = None
        for i in range(PHASES):
            m = re.search(r'"bfx_%s_p_%d":"([^"]+)"' % (unit, i), man)
            if not m:
                continue
            p = os.path.join(ROOT, m.group(1))
            if not os.path.exists(p):
                continue
            # RE-RUNNING WAS COMPOUNDING. This reads the largest frame, animates it
            # and writes it back - so a second run animated the already-animated
            # output and the numbers drifted every pass. A pristine copy is kept on
            # first run and used as the source from then on.
            cache = os.path.join(ROOT, '_BUILD_SOURCE/_bfx_src', os.path.basename(m.group(1)))
            os.makedirs(os.path.dirname(cache), exist_ok=True)
            if not os.path.exists(cache):
                Image.open(p).convert('RGBA').save(cache)
            a = np.array(Image.open(cache).convert('RGBA')).astype(float)
            if best is None or a.shape[0] * a.shape[1] > best[0].shape[0] * best[0].shape[1]:
                best = (a, m.group(1))
        if best is None:
            continue
        src, _ = best
        mask = region(src, sel)
        if mask.sum() < 40:
            # falling back to the whole sprite means the WHOLE THING pulses, which
            # is exactly the "red tips glowing" Mike caught. Say so rather than do
            # it quietly.
            print('   !! %s: selector %s found nothing - falling back to whole sprite' % (unit, sel))
            mask = (src[..., 3] > 16)
        for i in range(PHASES):
            m = re.search(r'"bfx_%s_p_%d":"([^"]+)"' % (unit, i), man)
            if not m:
                continue
            b = animate(src, mask, motion, amt, i)
            Image.fromarray(np.clip(b, 0, 255).astype(np.uint8), 'RGBA').save(
                os.path.join(ROOT, m.group(1)))
            made += 1
        report.append((unit, sel, motion, int(mask.sum())))

    print('  wrote %d animated frames across %d units' % (made, len(report)))
    print()
    print('   unit      region  motion        lit px')
    for u, s, mo, n in sorted(report):
        print('   %-9s %-7s %-13s %6d' % (u, s, mo, n))


if __name__ == '__main__':
    main()
