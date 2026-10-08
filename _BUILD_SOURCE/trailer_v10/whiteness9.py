"""whiteness9.py - measure, per recorded frame, how much of the boss area is a WHITE SILHOUETTE. Writes
takes9/<id>/white.json (a list of fractions) for the edit's scoring.

    python whiteness9.py B_s3b B_s4m E2_core ...      # or --all for every boss / pilot take

capture9's 'bf' reads the boss object's own flash field, and the modular bosses (Olive Warden, Rime Wall, the
Furnace's shield) flash PER PART, so 'bf' read 0 on frames where the hull was plainly white - the final stills of the
first render showed it. This reads the pixels instead: the share of bright, desaturated pixels (min channel > 196,
spread < 34) in the upper 60% of the playfield, where bosses live. The edit subtracts each take's own median so an
ice stage's snow is not scored as a flash.
"""
import os, sys, json
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TAKES = os.path.join(HERE, 'takes10')
PREFIX = ('B_', 'P_', 'V_', 'Z_', 'S6', 'M_', 'G_', 'X_')


def measure(tid):
    d = os.path.join(TAKES, tid)
    n = json.load(open(os.path.join(d, 'meta.json')))['frames']
    out = []
    for i in range(n):
        im = Image.open(os.path.join(d, 's%05d.jpg' % i))
        im.draft('RGB', (240, 256))                 # JPEG DCT scaling: decodes at 1/4 size, fast
        a = np.asarray(im.convert('RGB'), dtype=np.int16)
        a = a[: int(a.shape[0] * 0.6)]
        mn = a.min(axis=2)
        mx = a.max(axis=2)
        w = ((mn > 196) & ((mx - mn) < 34)).mean()
        out.append(round(float(w), 4))
    json.dump(out, open(os.path.join(d, 'white.json'), 'w'))
    return out


def main():
    ids = sys.argv[1:]
    if not ids or ids == ['--all']:
        ids = sorted(t for t in os.listdir(TAKES) if t.startswith(PREFIX) and os.path.exists(os.path.join(TAKES, t, 'meta.json')))
    for tid in ids:
        w = measure(tid)
        med = float(np.median(w)) if w else 0.0
        print('%-14s %5d frames  median %.3f  p90 %.3f  max %.3f' % (tid, len(w), med, float(np.percentile(w, 90)) if w else 0, max(w) if w else 0), flush=True)


if __name__ == '__main__':
    main()
