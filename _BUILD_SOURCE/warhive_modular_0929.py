#!/usr/bin/env python3
"""warhive_modular_0929.py - the Stage-6 carrier and ace as MODULES (Mike, 0929).

"stage 6 boss should be modular, the fans especially so they spin and we have something that makes sense
why beams are coming from there ... THe enemy boss jet ... should be a modular larger blue jet of its own."

Everything here is DERIVED from authored plates - nothing is painted or procedural:
  carrier_<state>_wells.png  the three carrier plates with both fan wells cut OPEN (r 27.5 plate px, measured:
                             blades run to r 27, the bright rim lip r 28-36), so a real fan spins UNDER the rim
  carrier_well.png           the well floor behind the fan: the plate's own well, at 32% value
  carrier_cannon.png         the Furnace Tyrant's authored coil cannon (fzt_arm_cannon_intact), its bronze
                             recoloured to the carrier's own gunmetal and its orange coils to the beam's cyan -
                             the module that deploys under each nacelle and that the beam comes out of
  ace_mod_<body|wingL|wingR>[_dmg].png   the Nightwing Ace cut at its wing roots (x 63 / 137 of 200) so the
                             wings can foreshorten independently in a bank; drawn together unmodified they
                             reproduce the plate exactly (asserted)
Run from the repo root. Writes into assets/game/bosses/skycarrier/.
"""
import os, math, colorsys
from PIL import Image

D = os.path.join('assets', 'game', 'bosses', 'skycarrier')
HUBS = [(256 - 169.5, 134.0), (256 + 169.5, 134.0)]
WELL_R = 27.5

def cut_wells(src, dst):
    im = Image.open(os.path.join(D, src)).convert('RGBA'); px = im.load()
    n = 0
    for (cx, cy) in HUBS:
        for y in range(int(cy - WELL_R - 2), int(cy + WELL_R + 3)):
            for x in range(int(cx - WELL_R - 2), int(cx + WELL_R + 3)):
                d = math.hypot(x + .5 - cx, y + .5 - cy)
                if d <= WELL_R:
                    r, g, b, a = px[x, y]
                    if a: px[x, y] = (r, g, b, 0); n += 1
    im.save(os.path.join(D, dst)); return n

def well_floor():
    im = Image.open(os.path.join(D, 'carrier_closed.png')).convert('RGBA')
    cx, cy = HUBS[0]; R = int(WELL_R + 3)
    c = im.crop((int(cx - R), int(cy - R), int(cx + R), int(cy + R))); px = c.load()
    for y in range(c.height):
        for x in range(c.width):
            r, g, b, a = px[x, y]
            d = math.hypot(x + .5 - R, y + .5 - R)
            px[x, y] = (int(r * .32), int(g * .32), int(b * .36), a if d <= WELL_R + 1 else 0)
    c.save(os.path.join(D, 'carrier_well.png')); return c.size

def carrier_gunmetal():
    """the carrier plate's own metal: mean hue/sat of its mid-value opaque pixels"""
    im = Image.open(os.path.join(D, 'carrier_closed.png')).convert('RGBA')
    hs = []
    for r, g, b, a in im.getdata():
        if a < 250: continue
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if .2 < v < .8: hs.append((h, s))
    return sum(h for h, _ in hs) / len(hs), sum(s for _, s in hs) / len(hs)

def cannon():
    src = os.path.join('assets', 'game', 'bosses', 'furnace', 'fzt_arm_cannon_intact.png')
    im = Image.open(src).convert('RGBA'); px = im.load()
    gh, gs = carrier_gunmetal()
    before = len({p for p in im.getdata() if p[3] > 0})
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a: continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s > .45 and v > .45 and (h < .14 or h > .95):      # the glowing coil: orange -> the beam's cyan
                h2, s2, v2 = .53, min(1, s * .95), v
            else:                                                    # bronze metal -> the carrier's gunmetal, value kept
                h2, s2, v2 = gh, min(s * .55, gs * 1.4), v * .96
            rr, gg, bb = colorsys.hsv_to_rgb(h2, s2, v2)
            px[x, y] = (int(rr * 255), int(gg * 255), int(bb * 255), a)
    after = len({p for p in im.getdata() if p[3] > 0})
    im.save(os.path.join(D, 'carrier_cannon.png')); return im.size, before, after

def ace_modules():
    out = {}
    for src, suf in (('ace_top.png', ''), ('ace_damaged.png', '_dmg')):
        im = Image.open(os.path.join(D, src)).convert('RGBA'); w, h = im.size
        parts = {'wingL': (0, 63), 'body': (63, 137), 'wingR': (137, w)}
        for k, (x0, x1) in parts.items():
            c = Image.new('RGBA', im.size, (0, 0, 0, 0)); c.paste(im.crop((x0, 0, x1, h)), (x0, 0))
            c.save(os.path.join(D, 'ace_mod_%s%s.png' % (k, suf)))
        # reassemble and require an exact match
        re = Image.new('RGBA', im.size, (0, 0, 0, 0))
        for k in parts: p = Image.open(os.path.join(D, 'ace_mod_%s%s.png' % (k, suf))); re.alpha_composite(p)
        assert list(re.getdata()) == list(im.getdata()), 'ace modules do not reassemble ' + src
        out[src] = 'exact'
    return out

if __name__ == '__main__':
    for s in ('closed', 'open', 'broken'):
        print('wells', s, cut_wells('carrier_%s.png' % s, 'carrier_%s_wells.png' % s), 'px cut')
    print('well floor', well_floor())
    print('cannon', cannon())
    print('ace', ace_modules())
