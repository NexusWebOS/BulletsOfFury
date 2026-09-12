#!/usr/bin/env python3
"""
strip_baked_plumes_0908c.py — TWO TAIL-ON FRAMES HAD AN EXHAUST PLUME PAINTED INTO THEM.

Mike, 0908: "erase these from these frames as cleanly as possible and clean up what you can via
the surrounding pixels. they dont belong on there."

so2 is the TAIL-ON frame of the somersault — you are looking straight up the exhausts — and the
game draws its own thruster over it, so a painted-in plume is a second flame on one engine.
ship_lizzie_so2 carries two orange/white tongues off her nozzle rings, ship_freezer_so2 one
white-blue tongue under his orb.

⚠ THE FIRST ATTEMPT KEYED ON CONNECTED COMPONENTS OF THE BRIGHT INK AND IT FOUND NOTHING ON
LIZZIE. The theory was that the nozzle's dark bottom lip splits the dome from the flame, so the
two would label as separate blobs. They do not: the lip has bright pixels through it, so dome and
flame are one component and the rule erased zero. On Freezer the same rule took the white tip and
left its black outline hanging as a loop under the orb. Both were visible the moment the preview
was rendered, which is why the preview exists.

Driven off MEASURED GEOMETRY instead — the per-row ink runs of each plate:

  lizzie so2 220x105   y=76 onward holds exactly two runs, 63-89 and 135-159, and they ARE the
                       two nozzle stacks; nothing else on the ship reaches that low. The dome's
                       lip sits at y=76..79 and the flame body starts at y=80, so the cut is a
                       plain y>=80. No column window needed.

  freezer so2 179x91   the plume is the run 76-102, and his claws and wings occupy 5-21, 43-56,
                       110-117, 122-135 and 155-176 at the same rows. So the cut is y>=68 AND
                       column 74..104, which reaches the plume and cannot reach a claw. y=68 is
                       the first row below the orb's pale metal rim.

Both cuts take whatever alpha they find, flame and its black outline together, and then the
silhouette is re-closed: any pixel just cleared that ends up 4-adjacent to remaining hull is
painted with the plate's own ring colour, sampled from its existing edge rather than assumed to
be black. Without that the hull is left with a raw un-ringed underside where the flame covered it.

⚠ THE ATLAS RECT IS NOT RE-CROPPED. Clearing pixels leaves the declared w/h larger than the ink,
and that is deliberate: the draw blits the rect, so the hull keeps the exact position and size it
had. Re-cropping would mean re-deriving offX/offY, which is a way to move a ship by accident.
"""
import io, json, os, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MAN  = os.path.join(ROOT, 'assets/manifest.js')
PNG  = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
PREVIEW = len(sys.argv) > 1 and sys.argv[1] == '--preview'

# key                 first row to clear, column window (None = the whole width)
CUTS = {'ship_lizzie_so2':  (78, None),
        'ship_freezer_so2': (68, (74, 104))}

src = io.open(MAN, encoding='utf-8', newline='').read()
i = src.index('"ships"'); j = src.index('{', i); d = 0
for k in range(j, len(src)):
    if src[k] == '{': d += 1
    elif src[k] == '}':
        d -= 1
        if d == 0:
            SHIPS = json.loads(src[j:k + 1]); break
atlas = Image.open(PNG).convert('RGBA')

def ring_colour(a, opaque):
    """the plate's own outline colour, from the darkest ink already on its silhouette edge"""
    p = np.pad(opaque, 1, constant_values=False)
    interior = p[:-2,1:-1] & p[2:,1:-1] & p[1:-1,:-2] & p[1:-1,2:]
    edge = opaque & ~interior
    px = a[:, :, :3][edge]
    if not len(px): return (0, 0, 0)
    v = px.max(axis=1)
    dark = px[v <= max(40, np.percentile(v, 12))]
    return tuple(int(c) for c in (dark.mean(axis=0) if len(dark) else px[v.argmin()]))

report, previews = [], []
for key, (cut, cols) in CUTS.items():
    x, y, w, h = SHIPS[key][:4]
    cell = atlas.crop((x, y, x + w, y + h))
    a = np.array(cell).astype(int)
    opaque = a[:, :, 3] > 40

    region = np.zeros((h, w), bool)
    region[cut:, :] = True
    if cols: region[:, :cols[0]] = False; region[:, cols[1] + 1:] = False
    erase = region & opaque

    # ⚠ A FLAT CUT LEAVES A SMUDGE, because the flame wraps UP around the sides of the nozzle's
    # dark lip: at lizzie y=78..79 the middle of the row is the lip (max V 4..98) while the same
    # rows carry flame fringe out at the edges (max V 245..253, R-G 128..190). Cutting at the
    # lowest row that is pure lip leaves those fringes; cutting above them takes the lip.
    #
    # So the flat cut is only a SEED, and the flame is grown upward from it through ink that is
    # flame-coloured and cannot cross the lip:
    #     red fringe   R-G > 95      (the gold hull tops out at R-G 87)
    #     white core   R-G < 25 and B > 150   (the gold hull's blue channel stays low)
    # and any pixel at max V <= 150 blocks the flood, which is what the lip is.
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    V = a[:, :, :3].max(axis=2)
    flameish = opaque & (V > 150) & (((R - G) > 95) | (((R - G) < 25) & (B > 150)))
    grown = erase.copy()
    while True:
        p_ = np.pad(grown, 1, constant_values=False)
        nb = p_[:-2,1:-1] | p_[2:,1:-1] | p_[1:-1,:-2] | p_[1:-1,2:]
        add = nb & flameish & ~grown
        if not add.any(): break
        grown |= add
    erase = grown

    ring = ring_colour(a, opaque)
    out = a.copy()
    out[erase] = [0, 0, 0, 0]
    still = out[:, :, 3] > 40
    p = np.pad(still, 1, constant_values=False)
    touches = p[:-2,1:-1] | p[2:,1:-1] | p[1:-1,:-2] | p[1:-1,2:]
    reclose = erase & touches & ~still
    out[reclose] = [ring[0], ring[1], ring[2], 255]

    report.append((key, w, h, int(opaque.sum()), cut, cols, int(erase.sum()), int(reclose.sum()), ring))
    previews.append((key, cell, Image.fromarray(out.astype(np.uint8), 'RGBA')))
    if not PREVIEW:
        atlas.paste(Image.fromarray(out.astype(np.uint8), 'RGBA'), (x, y))

print('%-20s %-10s %-6s %-6s %-12s %-8s %-10s %s' %
      ('frame','size','ink','cut y','columns','erased','re-ringed','ring rgb'))
for key, w, h, ink, cut, cols, e, rc, ring in report:
    print('%-20s %-10s %-6d %-6d %-12s %-8d %-10d %s' %
          (key, '%dx%d'%(w,h), ink, cut, ('%d..%d'%cols) if cols else 'all', e, rc, ring))

if PREVIEW:
    Z, PAD = 5, 26
    tw = sum(p[1].width for p in previews) * 2 * Z + PAD * 5
    th = max(p[1].height for p in previews) * Z + 62
    sh = Image.new('RGBA', (tw, th), (22, 24, 29, 255)); dr = ImageDraw.Draw(sh)
    dr.text((14, 12), 'BAKED PLUME REMOVAL — before / after at %dx' % Z, fill=(255, 210, 140, 255))
    cx = PAD
    for key, before, after in previews:
        for lab_, im in (('BEFORE', before), ('AFTER', after)):
            z = im.resize((im.width * Z, im.height * Z), Image.NEAREST)
            sh.alpha_composite(z, (cx, 46))
            dr.text((cx + 4, 32), '%s  %s' % (key.replace('ship_', ''), lab_),
                    fill=(255, 150, 150, 255) if lab_ == 'BEFORE' else (150, 230, 160, 255))
            cx += z.width + PAD
    SC = os.environ.get('BOF_SCRATCH', ROOT)
    for key, before, after in previews:
        after.save(os.path.join(SC, 'after_' + key.replace('ship_', '') + '.png'))
    out = os.path.join(SC, 'plume_preview.png')
    sh.save(out); print('preview ->', out)
else:
    atlas.save(PNG); print('wrote', PNG)
