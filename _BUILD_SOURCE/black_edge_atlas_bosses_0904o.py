"""
black_edge_atlas_bosses_0904o.py - black-edge the boss plates that live INSIDE shared atlases.

Mike: "stage-7 yes the black edges for the frames it and almost all bosses."

⚠ THE BOSSES HE NAMED ARE ALL ATLAS CELLS, AND THE OBVIOUS APPROACH WRECKS THE ATLAS. The Olive
   Warden (stage 7), Rime Wall, Magma Ward and Xeno Regent are cells inside mini_s4, boss_s3,
   mini_s2 and boss_s5. My first pass resolved their manifest entries to the atlas FILE and
   outlined each sheet as though it were one hull - tracing every cell's silhouette and padding
   the sheet, which invalidates every rect that indexes it. Six atlases were modified before
   git status caught it; all reverted.

   So an atlas cell cannot GROW an outline the way a standalone plate can. This darkens INWARD
   instead: the outermost rings of the silhouette are converted to the outline colour in place.
   The cell keeps its exact rect, the sheet keeps its exact size, and no other cell is touched -
   verified by diffing the atlas afterwards and asserting every changed pixel falls inside a
   target rect.

   Cost: two pixels of art at the silhouette boundary. That is what an outline is anyway, and
   these plates are minified 2.2x-3.6x so those two pixels resolve to roughly one on screen.
"""
import io, os, re, sys
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clean_hull_edges_0904h as CH

SKIP = ('nsb_dcarrmk2_closed',)      # a 640x320 multi-state launch cell, not a single hull
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


def targets():
    g = io.open(os.path.join(ROOT, 'assets', 'game.js'), encoding='utf-8', newline='').read()
    man = io.open(os.path.join(ROOT, 'assets', 'manifest.js'), encoding='utf-8').read()
    rects = {}
    for m in re.finditer(r'"([A-Za-z0-9_]+)":\["([A-Za-z0-9_]+)",(\d+),(\d+),(\d+),(\d+)\]', man):
        rects[m.group(1)] = (m.group(2),) + tuple(int(v) for v in m.groups()[2:])
    keys = set(re.findall(r"key:'(nsb_[a-z0-9_]+)'", g))
    for d in re.findall(r'dmg:\[([^\]]+)\]', g):
        keys.update(re.findall(r"'(nsb_[a-z0-9_]+)'", d))
    # the height each boss is DRAWN at, so the edge can be scaled to its own minification
    drawh = {}
    for k, key, nm, w, h in re.findall(
            r"(\w+):\s*\{key:'(nsb_[a-z0-9_]+)',\s*name:'([^']+)',\s*w:(\d+),h:(\d+)", g):
        drawh[key] = int(h)
        m = re.search(re.escape(k) + r":\s*\{.*?dmg:\[([^\]]+)\]", g, re.S)
        if m:
            for kk in re.findall(r"'(nsb_[a-z0-9_]+)'", m.group(1)):
                drawh[kk] = int(h)
    return [(k,) + rects[k] + (drawh.get(k, 0),) for k in sorted(keys)
            if k in rects and k not in SKIP]


def edge_inward(cell, rings):
    """convert the outermost `rings` of the silhouette to the outline colour, in place"""
    px = cell.load(); w, h = cell.size
    changed = 0
    for _r in range(rings):
        ring = []
        for y in range(h):
            for x in range(w):
                if px[x, y][3] == 0:
                    continue
                if px[x, y][:3] == CH.OUTLINE_RGB[:3]:
                    continue
                edge = False
                for dx, dy in N4:
                    i, j = x + dx, y + dy
                    if i < 0 or j < 0 or i >= w or j >= h or px[i, j][3] == 0 \
                       or px[i, j][:3] == CH.OUTLINE_RGB[:3]:
                        edge = True; break
                if edge:
                    ring.append((x, y))
        for q in ring:
            a = px[q][3]
            px[q] = (CH.OUTLINE_RGB[0], CH.OUTLINE_RGB[1], CH.OUTLINE_RGB[2], a)
        changed += len(ring)
    return changed


def main():
    apply = '--apply' in sys.argv
    T = targets()
    byatlas = {}
    for k, f, x, y, w, h, dh in T:
        byatlas.setdefault(f, []).append((k, x, y, w, h, dh))
    print('%-30s %-10s %-13s %-7s %s' % ('plate', 'atlas', 'cell', 'reduce', 'edge'))
    for f, items in sorted(byatlas.items()):
        path = os.path.join(ROOT, 'assets', 'game', 'atlas', f + '.png')
        if not os.path.exists(path):
            print('  missing atlas', path); continue
        im = Image.open(path).convert('RGBA')
        before = im.copy()
        total = 0
        for k, x, y, w, h, dh in items:
            factor = (h / float(dh)) if dh else 1.0
            rings = max(2, min(4, int(round(factor))))
            cell = im.crop((x, y, x + w, y + h))
            n = edge_inward(cell, rings)
            im.paste(cell, (x, y))
            total += n
            print('%-30s %-10s %-13s %-7.2f %d px  (%d rings)'
                  % (k, f, '%d,%d %dx%d' % (x, y, w, h), factor, n, rings))
        # ⚠ prove nothing outside a target rect moved before writing a shared sheet
        diff = ImageChops.difference(before, im).convert('L')
        bb = diff.getbbox()
        stray = 0
        if bb:
            dp = diff.load()
            for yy in range(bb[1], bb[3]):
                for xx in range(bb[0], bb[2]):
                    if not dp[xx, yy]:
                        continue
                    inside = any(x <= xx < x + w and y <= yy < y + h for _k, x, y, w, h, _d in items)
                    if not inside:
                        stray += 1
        print('   %s size %s -> %s   changed %d px, OUTSIDE the target cells: %d'
              % (f, before.size, im.size, total, stray))
        if stray:
            raise SystemExit('ABORT: %s would change %d pixels outside its target cells' % (f, stray))
        if before.size != im.size:
            raise SystemExit('ABORT: %s changed size - every rect indexing it would be wrong' % f)
        if apply:
            im.save(path)
    print()
    print('APPLIED' if apply else 'DRY RUN (pass --apply)')


if __name__ == '__main__':
    main()
