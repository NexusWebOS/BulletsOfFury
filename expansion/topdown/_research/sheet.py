"""Contact sheet of manifest cells: python sheet.py out.png key1 key2 ... (or @regex)."""
import json, re, sys, os
from PIL import Image, ImageDraw
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
M = json.load(open(os.path.join(os.path.dirname(__file__), 'bofx_cells.json')))
_cache = {}
def sheet(name):
    p = M['img'].get('nca_' + str(name)) or M['img'].get(str(name))
    if p is None: return None
    if p not in _cache: _cache[p] = Image.open(os.path.join(ROOT, p)).convert('RGBA')
    return _cache[p]
def cell(k):
    v = M['cells'].get(k)
    if v:
        s = sheet(v[0])
        return s.crop((v[1], v[2], v[1] + v[3], v[2] + v[4])) if s else None
    p = M['img'].get(k)
    if p and os.path.exists(os.path.join(ROOT, p)): return Image.open(os.path.join(ROOT, p)).convert('RGBA')
    return None
def main():
    out, args = sys.argv[1], sys.argv[2:]
    keys = []
    for a in args:
        if a.startswith('@'):
            rx = re.compile(a[1:]); keys += sorted(k for k in set(M['cells']) | set(M['img']) if rx.search(k))
        else: keys.append(a)
    ims = [(k, cell(k)) for k in keys]; ims = [(k, i) for k, i in ims if i is not None]
    T = 140; cols = 8; rows = (len(ims) + cols - 1) // cols
    S = Image.new('RGBA', (cols * T, rows * (T + 14)), (40, 44, 40, 255)); d = ImageDraw.Draw(S)
    for n, (k, im) in enumerate(ims):
        im = im.copy(); im.thumbnail((T - 6, T - 6), Image.NEAREST)
        x, y = (n % cols) * T, (n // cols) * (T + 14)
        S.paste(im, (x + (T - im.width) // 2, y + (T - im.height) // 2), im)
        d.text((x + 2, y + T), k[:22], fill=(230, 230, 200, 255))
    S.save(out); print(out, len(ims), 'of', len(keys))
main()
