"""Fetch only completed PixelLab job outputs into their owning source bank."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,urllib.request,time,sys
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/stage8_identity_1018'
jobs=json.loads((S/'jobs.json').read_text());names=sys.argv[1:] or list(jobs)
def fetch(task):
 name,i,url=task;p=S/'returned'/name/f'frame_{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():return
 for attempt in range(3):
  try:
   with urllib.request.urlopen(url,timeout=90) as response:data=response.read()
   assert data.startswith(b'\x89PNG'),name;p.write_bytes(data);return
  except Exception:
   if attempt==2:raise
   time.sleep(1+attempt)
tasks=[]
for name in names:
 j=jobs[name];count=j['count']+(0 if j['count']==1 else 1)
 for i in range(count):tasks.append((name,i,f"https://api.pixellab.ai/mcp/images/{j['id']}/download?index={i}"))
with ThreadPoolExecutor(max_workers=6) as ex:list(ex.map(fetch,tasks))
print('Downloaded '+', '.join(names))
