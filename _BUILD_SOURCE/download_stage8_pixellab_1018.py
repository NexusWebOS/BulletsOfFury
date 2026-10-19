"""Download completed PixelLab animation frames. No credentials or signed URLs."""
from pathlib import Path
import json,sys,urllib.request,concurrent.futures
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/stage8_pixellab_1018'
jobs=json.loads((S/'animation_jobs.json').read_text())
todo=sys.argv[1:] or [k for k,v in jobs.items() if v.get('job_id')]
def fetch(item):
 name,i,url=item;d=S/'returned'/name;d.mkdir(parents=True,exist_ok=True);p=d/f'frame_{i:03}.png'
 if p.exists():return 0
 for n in range(3):
  try:
   with urllib.request.urlopen(url,timeout=45) as r:raw=r.read()
   assert raw.startswith(b'\x89PNG'),name+' not PNG';p.write_bytes(raw);return len(raw)
  except Exception:
   if n==2:raise
tasks=[]
for name in todo:
 v=jobs[name];job=v['job_id'];assert job,name
 n=32 if name=='conversion' else 24 if name.endswith('emerge') else 16
 for i in range(n+1):tasks.append((name,i,f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}'))
with concurrent.futures.ThreadPoolExecutor(6) as pool:total=sum(pool.map(fetch,tasks))
print(json.dumps(dict(banks=todo,frames=len(tasks),downloadedBytes=total)))
