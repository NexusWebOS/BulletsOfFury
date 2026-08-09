#!/usr/bin/env python3
"""
strip_crackle_0801kl.py — REMOVE THE BAKED-IN CRACKLE FROM THE EIGHT 0801hm BODIES

Mike: "these bosses should never do that crackle effect at all."

WHAT THE CRACKLE ACTUALLY IS
----------------------------
Not a runtime effect. There is no draw call to disable. The zigzag bolts are
PAINTED INTO THE PNGs of every damaged / critical / destroyed frame by the
0801hm body builder. Measured, per family, one flat fully-opaque RGB:

    nlgt (225, 70, 55)   nobd (255,112, 20)   nmrv (255,170, 42)
    nglr ( 42,180,255)   nslc (144,255, 35)   nrmp (225, 54, 54)
    ntxl (118,255, 36)   ncyc ( 42,162,240)

Verified safe to key on:
  * alpha is 255 on every bolt pixel — no soft edge
  * a 1px ring around the bolts contains ZERO near-bolt colours — no glow halo,
    no anti-aliasing, so deleting the exact colour cannot leave a fringe
  * the colour is absent from every *_intact frame, so the body's own glowing
    detail (obsidian's magma vents, glacier's energy rails) is NOT this colour
    and is left completely untouched

WHY AN OFFSET TABLE IS EMITTED INSTEAD OF RE-CROPPING
-----------------------------------------------------
The builder grew the canvas to fit bolts that overhang the body, so every
damage plate is a different size from its intact counterpart (66 of 67 sections
mismatched). They therefore cannot be composited at the intact offsets.

Forcing them back onto the intact canvas was tried and REJECTED: it is lossy.
A destroyed plate is legitimately larger than its intact one (debris spreads
outward), and cropping ntxl_tail_blade_destroyed to its 12x2 intact plate threw
away 232 real pixels. The art is not wrong; the assumption was.

So nothing is resized. Instead each plate is aligned against its own intact
plate by silhouette match, and the resulting per-state (dx,dy) is written to
assets/section_offsets.json for the draw path to place them. Non-destructive
and exact.

FILLING THE HOLES
-----------------
A bolt drawn over the hull overwrote real body pixels; deleting it leaves a
hole. Each bolt pixel is classified:
  INTERIOR (mostly opaque body around it) -> inpainted from neighbours, so the
           local scorch/dent texture of THAT damage state is preserved
  EXTERIOR (out in open space)            -> left transparent, which is correct;
           there was never any body there
"""
import json, os, re, shutil, sys
import numpy as np
import cv2
from PIL import Image
from scipy import ndimage as nd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOLT = {
    'nlgt': (225, 70, 55), 'nobd': (255, 112, 20),
    'nmrv': (255, 170, 42), 'nglr': (42, 180, 255),
    'nslc': (144, 255, 35), 'nrmp': (225, 54, 54),
    'ntxl': (118, 255, 36), 'ncyc': (42, 162, 240),
}
BACKUP = os.path.join(ROOT, '_superseded', 'crackle_0801kl')


def load_manifest():
    s = open(os.path.join(ROOT, 'assets/manifest.js')).read()
    return json.loads(re.search(r'window\.BOFX=([\s\S]*?\});', s).group(1))


def bolt_mask(rgba, bc):
    rgb, a = rgba[:, :, :3], rgba[:, :, 3]
    return ((rgb[:, :, 0] == bc[0]) & (rgb[:, :, 1] == bc[1]) &
            (rgb[:, :, 2] == bc[2]) & (a > 0))


def declackle(rgba, bc):
    """Return a copy with the bolts removed. Interior holes inpainted,
       exterior strokes erased."""
    m = bolt_mask(rgba, bc)
    if not m.any():
        return rgba, 0
    out = rgba.copy()
    body = (rgba[:, :, 3] > 0) & ~m            # real body, bolts excluded

    # A bolt pixel is INTERIOR if real body surrounds it. Measured over a 5x5
    # neighbourhood: a stroke crossing the hull sits in dense body, a stroke
    # arcing through open air does not.
    dens = nd.uniform_filter(body.astype(np.float32), size=5)
    interior = m & (dens > 0.40)
    exterior = m & ~interior

    if interior.any():
        # Inpaint RGB from surrounding pixels so the damage texture of THIS
        # state is what fills the stroke, not a clean intact pixel.
        bgr = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2BGR)
        # Neutralise the bolt colour first so Telea cannot smear it inward.
        bgr[m] = 0
        fill = cv2.inpaint(bgr, m.astype(np.uint8) * 255, 3, cv2.INPAINT_TELEA)
        fill = cv2.cvtColor(fill, cv2.COLOR_BGR2RGB)
        out[:, :, :3][interior] = fill[interior]
        out[:, :, 3][interior] = 255
    out[:, :, :3][exterior] = 0
    out[:, :, 3][exterior] = 0
    return out, int(m.sum())


def align_offset(dmg, base):
    """Find where dmg's body sits relative to base's canvas, by matching the
       alpha silhouettes. Returns (dx, dy) to place dmg onto base's canvas."""
    db = (dmg[:, :, 3] > 128).astype(np.float32)
    bb = (base[:, :, 3] > 128).astype(np.float32)
    # pad base so the template can slide fully
    ph, pw = db.shape
    bh, bw = bb.shape
    pad = ((max(0, ph - bh) + 8, max(0, ph - bh) + 8),
           (max(0, pw - bw) + 8, max(0, pw - bw) + 8))
    bbp = np.pad(bb, pad)
    r = cv2.matchTemplate(bbp, db, cv2.TM_CCORR_NORMED)
    _, mx, _, loc = cv2.minMaxLoc(r)
    dx = loc[0] - pad[1][0]
    dy = loc[1] - pad[0][0]
    return dx, dy, float(mx)


def recanvas(dmg, base_shape, dx, dy):
    """Place dmg onto a canvas of base_shape at (dx,dy)."""
    H, W = base_shape[:2]
    out = np.zeros((H, W, 4), np.uint8)
    sh, sw = dmg.shape[:2]
    x0, y0 = max(0, dx), max(0, dy)
    x1, y1 = min(W, dx + sw), min(H, dy + sh)
    if x1 <= x0 or y1 <= y0:
        return out
    out[y0:y1, x0:x1] = dmg[y0 - dy:y1 - dy, x0 - dx:x1 - dx]
    return out


def main(apply=False):
    man = load_manifest()
    img = man['img']
    os.makedirs(BACKUP, exist_ok=True)
    report = []
    total_px = 0
    total_files = 0

    for fam, bc in BOLT.items():
        keys = sorted(k for k in img if k.startswith(fam + '_'))
        # group section -> {state: key} so damage states can be re-canvassed
        sect_states = {}
        for k in keys:
            m = re.match(rf'^{fam}_(.+)_(intact|damaged|critical|destroyed)$', k)
            if m:
                sect_states.setdefault(m.group(1), {})[m.group(2)] = k

        for k in keys:
            p = os.path.join(ROOT, img[k])
            if not os.path.exists(p):
                continue
            rgba = np.array(Image.open(p).convert('RGBA'))
            cleaned, n = declackle(rgba, bc)
            if n == 0:
                continue
            total_px += n
            total_files += 1
            report.append((k, n, rgba.shape[1::-1], None))
            if apply:
                rel = img[k]
                bp = os.path.join(BACKUP, rel.replace('/', '__'))
                if not os.path.exists(bp):
                    shutil.copy2(p, bp)
                Image.fromarray(cleaned).save(p)

    print(f"crackle: {total_px} px across {total_files} files")
    if not apply:
        print("DRY RUN — pass --apply to write")
        return

    # ---- second pass: measure placement, AFTER the bolts are gone, because the
    # bolts are exactly what made the silhouettes disagree in the first place.
    base_off = json.load(open(os.path.join(ROOT, 'assets/section_base_offsets.json')))
    table, weak = {}, []
    for fam, bc in BOLT.items():
        keys = sorted(k for k in img if k.startswith(fam + '_'))
        sect_states = {}
        for k in keys:
            m = re.match(rf'^{fam}_(.+)_(intact|damaged|critical|destroyed)$', k)
            if m:
                sect_states.setdefault(m.group(1), {})[m.group(2)] = k
        table[fam] = {}
        for sect, st in sect_states.items():
            if 'intact' not in st or sect not in base_off.get(fam, {}):
                continue
            bx, by = base_off[fam][sect]
            base = np.array(Image.open(os.path.join(ROOT, img[st['intact']])).convert('RGBA'))
            table[fam][sect] = {'intact': [bx, by]}
            for state in ('damaged', 'critical', 'destroyed'):
                if state not in st:
                    continue
                cur = np.array(Image.open(os.path.join(ROOT, img[st[state]])).convert('RGBA'))
                if cur.shape[:2] == base.shape[:2]:
                    table[fam][sect][state] = [bx, by]
                    continue
                dx, dy, score = align_offset(cur, base)
                table[fam][sect][state] = [bx + dx, by + dy]
                if score < 0.75:
                    weak.append((f'{fam}_{sect}_{state}', round(score, 3)))
    with open(os.path.join(ROOT, 'assets/section_offsets.json'), 'w') as f:
        json.dump(table, f, indent=1, sort_keys=True)
    n = sum(len(v) for v in table.values())
    print(f"placement table: {n} sections across {len(table)} families "
          f"-> assets/section_offsets.json")
    if weak:
        print(f"low-confidence alignments ({len(weak)}) — flagged, not trusted blindly:")
        for k, s in sorted(weak, key=lambda x: x[1])[:10]:
            print(f"   {k:44s} score={s}")
    print("APPLIED")


if __name__ == '__main__':
    main('--apply' in sys.argv)
