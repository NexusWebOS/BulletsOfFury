"""Publish the shipping Wind reels, green badges and native review captures."""
from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/wind_projectiles_1011';OUT.mkdir(parents=True,exist_ok=True)
art=json.loads((ROOT/'assets/audio_fx_art_1010.js').read_text().split('const AP10_FX_ART=',1)[1].strip().rstrip(';'))
names=['bullets','spread','missile','laser','gust','tornado','mist','heavy','electric'];captures=[]
for name in names+['stage6-live']:
    f=ROOT/'_shots/wind_projectiles_1011'/(name+'-native.png')
    if f.exists():
        im=Image.open(f);im.thumbnail((960,1200));im.convert('RGB').save(OUT/(name+'-native.webp'),quality=92)
        captures.append(dict(family=name,path=name+'-native.webp'))
data=dict(banks={k:art['wind_'+k] for k in names},icons=art['wind_icons'],symbol=art['wind_symbol'][0],captures=captures)
(OUT/'review.json').write_text(json.dumps(data),encoding='utf-8')
print('Wind review:144 drawn poses,45 green badges, '+str(len(captures))+' native captures')
