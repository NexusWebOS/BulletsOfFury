#!/usr/bin/env python3
"""Contact sheet for the infusion showcase: one frame from the MIDDLE of each beat, labelled.

Read the sheet before believing the reel. This is the check that rejected the first capture
(stage 2, FIRE DMG ABSORBED on every fire beat) and the second (stage 1's water, where the
pale water orb was invisible against a pale blue ocean).
"""
import os, sys
from PIL import Image, ImageDraw
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SH = os.path.join(ROOT, '_shots', 'infusions_0917')
FPS = 15
BEATS = [(2.5, 'MACHINE GUN, PLAIN'), (3.5, 'INCENDIARY'), (3.5, 'FIREBURST'),
         (3.5, 'GODS WRATH'), (3.5, 'GIANT BEAM (KINETIC)'), (4.0, 'CHROMIUM'),
         (3.5, 'WATER ORB'), (4.5, 'FUSION')]

def main():
    picks, n = [], 0
    for secs, name in BEATS:
        cnt = int(secs * FPS)
        picks.append((n + int(cnt * 0.62), name))      # past the grant, into the effect
        n += cnt
    cols = 4
    ims = []
    for idx, name in picks:
        p = os.path.join(SH, 'f%04d.png' % idx)
        if not os.path.exists(p):
            print('missing', p); continue
        im = Image.open(p).convert('RGBA')
        bg = Image.new('RGBA', im.size, (0, 0, 0, 255))
        bg.paste(im, (0, 0), im)                        # composite, never convert() (0906v)
        ims.append((bg, name, idx))
    if not ims: return
    w, h = ims[0][0].size
    tw, th = w // 2, h // 2
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * tw, rows * (th + 20)), (10, 10, 14))
    d = ImageDraw.Draw(sheet)
    for i, (im, name, idx) in enumerate(ims):
        x, y = (i % cols) * tw, (i // cols) * (th + 20)
        sheet.paste(im.resize((tw, th), Image.LANCZOS).convert('RGB'), (x, y + 20))
        d.text((x + 6, y + 5), '%d  %s  (f%04d)' % (i + 1, name, idx), fill=(235, 220, 150))
    out = os.path.join(SH, '_contact.png')
    sheet.save(out)
    print('contact sheet ->', out, sheet.size)

if __name__ == '__main__':
    main()
