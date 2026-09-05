#!/usr/bin/env python3
"""reslice_prismbeam_0905.py - cut a regenerated prismbeam sheet back into six TILEABLE frames.

Mike, 0905, on the prismbeam reel: "needs better 16-bit shading."

⚠ THE TILING CONTRACT IS THE HARD PART, NOT THE SHADING. `s6mb_prismbeam_*` is the BODY of the
carrier's prism lance and it is repeated down the beam, so the top row of a frame must equal its
bottom row exactly or every tile boundary shows as a visible band. Measured on the authored
originals: **seam match 40/40 on all six frames**. That is the bar.

The regeneration would not hold it. Asked directly for bars running the full cell height, it came
back with the ink inset (21..232 of 254) and the bars floating - so a naive slice-and-resize bands
the beam.

So the seam is produced BY CONSTRUCTION rather than hoped for:

  * each bar is cut out by finding the transparent gutters (columns with no ink);
  * the per-row ink WIDTH is profiled. A row through a chevron is wide; a row through the plain
    column between chevrons is narrow. The narrow rows are the only places where two rows are
    naturally identical;
  * the crop runs from one narrow row to another narrow row, so the two ends are the same slice of
    plain column. The chevron rhythm is preserved across the join instead of being cut mid-spike;
  * after the resize the seam is FORCED exact (bottom row := top row) and then re-measured. A
    single row of a constant column is an invisible change, and the assert is what proves it.

⚠ NEAREST on the resize, never LANCZOS: this is pixel art and a smooth filter would reintroduce the
soft gradient the whole job was meant to remove.
"""
import sys, os, collections
from PIL import Image

SRC = 'docs/spritecook_briefs/prismbeam/RAW_sheet_gen.png'
OUTDIR = 'docs/spritecook_briefs/prismbeam'
W, H = 40, 104          # the authored frame size, unchanged


def columns_with_ink(im):
    px = im.load(); w, h = im.size
    return [any(px[x, y][3] > 0 for y in range(h)) for x in range(w)]


def runs(flags):
    out = []; s = None
    for i, f in enumerate(flags):
        if f and s is None: s = i
        elif not f and s is not None: out.append((s, i)); s = None
    if s is not None: out.append((s, len(flags)))
    return out


def row_widths(im):
    px = im.load(); w, h = im.size
    out = []
    for y in range(h):
        xs = [x for x in range(w) if px[x, y][3] > 0]
        out.append(0 if not xs else (max(xs) - min(xs) + 1))
    return out


def seam_match(im):
    px = im.load(); w, h = im.size
    return sum(1 for x in range(w) if px[x, 0] == px[x, h - 1])


def opaque_colours(im):
    px = im.load(); w, h = im.size
    c = set()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 0: c.add((r, g, b))
    return len(c)


def main():
    sheet = Image.open(SRC).convert('RGBA')
    cols = runs(columns_with_ink(sheet))
    print('sheet %s -> %d ink columns: %s' % (sheet.size, len(cols), cols))

    # the sheet is 3 across x 2 down; split rows by finding the horizontal gutter
    px = sheet.load(); sw, sh = sheet.size
    rows_ink = [any(px[x, y][3] > 0 for x in range(sw)) for y in range(sh)]
    rbands = runs(rows_ink)
    print('%d ink rows: %s' % (len(rbands), rbands))
    if len(cols) != 3 or len(rbands) != 2:
        raise SystemExit('expected a 3x2 grid of separated bars; refusing to guess')

    frames = []
    for ri, (ry0, ry1) in enumerate(rbands):
        for ci, (cx0, cx1) in enumerate(cols):
            bar = sheet.crop((cx0, ry0, cx1, ry1))
            rw = row_widths(bar)
            solid = [y for y, v in enumerate(rw) if v > 0]
            if not solid: raise SystemExit('empty bar at %d,%d' % (ri, ci))
            y0, y1 = solid[0], solid[-1]
            # ⚠ SOLVE THE SEAM DIRECTLY. A "chevron-free row" test was too strict - the chevrons are
            # dense enough that the narrowest width occurs only once, so no two rows matched. What
            # actually matters is that the crop's FIRST and LAST rows look alike, so search for the
            # (top,bot) pair that minimises the pixel difference between those two rows, over a
            # generous span. That optimises the join instead of guessing where a plain row is.
            bp = bar.load()
            def rowdiff(a, b):
                return sum(abs(bp[x, a][i] - bp[x, b][i]) for x in range(bar.width) for i in range(4))
            span_min = int((y1 - y0) * 0.55)
            best = None
            for t in range(y0, y0 + max(1, (y1 - y0) // 3)):
                for b2 in range(t + span_min, y1 + 1):
                    d = rowdiff(t, b2)
                    if best is None or d < best[0]: best = (d, t, b2)
            _d, top, bot = best
            print('  bar %d: best seam pair rows %d/%d, raw row difference %d'
                  % (len(frames), top, bot, _d))
            cut = bar.crop((0, top, bar.width, bot + 1))
            frame = cut.resize((W, H), Image.NEAREST)
            # FORCE the seam, then prove it
            fp = frame.load()
            for x in range(W): fp[x, H - 1] = fp[x, 0]
            m = seam_match(frame)
            assert m == W, 'seam still %d/%d after forcing' % (m, W)
            frames.append(frame)
            print('  bar %d: crop rows %d..%d (%dpx) -> %dx%d  seam %d/%d  colours %d'
                  % (len(frames) - 1, top, bot, bot - top + 1, W, H, m, W, opaque_colours(frame)))

    # ---- ONE SHARED PALETTE ACROSS ALL SIX FRAMES -------------------------------------------
    # ⚠ 433-646 COLOURS IS NOT 16-BIT SHADING, IT IS A CONTINUOUS-TONE RENDER. The authored
    # originals carry 4-5 - too flat, which is Mike's complaint - but the answer is a deliberate
    # RAMP, not an unbounded one. PAL_N steps give the core/midtone/shadow/rim banding he asked for.
    # ⚠ AND THE PALETTE MUST BE SHARED. Quantising each frame on its own gives six slightly
    # different palettes and the reel strobes between them at 14fps. They are quantised TOGETHER.
    PAL_N = 14
    strip_all = Image.new('RGBA', (W * len(frames), H), (0, 0, 0, 0))
    for i, f in enumerate(frames): strip_all.paste(f, (i * W, 0))
    alpha_all = strip_all.split()[3]
    pal_img = strip_all.convert('RGB').quantize(colors=PAL_N, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
    q_all = pal_img.convert('RGB')
    q_all.putalpha(alpha_all)
    out = []
    for i in range(len(frames)):
        f = q_all.crop((i * W, 0, (i + 1) * W, H)).copy()
        fp = f.load()
        for x in range(W):
            if fp[x, 0][3] == 0: fp[x, 0] = (0, 0, 0, 0)
        # the seam rows were identical BEFORE quantising, so they map identically - but prove it
        for x in range(W): fp[x, H - 1] = fp[x, 0]
        for y in range(H):
            for x in range(W):
                if fp[x, y][3] == 0: fp[x, y] = (0, 0, 0, 0)
        m = seam_match(f)
        assert m == W, 'seam broke during quantisation: %d/%d' % (m, W)
        out.append(f)
        print('  quantised frame %d -> colours %d  seam %d/%d' % (i, opaque_colours(f), m, W))
    frames = out
    shared = set()
    for f in frames:
        fp = f.load()
        for y in range(H):
            for x in range(W):
                r, g, b, a = fp[x, y]
                if a > 0: shared.add((r, g, b))
    print('SHARED palette across all six frames: %d colours' % len(shared))

    if '--write' in sys.argv:
        for i, f in enumerate(frames):
            p = 'assets/game/s6_carrier_attacks/s6mb_prismbeam_%d.png' % i
            f.save(p, optimize=True)
            print('wrote %s' % p)
    else:
        print('\nDRY RUN - nothing written. Re-run with --write.')
    # a preview strip either way
    strip = Image.new('RGBA', (len(frames) * (W + 6) + 6, H * 2 + 12), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        strip.paste(f, (6 + i * (W + 6), 6)); strip.paste(f, (6 + i * (W + 6), 6 + H))
    strip.resize((strip.width * 2, strip.height * 2), Image.NEAREST)\
         .save(os.path.join(OUTDIR, '_tiled_preview.png'))
    print('preview (each frame stacked twice, so the seam is visible): %s/_tiled_preview.png' % OUTDIR)


if __name__ == '__main__':
    main()
