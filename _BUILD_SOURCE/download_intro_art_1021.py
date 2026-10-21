"""Download complete PixelLab banks and inspect fixed canvases; never fit frames."""
from pathlib import Path
import argparse,urllib.request,concurrent.futures,json,hashlib,time
from PIL import Image,ImageDraw
ap=argparse.ArgumentParser();ap.add_argument('--job',required=True);ap.add_argument('--name',required=True);ap.add_argument('--frames',type=int,required=True);ap.add_argument('--width',type=int,required=True);ap.add_argument('--height',type=int,required=True);a=ap.parse_args()
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/intro_repair_1021/raw'/a.name;O=R/'_shots/intro_repair_1021';D.mkdir(parents=True,exist_ok=True)
def get(i):
 p=D/f'{i:02}.png'
 if not p.exists():
  for attempt in range(3):
   try:
    with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{a.job}/download?index={i}',timeout=60) as r:data=r.read()
    assert data.startswith(b'\x89PNG\r\n\x1a\n');p.write_bytes(data);break
   except Exception:
    if attempt==2:raise
    time.sleep(1)
 im=Image.open(p).convert('RGBA');assert im.size==(a.width,a.height),(i,im.size)
 return dict(index=i,bounds=im.getbbox(),sha256=hashlib.sha256(im.tobytes()).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(get,range(a.frames)))
frames=[Image.open(D/f'{i:02}.png').convert('RGBA') for i in range(a.frames)];cw=a.width;ch=a.height+18
sheet=Image.new('RGBA',(cw*8,ch*((len(frames)+7)//8)),(7,13,22,255));onion=sheet.copy();draw=ImageDraw.Draw(sheet)
for i,im in enumerate(frames):
 xy=(i%8*cw,i//8*ch);sheet.alpha_composite(im,xy);draw.text((xy[0]+3,xy[1]+a.height+1),str(i),fill='white')
 for j in [max(0,i-1),min(len(frames)-1,i+1)]:
  ghost=frames[j].copy();ghost.putalpha(ghost.getchannel('A').point(lambda v:round(v*.22)));onion.alpha_composite(ghost,xy)
 ghost=im.copy();ghost.putalpha(ghost.getchannel('A').point(lambda v:round(v*.65)));onion.alpha_composite(ghost,xy)
sheet.convert('RGB').save(O/(a.name+'-contact.jpg'),quality=95);onion.save(O/(a.name+'-onions.png'))
frames[0].save(O/(a.name+'-motion.webp'),save_all=True,append_images=frames[1:],duration=100,loop=0,lossless=True)
q=dict(job=a.job,canvas=[a.width,a.height],pivot=[a.width//2,a.height//2],scale=1,frames=len(frames),unique=len({r['sha256'] for r in rows}),records=rows)
(D/'audit.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:q[k] for k in ['job','canvas','frames','unique']}))
