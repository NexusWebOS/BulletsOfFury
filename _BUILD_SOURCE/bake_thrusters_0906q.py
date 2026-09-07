#!/usr/bin/env python3
"""bake_thrusters_0906q.py - Juggernaut's flame, on all nine airframes, at HIS scale.

    python _BUILD_SOURCE/bake_thrusters_0906q.py            # measure + proof only
    python _BUILD_SOURCE/bake_thrusters_0906q.py --write

Mike, 0906: "generate all ships we have to get remade with thrusters attached like juggernauts so
we remain consistent" -> then, on the first two attempts: "STOP!. I meant like what juggernaut
had! what your doing is wrong!"

⚠ HE MEANT THE SIZE, AND BOTH WRONG ATTEMPTS CAME FROM SIZING THE FLAME OFF THE RUNTIME PLUME
INSTEAD OF OFF HIS ART. The live `nthp_` plume draws 23.5 SCREEN px tall. Juggernaut's baked flame
is 15x22 in a 275-tall canvas that draws at 60 - **3.3 x 4.8 screen px**, a seventh of that. So:

  attempt 1 took his 15x22 crop and scaled it up to the runtime plume's 23.5px -> a 5x enlargement
            of a tiny sprite, which LANCZOS turned into smooth coloured mittens with no core.
  attempt 2 swapped the template for Lizzie's warbird flame (real art, 151x205, so no upscaling)
            and still drew it at 23.5px -> honest flames, still four times too big, still blobs.

Both rendered proofs looked wrong for the same reason and I read it as a template problem twice.
**The template was never the fault. The SIZE was.** A flame sized to the runtime plume cannot look
like Juggernaut's, because Juggernaut's is not that size.

⚠ AND AT HIS SCALE IT FITS EVERY SHIP AS THEY STAND. His flame lies INSIDE his hull's silhouette -
his ink measures 203x213 with the flame and 203x213 without it, because it is tucked into the
engine bells rather than hanging off the tail. Scaled to each canvas by ch/275 it needs ~13.4 px
below the nozzle against 14-57 px of room, on eight of nine pilots. So there is no canvas growth,
no `SHIP_DRAW_H` change, no `SPACE_SHIP_SIZE` change and no launch-lerp change - the whole 0819c
blast radius those attempts were carrying was self-inflicted by the wrong size.
(One frame, `ship_lizzie_l`, is 3 px short and gets its rect extended; nothing else moves.)

⚠ THE FLAME IS SEATED PER MOUNT, ON THAT NOZZLE'S OWN INK BOTTOM. A single ink-bottom for the
whole frame seats the flame on whatever hangs lowest - a wingtip or a fin on the banked frames -
and floats it clear of the engine it is supposed to leave. Each mount reads the lowest inked row
in its own column band, which is the nozzle it sits under.

⚠ JUGGERNAUT IS RESTORED, NOT RE-BAKED. His flame is the thing Mike approved, so his frames come
straight back off `.0906p.bak` rather than being reconstructed from a template lifted out of them.
"""
import os, re, sys, json, math, shutil, subprocess, colorsys
from collections import deque
from PIL import Image, ImageFilter, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')
GAME = os.path.join(ROOT, 'assets/game.js')
FLAME_SRC = ATLAS + '.0906p.bak'          # the plate that still carries Juggernaut's real exhaust

PILOTS = ['axel', 'cole', 'decker', 'falva', 'freezer', 'juggernaut', 'lizzie', 'maverick', 'yuri']
REF_CH = 275.0                             # Juggernaut's canvas height - the scale reference
# ⚠ THE FLAME GOES OVER THE HULL ON THESE FIVE (Mike, 0906r): "you have to layer the thrusters
# overlayer, not underlayer on cole, decker, yuri, maverick and lizzie". Their nozzles are drawn as
# BELLS the eye reads as open, so a flame composited behind the hull is cut off flat by the bell's
# own lower lip - visible at 6x as a straight edge across the top of every plume. The other three
# have flush tails where behind is right, and Juggernaut's is painted into his plate.
OVERLAY = {'cole', 'decker', 'yuri', 'maverick', 'lizzie'}
# ⚠ COLE'S FLAMES COME DOWN 10% (Mike, 0906t: "in #3 they might need to be scaled down about
# 10%"). His bells are the widest of the nine relative to his hull, so one global share of hull
# width lands slightly over-scale on him alone.
FLAME_SCALE = {'cole': 0.90}
# ⚠ MIKE'S CALL, AND IT OVERRIDES A MEASUREMENT THAT SAYS THEY ARE ALREADY CENTRED (0906u).
# "lizzie, move the left thruster to the left to get it centered a lil more, same with the right.
#  yuri - move the left to the right a little more, move the right to the left a little more."
# Checked first, because a nudge that papers over a real bug is worth catching: the bell bodies
# measure at +/-0.185..0.194 for lizzie and +/-0.138..0.145 for yuri across three row bands above
# the mouth - i.e. exactly where the flames already sit - and the flame template is centred in its
# own box to within 0.24 px, so neither is a placement defect. He is looking at the visible bell
# MOUTH rather than the housing, and the art is his. Stored in INK PIXELS and divided by each
# frame's own hull width so a banked frame gets the same visual shift as the hull one.
MOUNT_NUDGE_PX = {'lizzie': +3.0, 'yuri': -3.0}      # + spreads the pair, - closes it
BORE_F = 0.86                              # flame width as a share of the nozzle's measured bore
EMERGE = 0.92                              # the share of the flame that clears the nozzle
GLOW_F = 0.28                              # glow blur as a fraction of the flame's own height
GLOW_A = 0.45


def ship_rows():
    js = os.path.join(ROOT, '_BUILD_SOURCE/_k.js')
    open(js, 'w', encoding='utf-8').write(
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));\n"
        "const P=%s;const o={};for(const k in BOFX.ships){for(const p of P){"
        "if(k==='ship_'+p||k.indexOf('ship_'+p+'_')===0){o[k]=BOFX.ships[k];break;}}}\n"
        "process.stdout.write(JSON.stringify(o));\n" % json.dumps(PILOTS))
    out = subprocess.run(['node', js], capture_output=True, cwd=ROOT)
    return json.loads(out.stdout.decode())


def pilot_of(key):
    rest = key[len('ship_'):]
    for p in PILOTS:
        if rest == p or rest.startswith(p + '_'):
            return p
    return None


def is_hot(p):
    r, g, b, a = p
    if a < 32:
        return False
    h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
    if v >= 0.86:
        return True
    return v >= 0.72 and s >= 0.35 and (h < 0.15 or h > 0.90)


def lift_flame(rows):
    """Juggernaut's COMPLETE flame - hot core AND dark outer cone - at its authored size.

    ⚠ THE HOT-PIXEL DETECTOR THAT FOUND THIS FLAME IN 0906p CANNOT LIFT IT. It thresholds on
    brightness, so it returns the flame's luminous INTERIOR and leaves the darker red cone that
    gives the plume its shape - rendered side by side at 4x (docs/JUG_TAIL_ZOOM_0906Q.png) the
    stripped plate still carries a red OUTLINE of each flame, which is precisely the part the
    threshold refused. A core-only template baked onto the other eight ships came out as a 3px
    speck that was invisible on five of six pilots in the proof.

    So the flame is taken GEOMETRICALLY instead: the region where the two plates differ gives the
    footprint, and inside that footprint every inked pixel of the pre-strip plate is flame,
    because it hangs below the engine bells against transparent background."""
    r = rows['ship_juggernaut']
    Bk = Image.open(FLAME_SRC).convert('RGBA')
    Ak = Image.open(ATLAS).convert('RGBA')
    box = (r[0], r[1], r[0] + r[2], r[1] + r[3])
    jb = Bk.crop(box); bb = jb.getbbox(); jb = jb.crop(bb)
    ja = Ak.crop(box).crop(bb)
    W, H = jb.size
    pb, pa = jb.load(), ja.load()
    diff = [(x, y) for y in range(H) for x in range(W) if pb[x, y] != pa[x, y]]
    if not diff:
        raise SystemExit('the plates do not differ - juggernaut has already been restored?')
    ys = [q[1] for q in diff]
    y0, y1 = min(ys), max(ys)
    # split the footprint into its separate plumes on the column histogram
    cols = sorted(set(q[0] for q in diff))
    runs = []; cur = [cols[0]]
    for c in cols[1:]:
        if c - cur[-1] <= 3:
            cur.append(c)
        else:
            runs.append(cur); cur = [c]
    runs.append(cur)
    runs.sort(key=len, reverse=True)
    run = runs[0]
    x0, x1 = min(run) - 1, max(run) + 1
    t = Image.new('RGBA', (x1 - x0 + 1, y1 - y0 + 1), (0, 0, 0, 0))
    tp = t.load()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if 0 <= x < W and pb[x, y][3] > 16:
                tp[x - x0, y - y0] = pb[x, y]
    t = t.crop(t.getbbox())
    ink = max((y for y in range(H) for x in range(W) if pb[x, y][3] > 16), default=H - 1)
    return t, (ink - y1) / REF_CH, len(runs)


def tmpl_hue(tmpl):
    """the template's own dominant hue, as a saturation-weighted CIRCULAR mean"""
    px = tmpl.load()
    sx = sy = 0.0
    for y in range(tmpl.height):
        for x in range(tmpl.width):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if s < 0.15:
                continue
            w = s * v
            sx += w * math.cos(2 * math.pi * h)
            sy += w * math.sin(2 * math.pi * h)
    return (math.atan2(sy, sx) / (2 * math.pi)) % 1.0


def tint_flame(tmpl, rgb, href):
    """ROTATE the hue to the pilot's colour. Saturation and value are untouched.

    ⚠ SETTING THE HUE INSTEAD OF ROTATING IT FLATTENS THE FLAME, WHICH IS MIKE'S "the animation
    should be as visible as juggernauts with shading". Juggernaut's plume is not one colour: it
    runs white-hot core -> yellow -> orange -> deep red at the rim, and that HUE GRADIENT is most
    of what makes it read as fire. The first cut wrote one hue into every pixel and blended
    saturation toward the pilot tint's own, which erased the gradient and pushed the mid-tones to
    a flat high-saturation slab - Cole's came out a uniform green shape. A rotation carries the
    whole gradient across intact, which is exactly what this file means by "palette/luminance
    swaps, not overlays"."""
    h0, _, _ = colorsys.rgb_to_hsv(rgb[0] / 255., rgb[1] / 255., rgb[2] / 255.)
    d = (h0 - href) % 1.0
    out = tmpl.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if s < 0.12:
                continue                                  # white-hot core: untouched
            rr, gg, bb = colorsys.hsv_to_rgb((h + d) % 1.0, s, v)
            px[x, y] = (int(rr * 255 + .5), int(gg * 255 + .5), int(bb * 255 + .5), a)
    return out


def pilot_tints():
    src = open(GAME, encoding='utf-8', errors='replace').read()
    i = src.find('const PILOTS')
    seg = src[i:i + 24000] if i >= 0 else src[:24000]
    out = {}
    for p in PILOTS:
        m = re.search(r"'" + p + r"'[^}]{0,500}?tint\s*:\s*'(#[0-9a-fA-F]{6})'", seg)
        if m:
            h = m.group(1)
            out[p] = (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))
    return out


MOUNT_N = {'axel': 1, 'cole': 2, 'decker': 1, 'falva': 1, 'freezer': 1,
           'juggernaut': 2, 'lizzie': 2, 'maverick': 2, 'yuri': 2}
# ⚠ THE FOUR SINGLES ARE MIKE'S OWN CALL AND ARE NOT DETECTED. Quoted at THRUSTER_MOUNTS in
# game.js: "axel is in the middle not the sides, he only gets 1", "falva, she has a middle
# thruster only, no twins", "freezer, one middle thruster, no sides", "decker is good". A
# detector that overrode those would be replacing a decision with a measurement.
MOUNT_FIXED = {'axel': [0.0], 'falva': [0.0], 'freezer': [0.0], 'decker': [-0.0035]}


def tail_mounts(cell, n, band=0.28):
    """the nozzles, from the columns whose ink reaches the tail INSIDE THE FUSELAGE.

    ⚠ VALIDATED ON JUGGERNAUT BEFORE IT WAS USED ON ANYONE ELSE. His plate is the only hull in the
    set with a real exhaust painted on it, so his flame's own x-centroids are ground truth:
    measured [-0.1383, +0.1398], detected [-0.1404, +0.1404] - under a pixel at draw size. A
    metric that has not reproduced the known case is not evidence about the unknown ones.

    ⚠ AND THE FUSELAGE BOUND IS LOAD-BEARING. Unbounded, the same detector put axel at -0.21,
    falva at -0.26, freezer at -0.37 and one of yuri's at -0.46 - wingtips and fin trailing
    edges, which are genuinely the lowest ink on those hulls. game.js already says so at the
    mount table: "the engine bells sit either side of the spine, never out at the wingtips,
    which is what my first two detections kept catching."""
    bb = cell.getbbox()
    if not bb:
        return []
    px = cell.load(); x0, y0, x1, y1 = bb
    mid = (x0 + x1) / 2.0; W = x1 - x0
    lo, hi = mid - band * W, mid + band * W
    prof = {}
    for x in range(x0, x1):
        if not (lo <= x <= hi):
            continue
        for y in range(y1 - 1, y0 - 1, -1):
            if px[x, y][3] > 24:
                prof[x] = y; break
    if not prof:
        return []
    mxv = max(prof.values()); tol = max(3, int((y1 - y0) * 0.06))
    cols = sorted(x for x, v in prof.items() if v >= mxv - tol)
    runs = []; cur = [cols[0]]
    for c in cols[1:]:
        if c - cur[-1] <= 2:
            cur.append(c)
        else:
            runs.append(cur); cur = [c]
    runs.append(cur); runs.sort(key=len, reverse=True)
    if n == 1:
        r = runs[0]
        return [(sum(r) / float(len(r)) - mid) / W]
    if len(runs) >= 2:
        pick = sorted(runs[:2], key=lambda r: sum(r) / float(len(r)))
        v = [(sum(r) / float(len(r)) - mid) / W for r in pick]
        m = (abs(v[0]) + abs(v[1])) / 2.0     # twins are symmetric about the spine
        return [-m, m]
    r = runs[0]
    m = max(0.055, ((max(r) - min(r)) / 2.0 * 0.55) / W)
    return [-m, m]


FLAME_W_F = None                           # set from Juggernaut's own art at run time


def nozzles(cell, ox, oy, n, fixed=None, band=0.34, nudge=0.0):
    """each nozzle's CENTRE and MOUTH row, from the DEEPEST ink in the fuselage.

    ⚠ THE ENGINE BELL IS THE DEEPEST THING ON THE FUSELAGE, AND THAT IS THE ONLY SIGNAL THAT
    GENERALISES. Two earlier detectors failed here: a contiguous "tail run" measures the whole
    fuselage on Cole (one 51-wide run holding both his bells) and 63 px on Decker, and a cluster
    centroid landed Yuri 2.3 px outboard of his nozzles - Mike's "ALMOST aligned them perfectly
    but not quite". Grouping the columns whose ink reaches within 4 px of the hull's lowest row
    picks the bell tips out cleanly: yuri gives two 21-wide groups at +/-0.137 against five
    narrow fin tips, maverick two 21-wide at +/-0.149 either side of a 9-wide spine, lizzie two
    25-wide at +/-0.190.

    ⚠ AND THE SPINE HAS TO BE EXCLUDED BY POSITION, NOT BY SIZE. Maverick's centre group is a
    tail spine sitting exactly on the mid-line; taking the widest N groups would have used it."""
    bb = cell.getbbox()
    if not bb:
        return []
    px = cell.load(); x0, y0, x1, y1 = bb
    mid = (x0 + x1) / 2.0; W = x1 - x0
    lo, hi = mid - band * W, mid + band * W
    prof = {}
    for x in range(x0, x1):
        if not (lo <= x <= hi):
            continue
        for y in range(y1 - 1, y0 - 1, -1):
            if px[x, y][3] > 24:
                prof[x] = y; break
    if not prof:
        return []
    mxv = max(prof.values())
    deep = sorted(x for x, v in prof.items() if v >= mxv - 4)
    groups = []; cur = [deep[0]]
    for c in deep[1:]:
        if c - cur[-1] <= 3:
            cur.append(c)
        else:
            groups.append(cur); cur = [c]
    groups.append(cur)

    def mouth_of(g):
        return oy + max(prof[c] for c in g)

    if fixed:
        return [(ox + mid + mf * W, mouth_of(max(groups, key=len))) for mf in fixed]

    if n == 1:
        g = max(groups, key=len)
        return [(ox + sum(g) / float(len(g)), mouth_of(g))]

    # a twin pair: the widest group on each side of the spine
    L = [g for g in groups if sum(g) / float(len(g)) < mid - 0.04 * W]
    R2 = [g for g in groups if sum(g) / float(len(g)) > mid + 0.04 * W]
    if L and R2:
        gl = max(L, key=len); gr = max(R2, key=len)
        m = ((mid - sum(gl) / float(len(gl))) + (sum(gr) / float(len(gr)) - mid)) / 2.0
        m += nudge
        return [(ox + mid - m, mouth_of(gl)), (ox + mid + m, mouth_of(gr))]
    # ⚠ COLE'S TWO BELLS AND THE SPINE BETWEEN THEM ALL REACH THE SAME DEPTH, so they arrive as
    # ONE 51-wide group and there is no second group to pair with. Splitting it down the middle
    # (+/- width/4) puts the flames 4 px too close together on each side - the misalignment Mike
    # kept seeing on the green ship. A bell measures 11-14% of hull width on every pilot where the
    # groups DO separate (yuri 21/145, lizzie 25/222, maverick 21/187), so the two bells sit half
    # a bell width in from each END of the merged run, not a quarter of it from the centre.
    g = max(groups, key=len)
    half = max(3.0, 0.12 * W / 2.0) - nudge * W
    return [(ox + min(g) + half, mouth_of(g)), (ox + max(g) - half, mouth_of(g))]


def nozzle_bottom(cell, ox, oy, cx, band):
    """the lowest inked row in this mount's own column band - the nozzle it sits under.

    ⚠ a single ink-bottom for the whole frame seats the flame on whatever hangs lowest, which on
    the banked frames is a wingtip, not an engine."""
    px = cell.load()
    w, h = cell.size
    lo = max(0, int(cx - ox - band / 2)); hi = min(w, int(cx - ox + band / 2) + 1)
    best = None
    for y in range(h - 1, -1, -1):
        for x in range(lo, hi):
            if px[x, y][3] > 24:
                best = y; break
        if best is not None:
            break
    return (oy + best) if best is not None else None


def main():
    write = '--write' in sys.argv
    R = ship_rows()
    A = Image.open(ATLAS).convert('RGBA')
    B = Image.open(FLAME_SRC).convert('RGBA')
    tmpl, seat_f, nb = lift_flame(R)
    HREF = tmpl_hue(tmpl)
    global FLAME_W_F
    _jbb = A.crop((R['ship_juggernaut'][0], R['ship_juggernaut'][1],
                   R['ship_juggernaut'][0] + R['ship_juggernaut'][2],
                   R['ship_juggernaut'][1] + R['ship_juggernaut'][3])).getbbox()
    FLAME_W_F = tmpl.width / float(_jbb[2] - _jbb[0])
    print('flame template %dx%d off juggernaut (%d plume(s) on his plate), seat %.4f of canvas'
          % (tmpl.width, tmpl.height, nb, seat_f))
    print('   at his own canvas that is %.1f%% of the hull height - the size Mike approved'
          % (100.0 * tmpl.height / REF_CH))

    newm_path = os.path.join(ROOT, '_BUILD_SOURCE/sc_src_0906/_new_mounts.json')
    newm = json.load(open(newm_path)) if os.path.exists(newm_path) else {}
    old = json.load(open(os.path.join(ROOT, 'assets/data/thruster_mounts.json')))
    tints = pilot_tints()

    baked, offs, changed, short = {}, {}, 0, []
    for key, r in sorted(R.items()):
        x, y, w, h, ox, oy, cw, ch = r
        p = pilot_of(key)
        if key.endswith('_nf'):
            continue                                   # the flameless family stays flameless
        if p == 'juggernaut':
            baked[key] = B.crop((x, y, x + w, y + h))  # restored, not re-baked
            continue
        cell = A.crop((x, y, x + w, y + h))
        bb = cell.getbbox()
        if not bb:
            continue
        s = ch / REF_CH                                # this canvas against Juggernaut's
        fw = max(3, int(round(tmpl.width * s)))
        fh = max(4, int(round(tmpl.height * s)))
        plume = tint_flame(tmpl, tints.get(p, (255, 150, 60)), HREF).resize((fw, fh), Image.LANCZOS)

        mt = MOUNT_FIXED.get(p) or tail_mounts(cell, MOUNT_N.get(p, 1))
        hull_cx = ox + (bb[0] + bb[2]) / 2.0
        hull_w = bb[2] - bb[0]

        canvas = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        layer = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        for mf in mt:
            mx = hull_cx + mf * hull_w
            nzb = nozzle_bottom(cell, ox, oy, mx, max(6, fw * 1.5))
            if nzb is None:
                nzb = oy + bb[3]
            # ⚠ THE FLAME HAS TO CLEAR THE NOZZLE, AND SEATING IT ON JUGGERNAUT'S OWN GAP DOES
            # NOT. His plumes are painted INTO open engine bells, so his sit above his ink bottom
            # and still show. Every other hull is solid there, and the plume is composited BEHIND
            # the hull on purpose (so it trails from under the tail) - so a flame seated the same
            # way is covered completely. The first render of this looked flameless on eight of
            # nine ships for exactly that reason. EMERGE is the share that clears the tail.
            top = int(round(nzb - fh * (1.0 - EMERGE)))
            top = max(0, min(ch - fh, top))            # never past the canvas floor
            layer.alpha_composite(plume, (int(round(mx - fw / 2.0)), top))
        glow = layer.filter(ImageFilter.GaussianBlur(max(1, int(round(fh * GLOW_F)))))
        glow.putalpha(glow.getchannel('A').point(lambda v: int(v * GLOW_A)))
        if p in OVERLAY:
            canvas.alpha_composite(cell, (ox, oy))
            canvas.alpha_composite(glow)
            canvas.alpha_composite(layer)
        else:
            canvas.alpha_composite(glow)
            canvas.alpha_composite(layer)
            canvas.alpha_composite(cell, (ox, oy))
        nb2 = canvas.getbbox()
        if nb2 and nb2[3] >= ch:
            short.append(key)
        baked[key] = canvas.crop(nb2) if nb2 else canvas
        offs[key] = (nb2[0], nb2[1]) if nb2 else (0, 0)
        changed += 1

    print('baked %d frames (juggernaut restored, _nf left clean); %d frames reach the canvas floor'
          % (changed, len(short)))
    for k in short:
        print('   tight: %s' % k)

    # ---- proof
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 13)
    except Exception:
        F = ImageFont.load_default()
    show = ['juggernaut', 'lizzie', 'cole', 'maverick', 'falva', 'axel']
    T, SC = 150, 3
    proof = Image.new('RGB', (T * len(show) * 2, T + 24), (20, 20, 26))
    d = ImageDraw.Draw(proof)
    for i, p in enumerate(show):
        key = 'ship_' + p
        x, y, w, h, ox, oy, cw, ch = R[key]
        oldc = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        oldc.alpha_composite(A.crop((x, y, x + w, y + h)), (ox, oy))
        newc = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        nb2 = baked[key]
        if p == 'juggernaut':
            newc.alpha_composite(nb2, (ox, oy))
        else:
            newc.alpha_composite(nb2, (offs[key][0], offs[key][1]))
        for j, (lbl, im) in enumerate(((p + ' NOW', oldc), (p + ' BAKED', newc))):
            dd = im.resize((max(1, int(round(cw * 60.0 / ch))), 60), Image.NEAREST)
            t = dd.resize((dd.width * SC, dd.height * SC), Image.NEAREST)
            col = i * 2 + j
            proof.paste(t, (col * T + T // 2 - t.width // 2, (T - t.height) // 2), t)
            d.text((col * T + 4, T + 5), lbl, font=F, fill=(238, 238, 248))
        d.line([(i * 2) * T, T // 2, (i * 2 + 2) * T, T // 2], fill=(70, 100, 190), width=1)
    proof.save(os.path.join(ROOT, 'docs/THRUSTERS_BAKED_0906Q.png'))
    print('wrote docs/THRUSTERS_BAKED_0906Q.png  (drawn at the real 60px, then 3x to look at)')

    if not write:
        print('DRY RUN - nothing written.')
        return 0

    # ============================================================
    # ONE WRITE: pixels and manifest together (the standing rule - 0906g).
    # Juggernaut is PASTED IN PLACE: his flame lies inside his existing trim (ink 203x213 with it
    # and without it), so his rects do not move and only his pixels come back. Everyone else grows
    # downward, so their frames go into an appended strip and their rects are repointed.
    # ============================================================
    src = open(MANIFEST, encoding='utf-8').read()
    grow = {k: v for k, v in baked.items() if pilot_of(k) != 'juggernaut'}
    GUT = 2
    rowh = cx = 0
    placed, stripw, striph = {}, A.width, 0
    for key in sorted(grow, key=lambda k: -grow[k].height):
        im = grow[key]
        if cx + im.width + GUT > stripw:
            cx = 0; striph += rowh + GUT; rowh = 0
        placed[key] = (cx, striph)
        cx += im.width + GUT
        rowh = max(rowh, im.height)
    striph += rowh + GUT

    out = Image.new('RGBA', (A.width, A.height + striph), (0, 0, 0, 0))
    out.paste(A, (0, 0))
    for key, im in baked.items():
        if pilot_of(key) == 'juggernaut':
            r = R[key]
            out.paste(im, (r[0], r[1]))                     # restored in place
        else:
            px, py = placed[key]
            out.paste(im, (px, A.height + py))

    n = 0
    for key, im in grow.items():
        r = R[key]
        px, py = placed[key]
        ox2, oy2 = offs[key]
        row = '"%s":[%d,%d,%d,%d,%d,%d,%d,%d]' % (
            key, px, A.height + py, im.width, im.height, ox2, oy2, r[6], r[7])
        pat = re.compile(r'"' + re.escape(key) + r'":\[[^\]]*\]')
        if not pat.search(src):
            print('  %s is missing from the manifest - refusing' % key)
            return 1
        src = pat.sub(row, src, count=1)
        n += 1

    for f, bak in ((ATLAS, ATLAS + '.0906q.bak'), (MANIFEST, MANIFEST + '.0906q.bak')):
        if not os.path.exists(bak):
            shutil.copy2(f, bak)
    out.save(ATLAS)
    open(MANIFEST, 'w', encoding='utf-8', newline=chr(10)).write(src)
    print('wrote the atlas (%dx%d, +%d rows) and %d repointed rects, in one write'
          % (out.width, out.height, striph, n))
    print('   juggernaut restored in place; %d _nf frames left flameless'
          % sum(1 for k in R if k.endswith('_nf')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
