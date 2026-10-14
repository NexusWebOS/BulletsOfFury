"""crack11.py - the cracked-screen overlay for the v11 ending (the robot HAMA throws AT THE CAMERA).

    python crack11.py            # writes brand/crack_<n>.png, a 1920x1080 RGBA overlay in 4 growth stages

A post-production effect, not game art: it sits on top of the finished frame like the glass of a monitor. Radial
fractures leave the impact point on jagged paths that fork; spider-web arcs join neighbouring fractures at a few radii;
a crushed core of small shards sits under the impact. Each line is drawn three times - a dark under-stroke (the crack's
shadow in the glass), a bright core and a faint wide glow - so it reads on both the dark logo card and busy footage.
The four stages share one random seed, so stage n+1 is stage n plus more cracks: the glass keeps breaking.
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'brand')
W, H = 1920, 1080


def fractures(cx, cy, rng, n=16):
    paths = []
    for i in range(n):
        a = (i + rng.uniform(-0.35, 0.35)) * math.tau / n
        L = rng.uniform(700, 1500)
        pts, x, y, d = [(cx, cy)], cx, cy, 0
        while d < L:
            step = rng.uniform(26, 70)
            a += rng.uniform(-0.13, 0.13)
            x += math.cos(a) * step; y += math.sin(a) * step; d += step
            pts.append((x, y))
            if rng.random() < 0.12 and d > 120:               # a fork
                b, fx, fy, fd, fp = a + rng.choice([-1, 1]) * rng.uniform(0.35, 0.8), x, y, 0, [(x, y)]
                FL = rng.uniform(120, 420)
                while fd < FL:
                    st = rng.uniform(20, 50); b += rng.uniform(-0.3, 0.3)
                    fx += math.cos(b) * st; fy += math.sin(b) * st; fd += st; fp.append((fx, fy))
                paths.append((fp, d))
        paths.append((pts, 0))
    return paths


def web(main, cx, cy, rng):
    arcs = []
    rads = sorted(rng.uniform(60, 520) for _ in range(5))
    tips = [p for p, d0 in main if d0 == 0]
    for r in rads:
        for i in range(len(tips)):
            if rng.random() < 0.25:
                continue
            A, B = tips[i], tips[(i + 1) % len(tips)]
            pa = min(A, key=lambda p: abs(math.hypot(p[0] - cx, p[1] - cy) - r))
            pb = min(B, key=lambda p: abs(math.hypot(p[0] - cx, p[1] - cy) - r))
            mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
            sag = rng.uniform(0.05, 0.18)
            mx += (cx - mx) * sag; my += (cy - my) * sag
            arcs.append([pa, (mx + rng.uniform(-8, 8), my + rng.uniform(-8, 8)), pb])
    return arcs


def draw(stage, seed=1014, cx=W * 0.52, cy=H * 0.46):
    rng = random.Random(seed)
    main = fractures(cx, cy, rng)
    arcs = web(main, cx, cy, rng)
    frac = [0.35, 0.6, 0.85, 1.0][stage]
    lines = []
    for pts, d0 in main:
        keep = max(2, int(len(pts) * frac))
        lines.append((pts[:keep], 3 if d0 == 0 else 2))
    if stage >= 1:
        k = int(len(arcs) * [0, 0.4, 0.75, 1.0][stage])
        lines += [(a, 2) for a in arcs[:k]]
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    for pts, w in lines:
        g.line(pts, fill=(200, 230, 255, 90), width=w + 8, joint='curve')
    glow = glow.filter(ImageFilter.GaussianBlur(6))
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    im.alpha_composite(glow)
    d = ImageDraw.Draw(im)
    for pts, w in lines:
        d.line([(x + 2, y + 2) for x, y in pts], fill=(0, 0, 0, 200), width=w + 2, joint='curve')
    for pts, w in lines:
        d.line(pts, fill=(245, 250, 255, 255), width=w, joint='curve')
    # the crushed core: little shards around the impact, white faces with dark seams
    for _ in range(26 + stage * 10):
        a, r = rng.uniform(0, math.tau), abs(rng.gauss(0, 34 + stage * 8))
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
        s = rng.uniform(5, 16)
        poly = [(x + math.cos(a + k * 2.1 + rng.uniform(-.4, .4)) * s, y + math.sin(a + k * 2.1 + rng.uniform(-.4, .4)) * s) for k in range(3)]
        d.polygon(poly, fill=(235, 245, 255, rng.randint(120, 220)), outline=(0, 0, 0, 220))
    d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)
    # the bruise: a pale haze in the glass around the impact
    haze = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(haze)
    R = 70 + stage * 25
    hd.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(225, 240, 255, 70))
    haze = haze.filter(ImageFilter.GaussianBlur(R * 0.45))
    haze.alpha_composite(im)
    im = haze
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for s in range(4):
        draw(s).save(os.path.join(OUT, 'crack_%d.png' % s))
    print('crack overlays written')
