"""Export the standalone reference art pack; never writes shipping game files.

Creative pixels come from the three retained imagegen sources. This owner only
separates sprites, adds shared padding, and makes proportional nearest exports.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import zipfile

import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, find_objects, label

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / '_ART_SOURCES/raiden_reference_1024'
OUT = ROOT / 'art-packs/raiden-reference-1024'
PROJECTILES = [
    ('amber_slug', 'Amber Slug', 'Ballistic', 'Compact machine-gun round.'),
    ('orange_tracer', 'Orange Tracer', 'Ballistic', 'Tapered high-visibility tracer.'),
    ('cyan_needle', 'Cyan Needle', 'Energy', 'Narrow single energy bolt.'),
    ('twin_needles', 'Twin Needles', 'Energy', 'Paired blue bolts in one sprite.'),
    ('ruby_drop', 'Ruby Drop', 'Energy', 'Red teardrop plasma shot.'),
    ('lime_dart', 'Lime Dart', 'Energy', 'Green pointed plasma round.'),
    ('micro_missile', 'Micro Missile', 'Missile', 'Steel homing-missile design with amber exhaust.'),
    ('blue_rocket', 'Blue Rocket', 'Missile', 'Blue fins and cyan exhaust.'),
    ('heavy_rocket', 'Heavy Rocket', 'Missile', 'Olive armored heavy rocket.'),
    ('red_torpedo', 'Red Torpedo', 'Missile', 'Silver body and red warhead.'),
    ('violet_rail_slug', 'Violet Rail Slug', 'Energy', 'Violet rail shot and short trailing sparks.'),
    ('triple_crescent', 'Triple Crescent', 'Special', 'Three gold blades around a hot core.'),
    ('blue_plasma', 'Blue Plasma', 'Orb', 'Cobalt shell and white plasma core.'),
    ('fire_orb', 'Fire Orb', 'Orb', 'Orange flame shell and hot center.'),
    ('ice_orb', 'Ice Orb', 'Orb', 'Angular cyan and white ice energy.'),
    ('lightning_orb', 'Lightning Orb', 'Orb', 'Yellow electrical branches.'),
    ('acid_orb', 'Acid Orb', 'Orb', 'Lime energy with satellite sparks.'),
    ('nova_orb', 'Nova Orb', 'Orb', 'Red shell and sharp yellow nova rays.'),
    ('void_orb', 'Void Orb', 'Orb', 'Purple rim and dark central aperture.'),
    ('vortex_orb', 'Vortex Orb', 'Orb', 'Turquoise spiral energy.'),
    ('gravity_orb', 'Gravity Orb', 'Orb', 'Rocky amber center and thin orbit ring.'),
    ('sonic_pulse', 'Sonic Pulse', 'Special', 'Concentric cobalt and white pulse.'),
    ('helix_pulse', 'Helix Pulse', 'Special', 'Green double helix and white core.'),
    ('ion_orb', 'Ion Orb', 'Orb', 'Magenta clustered ion burst.'),
]
LASERS = [
    ('cyan_lance', 'Cyan Lance', 'Laser', 'Narrow white-core cyan beam.'),
    ('twin_cobalt', 'Twin Cobalt', 'Laser', 'Two parallel blue lances.'),
    ('magenta_trident', 'Magenta Trident', 'Laser', 'Three connected magenta prongs.'),
    ('plasma_column', 'Plasma Column', 'Laser', 'Orange-red plasma stream.'),
    ('arc_lightning', 'Arc Lightning', 'Laser', 'Yellow branching electrical column.'),
    ('green_helix', 'Green Helix', 'Laser', 'Green coil around a white and cyan center.'),
    ('void_chain', 'Void Chain', 'Laser', 'Purple segmented column with dark apertures.'),
    ('crystal_lance', 'Crystal Lance', 'Laser', 'Icy lance with angular crystal edges.'),
    ('flame_jet', 'Flame Jet', 'Special', 'Continuous orange flame column.'),
    ('rail_streak', 'Rail Streak', 'Laser', 'Silver-blue streak with repeated shock bands.'),
    ('sonic_spiral', 'Sonic Spiral', 'Special', 'Turquoise spiraling column.'),
    ('gold_charge', 'Gold Charge', 'Laser', 'Broad gold charged beam.'),
]
ENEMIES = [
    ('steel_interceptor', 'Steel Interceptor', 'Air', 'Swept-wing light fighter; suggested attack: paired needles.', 'twin_needles'),
    ('olive_attack_jet', 'Olive Attack Jet', 'Air', 'Twin-engine assault aircraft; suggested attack: short tracer fans.', 'orange_tracer'),
    ('red_needle_fighter', 'Red Needle Fighter', 'Air', 'Slender interceptor; suggested attack: committed straight rail shots.', 'violet_rail_slug'),
    ('teal_strike_drone', 'Teal Strike Drone', 'Air', 'Compact twin-boom drone; suggested attack: cyan bolts.', 'cyan_needle'),
    ('ember_gunship', 'Ember Gunship', 'Air', 'Heavy orange craft; suggested attack: alternating rotary bursts.', 'amber_slug'),
    ('delta_bomber', 'Delta Bomber', 'Air', 'Silver delta aircraft; suggested attack: spaced heavy rockets.', 'heavy_rocket'),
    ('quad_nacelle_cruiser', 'Quad-Nacelle Cruiser', 'Air', 'Four-engine armored craft; suggested attack: slow plasma volleys.', 'blue_plasma'),
    ('violet_stealth_wing', 'Violet Stealth Wing', 'Air', 'Wide stealth wing; suggested attack: twin violet beams.', 'void_chain'),
    ('scout_tank', 'Scout Tank', 'Armor', 'Compact tracked cannon tank; suggested attack: aimed single rounds.', 'orange_tracer'),
    ('twin_cannon_tank', 'Twin-Cannon Tank', 'Armor', 'Tan heavy armor; suggested attack: alternating barrel shots.', 'ruby_drop'),
    ('rocket_carrier', 'Rocket Carrier', 'Armor', 'Tracked four-rocket carrier; suggested attack: staggered missiles.', 'micro_missile'),
    ('wheeled_flak', 'Wheeled Flak', 'Armor', 'Six-wheel armored vehicle; suggested attack: brief flak fans.', 'amber_slug'),
    ('cannon_bunker', 'Cannon Bunker', 'Fixture', 'Low cannon emplacement; suggested attack: slow heavy rounds.', 'fire_orb'),
    ('missile_battery', 'Missile Battery', 'Fixture', 'Fixed missile battery; suggested attack: separated rocket launches.', 'red_torpedo'),
    ('river_patrol', 'River Patrol', 'Naval', 'Narrow patrol boat; suggested attack: short aimed spread.', 'lime_dart'),
    ('iron_siege_craft', 'Iron Siege Craft', 'Heavy', 'Whole armored siege aircraft; suggested attack: alternating main-beam lanes.', 'plasma_column'),
]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def image_save(im, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, optimize=True)


def projectile_crops(im):
    """Use measured silhouettes: the source missed its requested grid spacing.

    Both halves of the twin shot share one owner. Detached sparks attach to the
    nearest actual silhouette. A common 288px canvas contains the 264px rocket
    and its padding without shrinking or changing any sprite's proportions.
    """
    rgba = np.asarray(im)
    labels, _ = label(rgba[:, :, 3] > 16)
    seeds = np.zeros(labels.shape, dtype=np.int16)
    for identity, sl in enumerate(find_objects(labels), 1):
        if sl is None or np.count_nonzero(labels[sl] == identity) <= 1000:
            continue
        row = min(3, max(0, ((sl[0].start + sl[0].stop) // 2) // 256))
        col = min(5, max(0, ((sl[1].start + sl[1].stop) // 2) // 256))
        seeds[labels == identity] = 1 + row * 6 + col
    assert len(np.unique(seeds)) == 25
    _, near = distance_transform_edt(seeds == 0, return_indices=True)
    owners = seeds[tuple(near)]
    result = []
    for number in range(1, 25):
        yy, xx = np.where((rgba[:, :, 3] > 16) & (owners == number))
        x0, y0 = max(0, int(xx.min()) - 8), max(0, int(yy.min()) - 8)
        x1, y1 = min(im.width, int(xx.max()) + 9), min(im.height, int(yy.max()) + 9)
        crop = rgba[y0:y1, x0:x1].copy()
        crop[owners[y0:y1, x0:x1] != number] = 0
        assert x1 - x0 <= 288 and y1 - y0 <= 288
        frame = Image.new('RGBA', (288, 288))
        offset = ((288 - crop.shape[1]) // 2, (288 - crop.shape[0]) // 2)
        frame.paste(Image.fromarray(crop), offset)
        result.append((frame, [x0, y0, x1 - x0, y1 - y0], list(offset)))
    return result


def enemy_crops(im):
    """Measure 16 actual opaque hulls, keeping their original alpha and RGB.

    The generated arrangement is not an exact grid. Nearest opaque silhouette
    ownership separates faint antialias pixels between neighboring hulls. The
    source is retained unchanged. Thresholds measure ownership, not output alpha.
    """
    rgba = np.asarray(im)
    labels, _ = label(rgba[:, :, 3] > 16)
    pieces = []
    for identity, sl in enumerate(find_objects(labels), 1):
        if sl is not None and np.count_nonzero(labels[sl] == identity) > 5000:
            pieces.append((identity, sl))
    assert len(pieces) == 16, f'Expected sixteen hulls; found {len(pieces)}'
    pieces.sort(key=lambda item: ((item[1][0].start + item[1][0].stop) // 600, item[1][1].start))
    seeds = np.zeros(labels.shape, dtype=np.int16)
    for number, (identity, _) in enumerate(pieces, 1):
        seeds[labels == identity] = number
    _, near = distance_transform_edt(seeds == 0, return_indices=True)
    owners = seeds[tuple(near)]
    result = []
    for number, (_, sl) in enumerate(pieces, 1):
        x0, y0 = max(0, sl[1].start - 8), max(0, sl[0].start - 8)
        x1, y1 = min(im.width, sl[1].stop + 8), min(im.height, sl[0].stop + 8)
        crop = rgba[y0:y1, x0:x1].copy()
        crop[owners[y0:y1, x0:x1] != number] = 0
        assert x1 - x0 <= 384 and y1 - y0 <= 384
        frame = Image.new('RGBA', (384, 384))
        offset = ((384 - crop.shape[1]) // 2, (384 - crop.shape[0]) // 2)
        frame.paste(Image.fromarray(crop), offset)
        result.append((frame, [x0, y0, x1 - x0, y1 - y0], list(offset)))
    return result


def make_sheet(frames, columns, cell, gutter, padding):
    rows = math.ceil(len(frames) / columns)
    size = (columns * cell[0] + (columns - 1) * gutter + 2 * padding,
            rows * cell[1] + (rows - 1) * gutter + 2 * padding)
    sheet = Image.new('RGBA', size)
    rects = []
    for i, frame in enumerate(frames):
        x = padding + (i % columns) * (cell[0] + gutter)
        y = padding + (i // columns) * (cell[1] + gutter)
        sheet.paste(frame, (x, y))
        rects.append([x, y, *cell])
    return sheet, rects


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    catalog = {'title': 'Arcade Armory & Enemy Roster', 'version': 1,
               'created': '2026-10-24', 'status': 'Standalone static art pack; not installed in gameplay.',
               'generator': 'Built-in image_gen; three reference-guided sheets.',
               'builder': '_BUILD_SOURCE/build_raiden_pack_1024.py',
               'frame_count_per_asset': 1, 'animations': False,
               'scale_policy': 'Master pixels kept at source scale 1; all native exports use uniform 0.5 nearest-neighbor scale.',
               'source': {}, 'sheets': [], 'assets': []}
    groups = [('projectiles', PROJECTILES, (288, 288), 6),
              ('lasers', LASERS, (256, 512), 6),
              ('enemies', ENEMIES, (384, 384), 4)]
    for group, specs, cell, columns in groups:
        path = SRC / 'source' / f'{group}.png'
        im = Image.open(path).convert('RGBA')
        catalog['source'][group] = {'path': str(path.relative_to(ROOT)).replace('\\', '/'),
                                     'size': list(im.size), 'sha256': sha(path)}
        if group == 'projectiles':
            crops = projectile_crops(im)
        elif group == 'enemies':
            crops = enemy_crops(im)
        else:
            assert im.size == (1536, 1024)
            crops = []
            for i in range(len(specs)):
                x, y = (i % columns) * cell[0], (i // columns) * cell[1]
                crops.append((im.crop((x, y, x + cell[0], y + cell[1])), [x, y, *cell], [0, 0]))
        masters, natives, records = [], [], []
        for spec, (master, source_rect, offset) in zip(specs, crops):
            key, name, role, description = spec[:4]
            native = master.resize((cell[0] // 2, cell[1] // 2), Image.Resampling.NEAREST)
            for exported in (master, native):
                alpha = np.asarray(exported)[:, :, 3]
                assert all(np.all(edge < 64) for edge in (alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1])), f'Clipped export: {key}'
            file_master, file_native = f'master/{group}/{key}.png', f'native/{group}/{key}.png'
            image_save(master, OUT / file_master)
            image_save(native, OUT / file_native)
            record = dict(id=key, name=name, group=group, role=role, description=description,
                          master=file_master, native=file_native, master_size=list(cell),
                          native_size=list(native.size), pivot=[cell[0] // 2, cell[1] // 2],
                          native_pivot=[cell[0] // 4, cell[1] // 4],
                          source_rect=source_rect, source_offset=offset,
                          alpha_bbox=list(master.getchannel('A').getbbox()),
                          master_sha256=sha(OUT / file_master), native_sha256=sha(OUT / file_native),
                          direction='south' if group == 'enemies' else 'north')
            if len(spec) > 4:
                record['suggested_weapon'] = spec[4]
            masters.append(master)
            natives.append(native)
            records.append(record)
        for resolution, frames, size, gutter, pad in [
                ('master', masters, cell, 8, 8),
                ('native', natives, (cell[0] // 2, cell[1] // 2), 4, 4)]:
            sheet, rects = make_sheet(frames, columns, size, gutter, pad)
            sheet_file = f'sheets/{group}-{resolution}.png'
            image_save(sheet, OUT / sheet_file)
            catalog['sheets'].append(dict(group=group, resolution=resolution, path=sheet_file,
                                         size=list(sheet.size), cell_size=list(size), columns=columns,
                                         rows=math.ceil(len(frames) / columns), gutter=gutter,
                                         padding=pad, sha256=sha(OUT / sheet_file)))
            for record, rect, frame in zip(records, rects, frames):
                record[f'{resolution}_sheet'] = sheet_file
                record[f'{resolution}_sheet_rect'] = rect
                assert np.array_equal(np.asarray(sheet.crop((rect[0], rect[1], rect[0]+rect[2], rect[1]+rect[3]))), np.asarray(frame))
        catalog['assets'].extend(records)
    from raiden_modular_1024 import extend_catalog
    extend_catalog(catalog, SRC, OUT)
    ids = {a['id'] for a in catalog['assets']}
    assert len(ids) == len(catalog['assets']) == 60
    for a in catalog['assets']:
        assert all(n % 2 == 0 for n in a['master_size'] + a['native_size'])
        if 'suggested_weapon' in a:
            assert a['suggested_weapon'] in ids
    manifest = json.dumps(catalog, indent=2) + '\n'
    (OUT / 'manifest.json').write_text(manifest, encoding='utf-8')
    (OUT / 'catalog.js').write_text('window.ART_PACK = ' + manifest.rstrip() + ';\n', encoding='utf-8')
    with (OUT / 'enemy-roster.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['id', 'name', 'tier', 'role', 'suggested_weapon', 'modules', 'description', 'native_png', 'master_png'])
        for a in catalog['assets']:
            if a.get('modular'):
                writer.writerow([a['id'], a['name'], a['tier'], a['role'], a['suggested_weapon'], '; '.join(p['id'] for p in a['parts']), a['description'], a['native'], a['master']])
    print(f'BUILD COMPLETE: 60 assemblies/effects, {catalog["module_count"]} modules, {len(catalog["sheets"])} category sheets.')
    return catalog


def package():
    archive = OUT.parent / 'raiden-reference-1024.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in sorted(OUT.rglob('*')):
            if path.is_file():
                z.write(path, str(path.relative_to(OUT.parent)))
    print(f'ZIP: {archive.relative_to(ROOT)} ({archive.stat().st_size:,} bytes)')


if __name__ == '__main__':
    build()
    package()
