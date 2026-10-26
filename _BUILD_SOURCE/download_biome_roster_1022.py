from pathlib import Path
import concurrent.futures,json,re,urllib.request,sys
from PIL import Image,ImageDraw
from pixellab_mcp import PixelLab
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/biome_roster_1022';O=R/'_shots/biome_roster_1022';O.mkdir(exist_ok=True)
def fetch(p):
 name=p.stem.removesuffix('-job');row=json.loads(p.read_text());s='\n'.join(x.get('text','') for x in row.get('content',[]) if x.get('type')=='text');m=re.search(r'job_id: ([\w-]+)',s)
 if not m or row.get('isError'):return dict(name=name,status='invalid receipt')
 count=9 if name.endswith(('_flight','_attack','_motion')) else 1;out=D/'raw'/name
 if (out/f'{count-1:02}.png').exists():return dict(name=name,status='downloaded')
 c=PixelLab()
 try:r=c.call('get_image',dict(job_id=m.group(1),index=count-1))
 finally:c.close()
 text='\n'.join(x.get('text','') for x in r.get('content',[]) if x.get('type')=='text');(D/(name+'-status.txt')).write_text(text,encoding='utf-8')
 if r.get('isError') or re.search(r'status: (?:processing|queued|pending)',text):return dict(name=name,status=text[:80])
 out.mkdir(parents=True,exist_ok=True)
 for i in range(count):
  dst=out/f'{i:02}.png'
  if dst.exists():continue
  with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{m.group(1)}/download?index={i}',timeout=90) as response:data=response.read()
  assert data.startswith(b'\x89PNG');dst.write_bytes(data)
 return dict(name=name,status='downloaded')
if __name__=='__main__':
 files=[D/(n+'-job.json') for n in sys.argv[1:]] if len(sys.argv)>1 else list(D.glob('*-job.json'))
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
  for row in ex.map(fetch,files):print(json.dumps(row),flush=True)
 ims=list((D/'raw').glob('*/00.png'));sheet=Image.new('RGB',(192*5,216*((len(ims)+4)//5)),'#18212b');dr=ImageDraw.Draw(sheet)
 for i,p in enumerate(ims):
  im=Image.open(p).convert('RGBA');x=i%5*192;y=i//5*216;sheet.paste(im,(x,y),im);dr.text((x+3,y+194),p.parent.name,fill='white')
 if ims:sheet.save(O/'generated-contact.png')
