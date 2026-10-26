"""Register provenance for the existing authored DNA-formation source banks."""
from pathlib import Path
from PIL import Image
import numpy as np
import hashlib
import json
import re

R = Path(__file__).resolve().parents[1]
O = R / '_BUILD_SOURCE/dracodia_dna_1026'
O.mkdir(exist_ok=True)
runtime = R / 'assets/dracodia_dna_1026.js'
crop = [int(v) for v in re.search(r'crop:\[([\d,]+)\]', runtime.read_text()).group(1).split(',')]
assert crop[2] % 2 == crop[3] % 2 == 0
sources = []
palette_banks = {}
palette_dir = R / 'assets/game/levels/stage_08/boss/dracodia_dna_1026'
palette_dir.mkdir(exist_ok=True)
stops = np.array([[0,0,0],[24,9,40],[80,25,117],[177,33,157],[242,62,139],[255,163,205],[255,236,248],[255,255,255]], dtype=float)
weights = np.array([.2126,.7152,.0722])
levels = stops @ weights
metrics = []
for file, bank in [('assets/alien_arena_art_1005.js', 'code'), ('assets/survivor_art_1010.js', 'crawl')]:
    text = (R / file).read_text(encoding='utf8')
    data = json.JSONDecoder().raw_decode(text[text.index('{'):])[0]
    count = len(data[bank]); cols = 4 if bank == 'code' else 8
    cell_w = data[bank][0]['w']; cell_h = data[bank][0]['h']
    sheet = Image.new('RGBA', (cols * cell_w, ((count + cols - 1) // cols) * cell_h))
    for index, a in enumerate(data[bank]):
        p = R / a['path']
        im = Image.open(p)
        assert all(v % 2 == 0 for v in im.size)
        if bank == 'code':
            assert crop[0] + crop[2] <= im.width and crop[1] + crop[3] <= im.height
        sources.append({'key': a['key'], 'path': a['path'], 'size': list(im.size),
                        'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                        'role': 'authored binary strand' if bank == 'code' else 'authored liquid symbiote lobe'})
        raw = np.array(im.convert('RGBA')); rgb = raw[:,:,:3].astype(float); luminance = rgb @ weights
        green = (rgb[:,:,1] > rgb[:,:,0] * 1.14) & (rgb[:,:,1] > rgb[:,:,2] * 1.08)
        mapped = np.stack([np.interp(luminance, levels, stops[:,i]) for i in range(3)], axis=-1)
        result = raw.copy(); result[:,:,:3] = np.where(green[:,:,None], np.rint(mapped), rgb).astype(np.uint8)
        assert np.array_equal(result[:,:,3], raw[:,:,3])
        error = float(np.abs(result[:,:,:3] @ weights - luminance).max())
        assert error <= .51
        metrics.append({'key': a['key'], 'changedPixels': int(green.sum()), 'maxLuminanceError': error, 'alphaPreserved': True})
        sheet.alpha_composite(Image.fromarray(result), (index % cols * cell_w, index // cols * cell_h))
    kind = 'code' if bank == 'code' else 'fluid'; dest = palette_dir / (kind + '-palette.webp')
    sheet.save(dest, lossless=True, method=6)
    decoded = np.array(Image.open(dest).convert('RGBA'))
    for index, a in enumerate(data[bank]):
        raw = np.array(Image.open(R / a['path']).convert('RGBA'))
        x, y = index % cols * cell_w, index // cols * cell_h
        cell = decoded[y:y+cell_h,x:x+cell_w]
        assert np.array_equal(cell[:,:,3], raw[:,:,3])
        visible = raw[:,:,3] > 0
        error = float(np.abs(cell[:,:,:3] @ weights - raw[:,:,:3] @ weights)[visible].max())
        assert error <= .51
        metrics[-count+index].update({'decodedAlphaPreserved': True, 'decodedMaxLuminanceError': error})
    palette_banks[kind] = {'key': 'rd28p_' + kind, 'path': dest.relative_to(R).as_posix(),
                           'w': cell_w, 'h': cell_h, 'cols': cols, 'count': count,
                           'sha256': hashlib.sha256(dest.read_bytes()).hexdigest()}
(R / 'assets/dracodia_dna_palette_1026.js').write_text("'use strict';\nconst RD28_PALETTE=" + json.dumps(palette_banks, separators=(',',':')) + ';\n', encoding='utf8')
manifest = {'owner': '_BUILD_SOURCE/build_dracodia_dna_1026.py',
            'runtime': runtime.relative_to(R).as_posix(), 'generatedCredits': 0,
            'sourceCount': len(sources), 'codeCrop': crop,
            'fragmentCell': [64, 64], 'skinCanvas': [256, 256],
            'normalization': 'Native even source canvases, common crop, proportional transforms only. Original canvases/crops preserved; two isolated palette-only sheets, no shared atlas edits or per-pose fitting.',
            'timing': {'start': 6.2, 'skeleton': 7, 'absorb': 13.8, 'finished': 15.8},
            'source': sources, 'palette': {'stops': stops.tolist(), 'banks': palette_banks, 'metrics': metrics,
                                          'note': 'Dracodia violet/red-magenta energy and pale highlights. Green-biased pixels only; native alpha, luminance and dark metallic outlines retained.'}}
(O / 'source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf8')
taxonomy = R / 'assets/data/ART_TAXONOMY.json'
raw = taxonomy.read_bytes()
if 'rd28p_' not in json.loads(raw.decode('utf8')):
    entry = {'rd28p_': {'role': 'dracodia_living_dna_final_form_palette', 'sheet': None,
                       'owner': '_BUILD_SOURCE/build_dracodia_dna_1026.py',
                       'manifest': '_BUILD_SOURCE/dracodia_dna_1026/source-manifest.json',
                       'note': 'Mike October26: isolated violet/red-magenta DNA code12 and liquid32 palette sheets retain native cells, alpha, luminance, dark outlines and highlights. Original green sources and other scenes stay unchanged.'}}
    fragment = json.dumps(entry, indent=2, ensure_ascii=False)[1:-2] + ','
    if b'\r\n' in raw:
        fragment = fragment.replace('\n', '\r\n')
    pos = raw.index(b'{') + 1
    updated = raw[:pos] + fragment.encode('utf8') + raw[pos:]
    json.loads(updated.decode('utf8'))
    taxonomy.write_bytes(updated)
print(json.dumps({'sourceCount': len(sources), 'codeCrop': crop, 'newPaletteSheets': 2}))
