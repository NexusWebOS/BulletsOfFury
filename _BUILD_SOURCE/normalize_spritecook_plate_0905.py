#!/usr/bin/env python3
"""normalize_spritecook_plate_0905.py - make a SpriteCook plate shippable next to authored BOF art.

    python _BUILD_SOURCE/normalize_spritecook_plate_0905.py <reference.png> <generated.png> <out.png>

Mike, 0905, approving the first Cryo Spear damage plate: "looks great to me". The DAMAGE is his
call and is left exactly as generated. What this fixes is the two things that are not design:

1. PALETTE. Measured on OPAQUE PIXELS ONLY (counting RGB under transparent pixels inflates the
   number by ~16k and is how this gets waved through): the authored intact plate is **61 colours**,
   the generated one **19,063**. It is a continuous-tone render wearing pixel-art clothes. Dropped
   in as-is the boss changes ART STYLE at 62% HP. Every opaque pixel is snapped to its nearest
   neighbour in the reference's own palette, DITHER OFF - dithering a 61-colour target sprays
   checkerboard noise through flat armour and reads as JPEG rot at 2x.

2. PIVOT. SpriteCook returned 257x274 for a requested 256x256, with `smart_crop=false` set. That is
   not a bug: `resolved_parameters.size_behavior` is **"hint"**, so width/height are suggestions.
   The plates are swapped IN PLACE at one draw size, so a plate whose ink sits differently reads as
   the boss growing or shrinking the instant it takes a hit.

   ⚠ THE SHIP IS NOT RESCALED. Ink measures 212 wide against the reference's 211 - a 0.5%
   difference, i.e. the same scale with a longer tail. Scaling to force the HEIGHT to match would
   squeeze the width to 198 and make the boss visibly narrower at 62% HP: a real defect introduced
   to fix a cosmetic one. Offset only.

   The offset is SOLVED, not guessed: the alpha masks are cross-correlated and the (dx,dy) with the
   highest intersection-over-union wins. Aligning by bbox edges would hang the whole ship off
   whichever edge happens to have grown; aligning by centroid is pulled by the same new mass. IoU
   asks the only question that matters - where does this ship most sit on top of the old one.
"""
import sys, os, collections
from PIL import Image


def opaque_stats(im):
    px = im.load(); w, h = im.size
    cols = collections.Counter(); op = 0; semi = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0: continue
            op += 1
            if a < 250: semi += 1
            cols[(r, g, b)] += 1
    return op, len(cols), semi, cols


def mask_of(im):
    """set of opaque (x,y)"""
    px = im.load(); w, h = im.size
    return {(x, y) for y in range(h) for x in range(w) if px[x, y][3] > 0}


def best_offset(ref, gen, search=28):
    """the (dx,dy) placing gen's ink most on top of ref's ink, by IoU. Seeded from bbox centres
    so the search window is small and centred on the plausible answer."""
    rb, gb = ref.getbbox(), gen.getbbox()
    seed_x = ((rb[0] + rb[2]) - (gb[0] + gb[2])) // 2
    seed_y = ((rb[1] + rb[3]) - (gb[1] + gb[3])) // 2
    R = mask_of(ref); G = mask_of(gen)
    best = None
    for dy in range(seed_y - search, seed_y + search + 1):
        for dx in range(seed_x - search, seed_x + search + 1):
            shifted = {(x + dx, y + dy) for (x, y) in G}
            inter = len(R & shifted)
            union = len(R) + len(G) - inter
            iou = inter / union if union else 0.0
            if best is None or iou > best[0]:
                best = (iou, dx, dy)
    return best


def main():
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    ref_p, gen_p, out_p = sys.argv[1], sys.argv[2], sys.argv[3]
    ref = Image.open(ref_p).convert('RGBA')
    gen = Image.open(gen_p).convert('RGBA')
    W, H = ref.size

    r_op, r_cols, r_semi, ref_cols = opaque_stats(ref)
    g_op, g_cols, g_semi, _ = opaque_stats(gen)
    print('reference %s  opaque %d  colours %d' % (ref.size, r_op, r_cols))
    print('generated %s  opaque %d  colours %d' % (gen.size, g_op, g_cols))

    # ---- 1. solve the offset on the RAW masks, before any palette work -----------------------
    iou, dx, dy = best_offset(ref, gen)
    print('best alignment: dx=%d dy=%d  silhouette IoU %.4f' % (dx, dy, iou))

    # ---- 2. place on the reference's canvas, no rescale ---------------------------------------
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    canvas.paste(gen, (dx, dy), gen)

    # how much ink did the canvas edge cut off?
    placed = len({(x + dx, y + dy) for (x, y) in mask_of(gen)
                  if 0 <= x + dx < W and 0 <= y + dy < H})
    lost = g_op - placed
    print('ink kept %d / %d   CLIPPED BY CANVAS: %d px (%.2f%%)' % (placed, g_op, lost, 100.0 * lost / g_op))

    # ---- 3. snap every opaque pixel to the reference palette, dither OFF -----------------------
    pal = sorted(ref_cols.keys())
    flat = []
    for c in pal: flat.extend(c)
    flat.extend([0, 0, 0] * (256 - len(pal)))
    pimg = Image.new('P', (1, 1)); pimg.putpalette(flat)

    alpha = canvas.split()[3]
    quant = canvas.convert('RGB').quantize(palette=pimg, dither=Image.Dither.NONE).convert('RGB')
    out = quant.convert('RGBA')
    out.putalpha(alpha)

    # zero the RGB under fully transparent pixels so the file cannot carry ghost colour
    px = out.load()
    for y in range(H):
        for x in range(W):
            if px[x, y][3] == 0: px[x, y] = (0, 0, 0, 0)

    o_op, o_cols, o_semi, _ = opaque_stats(out)
    print('OUT       %s  opaque %d  colours %d  semi-alpha %d  bbox %s'
          % (out.size, o_op, o_cols, o_semi, out.getbbox()))
    print('reference bbox %s' % (ref.getbbox(),))
    if o_cols > r_cols:
        print('  !! palette lock FAILED - output carries more colours than the reference')
    out.save(out_p, optimize=True)
    print('wrote %s' % out_p)


if __name__ == '__main__':
    main()
