from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json
W=Path(__file__).resolve().parent;path=W/'jobs.json';d=json.loads(path.read_text());d.update(head_rage='d5d4768c-df39-44c2-9cab-fc6609ffe0f5',head_grin='c30b1765-b0e9-46e6-bf9b-7842950df766',lightning='8b4ff2bc-0650-4a51-9d3f-ded2a8f884d1',code_round='ae521d02-2c41-4710-ada3-8427063ed123');path.write_text(json.dumps(d,indent=2))
def fetch(item):
 name,job,i=item;folder=W/'generated'/name;folder.mkdir(parents=True,exist_ok=True);p=folder/(str(i).zfill(2)+'.png')
 if not p.exists():
  with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',timeout=60)as r:p.write_bytes(r.read())
 return p
jobs=[(name,job,i)for name,job in d.items()if not name.endswith('_still')for i in range(17)]
with ThreadPoolExecutor(max_workers=6)as pool:
 for p in pool.map(fetch,jobs):pass
print('Downloaded',len(jobs),'canonical/reference and generated frames')
