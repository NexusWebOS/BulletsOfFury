#!/usr/bin/env python3
"""build_bank_handoff_0907c.py - the hand-authoring package for the frames SpriteCook cannot make.

    python _BUILD_SOURCE/build_bank_handoff_0907c.py

Mike, 0907: "give me the top down ships that we need that spritecook cant generate and I'll use
gpt to do so" -> "I need yuri's, lizzie's, falva's, cole's too" -> "Ill need juggernauts too."

⚠ WHICH SHIPS NEED THIS IS A MEASUREMENT, AND I GOT IT WRONG TWICE BY GUESSING FROM WIDTHS.
A DERIVED reel is a horizontal squash of the top view, and `abs(cos t)` is symmetric in t, so its
left and right poses are THE SAME PIXELS. Comparing `_l` against `_r` and `pv0` against `pv4` byte
for byte is the only test that separates them:

    DERIVED  juggernaut, decker, axel, falva
    AUTHORED maverick, lizzie, yuri, cole, freezer

Judging by width progression instead called juggernaut "clean, leave alone" (his widths run
203/194/190/181/143/21/143, which is a perfect cosine - because that is exactly what produced
them) and called falva fine for the same reason. Both are symmetric and carry no direction.

⚠ AND THE POSE REFERENCE MUST BE AN AUTHORED REEL. An earlier pass used Juggernaut, which would
have taught the artist the very symmetry this exercise exists to remove. Maverick is authored and
his l/r genuinely differ; his WIDTHS are degenerate (l, pv0 and br1 all 156) so the picture teaches
the pose and the table governs the size.
"""
import os, json, math, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'docs/HANDOFF_BANK_FRAMES')
H = os.path.join(ROOT, '_BUILD_SOURCE/sc_hero_0906x')
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')

NEED = ['decker', 'axel', 'juggernaut', 'yuri', 'lizzie', 'falva', 'cole']
DIAG = {
 'decker': 'DERIVED - new hull (0906x), no authored bank art ever existed; l and r are identical.',
 'axel': 'DERIVED - new hull (0906x), no authored bank art ever existed; l and r are identical.',
 'juggernaut': ['DERIVED - his hull was replaced in 0906m and the reel derived from it, so l and r are',
                'pixel identical. His widths run 203/194/190/181/143/21/143, a perfect cosine, which',
                'is why an earlier pass wrongly called him clean - the widths were never the problem.'],
 'yuri': ['AUTHORED but broken - every bank and roll frame is 145 px, exactly his hull width.',
          'pv1, l, pv0, br1 and br2 do not narrow by a single pixel; he never banks or rolls.'],
 'lizzie': ['AUTHORED but degenerate - pv1, l and pv0 are all 211 px, so the three pivot steps',
            'share one width and the lean never progresses.'],
 'falva': ['DERIVED - l and r are identical. Her widths progress cleanly, which is why an earlier',
           'pass called her fine, and her old turn frames also carried a BAKED ENGINE FLAME that',
           'game.js refuses to use.'],
 'cole': ['AUTHORED but out of order - pv0 (27 deg) is 156 px against pv1 (17 deg) at 153, so the',
          'HARDER bank is WIDER than the gentle one. l and pv0 also share a width.'],
}
FRAMES = [(17, 'pv3', 'gentle bank right - you start to see its right side'),
          (20, 'r', 'bank right - the standard lean'),
          (27, 'pv4', 'hard bank right'),
          (45, 'br7', 'rolling right - wings clearly foreshortened'),
          (90, 'br6', 'KNIFE EDGE - fuselage spine and the razor edge of the wings only'),
          (135, 'br5', 'past vertical - now showing the BELLY, still narrow')]


def flat(x, bg=(20, 20, 26)):
    o = Image.new('RGB', x.size, bg)
    o.paste(x, (0, 0), x)
    return o


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = json.loads(subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "process.stdout.write(JSON.stringify(BOFX.ships));"], capture_output=True, cwd=ROOT).stdout.decode())
    A = Image.open(ATLAS).convert('RGBA')

    def cut(k):
        r = rows[k]
        c = A.crop((r[0], r[1], r[0] + r[2], r[1] + r[3]))
        return c.crop(c.getbbox())

    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 13)
    except Exception:
        F = ImageFont.load_default()

    POSES = [('_pv2', 'LEVEL 0 deg'), ('_pv1', 'bank right 17'), ('_l', 'bank right 20'),
             ('_pv0', 'bank right 27'), ('_br1', 'roll right 45'),
             ('_br2', 'roll right 90 EDGE'), ('_br3', 'roll 135 BELLY')]
    T = 200
    S = Image.new('RGB', (T * len(POSES), T + 66), (16, 16, 22))
    d = ImageDraw.Draw(S)
    d.text((6, 4), 'MAVERICK, AUTHORED - copy the POSE, not the sizes. His nose never leaves vertical;', font=F, fill=(255, 220, 120))
    d.text((6, 20), 'as he rolls you see the SIDE of his fuselage. That is what makes left differ from right,', font=F, fill=(255, 220, 120))
    d.text((6, 36), 'and it is the one thing a squash cannot fake. Target WIDTHS are in the table, not here.', font=F, fill=(255, 220, 120))
    for i, (k, lbl) in enumerate(POSES):
        im = cut('ship_maverick' + k)
        sc = min((T - 14) / im.width, (T - 74) / im.height)
        t = flat(im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.NEAREST))
        S.paste(t, (i * T + (T - t.width) // 2, 54 + (T - 54 - t.height) // 2))
        d.text((i * T + 5, T + 44), lbl, font=F, fill=(238, 238, 248))
    S.save(os.path.join(OUT, 'POSE_REFERENCE_maverick.png'))

    L = []
    def W_(s=''):
        L.append(s)
    W_('BULLETS OF FURY - BANK / ROLL FRAMES NEEDED (hand-authored)')
    W_('=' * 76)
    W_()
    W_('SpriteCook cannot produce these. Tested four ways - plain prompt, emphatic prompt, a')
    W_('picture of the exact pose as reference, and per-frame editing of the hull. Every time it')
    W_('YAWED the sprite in the image plane instead of ROLLING it about the nose-to-tail axis:')
    W_('principal axis came back -49, -64 and -45 degrees where the correct answer is +90 (nose')
    W_('straight up). It also cannot draw a knife-edge - asked for one it returns a narrowed top')
    W_('view with the canopy still visible, 39 px wide where a true edge is 18.')
    W_()
    W_('THE RULES FOR EVERY FRAME')
    W_('-' * 76)
    W_('  * The NOSE STAYS POINTING STRAIGHT UP, dead vertical, in every single frame. The ship')
    W_('    rolls about its own nose-to-tail axis. Do NOT rotate the image.')
    W_('  * As it rolls you should see the SIDE of the fuselage. That is what makes a left bank')
    W_('    differ from a right one, and it is the whole reason these are worth drawing by hand.')
    W_('  * Camera stays directly overhead. Same design, colours, panel detail, light from above.')
    W_('  * Transparent background. 1px black outline. NO glow, aura or bloom.')
    W_('  * NO ENGINE FLAME - the build bakes the flame on, and a drawn one gets doubled.')
    W_('  * Height stays the same in every frame; only the WIDTH narrows as it rolls.')
    W_()
    W_('ONLY ONE SIDE IS NEEDED. Draw the ship banking to ITS RIGHT; the build mirrors each frame')
    W_('for the left-hand pose. These airframes are laterally symmetric, so the mirror is exact.')
    W_()
    W_('SIZE DRIFT IS FINE. If the tool returns a frame a little off the target size, or slightly')
    W_('restyled, the build absorbs it - frames are fitted to the reel height and aligned by')
    W_('silhouette, not by their bounding box. What CANNOT be absorbed is the appearance drifting')
    W_('BETWEEN frames of the same ship, because that makes the aircraft morph mid-lean. Keep one')
    W_('ship consistent across its six frames and any overall size difference gets normalised.')
    W_()
    W_()
    W_('WHY EACH SHIP IS ON THE LIST (measured, not opinion)')
    W_('=' * 76)
    W_('A DERIVED reel is a horizontal squash of the top view, and that squash is symmetric about')
    W_('the roll angle - so its left and right poses are THE SAME PIXELS and it can never show')
    W_('direction. Verified per ship by comparing l against r, and pv0 against pv4, byte for byte.')
    W_()
    for p in NEED:
        v = DIAG[p]
        if isinstance(v, str):
            v = [v]
        W_('  %-11s %s' % (p.upper(), v[0]))
        for extra in v[1:]:
            W_('              %s' % extra)
    W_()
    W_('NOT ON THE LIST - authored, and they do carry direction:')
    W_('  MAVERICK   l, pv0 and br1 are all 156 px - three roll angles sharing one width.')
    W_('  FREEZER    br2 is 85 px against a 197 px hull (0.43) - not a true edge, and br2 and br3')
    W_('             share a width.')
    W_()
    for p in NEED:
        f = os.path.join(OUT, '%s_TOP_reference.png' % p)
        if not os.path.exists(f):
            im = Image.open(os.path.join(H, '%s_hero.png' % p)).convert('RGBA')
            im = im.crop(im.getbbox())
            im.save(f)
        im = Image.open(f)
        bw, bh = im.width, im.height
        bf = os.path.join(H, '%s_belly.png' % p)
        if os.path.exists(bf):
            b = Image.open(bf).convert('RGBA')
            b = b.crop(b.getbbox())
            b.save(os.path.join(OUT, '%s_BELLY_reference.png' % p))
        W_()
        W_('%s   - work from %s_TOP_reference.png  (%dx%d)' % (p.upper(), p, bw, bh))
        W_('-' * 76)
        W_('  %-24s %-12s %s' % ('frame', 'target size', 'what it is'))
        for ang, name, desc in FRAMES:
            w = max(int(round(bw * abs(math.cos(math.radians(ang))))), 16 if ang == 90 else 1)
            W_('  %-24s %-12s %s' % ('%s  (roll %d deg)' % (name, ang), '%dx%d' % (w, bh), desc))
        W_('  the 135 deg frame shows the UNDERSIDE - use %s_BELLY_reference.png as its source.' % p)
    W_()
    W_('NOT NEEDED - the build already has these:')
    W_('  level (0 deg) = the top reference;   180 deg = the belly reference;')
    W_('  every left-hand pose = a mirror of its right-hand twin;')
    W_('  the eight somersault frames = derived from top / nose-on / belly / tail-on views.')
    W_()
    W_('THE TOP AND BELLY PLATES DOUBLE AS SHIP AVATARS. They are clean, flameless,')
    W_('transparent-background renders of each aircraft at full detail, which is exactly what a')
    W_('menu, a stat panel or a pilot card wants. Reuse them there rather than cutting new ones.')
    open(os.path.join(OUT, 'README_WHAT_IS_NEEDED.txt'), 'w', encoding='utf-8').write('\n'.join(L))

    # one sheet of every source plate
    T2 = 210
    S2 = Image.new('RGB', (T2 * len(NEED), 2 * T2 + 30), (16, 16, 22))
    d2 = ImageDraw.Draw(S2)
    d2.text((6, 4), 'SEVEN SHIPS NEEDING BANK ART - top view (what to roll) and belly (source for the 135 deg frame)', font=F, fill=(255, 220, 120))
    for i, p in enumerate(NEED):
        for r, tag in enumerate(('TOP', 'BELLY')):
            f = os.path.join(OUT, '%s_%s_reference.png' % (p, tag))
            if not os.path.exists(f):
                continue
            im = Image.open(f).convert('RGBA')
            im = im.crop(im.getbbox())
            sc = min((T2 - 16) / im.width, (T2 - 40) / im.height)
            t = flat(im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.NEAREST))
            S2.paste(t, (i * T2 + (T2 - t.width) // 2, 24 + r * T2 + (T2 - 24 - t.height) // 2))
            d2.text((i * T2 + 5, 20 + r * T2), '%s %s %dx%d' % (p, tag, im.width, im.height), font=F, fill=(238, 238, 248))
    S2.save(os.path.join(OUT, 'ALL_SOURCES.png'))
    print('package rebuilt for %d ships' % len(NEED))
    for f in sorted(os.listdir(OUT)):
        print('   ', f)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
