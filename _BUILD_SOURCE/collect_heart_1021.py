from pathlib import Path
import json,urllib.request,concurrent.futures
from PIL import Image,ImageDraw
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');S=R/'_ART_SOURCES/menu_heart_1021';S.mkdir(parents=True,exist_ok=True)
J={'idle':('5d469646-109c-49af-a80a-2764e260bc2a',8),'dance':('fd383f74-5191-4adf-b08b-50823509480f',24),'slam':('3b145433-89f5-403b-b128-1735ddba1e65',20),'spin':('df8fa93c-5897-4640-85d7-e9d8ce7a0a9b',16),'channel':('66743bea-4e53-4601-880a-1940fcd32da3',16),'heart':('d2dfa5ad-18fa-4cb6-8e6b-6d78f0f33bf2',12),'shield':('6c566c2e-5068-4e9f-bbc5-a5164f261ca8',16)}
json.dump(J,open(S/'pixellab-jobs.json','w'),indent=2)
def get(v):
 name,id,i=v;p=S/name/f'{i:02}.png';p.parent.mkdir(exist_ok=True)
 if p.exists():return
 try:
  with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{id}/download?index={i}',timeout=60) as q:b=q.read()
  p.write_bytes(b);Image.open(p).verify()
 except Exception as e:
  if p.exists():p.unlink()
  print(name,i,str(e)[:70],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(get,[(n,j,i) for n,(j,c) in J.items() for i in range(1,c+1)]))
for n,(j,c) in J.items():
 fs=list((S/n).glob('*.png'));print(n,len(fs),'/',c,flush=True)
 if len(fs)!=c:continue
 thumb=128 if n not in ['heart'] else 64;sheet=Image.new('RGBA',(thumb*8, (c+7)//8*(thumb+18)),(13,17,28,255));d=ImageDraw.Draw(sheet)
 for k,p in enumerate(sorted(fs)):
  im=Image.open(p).convert('RGBA');im.thumbnail((thumb,thumb),Image.Resampling.NEAREST);x=k%8*thumb;y=k//8*(thumb+18);sheet.alpha_composite(im,(x+(thumb-im.width)//2,y));d.text((x+4,y+thumb),str(k+1))
 sheet.save(S/f'{n}-contact.png')
