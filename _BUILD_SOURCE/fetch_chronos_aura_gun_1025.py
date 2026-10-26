"""Fetch the three explicitly selected PixelLab animation jobs, preserving sources."""
from pathlib import Path
import urllib.request,json,concurrent.futures
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/chronos_aura_gun_1025';O=R/'_shots/chronos_aura_gun_1025'
jobs={'barrel':'1c84e602-231b-4ea2-b4a4-437ecce28111','body':'ba480b8c-4766-4829-b6a4-09fa2f0b19c8','crate':'60e4376d-e3fe-41b1-8ea3-f054383ed819'}
def fetch(item):
 name,job,i=item;p=D/name/f'{i:02}.png';p.parent.mkdir(exist_ok=True)
 if not p.exists():
  with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',timeout=90) as q:p.write_bytes(q.read())
 return p
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,[(n,j,i) for n,j in jobs.items() for i in range(9)]))
(D/'jobs.json').write_text(json.dumps(dict(jobs=jobs,frames=9,format={'body':[192,256],'barrel':[128,224],'crate':[80,80]},source='Current authored CH23 whole body/rotary gun and HT23 exclusive chaingun icon crate; first-frame sources preserved beside jobs.'),indent=2),encoding='utf8')
out=Image.new('RGB',(9*192,3*280),'#122034');d=ImageDraw.Draw(out)
for y,name in enumerate(jobs):
 for i in range(9):
  im=Image.open(D/name/f'{i:02}.png').convert('RGBA');im.thumbnail((192,256));out.paste(im,(i*192,y*280+24),im);d.text((i*192+4,y*280+4),f'{name} {i}',fill='white')
out.save(O/'pixellab-contact.png');print('27 source frames downloaded; contact sheet ready.')
