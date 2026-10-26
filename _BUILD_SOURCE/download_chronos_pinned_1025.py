from pathlib import Path
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw
D=Path('_ART_SOURCES/chronos_contract_1025/motion-pinned');D.mkdir(exist_ok=True)
def dl(i):
 with urllib.request.urlopen('https://api.pixellab.ai/mcp/images/639ea9e8-d9c6-4f45-8474-55a17c937be1/download?index='+str(i),timeout=60) as r:data=r.read()
 (D/f'{i:02}.png').write_bytes(data)
with ThreadPoolExecutor(max_workers=4) as p:list(p.map(dl,range(9)))
out=Image.new('RGB',(5*256,4*280),'#17212c');g=ImageDraw.Draw(out)
for i,p in enumerate(sorted(D.glob('*.png'))):
 im=Image.open(p).convert('RGBA');out.paste(im,(i%5*256,i//5*280),im);g.text((i%5*256+8,i//5*280+260),str(i),fill='white')
out.save('_shots/chronos_contract_1025/empty-pinned-contact.png')
