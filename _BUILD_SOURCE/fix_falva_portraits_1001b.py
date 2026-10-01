"""Falva's dialogue portraits were sliced off a 244px-pitch sheet with a 256px cell.

Measured (rows of the magenta rail lights at column 128):
  * idle and every emotion: box = rows 0..243, then rows 244..255 are the NEXT cell's top rail -
    "the top of her box added under the box".
  * talk-small / medium / wide / o: cut 22 rows low (best match against idle: dy=+22, dx=0), so the
    top rail is missing and rows 222..255 are empty.
  * crash / sad / victory: cut 11 rows low (bottom rail lights at 220..223 against idle's 231..234),
    so they lose 11 rows of top rail AND carry the next cell's rail at 240..244.
Rebuild from the untouched originals in _backups (never from this script's own output):
  full frames -> crop to rows 0..243;  shifted talk frames -> idle's rows 0..21 (top rail) over the
  talk frame placed at row 22.  Alpha is carried through unchanged.
"""
import os, glob
from PIL import Image
SRC = os.path.join(os.path.dirname(__file__), '_backups', 'falva_portraits_pre1001b')
DST = os.path.join(os.path.dirname(__file__), '..', 'assets', 'game', 'pilots_0922', 'portraits')
BOX_H = 244
SHIFT = {'talk-small': 22, 'talk-medium': 22, 'talk-wide': 22, 'talk-o': 22, 'crash': 11, 'sad': 11, 'victory': 11}
idle = Image.open(os.path.join(SRC, 'falva-idle.png')).convert('RGBA')
for f in sorted(glob.glob(os.path.join(SRC, 'falva-*.png'))):
    name = os.path.basename(f)[6:-4]
    im = Image.open(f).convert('RGBA')
    sh = SHIFT.get(name, 0)
    if sh:
        out = Image.new('RGBA', (256, BOX_H), (0, 0, 0, 0))
        out.paste(im.crop((0, 0, 256, BOX_H - sh)), (0, sh))
        out.paste(idle.crop((0, 0, 256, sh)), (0, 0))
    else:
        out = im.crop((0, 0, 256, BOX_H))
    out.save(os.path.join(DST, os.path.basename(f)), optimize=True)
    print(name, out.size)


# The in-play dialogue box draws the COMPACT comm set (comm_<pilot>_<emo>, 128px redraws), which inherited
# the same slicing at half scale: a 122px box pitch, talk-small/medium/wide/o 11 rows low and
# crash/sad/victory 6 rows low (best match against comm idle). Same repair, at that scale.
CSRC = os.path.join(os.path.dirname(__file__), '_backups', 'falva_comm_pre1001b')
CDST = os.path.join(os.path.dirname(__file__), '..', 'assets', 'game', 'pilots_0922', 'comm')
CBOX = 122
CSHIFT = {'talk-small': 10, 'talk-medium': 10, 'talk-wide': 10, 'talk-o': 10, 'crash': 5, 'sad': 5, 'victory': 5}   # set by the bottom rail lights (115..116), which a 1px face match disagrees with
cidle = Image.open(os.path.join(CSRC, 'comm_falva_idle.png')).convert('RGBA')
for f in sorted(glob.glob(os.path.join(CSRC, 'comm_falva_*.png'))):
    name = os.path.basename(f)[11:-4]
    im = Image.open(f).convert('RGBA')
    sh = CSHIFT.get(name, 0)
    if sh:
        out = Image.new('RGBA', (128, CBOX), (0, 0, 0, 0))
        out.paste(im.crop((0, 0, 128, CBOX - sh)), (0, sh))
        out.paste(cidle.crop((0, 0, 128, sh)), (0, 0))
    else:
        out = im.crop((0, 0, 128, CBOX))
    out.save(os.path.join(CDST, os.path.basename(f)), optimize=True)
    print('comm', name, out.size)
