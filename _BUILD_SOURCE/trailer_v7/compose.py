"""compose.py - render the Bullets of Fury trailer from an EDL at 1920x1080, 60 fps.

    python compose.py edl.json video.mp4 [--workers 8] [--start F --end F]
    python compose.py edl.json board.jpg --board 90          # storyboard: one frame every 90

AN EDL is JSON: {"clips": [...], "overlays": [...], "hits": [...]} on a frame-exact 60 fps clock.

  clip    {"t0": s, "t1": s, "panes": [pane, ...], "layers": [layer, ...],
           "fade_in": s, "fade_out": s, "letterbox": px, "grade": {"sat": 1.2, "con": 1.1}}
  pane    {"rect": [x, y, w, h], "take": "B_yuri", "src": frame, "speed": 1.0, "hold": s|null,
           "cam": {"s0": 1.0, "s1": 2.0, "ease": "out", "cx": 480, "cy": 700,
                   "track": "player"|"target"|null, "lead": 0},
           "bg": "blur"|"black", "desat": 0..1, "tint": [r, g, b, a], "border": [r, g, b]}
  layer   {"kind": "image"|"text", "src": "brand/nbl_logo.png", "text": "...", "face": "2", "height": 150,
           "x": 960, "y": 540, "anchor": "c", "scale": 1.0, "t_in": s, "t_out": s,
           "in": "cut"|"slam"|"fade"|"slide-l"|"slide-r"|"rise", "out": "cut"|"fade", "drift": 0.0,
           "shadow": true, "resample": "nearest"|"lanczos"}
  hit     {"t": s, "kind": "flash"|"punch"|"shake"|"rgb"|"black", "dur": s, "amp": x}

Layer times are absolute trailer seconds, so a title can outlive the cut beneath it; overlays are
layers that belong to no clip. Hits are global for the same reason - a beat accent lands on the
music, not on whichever shot happens to be under it.

THE PLAYFIELD IS 960x1024 (the game's SS=2 backing store), and a pane is a camera onto it: scale s
maps s screen pixels to one playfield pixel. s=1 is the whole cabinet, 1:1 and razor sharp, with
the blurred frame filling the sides; s=2 is a full-bleed 16:9 punch-in that doubles every pixel with
nearest-neighbour so the art stays pixel art. In-between scales exist only while a zoom is moving,
where bilinear softness reads as motion rather than blur.

Every output frame is a pure function of its frame number - no state carried between frames, no
random numbers - so a sub-range render is bit-identical to the same frames of a full render. That
is what lets the timeline be split across processes and the H.264 segments joined with -c copy.
"""
import os, sys, json, math, time, argparse, subprocess
from collections import OrderedDict
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1920, 1080, 60
PF_W, PF_H = 960, 1024
TAKES_SUBDIR = os.environ.get('BOF_TAKES', 'takes3')     # v2 cut from 'takes'; v3 from the sound-logged library


def ffmpeg_exe():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def ease(k, kind='out'):
    k = min(1.0, max(0.0, k))
    if kind == 'out':
        return 1 - (1 - k) ** 3
    if kind == 'in':
        return k ** 3
    if kind == 'inout':
        return k * k * (3 - 2 * k)
    return k


def lerp(a, b, k):
    return a + (b - a) * k


class Takes:
    """lazy JPEG frames with an LRU, plus per-take metrics and smoothed camera tracks"""

    def __init__(self, cap=96):
        self.cache, self.cap, self._meta, self._tracks = OrderedDict(), cap, {}, {}

    def meta(self, tid):
        if tid not in self._meta:
            d = os.path.join(HERE, TAKES_SUBDIR, tid)
            m = json.load(open(os.path.join(d, 'meta.json')))
            m['metrics'] = json.load(open(os.path.join(d, 'metrics.json')))
            self._meta[tid] = m
        return self._meta[tid]

    def n(self, tid):
        return self.meta(tid)['frames']

    def frame(self, tid, i):
        i = max(0, min(self.n(tid) - 1, int(i)))
        key = (tid, i)
        im = self.cache.get(key)
        if im is not None:
            self.cache.move_to_end(key)
            return im
        im = Image.open(os.path.join(HERE, TAKES_SUBDIR, tid, 's%05d.jpg' % i))
        im.load()
        im = im.convert('RGB')
        self.cache[key] = im
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)
        return im

    def track(self, tid, what):
        """playfield-pixel (x, y) per frame for the player or the live target, smoothed over 1/2 s
        either side so a camera that follows it glides instead of twitching with every dodge"""
        key = (tid, what)
        if key in self._tracks:
            return self._tracks[key]
        M = self.meta(tid)['metrics']
        xs, ys = [], []
        for m in M:
            if what == 'target' and m.get('ty') is not None:
                x, y = m.get('tsx', PF_W / 2), m['ty'] * 2
            else:
                x = (m['px'] - m['cx']) * 2 if m.get('cx') is not None else PF_W / 2
                y = m['py'] * 2
            xs.append(x)
            ys.append(y)
        xs, ys = np.array(xs, float), np.array(ys, float)
        k = 31
        pad = lambda a: np.concatenate([np.full(k, a[0]), a, np.full(k, a[-1])])
        ker = np.ones(k) / k
        sx = np.convolve(pad(xs), ker, 'same')[k:-k]
        sy = np.convolve(pad(ys), ker, 'same')[k:-k]
        self._tracks[key] = (sx, sy)
        return self._tracks[key]


class Assets:
    def __init__(self):
        self.cache = {}

    def image(self, L):
        if L.get('kind') == 'text':
            key = ('t', L['text'], str(L.get('face', 'final')), int(L.get('height', 120)),
                   float(L.get('tracking', 0.05)), bool(L.get('shadow', True)), L.get('tint'), float(L.get('tint_a', 1.0)))
        else:
            key = ('i', L['src'], bool(L.get('shadow', False)), float(L.get('prescale', 1.0)), L.get('resample', 'lanczos'))
        if key in self.cache:
            return self.cache[key]
        if L.get('kind') == 'text':
            sys.path.insert(0, HERE)
            from typeset import text
            im = text(L['text'], face=str(L.get('face', 'final')), height=int(L.get('height', 120)),
                      tracking=float(L.get('tracking', 0.05)), tint=L.get('tint'), tint_a=float(L.get('tint_a', 1.0)))
        else:
            im = Image.open(os.path.join(HERE, L['src'])).convert('RGBA')
            ps = float(L.get('prescale', 1.0))
            if ps != 1.0:
                rs = Image.NEAREST if L.get('resample') == 'nearest' else Image.LANCZOS
                im = im.resize((max(1, int(im.width * ps)), max(1, int(im.height * ps))), rs)
        if L.get('shadow', L.get('kind') == 'text'):
            pad = max(8, im.height // 10)
            big = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
            a = Image.new('L', big.size, 0)
            a.paste(im.getchannel('A'), (pad, pad + max(2, im.height // 40)))
            a = a.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(max(2, im.height // 30)))
            sh = Image.new('RGBA', big.size, (0, 0, 0, 0))
            sh.putalpha(a.point(lambda v: min(255, int(v * 0.9))))
            big.alpha_composite(sh)
            big.alpha_composite(im, (pad, pad))
            im = big
        self.cache[key] = im
        return im


VIGNETTE = None


def vignette():
    global VIGNETTE
    if VIGNETTE is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        VIGNETTE = np.clip(1.08 - 0.32 * r ** 2, 0.55, 1.0)[..., None]
    return VIGNETTE


def blur_cover(im, w, h, dark=0.42):
    sc = max(w / im.width, h / im.height)
    small = im.resize((max(1, im.width // 12), max(1, im.height // 12)), Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.5))
    big = small.resize((int(math.ceil(im.width * sc)), int(math.ceil(im.height * sc))), Image.BILINEAR)
    x0, y0 = (big.width - w) // 2, (big.height - h) // 2
    big = big.crop((x0, y0, x0 + w, y0 + h))
    return Image.eval(big, lambda v: int(v * dark))


def render_pane(canvas, clip, pane, f, T):
    x, y, w, h = [int(v) for v in pane['rect']]
    f0, f1 = clip['_f0'], clip['_f1']
    rel = f - f0
    tid = pane['take']
    speed = float(pane.get('speed', 1.0))
    if pane.get('hold') is not None and rel >= pane['hold'] * FPS:
        rel = int(pane['hold'] * FPS)
    i = int(pane.get('src', 0) + rel * speed)
    im = T.frame(tid, i)
    cam = pane.get('cam', {})
    k = ease(rel / float(max(1, f1 - f0 - 1)), cam.get('ease', 'out'))
    s = lerp(float(cam.get('s0', 1.0)), float(cam.get('s1', cam.get('s0', 1.0))), k)
    cx, cy = float(cam.get('cx', PF_W / 2)), float(cam.get('cy', PF_H / 2))
    if cam.get('track'):
        sx, sy = T.track(tid, cam['track'])
        j = max(0, min(len(sx) - 1, i))
        cx = float(sx[j]) if cam.get('track_x') else cx
        cy = float(sy[j]) + float(cam.get('lead', 0))
    vw, vh = w / s, h / s
    cx = min(max(cx, vw / 2), PF_W - vw / 2) if vw <= PF_W else PF_W / 2
    cy = min(max(cy, vh / 2), PF_H - vh / 2) if vh <= PF_H else PF_H / 2
    x0, y0 = cx - vw / 2, cy - vh / 2
    ix0, iy0 = max(0.0, x0), max(0.0, y0)
    ix1, iy1 = min(float(PF_W), x0 + vw), min(float(PF_H), y0 + vh)
    if pane.get('bg', 'blur') == 'blur' and (x0 < 0 or y0 < 0 or x0 + vw > PF_W or y0 + vh > PF_H):
        pc = blur_cover(im, w, h)
    else:
        pc = Image.new('RGB', (w, h), (0, 0, 0))
    box = (int(round(ix0)), int(round(iy0)), int(round(ix1)), int(round(iy1)))
    region = im.crop(box)
    dw, dh = int(round((box[2] - box[0]) * s)), int(round((box[3] - box[1]) * s))
    integer = abs(s - round(s)) < 1e-3
    region = region.resize((max(1, dw), max(1, dh)), Image.NEAREST if integer else Image.BILINEAR)
    pc.paste(region, (int(round((box[0] - x0) * s)), int(round((box[1] - y0) * s))))
    if pane.get('desat') or pane.get('tint'):
        a = np.asarray(pc).astype(np.float32)
        if pane.get('desat'):
            g = (a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114)[..., None]
            a = lerp(a, np.repeat(g, 3, axis=2), float(pane['desat']))
        if pane.get('tint'):
            r, gg, b, al = pane['tint']
            a = a * (1 - al) + np.array([r, gg, b], np.float32) * al * (a / 255.0 + 0.35)
        pc = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    canvas.paste(pc, (x, y))
    if pane.get('border'):
        bc = tuple(pane['border'])
        canvas.paste(Image.new('RGB', (w, 4), bc), (x, y))
        canvas.paste(Image.new('RGB', (w, 4), bc), (x, y + h - 4))
        canvas.paste(Image.new('RGB', (4, h), bc), (x, y))
        canvas.paste(Image.new('RGB', (4, h), bc), (x + w - 4, y))


def render_layer(canvas, L, t, A):
    if t < L['t_in'] or t >= L['t_out']:
        return
    img = A.image(L)
    a_in, a_out = t - L['t_in'], L['t_out'] - t
    scale, alpha, ox, oy = float(L.get('scale', 1.0)), 1.0, 0.0, 0.0
    kin = L.get('in', 'cut')
    if kin == 'slam':
        kk = ease(a_in / 0.16)
        scale *= 1 + 1.1 * (1 - kk)
        alpha = min(1.0, a_in / 0.05)
    elif kin == 'fade':
        alpha = min(1.0, a_in / float(L.get('fade', 0.25)))
    elif kin in ('slide-l', 'slide-r'):
        kk = ease(a_in / 0.22)
        ox = (-1 if kin == 'slide-l' else 1) * (1 - kk) * W * 0.55
    elif kin == 'rise':
        kk = ease(a_in / 0.3)
        oy = (1 - kk) * 120
        alpha = kk
    if L.get('out') == 'fade':
        alpha *= min(1.0, a_out / float(L.get('fade_out', 0.18)))
    scale *= 1 + float(L.get('drift', 0.0)) * a_in
    if alpha <= 0.003:
        return
    if abs(scale - 1.0) > 1e-3:
        rs = Image.NEAREST if L.get('resample') == 'nearest' else Image.BILINEAR
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), rs)
    if alpha < 0.999:
        img = img.copy()
        img.putalpha(img.getchannel('A').point(lambda v: int(v * alpha)))
    anc = L.get('anchor', 'c')
    px, py = float(L.get('x', W / 2)) + ox, float(L.get('y', H / 2)) + oy
    if 'c' in anc or anc in ('t', 'b'):
        px -= img.width / 2
    if anc.endswith('r') or anc == 'r':
        px -= img.width
    if anc in ('c', 'l', 'r'):
        py -= img.height / 2
    if anc.startswith('b'):
        py -= img.height
    if L.get('band'):
        # a soft full-width dark band behind the lettering: the molten face vanished into stage 2's
        # lava in the first test board, and a drop shadow alone cannot separate texture from texture
        pad = int(img.height * 0.3)
        y0 = int(round(py)) - pad
        m = band_mask(img.height + 2 * pad, float(L['band']) * alpha)
        top = max(0, y0)
        bot = min(H, y0 + m.height)
        if bot > top:
            canvas.paste((0, 0, 0), (0, top, W, bot), m.crop((0, top - y0, W, bot - y0)))
    canvas.paste(img, (int(round(px)), int(round(py))), img)


BANDS = {}


def band_mask(h, a):
    key = (h, round(a, 2))
    if key not in BANDS:
        ys = np.linspace(-1.0, 1.0, h)
        prof = np.clip(1.0 - np.abs(ys) ** 4, 0.0, 1.0) * a * 255.0
        BANDS[key] = Image.fromarray(np.repeat(prof[:, None], W, axis=1).astype(np.uint8), 'L')
    return BANDS[key]


def apply_hits(arr, f, hits):
    t = f / FPS
    fx = {'flash': 0.0, 'punch': 0.0, 'shake': 0.0, 'rgb': 0.0, 'black': 0.0}
    for h in hits:
        dt = t - h['t']
        if 0 <= dt < h['dur']:
            k = 1 - dt / h['dur']
            v = float(h.get('amp', 1.0)) * (k if h['kind'] != 'black' else 1.0)
            fx[h['kind']] = max(fx[h['kind']], v)
    if fx['punch'] > 0:
        s = 1 + fx['punch']
        cw, ch = int(W / s), int(H / s)
        im = Image.fromarray(arr).crop(((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw, (H - ch) // 2 + ch))
        arr = np.array(im.resize((W, H), Image.BILINEAR))
    if fx['shake'] > 0:
        a = fx['shake']
        dx = int(round(a * math.sin(f * 2.39 + 0.7)))
        dy = int(round(a * 0.6 * math.cos(f * 3.17 + 0.2)))
        arr = np.roll(arr, (dy, dx), axis=(0, 1))
    if fx['rgb'] >= 1:
        k = int(round(fx['rgb']))
        arr = arr.copy()
        arr[..., 0] = np.roll(arr[..., 0], -k, axis=1)
        arr[..., 2] = np.roll(arr[..., 2], k, axis=1)
    if fx['flash'] > 0:
        a = min(1.0, fx['flash'])
        arr = (arr.astype(np.uint16) * int((1 - a) * 256) // 256 + int(255 * a)).astype(np.uint8)
    if fx['black'] > 0:
        a = min(1.0, fx['black'])
        arr = (arr.astype(np.uint16) * int((1 - a) * 256) // 256).astype(np.uint8)
    return arr


def load_edl(path):
    E = json.load(open(path))
    for c in E['clips']:
        c['_f0'], c['_f1'] = int(round(c['t0'] * FPS)), int(round(c['t1'] * FPS))
    E.setdefault('overlays', [])
    E.setdefault('hits', [])
    E['_frames'] = max([c['_f1'] for c in E['clips']] + [int(round(L['t_out'] * FPS)) for L in E['overlays']] + [0])
    return E


def render_frame(E, f, T, A):
    t = f / FPS
    canvas = Image.new('RGB', (W, H), (0, 0, 0))
    for c in E['clips']:
        if not (c['_f0'] <= f < c['_f1']):
            continue
        for p in c.get('panes', []):
            render_pane(canvas, c, p, f, T)
        g = c.get('grade')
        if g or c.get('vignette'):
            a = np.asarray(canvas).astype(np.float32)
            if g:
                mean = a.mean(axis=(0, 1), keepdims=True)
                a = (a - mean) * float(g.get('con', 1.0)) + mean
                gray = a.mean(axis=2, keepdims=True)
                a = gray + (a - gray) * float(g.get('sat', 1.0))
            if c.get('vignette'):
                a = a * vignette()
            canvas = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        for L in c.get('layers', []):
            render_layer(canvas, L, t, A)
        lb = int(c.get('letterbox', 0))
        if lb:
            canvas.paste(Image.new('RGB', (W, lb), (0, 0, 0)), (0, 0))
            canvas.paste(Image.new('RGB', (W, lb), (0, 0, 0)), (0, H - lb))
        fi, fo = float(c.get('fade_in', 0)), float(c.get('fade_out', 0))
        k = 1.0
        if fi > 0:
            k = min(k, (f - c['_f0']) / (fi * FPS))
        if fo > 0:
            k = min(k, (c['_f1'] - 1 - f) / (fo * FPS))
        if k < 1.0:
            canvas = Image.eval(canvas, lambda v, k=max(0.0, k): int(v * k))
    for L in E['overlays']:
        render_layer(canvas, L, t, A)
    return apply_hits(np.array(canvas), f, E['hits'])


def encode_range(edl_path, out_path, a, b, threads=3):
    E = load_edl(edl_path)
    T, A = Takes(), Assets()
    cmd = [ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H),
           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
           '-threads', str(threads), '-x264-params', 'keyint=120:min-keyint=1', out_path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    for f in range(a, b):
        p.stdin.write(render_frame(E, f, T, A).tobytes())
    p.stdin.close()
    p.wait()
    print('segment %d-%d: %.1f s (%.1f ms/frame)' % (a, b, time.time() - t0, 1000 * (time.time() - t0) / max(1, b - a)), flush=True)


def board(edl_path, out_path, every):
    E = load_edl(edl_path)
    T, A = Takes(), Assets()
    frames = list(range(0, E['_frames'], every))
    tw, th, cols = 384, 216, 6
    S = Image.new('RGB', (tw * cols, (th + 16) * ((len(frames) + cols - 1) // cols)), (8, 8, 10))
    from PIL import ImageDraw
    d = ImageDraw.Draw(S)
    for k, f in enumerate(frames):
        im = Image.fromarray(render_frame(E, f, T, A)).resize((tw, th), Image.BILINEAR)
        x, y = (k % cols) * tw, (k // cols) * (th + 16)
        S.paste(im, (x, y + 16))
        d.text((x + 3, y + 2), 'f%d  %.2fs' % (f, f / FPS), fill=(255, 220, 140))
    S.save(out_path, quality=90)
    print('wrote %s (%d frames)' % (out_path, len(frames)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('edl')
    ap.add_argument('out')
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--end', type=int, default=-1)
    ap.add_argument('--board', type=int, default=0)
    ap.add_argument('--segment', nargs=2, type=int, help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.board:
        return board(a.edl, a.out, a.board)
    if a.segment:
        return encode_range(a.edl, a.out, a.segment[0], a.segment[1])
    E = load_edl(a.edl)
    end = E['_frames'] if a.end < 0 else a.end
    n = end - a.start
    segdir = os.path.join(HERE, 'segments')
    os.makedirs(segdir, exist_ok=True)
    cuts = [a.start + n * k // a.workers for k in range(a.workers + 1)]
    procs, parts = [], []
    t0 = time.time()
    for k in range(a.workers):
        part = os.path.join(segdir, 'seg_%02d.mp4' % k)
        parts.append(part)
        procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), a.edl, part,
                                       '--segment', str(cuts[k]), str(cuts[k + 1])], cwd=HERE))
    codes = [p.wait() for p in procs]
    if any(codes):
        sys.exit('segment failed: %s' % codes)
    lst = os.path.join(segdir, 'list.txt')
    with open(lst, 'w') as fh:
        for part in parts:
            fh.write("file '%s'\n" % part.replace('\\', '/'))
    subprocess.check_call([ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
                           '-c', 'copy', a.out])
    print('wrote %s: %d frames in %.0f s' % (a.out, n, time.time() - t0))


if __name__ == '__main__':
    main()
