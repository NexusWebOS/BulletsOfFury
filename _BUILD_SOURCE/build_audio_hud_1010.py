"""Own the generated, empty October 10 bottom HUD. Crop/pad only; native alpha."""
from pathlib import Path
from PIL import Image
import json, shutil, hashlib

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r'C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c/exec-d390024d-90f8-4f70-8ca2-04c3565719f4.png')
archive = ROOT / '_ART_SOURCES/audio_1010'
archive.mkdir(parents=True, exist_ok=True)
raw = archive / 'hud_raw.png'
if not raw.exists(): shutil.copy2(SOURCE, raw)
im = Image.open(raw).convert('RGBA')
# Same source scale and margins throughout this single housing. The insignificant
# outside alpha tail is documented; no painted pixel or well is reconstructed.
crop = [8,148,2164,560]
canvas = Image.new('RGBA',(2160,432))
canvas.alpha_composite(im.crop(crop),(2,10))
dest = ROOT / 'assets/game/shared/ui/audio_hud_1010.png'
dest.parent.mkdir(parents=True, exist_ok=True)
canvas.save(dest,optimize=True)
metadata = dict(key='ap10_hud',path=dest.relative_to(ROOT).as_posix(),w=2160,h=432,
                source_crop=crop,padding=[2,10],scale=1,mode='built-in image_gen edit',
                raw_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),
                shipping_sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
(archive/'hud_registration.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
(ROOT/'assets/audio_hud_art_1010.js').write_text('"use strict";\nconst AP10_HUD_ART='+json.dumps(metadata)+';\n',encoding='utf-8',newline='\n')
print(json.dumps(metadata))
