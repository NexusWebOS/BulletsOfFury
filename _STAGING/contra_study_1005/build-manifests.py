"""Read-only image analysis; preserves all authored RGBA pixels."""
from pathlib import Path
from PIL import Image
import json, hashlib

root = Path(__file__).resolve().parent
path = root / 'art' / 'reactor_pressure_discharge.png'
im = Image.open(path)
w, h = im.size
assert im.mode == 'RGBA' and w % 4 == 0 and h % 3 == 0
cw, ch = w // 4, h // 3
assert cw == ch
alpha = im.getchannel('A')
frames = []
for i in range(12):
    x, y = i % 4 * cw, i // 4 * ch
    a = alpha.crop((x, y, x + cw, y + ch))
    bbox = a.point(lambda p: 255 if p >= 16 else 0).getbbox()
    margins = [bbox[0], bbox[1], cw - bbox[2], ch - bbox[3]]
    frames.append({'frame': i, 'sourceRect': [x, y, cw, ch],
                   'pivot': [cw / 2, ch / 2], 'alphaBoundsAt16': list(bbox),
                   'minimumSignificantAlphaPadding': min(margins)})
manifest = {'id': 'bof_study_pressure_1005', 'status': 'candidate_native_review_required',
            'file': 'reactor_pressure_discharge.png', 'mode': 'RGBA',
            'nativeSize': [w, h], 'grid': [4, 3], 'cellSize': [cw, ch],
            'requestedSize': [1024, 768], 'fps': 20, 'loop': False,
            'durationSeconds': .6, 'sampling': 'nearest', 'collision': 'cosmetic_only',
            'alphaExtrema': list(alpha.getextrema()), 'frames': frames,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'generator': 'OpenAI built-in imagegen; new original asset; no Contra pixels supplied',
            'promptFile': 'generation-prompt.txt',
            'sourceOriginal': r'C:\Users\Mike\.codex\generated_images\01a10ef4-27c3-71d2-97c8-0d9fa5c0bb2f\exec-af924243-184c-4727-850c-f01c63a5c7ff.png',
            'processing': 'Exact copy; alpha and cell bounds analyzed only; no raster edits',
            'qa': {'transparentBackground': alpha.getextrema()[0] == 0,
                   'squareEqualCells': cw == ch,
                   'requested12PixelPaddingMet': min(f['minimumSignificantAlphaPadding'] for f in frames) >= 12,
                   'notes': 'Largest cells have 1 px significant-alpha padding; review native renderer for bleed before production registration.'}}
(root / 'art' / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'dimensions': [w, h], 'cells': [cw, ch], 'frames': len(frames),
                  'minimumPadding': min(f['minimumSignificantAlphaPadding'] for f in frames),
                  'sourceSha256': manifest['sha256']}))
