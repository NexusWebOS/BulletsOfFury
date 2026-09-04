"""
redraw_emr_missiles_0904c.py - redraw the four mfx_emr_0 enemy missiles, authored FOR the
downscale the game actually performs.

Mike, 0904: "your gonna wanna re-do these missiles too to get cleaner and better results"

⚠ THE "WEIRD PIXELATION" IS A RESAMPLING DEFECT, NOT (ONLY) AN ART DEFECT. Measured:

    key            source   drawn at   downscale
    mfx_emr_0_0    16x44    h:20       2.20x
    mfx_emr_0_1    19x44    h:20       2.20x
    mfx_emr_0_2    25x52    h:20       2.60x
    mfx_emr_0_3    29x52    h:20       2.60x

  and this game renders with ctx.imageSmoothingEnabled=false - "nearest-neighbour, per the
  contract" (game.js:3714). A 2.2x NEAREST reduction keeps source rows 0,2,4,7,9,11,13,16... -
  it DROPS rows unevenly, so one-pixel details survive or vanish depending on where they sit, and
  they change as the sprite moves. That is the shimmer. No amount of detail in a 52px source
  survives being sampled down to 20 rows; extra detail actively makes it worse.

  So these are authored at the EXISTING cell sizes (no atlas repack, no manifest change) but with
  every feature >=2px thick and the silhouette carrying the read, and the generator SIMULATES the
  exact nearest-neighbour reduction the engine will do so the 20px result is what gets judged.

⚠ WHY NOT SPRITECOOK. Generated art comes back photoreal and heavily dithered (a 128px character
  sheet measured 76k distinct colours). Reduced to 9x20 by nearest-neighbour that is mush. Hand
  placement wins below ~32px; SpriteCook earns its keep on big art, not on a 20px bullet.

House style, matched from the surrounding atlas: 1px BLACK outline round the whole silhouette,
binary alpha only (0 or 255 - the atlas has zero partial-alpha pixels), bright core reading
against a dark stage.
"""
import io, os, re, sys, shutil, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS_DIR = os.path.join(ROOT, 'assets', 'game', 'atlas')
DRAW_H = 20                      # FIRETYPES.missile / .laser both draw at h:20

# per-stage colour families, matching EMR_GLOW in game.js: red, green, blue, purple
RAMPS = {
    0: dict(name='red',    dark=(88, 16, 20),  mid=(198, 40, 42),  lite=(255, 107, 90),  hot=(255, 214, 198)),
    1: dict(name='green',  dark=(18, 66, 30),  mid=(46, 158, 58),  lite=(143, 255, 159), hot=(224, 255, 228)),
    2: dict(name='blue',   dark=(20, 44, 86),  mid=(46, 107, 190), lite=(127, 176, 255), hot=(219, 236, 255)),
    3: dict(name='purple', dark=(46, 20, 78),  dark2=(70, 30, 110), mid=(122, 62, 198),
            lite=(196, 107, 255), hot=(238, 216, 255)),
}
BLACK = (12, 10, 14, 255)


def draw_missile(w, h, ramp):
    """A missile pointing UP in a w x h cell.

    ⚠ FIRST CUT CAME BACK AS A PILL. A dome nose, fins hidden inside the body silhouette and a fat
       white exhaust read as a coloured capsule, not ordnance - cleaner than the original but
       WORSE, because at 7-11px wide the SILHOUETTE is the only thing that survives the reduction.
       So: a pointed cone, fins that actually break the outline, and a tapered flame.
    """
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    px = im.load()
    cx = (w - 1) // 2
    dark, mid, lite, hot = ramp['dark'], ramp['mid'], ramp['lite'], ramp['hot']

    # ⚠ BODY WIDTH COMES FROM THE HEIGHT, NOT THE CELL WIDTH. Deriving it from w made the two
    #   wide cells (25x52 and 29x52) into fat capsules while the narrow ones (16x44) read as
    #   rockets - the cells differ in width but all four are the SAME object, so the proportion
    #   has to come from the one dimension they share. The extra width in those cells is fin span.
    bh = max(3, min(int(round(h * 0.115)), (w - 2) // 2 - 1))
    nose_end = max(6, int(h * 0.30))
    body_end = int(h * 0.62)
    fin_top  = int(h * 0.44)
    noz_end  = int(h * 0.70)

    def put(x, y, c):
        if 0 <= x < w and 0 <= y < h:
            px[x, y] = (c[0], c[1], c[2], 255)

    def cyl(x, tail=False):
        """cylinder shading: 2px specular left of centre, dark down the right"""
        off = x - cx
        if off <= -bh + 1:      c = mid
        elif off <= -bh + 3:    c = lite
        elif off >= bh - 1:     c = dark
        else:                   c = mid
        return tuple(int(v * 0.70) for v in c) if tail else c

    # ---- nose: a real cone, 1px tip, convex flanks ----
    for y in range(nose_end):
        t = (y + 1) / float(nose_end)
        hw = int(round(bh * (t ** 0.70)))
        for x in range(cx - hw, cx + hw + 1):
            put(x, y, hot if y <= 1 else cyl(x))

    # ---- body ----
    for y in range(nose_end, body_end):
        for x in range(cx - bh, cx + bh + 1):
            put(x, y, cyl(x))
    ring = nose_end + max(2, (body_end - nose_end) // 3)
    for y in (ring, ring + 1):
        for x in range(cx - bh, cx + bh + 1):
            put(x, y, tuple(int(v * 0.45) for v in mid))

    # ---- fins: solid triangles OUTSIDE the body, so they break the silhouette ----
    reach = max(2, min(bh, (w - 1) // 2 - bh))
    for y in range(fin_top, body_end + 1):
        t = (y - fin_top) / float(max(1, body_end - fin_top))
        e = int(round(reach * t))
        for o in range(1, e + 1):
            put(cx - bh - o, y, mid if o < e else dark)
            put(cx + bh + o, y, dark)

    # ---- nozzle: narrower and dark, so the body visually ends ----
    for y in range(body_end, noz_end):
        for x in range(cx - bh + 1, cx + bh):
            put(x, y, tuple(int(v * 0.42) for v in mid))

    # ---- exhaust: tapers to a point, 2px white core, never a blob ----
    for y in range(noz_end, h):
        t = (y - noz_end) / float(max(1, h - 1 - noz_end))
        hw = int(round((bh - 1) * (1.0 - t) ** 0.85))
        if hw < 0:
            break
        for x in range(cx - hw, cx + hw + 1):
            d = abs(x - cx)
            if d <= 1 and t < 0.55:   c = (255, 255, 255)
            elif d < hw:              c = hot
            else:                     c = lite
            put(x, y, c)

    # ---- 1px black outline round the silhouette (house style) ----
    solid = [[px[x, y][3] > 0 for y in range(h)] for x in range(w)]
    for x in range(w):
        for y in range(h):
            if solid[x][y]:
                continue
            if any(0 <= x + dx < w and 0 <= y + dy < h and solid[x + dx][y + dy]
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                px[x, y] = BLACK
    return im


def nearest_to_h(im, h):
    """exactly what drawMfx does: scale by height, round the width, nearest-neighbour"""
    s = h / float(im.height)
    w = max(1, int(round(im.width * s)))
    return im.resize((w, h), Image.NEAREST)


def main():
    apply = '--apply' in sys.argv
    s = io.open(os.path.join(ROOT, 'assets', 'manifest.js'), encoding='utf-8').read()
    rects = {}
    for m in re.finditer(r'"([A-Za-z0-9_]+)":\["([A-Za-z0-9_]+)",(\d+),(\d+),(\d+),(\d+)\]', s):
        rects[m.group(1)] = (m.group(2),) + tuple(int(v) for v in m.groups()[2:])

    atlases, made = {}, []
    for i in range(4):
        k = 'mfx_emr_0_%d' % i
        f, x, y, w, h = rects[k]
        if f not in atlases:
            atlases[f] = Image.open(os.path.join(ATLAS_DIR, f + '.png')).convert('RGBA')
        old = atlases[f].crop((x, y, x + w, y + h))
        new = draw_missile(w, h, RAMPS[i])
        made.append((k, old, new, w, h))
        if apply:
            atlases[f].paste(new, (x, y))     # same rect, so no repack and no manifest change

    print('%-14s %-8s %-9s %s' % ('key', 'cell', 'colour', 'on screen after the engine reduction'))
    for k, old, new, w, h in made:
        shown = nearest_to_h(new, DRAW_H)
        print('%-14s %-8s %-9s %dx%d  (%.2fx reduction)'
              % (k, '%dx%d' % (w, h), RAMPS[int(k[-1])]['name'], shown.width, shown.height, h / float(DRAW_H)))

    if apply:
        for f, im in atlases.items():
            dst = os.path.join(ATLAS_DIR, f + '.png')
            bak = os.path.join(tempfile.gettempdir(), f + '.pre0904c.png')
            if not os.path.exists(bak):
                shutil.copy2(dst, bak)
            im.save(dst)
            print('WROTE', dst, '(pre-change copy at %s)' % bak)
    return made


if __name__ == '__main__':
    main()
