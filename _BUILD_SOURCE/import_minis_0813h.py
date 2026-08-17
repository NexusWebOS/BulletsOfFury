#!/usr/bin/env python3
"""
DROP 0813H - IMPORT MIKE'S ICE AND OLIVE MINIBOSSES

Mike sent six 1254x1254 plates on a magenta key: an ICE unit and an OLIVE unit, each in intact and
two progressively battle-damaged states. These fill the two slots the reshuffle emptied - stage 3
(thorn rime out) and stage 4 (blacksteel moving to stage 6).

THE KEY IS REMOVED BY CONNECTIVITY, NOT BY COLOUR. A threshold on magenta would also eat the blue
highlights and any magenta-ish pixel inside the hull. Flood-filling inward from the borders is what
separates BACKGROUND from SUBJECT - the same argument the nfw_wall_0 cleanup makes, where 62% of the
image was near-white and a colour key would have eaten the flame's own core.

ANY MAGENTA LEFT ON THE RIM BECOMES A BLACK EDGE. Standing rule: purple/magenta halos are converted,
never deleted. The alpha key leaves a fringe on an anti-aliased edge; those pixels keep their alpha
and take black, so the silhouette is unchanged.

Ordered intact -> damaged by SUBJECT PIXEL COUNT: battle damage removes hull, so the intact plate is
the one with the most subject left.
"""
import os, sys, glob
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DL   = os.path.join(os.path.expanduser('~'), 'Downloads')
OUTD = os.path.join(ROOT, 'assets', 'game')
TARGET = 256          # authored size for the nsb_ miniboss family

def is_key(p):
    r, g, b, a = p
    return a > 0 and r > 180 and b > 180 and g < 110      # magenta family

def is_fringe(p):
    r, g, b, a = p
    return a > 0 and r > 120 and b > 120 and g < r * 0.72 and g < b * 0.72

def process(path):
    im = Image.open(path).convert('RGBA')
    W, H = im.size
    px = im.load()
    # --- flood fill the key inward from every border pixel that is key-coloured
    seen = bytearray(W * H)
    stack = []
    for x in range(W):
        for y in (0, H - 1):
            if is_key(px[x, y]): stack.append((x, y))
    for y in range(H):
        for x in (0, W - 1):
            if is_key(px[x, y]): stack.append((x, y))
    while stack:
        x, y = stack.pop()
        i = y * W + x
        if seen[i]: continue
        if not is_key(px[x, y]): continue
        seen[i] = 1
        px[x, y] = (0, 0, 0, 0)
        if x > 0:     stack.append((x - 1, y))
        if x < W - 1: stack.append((x + 1, y))
        if y > 0:     stack.append((x, y - 1))
        if y < H - 1: stack.append((x, y + 1))
    # --- surviving magenta fringe on the rim -> BLACK, alpha preserved
    fringe = 0
    for y in range(H):
        for x in range(W):
            p = px[x, y]
            if p[3] == 0 or not is_fringe(p): continue
            edge = False
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x+dx, y+dy
                if nx<0 or ny<0 or nx>=W or ny>=H or px[nx,ny][3]==0: edge=True; break
            if edge:
                px[x, y] = (0, 0, 0, p[3]); fringe += 1
    bbox = im.getbbox()
    if bbox: im = im.crop(bbox)
    subject = sum(1 for p in im.getdata() if p[3] > 0)
    return im, subject, fringe

# ⚠ SIZE ALONE IS NOT A FILTER. The first run matched EVERY 1254x1254 png in Downloads and swept up
# mysterynexus.png, "roster builder.png" and two SE1_ui_clean screenshots, then wrote them into
# assets/game as olivewarden plates. Three tests now, all of which a screenshot fails:
#   1. the filename is a UUID (what the image drop produces)
#   2. the plate is MOSTLY key colour - a sprite on magenta is >50% background
#   3. after keying it has real transparency - a screenshot keeps ~100% of its pixels
import re
UUID = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.png$', re.I)
cands = []
for f in glob.glob(os.path.join(DL, '*.png')):
    if not UUID.match(os.path.basename(f)): continue
    try:
        with Image.open(f) as t:
            if t.size != (1254, 1254): continue
            im = t.convert('RGBA'); px = im.load()
            key = tot = 0
            for y in range(0, 1254, 6):
                for x in range(0, 1254, 6):
                    tot += 1
                    if is_key(px[x, y]): key += 1
            if key < tot * 0.35:
                print('skip %-40s only %d%% key colour - not a sprite on magenta'
                      % (os.path.basename(f), 100*key//max(1,tot)))
                continue
    except Exception:
        continue
    cands.append(f)
print('%d plate(s) accepted' % len(cands))

done = []
for f in sorted(cands):
    im, subj, fr = process(f)
    px = im.load()
    n = R = G = B = 0
    for y in range(0, im.height, 3):
        for x in range(0, im.width, 3):
            p = px[x, y]
            if p[3] < 40: continue
            n += 1; R += p[0]; G += p[1]; B += p[2]
    if not n: print('%-40s empty after key' % os.path.basename(f)); continue
    R//=n; G//=n; B//=n
    fam = 'ice' if B > R + 15 else 'olive'
    done.append((fam, subj, im, os.path.basename(f), fr))
    print('%-40s %-6s subject %7d px  trimmed %dx%d  fringe->black %d'
          % (os.path.basename(f)[:40], fam, subj, im.width, im.height, fr))

os.makedirs(OUTD, exist_ok=True)
written = []
for fam in ('ice', 'olive'):
    grp = sorted([d for d in done if d[0] == fam], key=lambda d: -d[1])   # most subject = intact
    names = ['intact', 'damaged', 'critical']
    for i, d in enumerate(grp[:3]):
        im = d[2]
        im2 = im.copy(); im2.thumbnail((TARGET, TARGET), Image.NEAREST)
        key = 'nsb_%s_%s' % ('rimewall' if fam == 'ice' else 'olivewarden', names[i])
        p = os.path.join(OUTD, key + '.png')
        im2.save(p)
        written.append((key, im2.width, im2.height, d[1]))
        print('  -> assets/game/%s.png  %dx%d' % (key, im2.width, im2.height))

print('\n%d plate(s) written' % len(written))
for k, w, h, s in written: print('   %-34s %dx%d' % (k, w, h))
