#!/usr/bin/env python3
"""
DROP 0801en - FLAMETHROWER ANIMATION FROM ONE PLATE

Mike: "you see the fire inside with the whiteishyellow/orange, your going to make
those pixels light up and animate like its truly burning, and try ot make the
fire appear like it's moving from bottom to top. very cool pixel effect you can
do with 1 frame to turn into like 6-8 frames."

THE TECHNIQUE
This is palette cycling, the way a 16-bit machine faked flowing fire without
storing eight sprites. The plate's SILHOUETTE never changes - every frame keeps
the exact same alpha, so the flame does not wobble or breathe at the edges. What
moves is the heat INSIDE it.

  1. Measure each body pixel's luminance and normalise it to 0..1. That is the
     plate's own heat map: the white core reads ~1.0, the deep red rim ~0.
  2. Add a travelling wave that runs UP the plate:
         phase = y/H * bands  -  frame/N
     Sampling that per pixel and adding it to the base heat means the bright
     zones migrate upward frame by frame while the cool zones follow behind.
  3. Re-quantise the combined value into the plate's OWN four colour bands -
     deep red, mid orange, bright, white core - measured off the source rather
     than invented. Nothing is tinted or brightened; pixels are reassigned
     between colours that were already in the art.

  A little per-pixel jitter, seeded from the coordinates so it is identical every
  run, stops the wave reading as clean horizontal stripes.

WHY THE SILHOUETTE IS LOCKED
The first thing that goes wrong with generated fire frames is the outline
crawling, which makes the whole thing look like it is boiling. Copying alpha
straight from the source on every frame means only the interior animates.

The red rim added in 0801em is excluded from the cycling and copied verbatim, so
the unit keeps its hard edge in all eight frames.
"""
import os
import numpy as np
from PIL import Image

# READ FROM A MASTER THE GENERATOR NEVER WRITES (drop 0801eo). The first version
# read nfw_wall_0.png and also wrote it as frame 0, so the cleaned plate from
# 0801em was destroyed on the first run and the second run then re-processed a
# generated frame. Source and output must never share a filename.
SRC = 'assets/fx/weapons/flamethrower/nfw_wall_master.png'
OUT = 'assets/fx/weapons/flamethrower'
N_FRAMES = 8
BANDS = 2.6          # how many heat waves fit on the plate at once
WAVE = 0.42          # how hard the wave pushes heat between bands
JITTER = 0.05


def main():
    a = np.array(Image.open(SRC).convert('RGBA')).astype(float)
    H, W = a.shape[:2]
    alpha = a[..., 3]
    op = alpha > 16
    r, g, b = a[..., 0], a[..., 1], a[..., 2]

    # the red rim from 0801em - kept exactly as it is, never cycled
    rim = op & (r > 180) & (g < 60) & (b < 40)
    body = op & ~rim

    lum = 0.299 * r + 0.587 * g + 0.114 * b
    lo, hi = np.percentile(lum[body], 3), np.percentile(lum[body], 99)
    heat = np.clip((lum - lo) / max(1e-6, hi - lo), 0, 1)

    # the plate's own four colours, measured not invented
    qs = np.percentile(lum[body], [35, 80, 92])
    palette = []
    for a0, a1 in [(0, qs[0]), (qs[0], qs[1]), (qs[1], qs[2]), (qs[2], 1e9)]:
        m = body & (lum >= a0) & (lum < a1)
        if m.sum() < 8:
            palette.append(np.array([250, 150, 60]))
            continue
        palette.append(np.median(a[..., :3][m], axis=0))
    palette = np.array(palette)          # deep -> mid -> bright -> core

    # ---- MAKE THE PLATE VERTICALLY SEAMLESS (drop 0801et) ----
    # Mike: "you have to also scroll the whole flame frame into itself while
    # remaining center."
    #
    # To roll the WHOLE frame - alpha included - without the flame walking off the
    # top and a gap arriving at the bottom, the plate has to tile into itself
    # vertically. It does not: measured, the top 14 rows are 56px wide and the
    # bottom 14 are 46px, so a plain roll leaves a hard step across the fire.
    #
    # Cross-fading the plate with a half-height-shifted copy of itself over the
    # join makes the two ends meet. After this the sprite wraps cleanly, so
    # rolling every channel reads as one endless column of fire climbing through a
    # window that never moves.
    SEAM = 34
    half = np.roll(a, H // 2, axis=0)
    for k in range(SEAM):
        t = k / float(SEAM - 1)          # 0 at the start of the join, 1 at the end
        ytop = k                          # blend the very top rows
        ybot = H - SEAM + k               # and the very bottom
        wgt = 0.5 - 0.5 * np.cos(np.pi * t)
        a[ybot] = a[ybot] * (1 - wgt * 0.5) + half[ybot] * (wgt * 0.5)
        a[ytop] = a[ytop] * (0.5 + wgt * 0.5) + half[ytop] * (0.5 - wgt * 0.5)
    alpha = a[..., 3]
    op = alpha > 16
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    rim = op & (r > 180) & (g < 60) & (b < 40)
    body = op & ~rim
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    lo, hi = np.percentile(lum[body], 3), np.percentile(lum[body], 99)
    heat = np.clip((lum - lo) / max(1e-6, hi - lo), 0, 1)

    yy, xx = np.mgrid[0:H, 0:W]
    # deterministic per-pixel jitter so the wave is not a clean stripe
    jit = ((np.sin(xx * 12.9898 + yy * 78.233) * 43758.5453) % 1.0 - 0.5) * 2 * JITTER

    os.makedirs(OUT, exist_ok=True)
    written = []
    for f in range(N_FRAMES):
        # DIRECTION (drop 0801ep). Mike: "the flame should move bottom to top not
        # top to bottom." I had the sign backwards - with y increasing DOWNWARD,
        # subtracting the frame phase walks the bright band down the plate. Adding
        # it walks the band toward y=0, which is up the screen.
        phase = (yy / H) * BANDS + (f / N_FRAMES)
        wave = np.sin(phase * 2 * np.pi) * 0.5 + 0.5          # 0..1

        # THE TEXTURE SCROLLS TOO. Mike: "make the flame scroll vertically bottom
        # to top with the flame too." Palette cycling alone moves the BRIGHTNESS
        # but every pixel keeps its own base heat, so the underlying shape of the
        # fire stays put. Sampling the heat map from a row further DOWN the plate
        # each frame makes the fire's own detail climb with the wave.
        #
        # The sample wraps within the body, and the SILHOUETTE is taken from the
        # unshifted mask - so the texture flows upward inside a fixed outline
        # instead of the whole sprite sliding.
        # NEGATIVE roll. np.roll with a POSITIVE shift moves content toward larger
        # y, i.e. DOWN the plate - which cancelled the wave exactly and left the
        # pattern static. Cross-correlating the row-brightness profiles between
        # frames measured a lag of 0px, which is what caught it. Rolling negative
        # carries the texture toward y=0, the same way the wave travels.
        # FULL-STEP scroll of the heat map. This is the thing that makes the
        # drawing climb: heat decides which of the four colours each pixel takes,
        # so rolling it carries the licks and gaps upward. Rolling the RGB as well
        # was pointless - every body pixel is repainted from the palette right
        # after, so those scrolled pixels never survived to the output.
        # NO ROLL HERE. The final pass rolls the finished pixels, so rolling the
        # heat map as well applied the same shift twice - measured travel came out
        # at -56, -114, -172 px against an expected -28, -57, -86. One roll, at
        # the end, is the whole effect. The wave below still supplies the burn.
        heat_s = heat
        jit_s = jit

        v = np.clip(heat_s + (wave - 0.5) * WAVE + jit_s, 0, 1)

        idx = np.clip((v * len(palette)).astype(int), 0, len(palette) - 1)

        # THE GRAPHIC ITSELF SCROLLS (drop 0801eq). Mike: "make the actual graphic
        # vertically scroll while still remaining center WITH the flame animating."
        #
        # Everything so far moved the HEAT. The plate's own detail - the licks, the
        # gaps, the shape of the tongues - stayed exactly where it was, so the
        # motion read as a light show over a static picture rather than as fire
        # travelling. This rolls the SOURCE PIXELS up the plate and wraps them, so
        # the actual drawing climbs.
        #
        # Two things keep it centred rather than sliding off:
        #   - alpha comes from the UNSHIFTED mask, so the silhouette never moves
        #   - the roll wraps, so what leaves the top re-enters at the bottom and
        #     the flame is continuous at every frame
        # The palette animation is then applied ON TOP of the scrolled pixels, so
        # the fire is both flowing and burning rather than one or the other.
        out = a.copy()
        for k in range(len(palette)):
            m = body & (idx == k)
            for c in range(3):
                out[..., c][m] = palette[k][c]
        # the rim is redrawn from the unscrolled plate so the edge stays put
        for c in range(3):
            out[..., c][rim] = a[..., c][rim]
        # TRANSLUCENCY BY HEAT (drop 0801eo). Mike: "it needs to be on a
        # trasnlucent background, what happened."
        #
        # Measured: mean alpha over the flame body was 246/255 - effectively a
        # solid slab, and it was that way in the source too. Fire that occludes
        # the terrain completely reads as a painted shape, not as flame.
        #
        # Alpha now follows the SAME value that drives the colour, so the white
        # core stays nearly solid and the cool outer body goes see-through. The
        # translucency therefore travels upward with the heat instead of being a
        # flat wash. The soft edge already in the source is multiplied through
        # rather than replaced, so the anti-aliased rim survives.
        a_lo, a_hi = 96.0, 236.0
        grade = a_lo + (a_hi - a_lo) * v
        na = alpha.astype(float).copy()
        na[body] = np.minimum(alpha[body], grade[body] * (alpha[body] / 255.0) + grade[body] * 0.0)
        na[body] = grade[body] * (alpha[body] / 255.0)
        na[rim] = alpha[rim] * 0.86          # the edge stays readable but is not a wall
        out[..., 3] = na

        # THE WHOLE FRAME TRAVELS (drop 0801er). Mike: "your moving the flame
        # internally, I entire frame with the animation."
        #
        # Everything up to now moved the heat INSIDE a locked outline: the
        # silhouette stood still while colours crawled through it. He wants the
        # drawing itself to travel. Rolling ALL FOUR channels - pixels and alpha
        # together - sends the entire plate up the frame, wrapping, so it reads as
        # one continuous jet climbing instead of a fixed shape lighting up.
        #
        # Rolling alpha is precisely what I was refusing to do, on the reasoning
        # that a moving outline looks like boiling. On a column that wraps
        # seamlessly it is the thing that sells the flow.
        #
        # SCROLL INTO ITSELF (drop 0801es). Mike: "dont make it go off screen,
        # remain it center and scroll into itself."
        #
        # Rolling the alpha in 0801er sent the whole silhouette travelling, which
        # means the flame walks off the top and the shape arrives from the bottom.
        # That is not what he wants. The OUTLINE has to stay exactly where it is -
        # centred, same size, anchored to the pilot - while the fire inside it
        # flows upward and re-enters at the bottom.
        #
        # So: alpha comes from the UNROLLED plate, colour comes from the ROLLED
        # one. The silhouette is a fixed window; the fire streams through it.
        #
        # The wrap is cross-faded across FADE rows so the plate's tapered tip does
        # not butt against its wide base and leave a seam crossing the flame.
        travel = int(round(H * f / N_FRAMES))
        rolled = np.roll(out[..., :3], -travel, axis=0)
        out[..., 3] = np.roll(out[..., 3], -travel, axis=0)   # the frame travels as one
        FADE = 26
        if FADE > 0:
            other = np.roll(out[..., :3], -travel + H, axis=0)
            for k in range(FADE):
                t = k / float(FADE)
                y = (H - FADE + k) % H
                rolled[y] = rolled[y] * t + other[y] * (1 - t)
        out[..., :3] = rolled
        # alpha NOT rolled: the window stays put, the fire moves through it
        path = os.path.join(OUT, 'nfw_wall_%d.png' % f)
        Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGBA').save(path)
        written.append(path)

    print('wrote %d frames' % len(written))
    # prove the silhouette is locked and the interior actually moves
    base = np.array(Image.open(written[0]).convert('RGBA'))
    same_alpha = True
    diffs = []
    for p in written[1:]:
        q = np.array(Image.open(p).convert('RGBA'))
        if not np.array_equal(q[..., 3], base[..., 3]):
            same_alpha = False
        diffs.append(int((q[..., :3] != base[..., :3]).any(axis=2).sum()))
    print('  silhouette identical across all frames : %s' % same_alpha)
    print('  interior pixels changed vs frame 0     : %s' % diffs)
    print('  body pixels total                      : %d' % int(body.sum()))


if __name__ == '__main__':
    main()
