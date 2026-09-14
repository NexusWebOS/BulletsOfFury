#!/usr/bin/env python3
"""
spaceship_somersault_0913a.py - THE FURY SPACESHIP'S SOMERSAULT REEL, APPENDED TO THE SPACE ATLAS.

    python _BUILD_SOURCE/spaceship_somersault_0913a.py [--check]

Mike (0913): "Show the spaceship transformation scene and make it properly fixed and working in-game."
In space a somersault never flipped the ship: gravityModeDrawShip only knew ship_base, the bank row and the
17-frame ROLL cycle, so the double-tap-UP flip played the level plate for its whole 0.62 s.

⚠ A SOMERSAULT IS A PITCH, NOT A ROLL (CLAUDE.md 0912a: "so IS NOT br"). ship_roll_00..16 is the recovered
barrel-roll cycle - a roll presents the CHORD and keeps its height. Aliasing it would ship a barrel roll wearing
a somersault's name. So the reel is DERIVED from the spaceship's own level plate, ship_base, by exactly the
method Lizzie's reel used (_BUILD_SOURCE/lizzie_somersault_0912a.py): the pitch profile measured off Maverick's
authored eight, applied to the plate.

    frame       so0   so1   so2   so3   so4   so5   so6   so7
    height/so0  1.00  0.81  0.44  0.89  0.96  0.88  0.54  0.81
    width /so0  1.00  1.08  1.12  1.07  0.99  1.04  1.12  1.08
    surface     top   top   EDGE  belly belly belly EDGE  top

Two deliberate differences from Lizzie's script, both forced by this atlas:
  1. A FIXED CANVAS, NOT A TRIM. This atlas has no ox/oy offsets, and gravityModeDrawShip scales every frame to
     its draw height - so a trimmed 0.44-tall frame would be stretched back to full height and the pitch would
     vanish. All eight frames sit on one 153x148 canvas (ship_base's 148 height; its width grown for the 1.12
     span), centred where ship_base's own ink is centred, so a frame drawn at the ship's height lands at
     exactly ship_base's scale and the collapse is real.
  2. NO HOT-PIXEL EXEMPTION ON THE BELLY. Lizzie's belly pass kept lum>205 pixels because her plate carries a
     BAKED PLUME, which is brighter from below. ship_base carries no plume (the thruster is a separate reel
     drawn under it); its 699 pixels over that threshold are top-surface steel speculars, which the underside
     does not have. So the whole hull is shaded.

⚠ THE PILOT PALETTE COMES WITH IT. Every pilot-colourable frame in this atlas has a `_blue` luminance mask
beside it (the 0827b blue-only contract: spaceAtlasCanvas tints that mask and nothing else). Each pitch frame's
mask is ship_base_blue put through the SAME resize, with its grey scaled by the same shade factor, so the tint
covers exactly the accent pixels of the transformed frame and darkens on the belly with them.

⚠ APPENDED, NOT REPACKED. The eight frames and eight masks go into one new shelf below the existing packing, so
no existing rect moves - the PNG, the .json and the .js map are written in ONE run and the script refuses to run
twice. build_gravity_mode_v2.py would repack from sources and drop these; if it is ever re-run, run this after.
"""
import os, sys, json, argparse
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ATLAS_DIR = os.path.join(ROOT, 'assets', 'game', 'atlas')
PNG = os.path.join(ATLAS_DIR, 'bof_gravity_mode_space_weapons.png')
JSONF = os.path.join(ATLAS_DIR, 'bof_gravity_mode_space_weapons.json')
JSF = os.path.join(ATLAS_DIR, 'bof_gravity_mode_space_weapons.js')
PROOF = os.path.join(ROOT, 'docs', 'proofs', 'spaceship_0913a')

# measured off ship_maverick_so0..so7 - the same table lizzie_somersault_0912a.py applies
VSC = [1.00, 0.81, 0.44, 0.89, 0.96, 0.88, 0.54, 0.81]
HSC = [1.00, 1.08, 1.12, 1.07, 0.99, 1.04, 1.12, 1.08]
BELLY = [0, 0, 0, 1, 1, 1, 0, 0]
EDGE = [0, 0, 1, 0, 0, 0, 1, 0]
PAD = 4                      # the atlas packer's own gutter
CANVAS_H = 148               # ship_base's cell height: same draw height => same scale


def neutralize_ship_edge_purple(im, passes=10):
    """Copied from build_gravity_mode_v2.py (importing that module RUNS the whole atlas build). LANCZOS can pull
    a key-coloured value back into a boundary pixel; the ship frames there all get this pass after resizing."""
    a = np.asarray(im.convert('RGBA')).copy()
    opaque = a[..., 3] > 0
    near_clear = ~opaque
    for _ in range(max(1, passes)):
        e = near_clear.copy()
        e[1:] |= near_clear[:-1]; e[:-1] |= near_clear[1:]
        e[:, 1:] |= near_clear[:, :-1]; e[:, :-1] |= near_clear[:, 1:]
        near_clear = e
    rgb = a[..., :3].astype(int)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    purple = (r > g + 10) & (b > g + 18) & (r > 35) & (b > 35)
    rim = opaque & near_clear & purple
    shades = np.asarray(((6, 9, 13), (12, 16, 22), (19, 24, 32), (27, 33, 43), (38, 45, 56)), dtype=np.uint8)
    lum = (r * 21 + g * 72 + b * 7) // 100
    band = np.clip(lum * len(shades) // 96, 0, len(shades) - 1)
    a[rim, :3] = shades[band[rim]]
    a[~opaque, :3] = 0
    return Image.fromarray(a, 'RGBA')


def belly(im):
    """Lizzie's underside: 62% value, pulled 45% toward its own luminance, a hair cool. No plume exemption -
    see the header."""
    a = np.asarray(im).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = (r * 299 + g * 587 + b * 114) / 1000.0
    out = a.copy()
    out[..., 0] = (r * 0.55 + lum * 0.45) * 0.62
    out[..., 1] = (g * 0.55 + lum * 0.45) * 0.62
    out[..., 2] = (b * 0.55 + lum * 0.45) * 0.66
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGBA')


def edge_shade(im):
    a = np.asarray(im).astype(np.float32)
    a[..., 0] *= 0.84; a[..., 1] *= 0.84; a[..., 2] *= 0.88
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def shade_mask(im, k):
    """a mask is grey luminance in RGB; darken it by the frame's own shade factor, keep it grey"""
    a = np.asarray(im).astype(np.float32)
    a[..., :3] *= k
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def build(plate, mask):
    bb = plate.getbbox()
    body, mbody = plate.crop(bb), mask.crop(bb)
    bw, bh = body.size
    cx, cy = (bb[0] + bb[2]) / 2.0, (bb[1] + bb[3]) / 2.0
    # grow the canvas symmetrically about the plate's ink centre so the widest frame fits
    span = max(int(round(bw * s)) for s in HSC)
    cw = max(plate.width, span + 2 * 3)
    cw += (cw - plate.width) % 2          # keep the centre on the same pixel column
    ox = (cw - plate.width) // 2
    frames, masks = [], []
    for i in range(8):
        nw, nh = max(1, int(round(bw * HSC[i]))), max(1, int(round(bh * VSC[i])))
        f = body.resize((nw, nh), Image.LANCZOS)
        m = mbody.resize((nw, nh), Image.LANCZOS)
        if BELLY[i]:
            f, m = belly(f), shade_mask(m, 0.62)
        elif EDGE[i]:
            f, m = edge_shade(f), shade_mask(m, 0.84)
        f = neutralize_ship_edge_purple(f, passes=10)
        px, py = int(round(ox + cx - nw / 2.0)), int(round(cy - nh / 2.0))
        c = Image.new('RGBA', (cw, CANVAS_H), (0, 0, 0, 0)); c.alpha_composite(f, (px, py))
        cm = Image.new('RGBA', (cw, CANVAS_H), (0, 0, 0, 0)); cm.alpha_composite(m, (px, py))
        frames.append(c); masks.append(cm)
    return frames, masks, (cw, CANVAS_H), ox


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='build and write the proof only; touch no atlas file')
    a = ap.parse_args()
    raw_json = open(JSONF, encoding='utf-8').read()
    raw_js = open(JSF, encoding='utf-8').read()
    meta = json.loads(raw_json)
    frames_meta = meta['frames']
    # both map files must be exactly what the atlas builder writes, or a rewrite would reformat every entry
    if json.dumps(meta, indent=2) + '\n' != raw_json:
        raise SystemExit('the .json is not in build_gravity_mode_v2.py format - refusing to rewrite it')
    js_meta = json.loads(raw_js[len('window.BOF_GRAVITY_ATLAS='):].rstrip().rstrip(';'))
    if 'window.BOF_GRAVITY_ATLAS=' + json.dumps(js_meta, separators=(',', ':')) + ';\n' != raw_js:
        raise SystemExit('the .js is not in build_gravity_mode_v2.py format - refusing to rewrite it')
    if js_meta != meta:
        raise SystemExit('the .js and .json maps disagree - refusing to append to either')
    if 'ship_so_00' in frames_meta:
        raise SystemExit('the atlas already carries ship_so_00 - this script appends, it does not rebuild')
    atlas = Image.open(PNG).convert('RGBA')
    W, H = atlas.size
    bottom = max(r['y'] + r['h'] for r in frames_meta.values())
    if bottom + PAD > H:
        raise SystemExit('a rect reaches past the atlas bottom (%d > %d)' % (bottom + PAD, H))
    r0 = frames_meta['ship_base']
    plate = atlas.crop((r0['x'], r0['y'], r0['x'] + r0['w'], r0['y'] + r0['h']))
    rm = frames_meta['ship_base_blue']
    mask = atlas.crop((rm['x'], rm['y'], rm['x'] + rm['w'], rm['y'] + rm['h']))
    frames, masks, (cw, ch), ox = build(plate, mask)

    # one new shelf below everything
    y0 = H
    new_h = H + ch + PAD
    out = Image.new('RGBA', (W, new_h), (0, 0, 0, 0))
    out.alpha_composite(atlas, (0, 0))
    x = PAD
    add = {}
    for i in range(8):
        for key, im in (('ship_so_%02d' % i, frames[i]), ('ship_so_%02d_blue' % i, masks[i])):
            if x + im.width + PAD > W:
                raise SystemExit('the shelf overflowed the atlas width')
            out.alpha_composite(im, (x, y0))
            add[key] = {'x': x, 'y': y0, 'w': im.width, 'h': im.height}
            x += im.width + PAD

    # nothing that was already packed may change by one pixel
    if not np.array_equal(np.asarray(out)[:H], np.asarray(atlas)):
        raise SystemExit('the append changed existing pixels - aborting')

    os.makedirs(PROOF, exist_ok=True)
    tile = 3
    sheet = Image.new('RGB', ((cw * tile // 2 + 8) * 9, ch * tile // 2 * 2 + 70), (12, 14, 20))
    d = ImageDraw.Draw(sheet)
    d.text((8, 6), 'ship_base + ship_so_00..07 (pitch, Maverick profile) - top: frame, bottom: its blue mask', fill=(245, 190, 80))
    cells = [('ship_base', plate, mask)] + [('ship_so_%02d' % i, frames[i], masks[i]) for i in range(8)]
    for k, (name, f, m) in enumerate(cells):
        xx = 4 + k * (cw * tile // 2 + 8)
        pad = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        pad.alpha_composite(f, (0 if f.width == cw else ox, 0))
        fm = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        fm.alpha_composite(m, (0 if m.width == cw else ox, 0))
        for row, im in enumerate((pad, fm)):
            bg = Image.new('RGBA', (cw, ch), (26, 30, 40, 255)); bg.alpha_composite(im)
            big = bg.resize((cw * tile // 2, ch * tile // 2), Image.NEAREST).convert('RGB')
            sheet.paste(big, (xx, 24 + row * (ch * tile // 2 + 4)))
        d.text((xx + 2, sheet.height - 18), name, fill=(220, 222, 230))
    sheet.save(os.path.join(PROOF, '00_somersault_reel_build.png'))
    print('canvas %dx%d, shelf y=%d, atlas %dx%d -> %dx%d' % (cw, ch, y0, W, H, W, new_h))
    for k in sorted(add):
        print('  %-18s %s' % (k, add[k]))
    if a.check:
        print('--check: atlas untouched')
        return
    meta2 = {'image': meta['image'], 'frames': dict(frames_meta)}
    meta2['frames'].update(add)
    out.save(PNG, optimize=True)
    open(JSONF, 'w', encoding='utf-8', newline='\n').write(json.dumps(meta2, indent=2) + '\n')
    open(JSF, 'w', encoding='utf-8', newline='\n').write('window.BOF_GRAVITY_ATLAS=' + json.dumps(meta2, separators=(',', ':')) + ';\n')
    back = Image.open(PNG).convert('RGBA')
    if back.size != (W, new_h) or not np.array_equal(np.asarray(back), np.asarray(out)):
        raise SystemExit('the saved PNG does not read back as written')
    print('wrote %s, %s, %s (+%d frames)' % (os.path.basename(PNG), os.path.basename(JSONF), os.path.basename(JSF), len(add)))


if __name__ == '__main__':
    main()
