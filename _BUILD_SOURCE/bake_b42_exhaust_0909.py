#!/usr/bin/env python3
"""
bake_b42_exhaust_0909.py - THE B-42 GETS AN EXHAUST THE WAY THE IN-GAME HULLS HAVE ONE.

Mike, 0909: "do not overlay the thrusters the way the cinematic does, instead do the way the
in-game version is while playing."

There is no longer any live thruster overlay to choose - drawShipThruster is gone from game.js and
nthp_ survives only in comments. Since 0906q every in-game hull carries its flame PAINTED ONTO THE
PLATE (SHIP_FLAME_BAKED), and the cinematic simply blits whatever plate it is handed. So "the way
the in-game version is" means the plate must carry the flame, and the B-42 plates do not: measured
across her costume, ZERO white-hot pixels against 97-111 on every frame of her stock ship.

The flame is lifted from HER OWN stock plate rather than generated, so the costume burns exactly
what the ship it replaces burns. Her level frame carries two plumes below the hull at y>=176; the
left one is taken as the template and seated centred on the B-42's tail, scaled to the same share
of hull height it occupies on the stock ship.

⚠ ONLY THE NINE LEVEL-ISH FRAMES ARE BAKED. base/_nf/_l/_r/_pv0.._pv4 are nose-up views where
"behind the aircraft" is unambiguously down. The eight _br frames are the warbird rotated in the
image plane, so a downward plume would point out of its flank; those need the flame drawn per
orientation the way her stock roll frames have it, and inventing it here would be the 0906y
mistake - deriving a pose by rotation because the maths is easy rather than because it is right.

⚠ AND THE B-42 IS A PROPELLER AIRCRAFT. A jet plume under a warbird is a judgement call, not a
measurement, so this is written to be trivially reversible: run with --revert to restore the
plates from the .prebake backup it writes on the first run.
"""
import io, json, os, re, shutil, sys
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
GAME = os.path.join(ROOT, 'assets/game.js')
MAN = os.path.join(ROOT, 'assets/manifest.js')
LIZ = os.path.join(ROOT, 'assets/game/atlas/ships/ship_lizzie.png')
B42 = os.path.join(ROOT, 'assets/game/atlas/ships/ship_lizzie_b42.png')
BAK = os.path.join(ROOT, '_BUILD_SOURCE', '_backups', 'ship_lizzie_b42.png.prebake')
LEVELISH = ['', '_nf', '_l', '_r', '_pv0', '_pv1', '_pv2', '_pv3', '_pv4']

if '--revert' in sys.argv:
    if os.path.exists(BAK):
        shutil.copyfile(BAK, B42)
        print('restored ' + B42)
    else:
        print('no backup at ' + BAK)
    sys.exit(0)

g = io.open(GAME, encoding='utf-8', newline='').read()
gst = g.index('const LIZZIE_B42_RECTS={')
R = {m.group(1): [int(v) for v in m.group(2).split(',')]
     for m in re.finditer(r'"([^"]*)":\[([0-9,\s]+)\]', g[gst:g.index('};', gst) + 2])}
src = io.open(MAN, encoding='utf-8', newline='').read()
i = src.index('"ships"')
j = src.index('{', i)
d = 0
for k in range(j, len(src)):
    if src[k] == '{':
        d += 1
    elif src[k] == '}':
        d -= 1
        if d == 0:
            SHIPS = json.loads(src[j:k + 1])
            break

# ---- lift the template off her own stock level plate ------------------------------------------
e = SHIPS['ship_lizzie']
stock = Image.open(LIZ).convert('RGBA').crop((e[0], e[1], e[0] + e[2], e[1] + e[3]))
sa = np.array(stock)
H0 = sa.shape[0]
tail = sa[176:, :, :]                       # below the hull: the two plumes and nothing else
cols = np.where((tail[:, :, 3] > 40).any(axis=0))[0]
# split the two plumes on the widest gap between inked columns
gaps = np.diff(cols)
cut = cols[int(np.argmax(gaps))] if len(gaps) else cols[-1]
left = cols[cols <= cut]
plume = Image.fromarray(tail[:, left.min():left.max() + 1].astype(np.uint8), 'RGBA')
pa = np.array(plume)
ys = np.where((pa[:, :, 3] > 40).any(axis=1))[0]
plume = plume.crop((0, ys.min(), plume.width, ys.max() + 1))
share = plume.height / float(H0)            # the plume as a share of the stock hull's height
print('template lifted from her stock plate: %dx%d, %.1f%% of hull height'
      % (plume.width, plume.height, 100 * share))

if not os.path.exists(BAK):
    shutil.copyfile(B42, BAK)
sheet = Image.open(BAK).convert('RGBA')
out = sheet.copy()
done = []
for suf in LEVELISH:
    r = R[suf]
    cell = sheet.crop((r[0], r[1], r[0] + r[2], r[1] + r[3]))
    ca = np.array(cell)
    m = ca[:, :, 3] > 40
    if not m.any():
        continue
    ys = np.where(m.any(axis=1))[0]
    bot = ys.max()
    # the tail is the inked columns on the lowest few rows - the fuselage, not a wingtip
    band = m[max(0, bot - 6):bot + 1]
    xs = np.where(band.any(axis=0))[0]
    cx = int((xs.min() + xs.max()) / 2)
    ph = max(4, int(round(r[3] * share)))
    pw = max(2, int(round(plume.width * ph / plume.height)))
    p = plume.resize((pw, ph), Image.LANCZOS)
    # seat it INSIDE the tail by a fifth of its height so it can never float
    layer = Image.new('RGBA', cell.size, (0, 0, 0, 0))
    layer.paste(p, (cx - pw // 2, bot - ph // 5))
    cell = Image.alpha_composite(cell, layer)
    out.paste(cell, (r[0], r[1]))
    done.append(suf or '(base)')
out.save(B42)
print('baked onto %d frames: %s' % (len(done), ', '.join(done)))
print('left alone: the 8 _br frames - a rotated warbird needs its flame drawn per orientation')
print('backup at ' + os.path.basename(BAK) + '   (--revert restores it)')
