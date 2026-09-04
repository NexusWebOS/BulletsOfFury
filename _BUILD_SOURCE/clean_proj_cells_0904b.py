"""
clean_proj_cells_0904b.py - de-halo and de-speck enemy projectile cells in the shared atlas.

Mike, 0904: "you need to clean up the purple halo's and clean up these lasers. the lasers have
black holes and weird pixelation going on, the missiles are clearly halo'd purple"

⚠ RE-RUN THIS AFTER ANY ATLAS REPACK. atlas_repack_0903.py crops these cells out of the upstream
   CF_EnemyCombatPatterns vendor packs, and the purple is in that SOURCE art - so a repack puts it
   straight back. This script is the fix-up pass, not a one-time edit.

TWO DEFECTS, MEASURED BEFORE ANYTHING WAS CHANGED:

  PURPLE HALO   mfx_hom_0 carries 11-17% magenta pixels on frames 1,2,5,6,7 (2-3% on the rest).
                It is NOT alpha fringing - every cell in this atlas is binary alpha, 0 or 255,
                with zero partial pixels. It is opaque magenta sitting in what should be grey
                rocket smoke, so it reads as a purple halo around the plume.

  BLACK SPECKS  isolated dark pixels INSIDE a bright body (mfx_ea_3 frames 1,4,6,7; mfx_mg_2 1,2,3).

⚠ THE OBVIOUS RULE FOR "BLACK HOLE" IS WRONG AND WOULD HAVE WRECKED THE ART. "an opaque dark pixel
   that does not touch transparency" flags 4,553 pixels on bfx_toxic_i_5 and 166 on mfx_emr_0_3 -
   because these sprites have black OUTLINES (a 1px black edge tracing every silhouette, which is
   the house style) and dark metallic bodies. Rendered the masks: the black traces the outline
   exactly. So a speck here is only a dark pixel SURROUNDED BY BRIGHT ONES - >=6 of its 8
   neighbours opaque and bright. That leaves outlines and dark shading untouched by construction.

⚠ AND NOT ALL PURPLE IS A DEFECT. mfx_ea_18_*/mfx_ea_19_* run 54-70% purple and mfx_emr_0_3 is
   45.9% - those are DESIGNED purple ordnance (emr_0 is four COLOUR variants: red/green/blue/
   purple, not four frames). They are excluded by name. Only families whose surrounding art is
   grey smoke get de-purpled.
"""
import io, re, os, sys, colorsys, shutil, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS_DIR = os.path.join(ROOT, 'assets', 'game', 'atlas')

# family -> (frame count, de-purple?, de-speck?)
TARGETS = {
    'mfx_hom_0': (10, True,  True),   # rocket smoke that went magenta
    'mfx_ea_3':  (8,  False, True),   # the red capsules/fork: specks only, zero purple measured
    'mfx_mg_2':  (5,  False, True),
}
NEVER_DEPURPLE = ('mfx_emr_0', 'mfx_ea_18', 'mfx_ea_19', 'xlz_shadow', 'xorb_void', 'xorb_antimatter')


def rects_from_manifest():
    s = io.open(os.path.join(ROOT, 'assets', 'manifest.js'), encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'"([A-Za-z0-9_]+)":\["([A-Za-z0-9_]+)",(\d+),(\d+),(\d+),(\d+)\]', s):
        out[m.group(1)] = (m.group(2),) + tuple(int(v) for v in m.groups()[2:])
    return out


def is_purple(r, g, b):
    """⚠ THE FIRST CUT USED hue 265-340 / sat>0.25 AND LEFT HALF THE HALO BEHIND. Measured the
    residue on the cleaned frames: 147 pixels still in the magenta band on mfx_hom_0_7, piled up
    at hue 335-350 with sat 0.2-0.8 - a dark PLUM just outside the band, which is what still read
    as a purple wash down the lower plume. Two bands now, and a much lower saturation floor so the
    pale lavender in the bright smoke (sat ~0.10) goes too.

    Widening toward red is safe here BY CONSTRUCTION: the repair takes its chroma from the
    pixel's non-purple neighbours, so a pixel wrongly flagged beside the rocket flame is re-tinted
    like the flame rather than turned grey. The black outline (v<0.10) and the bright orange
    flame (hue 20-50) fall outside both bands anyway."""
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    h *= 360.0
    if 265 <= h <= 340 and s > 0.08 and v > 0.10:
        return True                       # magenta/violet, including the pale lavender cast
    if 330 <= h <= 355 and s > 0.15 and v < 0.50:
        return True                       # the dark plum residue in the lower plume
    return False


def lum(r, g, b):
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def clean_cell(im, depurple, despeck):
    """returns (new image, n_purple_fixed, n_specks_fixed)"""
    im = im.copy()
    px = im.load()
    w, h = im.size
    nb8 = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]

    def neigh(x, y):
        for dx, dy in nb8:
            i, j = x + dx, y + dy
            if 0 <= i < w and 0 <= j < h:
                yield px[i, j]

    npur = nspk = 0

    if depurple:
        # Iterative, edge-inward. A purple pixel KEEPS ITS LUMINANCE (so the smoke's shading
        # survives) and borrows hue+saturation from its non-purple opaque neighbours. Pure
        # neighbour-averaging would blur the plume flat; this only moves the colour.
        for _ in range(6):
            targets = [(x, y) for y in range(h) for x in range(w)
                       if px[x, y][3] and is_purple(*px[x, y][:3])]
            if not targets:
                break
            changed = False
            snap = {}
            for x, y in targets:
                src = [n for n in neigh(x, y) if n[3] and not is_purple(*n[:3])]
                if not src:
                    continue
                r, g, b, a = px[x, y]
                mr = sum(n[0] for n in src) / len(src)
                mg = sum(n[1] for n in src) / len(src)
                mb = sum(n[2] for n in src) / len(src)
                ml = lum(mr, mg, mb)
                k = (lum(r, g, b) / ml) if ml > 4 else 0.0
                if ml <= 4:            # neighbours are essentially black (the outline) -> go grey
                    v = lum(r, g, b)
                    snap[(x, y)] = (int(v), int(v), int(v), a)
                else:
                    snap[(x, y)] = (max(0, min(255, int(mr * k))),
                                    max(0, min(255, int(mg * k))),
                                    max(0, min(255, int(mb * k))), a)
                changed = True
            for p, v in snap.items():
                px[p] = v
                npur += 1
            if not changed:
                break

    if despeck:
        # a speck is DARK and RINGED BY BRIGHT - never an outline pixel, never dark shading
        fix = {}
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if not a or max(r, g, b) >= 40:
                    continue
                ns = list(neigh(x, y))
                bright = [n for n in ns if n[3] and max(n[:3]) > 120]
                if len(ns) == 8 and len(bright) >= 6:
                    bright.sort(key=lambda n: lum(*n[:3]))
                    m = bright[len(bright) // 2]
                    fix[(x, y)] = (m[0], m[1], m[2], a)
        for p, v in fix.items():
            px[p] = v
            nspk += 1

    return im, npur, nspk


def main():
    apply = '--apply' in sys.argv
    rects = rects_from_manifest()
    byfile = {}
    report = []
    for fam, (n, dp, ds) in TARGETS.items():
        if dp and fam.startswith(NEVER_DEPURPLE):
            raise SystemExit('refusing to de-purple %s - it is designed purple' % fam)
        for i in range(n):
            k = '%s_%d' % (fam, i)
            if k not in rects:
                report.append((k, 'MISSING', 0, 0))
                continue
            f, x, y, w, hh = rects[k]
            path = os.path.join(ATLAS_DIR, f + '.png')
            if f not in byfile:
                byfile[f] = Image.open(path).convert('RGBA')
            src = byfile[f].crop((x, y, x + w, y + hh))
            new, npur, nspk = clean_cell(src, dp, ds)
            if npur or nspk:
                byfile[f].paste(new, (x, y))
            report.append((k, '%dx%d' % (w, hh), npur, nspk))

    print('%-14s %-8s %8s %8s' % ('key', 'size', 'purple', 'specks'))
    tp = ts = 0
    for k, sz, a, b in report:
        print('%-14s %-8s %8d %8d' % (k, sz, a, b))
        tp += a; ts += b
    print('%-14s %-8s %8d %8d' % ('TOTAL', '', tp, ts))

    for f, im in byfile.items():
        dst = os.path.join(ATLAS_DIR, f + '.png')
        if apply:
            # ⚠ THE BACKUP GOES TO TEMP, NOT NEXT TO THE ATLAS. Writing eproj_shared.png.pre0904b
            #   into assets/ once put a 4.7MB blob into a `git add -A` and therefore into history
            #   forever. The repo IS the backup - `git show HEAD:assets/game/atlas/<f>.png` gets
            #   the previous bytes back - so a working copy in temp is enough.
            bak = os.path.join(tempfile.gettempdir(), f + '.pre_clean.png')
            if not os.path.exists(bak):
                shutil.copy2(dst, bak)
            im.save(dst)
            print('WROTE', dst, '(pre-change copy at %s)' % bak)
        else:
            prev = os.path.join(os.environ.get('TMPDIR', '.'), f + '_cleaned_preview.png')
            im.save(prev)
            print('PREVIEW ONLY ->', prev, '   (pass --apply to write the atlas)')


if __name__ == '__main__':
    main()
