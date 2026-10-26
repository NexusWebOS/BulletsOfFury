from pathlib import Path
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw
D=Path('_ART_SOURCES/chronos_contract_1025/motion');D.mkdir(exist_ok=True)
def dl(i):
 with urllib.request.urlopen('https://api.pixellab.ai/mcp/images/793fba39-5c41-4dfa-b647-35312c19d3b9/download?index='+str(i),timeout=60) as r:data=r.read()
 (D/f'{i:02}.png').write_bytes(data)
with ThreadPoolExecutor(max_workers=4) as p:list(p.map(dl,range(17)))
out=Image.new('RGB',(5*256,4*280),'#17212c');g=ImageDraw.Draw(out)
for i,p in enumerate(sorted(D.glob('*.png'))):
 im=Image.open(p).convert('RGBA');out.paste(im,(i%5*256,i//5*280),im);g.text((i%5*256+8,i//5*280+260),str(i),fill='white')
out.save('_shots/chronos_contract_1025/empty-contact.png')
