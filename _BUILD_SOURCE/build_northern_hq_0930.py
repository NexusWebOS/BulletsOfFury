"""Extract the generated Fury HQ map island at the scale used by campaign plates."""
from pathlib import Path
import json,hashlib
from PIL import Image

root=Path(__file__).resolve().parents[1]
source=root/'_ART_SOURCES/campaign_0930/northern_hq_island.png'
out=root/'assets/game/shared/campaign/campaign_0930/northern_hq_island.png'
im=Image.open(source).convert('RGBA')
assert im.size==(1254,1254)
box=im.getchannel('A').getbbox()
assert box
im=im.crop(box)
im.thumbnail((384,384),Image.Resampling.NEAREST)
assert im.getchannel('A').getextrema()==(0,255)
im.save(out,optimize=True)
(out.with_suffix('.json')).write_text(json.dumps({
 'image':out.name,'source':'_ART_SOURCES/campaign_0930/northern_hq_island.png',
 'source_crop':box,'runtime_size':im.size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'placement_world':[385,185,205,190],
 'role':'decorative Fury HQ island north of the Stage 1 jungle; no hit area'},indent=2)+'\n',encoding='utf-8')
print('Built northern HQ island',im.size,'source crop',box)
