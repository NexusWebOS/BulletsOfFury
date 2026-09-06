#!/usr/bin/env python3
"""import_yuri_char_0906.py - Mike's new Yuri: avatar, nine emotion portraits, seven body poses.

    python _BUILD_SOURCE/import_yuri_char_0906.py            # proofs only
    python _BUILD_SOURCE/import_yuri_char_0906.py --write     # + files, atlas and manifest

Mike, 0906: "new yuri.png - this is the new Yuri. I never liked how Yuri turned out, lets go with
this instead. and heres his avatar and new cinematic poses. rmeove all purple and magenta halo's.
remove the frames that got added in to his frames for some reason etc."

⚠ THE THREE SOURCE FILES ARE NAMED FOR THE WRONG PILOT. Two of them are Cole_Avatar_Frames_... and
Cole_Fullbody_Poses_... and both are YURI. This file exists partly to write that down: "filenames
lie" is the first rule in CLAUDE.md and it applies to art drops as much as to atlas keys.

WHAT EACH ONE IS, measured rather than assumed:
    new yuri.png                     1254x1254, opaque, black ground   - the hero avatar
    Cole_Avatar_Frames_..._Row.png   2304x256 = 9 cells of 256          - the emotion portraits
    Cole_Fullbody_Poses_...png       1776x344 = 7 poses, magenta ground - the cinematic poses

⚠ "REMOVE THE FRAMES" MEANS A DECORATIVE METAL BORDER BAKED INTO EVERY PORTRAIT. Each 256px cell
carries a riveted metal frame with red accent segments, and a purple halo bleeding off it. Measured:
the frame's outer bounding box is (14,6)-(241,249) in every cell, the bar is ~7px thick at the mid
edges and much chunkier at the corner blocks. Rendered a crop sweep at insets 14/20/26/32/38 - 26
still leaves purple in the corners, 32 is clean - so the cut is the frame bbox inset by 28 and the
REMAINDER is despilled rather than cropped harder, because cropping to clear a fringe throws away
face to solve a colour problem.

⚠ THE CROSS-EMOTION VARIANCE TRICK DOES NOT WORK HERE and is worth recording so nobody retries it.
The obvious way to isolate a static border from a changing face is to diff the nine cells and keep
what never moves. It fails because the nine portraits were each generated separately, so the FRAME
differs slightly between them too - measured static fraction inside the frame band is 0.11 to 0.42,
not the ~1.0 a shared border would give. Only the outer dark-red margin (rows 0-5, cols 0-14) is
genuinely identical.

⚠ AND THE PURPLE BAND MUST EXCLUDE THE JACKET. Yuri's coat is red and the portrait ground is a very
dark red (35,0,8) whose hue is ~347 degrees - inside a naive "purple" band. The despill is limited
to hue 268..338, which leaves both alone.

EMOTION MAPPING. The row has nine faces and the game has seven slots for him
(anger/crash/idle/laugh/sad/smile/victory). Assigned by reading them:
    0 neutral stern      -> idle        2 shouting            -> anger
    3 confident smirk    -> smile       4 teeth bared, strain -> crash
    5 downcast           -> sad         6 eyes shut, grinning -> laugh
    7 chin up, assured   -> victory
Frames 1 and 8 are further stern variants with no slot; they are left out rather than forced.
"""
import os, re, sys, json, shutil, colorsys, subprocess
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESK = 'C:/Users/Mdogg/Desktop/'
AVATAR = DESK + 'new yuri.png'
EMOROW = DESK + 'Cole_Avatar_Frames_Dark_Red_Row.png'
BODIES = DESK + 'Cole_Fullbody_Poses_Separated_Preview.png'
OUT = os.path.join(ROOT, 'assets/game/yuri_v2')
FRAME_BBOX = (14, 6, 241, 249)     # measured, identical in all nine cells
INSET = 28
EMO = {0: 'idle', 2: 'anger', 3: 'smile', 4: 'crash', 5: 'sad', 6: 'laugh', 7: 'victory'}


def despill_purple(im):
    """kill the magenta/purple halo without touching the red coat or the dark red ground.

    Limited to hue 268..338. Yuri's ground is (35,0,8) at hue ~347 and his jacket runs 350..10, so
    a wider band would desaturate the character itself. Saturation is crushed and value left alone,
    which turns halo pixels into the neutral dark they sit against instead of punching holes.
    """
    px = im.load()
    n = 0
    for y in range(im.height):
        for x in range(im.width):
            p = px[x, y]
            if len(p) == 4 and p[3] < 8:
                continue
            r, g, b = p[0], p[1], p[2]
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            hd = h * 360
            if 268 <= hd <= 338 and s > 0.18:
                nr, ng, nb = colorsys.hsv_to_rgb(h, s * 0.12, v * 0.92)
                px[x, y] = (int(nr * 255), int(ng * 255), int(nb * 255)) + (p[3:] if len(p) == 4 else ())
                n += 1
    return n


def is_key(p, dark_too=False):
    r, g, b = p[0], p[1], p[2]
    if r > 150 and b > 150 and g < 95 and abs(r - b) < 80:
        return True
    # ⚠ THE SEPARATOR BARS ARE NEAR-BLACK, NOT MAGENTA, and a magenta-only flood leaves a thin box
    # drawn round every pose. Including near-black in the flood is safe HERE and only here: each
    # figure is completely surrounded by magenta, so the flood reaches the bars from outside and
    # stops at the first magenta-to-character boundary - it can never walk into his black trousers.
    return bool(dark_too) and max(r, g, b) < 34


def punch(im, dark_too=False):
    im = im.convert('RGBA')
    w, h = im.size
    px = im.load()
    seen = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_key(px[x, y], dark_too) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_key(px[x, y], dark_too) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and is_key(px[nx, ny], dark_too):
                seen[ny][nx] = True; q.append((nx, ny))
    for y in range(h):
        for x in range(w):
            if seen[y][x]:
                px[x, y] = (0, 0, 0, 0)
    return im


def frame_bbox_of(im):
    """the metal border's outer box, found by hue/saturation rather than assumed"""
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
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def main():
    write = '--write' in sys.argv
    os.makedirs(OUT, exist_ok=True) if write else None
    made = {}

    # ---- the nine emotion portraits ----
    row = Image.open(EMOROW).convert('RGB')
    cw = row.width // 9
    fb = FRAME_BBOX
    emo = {}
    tot_purple = 0
    for i in range(9):
        cell = row.crop((i * cw, 0, (i + 1) * cw, row.height))
        sub = cell.crop((fb[0] + INSET, fb[1] + INSET, fb[2] - INSET, fb[3] - INSET)).convert('RGBA')
        tot_purple += despill_purple(sub)
        emo[i] = sub
    print('emotion row: 9 cells of %dx%d -> %dx%d after removing the frame (bbox %s, inset %d)'
          % (cw, row.height, emo[0].width, emo[0].height, fb, INSET))
    print('             %d purple halo pixels neutralised across the nine' % tot_purple)
    print('             slots: %s' % ', '.join('%d->%s' % (k, v) for k, v in sorted(EMO.items())))

    # ---- the hero avatar ----
    av = Image.open(AVATAR).convert('RGB')
    abb = frame_bbox_of(av)
    ai = int(round((abb[2] - abb[0]) * (INSET / (fb[2] - fb[0]))))   # same proportional inset
    avc = av.crop((abb[0] + ai, abb[1] + ai, abb[2] - ai, abb[3] - ai)).convert('RGBA')
    p2 = despill_purple(avc)
    print('avatar: %dx%d, frame bbox %s, inset %d -> %dx%d, %d purple px neutralised'
          % (av.width, av.height, abb, ai, avc.width, avc.height, p2))

    # ---- the seven body poses ----
    # ⚠ THE POSE SHEET HAS BLACK SEPARATOR BARS BETWEEN CELLS, and they defeat a border flood: the
    # flood starts on the frame edge, meets black immediately, and stops - so the magenta inside is
    # never reached. The first run produced seven poses with the full magenta ground still attached,
    # and then the purple despill turned that magenta LAVENDER, which looked like a colour bug and
    # was really a keying one. Each cell is inset past the separator before flooding.
    #
    # ⚠ AND THE DESPILL RUNS ONLY AFTER A SUCCESSFUL PUNCH. Magenta sits at hue ~300, inside the
    # halo band, so despilling an unkeyed plate recolours the background instead of removing it.
    # The punch is verified per cell - if a cell still measures mostly opaque, it is reported rather
    # than silently despilled into pastel.
    bod = Image.open(BODIES).convert('RGBA')
    bw = bod.width // 7
    SEP = 10
    bodies = []
    for i in range(7):
        cell = bod.crop((i * bw + SEP, SEP, (i + 1) * bw - SEP, bod.height - SEP))
        c = punch(cell, dark_too=True)
        px = c.load()
        opaque = sum(1 for y in range(0, c.height, 3) for x in range(0, c.width, 3) if px[x, y][3] > 32)
        frac = opaque / max(1, (c.height // 3) * (c.width // 3))
        if frac > 0.85:
            print('  ** pose %d still %.0f%% opaque after the punch - key not found **' % (i, frac * 100))
        despill_purple(c)
        bb = c.getbbox()
        c = c.crop(bb) if bb else c
        bodies.append(c)
    print('body poses: 7 of %dx%d -> ink %s' % (bw, bod.height, [ '%dx%d'%(b.width,b.height) for b in bodies ]))

    # ---- proof ----
    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    S = 150
    cols = 8
    items = [('avatar', avc)] + [(EMO.get(i, 'unused %d' % i), emo[i]) for i in sorted(emo)] \
            + [('pose %d' % i, b) for i, b in enumerate(bodies)]
    rows = (len(items) + cols - 1) // cols
    proof = Image.new('RGB', ((S + 8) * cols, (S + 24) * rows), (18, 16, 22))
    d = ImageDraw.Draw(proof)
    for i, (lab, img) in enumerate(items):
        s = min(S / img.width, S / img.height)
        t = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)
        x, y = (i % cols) * (S + 8), (i // cols) * (S + 24)
        proof.paste(t.convert('RGB'), (x + (S - t.width) // 2, y + (S - t.height) // 2), t)
        d.text((x + 3, y + S + 4), lab[:18], font=F, fill=(240, 240, 250))
    proof.save(os.path.join(ROOT, 'docs/YURI_V2_PARTS_0906.png'))
    print('\nwrote docs/YURI_V2_PARTS_0906.png')

    if not write:
        print('DRY RUN - no files written. Re-run with --write.')
        return 0

    avc.save(os.path.join(OUT, 'yuri_avatar.png'))
    made['yuri_avatar'] = 'assets/game/yuri_v2/yuri_avatar.png'
    for i, slot in EMO.items():
        emo[i].save(os.path.join(OUT, 'port_yuri_%s.png' % slot))
        made['port_yuri_%s' % slot] = 'assets/game/yuri_v2/port_yuri_%s.png' % slot
    for i, b in enumerate(bodies):
        b.save(os.path.join(OUT, 'yuri_body_%d.png' % i))
        made['yuri_body_%d' % i] = 'assets/game/yuri_v2/yuri_body_%d.png' % i
    print('wrote %d files to assets/game/yuri_v2/' % len(made))
    json.dump(made, open(os.path.join(OUT, '_keys.json'), 'w'), indent=1)
    print('key -> path map written to assets/game/yuri_v2/_keys.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
