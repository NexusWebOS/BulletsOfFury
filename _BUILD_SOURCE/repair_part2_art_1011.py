"""Measured pose/anchor correction, called by the existing owning art builder."""
from pathlib import Path
import colorsys, hashlib, json, shutil
import numpy as np
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / '_ART_SOURCES/part2_1011'
OUT = ROOT / 'assets/game/shared/combat/part2_1010'
GEN = Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')

def save(bank, name, c, pivot, **meta):
    f = OUT / (name + '.png'); c.save(f, optimize=True)
    a = dict(key='p2_' + name, path=f.relative_to(ROOT).as_posix(), w=c.width, h=c.height,
             pivot=pivot, sha256=hashlib.sha256(f.read_bytes()).hexdigest(), opaque_bounds=c.getbbox(), **meta)
    bank.append(a); return a

def clean(cell):
    p = np.asarray(cell).copy(); p[p[:, :, 3] <= 20, 3] = 0
    return Image.fromarray(p)

def rect_for(im, i, cols, rows):
    cw, ch = im.width / cols, im.height / rows
    return [round(i % cols * cw), round(i // cols * ch), round((i % cols + 1) * cw), round((i // cols + 1) * ch)]

def palette(cell, hue):
    """Blue paint only: same alpha, non-paint pixels and RGB luminance."""
    p = np.asarray(cell).copy(); count = 0
    for y in range(cell.height):
        for x in range(cell.width):
            r, g, b, a = map(int, p[y, x])
            if not a or b <= 36 or b <= r * 1.20 or b <= g * 1.06: continue
            _, sat, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            lum = (.2126 * r + .7152 * g + .0722 * b) / 255
            for _ in range(24):
                rgb = colorsys.hsv_to_rgb(hue, sat, 1)
                peak = sum(v * w for v, w in zip(rgb, [.2126, .7152, .0722]))
                if peak >= lum: break
                sat *= .94
            p[y, x, :3] = [round(v * min(1, lum / peak) * 255) for v in rgb]; count += 1
    return Image.fromarray(p), count

def add_repaired_banks(bank):
    import prepare_part2_onion_1011
    for fn, target in [('exec-9d8fb132-b028-4420-bbf1-f7bd840a91e0.png', 'atom_inbetweens_raw.png'),
                       ('exec-3f166218-5243-4364-99b0-4d35e11c2060.png', 'fire_root_raw.png')]:
        if not (SRC / target).exists(): shutil.copyfile(GEN / fn, SRC / target)
    crops = json.loads((SRC / 'atom_source_crops.json').read_text())
    raw = Image.open(SRC / 'atom_inbetweens_raw.png').convert('RGBA'); inserts = {}
    for n, after in enumerate([3, 6, 15, 23]):
        rect = rect_for(raw, n, 2, 2); cell = clean(raw.crop(rect)); p = np.asarray(cell)
        ys, xs = np.nonzero(p[:, :, 3] >= 24); ground = int(ys.max()) + 1
        base = np.nonzero((p[:, :, 3] >= 24) & (np.indices(p.shape[:2])[0] >= ground - 7))[1]
        cx = (float(base.min()) + float(base.max()) + 1) / 2; k = .625
        c = Image.new('RGBA', (384, 576)); cell = cell.resize((round(cell.width * k), round(cell.height * k)), Image.Resampling.NEAREST)
        move = [round(192 - cx * k), round(480 - ground * k)]; c.alpha_composite(cell, move)
        inserts[after] = (c, dict(source='part2_1011/atom_inbetweens_raw.png', source_rect=rect,
            source_pivot=[cx, ground], scale=k, translation=move, parents=[after, after + 1]))
    bank['atom'] = []
    for i, crop in enumerate(crops):
        c = Image.open(SRC / f'atom_source_{i:02d}.png').convert('RGBA')
        save(bank['atom'], f'atom_{len(bank["atom"]):02d}', c, [192, 480], source='part2_1010/atom_raw.png',
             source_index=i, **{k: v for k, v in crop.items() if k != 'opaque_bounds'})
        if i in inserts:
            c, meta = inserts[i]; save(bank['atom'], f'atom_{len(bank["atom"]):02d}', c, [192, 480], **meta)
    assert len(bank['atom']) == 32
    raw = Image.open(ROOT / '_ART_SOURCES/part2_1010/fire_raw.png').convert('RGBA'); bank['fire'] = []
    for i in range(32):
        rect = rect_for(raw, i, 4, 8); cell = clean(raw.crop(rect)).transpose(Image.Transpose.ROTATE_180); p = np.asarray(cell)
        white = (p[:, :, 0] > 230) & (p[:, :, 1] > 220) & (p[:, :, 2] > 160) & (p[:, :, 3] > 180)
        peak = int(np.convolve(white.sum(axis=1), np.ones(5) / 5, mode='same').argmax())
        yy, xx = np.nonzero(white[max(0, peak - 3):peak + 4]); cx = float(np.median(xx))
        move = [round(192 - cx), 280 - peak]; c = Image.new('RGBA', (384, 384)); c.alpha_composite(cell, move)
        save(bank['fire'], f'fire_{i:02d}', c, [192, 280], source='part2_1010/fire_raw.png', source_rect=rect,
             scale=1, normalization=dict(muzzle=[cx, peak], translation=move), body_rect=[142, 143, 100, 102], muzzle_rect=[96, 218, 192, 148])
    raw = Image.open(SRC / 'fire_root_raw.png').convert('RGBA'); bank['fire_root'] = []
    for i in range(16):
        rect = rect_for(raw, i, 4, 4); cell = clean(raw.crop(rect)); p = np.asarray(cell)
        white = (p[:, :, 0] > 235) & (p[:, :, 1] > 220) & (p[:, :, 2] > 160) & (p[:, :, 3] > 180)
        lo, hi = round(cell.height * .75), round(cell.height * .90)
        peak = lo + int(np.convolve(white.sum(axis=1)[lo:hi], np.ones(5) / 5, mode='same').argmax())
        yy, xx = np.nonzero(white[max(lo, peak - 3):min(hi, peak + 4)]); cx = float(np.median(xx))
        cell = cell.crop((0, 0, cell.width, min(cell.height, peak + 33)))
        move = [round(192 - cx), 320 - peak]; c = Image.new('RGBA', (384, 384)); c.alpha_composite(cell, move)
        save(bank['fire_root'], f'fire_root_{i:02d}', c, [192, 320], source='part2_1011/fire_root_raw.png', source_rect=rect,
             scale=1, normalization=dict(contact=[cx, peak], translation=move), join_y=round(move[1] + 14), join_width=180)
    ace = ROOT / 'assets/game/levels/stage_06/boss/bosses/skycarrier'
    poses = [('idle', 'ace_top.png'), ('damaged', 'ace_damaged.png')] + [(f'br{i}', f'ace_br{i}.png') for i in range(8)]
    bank['stealth'] = []
    for role, hue in [('blue', None), ('red', .995), ('green', .33)]:
        for pose, fn in poses:
            file = ace / fn; original = Image.open(file).convert('RGBA')
            cell, count = (original, 0) if hue is None else palette(original, hue)
            c = Image.new('RGBA', (256, 256)); c.alpha_composite(cell, ((256 - cell.width) // 2, (256 - cell.height) // 2))
            save(bank['stealth'], f'stealth_{role}_{pose}', c, [128, 128], role=role, pose=pose,
                 source=file.relative_to(ROOT).as_posix(), source_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
                 scale=1, palette_pixels=count, palette='blue paint only; RGB luminance preserved; alpha and all non-paint pixels unchanged')
    audits = {}
    for name in ['atom', 'fire', 'fire_root']:
        cells = bank[name]; bounds = [c['opaque_bounds'] for c in cells]
        audits[name] = dict(frames=len(cells), unique_hashes=len({c['sha256'] for c in cells}),
            union_bounds=[min(b[0] for b in bounds), min(b[1] for b in bounds), max(b[2] for b in bounds), max(b[3] for b in bounds)],
            padded_edges=all(b[0] >= 2 and b[1] >= 2 and b[2] <= c['w'] - 2 and b[3] <= c['h'] - 2 for c, b in zip(cells, bounds)))
        assert audits[name]['padded_edges'], (name, audits[name]); assert audits[name]['unique_hashes'] == len(cells)
    (SRC / 'audit.json').write_text(json.dumps(audits, indent=2), encoding='utf-8')
    (SRC / 'provenance.json').write_text(json.dumps(dict(tool='built-in image_gen; measured registration; requested deterministic palette swaps',
        correction='Raw atomic sheet28 poses in7 rows: retain28 and add4 drawn inbetweens; no duplicated/interpolated poses',
        gutter_alpha_cutoff=20, banks={k: bank[k] for k in ['atom', 'fire', 'fire_root', 'stealth']}), indent=2), encoding='utf-8')
