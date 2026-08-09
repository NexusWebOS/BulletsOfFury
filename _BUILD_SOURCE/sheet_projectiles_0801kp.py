#!/usr/bin/env python3
"""
sheet_projectiles_0801kp.py — CONTACT SHEETS OF EVERY PROJECTILE IN THE BUILD

Mike: "show me all the projecticles you have in the entire game folder. I meant
all of them. this will sort things out quickly."

Renders labelled sheets so a plate can be pointed at by name. Four groups:

  1. nep_<stage>_<slot>   enemy projectiles      9 stages x 7 slots
  2. nbp_<stage>_<slot>   BOSS projectiles       9 stages x 7 slots
                          These two are the ones the arsenal actually draws.
                          Column = the slot ARSENAL_SLOT maps a kind onto, so
                          the header names Mike's six against each column.
  3. per-boss <name>_projectile_NN
  4. bfx_ / mfx_ / lzr_ / msl_ fire FX reels

Everything is drawn on a mid-grey checker so both dark and bright plates read,
and each cell is labelled with its exact manifest key.
"""
import json, os, re, sys, collections
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = '/home/claude/work/sheets'
SLOT_NAMES = ['0 pellet', '1 flare', '2 comet', '3 blast', '4 homing', '5 missile', '6 (extra)']


def manifest():
    s = open(os.path.join(ROOT, 'assets/manifest.js')).read()
    return json.loads(re.search(r'window\.BOFX=([\s\S]*?\});', s).group(1))['img']


def font(sz):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
              '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()


def checker(w, h, sz=8, a=(58, 60, 68), b=(46, 48, 55)):
    im = Image.new('RGBA', (w, h), a)
    d = ImageDraw.Draw(im)
    for y in range(0, h, sz):
        for x in range(0, w, sz):
            if (x // sz + y // sz) % 2:
                d.rectangle([x, y, x + sz - 1, y + sz - 1], fill=b)
    return im


def cell(img, key, path, CW, CH, f_key):
    """One labelled tile."""
    c = checker(CW, CH)
    d = ImageDraw.Draw(c)
    try:
        im = Image.open(path).convert('RGBA')
        src = im.size
        im.thumbnail((CW - 12, CH - 30), Image.LANCZOS)
        c.alpha_composite(im, ((CW - im.width) // 2, (CH - 26 - im.height) // 2 + 4))
        lbl = f'{key}'
        sub = f'{src[0]}x{src[1]}'
    except Exception as e:
        lbl, sub = key, 'MISSING'
    d.rectangle([0, CH - 24, CW, CH], fill=(18, 20, 26))
    d.text((4, CH - 22), lbl, font=f_key, fill=(232, 236, 244))
    d.text((4, CH - 12), sub, font=f_key, fill=(140, 150, 165))
    d.rectangle([0, 0, CW - 1, CH - 1], outline=(90, 94, 106))
    return c


def grid_sheet(img, prefix, title, note):
    stages = sorted({int(m.group(1)) for k in img
                     if (m := re.match(rf'^{prefix}_(\d+)_(\d+)$', k))})
    slots = sorted({int(m.group(2)) for k in img
                    if (m := re.match(rf'^{prefix}_(\d+)_(\d+)$', k))})
    CW, CH = 150, 138
    LEFT, TOP = 96, 78
    W = LEFT + CW * len(slots)
    H = TOP + CH * len(stages) + 14
    sheet = Image.new('RGBA', (W, H), (24, 26, 34))
    d = ImageDraw.Draw(sheet)
    fT, fH, fK = font(24), font(14), font(11)
    d.text((14, 14), title, font=fT, fill=(255, 255, 255))
    d.text((14, 46), note, font=fH, fill=(160, 200, 255))
    for ci, s in enumerate(slots):
        nm = SLOT_NAMES[s] if s < len(SLOT_NAMES) else str(s)
        d.text((LEFT + ci * CW + 6, TOP - 22), nm, font=fH, fill=(255, 214, 120))
    for ri, st in enumerate(stages):
        d.text((10, TOP + ri * CH + CH // 2 - 8), f'stage {st}', font=fH, fill=(190, 198, 212))
        for ci, sl in enumerate(slots):
            k = f'{prefix}_{st}_{sl}'
            if k not in img: continue
            sheet.alpha_composite(cell(img, k, os.path.join(ROOT, img[k]), CW, CH, fK),
                                  (LEFT + ci * CW, TOP + ri * CH))
    return sheet


def flat_sheet(keys, img, title, note, cols=8):
    CW, CH = 150, 138
    TOP = 78
    rows = (len(keys) + cols - 1) // cols
    sheet = Image.new('RGBA', (cols * CW, TOP + rows * CH + 12), (24, 26, 34))
    d = ImageDraw.Draw(sheet)
    d.text((14, 14), title, font=font(24), fill=(255, 255, 255))
    d.text((14, 46), note, font=font(14), fill=(160, 200, 255))
    fK = font(11)
    for i, k in enumerate(keys):
        r, c = divmod(i, cols)
        sheet.alpha_composite(cell(img, k, os.path.join(ROOT, img[k]), CW, CH, fK),
                              (c * CW, TOP + r * CH))
    return sheet


def main():
    img = manifest()
    os.makedirs(OUT, exist_ok=True)
    made = []

    s = grid_sheet(img, 'nep', 'ENEMY PROJECTILES — nep_<stage>_<slot>',
                   'Column = the ARSENAL_SLOT a kind maps onto. This is what ordinary enemies draw.')
    p = f'{OUT}/1_enemy_projectiles.png'; s.save(p); made.append(p)

    s = grid_sheet(img, 'nbp', 'BOSS PROJECTILES — nbp_<stage>_<slot>',
                   'Same slots, boss plates. Bigger art: this is where the large green/blue orbs live.')
    p = f'{OUT}/2_boss_projectiles.png'; s.save(p); made.append(p)

    # per-boss named projectiles
    bk = sorted(k for k in img if re.search(r'_projectile(_\d+)?$', k))
    if bk:
        s = flat_sheet(bk, img, 'PER-BOSS PROJECTILES — <boss>_projectile_NN',
                       f'{len(bk)} plates authored per boss, outside the slot system.')
        p = f'{OUT}/3_perboss_projectiles.png'; s.save(p); made.append(p)

    # fire FX reels — sample each reel's frames
    for pre, tt in [('bfx', 'BOSS FIRE FX — bfx_'), ('mfx', 'MUZZLE / FIRE FX — mfx_'),
                    ('lzr', 'LASERS — lzr_'), ('msl', 'MISSILES — msl_')]:
        ks = sorted(k for k in img if k.startswith(pre + '_'))
        if not ks: continue
        # one frame per reel family, so 216 keys become a readable page
        fam = collections.OrderedDict()
        for k in ks:
            base = re.sub(r'_\d+$', '', k)
            fam.setdefault(base, k)
        s = flat_sheet(list(fam.values()), img, tt,
                       f'{len(ks)} keys in {len(fam)} reels — first frame of each reel shown.')
        p = f'{OUT}/4_{pre}.png'; s.save(p); made.append(p)

    for m in made:
        print(m, Image.open(m).size)


if __name__ == '__main__':
    main()
