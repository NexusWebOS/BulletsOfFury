#!/usr/bin/env python3
"""strip_jug_flame_0906p.py - a genuinely flameless Juggernaut, and his real mounts from the flame.

    python _BUILD_SOURCE/strip_jug_flame_0906p.py            # proof only
    python _BUILD_SOURCE/strip_jug_flame_0906p.py --write

Mike, 0906: "just make sure you get a frame without the thrusters."

⚠ ONLY ONE OF THE NINE HULLS ACTUALLY HAS FLAME BAKED IN, AND I NEARLY BELIEVED OTHERWISE. A
hot-pixel count over the tail band reported flame on five ships (falva 850 px, juggernaut 369,
decker 168, lizzie 140, yuri 103). Rendering the tails settled it: on all of them except Juggernaut
those hot pixels are NOZZLE INTERIORS and white metal highlights, not exhaust. Juggernaut is the
only hull carrying a real plume, because his art was generated with one. **The count was measuring
brightness; only the picture could say what was bright.**

⚠ AND THE FLAME IS WHAT MAKES HIS MOUNTS MEASURABLE. A generic "find the engines" detector was
written for all nine and FAILED ITS VALIDATION - constrained to the fuselage it still reproduced
only 1 of the 4 ships whose art has not changed since the mounts were authored, finding wingtip
and canopy highlights instead. It is therefore not used to move anybody's mounts. Juggernaut is
the exception on evidence rather than on preference: his exhaust is literally drawn on the plate,
so the x-centroid of each flame blob IS a mount, with nothing to confuse it for.

The flame is found by connected components of hot pixels reaching the BOTTOM 15% of the ink -
exhaust leaves the ship, a lit nozzle interior does not - so a bright engine bell cannot be mistaken
for a plume even on his own hull. See the two inline notes for the tolerance and for why a white-hot
core needs catching on brightness rather than on warmth.
"""
import os, re, sys, json, shutil, subprocess, colorsys
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')


def is_hot(p):
    """⚠ A WHITE-HOT FLAME CORE HAS NEAR-ZERO SATURATION, WHICH THE FIRST VERSION OF THIS EXCLUDED.
    Requiring s >= 0.35 kept the very hottest part of the exhaust and removed only the orange around
    it, leaving a pale ghost sitting in each nozzle - visible in the first proof render and easy to
    mistake for nozzle art. Fire runs orange -> yellow -> WHITE, so the top of that ramp is
    desaturated by definition and has to be caught on brightness alone."""
    r, g, b, a = p
    if a < 32:
        return False
    h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
    if v >= 0.86:
        return True                                     # white-hot core, whatever its saturation
    return v >= 0.72 and s >= 0.35 and (h < 0.15 or h > 0.90)


def flame_blobs(cell):
    """hot components that reach the bottom edge of the ink - i.e. exhaust leaving the ship"""
    W, H = cell.size
    px = cell.load()
    # the lowest inked row, so "bottom edge" means the ship's tail and not the canvas
    bot = max((y for y in range(H) for x in range(W) if px[x, y][3] > 16), default=H - 1)
    seen = [[False] * W for _ in range(H)]
    out = []
    for y0 in range(H):
        for x0 in range(W):
            if seen[y0][x0] or not is_hot(px[x0, y0]):
                continue
            q = deque([(x0, y0)]); seen[y0][x0] = True; pts = []
            while q:
                x, y = q.popleft(); pts.append((x, y))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < W and 0 <= ny < H and not seen[ny][nx] and is_hot(px[nx, ny]):
                            seen[ny][nx] = True; q.append((nx, ny))
            # ⚠ "REACHES THE TAIL" IS THE BOTTOM 15% OF THE INK, NOT THE LAST TWO ROWS. Measured on
            # this hull: the flame ends at y205 against an ink bottom of y212, so a 2px tolerance
            # found ZERO blobs and reported a hull with visible exhaust as flameless. The scattered
            # single hot pixels higher up the fuselage (y50, y76, y111...) are highlights, and a
            # 15% band still excludes every one of them.
            if max(p[1] for p in pts) >= bot - max(4, int(bot * 0.15)) and len(pts) >= 25:
                out.append(pts)
    return out, bot


def main():
    write = '--write' in sys.argv
    js = subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "const o={};for(const k in BOFX.ships)"
        "if(k==='ship_juggernaut'||k.indexOf('ship_juggernaut_')===0)o[k]=BOFX.ships[k];"
        "process.stdout.write(JSON.stringify(o));"], capture_output=True, cwd=ROOT)
    R = json.loads(js.stdout.decode())
    A = Image.open(ATLAS).convert('RGBA')

    hull = R['ship_juggernaut']
    hx, hy, hw, hh = hull[0], hull[1], hull[2], hull[3]
    cell = A.crop((hx, hy, hx + hw, hy + hh))
    bb = cell.getbbox()
    trim = cell.crop(bb) if bb else cell
    blobs, bot = flame_blobs(trim)
    W = trim.width
    mounts = sorted(round((sum(p[0] for p in pts) / len(pts) - (W - 1) / 2.0) / W, 4) for pts in blobs)
    print('hull ink %dx%d - %d flame blob(s) reaching the tail' % (trim.width, trim.height, len(blobs)))
    for i, pts in enumerate(blobs):
        cx = sum(p[0] for p in pts) / len(pts)
        print('   blob %d: %d px, centre x %+.4f of width' % (i, len(pts), (cx - (W - 1) / 2.0) / W))
    print('measured mounts: %s' % ', '.join('%+.4f' % m for m in mounts))
    print('authored (stale - his art was replaced twice since): %s'
          % ', '.join('%+.4f' % m for m in json.load(open(os.path.join(ROOT, 'assets/data/thruster_mounts.json')))['juggernaut']['mounts']))

    # ---- build the flameless frames
    before = trim.copy()
    stripped = 0
    for k, r in sorted(R.items()):
        x, y, w, h = r[0], r[1], r[2], r[3]
        c = A.crop((x, y, x + w, y + h))
        b2 = c.getbbox()
        if not b2:
            continue
        t = c.crop(b2)
        bl, _ = flame_blobs(t)
        if not bl:
            continue
        px = t.load()
        for pts in bl:
            for (a, b3) in pts:
                px[a, b3] = (0, 0, 0, 0)
                stripped += 1
        c.paste(t, (b2[0], b2[1]))
        A.paste(c, (x, y))
    print('stripped %d flame pixels across %d frames' % (stripped, len(R)))

    after = A.crop((hx, hy, hx + hw, hy + hh))
    b3 = after.getbbox()
    after = after.crop(b3) if b3 else after

    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    T = 320
    proof = Image.new('RGB', (T * 2, T + 24), (22, 22, 28))
    d = ImageDraw.Draw(proof)
    for i, (lbl, im) in enumerate((('WITH baked flame', before), ('flameless (_nf)', after))):
        s = min((T - 14) / im.width, (T - 14) / im.height)
        t = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
        proof.paste(t, (i * T + (T - t.width) // 2, (T - t.height) // 2), t)
        d.text((i * T + 5, T + 5), lbl, font=F, fill=(240, 240, 250))
    proof.save(os.path.join(ROOT, 'docs/JUG_FLAMELESS_0906P.png'))
    print('wrote docs/JUG_FLAMELESS_0906P.png')

    if not write:
        print('DRY RUN - nothing written.')
        return 0
    bak = ATLAS + '.0906p.bak'
    if not os.path.exists(bak):
        shutil.copy2(ATLAS, bak)
    A.save(ATLAS)
    # his mounts are now measured from his own exhaust, so the stale authored row is replaced
    mp = os.path.join(ROOT, 'assets/data/thruster_mounts.json')
    mj = json.load(open(mp))
    mj['juggernaut']['mounts'] = mounts
    mj['juggernaut']['note'] = ('measured 0906p from the x-centroids of the baked exhaust on his own '
                                'hull, which is the only unambiguous source any of the nine has; the '
                                'previous three-mount row was authored against an airframe replaced twice since')
    json.dump(mj, open(mp, 'w', encoding='utf-8'), indent=2)
    print('wrote the atlas and juggernaut\'s mounts')
    return 0


if __name__ == '__main__':
    sys.exit(main())
