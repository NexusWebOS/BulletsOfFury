"""Per-frame QA over the projectile gallery films.

    python _BUILD_SOURCE/audit_projectile_frames_1103.py [--sheet]

Reads _shots/projectiles_1103/{before,after}/catalog.json + strips and flags, per clip:
  bleed     a small flat strip detached from the round that recurs: a neighbouring sheet cell cut into
  cut       a straight edge sliced through the round's own body: the source rect is too small
  pump      the body's pixel area swings (size animation where the art should hold its size)
  hueflip   the body's colour family changes between frames (e.g. a red needle turning blue)
  blank     an empty frame between lit ones (a missing/transparent reel cell)
  pop       area jumps 2x frame-to-frame (an extra/odd cell in the reel)
  crop      lit pixels on the capture border: the gallery crop is too small for this round
  mismatch  (after vs before) the body itself changed colour or size: the pass altered the art
Writes _shots/projectiles_1103/audit/report.json and, with --sheet, one contact sheet per flag.
"""
from pathlib import Path
import json, sys, colorsys, argparse
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

R = Path(__file__).resolve().parents[1]; G = R / '_shots/projectiles_1103'
A = argparse.ArgumentParser(); A.add_argument('--sheet', action='store_true'); A.add_argument('--tags', default='before,after')
args = A.parse_args()
F = 256  # frame px (128 game px at SS=2)
OUT = G / 'audit'; OUT.mkdir(exist_ok=True)

def frames(tag, it):
    im = np.asarray(Image.open(G / tag / it['file']).convert('RGB'))
    return [im[:, i * F:(i + 1) * F] for i in range(it['frames'])]

def body(fr, thr=70):
    """largest solid component of the round (glow rings and faint trails excluded by threshold)"""
    lit = fr.max(axis=2) > thr
    lab, n = ndimage.label(lit, structure=np.ones((3, 3)))
    if not n: return None, lab, n, lit
    sizes = ndimage.sum(lit, lab, range(1, n + 1))
    k = int(np.argmax(sizes)) + 1
    return k, lab, n, lit

def hue_of(fr, mask):
    px = fr[mask].astype(float) / 255
    if not len(px): return None, 0
    sat = px.max(1) - px.min(1); keep = sat > .18
    if keep.sum() < 4: return None, float(px.max(1).mean())
    r, g, b = px[keep].mean(0); h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h * 360, s

def family(h):
    if h is None: return 'neutral'
    for name, lo, hi in [('red', 0, 20), ('orange', 20, 45), ('yellow', 45, 70), ('green', 70, 160), ('cyan', 160, 200), ('blue', 200, 255), ('violet', 255, 295), ('pink', 295, 340), ('red', 340, 361)]:
        if lo <= h < hi: return name
    return 'neutral'

def analyse(tag, it):
    fl = {}; fs = frames(tag, it); areas = []; hues = []; lits = []; bleed_hits = 0; cut_hits = 0; crop_hits = 0
    for fr in fs:
        k, lab, n, lit = body(fr)
        lits.append(int(lit.sum()))
        border = np.concatenate([lit[0], lit[-1], lit[:, 0], lit[:, -1]]).sum()
        if border > 6: crop_hits += 1
        if k is None: areas.append(0); hues.append(None); continue
        m = lab == k; areas.append(int(m.sum())); hues.append(hue_of(fr, m)[0])
        ys, xs = np.nonzero(m); by0, by1, bx0, bx1 = ys.min(), ys.max(), xs.min(), xs.max()
        # bleed: other components that are flat strips near the body
        found = False
        for j in range(1, n + 1):
            if j == k: continue
            mj = lab == j; a = int(mj.sum())
            if a < 6: continue
            yy, xx = np.nonzero(mj); h = yy.max() - yy.min() + 1; w = xx.max() - xx.min() + 1
            flat = (h <= 7 and w >= 6 and w >= 2.2 * h) or (w <= 7 and h >= 6 and h >= 2.2 * w)
            near = (yy.min() <= by1 + 30 and yy.max() >= by0 - 30 and xx.min() <= bx1 + 30 and xx.max() >= bx0 - 30)
            if flat and near and a < areas[-1] * .5: found = True; break
        if found: bleed_hits += 1
        # cut: a long perfectly straight row/column run on the body's own boundary
        rows = m.sum(1); cols = m.sum(0)
        for line in (rows[by0], rows[by1], cols[bx0], cols[bx1]):
            span = max(bx1 - bx0, by1 - by0) + 1
            if line >= 10 and line >= .55 * span and span >= 18: cut_hits += 1; break
    N = len(fs); lit_frames = [a for a in areas if a > 0]
    if bleed_hits >= max(3, N * .4): fl['bleed'] = bleed_hits
    if cut_hits >= max(3, N * .5): fl['cut'] = cut_hits
    if crop_hits >= max(2, N * .25): fl['crop'] = crop_hits
    if len(lit_frames) >= 4:
        lo, hi, med = min(lit_frames), max(lit_frames), float(np.median(lit_frames))
        if med > 40 and hi / max(1, lo) > 1.6: fl['pump'] = round(hi / max(1, lo), 2)
        jumps = sum(1 for a, b in zip(lit_frames, lit_frames[1:]) if min(a, b) > 0 and max(a, b) / min(a, b) > 2.2)
        if jumps >= 2: fl['pop'] = jumps
        fams = [family(h) for h in hues if h is not None]
        if len(fams) >= 4:
            from collections import Counter
            c = Counter(fams); top, cnt = c.most_common(1)[0]
            odd = [f for f in fams if f != top and f != 'neutral']
            adj = {'red': {'orange', 'pink'}, 'orange': {'red', 'yellow'}, 'yellow': {'orange', 'green'}, 'green': {'yellow', 'cyan'},
                   'cyan': {'green', 'blue'}, 'blue': {'cyan', 'violet'}, 'violet': {'blue', 'pink'}, 'pink': {'violet', 'red'}}
            far = [f for f in odd if f not in adj.get(top, set())]
            if len(far) >= 2: fl['hueflip'] = f"{top}->{sorted(set(far))} x{len(far)}"
    first = next((i for i, a in enumerate(areas) if a), None); last = max((i for i, a in enumerate(areas) if a), default=None)
    if first is not None:
        holes = sum(1 for a in areas[first:last + 1] if a == 0)
        if holes: fl['blank'] = holes
    return fl, dict(areas=areas, hues=[None if h is None else round(h) for h in hues])

cat = {t: {i['sig']: i for i in json.load(open(G / t / 'catalog.json'))['items']} for t in args.tags.split(',')}
report = {}
for tag, items in cat.items():
    for sig, it in items.items():
        fl, info = analyse(tag, it)
        report.setdefault(sig, {'kind': it['kind'], 'enc': it['enc'], 'art': it.get('art')})[tag] = {'flags': fl, **info, 'file': it['file']}
# before -> after body mismatch: compare the body's colour family and median area
if 'before' in cat and 'after' in cat:
    for sig, r in report.items():
        if 'before' not in r or 'after' not in r: continue
        b, a = r['before'], r['after']
        ab = [x for x in b['areas'] if x]; aa = [x for x in a['areas'] if x]
        if not ab or not aa: continue
        fb = [family(h) for h in b['hues'] if h is not None]; fa = [family(h) for h in a['hues'] if h is not None]
        from collections import Counter
        tb = Counter(fb).most_common(1)[0][0] if fb else 'neutral'; ta = Counter(fa).most_common(1)[0][0] if fa else 'neutral'
        ratio = float(np.median(aa)) / max(1, float(np.median(ab)))
        if (tb != ta and 'neutral' not in (tb, ta)) or ratio < .55 or ratio > 1.9:
            a['flags']['mismatch'] = f"{tb}->{ta} area x{ratio:.2f}"
(OUT / 'report.json').write_text(json.dumps(report, indent=1))
from collections import Counter
summary = {t: Counter(f for r in report.values() if t in r for f in r[t]['flags']) for t in cat}
print(json.dumps(summary))
if args.sheet:
    for flag in ['bleed', 'cut', 'pump', 'hueflip', 'blank', 'pop', 'crop', 'mismatch']:
        rows = [(s, r) for s, r in report.items() for t in ['before', 'after'] if t in r and flag in r[t]['flags'] and (t == 'before' or flag == 'mismatch' or flag not in r.get('before', {}).get('flags', {}))]
        seen = set(); rows = [x for x in rows if not (x[0] in seen or seen.add(x[0]))][:40]
        if not rows: continue
        sheet = Image.new('RGB', (10 + 12 * 100, len(rows) * 112), (28, 30, 40)); d = ImageDraw.Draw(sheet)
        for y, (s, r) in enumerate(rows):
            for col, t in enumerate(['before', 'after']):
                if t not in r: continue
                im = Image.open(G / t / r[t]['file']).convert('RGB'); n = im.width // F
                for k in range(6):
                    f = min(n - 1, k * max(1, n // 6)); c = im.crop((f * F + 28, 28, f * F + 228, 228)).resize((100, 100), Image.NEAREST)
                    sheet.paste(c, (col * 610 + k * 100, y * 112 + 10))
            d.text((2, y * 112), s[:90] + '  ' + str(r.get('before', {}).get('flags', '')) + ' | ' + str(r.get('after', {}).get('flags', '')), fill=(240, 220, 120))
        sheet.save(OUT / f'{flag}.png')
        print('sheet', flag, len(rows))
