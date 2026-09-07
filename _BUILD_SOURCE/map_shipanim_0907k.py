#!/usr/bin/env python3
"""map_shipanim_0907k.py - which pack cell fills each of the game's 25 ship frames.

    python _BUILD_SOURCE/map_shipanim_0907k.py juggernaut

Renders the mapping so it can be looked at before anything is written into the atlas. Reads the
de-fringed cells and `_audit.json` that `audit_shipanim_0907j.py --write` leaves behind.

⚠ THE MAP IS PER SHIP AND IT IS NOT THE GRID. The pack's own README says so - "repeated angles,
underside/design drift, and inconsistent rotation order" - and Juggernaut proves it twice: his
row 3 is a full 360-degree in-plane SPIN, which is not the game's `_pv*` bank steps at all, and
his row 2 carries THREE left banks against TWO right ones.

⚠ AND A MISSING PARTNER IS SHARED, NEVER MIRRORED. Mirroring r2c0 to make a right bank is exactly
the left-right symmetry 0907b/0907c exist to remove: a mirrored pair reads as "banking" and never
as WHICH WAY, which is the whole reason these sheets were commissioned. Where the sheet is short a
frame, two names point at one authored cell and that is recorded here rather than papered over.
"""
import os, sys, json
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLICED = os.path.join(ROOT, 'assets/game/ships_sliced')

# frame name -> (source cell, why)
MAP = {
    'juggernaut': [
        ('HULL', [
            ('',      'r0c0', 'level top view'),
            ('_nf',   'r0c0', 'same plate; the pack is flameless, the build bakes the flame on'),
        ]),
        ('BANK / PIVOT', [
            ('_pv0',  'r2c2', 'lean -0.106'),
            ('_pv1',  'r2c1', 'lean -0.058'),
            ('_pv2',  'r2c3', 'level'),
            ('_pv3',  'r2c6', 'lean +0.041'),
            ('_pv4',  'r2c5', 'lean +0.107'),
            ('_l',    'r2c0', 'narrowest bank, 154 px'),
            ('_r',    'r2c6', 'SHARED with _pv3 - the sheet has no third right bank'),
        ]),
        ('BARREL ROLL', [('_br%d' % i, 'r0c%d' % i, '') for i in range(8)]),
        # ⚠ ROW 1 IS READ BACKWARDS, BECAUSE THIS SHEET LOOPS THE OTHER WAY FROM THE FLEET.
        # Rendered at 2x, Juggernaut's r1c2 is TAIL-ON (both engine bells face-on) and r1c6 is
        # NOSE-ON (the canopy dome, wings at full span). Maverick's authored reel - the fleet's
        # reference since 0906z, and what derive_somersault_0907a's SO_VIEW encodes - has nose-on
        # at so2 and tail-on at so6. So the pack pitches nose-UP-and-over where every other ship
        # pitches nose-DOWN-and-under. Reversing the row costs nothing and keeps one manoeuvre
        # across nine pilots; playing it as-authored would make Juggernaut alone loop backwards.
        # ⚠ AND THE ROW IS ONE FRAME SHORT: its quarter points sit at c2/c4/c6 with LEVEL at
        # BOTH c0 and c7, i.e. 0/45/90/135/180/225/270/360 with 315 never drawn.
        ('SOMERSAULT', [
            ('_so0', 'r1c0', 'level'),
            ('_so1', 'r1c7', 'the 315 step is not on the sheet - this is its second level frame'),
            ('_so2', 'r1c6', 'NOSE-ON'),
            ('_so3', 'r1c5', ''),
            ('_so4', 'r1c4', 'BELLY'),
            ('_so5', 'r1c3', ''),
            ('_so6', 'r1c2', 'TAIL-ON'),
            ('_so7', 'r1c1', ''),
        ]),
    ],
}
UNUSED = {'juggernaut': ('row 3 (all 8)', 'a full 360-degree in-plane SPIN - no game frame family '
                                          'uses it, but it is exactly a spin-out reel')}


def flat(x, bg=(24, 24, 30)):
    o = Image.new('RGB', x.size, bg)
    o.paste(x, (0, 0), x)
    return o


def main():
    pilot = sys.argv[1] if len(sys.argv) > 1 else 'juggernaut'
    if pilot not in MAP:
        print('no mapping authored for %r yet' % pilot)
        return 1
    d = os.path.join(SLICED, pilot)
    aud = json.load(open(os.path.join(d, '_audit.json')))
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
        FS = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 13)
        FB = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 18)
    except Exception:
        F = FS = FB = ImageFont.load_default()

    T, HEAD = 232, 30
    secs = MAP[pilot]
    W = T * 8 + 16
    H = sum(HEAD + T + 44 for _ in secs) + 56
    S = Image.new('RGB', (W, H), (14, 14, 20))
    dr = ImageDraw.Draw(S)
    dr.text((10, 10), '%s  -  %d game frames from the animation pack'
            % (pilot.upper(), sum(len(s[1]) for s in secs)), font=FB, fill=(255, 226, 140))
    y = 46
    for title, rows in secs:
        dr.text((10, y + 6), title, font=F, fill=(120, 200, 255))
        dr.line([(10, y + 26), (W - 10, y + 26)], fill=(48, 52, 70))
        for i, (suf, cell, why) in enumerate(rows):
            im = Image.open(os.path.join(d, cell + '.png')).convert('RGBA')
            sc = min((T - 18) / im.width, (T - 26) / im.height)
            w, h = max(1, int(im.width * sc)), max(1, int(im.height * sc))
            t = flat(im.resize((w, h), Image.NEAREST))
            ox = 8 + i * T + (T - w) // 2
            S.paste(t, (ox, y + HEAD + (T - h) // 2))
            k = '%s,%s' % (cell[1], cell[3])
            a = aud.get(k, {})
            dr.text((8 + i * T + 4, y + HEAD + T + 2), 'ship_%s%s' % (pilot, suf),
                    font=F, fill=(238, 240, 250))
            dr.text((8 + i * T + 4, y + HEAD + T + 20),
                    '%s  %dx%d  %s' % (cell, a.get('w', 0), a.get('h', 0), why),
                    font=FS, fill=(255, 176, 96) if why else (140, 150, 180))
        y += HEAD + T + 44
    if pilot in UNUSED:
        dr.text((10, y - 6), 'NOT USED:  %s  -  %s' % UNUSED[pilot], font=F, fill=(255, 140, 140))
    out = os.path.join(ROOT, 'docs/SHIPANIM_MAP_%s_0907K.png' % pilot.upper())
    S.save(out)
    print('wrote docs/SHIPANIM_MAP_%s_0907K.png' % pilot.upper())
    return 0


if __name__ == '__main__':
    sys.exit(main())
