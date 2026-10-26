from pathlib import Path
import json,re,urllib.request,sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw
from pixellab_mcp import PixelLab
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/stage59_1024';O=R/'_shots/stage59_1024';O.mkdir(exist_ok=True)
for p in ([D/(n+'-job.json') for n in sys.argv[1:]] if len(sys.argv)>1 else D.glob('*-job.json')):
 name=p.stem.removesuffix('-job');receipt=json.loads(p.read_text());text='\n'.join(x.get('text','') for x in receipt.get('content',[]) if x.get('type')=='text');m=re.search(r'job_id: ([\w-]+)',text)
 if not m or receipt.get('isError'):continue
 count=17 if name=='black_spin' else 9 if name.startswith('black_') else 25 if name=='warp_motion' else 1;out=D/'raw'/name
 if (out/f'{count-1:02}.png').exists():continue
 c=PixelLab()
 try:r=c.call('get_image',dict(job_id=m.group(1),index=count-1))
 finally:c.close()
 text='\n'.join(x.get('text','') for x in r.get('content',[]) if x.get('type')=='text');(D/(name+'-status.txt')).write_text(text,encoding='utf-8')
 if r.get('isError') or re.search(r'status: (processing|queued|pending)',text):print(name+' pending',flush=True);continue
 out.mkdir(parents=True,exist_ok=True)
 def download(i):
  q=out/f'{i:02}.png'
  if not q.exists():
   with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{m.group(1)}/download?index={i}',timeout=90) as response:data=response.read()
   assert data.startswith(b'\x89PNG');q.write_bytes(data)
 with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(download,range(count)))
 ims=[Image.open(out/f'{i:02}.png').convert('RGBA') for i in range(count)];cols=min(6,count);sheet=Image.new('RGB',(cols*256,280*((count+cols-1)//cols)),'#17212c');d=ImageDraw.Draw(sheet)
 for i,im in enumerate(ims):
  x=i%cols*256;y=i//cols*280;sheet.paste(im,(x,y),im);d.text((x+4,y+258),f'{name} {i}',fill='white')
 sheet.save(O/(name+'-contact.png'));print(name+' downloaded',flush=True)
