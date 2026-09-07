#!/usr/bin/env python3
"""bake_thruster_glow_0906s.py - the baked flames flicker, by animating the glow INSIDE them.

    python _BUILD_SOURCE/bake_thruster_glow_0906s.py            # measure + proof only
    python _BUILD_SOURCE/bake_thruster_glow_0906s.py --write

Mike, 0906: "now you may make them animate via pixel glow inside and viola."

⚠ THE SILHOUETTE MUST NOT MOVE, AND THAT IS THE WHOLE DESIGN. 0906q/r spent two rounds getting
each plume sized to its bell and centred on it; an animation that redraws the flame shape would
put that back at risk every frame, and a plume whose OUTLINE jitters reads as a sprite glitch
rather than as combustion. So every phase here shares one silhouette and differs only in the
brightness of the pixels inside it — which is exactly what a real exhaust does.

⚠ THE FLAME PIXELS ARE RECOVERED BY DIFFING, NOT BY RE-DETECTING THEM. The 0906q backup is the
plate as it stood BEFORE the bake, so `current cell XOR pre-bake cell` is precisely the flame and
its glow, per frame, for all nine pilots — including Juggernaut, whose flame is painted into his
plate and could not be found any other way now that it is restored. Re-running a hot-pixel finder
over the baked plate would have re-made the 0906q mistake of catching the core and missing the
cone. **Both plates are composited into their own canvas first**, because the two manifests give
these frames different trim rects — diffing the raw atlas rectangles would compare a frame with
its own neighbour.

⚠ ONLY THE EIGHT STEADY FRAMES PER PILOT GET PHASES. base/l/r/pv0..pv4 is what is on screen while
the player flies; br0..br7 is a barrel roll and so0..so7 a spin-out, both of which are over in a
few frames and neither of which can show a flicker. Phasing all 185 would have cost 320 extra
cells for animation nobody can see; this costs 144.
"""
import os, re, sys, json, shutil, subprocess, colorsys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
# ⚠ THE PRE-BAKE REFERENCE MUST MATCH THE HULLS THE BAKE USED, HALO CONVERSION INCLUDED. Diffing
# against the 0906q plate after 0906t blacked 42,688 halo pixels would report every one of them as
# "added by the bake" and hand them to the glow modulation - a pulsing violet rim around the whole
# airframe. 0906t2 is the plate as it stood immediately before the flames went on.
PREBAKE = ATLAS + '.0906t2.bak'
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')
PREMAN = MANIFEST + '.0906t2.bak'

PILOTS = ['axel', 'cole', 'decker', 'falva', 'freezer', 'juggernaut', 'lizzie', 'maverick', 'yuri']
STEADY = {'', 'l', 'r', 'pv0', 'pv1', 'pv2', 'pv3', 'pv4'}

# ⚠ CHOSEN SO THE MID PHASE IS THE ONE ALREADY APPROVED. Phase 0 is the plate Mike signed off in
# 0906r and is left byte-identical; g1 flares and g2 settles, so the reel reads 0 -> 1 -> 0 -> 2.
PHASE = {
    'g1': dict(core=1.32, body=1.17, glow=1.55),
    'g2': dict(core=0.76, body=0.87, glow=0.60),
}


def rows_from(path):
    js = os.path.join(ROOT, '_BUILD_SOURCE/_g.js')
    open(js, 'w', encoding='utf-8').write(
        "global.window=global;eval(require('fs').readFileSync(%s,'utf8'));\n"
        "const P=%s;const o={};for(const k in BOFX.ships){for(const p of P){"
        "if(k==='ship_'+p||k.indexOf('ship_'+p+'_')===0){o[k]=BOFX.ships[k];break;}}}\n"
        "process.stdout.write(JSON.stringify(o));\n"
        % (json.dumps(os.path.relpath(path, ROOT).replace('\\', '/')), json.dumps(PILOTS)))
    out = subprocess.run(['node', js], capture_output=True, cwd=ROOT)
    return json.loads(out.stdout.decode())


def split_key(key):
    rest = key[len('ship_'):]
    for p in PILOTS:
        if rest == p:
            return p, ''
        if rest.startswith(p + '_'):
            return p, rest[len(p) + 1:]
    return None, None


def canvas_of(atlas, r):
    x, y, w, h, ox, oy, cw, ch = r
    c = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    c.alpha_composite(atlas.crop((x, y, x + w, y + h)), (ox, oy))
    return c


def phased(new_c, old_c, spec):
    """brighten/dim the pixels the bake ADDED, IN PROPORTION TO HOW MUCH IT CHANGED THEM.

    ⚠ A BARE "DID THIS PIXEL CHANGE" MASK PULSES THE WHOLE AIRFRAME. On the five overlay pilots
    the flame's soft glow is composited OVER the hull, so a large halo of hull pixels differ from
    the pre-bake plate by a few levels each - and modulating all of them equally made the entire
    ship brighten and dim, which the first proof shows plainly on Cole, Yuri and Lizzie while
    Juggernaut (not overlaid) was correct. Weighting by the size of the change confines the
    animation to the flame: its core moved 100+ levels and takes the full effect, the haze over
    the hull moved 2-5 and takes almost none."""
    out = new_c.copy()
    pn, po, pp = new_c.load(), old_c.load(), out.load()
    W, H = new_c.size
    n = 0
    for y in range(H):
        for x in range(W):
            a, b = pn[x, y], po[x, y]
            if a == b or a[3] == 0:
                continue
            d = max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]),
                    abs(a[3] - b[3])) if b[3] else a[3]
            w = min(1.0, d / 110.0)
            if w < 0.04:
                continue
            n += 1
            h, s, v = colorsys.rgb_to_hsv(a[0] / 255., a[1] / 255., a[2] / 255.)
            f = spec['core'] if (s < 0.25 and v > 0.72) else spec['body']
            f = 1.0 + (f - 1.0) * w
            g = 1.0 + (spec['glow'] - 1.0) * w
            rr, gg, bb = colorsys.hsv_to_rgb(h, s, max(0.0, min(1.0, v * f)))
            na = a[3] if a[3] > 200 else max(0, min(255, int(a[3] * g)))
            pp[x, y] = (int(rr * 255 + .5), int(gg * 255 + .5), int(bb * 255 + .5), na)
    return out, n


def main():
    write = '--write' in sys.argv
    if not os.path.exists(PREBAKE) or not os.path.exists(PREMAN):
        raise SystemExit('the 0906q backups are missing - cannot recover the flame by diffing')
    R, R0 = rows_from(MANIFEST), rows_from(PREMAN)
    A, A0 = Image.open(ATLAS).convert('RGBA'), Image.open(PREBAKE).convert('RGBA')

    todo = []
    for k in sorted(R):
        p, suf = split_key(k)
        if p and suf in STEADY:
            todo.append(k)
    print('%d steady frames of %d total will be phased (%d new cells)'
          % (len(todo), len(R), len(todo) * len(PHASE)))

    made, flame_px = {}, 0
    for k in todo:
        new_c = canvas_of(A, R[k])
        old_c = canvas_of(A0, R0[k])
        for tag, spec in PHASE.items():
            im, n = phased(new_c, old_c, spec)
            bb = im.getbbox()
            if not bb:
                continue
            made[k + '_' + tag] = (im.crop(bb), bb[0], bb[1], R[k][6], R[k][7])
            if tag == 'g1':
                flame_px += n
    print('built %d phase cells; the flame masks total %d px (avg %d per frame)'
          % (len(made), flame_px, flame_px // max(1, len(todo))))

    # ---- proof: one pilot's three phases side by side at the size the game draws
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 14)
    except Exception:
        F = ImageFont.load_default()
    show = ['cole', 'yuri', 'juggernaut', 'lizzie']
    T = 200
    proof = Image.new('RGB', (T * 3 * len(show), T + 24), (18, 18, 24))
    d = ImageDraw.Draw(proof)
    for i, p in enumerate(show):
        k = 'ship_' + p
        base = canvas_of(A, R[k])
        cells = [('phase 0', base)] + [(t, made[k + '_' + t][0]) for t in ('g1', 'g2')]
        for j, (lbl, im) in enumerate(cells):
            c = im if j == 0 else im
            ch = R[k][7]
            sc = 60.0 / ch
            dd = c.resize((max(1, int(c.width * sc)), max(1, int(c.height * sc))), Image.NEAREST)
            t = dd.resize((dd.width * 3, dd.height * 3), Image.NEAREST)
            col = i * 3 + j
            proof.paste(t, (col * T + T // 2 - t.width // 2, (T - t.height) // 2), t)
            d.text((col * T + 4, T + 5), p + ' ' + lbl, font=F, fill=(238, 238, 248))
    proof.save(os.path.join(ROOT, 'docs/THRUSTER_GLOW_0906S.png'))
    print('wrote docs/THRUSTER_GLOW_0906S.png')

    if not write:
        print('DRY RUN - nothing written.')
        return 0

    # ---- one write: pixels + manifest
    src = open(MANIFEST, encoding='utf-8').read()
    GUT = 2
    cx = rowh = striph = 0
    placed = {}
    for key in sorted(made, key=lambda k: -made[k][0].height):
        im = made[key][0]
        if cx + im.width + GUT > A.width:
            cx = 0; striph += rowh + GUT; rowh = 0
        placed[key] = (cx, striph)
        cx += im.width + GUT
        rowh = max(rowh, im.height)
    striph += rowh + GUT

    out = Image.new('RGBA', (A.width, A.height + striph), (0, 0, 0, 0))
    out.paste(A, (0, 0))
    for key, (im, ox, oy, cw, ch) in made.items():
        px, py = placed[key]
        out.paste(im, (px, A.height + py))

    n = 0
    for key, (im, ox, oy, cw, ch) in sorted(made.items()):
        px, py = placed[key]
        row = '"%s":[%d,%d,%d,%d,%d,%d,%d,%d]' % (
            key, px, A.height + py, im.width, im.height, ox, oy, cw, ch)
        base = key.rsplit('_', 1)[0]
        pat = re.compile(r'("' + re.escape(base) + r'":\[[^\]]*\])')
        if not pat.search(src):
            print('  base %s not in the manifest - refusing' % base)
            return 1
        if ('"%s":' % key) in src:                      # idempotent re-run
            src = re.sub(r'"' + re.escape(key) + r'":\[[^\]]*\]', row, src, count=1)
        else:
            src = pat.sub(lambda m: m.group(1) + ',' + row, src, count=1)
        n += 1

    for f, bak in ((ATLAS, ATLAS + '.0906s.bak'), (MANIFEST, MANIFEST + '.0906s.bak')):
        if not os.path.exists(bak):
            shutil.copy2(f, bak)
    out.save(ATLAS)
    open(MANIFEST, 'w', encoding='utf-8', newline=chr(10)).write(src)
    print('wrote the atlas (%dx%d, +%d rows) and %d new cells, in one write'
          % (out.width, out.height, striph, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
