#!/usr/bin/env python3
"""
sc_fetch.py - pull a SpriteCook asset at FULL resolution WITH correct alpha.

    python3 _BUILD_SOURCE/sc_fetch.py out.png --raw <raw_url> --pixel <pixel_url>

⚠ NEITHER SPRITECOOK URL IS USABLE ON ITS OWN, and this is the third time in two drops it has cost
a rebuild:

    pixel_url   real alpha, but SMART-CROPPED AND DOWNSCALED. A transparent-heavy asset collapses
                hard - a 2K window frame came back 98x98, a 16-cursor sheet came back 98x98.
    raw_url     full resolution, but NO alpha: transparency is rendered as a light grey
                CHECKERBOARD (sampled 224,224,224 / 255,255,255 along the top edge), which a
                luminance key turns into a half-opaque chessboard baked into the sprite.

So: take the COLOUR from raw and the ALPHA from pixel. The pixel alpha is low-resolution but it is
geometrically correct, so upscaling it to the raw size and using it as a mask gives full detail with
honest transparency. Smart-crop means the two images are not the same framing, so the mask is fitted
by matching aspect and scaling - which holds because smart_crop only ever crops to the ink.

A threshold is applied after the upscale because a LANCZOS-resized mask has soft shoulders, and a
soft shoulder over a checkerboard is exactly how grey fringing gets in.
"""
import argparse, io, os, sys, urllib.request
from PIL import Image


def get(url):
    with urllib.request.urlopen(url, timeout=180) as r:
        return Image.open(io.BytesIO(r.read())).copy()


def key_checkerboard(raw, light=200, sat=26, seed_centre=False):
    """Flood the transparency CHECKERBOARD out of a raw plate, from the borders inward.

       ⚠ NEEDED WHEN pixel_url ITSELF IS UNUSABLE. The normal path takes alpha from pixel_url, but
       smart-crop can mangle that asset outright - the BULLETS OF DEBUG button sheet came back as a
       92px-wide vertical sliver of a 6x3 grid, so there was no mask to borrow. The raw plate was
       perfect.

       Keyed by FLOOD FILL FROM THE EDGES, not by colour alone: the checker greys (~224 and ~255,
       near-neutral) also occur inside artwork as highlights, and a global colour key eats them.
       Only near-neutral light pixels REACHABLE from the border are background, so a white specular
       inside a button is safe because it is enclosed by dark outline."""
    raw = raw.convert('RGB')
    w, h = raw.size
    px = raw.load()
    def isbg(x, y):
        r, g, b = px[x, y]
        return (max(r, g, b) >= light) and (max(r, g, b) - min(r, g, b) <= sat)
    seen = bytearray(w * h)
    stack = []
    for x in range(w):
        for y in (0, h - 1):
            if isbg(x, y) and not seen[y * w + x]: seen[y * w + x] = 1; stack.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if isbg(x, y) and not seen[y * w + x]: seen[y * w + x] = 1; stack.append((x, y))
    # ⚠ A HOLLOW FRAME NEEDS A SECOND SEED. The window plate is a nine-patch: its interior is
    # ALSO checkerboard, but it is enclosed by the frame, so a flood that starts only at the
    # border can never reach it and the middle comes back opaque white. Seeding the centre too
    # clears the well, and costs nothing on a solid sprite because the centre is then not
    # background and the seed simply does not take.
    if seed_centre:
        cx, cy = w // 2, h // 2
        if isbg(cx, cy) and not seen[cy * w + cx]:
            seen[cy * w + cx] = 1; stack.append((cx, cy))
    while stack:
        x, y = stack.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and isbg(nx, ny):
                seen[ny * w + nx] = 1; stack.append((nx, ny))
    out = raw.convert('RGBA')
    op = out.load()
    for y in range(h):
        row = y * w
        for x in range(w):
            if seen[row + x]:
                op[x, y] = (0, 0, 0, 0)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--raw', required=True)
    ap.add_argument('--pixel')
    ap.add_argument('--centre', action='store_true',
                    help='also seed the flood at the image centre, for hollow nine-patch frames')
    ap.add_argument('--keycheck', action='store_true',
                    help='ignore --pixel and flood the checkerboard out of --raw instead')
    ap.add_argument('--thresh', type=int, default=128)
    ap.add_argument('--scale', type=float, default=1.0, help='resize the finished plate')
    a = ap.parse_args()

    raw = get(a.raw).convert('RGB')
    if a.keycheck:
        out = key_checkerboard(raw, seed_centre=a.centre)
        bb = out.getbbox()
        if bb: out = out.crop(bb)
        if a.scale != 1.0:
            out = out.resize((max(1,int(out.width*a.scale)), max(1,int(out.height*a.scale))), Image.LANCZOS)
        os.makedirs(os.path.dirname(os.path.abspath(a.out)) or '.', exist_ok=True)
        out.save(a.out)
        print('%s  %dx%d  (raw %dx%d, checkerboard keyed)' % (a.out, out.width, out.height, raw.width, raw.height))
        return
    pix = get(a.pixel).convert('RGBA')
    alpha = pix.split()[3]

    # the two framings differ only by smart-crop; fit the mask onto the raw plate
    if alpha.size != raw.size:
        alpha = alpha.resize(raw.size, Image.LANCZOS)
    alpha = alpha.point(lambda v: 255 if v >= a.thresh else 0)

    out = raw.convert('RGBA')
    out.putalpha(alpha)
    bb = out.getbbox()
    if bb:
        out = out.crop(bb)
    if a.scale != 1.0:
        out = out.resize((max(1, int(out.width * a.scale)), max(1, int(out.height * a.scale))), Image.LANCZOS)

    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or '.', exist_ok=True)
    out.save(a.out)
    px = out.load()
    opaque = sum(1 for y in range(0, out.height, 4) for x in range(0, out.width, 4) if px[x, y][3] > 200)
    tot = len(range(0, out.height, 4)) * len(range(0, out.width, 4))
    print('%s  %dx%d  (raw %dx%d, mask %dx%d)  %d%% opaque'
          % (a.out, out.width, out.height, raw.width, raw.height, pix.width, pix.height,
             round(100 * opaque / max(1, tot))))


if __name__ == '__main__':
    main()
