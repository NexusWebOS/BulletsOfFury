"""Bullets of Fury - social channel art kit.

Builds every avatar / banner / thumbnail plate the YouTube, X and Instagram
pages need, from the SHIPPED art only:

    assets/game/ui/logo_0916/bof_logo.png   the authored wordmark (magenta already keyed)
    docs/marketing_0916/cover_b_with_logo.png   the cover painting

Nothing here is generated or invented -- it is crop, scale and composite, so the
channel reads as the same game the player sees on the title screen.

    python _BUILD_SOURCE/social_kit_0916.py            build everything
    python _BUILD_SOURCE/social_kit_0916.py --avatars  just the avatar candidates

Output: docs/marketing_0916/social/
"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, 'assets', 'game', 'ui', 'logo_0916', 'bof_logo.png')
COVER_B = os.path.join(ROOT, 'docs', 'marketing_0916', 'cover_b_with_logo.png')
COVER_A = os.path.join(ROOT, 'docs', 'marketing_0916', 'cover_a_with_logo.png')
OUT = os.path.join(ROOT, 'docs', 'marketing_0916', 'social')

# Measured off bof_logo.png (1506x747) with a ruled overlay, not guessed. The
# wordmark is BULLETS OF across the top and FURY filling the rest, with chevron
# wings out to both plate edges and the turbine emblem at bottom centre.
FURY_BOX = (95, 168, 1420, 700)     # the whole FURY word incl. wings
FU_BOX = (150, 175, 810, 640)       # the FU pair -- the tight avatar crop

# The three words, cut apart so the square lockup can restack them. A 2:1
# wordmark cannot fill a square; every avatar surface that matters (YouTube's
# circle, X, Instagram) is square, so the words are re-laid-out rather than
# letterboxed with dead air top and bottom.
W_BULLETS = (243, 2, 1038, 186)
W_OF = (1040, 12, 1302, 182)
W_FURY = (0, 172, 1506, 747)        # letters + wings + turbine

# Colours sampled from the cover painting.
DEEP = (9, 12, 26)
NAVY = (18, 26, 54)
EMBER = (255, 122, 26)
HOT = (255, 196, 86)


def _ensure():
    os.makedirs(OUT, exist_ok=True)


def logo():
    return Image.open(LOGO).convert('RGBA')


def cover(which='b'):
    return Image.open(COVER_B if which == 'b' else COVER_A).convert('RGB')


def fit(im, w, h):
    """Scale to fit inside w,h keeping aspect. Returns the scaled image."""
    r = min(w / im.width, h / im.height)
    return im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)


def cover_fill(im, w, h):
    """Scale to COVER w,h then centre-crop."""
    r = max(w / im.width, h / im.height)
    s = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x = (s.width - w) // 2
    y = (s.height - h) // 2
    return s.crop((x, y, x + w, y + h))


def radial_bg(w, h, inner=NAVY, outer=DEEP):
    """A cheap radial: a small gradient blown up, which is smooth at any size."""
    s = 64
    g = Image.new('RGB', (s, s), outer)
    d = ImageDraw.Draw(g)
    cx, cy = s / 2, s / 2
    for i in range(s // 2, 0, -1):
        t = 1 - (i / (s / 2))
        c = tuple(int(outer[k] + (inner[k] - outer[k]) * (t ** 1.6)) for k in range(3))
        d.ellipse((cx - i, cy - i, cx + i, cy + i), fill=c)
    return g.resize((w, h), Image.BICUBIC)


def glow(mask_src, colour, radius, strength=1.0):
    """An outward glow built from a source image's own alpha."""
    a = mask_src.split()[3]
    g = Image.new('RGBA', mask_src.size, colour + (0,))
    blur = a.filter(ImageFilter.GaussianBlur(radius))
    blur = blur.point(lambda v: min(255, int(v * strength)))
    g.putalpha(blur)
    return g


def scanlines(im, alpha=26, pitch=3):
    """The game draws a scanline every 2px; the plates keep the same signature."""
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(0, im.size[1], pitch):
        d.line((0, y, im.size[0], y), fill=(0, 0, 0, alpha))
    return Image.alpha_composite(im.convert('RGBA'), ov)


def vignette(im, power=0.85):
    w, h = im.size
    v = radial_bg(w, h, (255, 255, 255), (0, 0, 0)).convert('L')
    v = v.point(lambda x: int(255 - (255 - x) * power))
    out = im.convert('RGB')
    black = Image.new('RGB', (w, h), (0, 0, 0))
    return Image.composite(out, black, v)


# ----------------------------------------------------------------- avatars
def build_avatar(box, size=800, name='avatar.png', pad=0.90):
    """A square avatar. `box` is the crop taken out of the wordmark."""
    lg = logo().crop(box)
    bg = radial_bg(size, size).convert('RGBA')

    # a fire wash behind the mark, from the cover's own flame band
    cv = cover('b')
    flame = cv.crop((0, int(cv.height * 0.60), cv.width, int(cv.height * 0.80)))
    flame = cover_fill(flame, size, size).filter(ImageFilter.GaussianBlur(size // 14))
    flame = ImageEnhance.Brightness(flame).enhance(0.55)
    bg = Image.blend(bg, flame.convert('RGBA'), 0.42)

    mark = fit(lg, int(size * pad), int(size * pad))
    x = (size - mark.width) // 2
    y = (size - mark.height) // 2

    layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    layer.paste(mark, (x, y), mark)
    bg = Image.alpha_composite(bg, glow(layer, EMBER, size // 22, 0.9))
    bg = Image.alpha_composite(bg, glow(layer, HOT, size // 60, 1.0))
    bg = Image.alpha_composite(bg, layer)

    bg = scanlines(bg, 22, 3)
    bg = vignette(bg, 0.55).convert('RGB')
    bg.save(os.path.join(OUT, name))
    return bg


def build_avatar_stack(size=800, name='avatar_d_stack.png', words=('bullets', 'of', 'fury')):
    """The square lockup: BULLETS / OF / FURY restacked out of the wordmark.

    Widths are chosen so FURY dominates -- at the 48px YouTube draws in a
    comment thread only the bottom word can carry the brand, so it gets the
    full frame width and the other two ride above it.
    """
    lg = logo()
    cuts = {'bullets': lg.crop(W_BULLETS), 'of': lg.crop(W_OF), 'fury': lg.crop(W_FURY)}
    # FURY at 0.92 rather than full bleed: the avatar is CROPPED TO A CIRCLE on
    # YouTube and X, and a full-width row sitting below the vertical centre has
    # its chevron wings cut off by the circle. 0.92 keeps both wings inside.
    widths = {'bullets': 0.58, 'of': 0.14, 'fury': 0.92}

    rows = []
    for w in words:
        c = cuts[w]
        tw = int(size * widths[w])
        rows.append(c.resize((tw, max(1, int(c.height * tw / c.width))), Image.LANCZOS))

    gap = int(size * 0.018)
    total = sum(r.height for r in rows) + gap * (len(rows) - 1)

    bg = radial_bg(size, size).convert('RGBA')
    cv = cover('b')
    flame = cv.crop((0, int(cv.height * 0.60), cv.width, int(cv.height * 0.80)))
    flame = cover_fill(flame, size, size).filter(ImageFilter.GaussianBlur(size // 14))
    flame = ImageEnhance.Brightness(flame).enhance(0.50)
    bg = Image.blend(bg, flame.convert('RGBA'), 0.40)

    layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    y = (size - total) // 2
    for r in rows:
        layer.paste(r, ((size - r.width) // 2, y), r)
        y += r.height + gap

    bg = Image.alpha_composite(bg, glow(layer, EMBER, size // 20, 0.95))
    bg = Image.alpha_composite(bg, glow(layer, HOT, size // 64, 1.0))
    bg = Image.alpha_composite(bg, layer)
    bg = scanlines(bg, 22, 3)
    bg = vignette(bg, 0.55).convert('RGB')
    bg.save(os.path.join(OUT, name))
    return bg


# ------------------------------------------------------------------ banner
def build_banner(w=2560, h=1440, name='youtube_banner.png',
                 safe=(1546, 423), tv_safe=(2560, 1440), tagline=None):
    """YouTube channel banner.

    2560x1440 is the upload size. Only the centred 1546x423 is guaranteed
    visible on every device, and 1235x338 is what a phone shows -- so the
    wordmark and the tagline both live inside the phone box, and the painting
    fills the rest.
    """
    cv = cover('b')
    bg = cover_fill(cv, w, h)
    bg = ImageEnhance.Brightness(bg).enhance(0.62)
    bg = bg.filter(ImageFilter.GaussianBlur(2)).convert('RGBA')

    # darken outside the safe area so the wordmark always has contrast
    sx, sy = (w - safe[0]) // 2, (h - safe[1]) // 2
    shade = Image.new('RGBA', (w, h), (0, 0, 0, 120))
    d = ImageDraw.Draw(shade)
    d.rectangle((sx - 120, sy - 90, sx + safe[0] + 120, sy + safe[1] + 90), fill=(0, 0, 0, 40))
    shade = shade.filter(ImageFilter.GaussianBlur(70))
    bg = Image.alpha_composite(bg, shade)

    phone = (1235, 338)
    px, py = (w - phone[0]) // 2, (h - phone[1]) // 2

    lg = logo()
    mark = fit(lg, int(phone[0] * 0.86), int(phone[1] * 0.72))
    mx = (w - mark.width) // 2
    my = py + int(phone[1] * 0.04)

    layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    layer.paste(mark, (mx, my), mark)
    bg = Image.alpha_composite(bg, glow(layer, EMBER, 46, 0.85))
    bg = Image.alpha_composite(bg, glow(layer, HOT, 12, 1.0))
    bg = Image.alpha_composite(bg, layer)

    if tagline:
        bg = draw_tagline(bg, tagline, (w // 2, my + mark.height + 34))

    bg = scanlines(bg, 20, 3)
    bg.convert('RGB').save(os.path.join(OUT, name))
    return bg


def _face(px):
    from PIL import ImageFont
    for c in (r'C:\Windows\Fonts\impact.ttf', r'C:\Windows\Fonts\arialbd.ttf',
              r'C:\Windows\Fonts\segoeuib.ttf'):
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, px)
            except Exception:
                pass
    return None


def measure_tagline(text, height):
    """The width draw_tagline WILL draw at.

    ⚠ It is not `font.getbbox(text)[2]`. draw_tagline lays out character by character and adds
    `height//12` of tracking between each one, so a fit loop measuring the plain string is short
    by roughly a pixel per character -- which shipped "THE RIME WALL" running off the panel on a
    thumbnail whose fit check had passed. Measure with the same arithmetic that draws.
    """
    f = _face(height)
    if f is None:
        return 0
    sp = max(2, height // 12)
    ws = [(f.getbbox(c)[2] - f.getbbox(c)[0]) if c != ' ' else height // 3 for c in text]
    return sum(ws) + sp * max(0, len(text) - 1)


def draw_tagline(im, text, centre, height=44, colour=(255, 226, 180)):
    """Tagline in a heavy face, letter-spaced, with a hard drop shadow.

    Uses a system face rather than the game's bitmap alphabet: the stage fonts
    have no lowercase and no apostrophe at UI size (0912b), and a channel
    banner is not a game screen.
    """
    from PIL import ImageFont
    cand = [
        r'C:\Windows\Fonts\impact.ttf',
        r'C:\Windows\Fonts\arialbd.ttf',
        r'C:\Windows\Fonts\segoeuib.ttf',
    ]
    f = None
    for c in cand:
        if os.path.exists(c):
            try:
                f = ImageFont.truetype(c, height)
                break
            except Exception:
                pass
    if f is None:
        return im
    sp = max(2, height // 12)
    widths = [f.getbbox(ch)[2] - f.getbbox(ch)[0] if ch != ' ' else height // 3 for ch in text]
    total = sum(widths) + sp * (len(text) - 1)
    x = centre[0] - total // 2
    y = centre[1]
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for ch, cw in zip(text, widths):
        if ch != ' ':
            d.text((x + 2, y + 3), ch, font=f, fill=(0, 0, 0, 210))
            d.text((x, y), ch, font=f, fill=colour + (255,))
        x += cw + sp
    return Image.alpha_composite(im.convert('RGBA'), ov)


# --------------------------------------------------------------- thumbnail
def build_thumb_base(w=1280, h=720, name='thumb_base.png', source='b', crop=None):
    """A 16:9 thumbnail bed: the painting, darkened, with the wordmark small
    in a corner so the frame's own subject owns the middle."""
    cv = cover(source)
    if crop:
        cv = cv.crop(crop)
    bg = cover_fill(cv, w, h)
    bg = ImageEnhance.Color(ImageEnhance.Brightness(bg).enhance(0.86)).enhance(1.12)
    bg = bg.convert('RGBA')
    lg = fit(logo(), int(w * 0.34), int(h * 0.22))
    layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    layer.paste(lg, (int(w * 0.03), int(h * 0.04)), lg)
    bg = Image.alpha_composite(bg, glow(layer, EMBER, 18, 0.8))
    bg = Image.alpha_composite(bg, layer)
    bg = scanlines(bg, 18, 3)
    bg.convert('RGB').save(os.path.join(OUT, name))
    return bg


def build_thumb_from_frame(frame_path, title, name, w=1280, h=720, logo_scale=0.30):
    """A thumbnail built on a REAL captured game frame.

    ⚠ THE FRAME IS NOT CROPPED TO 16:9. The game records at 960x1152 -- taller than wide -- and
    centre-cropping that to a 16:9 thumbnail throws away the top and bottom of the playfield,
    which on a vertical shmup is most of the composition. The first cut did exactly that and the
    Doomsday Carrier's thumbnail was a band of hull with the fight missing above and below it.

    So: the frame sits whole on the left at its native aspect, the wordmark and title take the
    right. That also puts the text on a controlled dark panel rather than over busy art, which is
    what keeps it legible at the 210px YouTube actually draws in a sidebar.
    """
    fr = Image.open(frame_path).convert('RGB')

    # backdrop: the frame itself, blown up and blurred, so the palette always matches the shot
    bg = cover_fill(fr, w, h).filter(ImageFilter.GaussianBlur(28))
    bg = ImageEnhance.Brightness(bg).enhance(0.38).convert('RGBA')

    gh = h - 40
    gw = max(1, int(round(fr.width * gh / fr.height)))
    gx, gy = 34, 20
    game = fr.resize((gw, gh), Image.LANCZOS)
    game = ImageEnhance.Color(game).enhance(1.12)

    frame_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    frame_layer.paste(game.convert('RGBA'), (gx, gy))
    edge = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(edge).rectangle((gx - 5, gy - 5, gx + gw + 4, gy + gh + 4),
                                   outline=EMBER + (255,), width=9)
    bg = Image.alpha_composite(bg, edge.filter(ImageFilter.GaussianBlur(16)))
    bg = Image.alpha_composite(bg, frame_layer)
    ImageDraw.Draw(bg).rectangle((gx - 2, gy - 2, gx + gw + 1, gy + gh + 1),
                                 outline=(255, 196, 120, 240), width=3)

    rx = gx + gw + 34
    rw = w - rx - 34
    lg = fit(logo(), int(rw * 0.98), int(h * 0.30))
    layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    layer.paste(lg, (rx + (rw - lg.width) // 2, 56), lg)
    bg = Image.alpha_composite(bg, glow(layer, EMBER, 22, 0.85))
    bg = Image.alpha_composite(bg, layer)

    if title:
        # Fit to the panel and wrap, measuring through measure_tagline -- the same arithmetic
        # draw_tagline uses, tracking included.
        size = 96
        lines = [title]
        while size > 30:
            lines, cur = [], ''
            for word in title.split(' '):
                t = (cur + ' ' + word).strip()
                if measure_tagline(t, size) > rw and cur:
                    lines.append(cur); cur = word
                else:
                    cur = t
            if cur:
                lines.append(cur)
            if len(lines) <= 3 and max(measure_tagline(l, size) for l in lines) <= rw:
                break
            size -= 6
        y = 56 + lg.height + 54
        for ln in lines:
            bg = draw_tagline(bg, ln, (rx + rw // 2, y), height=size, colour=(255, 234, 196))
            y += int(size * 1.12)

    bg = scanlines(bg, 16, 3)
    bg.convert('RGB').save(os.path.join(OUT, name))
    return bg


def main():
    _ensure()
    args = sys.argv[1:]

    # ---- avatar candidates
    build_avatar(FU_BOX, 800, 'avatar_a_fu.png', 0.94)
    build_avatar(FURY_BOX, 800, 'avatar_b_fury.png', 0.98)
    build_avatar((0, 0, 1506, 747), 800, 'avatar_c_full.png', 0.98)
    print('avatars ->', OUT)
    if '--avatars' in args:
        return

    build_banner(tagline='NINE PILOTS.  NINE STAGES.  ONE SKY.')
    # X header is a short letterbox; the same construction at its own aspect
    build_banner(1500, 500, 'x_header.png', safe=(1400, 400),
                 tagline='ARCADE SHMUP  -  IN DEVELOPMENT')
    print('banners ->', OUT)

    build_thumb_base(name='thumb_base_cover.png', source='b')
    print('thumb bed ->', OUT)

    # Instagram: 1:1 and 4:5
    for (w, h, nm) in ((1080, 1080, 'ig_square.png'), (1080, 1350, 'ig_portrait.png')):
        cv = cover('b')
        bg = cover_fill(cv, w, h).convert('RGBA')
        bg = scanlines(bg, 18, 3)
        bg.convert('RGB').save(os.path.join(OUT, nm))
    print('instagram ->', OUT)


if __name__ == '__main__':
    main()
