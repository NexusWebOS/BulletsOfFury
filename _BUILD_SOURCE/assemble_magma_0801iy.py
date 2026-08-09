#!/usr/bin/env python3
"""
DROP 0801iy - THE COLOSSUS ASSEMBLED, WITH CHAINS

Mike: "from the torso socket, two chains angled should be fused to the sockets of
the legs. the chains from the arm sockets should be fused into his torso, we dont
have side sockets, so you anchor them to his shoulder. show me a full version of
this in game, and make sure each piece is stretched out but scaled properly to make
the boss a full 256x256 figure"

THE PIECES, AT SOURCE SIZE
  torso       275 x 335
  upper arm   186 x 350   (x2)
  cannon      127 x 269   (x2)
  leg         162 x 350   (x2)
  head        104 x 111
  chain link   73 x  17   mbg2_bchaind, tiles to any length

HOW THE LAYOUT WORKS
Everything is placed on a large working canvas at SOURCE resolution first, then the
whole figure is scaled ONCE to 256x256. Scaling each piece independently would let
them disagree - an arm ending up a different scale from the torso it hangs off.

CHAIN RUNS, per Mike
  torso lower socket  ->  each leg socket, ANGLED outward
  each shoulder       ->  the arm socket        (no side sockets exist, so the
                                                 shoulder is the anchor)
  arm socket          ->  cannon socket         (the dangle he asked for earlier)

A chain is drawn by tiling the 73x17 link along the line and rotating each copy to
the run's angle, so a chain of any length and angle is built from the one authored
segment rather than stretched.
"""
import os
import re
import json
import math
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma'
TARGET = 256
PAD = 40


def L(man, key):
    m = re.search(r'"%s":"([^"]+)"' % key, man)
    if not m:
        return None
    p = os.path.join(ROOT, m.group(1))
    return Image.open(p).convert('RGBA') if os.path.exists(p) else None


def chain_run(canvas, chain, a, b, thick=1.0, links=None):
    """Lay individual links along a->b, each rotated to the run's angle.

    This is the SotN whip approach Mike described: one link sprite placed N times
    along a path, each copy at the nearest of 16 authored angles. A chain built this
    way bends and dangles for free - nothing about its shape is baked - which a
    stretched sprite could never do.

    `chain` here is the LIST of 16 rotation frames, not a single image."""
    if not chain:
        return 0
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    dist = math.hypot(dx, dy)
    if dist < 10:
        return 0
    ang = math.degrees(math.atan2(dy, dx))
    idx = int(round(((ang + 90) % 360) / 22.5)) % 16
    frame = chain[idx]
    if frame is None:
        return 0
    # pitch from the link's own long axis, so links interlock rather than gap
    pitch = max(10, int(min(frame.width, frame.height) * 0.34 * thick))
    n = max(2, int(dist / pitch))
    for i in range(n + 1):
        t = i / float(n)
        x = ax + dx * t
        y = ay + dy * t
        canvas.alpha_composite(frame, (int(x - frame.width / 2), int(y - frame.height / 2)))
    return n + 1


def main():
    man = open(os.path.join(ROOT, 'assets/manifest.js'), encoding='utf-8').read()
    torso = L(man, 'mbg2_m_torso')
    head = L(man, 'mgx_head')
    armL = L(man, 'mbg2_m_left-upper-arm')
    armR = L(man, 'mbg2_m_right-upper-arm')
    canL = L(man, 'mbg2_m_left-cannon-forearm')
    canR = L(man, 'mbg2_m_right-cannon-forearm')
    legL = L(man, 'mbg2_m_left-leg')
    legR = L(man, 'mbg2_m_right-leg')
    # THE ROTATING LINK SET (drop 0801jf). One link, 16 angles - see
    # build_chain_link_0801je.py. A run picks the frame nearest its own angle, so a
    # chain can follow any path.
    ROT = [L(man, 'nchx_r%02d' % i) for i in range(16)]
    ROT = [r for r in ROT] if any(ROT) else []
    # the links are drawn at boss scale, so knock them back for the working canvas
    if ROT and ROT[0]:
        sc = 0.34
        ROT = [None if r is None else r.resize((max(1, int(r.width * sc)),
                                                max(1, int(r.height * sc))), Image.NEAREST)
               for r in ROT]
    chainL = chainR = ROT
    link = ROT[0] if ROT else None
    print('  chain: %d rotation frames, link %s'
          % (len(ROT), '%dx%d' % ROT[0].size if ROT and ROT[0] else 'none'))

    if not all([torso, head, armL, armR, legL, legR]) or not ROT:
        print('  missing a piece'); return

    # crop the link to its own art so tiling has no dead space
    b = link.getbbox()
    if b:
        link = link.crop(b)

    # ---- lay out at SOURCE resolution ----
    CW, CH = 1100, 1000
    canvas = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    cx = CW // 2

    # THE ARMS WERE READING AS LEGS (drop 0801iy). First pass hung them level with
    # the torso's full height and dropped the cannons below them, so the silhouette
    # came out with four downward limbs and no clear shoulder line.
    #
    # Fixed by raising the arms to the SHOULDER, overlapping the torso so they read
    # as attached, and pulling the cannons up alongside rather than below - a mech
    # holds its guns out, not underneath.
    TY = 90
    tx = cx - torso.width // 2
    AY = TY + 10                                   # up at the shoulder line
    axL = tx - armL.width + 78                     # overlapping the torso edge
    axR = tx + torso.width - 78
    LY = TY + torso.height - 46
    lxL = cx - legL.width + 14
    lxR = cx - 14
    # THE CANNONS DANGLE FROM THE PLATES (drop 0801ja). Mike: "the cannons are
    # covering the plates, they should be dangling from the plates." So they hang
    # BELOW the shoulder pod, on a chain, rather than sitting across it.
    CY = AY + 252
    cxL = axL - canL.width + 118
    cxR = axR + armR.width - 118

    # CHAINS FIRST so they read as running behind the plate
    n = 0
    torso_low = (cx, TY + torso.height - 40)
    n += chain_run(canvas, ROT, torso_low, (lxL + legL.width // 2, LY + 60))
    n += chain_run(canvas, ROT, torso_low, (lxR + legR.width // 2, LY + 60))
    shoulderL = (tx + 46, TY + 58)
    shoulderR = (tx + torso.width - 46, TY + 58)
    n += chain_run(canvas, ROT, shoulderL, (axL + 70, AY + 80))
    n += chain_run(canvas, ROT, shoulderR, (axR + armR.width - 70, AY + 80))
    # cannon back to the ARM SOCKET, per Mike
    n += chain_run(canvas, ROT, (axL + 92, AY + 150), (cxL + canL.width // 2 + 20, CY + 60))
    n += chain_run(canvas, ROT, (axR + armR.width - 92, AY + 150), (cxR + canR.width // 2 - 20, CY + 60))
    # SHOULDER SOCKET -> the pods sitting on top of each shoulder
    n += chain_run(canvas, ROT, shoulderL, (axL + 108, AY + 34))
    n += chain_run(canvas, ROT, shoulderR, (axR + armR.width - 108, AY + 34))
    print('  %d chain links placed across 6 runs' % n)

    # then the pieces, back to front
    canvas.alpha_composite(legL, (lxL, LY))
    canvas.alpha_composite(legR, (lxR, LY))
    canvas.alpha_composite(armL, (axL, AY))
    canvas.alpha_composite(armR, (axR, AY))
    canvas.alpha_composite(canL, (cxL, CY))
    canvas.alpha_composite(canR, (cxR, CY))
    canvas.alpha_composite(torso, (tx, TY))
    canvas.alpha_composite(head, (cx - head.width // 2, TY - 10))

    # THE BASE PLATE AS A HOVER EMITTER. Selected from the torso's own pixels - the
    # pale metal disc at its waist - and lit with the same banded ramp used
    # everywhere else, so it belongs to the machine rather than sitting on it.
    tarr = np.array(canvas).astype(float)
    top = tarr[..., 3] > 16
    rr, gg, bb2 = tarr[..., 0], tarr[..., 1], tarr[..., 2]
    plateY0, plateY1 = TY + torso.height - 96, TY + torso.height + 10
    band = np.zeros(tarr.shape[:2], dtype=bool)
    band[plateY0:plateY1, :] = True
    # the plate is the light, low-saturation metal in that band
    mx = np.maximum(np.maximum(rr, gg), bb2)
    mn = np.minimum(np.minimum(rr, gg), bb2)
    plate = top & band & (mx > 120) & ((mx - mn) < 70)
    if plate.any():
        for c, tgt in zip(range(3), (255, 196, 96)):
            tarr[..., c] = np.where(plate, np.clip(tarr[..., c] * 0.55 + tgt * 0.45, 0, 255), tarr[..., c])
        # and a short downward wash under it, so it reads as thrust
        yy2, xx2 = np.mgrid[0:tarr.shape[0], 0:tarr.shape[1]]
        px2 = np.where(plate)
        if len(px2[0]):
            pcx = int(px2[1].mean()); pcy = int(px2[0].max())
            d2 = np.hypot((xx2 - pcx) / 1.9, yy2 - pcy)
            wash = (yy2 > pcy) & (d2 < 92) & top
            amt = np.clip(1.0 - d2 / 92.0, 0, 1) * wash * 0.42
            for c, tgt in zip(range(3), (255, 176, 84)):
                tarr[..., c] = np.clip(tarr[..., c] * (1 - amt) + tgt * amt, 0, 255)
        canvas = Image.fromarray(np.clip(tarr, 0, 255).astype(np.uint8), 'RGBA')
        print('  base plate lit as a hover emitter: %d px' % int(plate.sum()))


    # ---- THE SHADOW, and the BASE PLATE as a hover pad ----
    # Mike: "create a shadow under his feet. Im not sure what to do with the middle
    # base plate, but if you have ideas."
    #
    # THE BASE PLATE IDEA: he LEVITATES. The whole intro has him floating in on
    # chains and hovering through the fight, so that oval plate at his waist reads
    # naturally as the hover emitter - the thing holding him up. Lighting it and
    # casting the shadow FROM it, rather than from the feet, sells the levitation:
    # the shadow sits below a machine that is not touching the ground.
    shadow = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    footY = LY + legL.height - 26
    sw, shh = int(legL.width * 2.35), int(legL.height * 0.20)
    # three stacked ellipses, hard-edged - a 16-bit shadow is banded, not blurred
    for k, (grow, alpha) in enumerate([(1.00, 66), (0.74, 96), (0.48, 128)]):
        w2, h2 = int(sw * grow), int(shh * grow)
        sd.ellipse([cx - w2 // 2, footY - h2 // 2, cx + w2 // 2, footY + h2 // 2],
                   fill=(8, 6, 14, alpha))
    print('  shadow: 3 banded ellipses at y=%d, %dx%d' % (footY, sw, shh))
    canvas = Image.alpha_composite(shadow, canvas)

    # ---- ONE scale to 256, applied to the whole figure ----
    bb = canvas.getbbox()
    fig = canvas.crop(bb)
    s = min(TARGET / float(fig.width), TARGET / float(fig.height))
    scaled = fig.resize((max(1, int(fig.width * s)), max(1, int(fig.height * s))), Image.LANCZOS)
    out = Image.new('RGBA', (TARGET, TARGET), (0, 0, 0, 0))
    out.alpha_composite(scaled, ((TARGET - scaled.width) // 2, (TARGET - scaled.height) // 2))

    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    rel = '%s/mgx_assembled.png' % OUT
    out.save(os.path.join(ROOT, rel))

    man_path = os.path.join(ROOT, 'assets/manifest.js')
    if '"mgx_assembled"' not in man:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(
            man[:i] + '"mgx_assembled":"%s",' % rel + man[i:])

    # anchors, in FIGURE space, so the game can place the real pieces itself
    anchors = {'scale': round(s, 4), 'figure_source': [fig.width, fig.height],
               'target': TARGET,
               'pieces': {'torso': [tx - bb[0], TY - bb[1]],
                          'head': [cx - head.width // 2 - bb[0], TY - 10 - bb[1]],
                          'arm_l': [axL - bb[0], AY - bb[1]],
                          'arm_r': [axR - bb[0], AY - bb[1]],
                          'cannon_l': [cxL - bb[0], CY - bb[1]],
                          'cannon_r': [cxR - bb[0], CY - bb[1]],
                          'leg_l': [lxL - bb[0], LY - bb[1]],
                          'leg_r': [lxR - bb[0], LY - bb[1]]}}
    json.dump(anchors, open(os.path.join(ROOT, '%s/assembled_anchors.json' % OUT), 'w'), indent=1)

    print('  figure %dx%d at source  ->  scale %.3f  ->  %dx%d in a %d box'
          % (fig.width, fig.height, s, scaled.width, scaled.height, TARGET))
    print('  every piece scaled by the SAME factor, so nothing disagrees')


if __name__ == '__main__':
    main()
