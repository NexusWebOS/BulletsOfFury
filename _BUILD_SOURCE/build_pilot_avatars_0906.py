#!/usr/bin/env python3
"""build_pilot_avatars_0906.py - one square bordered avatar per pilot, from Mike's own frame.

    python _BUILD_SOURCE/build_pilot_avatars_0906.py --write

Mike, 0906: "make sure you use square'd bordered portraits for each pilot."

The reference he sent is his framed Yuri avatar - a square portrait inside a riveted metal border
with red accent segments. This takes THAT FRAME, lifts it off the plate, and composites every
pilot's own portrait inside it.

⚠ WHY THIS RATHER THAN NINE SPRITECOOK GENERATIONS, WHICH IS WHAT HE ASKED FOR. Two reasons, both
worth him knowing:

  BUDGET. 66 credits remain and a per-pilot edit is 18, so eight pilots is 144. It does not fit,
  and a single generation cannot do it either: `edit_asset_id` takes ONE source, so nine faces in
  one sheet would come back as nine invented people rather than nine likenesses.

  CONSISTENCY. Nine separate generations give nine slightly different borders - different rivet
  spacing, different accent lengths, different weights. Lifting one authored frame and reusing it
  gives a roster where the only thing that changes between slots is the face, which is the point of
  a lineup. It is also reversible and free to redo.

If he wants the FACES redrawn in the new style as well, that is the generation job and it needs
credits - this gets the square bordered look he asked for today, out of art he already owns.

⚠ THE FRAME IS LIFTED BY MEASUREMENT, NOT BY A GUESSED INSET. The plate's border is found by
hue/saturation (grey metal or the purple halo bleeding off it), the interior is punched to
transparent, and the portrait is composited UNDER it - so the frame's inner edge overlaps the
portrait exactly as it does on Yuri's original, with no seam and no double border.

⚠ AND THE PORTRAIT IS FITTED BY ITS INK, NOT ITS CANVAS. The nine port_*_idle cells have different
trims and aspect ratios (212x262 up to 394x433), so fitting by canvas would leave some faces tiny
and float others off-centre. Each is trimmed to its own ink first, then scaled to COVER the window
and centred on the upper third - a portrait crops best around the eyes, not the middle.
"""
import os, sys, json, colorsys, subprocess
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAME_SRC = 'C:/Users/Mdogg/Desktop/new yuri.png'
OUT = os.path.join(ROOT, 'assets/game/pilot_avatars')
SIZE = 256
PILOTS = ['axel', 'decker', 'maverick', 'freezer', 'juggernaut', 'yuri', 'lizzie', 'falva', 'cole']


def frame_mask(im):
    """the border's outer box, by colour rather than by a guessed inset"""
    px = im.convert('RGB').load()
    W, H = im.size
    xs, ys = [], []
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y]
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            hd = h * 360
            if (s < 0.25 and v > 0.16) or (268 <= hd <= 338 and s > 0.22 and v > 0.10):
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def build_frame():
    """the border as an RGBA overlay with a transparent middle"""
    src = Image.open(FRAME_SRC).convert('RGBA')
    bb = frame_mask(src)
    src = src.crop(bb)
    src = src.resize((SIZE, SIZE), Image.LANCZOS)
    # the ring thickness, measured on the original and scaled: the border runs ~12% of the plate
    ring = int(round(SIZE * 0.115))
    px = src.load()
    for y in range(ring, SIZE - ring):
        for x in range(ring, SIZE - ring):
            px[x, y] = (0, 0, 0, 0)
    return src, ring


def portrait(key):
    """the pilot's face, trimmed to its ink"""
    js = subprocess.run(['node', '-e',
        "const fs=require('fs');global.window=global;eval(fs.readFileSync('assets/manifest.js','utf8'));"
        "const k='port_%s_idle';const c=(BOFX.cells&&BOFX.cells[k])||null;"
        "process.stdout.write(JSON.stringify({cell:c, src:(BOFX.img&&BOFX.img[k])||null}));" % key],
        capture_output=True, cwd=ROOT)
    m = json.loads(js.stdout.decode())
    if m.get('cell'):
        sheet, x, y, w, h = m['cell']
        p = os.path.join(ROOT, 'assets/game/atlas/%s.png' % sheet)
        if not os.path.exists(p):
            return None
        im = Image.open(p).convert('RGBA').crop((x, y, x + w, y + h))
    elif m.get('src'):
        im = Image.open(os.path.join(ROOT, m['src'])).convert('RGBA')
    else:
        return None
    bb = im.getbbox()
    return im.crop(bb) if bb else im


def main():
    write = '--write' in sys.argv
    frame, ring = build_frame()
    win = SIZE - ring * 2
    print('frame lifted from %s -> %dx%d, ring %dpx, window %dpx'
          % (os.path.basename(FRAME_SRC), SIZE, SIZE, ring, win))

    made, tiles = {}, []
    for key in PILOTS:
        face = portrait(key)
        if face is None:
            print('  %-11s NO PORTRAIT' % key); continue
        # COVER the window, biased to the upper third - a face crops best around the eyes
        s = max(win / face.width, win / face.height)
        fw, fh = max(1, int(face.width * s)), max(1, int(face.height * s))
        big = face.resize((fw, fh), Image.LANCZOS)
        cv = Image.new('RGBA', (SIZE, SIZE), (10, 9, 14, 255))
        cv.alpha_composite(big, (ring + (win - fw) // 2, ring + int((win - fh) * 0.36)))
        cv.alpha_composite(frame, (0, 0))
        made[key] = cv
        tiles.append((key, cv))
        print('  %-11s portrait %dx%d -> fitted %dx%d' % (key, face.width, face.height, fw, fh))

    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    T = 150
    proof = Image.new('RGB', ((T + 8) * 5, (T + 22) * 2), (18, 16, 22))
    d = ImageDraw.Draw(proof)
    for i, (k, im) in enumerate(tiles):
        x, y = (i % 5) * (T + 8), (i // 5) * (T + 22)
        proof.paste(im.resize((T, T), Image.LANCZOS).convert('RGB'), (x, y))
        d.text((x + 3, y + T + 4), k, font=F, fill=(240, 240, 250))
    proof.save(os.path.join(ROOT, 'docs/PILOT_AVATARS_0906.png'))
    print('\nwrote docs/PILOT_AVATARS_0906.png')

    if not write:
        print('DRY RUN - no files written. Re-run with --write.')
        return 0
    os.makedirs(OUT, exist_ok=True)
    for k, im in made.items():
        im.save(os.path.join(OUT, 'pav_%s.png' % k))
    print('wrote %d avatars to assets/game/pilot_avatars/' % len(made))
    return 0


if __name__ == '__main__':
    sys.exit(main())
