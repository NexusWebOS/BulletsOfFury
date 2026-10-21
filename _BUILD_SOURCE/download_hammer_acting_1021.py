"""Poll and download only this pass's PixelLab jobs; keep native PNGs as provenance."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,re,urllib.request,sys
from PIL import Image,ImageDraw
from pixellab_mcp import PixelLab
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/hammer_acting_1021';O=R/'_shots/hammer_acting_1021';O.mkdir(exist_ok=True)
def run(p):
 row=json.loads(p.read_text());s='\n'.join(c.get('text','') for c in row.get('content',[]) if c.get('type')=='text');m=re.search(r'job_id: ([\w-]+)',s)
 if row.get('isError') or not m:return
 name=p.stem.removesuffix('-job');out=D/'raw'/name;count=9 if name=='blue_throw_follow' else 1 if name.endswith('_pose') else 17
 if (out/f'{count-1:02}.png').exists():return dict(bank=name,status='downloaded')
 c=PixelLab()
 try:r=c.call('get_image',dict(job_id=m.group(1),index=count-1))
 finally:c.close()
 text='\n'.join(x.get('text','') for x in r.get('content',[]) if x.get('type')=='text');status=re.search(r'status: ([^\n]+)',text);status=status.group(1) if status else text[:80]
 (D/(name+'-status.txt')).write_text(text)
 if 'processing' in status or 'queued' in status:return dict(bank=name,status=status)
 if r.get('isError'):return dict(bank=name,status='error '+text[:90])
 out.mkdir(parents=True,exist_ok=True)
 def fetch(i):
  p=out/f'{i:02}.png'
  if p.exists():return
  for attempt in range(3):
   try:
    with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{m.group(1)}/download?index={i}',timeout=60) as response:data=response.read()
    assert data.startswith(b'\x89PNG');p.write_bytes(data);return
   except Exception:
    if attempt==2:raise
 with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,range(count)))
 ims=[Image.open(out/f'{i:02}.png').convert('RGBA') for i in range(count)]
 sheet=Image.new('RGB',(256*6,280*3),'#121a24');dr=ImageDraw.Draw(sheet)
 for i,im in enumerate(ims):
  x=i%6*256;y=i//6*280;sheet.paste(im,(x,y),im);dr.text((x+8,y+258),f'{name} {i}',fill='white')
 sheet.save(O/(name+'-contact.png'))
 return dict(bank=name,status='downloaded',size=ims[0].size)
if __name__=='__main__':
 files=list(D.glob('*-job.json'))
 if len(sys.argv)>1:files=[D/(n+'-job.json') for n in sys.argv[1:]]
 with ThreadPoolExecutor(max_workers=3) as pool:
  for r in pool.map(run,files):
   if r:print(json.dumps(r),flush=True)
