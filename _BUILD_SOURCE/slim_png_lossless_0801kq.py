#!/usr/bin/env python3
"""
slim_png_lossless_0801kq.py — PALETTISE ONLY WHERE IT IS PROVABLY LOSSLESS

The build is 419 MB of PNG. Most of it is pixel art stored as 32-bit RGBA while
using a few dozen colours: the boss breakup frames measured 31-47 unique colours
each and shrank 75% as PNG-8.

THE RULE: a file is converted ONLY if it has <= 256 unique RGBA values, which is
exactly the condition under which a 256-entry palette can hold every colour with
no substitution. Every converted file is then re-opened and compared pixel by
pixel against the original; if a single pixel differs, the original is kept. So
this cannot degrade art — it either proves identity or backs out.

WHAT IS DELIBERATELY LEFT ALONE:
  The big level masters. nst4_master_crash has 37,277 unique colours, mapJungle
  366,267, atlases/main.png 1,093,963. Quantising those to 256 would cut 46 MB
  down to 8 MB, but it is LOSSY on the backgrounds a player stares at for the
  whole level. That is Mike's call to make with his own eyes, not something to
  slip into a size-reduction pass.
"""
import io, os, shutil, sys
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP = os.path.join(ROOT, '_superseded', 'png_palette_0801kq')


def convert(p):
    """Return (newbytes, oldbytes) if a provably lossless smaller version exists."""
    old = os.path.getsize(p)
    im = Image.open(p)
    if im.mode not in ('RGBA', 'RGB', 'P', 'LA', 'L'):
        return None
    rgba = im.convert('RGBA')
    cols = rgba.getcolors(maxcolors=256)
    if cols is None:
        return None                      # more than 256 colours: not losslessly palettisable
    # BUILD THE PALETTE FROM THE ACTUAL COLOURS. Letting FASTOCTREE choose was
    # tried first and the identity check refused nearly every file: the quantiser
    # shifts colours even when there are fewer than 256 of them, so "<=256 colours"
    # did not survive the round trip. Mapping each unique RGBA to its own index is
    # what makes this provably lossless — the palette IS the colour list.
    uniq = [c for _, c in cols]
    idx = {c: i for i, c in enumerate(uniq)}
    q = Image.new('P', rgba.size)
    px = rgba.load()
    q.putdata([idx[px[x, y]] for y in range(rgba.height) for x in range(rgba.width)])
    pal = []
    for c in uniq:
        pal += [c[0], c[1], c[2]]
    pal += [0] * (768 - len(pal))
    q.putpalette(pal)
    alphas = bytes(c[3] for c in uniq)
    buf = io.BytesIO()
    if any(a < 255 for a in alphas):
        q.save(buf, 'PNG', optimize=True, transparency=alphas)
    else:
        q.save(buf, 'PNG', optimize=True)
    if buf.tell() >= old:
        return None                      # no win
    # PROVE IT. Round-trip and compare every pixel, alpha included.
    buf.seek(0)
    back = Image.open(buf).convert('RGBA')
    if back.size != rgba.size or back.tobytes() != rgba.tobytes():
        return None                      # not identical -> refuse
    return buf.getvalue(), old


def main(apply=False):
    pngs = []
    for root, _, fs in os.walk(os.path.join(ROOT, 'assets')):
        for f in fs:
            if f.endswith('.png'):
                pngs.append(os.path.join(root, f))
    if apply:
        os.makedirs(BACKUP, exist_ok=True)
    before = after = 0
    done = skipped = refused = 0
    for p in pngs:
        try:
            r = convert(p)
        except Exception:
            r = None
        if r is None:
            skipped += 1
            before += os.path.getsize(p); after += os.path.getsize(p)
            continue
        data, old = r
        before += old; after += len(data); done += 1
        if apply:
            rel = os.path.relpath(p, ROOT)
            bp = os.path.join(BACKUP, rel.replace('/', '__'))
            if not os.path.exists(bp):
                shutil.copy2(p, bp)
            open(p, 'wb').write(data)
    print(f'PNGs scanned      : {len(pngs)}')
    print(f'converted (proven lossless): {done}')
    print(f'left alone (>256 colours or no win): {skipped}')
    print(f'{before/1048576:.1f} MB -> {after/1048576:.1f} MB   saved {(before-after)/1048576:.1f} MB')
    print('APPLIED' if apply else 'DRY RUN — pass --apply')


if __name__ == '__main__':
    main('--apply' in sys.argv)
