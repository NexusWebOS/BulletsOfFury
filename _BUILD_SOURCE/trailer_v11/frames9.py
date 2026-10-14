"""frames9.py - render chosen trailer frames from an EDL with compose.py's own renderer, as a contact sheet.

    python frames9.py edl9.json out.jpg 115.2 117.5 118.6 126.4 130.0          # trailer seconds
    python frames9.py edl9.json out.jpg --every 2.0 --from 60 --to 90            # a range
"""
import os, sys, argparse
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compose   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('edl')
    ap.add_argument('out')
    ap.add_argument('times', nargs='*', type=float)
    ap.add_argument('--every', type=float, default=0)
    ap.add_argument('--from', dest='t_from', type=float, default=0)
    ap.add_argument('--to', dest='t_to', type=float, default=0)
    ap.add_argument('--cols', type=int, default=4)
    ap.add_argument('--w', type=int, default=480)
    a = ap.parse_args()
    E = compose.load_edl(a.edl)
    T, A = compose.Takes(), compose.Assets()
    times = list(a.times)
    if a.every:
        t = a.t_from
        while t < (a.t_to or E['_frames'] / 60.0):
            times.append(round(t, 3))
            t += a.every
    tw = a.w
    th = tw * 9 // 16
    cols = min(a.cols, max(1, len(times)))
    rows = (len(times) + cols - 1) // cols
    S = Image.new('RGB', (tw * cols, (th + 16) * rows), (8, 8, 10))
    d = ImageDraw.Draw(S)
    for k, t in enumerate(times):
        f = int(round(t * 60))
        im = Image.fromarray(compose.render_frame(E, f, T, A)).resize((tw, th), Image.BILINEAR)
        x, y = (k % cols) * tw, (k // cols) * (th + 16)
        S.paste(im, (x, y + 16))
        d.text((x + 3, y + 2), '%.2fs f%d' % (t, f), fill=(255, 220, 140))
    S.save(a.out, quality=90)
    print('wrote', a.out, len(times), 'frames')


if __name__ == '__main__':
    main()
