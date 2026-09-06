#!/usr/bin/env python3
"""tint_avatar_boxes_0906g.py - each pilot's portrait box takes their own SHIP's colour.

    python _BUILD_SOURCE/tint_avatar_boxes_0906g.py            # measure + proof
    python _BUILD_SOURCE/tint_avatar_boxes_0906g.py --write

Mike, 0906: "each of there portrait boxes should be palette swapped to there ship color."

⚠ THE COLOUR IS MEASURED OFF EACH SHIP, NOT READ FROM THE TINT TABLE. `PILOTS[].tint` is close for
most pilots and WRONG for the two that just changed: Decker's hull is now yellow-dominant where it
was black, and Juggernaut's and Falva's hulls were replaced outright this drop. Taking the hue from
the art means the box cannot drift from the aircraft it is supposed to match - which is the whole
request - and it keeps working the next time a ship is recoloured.

The dominant hue is the SATURATED ink's circular mean, weighted by saturation. A plain average over
all pixels would be dragged to grey by the gunmetal every one of these ships is mostly made of, and
a plain modal hue would pick whichever accent happens to occupy the most pixels rather than the
colour the ship reads as.

⚠ AND ONLY THE FRAME MOVES, NOT THE FACE. The recolour is restricted to the box's grey metal -
saturation under 0.30 - and the accent bars, which are already the pilot's colour and are simply
re-hued. Skin sits at 0.18-0.75 saturation in the same hue band as several of these tints, so a
blanket hue rotation would turn faces blue for Axel and green for Cole. The interior window is
excluded by geometry as well as by saturation: nothing inside the frame's ring is touched.
"""
import os, sys, json, math, shutil, subprocess, colorsys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
AVATARS = os.path.join(ROOT, 'assets/game/pilot_avatars')
PILOTS = ['axel', 'decker', 'maverick', 'freezer', 'juggernaut', 'yuri', 'lizzie', 'falva', 'cole']
RING = 0.135          # fraction of the avatar's width that is frame; matches the authored plate


def ship_hue(pilot, rects, atlas):
    r = rects['ship_' + pilot]
    im = atlas.crop((r[0], r[1], r[0] + r[2], r[1] + r[3]))
    px = im.load()
    sx = sy = w = 0.0
    for y in range(im.height):
        for x in range(im.width):
            rr, gg, bb, aa = px[x, y]
            if aa < 32:
                continue
            h, s, v = colorsys.rgb_to_hsv(rr / 255., gg / 255., bb / 255.)
            if s < 0.28 or v < 0.20:
                continue
            wt = s * v
            sx += math.cos(h * 2 * math.pi) * wt
            sy += math.sin(h * 2 * math.pi) * wt
            w += wt
    if w <= 0:
        return None
    h = (math.atan2(sy, sx) / (2 * math.pi)) % 1.0
    return h


def retint(im, hue):
    """re-hue the frame only: its grey metal and its accent bars, never the portrait inside"""
    W, H = im.size
    ring = int(round(W * RING))
    px = im.load(); n = 0
    for y in range(H):
        for x in range(W):
            inside = (ring <= x < W - ring) and (ring <= y < H - ring)
            if inside:
                continue                       # the portrait window is off limits, by geometry
            r, g, b, a = px[x, y]
            if a < 32:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if v < 0.10:
                continue                       # the frame's black bevel stays black
            if s < 0.30:
                ns = 0.16 + 0.22 * v           # grey metal takes a restrained wash of the colour
            else:
                ns = s                         # the accent bars keep their punch, change their hue
            rr, gg, bb = colorsys.hsv_to_rgb(hue, min(1.0, ns), v)
            px[x, y] = (int(rr * 255 + .5), int(gg * 255 + .5), int(bb * 255 + .5), a)
            n += 1
    return n


def main():
    write = '--write' in sys.argv
    js = subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "const o={};for(const p of " + json.dumps(PILOTS) + ")o['ship_'+p]=BOFX.ships['ship_'+p];"
        "process.stdout.write(JSON.stringify(o));"], capture_output=True, cwd=ROOT)
    rects = json.loads(js.stdout.decode())
    atlas = Image.open(ATLAS).convert('RGBA')

    made, rows = {}, []
    for p in PILOTS:
        h = ship_hue(p, rects, atlas)
        f = os.path.join(AVATARS, 'pav_%s.png' % p)
        if h is None or not os.path.exists(f):
            rows.append((p, 'NO SHIP HUE' if h is None else 'NO AVATAR', '', '')); continue
        im = Image.open(f).convert('RGBA')
        n = retint(im, h)
        made[f] = im
        rgb = colorsys.hsv_to_rgb(h, 0.75, 0.92)
        rows.append((p, '%3d deg' % round(h * 360),
                     '#%02x%02x%02x' % tuple(int(c * 255) for c in rgb), '%d px' % n))
    print('%-11s %-8s %-9s %s' % ('pilot', 'ship hue', 'box tint', 'frame pixels'))
    print('-' * 46)
    for r in rows:
        print('%-11s %-8s %-9s %s' % r)

    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    T = 200
    proof = Image.new('RGB', ((T + 6) * 5, (T + 22) * 2), (18, 16, 22))
    d = ImageDraw.Draw(proof)
    for i, p in enumerate(PILOTS):
        f = os.path.join(AVATARS, 'pav_%s.png' % p)
        if f not in made:
            continue
        x, y = (i % 5) * (T + 6), (i // 5) * (T + 22)
        proof.paste(made[f].resize((T, T), Image.LANCZOS).convert('RGB'), (x, y))
        d.text((x + 3, y + T + 4), p, font=F, fill=(240, 240, 250))
    proof.save(os.path.join(ROOT, 'docs/PILOT_AVATARS_0906G.png'))
    print(os.linesep + 'wrote docs/PILOT_AVATARS_0906G.png')

    if not write:
        print('DRY RUN - nothing written. Re-run with --write.')
        return 0
    for f, im in made.items():
        bak = f + '.0906g.bak'
        if not os.path.exists(bak):
            shutil.copy2(f, bak)
        im.save(f)
    print('retinted %d avatar boxes' % len(made))
    return 0


if __name__ == '__main__':
    sys.exit(main())
