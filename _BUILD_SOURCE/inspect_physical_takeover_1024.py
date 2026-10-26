from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request
from PIL import Image,ImageDraw,ImageChops
import json
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/orbital_takeover_1024/physical';D.mkdir(exist_ok=True)
def dl(i):
 urllib.request.urlretrieve(f'https://api.pixellab.ai/mcp/images/f0274aa1-4b6b-433e-aa24-b95b997bcca9/download?index={i}',D/f'{i:02}.png')
with ThreadPoolExecutor(max_workers=6)as e:list(e.map(dl,range(41)))
ims=[Image.open(p).convert('RGBA')for p in sorted(D.glob('*.png'))]
assert len(ims)==41 and all(i.size==(256,256)for i in ims)
out=Image.new('RGB',(8*192,6*212),(28,30,36));dr=ImageDraw.Draw(out)
for i,im in enumerate(ims):
 z=im.resize((192,192),Image.Resampling.NEAREST);out.paste(z,(i%8*192,i//8*212+20),z);dr.text((i%8*192,i//8*212),str(i))
out.save(R/'_shots/intro_order_1024/physical-contact.png')
print('Downloaded and inspected geometry of41 frames')
