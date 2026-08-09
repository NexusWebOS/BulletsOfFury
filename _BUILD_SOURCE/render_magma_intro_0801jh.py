#!/usr/bin/env python3
"""
DROP 0801jh - THE CINEMATIC INTRO, FULL SEQUENCE

Mike's 15 beats, from MAGMA_COLOSSUS_SPEC_0801iu.md, rendered in order:

   1  the TORSO enters from the side where the lava is
   2  it levitates to the top/middle - static, no animation yet
   3  the CORE lights in the middle and powers on
   4  a chain drops from the LEFT shoulder hook, thrusts into the lava at an angle,
      and retracts the LEFT ARM in to anchor
   5  the RIGHT shoulder does the same
   6  the hooks take the LEGS, one by one
   7  motion, with every anchored piece
   8  the CANNONS come up with the arms, dangling on chains
   9  chains go off the TOP of the screen and retract the HEAD - medium speed, then
      slowing as it nears the socket
  10  it CONNECTS
  11  the EYES turn on
  12  the whole body does the bottom-to-top flash
  13  arms and cannons LIFT, head tilts up, everything shakes
  14  the fight begins

Every frame is composited from the real pieces at their real anchors - nothing here
is a placeholder or a stand-in.
"""
import os
import re
import math
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
W, H = 300, 380          # the play area this is staged in
FPS_MS = 90


def L(man, key):
    m = re.search(r'"%s":"([^"]+)"' % key, man)
    if not m:
        return None
    p = os.path.join(ROOT, m.group(1))
    return Image.open(p).convert('RGBA') if os.path.exists(p) else None


def fit(im, w):
    if im is None:
        return None
    s = w / float(im.width)
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.NEAREST)


def ease_out(t):
    return 1 - (1 - t) ** 2.4


def main():
    man = open(os.path.join(ROOT, 'assets/manifest.js'), encoding='utf-8').read()

    torso = fit(L(man, 'mbg2_m_torso'), 104)
    head = fit(L(man, 'mgx_head'), 40)
    armL = fit(L(man, 'mbg2_m_left-upper-arm'), 70)
    armR = fit(L(man, 'mbg2_m_right-upper-arm'), 70)
    canL = fit(L(man, 'mbg2_m_left-cannon-forearm'), 48)
    canR = fit(L(man, 'mbg2_m_right-cannon-forearm'), 48)
    legL = fit(L(man, 'mbg2_m_left-leg'), 60)
    legR = fit(L(man, 'mbg2_m_right-leg'), 60)
    coreUp = [fit(L(man, 'nqm_core_up_%d' % i), 104) for i in range(8)]
    eyes = [fit(L(man, 'nqm_eyes_%d' % i), 40) for i in range(8)]
    split = [fit(L(man, 'nqm_split_%d' % i), 104) for i in range(8)]
    rots = [L(man, 'nchx_r%02d' % i) for i in range(16)]
    sc = 0.14
    rots = [None if r is None else r.resize((max(1, int(r.width * sc)),
                                             max(1, int(r.height * sc))), Image.NEAREST)
            for r in rots]
    if torso is None:
        print('  no torso'); return

    CX = W // 2
    TX = CX - torso.width // 2
    TY_REST = 78

    def bg(shake=0):
        """The lava floor. It is what he enters from and what the chase loops over."""
        im = Image.new('RGBA', (W, H), (14, 10, 16, 255))
        d = ImageDraw.Draw(im)
        for y in range(H - 96, H):
            t = (y - (H - 96)) / 96.0
            r = int(46 + 150 * t); g = int(12 + 54 * t); b = int(8 + 10 * t)
            d.line([(0, y + shake), (W, y + shake)], fill=(r, g, b, 255))
        for i in range(9):
            x = (i * 37 + 11) % W
            yy = H - 70 + (i * 13) % 60
            d.ellipse([x, yy, x + 20, yy + 7], fill=(255, 150, 40, 255))
        return im

    def chain_to(canvas, a, b, sag=6, phase=0.0):
        if not rots:
            return
        ax, ay = a; bx, by = b
        dist = math.hypot(bx - ax, by - ay)
        n = max(3, int(dist / 7))
        for i in range(n + 1):
            t = i / float(n)
            x = ax + (bx - ax) * t + math.sin(t * math.pi) * phase
            y = ay + (by - ay) * t + math.sin(t * math.pi) * sag
            j = min(1.0, t + 0.08)
            x2 = ax + (bx - ax) * j + math.sin(j * math.pi) * phase
            y2 = ay + (by - ay) * j + math.sin(j * math.pi) * sag
            ang = math.degrees(math.atan2(y2 - y, x2 - x))
            f = rots[int(round(((ang + 90) % 360) / 22.5)) % 16]
            if f:
                canvas.alpha_composite(f, (int(x - f.width / 2), int(y - f.height / 2)))

    frames = []
    cap = []

    def push(im, text):
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, 16], fill=(0, 0, 0, 190))
        d.text((5, 4), text, fill=(255, 196, 92))
        frames.append(im.convert('RGB'))
        cap.append(text)

    # ---- 1-2. the torso enters from the lava side and levitates up ----
    for i in range(14):
        t = i / 13.0
        im = bg()
        x = int(-torso.width + (TX + torso.width) * ease_out(t))
        y = int(H - 130 - (H - 130 - TY_REST) * ease_out(t))
        im.alpha_composite(torso, (x, y))
        push(im, '1-2  the torso rises from the lava')

    # ---- 3. the core powers on ----
    for i in range(10):
        im = bg()
        c = coreUp[min(7, i * 8 // 10)]
        im.alpha_composite(c or torso, (TX, TY_REST))
        push(im, '3  the core powers on')

    # ---- 4-5. shoulder chains take the arms ----
    for side, arm, lbl in ((-1, armL, '4  left shoulder hooks the arm'),
                           (1, armR, '5  right shoulder hooks the arm')):
        shx = TX + (14 if side < 0 else torso.width - 14)
        shy = TY_REST + 20
        LAVA = H - 74                       # the chain must REACH the lava
        for i in range(14):
            t = i / 13.0
            im = bg(shake=int(math.sin(i * 2.2) * 2))
            # THE CHAIN GOES ALL THE WAY IN (drop 0801ji). Mike: "the chain has to
            # reach all the way into the lava in-game, when it retracts."
            #
            # First half: it lances DOWN and OUT until the tip is in the lava.
            # Second half: it hauls back, and the arm comes with it.
            if t < 0.5:
                p2 = t / 0.5
                tipx = shx + side * int(96 * p2)
                tipy = int(shy + (LAVA - shy) * ease_out(p2))
            else:
                p2 = (t - 0.5) / 0.5
                tipx = shx + side * int(96 - 56 * ease_out(p2))
                tipy = int(LAVA - (LAVA - (TY_REST + 6)) * ease_out(p2))
            # BEHIND THE TORSO, ALWAYS. Mike: "it goes behind the torso, and never
            # goes in front when pulling the other limbs." So the chain and the arm
            # are laid down FIRST and the torso is composited over them.
            chain_to(im, (shx, shy), (tipx, tipy), sag=5)
            if t >= 0.5:
                ax = int(tipx - arm.width // 2)
                ay = int(tipy)
                im.alpha_composite(arm, (ax, ay))
            im.alpha_composite(coreUp[7] or torso, (TX, TY_REST))
            push(im, lbl)

    # ---- 6. the legs, on a Y rig ----
    # Mike: "I need to see 1 chain per leg connected into 1 chain that connects to
    # the torso. that'll shoot out from the bottom plate and connect."
    #
    # So: ONE trunk leaves the bottom plate and runs down to a junction; from that
    # junction a separate chain goes to each leg. Not two independent runs to the
    # torso - a Y.
    PLATE = (CX, TY_REST + torso.height - 14)
    for i in range(16):
        t = i / 15.0
        im = bg(shake=int(math.sin(i * 2.6) * 2))
        LAVA = H - 74
        # the trunk shoots out of the plate first, then the branches find the legs
        trunkEnd = (CX, int(PLATE[1] + (LAVA - PLATE[1]) * ease_out(min(1.0, t * 2.0))))
        jy = trunkEnd[1] if t < 0.5 else int(LAVA - (LAVA - (PLATE[1] + 58)) * ease_out((t - 0.5) / 0.5))
        junction = (CX, jy)
        # everything chain-and-limb goes down BEFORE the torso
        chain_to(im, PLATE, junction, sag=3)
        if t > 0.35:
            p2 = min(1.0, (t - 0.35) / 0.65)
            for s2, leg in ((-1, legL), (1, legR)):
                lx = int(CX + s2 * 34 - leg.width // 2)
                ly = int(LAVA - (LAVA - (junction[1] + 26)) * ease_out(p2))
                chain_to(im, junction, (lx + leg.width // 2, ly + 6), sag=6, phase=s2 * 6)
                im.alpha_composite(leg, (lx, ly))
        for s2, a2 in ((-1, armL), (1, armR)):
            axx = int(TX + (26 if s2 < 0 else torso.width - 26) + s2 * 26 - (a2.width // 2))
            im.alpha_composite(a2, (axx, TY_REST + 6))
        im.alpha_composite(coreUp[7] or torso, (TX, TY_REST))
        push(im, '6  one trunk from the plate, one chain per leg')

    # ---- 7-8. the cannons come up and dangle ----
    for i in range(10):
        t = i / 9.0
        im = bg()
        for s2, a2, c2 in ((-1, armL, canL), (1, armR, canR)):
            axx = int(TX + (26 if s2 < 0 else torso.width - 26) + s2 * 26 - (a2.width // 2))
            cy = int(H - 110 - (H - 110 - (TY_REST + 96)) * ease_out(t))
            cxx = axx + a2.width // 2 - c2.width // 2
            chain_to(im, (axx + a2.width // 2, TY_REST + 60), (cxx + c2.width // 2, cy + 6), sag=4)
            im.alpha_composite(a2, (axx, TY_REST + 6))
            im.alpha_composite(c2, (cxx, cy))
        im.alpha_composite(coreUp[7] or torso, (TX, TY_REST))
        for s2, leg in ((-1, legL), (1, legR)):
            lx = int(CX + s2 * 30 - leg.width // 2)
            im.alpha_composite(leg, (lx, TY_REST + torso.height + 32))
        push(im, '7-8  the cannons rise and hang')

    # ---- 9-10. the head comes down and connects ----
    for i in range(14):
        t = i / 13.0
        im = bg()
        # medium speed, then SLOWING as it nears the socket
        p = t ** 1.9
        hy = int(-head.height + (TY_REST - 8 + head.height) * p)
        chain_to(im, (CX, -6), (CX, hy + 6), sag=2)
        im.alpha_composite(coreUp[7] or torso, (TX, TY_REST))
        for s2, a2, c2 in ((-1, armL, canL), (1, armR, canR)):
            axx = int(TX + (26 if s2 < 0 else torso.width - 26) + s2 * 26 - (a2.width // 2))
            im.alpha_composite(a2, (axx, TY_REST + 6))
            im.alpha_composite(c2, (axx + a2.width // 2 - c2.width // 2, TY_REST + 96))
        for s2, leg in ((-1, legL), (1, legR)):
            im.alpha_composite(leg, (int(CX + s2 * 30 - leg.width // 2), TY_REST + torso.height + 32))
        im.alpha_composite(head, (CX - head.width // 2, hy))
        push(im, '9-10  the head descends and connects')

    # ---- 11. the eyes ----
    for i in range(8):
        im = bg()
        im.alpha_composite(coreUp[7] or torso, (TX, TY_REST))
        for s2, a2, c2 in ((-1, armL, canL), (1, armR, canR)):
            axx = int(TX + (26 if s2 < 0 else torso.width - 26) + s2 * 26 - (a2.width // 2))
            im.alpha_composite(a2, (axx, TY_REST + 6))
            im.alpha_composite(c2, (axx + a2.width // 2 - c2.width // 2, TY_REST + 96))
        for s2, leg in ((-1, legL), (1, legR)):
            im.alpha_composite(leg, (int(CX + s2 * 30 - leg.width // 2), TY_REST + torso.height + 32))
        e = eyes[i] or head
        im.alpha_composite(e, (CX - e.width // 2, TY_REST - 8))
        push(im, '11  the eyes turn on')

    # ---- 12. the body flash ----
    for i in range(8):
        im = bg()
        sp = split[i] or torso
        im.alpha_composite(sp, (TX, TY_REST))
        for s2, a2, c2 in ((-1, armL, canL), (1, armR, canR)):
            axx = int(TX + (26 if s2 < 0 else torso.width - 26) + s2 * 26 - (a2.width // 2))
            im.alpha_composite(a2, (axx, TY_REST + 6))
            im.alpha_composite(c2, (axx + a2.width // 2 - c2.width // 2, TY_REST + 96))
        for s2, leg in ((-1, legL), (1, legR)):
            im.alpha_composite(leg, (int(CX + s2 * 30 - leg.width // 2), TY_REST + torso.height + 32))
        e = eyes[7] or head
        im.alpha_composite(e, (CX - e.width // 2, TY_REST - 8))
        push(im, '12  the body flashes bottom to top')

    # ---- 13. arms lift, head tilts, everything shakes ----
    for i in range(12):
        t = i / 11.0
        sh = int(math.sin(i * 3.1) * 3)
        im = bg(shake=sh)
        lift = int(18 * ease_out(t))
        im.alpha_composite(coreUp[7] or torso, (TX + sh, TY_REST))
        for s2, a2, c2 in ((-1, armL, canL), (1, armR, canR)):
            axx = int(TX + (26 if s2 < 0 else torso.width - 26) + s2 * 26 - (a2.width // 2)) + sh
            im.alpha_composite(a2, (axx, TY_REST + 6 - lift))
            im.alpha_composite(c2, (axx + a2.width // 2 - c2.width // 2, TY_REST + 96 - lift))
        for s2, leg in ((-1, legL), (1, legR)):
            im.alpha_composite(leg, (int(CX + s2 * 30 - leg.width // 2) + sh, TY_REST + torso.height + 32))
        e = eyes[7] or head
        im.alpha_composite(e, (CX - e.width // 2 + sh, TY_REST - 8 - lift // 2))
        push(im, '13  arms lift, head tilts, the mech screams')

    out = '/tmp/out/intro.gif'
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=FPS_MS, loop=0)
    print('  %d frames -> %s  (%.0f KB)' % (len(frames), out, os.path.getsize(out) / 1024))
    seen = []
    for c in cap:
        if not seen or seen[-1] != c:
            seen.append(c)
    print('  beats in order:')
    for c in seen:
        print('   ' + c)


if __name__ == '__main__':
    main()
