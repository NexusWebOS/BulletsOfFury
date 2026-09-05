#!/usr/bin/env python3
"""sheet_s9_rosters_0905.py - put the three stage-9 casts side by side so Mike can SEE what the
prototype-roster decision is actually about.

He asked "show me the art we have first". Three panels, all from the plates on disk, no mock-ups:

  A  THE PROTOTYPE ROSTER   - S9_UNITS. Ten units, real art, real behaviours, currently shut out
                              of the waves by an explicit assertion in test_fl.js.
  B  THE CAST IN STAGE 9 NOW - S9VOID. The eight sanctioned hulls the ramp is built from.
  C  ALREADY CUT BY MIKE     - the four whose art is still on disk but which he rejected by name.

⚠ THE PROTOTYPE PLATES ARE ATLAS CELLS, NOT LOOSE FILES. BOFX.cells['ns9e_wskim_idle'] is
['en_s9',1490,2120,128,128] - a crop out of assets/game/atlas/en_s9.png. Reading the manifest's
BOFX.img entry instead gives the path of the WHOLE 4096px sheet, and pasting that would put the
entire atlas in every slot. The rects come from a node dump of BOFX.cells.

⚠ NEAREST on every resize. These are pixel plates; a smooth filter would show Mike a softened
version of art he has not approved in that form.
"""
import json, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELLS = json.load(open('/tmp/ns9e_cells.json'))
ATLAS = Image.open(os.path.join(ROOT, 'assets/game/atlas/en_s9.png')).convert('RGBA')

# name, hp, behaviour, shield  - straight from S9_UNITS in game.js
PROTO = [
    ('wskim',   24, 'weaver, barrel roll',   None,    'cell'),
    ('pneedle', 20, 'phase needle',          None,    'cell'),
    ('pmine',   36, 'parks, 6-spoke wheel',  'prism', 'cell'),
    ('gleech',  30, 'rides to the walls',    None,    'cell'),
    ('vmanta',  38, 'wide pivot, 5-shot',    'hex',   'cell'),
    ('echof',   28, 'afterimages shoot too', None,    'cell'),
    ('tsplit',  42, 'halves into 2 needles', 'ion',   'cell'),
    ('cbreak',  52, 'narrow weave, tanky',   None,    'cell'),
    ('horizon', 88, 'apex drone, 5-wide',    'violet',
     'assets/game/stage9_void_rift/enemies/event_horizon_0.png'),
    ('dreadv', 130, 'apex, 7-wide @0.78s',   'prism',
     'assets/game/stage9_void_rift/enemies/dreadnought_vanguard.png'),
]

LIVE = [
    ('s9comet',       28, 'comet_skimmer'),
    ('s9interceptor', 30, 'galaxy_interceptor'),
    ('s9ring',        32, 'ring_drone'),
    ('s9beacon',      34, 'alien_beacon'),
    ('s9gateturret',  42, 'gate_turret'),
    ('s9singularity', 46, 'singularity_mine'),
    ('s9gunship',     62, 'dimensional_gunship'),
    ('s9prism',       66, 'hyperspace_prism'),
]

CUT = [
    ('chronal_crawler_tank', '0904e  "its a 45 degree titled tank"'),
    ('gravity_artillery',    '0904i  "delete these 2 enemies. no good."'),
    ('gate_carrier',         '0904r  turned hull, axis 145.7 deg'),
    ('mini_warp_tank',       '0904r  a tracked tank, in deep space'),
]

BG, INK, DIM, HOT = (14, 16, 26), (222, 236, 255), (128, 146, 176), (255, 190, 74)
BOX, PAD, COLS = 118, 16, 5
L2MAX = 30           # a 200px column holds ~30 chars at 11px consolas; longer labels collided


def font(sz, bold=False):
    for p in ('C:/Windows/Fonts/consolab.ttf' if bold else 'C:/Windows/Fonts/consola.ttf',
              'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf'):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


F_H, F_N, F_S = font(17, True), font(13, True), font(11)


def plate(spec):
    """spec is 'cell' (crop it out of en_s9 by its manifest rect) or a repo-relative png path."""
    if spec != 'cell':
        return Image.open(os.path.join(ROOT, spec)).convert('RGBA')
    return None


def fit(im, box=BOX):
    """scale to fit the box on the LONG side, integer-ish, NEAREST, keeping the aspect."""
    b = im.getbbox()
    if b:
        im = im.crop(b)
    s = min(box / max(1, im.width), box / max(1, im.height))
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.NEAREST)


def cell_for(unit):
    k = 'ns9e_%s_idle' % unit
    if k not in CELLS:
        k = 'ns9e_%s_0' % unit
    _atlas, x, y, w, h = CELLS[k]
    return ATLAS.crop((x, y, x + w, y + h))


def panel(draw, img, title, sub, items, y, kind):
    draw.text((PAD, y), title, font=F_H, fill=HOT)
    y += 22
    draw.text((PAD, y), sub, font=F_S, fill=DIM)
    y += 18
    rows = (len(items) + COLS - 1) // COLS
    cw = (img.width - PAD * 2) // COLS
    for i, it in enumerate(items):
        cx = PAD + (i % COLS) * cw
        cy = y + (i // COLS) * (BOX + 46)
        if kind == 'proto':
            name, hp, beh, sh, spec = it
            im = cell_for(name) if spec == 'cell' else plate(spec)
            l1 = '%s  hp %d' % (name, hp)
            l2 = beh + ('  [%s shld]' % sh if sh else '')
        elif kind == 'live':
            name, hp, art = it
            im = Image.open(os.path.join(ROOT, 'assets/game/stage9_enemy_attacks/%s/01.png' % art)).convert('RGBA')
            l1 = '%s  hp %d' % (name, hp)
            l2 = art
        else:
            art, why = it
            im = Image.open(os.path.join(ROOT, 'assets/game/stage9_enemy_attacks/%s/01.png' % art)).convert('RGBA')
            l1 = art
            l2 = why
        im = fit(im)
        img.paste(im, (cx + (cw - im.width) // 2, cy + (BOX - im.height) // 2), im)
        draw.text((cx + 2, cy + BOX + 4), l1, font=F_N, fill=INK if kind != 'cut' else DIM)
        draw.text((cx + 2, cy + BOX + 20), l2[:L2MAX], font=F_S, fill=DIM)
    return y + rows * (BOX + 46) + 14


def main():
    W = PAD * 2 + COLS * 200
    H = 1180
    img = Image.new('RGBA', (W, H), BG + (255,))
    d = ImageDraw.Draw(img)
    d.text((PAD, 14), 'STAGE 9 - THE THREE CASTS, AS THE ART ACTUALLY SITS ON DISK', font=font(20, True), fill=INK)
    y = 46
    y = panel(d, img, 'A.  THE PROTOTYPE ROSTER  (S9_UNITS - built, arted, and shut out)',
              'ten units. test_fl.js asserts by name that these stay OUT of the stage-9 waves. '
              'this is the decision.', PROTO, y, 'proto')
    d.line([(PAD, y), (W - PAD, y)], fill=(40, 46, 66), width=1)
    y += 14
    y = panel(d, img, 'B.  THE CAST IN STAGE 9 TODAY  (S9VOID - what the new ramp is built from)',
              'eight hulls, hp 28 to 66. every one of them appears in the rebuilt plan.',
              LIVE, y, 'live')
    d.line([(PAD, y), (W - PAD, y)], fill=(40, 46, 66), width=1)
    y += 14
    y = panel(d, img, 'C.  ALREADY CUT BY YOU  (art still on disk, deliberately not in the game)',
              'for contrast - this is what a rejected stage-9 hull looks like.', CUT, y, 'cut')
    out = os.path.join(ROOT, 'docs/S9_ROSTERS_0905.png')
    img.crop((0, 0, W, min(H, y + 10))).save(out)
    print('wrote %s  (%dx%d)' % (out, W, min(H, y + 10)))


if __name__ == '__main__':
    main()
