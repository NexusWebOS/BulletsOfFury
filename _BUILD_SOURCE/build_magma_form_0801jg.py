#!/usr/bin/env python3
"""
DROP 0801jg - THE FULL FORM, LEGS DANGLING AND SWAYING

Mike: "his full form should have the legs dangling to where they each can sway, and
you attach the chains from the torso socket to each leg, and allow the chains to
flex and sway ... when he forms, the stage is going to merge a section to it that
infinitely loops ... he will fly backwards as we chase him on a highspeed chase ...
so drop them legs down, the chain should be attached an anchored to the plates, make
them appeared to be 'mounted in' so it doesnt look janky either."

WHY THIS SHAPE
He flies BACKWARDS over looping lava while the player chases. Legs bolted rigidly to
a hovering torso would read as a statue being dragged; legs hanging on chains and
swinging read as a machine under power at speed. So they drop clear of the body and
each one swings on its own phase.

THE CHAIN IS A CATENARY, NOT A LINE
A chain between two points hangs - it does not run straight. Each run is sampled
along a curve that sags under its own weight and swings with the leg, and every link
is placed at the local tangent using the 16 rotation frames. That is what stops it
reading as a stiff rod.

MOUNTED, NOT FLOATING
Mike: "make them appeared to be 'mounted in' so it doesnt look janky." At both ends
of every run an anchor clamp is drawn OVER the last link, so the chain visibly
terminates in hardware rather than stopping in mid-air.

  nqm_form_0..11   twelve frames of the full form, legs swaying
"""
import os
import re
import math
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma'
FRAMES = 12
TARGET = 256


def L(man, key):
    m = re.search(r'"%s":"([^"]+)"' % key, man)
    if not m:
        return None
    p = os.path.join(ROOT, m.group(1))
    return Image.open(p).convert('RGBA') if os.path.exists(p) else None


def hang(canvas, rots, a, b, sag, phase, clamp=None):
    """Lay links along a sagging, swinging curve from a to b."""
    if not rots:
        return
    ax, ay = a
    bx, by = b
    dist = math.hypot(bx - ax, by - ay)
    n = max(4, int(dist / max(8, rots[0].width * 0.30)))
    pts = []
    for i in range(n + 1):
        t = i / float(n)
        x = ax + (bx - ax) * t
        y = ay + (by - ay) * t
        # sag peaks mid-run; sway leans the whole curve and grows toward the free end
        y += math.sin(t * math.pi) * sag
        x += math.sin(t * math.pi) * phase * 0.55 + t * phase * 0.45
        pts.append((x, y))
    for i, (x, y) in enumerate(pts):
        j = min(len(pts) - 1, i + 1)
        ang = math.degrees(math.atan2(pts[j][1] - y, pts[j][0] - x)) if j != i else 90
        idx = int(round(((ang + 90) % 360) / 22.5)) % 16
        f = rots[idx]
        if f:
            canvas.alpha_composite(f, (int(x - f.width / 2), int(y - f.height / 2)))
    # MOUNTED: hardware over both ends so the run terminates in something
    if clamp:
        for (x, y) in (pts[0], pts[-1]):
            canvas.alpha_composite(clamp, (int(x - clamp.width / 2), int(y - clamp.height / 2)))


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    torso = L(man, 'mbg2_m_torso'); head = L(man, 'mgx_head')
    armL = L(man, 'mbg2_m_left-upper-arm'); armR = L(man, 'mbg2_m_right-upper-arm')
    canL = L(man, 'mbg2_m_left-cannon-forearm'); canR = L(man, 'mbg2_m_right-cannon-forearm')
    legL = L(man, 'mbg2_m_left-leg'); legR = L(man, 'mbg2_m_right-leg')
    if not all([torso, head, armL, armR, legL, legR]):
        print('  missing a piece'); return

    rots = [L(man, 'nchx_r%02d' % i) for i in range(16)]
    sc = 0.30
    rots = [None if r is None else r.resize((max(1, int(r.width * sc)), max(1, int(r.height * sc))),
                                            Image.NEAREST) for r in rots]
    clamp = L(man, 'nch_clamp_0')
    if clamp:
        clamp = clamp.resize((max(8, int(clamp.width * 0.22)), max(8, int(clamp.height * 0.22))),
                             Image.NEAREST)

    CW, CH = 1100, 1250
    add = {}
    for f in range(FRAMES):
        ph = f / float(FRAMES) * 2 * math.pi
        canvas = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
        cx = CW // 2
        TY = 90
        tx = cx - torso.width // 2
        AY = TY + 10
        axL = tx - armL.width + 78
        axR = tx + torso.width - 78
        CY = AY + 252
        cxL = axL - canL.width + 118
        cxR = axR + armR.width - 118

        # THE LEGS DROP CLEAR AND SWING, each on its own phase so they do not move
        # as a pair - a machine at speed does not swing symmetrically
        DROP = 210
        swayL = math.sin(ph) * 34
        swayR = math.sin(ph + 2.1) * 34
        LY = TY + torso.height + DROP
        lxL = cx - legL.width - 4 + int(swayL)
        lxR = cx + 4 + int(swayR)

        # sockets on the torso's lower plate
        sockL = (cx - 52, TY + torso.height - 30)
        sockR = (cx + 52, TY + torso.height - 30)

        hang(canvas, rots, sockL, (lxL + legL.width // 2, LY + 30), 26, swayL, clamp)
        hang(canvas, rots, sockR, (lxR + legR.width // 2, LY + 30), 26, swayR, clamp)
        # arm and cannon runs keep their short hangs
        hang(canvas, rots, (tx + 46, TY + 58), (axL + 92, AY + 80), 8, swayL * 0.3, clamp)
        hang(canvas, rots, (tx + torso.width - 46, TY + 58), (axR + armR.width - 92, AY + 80),
             8, swayR * 0.3, clamp)

        canvas.alpha_composite(legL, (lxL, LY))
        canvas.alpha_composite(legR, (lxR, LY))
        canvas.alpha_composite(armL, (axL, AY))
        canvas.alpha_composite(armR, (axR, AY))
        canvas.alpha_composite(canL, (cxL, CY))
        canvas.alpha_composite(canR, (cxR, CY))
        canvas.alpha_composite(torso, (tx, TY))
        canvas.alpha_composite(head, (cx - head.width // 2, TY - 10))

        bb = canvas.getbbox()
        fig = canvas.crop(bb)
        s = min(TARGET / float(fig.width), TARGET / float(fig.height))
        sc2 = fig.resize((max(1, int(fig.width * s)), max(1, int(fig.height * s))), Image.LANCZOS)
        out = Image.new('RGBA', (TARGET, TARGET), (0, 0, 0, 0))
        out.alpha_composite(sc2, ((TARGET - sc2.width) // 2, (TARGET - sc2.height) // 2))

        os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
        k = 'nqm_form_%d' % f
        rel = '%s/%s.png' % (OUT, k)
        out.save(os.path.join(ROOT, rel))
        add[k] = rel
        if f == 0:
            print('  figure %dx%d -> scale %.3f -> %dx%d' % (fig.width, fig.height, s, sc2.width, sc2.height))

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])
    print('  %d frames, legs swinging on separate phases, chains sagging with them' % FRAMES)


if __name__ == '__main__':
    main()
