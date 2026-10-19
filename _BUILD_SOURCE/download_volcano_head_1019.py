"""Download only the two returned PixelLab head candidates, then render inspection sheets."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,urllib.request
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/volcano_head_1019';O=R/'_shots/overnight_combat_1019/volcano';O.mkdir(exist_ok=True)
jobs={'spin':'733f3cb3-aad1-4351-bc46-c54285bfb3d5','charge':'e7ee3184-39dc-4cb2-9f07-1121180eb9a7',
      'turn-0':'eccfc929-1c31-45e3-a1d4-6a6e4da22aff','turn-1':'3a481302-660c-48a9-ad17-6c3325ddeb78',
      'turn-2':'259f5c2b-ea5b-4d08-b2c4-54aabe210402','turn-3':'0f435422-8e80-4699-9536-19aee8ffba51'}
def download(item):
 name,job,i=item;folder=S/name;folder.mkdir(exist_ok=True);p=folder/f'frame_{i:02}.png'
 if not p.exists():p.write_bytes(urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',timeout=90).read())
 with Image.open(p) as im:assert im.size==(128,128),(name,i,im.size)
 return dict(bank=name,frame=i,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
with ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(download,[(name,job,i) for name,job in jobs.items() for i in range(9 if name.startswith('turn-') else 17)]))
for name in jobs:
 frames=[Image.open(S/name/f'frame_{i:02}.png').convert('RGBA') for i in range(9 if name.startswith('turn-') else 17)]
 sheet=Image.new('RGBA',(1024,((len(frames)+7)//8)*148),(8,13,23,255));onion=sheet.copy()
 for i,im in enumerate(frames):
  at=(i%8*128,i//8*148);sheet.alpha_composite(im,at);ImageDraw.Draw(sheet).text((at[0]+3,at[1]+128),str(i),fill='white')
  for j in [max(0,i-1),min(len(frames)-1,i+1)]:
   ghost=frames[j].copy();ghost.putalpha(ghost.getchannel('A').point(lambda a:round(a*.22)));onion.alpha_composite(ghost,at)
  onion.alpha_composite(im,at)
 sheet.save(O/(name+'-candidate.png'));onion.save(O/(name+'-candidate-onions.png'))
 frames[0].save(O/(name+'-candidate.webp'),save_all=True,append_images=frames[1:],duration=90,loop=0,lossless=True)
(S/'generation.json').write_text(json.dumps(dict(jobs=jobs,frame=[128,128],pivot=[64,64],scale=1,frames=records,inspection='PENDING. Candidates only; no shipping manifest.'),indent=2)+'\n')
print(json.dumps(dict(downloaded=len(records),jobs=jobs)))
