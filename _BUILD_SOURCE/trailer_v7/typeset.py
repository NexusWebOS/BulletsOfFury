"""typeset.py - set trailer title cards in Bullets of Fury's own authored stage faces, at 1080p.

    from typeset import text
    im = text('9 PILOTS', face='final', height=180)          # RGBA, trimmed to ink

Faces come from window.BOF.stageFontV4 (assets/stagefonts_v4.js): per-stage glyph atlases with
[x,y,w,h] rects at an 84 px cap height. Scaling goes UP by an integer with nearest-neighbour first
and then down to the exact height with Lanczos, so the pixel-art lettering stays crisp at any size
instead of smearing at a fractional scale.

CLAUDE.md traps this respects:
  * a missing glyph must not silently become a space ("CHOO E YOUR PILOT", 0903) - it RAISES.
  * a hyphen bottom-aligned reads as an underscore ("MID_AIR", 0822a) - '-' is centred on the
    cap height, and ' " * ride at the top, instead of every glyph sitting on the baseline.
"""
import os, re, json, math
from PIL import Image

ROOT = r'C:\Users\Mdogg\Desktop\BOF-CODE\BulletsOfFury'
_SRC = open(os.path.join(ROOT, 'assets', 'stagefonts_v4.js'), encoding='utf-8').read()
_FACES, _ = json.JSONDecoder().raw_decode(_SRC[_SRC.index('{', _SRC.index('stageFontV4')):])
_NAMED = {'EXCL': '!', 'EXCLAM': '!', 'QMARK': '?', 'QUEST': '?', 'DOT': '.', 'PERIOD': '.', 'COMMA': ',',
          'DASH': '-', 'HYPHEN': '-', 'COLON': ':', 'APOS': "'", 'QUOTE': '"', 'SLASH': '/', 'AMP': '&',
          'PLUS': '+', 'PCT': '%', 'HASH': '#', 'LPAREN': '(', 'RPAREN': ')', 'STAR': '*', 'AT': '@'}
_TOP = set("'\"*")
_MID = set('-+=:')
_cache = {}


def faces():
    return sorted(_FACES, key=lambda k: (len(k), k))


def _face(key):
    if key in _cache:
        return _cache[key]
    f = _FACES[str(key)]
    atlas = Image.open(os.path.join(ROOT, f['atlas'])).convert('RGBA')
    if isinstance(f.get('font'), dict) and f['font']:
        cmap = {ch: nm for ch, nm in f['font'].items() if nm in f['frames']}
    else:
        cmap = {}
        for nm in f['frames']:
            suf = nm.split('_', 2)[-1] if nm.count('_') >= 2 else nm
            if len(suf) == 1:
                cmap[suf] = nm
            elif suf.upper() in _NAMED:
                cmap[_NAMED[suf.upper()]] = nm
            elif re.fullmatch(r'p\d+', suf):
                cmap[chr(int(suf[1:]))] = nm
    cap = max(r[3] for r in f['frames'].values())
    glyphs = {ch: atlas.crop((r[0], r[1], r[0] + r[2], r[1] + r[3])) for ch, nm in cmap.items() for r in [f['frames'][nm]]}
    _cache[key] = (glyphs, cap)
    return _cache[key]


def has_glyphs(s, face='final'):
    glyphs, _ = _face(face)
    return [ch for ch in s if ch != ' ' and ch not in glyphs]


def palette_swap(img, color, alpha=1.0):
    """The game's drawFrameTinted, in numpy: an opaque fill of `color` drawn over the glyph with the canvas
    'color' composite at globalAlpha `alpha`, then destination-in by the glyph. Hue and saturation come from
    the tint and LUMINOSITY from the glyph, so the drop shadow stays dark and the face stays bright - the flat
    flood this replaced is what turned an E into a B (0809q). The pilot screen names each pilot this way at
    alpha 1 in their own PILOTS[].tint."""
    import numpy as np
    a = np.asarray(img.convert('RGBA'), dtype=np.float32) / 255.0
    cb, ab = a[..., :3], a[..., 3:4]
    cs = (np.array([int(color[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float32) / 255.0)[None, None, :]

    def lum(c):
        return c[..., 0:1] * 0.3 + c[..., 1:2] * 0.59 + c[..., 2:3] * 0.11

    c = cs + (lum(cb) - lum(cs))                                  # SetLum(tint, Lum(glyph))
    L = lum(c)
    n = c.min(axis=-1, keepdims=True)
    x = c.max(axis=-1, keepdims=True)
    c = np.where(n < 0, L + (c - L) * L / np.maximum(L - n, 1e-6), c)            # ClipColor
    c = np.where(x > 1, L + (c - L) * (1 - L) / np.maximum(x - L, 1e-6), c)
    over = (1 - ab) * cs + ab * c                                 # the opaque fill, blended where the glyph is
    out = alpha * over + (1 - alpha) * cb                         # globalAlpha leans back toward the untinted glyph
    rgba = np.concatenate([np.clip(out, 0, 1), ab], axis=-1)      # destination-in keeps only the glyph's ink
    return Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), 'RGBA')


def text(s, face='final', height=160, tracking=0.05, space=0.34, tint=None, tint_a=1.0):
    """RGBA image of `s` in stage face `face`, cap height `height` px, trimmed to its ink box. `tint` is a #rrggbb
    palette swap applied at the glyphs' native size, before scaling, the way the game tints a frame."""
    glyphs, cap = _face(face)
    missing = [ch for ch in s if ch != ' ' and ch not in glyphs]
    if missing:
        raise ValueError('face %s has no glyph for %r - refusing to draw a gap' % (face, ''.join(sorted(set(missing)))))
    gap = int(round(cap * tracking))
    width = 0
    for ch in s:
        width += int(cap * space) if ch == ' ' else glyphs[ch].width + gap
    width = max(1, width - gap)
    line = Image.new('RGBA', (width, cap), (0, 0, 0, 0))
    x = 0
    for ch in s:
        if ch == ' ':
            x += int(cap * space)
            continue
        g = glyphs[ch]
        if ch in _TOP:
            y = 0
        elif ch in _MID:
            y = (cap - g.height) // 2
        else:
            y = cap - g.height
        line.alpha_composite(g, (x, y))
        x += g.width + gap
    if tint:
        line = palette_swap(line, tint, tint_a)   # at native size, before scaling - the way the game tints a frame
    k = max(1, math.ceil(height / float(cap)))
    big = line.resize((line.width * k, line.height * k), Image.NEAREST)
    if big.height != height:
        big = big.resize((max(1, int(round(big.width * height / float(big.height)))), height), Image.LANCZOS)
    bb = big.getbbox()
    return big.crop(bb) if bb else big


def fit(s, face='final', max_w=1600, max_h=200, **kw):
    """the largest cap height <= max_h at which `s` fits inside max_w"""
    probe = text(s, face=face, height=100, **kw)
    h = min(max_h, int(100 * max_w / float(max(1, probe.width))))
    return text(s, face=face, height=max(8, h), **kw)


if __name__ == '__main__':
    out = os.path.dirname(os.path.abspath(__file__))
    demo = Image.new('RGBA', (1920, 1080), (10, 10, 14, 255))
    y = 40
    for s, fk, h in [('BULLETS OF FURY', '2', 170), ('9 PILOTS', 'final', 150), ('BOSS WARNING!', '2', 120), ('MID-AIR', '6', 110)]:
        im = text(s, face=fk, height=h)
        demo.alpha_composite(im, ((1920 - im.width) // 2, y))
        y += im.height + 60
    demo.save(os.path.join(out, 'typeset_demo.png'))
    print('faces:', faces())
    print('wrote typeset_demo.png')
