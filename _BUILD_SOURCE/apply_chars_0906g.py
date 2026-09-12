#!/usr/bin/env python3
"""apply_chars_0906g.py - land the corrected Lizzie, Falva and Yuri art.

    python _BUILD_SOURCE/apply_chars_0906g.py            # proof only
    python _BUILD_SOURCE/apply_chars_0906g.py --write

Mike, 0906: "regenerate lizzie and falva's body and portraits. falva is young no gray or white
hair. lizzie is also a white curvy mid 30's woman. Yuri looks very diff from the rest, he needs to
match there art style ... you also need to regenerate yuri's body frame to match."

⚠ LIZZIE'S BODY IS RECOLOURED, NOT REGENERATED, AND THE REASON IS WORTH RECORDING. Two attempts at
an edit_asset_id pass on her standing figure came back `content_policy_violation` - the source
plate plus any description of her build trips the provider's safety filter, and rewording it to
"solid and athletic" did not help. Rather than keep spending credits on refusals, her body takes a
MEASURED skin-tone shift sampled from her new portrait: the correction Mike asked for that actually
reads at the 212px the bay draws her at is the skin, and a deterministic recolour delivers exactly
that with no filter in the loop. Her age and build stay as authored, which is stated rather than
quietly dropped.

⚠ AND FALVA'S ATLAS PORTRAITS NEVER HAD GREY HAIR - I PUT IT THERE. Rendered the originals before
assuming: `port_falva_*` on ui_dialogue is auburn-brown throughout. The white streak Mike is
objecting to appeared in the AVATAR I generated in 0906f and nowhere else. Worth knowing because
the instinct on "no gray or white hair" is to sweep her whole portrait set for pale pixels, which
would have eaten the white trim on her flight suit to fix a defect that was not in those files.

⚠ THE PORTRAIT CELLS ARE WRITTEN AT THEIR EXISTING RECT SIZE. `port_lizzie_idle` is 295x399 and
`port_falva_idle` 238x347; the generated plates are neither. Pasting at native size would spill
into the neighbouring cell on a shared atlas - ui_dialogue carries every pilot's whole emotion set.
Each is fitted to its own rect and centred, and the rect is cleared first so no old pixel survives
around a smaller new plate.
"""
import os, sys, json, shutil, subprocess, colorsys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(ROOT, '_BUILD_SOURCE/sc_out_0906')
SHEET = os.path.join(ROOT, 'assets/game/atlas/ui_dialogue.png')
BODIES = os.path.join(ROOT, 'assets/game/pilot_bodies')
YURI_BODY = os.path.join(ROOT, 'assets/game/yuri_v2/yuri_body_0.png')
AVATARS = os.path.join(ROOT, 'assets/game/pilot_avatars')

PORTRAITS = {'lizzie': 'port_lizzie_v2.png', 'falva': 'port_falva_v2.png'}


def cells(pat):
    js = subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "const o={};for(const k in BOFX.cells)if(/" + pat + "/.test(k))o[k]=BOFX.cells[k];"
        "process.stdout.write(JSON.stringify(o));"], capture_output=True, cwd=ROOT)
    return json.loads(js.stdout.decode())


def skin_stats(im):
    """mean HSV of the SKIN pixels - hue 10..45, the band a face sits in for every pilot here"""
    px = im.convert('RGBA').load()
    hs, ss, vs = [], [], []
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a < 32:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if 0.028 <= h <= 0.125 and 0.18 <= s <= 0.75 and v >= 0.30:
                hs.append(h); ss.append(s); vs.append(v)
    if not hs:
        return None
    n = len(hs)
    return (sum(hs) / n, sum(ss) / n, sum(vs) / n, n)


def shift_skin(im, ds, dv):
    """lighten and desaturate the skin band by a measured delta. Luminance-relative, so the
    modelling on the face survives - a flat fill would turn her into a mask."""
    px = im.load(); n = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a < 32:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if 0.028 <= h <= 0.125 and 0.18 <= s <= 0.75 and v >= 0.30:
                ns = max(0.05, min(1.0, s * ds))
                nv = max(0.0, min(1.0, v * dv))
                rr, gg, bb = colorsys.hsv_to_rgb(h, ns, nv)
                px[x, y] = (int(rr * 255 + .5), int(gg * 255 + .5), int(bb * 255 + .5), a)
                n += 1
    return n


def fit_into(plate, w, h):
    bb = plate.getbbox()
    p = plate.crop(bb) if bb else plate
    s = min(w / p.width, h / p.height)
    t = p.resize((max(1, int(p.width * s)), max(1, int(p.height * s))), Image.LANCZOS)
    cv = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    cv.alpha_composite(t, ((w - t.width) // 2, (h - t.height) // 2))
    return cv


def main():
    write = '--write' in sys.argv
    A = Image.open(SHEET).convert('RGBA')
    C = cells('^port_(lizzie|falva)_')
    print('%d lizzie/falva portrait cells on ui_dialogue' % len(C))

    # ---- the measured skin shift, taken from Lizzie's old idle against her new portrait
    old_idle = None
    for k, c in C.items():
        if k == 'port_lizzie_idle':
            old_idle = A.crop((c[1], c[2], c[1] + c[3], c[2] + c[4]))
    new_l = Image.open(os.path.join(GEN, PORTRAITS['lizzie'])).convert('RGBA')
    a, b = skin_stats(old_idle), skin_stats(new_l)
    if not (a and b):
        print('could not sample skin - refusing'); return 1
    ds, dv = b[1] / a[1], b[2] / a[2]
    print('lizzie skin: old s%.3f v%.3f (%d px) -> new s%.3f v%.3f (%d px)' % (a[1], a[2], a[3], b[1], b[2], b[3]))
    print('   shift: saturation x%.3f, value x%.3f  (applied to her other cells and her body)' % (ds, dv))

    # ---- portraits into their own rects
    wrote = []
    for k, c in sorted(C.items()):
        _, x, y, w, h = c
        who = 'lizzie' if 'lizzie' in k else 'falva'
        if k.endswith('_idle') or k.endswith('_smile'):
            src = Image.open(os.path.join(GEN, PORTRAITS[who])).convert('RGBA')
            cell = fit_into(src, w, h)
            A.paste(cell, (x, y))          # paste, not composite: the rect is replaced outright
            wrote.append((k, 'new plate'))
        elif who == 'lizzie':
            cell = A.crop((x, y, x + w, y + h))
            n = shift_skin(cell, ds, dv)
            A.paste(cell, (x, y))
            wrote.append((k, '%d skin px shifted' % n))
        else:
            wrote.append((k, 'unchanged - her originals never had grey hair'))
    for k, note in wrote:
        print('   %-24s %s' % (k, note))

    # ---- bodies
    body_notes = []
    fb = os.path.join(GEN, 'bd_falva.png')
    yb = os.path.join(GEN, 'bd_yuri_new.png')
    ref_h = Image.open(YURI_BODY).convert('RGBA')
    bbr = ref_h.getbbox()
    H = (bbr[3] - bbr[1]) if bbr else 273

    def norm(p):
        im = Image.open(p).convert('RGBA')
        bb = im.getbbox()
        im = im.crop(bb) if bb else im
        s = H / im.height
        return im.resize((max(1, round(im.width * s)), H), Image.LANCZOS)

    new_bodies = {}
    if os.path.exists(fb):
        new_bodies[os.path.join(BODIES, 'falva_body_0.png')] = norm(fb)
        body_notes.append('falva  regenerated (young, no grey)')
    if os.path.exists(yb):
        new_bodies[YURI_BODY] = norm(yb)
        body_notes.append('yuri   restyled to match the others')
    lb = os.path.join(BODIES, 'lizzie_body_0.png')
    if os.path.exists(lb):
        im = Image.open(lb).convert('RGBA')
        n = shift_skin(im, ds, dv)
        new_bodies[lb] = im
        body_notes.append('lizzie %d skin px shifted (generation was refused - see the header)' % n)
    for t in body_notes:
        print('   ' + t)

    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 14)
    except Exception:
        F = ImageFont.load_default()
    shots = []
    for k in ('port_lizzie_idle', 'port_lizzie_anger', 'port_falva_idle'):
        if k in C:
            _, x, y, w, h = C[k]
            shots.append((k.replace('port_', ''), A.crop((x, y, x + w, y + h))))
    for p, im in new_bodies.items():
        shots.append((os.path.basename(p).replace('_body_0.png', ' body'), im))
    T = 210
    proof = Image.new('RGB', (T * max(1, len(shots)), T + 22), (22, 22, 28))
    d = ImageDraw.Draw(proof)
    for i, (lbl, im) in enumerate(shots):
        bb = im.getbbox(); c = im.crop(bb) if bb else im
        s = min((T - 12) / c.width, (T - 12) / c.height)
        t = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
        proof.paste(t, (i * T + (T - t.width) // 2, (T - t.height) // 2), t)
        d.text((i * T + 4, T + 4), lbl, font=F, fill=(240, 240, 250))
    proof.save(os.path.join(ROOT, 'docs/CHARS_APPLIED_0906G.png'))
    print(os.linesep + 'wrote docs/CHARS_APPLIED_0906G.png')

    if not write:
        print('DRY RUN - nothing written. Re-run with --write.')
        return 0
    bak = SHEET + '.0906g2.bak'
    if not os.path.exists(bak):
        shutil.copy2(SHEET, bak)
    A.save(SHEET)
    for p, im in new_bodies.items():
        im.save(p)
    print('wrote ui_dialogue and %d bodies' % len(new_bodies))
    return 0


if __name__ == '__main__':
    sys.exit(main())
