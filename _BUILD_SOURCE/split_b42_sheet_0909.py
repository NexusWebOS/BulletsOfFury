#!/usr/bin/env python3
"""
split_b42_sheet_0909.py - LIZZIE'S B-42 COSTUME GETS ITS OWN SHEET.

Mike, 0909: "make a seperate atlas sheet for lizzie's alternate costume ... thats her b-42 sheet
that will be used in place of her ship if we use the password Bomber when the game loads."

The costume was riding inside ship_lizzie.png, so every player downloaded 17 bomber frames whether
or not they had ever typed BOMBER. It moves to assets/game/atlas/ships/ship_lizzie_b42.png and is
loaded only when the skin is actually on.

⚠ THE SHEET CANNOT BE CHOSEN BY KEY ALONE, WHICH IS WHY THIS NEEDED A LOADER CHANGE TOO.
Every other pilot resolves ship_<pilot>_* to nsa_ship_<pilot> from the key, because the key names
the owner. The costume uses THE SAME KEYS - applyLizzieSkin repoints BOFX.ships in place - so the
key cannot say which of her two sheets a rect belongs to. _shipSheetOf reads lizzieSkinOn for her
keys, and applyLizzieSkin flushes that cache alongside _shipCells. Flushing one and not the other
is the 0906g bug exactly: the table changes and every draw keeps showing the plate it already
baked, state correct and pixels wrong.

⚠ AND FOUR OF THE SEVENTEEN FRAMES ARE ALREADY WRONG, FROM BEFORE ANY OF THIS.
(base) and _pv2 crop Juggernaut's and Maverick's aircraft, and _br1 and _br5 are stubs of a few
hundred pixels rather than an aeroplane. They are wrong in the pre-0909 atlas too, so they are
carried across unchanged rather than quietly patched - moving art is not the place to start
guessing at rects nobody has verified.
"""
import io, json, os, re, sys
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
GAME = os.path.join(ROOT, 'assets/game.js')
MAN = os.path.join(ROOT, 'assets/manifest.js')
SRC = os.path.join(ROOT, 'assets/game/atlas/ships/ship_lizzie.png')
OUT = os.path.join(ROOT, 'assets/game/atlas/ships/ship_lizzie_b42.png')
B42J = os.path.join(ROOT, 'assets/data/lizzie_b42_source_rects.json')
PAD = 2

g = io.open(GAME, encoding='utf-8', newline='').read()
gst = g.index('const LIZZIE_B42_RECTS={')
gen = g.index('};', gst) + 2
B42 = {m.group(1): [int(v) for v in m.group(2).split(',')]
       for m in re.finditer(r'"([^"]*)":\[([0-9,\s]+)\]', g[gst:gen])}
if len(B42) != 17:
    print('expected 17 B-42 rects, parsed %d' % len(B42))
    sys.exit(1)

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
            SPAN = (j, k + 1)
            SHIPS = json.loads(src[j:k + 1])
            break

sheet = Image.open(SRC).convert('RGBA')
cells = [(suf, sheet.crop((e[0], e[1], e[0] + e[2], e[1] + e[3])), e) for suf, e in B42.items()]

area = sum((im.width + PAD * 2) * (im.height + PAD * 2) for _, im, _ in cells)
W = 1 << (max(256, int((area * 1.18) ** 0.5)) - 1).bit_length()
placed, x, y, rowh = {}, 0, 0, 0
for suf, im, _ in sorted(cells, key=lambda t: -t[1].height):
    ww, hh = im.width + PAD * 2, im.height + PAD * 2
    if x + ww > W:
        x, y, rowh = 0, y + rowh, 0
    placed[suf] = (x + PAD, y + PAD)
    x += ww
    rowh = max(rowh, hh)
H = y + rowh

out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
newb42 = {}
for suf, im, e in cells:
    nx, ny = placed[suf]
    out.paste(im, (nx, ny))
    newb42[suf] = [nx, ny, im.width, im.height, e[4], e[5], e[6], e[7]]
out.save(OUT)

chk = Image.open(OUT).convert('RGBA')
bad = [suf for suf, im, _ in cells
       if not np.array_equal(np.array(im),
                             np.array(chk.crop((newb42[suf][0], newb42[suf][1],
                                                newb42[suf][0] + newb42[suf][2],
                                                newb42[suf][1] + newb42[suf][3]))))]
if bad:
    print('ABORT - %d cells did not survive: %s' % (len(bad), ', '.join(bad)))
    sys.exit(1)

# --- rebuild ship_lizzie.png WITHOUT the costume ------------------------------------------------
liz = [(k, sheet.crop((e[0], e[1], e[0] + e[2], e[1] + e[3])), e)
       for k, e in SHIPS.items() if k.startswith('ship_lizzie')]
# aliases share a rect; pack each distinct rect once and point every key at it
uniq = {}
for k, im, e in liz:
    uniq.setdefault(tuple(e[:4]), (im, e))
area = sum((im.width + PAD * 2) * (im.height + PAD * 2) for im, _ in uniq.values())
W2 = 1 << (max(256, int((area * 1.18) ** 0.5)) - 1).bit_length()
p2, x, y, rowh = {}, 0, 0, 0
for r, (im, e) in sorted(uniq.items(), key=lambda t: -t[1][0].height):
    ww, hh = im.width + PAD * 2, im.height + PAD * 2
    if x + ww > W2:
        x, y, rowh = 0, y + rowh, 0
    p2[r] = (x + PAD, y + PAD)
    x += ww
    rowh = max(rowh, hh)
H2 = y + rowh
liznew = Image.new('RGBA', (W2, H2), (0, 0, 0, 0))
for r, (im, e) in uniq.items():
    liznew.paste(im, p2[r])
newships = dict(SHIPS)
for k, im, e in liz:
    nx, ny = p2[tuple(e[:4])]
    newships[k] = [nx, ny, e[2], e[3], e[4], e[5], e[6], e[7]]
liznew.save(SRC)

chk2 = Image.open(SRC).convert('RGBA')
bad2 = [k for k, im, e in liz
        if not np.array_equal(np.array(im),
                              np.array(chk2.crop((newships[k][0], newships[k][1],
                                                  newships[k][0] + newships[k][2],
                                                  newships[k][1] + newships[k][3]))))]
if bad2:
    print('ABORT - %d lizzie cells did not survive: %s' % (len(bad2), ', '.join(bad2[:8])))
    sys.exit(1)

print('ship_lizzie_b42.png  %dx%d  %.2f MB   17 costume frames' % (W, H, os.path.getsize(OUT) / 1e6))
print('ship_lizzie.png      %dx%d  %.2f MB   %d keys over %d distinct cells'
      % (W2, H2, os.path.getsize(SRC) / 1e6, len(liz), len(uniq)))
print('verify: all %d cells byte-identical across both sheets' % (len(cells) + len(liz)))

io.open(MAN, 'w', encoding='utf-8', newline='').write(
    src[:SPAN[0]] + json.dumps(newships, separators=(',', ':'), sort_keys=False) + src[SPAN[1]:])
nl = '\r\n' if '\r\n' in g[:20000] else '\n'
lines = ['const LIZZIE_B42_RECTS={']
for suf, r in newb42.items():
    lines.append('  %s:%s,' % (json.dumps(suf), json.dumps(r, separators=(',', ','))))
lines.append('};')
io.open(GAME, 'w', encoding='utf-8', newline='').write(g[:gst] + nl.join(lines) + g[gen:])
io.open(B42J, 'w', encoding='utf-8', newline='\n').write(json.dumps(newb42, indent=1) + '\n')
print('wrote both sheets, the manifest, LIZZIE_B42_RECTS and the b42 json')
