from pathlib import Path
import json,re,urllib.request,concurrent.futures
from pixellab_mcp import PixelLab
from pixellab_intro_1021 import content
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/chronos_final_1025';c=PixelLab();results=[]
def download(args):
 job,i,dest=args;p=dest/f'{i:02}.png'
 if not p.exists():
  with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',timeout=90) as r:p.write_bytes(r.read())
 im=Image.open(p);assert im.size==(256,256),(p,im.size)
try:
 for q in json.loads((D/'motion-spec.json').read_text()):
  p=D/'jobs'/(q['name']+'.json');r=json.loads(p.read_text());m=re.search(r'job_id[:"\s]+([\w-]{20,})',content(r))
  if not m:results.append({'bank':q['name'],'state':'not submitted'});continue
  job=m.group(1);dest=D/'frames'/q['name'];dest.mkdir(parents=True,exist_ok=True)
  if len(list(dest.glob('*.png')))==q['frames']+1:results.append({'bank':q['name'],'state':'downloaded'});continue
  r=c.call('get_image',{'job_id':job,'index':q['frames']});text=content(r);(dest/'status.json').write_text(json.dumps({'isError':r.get('isError',False),'text':text},indent=2)+'\n',encoding='utf8')
  if '/download' in text:
   with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(download,[(job,i,dest) for i in range(q['frames']+1)]))
   results.append({'bank':q['name'],'state':'downloaded'})
  else:results.append({'bank':q['name'],'state':text[:240]})
  print(json.dumps(results[-1]),flush=True)
finally:c.close()
(D/'download-status.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf8');print('Downloaded',sum(q['state']=='downloaded' for q in results),'/',len(results),flush=True)
