"""brand9.py - pull the trailer's brand art out of the game's own atlases into brand/ (no new art is made here).

    python brand9.py

  cf_logo.png            the ColeForge Phoenix engine plate (BOFX cell cf_logo)
  bof_logo.png           the 0916 wordmark (assets/game/shared/ui/ui/logo_0916/bof_logo.png, loose)
  pose_<pilot>.png       each pilot's standing figure (pose_<pilot>_0, 256x320)
  pav_<pilot>.png        each pilot's avatar (pav_<pilot>)
  copyright.png          "(c) 2026 COLEFORGE PRODUCTIONS" - the stage face has no (c) glyph, so the mark is the
                         face's own C set inside a ring drawn from the face's own highlight and shadow colours
                         rather than a system font dropped into the card.

A cell row is [sheet, x, y, w, h]; the sheet resolves through BOFX.img['nca_' + sheet] (CLAUDE.md: a sheet index is
a NAME since the 0903 repack, and sheet 79 was never nca_79.png - resolve through the registration, never by index).
"""
import os, sys, json
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(HERE, 'brand')
PILOTS = ['axel', 'decker', 'maverick', 'freezer', 'juggernaut', 'yuri', 'lizzie', 'falva', 'cole']


def manifest():
    src = open(os.path.join(ROOT, 'assets', 'manifest.js'), encoding='utf-8').read()
    i = src.index('window.BOFX=') + len('window.BOFX=')
    bofx, _ = json.JSONDecoder().raw_decode(src[i:])
    return bofx


def cell(bofx, key):
    img = bofx.get('img', {})
    cells = bofx.get('cells', {})
    if key in cells:
        sheet, x, y, w, h = cells[key][:5]
        path = img.get('nca_' + str(sheet))
        if not path:
            raise KeyError('sheet nca_%s for %s is not registered' % (sheet, key))
        return Image.open(os.path.join(ROOT, path)).convert('RGBA').crop((x, y, x + w, y + h))
    if key in img:
        return Image.open(os.path.join(ROOT, img[key])).convert('RGBA')
    raise KeyError(key)


def trim(im):
    bb = im.getbbox()
    return im.crop(bb) if bb else im


def copyright_card(height=46, face='final', tint='#dfe7f2'):
    sys.path.insert(0, HERE)
    import typeset
    words = typeset.text('2026 COLEFORGE PRODUCTIONS', face=face, height=height, tint=tint)
    c = typeset.text('C', face=face, height=int(height * 0.58), tint=tint)
    d = int(height * 1.02)
    ring = Image.new('RGBA', (d + 6, d + 6), (0, 0, 0, 0))
    dr = ImageDraw.Draw(ring)
    lw = max(3, height // 11)
    # shadow ring, then the face-coloured ring, then the face's own C centred inside
    dr.ellipse((3, 5, 3 + d - 1, 5 + d - 1), outline=(10, 12, 18, 255), width=lw + 2)
    dr.ellipse((2, 2, 2 + d - 1, 2 + d - 1), outline=(223, 231, 242, 255), width=lw)
    ring.alpha_composite(c, ((ring.width - c.width) // 2, (ring.height - c.height) // 2))
    gap = int(height * 0.34)
    out = Image.new('RGBA', (ring.width + gap + words.width, max(ring.height, words.height)), (0, 0, 0, 0))
    out.alpha_composite(ring, (0, (out.height - ring.height) // 2))
    out.alpha_composite(words, (ring.width + gap, (out.height - words.height) // 2))
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    B = manifest()
    got = []
    for key, name in [('cf_logo', 'cf_logo.png'), ('nbl_logo', 'nbl_logo.png')]:
        try:
            trim(cell(B, key)).save(os.path.join(OUT, name))
            got.append(name)
        except Exception as e:
            print('  missing', key, e)
    Image.open(os.path.join(ROOT, 'assets', 'game', 'ui', 'logo_0916', 'bof_logo.png')).convert('RGBA').save(os.path.join(OUT, 'bof_logo.png'))
    got.append('bof_logo.png')
    # the body the pilot-select screen draws (psBodyKey): <pilot>_body_0 first; cole_body_0 is redirected to
    # cole_body_0922 by XART itself; Yuri's pose_ set is art Mike rejected (PS_POSE_STALE) and is never used.
    for p in PILOTS:
        path = os.path.join(ROOT, 'assets', 'game', 'pilots_0922', 'bodies', 'cole.png') if p == 'cole' else \
            os.path.join(ROOT, 'assets', 'game', 'pilot_bodies', '%s_body_0.png' % p)
        trim(Image.open(path).convert('RGBA')).save(os.path.join(OUT, 'body_%s.png' % p))
        got.append('body_%s.png' % p)
        # THE PILOT-SELECT PORTRAIT BOX (Mike, 0930: "use their portrait boxes from the pilot select screen"): psDrawLineup
        # draws 'pav_'+key, registered from pilots_0922/portraits/<pilot>-idle.png - a 256x256 bordered avatar. Copied
        # WHOLE (never trimmed: the border is the box) and scaled nearest-neighbour in the edit.
        Image.open(os.path.join(ROOT, 'assets', 'game', 'pilots_0922', 'portraits', '%s-idle.png' % p)).convert('RGBA') \
            .save(os.path.join(OUT, 'pav_%s.png' % p))
        got.append('pav_%s.png' % p)
    copyright_card().save(os.path.join(OUT, 'copyright.png'))
    got.append('copyright.png')
    for n in got:
        im = Image.open(os.path.join(OUT, n))
        print('%-22s %4dx%-4d' % (n, im.width, im.height))


if __name__ == '__main__':
    main()
