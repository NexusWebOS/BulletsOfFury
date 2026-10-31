from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,time,sys
W=Path(__file__).resolve().parent;J=json.loads((W/'jobs.json').read_text());names=sys.argv[1:]or list(J)
def one(q):
 name,i=q;p=W/'raw'/name/f'{i:02}.png';p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():return str(p)
 for n in range(3):
  try:
   with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{J[name]}/download?index={i}',timeout=25)as r:p.write_bytes(r.read())
   return str(p)
  except Exception:
   if n==2:raise
   time.sleep(1)
tasks=[(name,i)for name in names for i in range(9 if name.endswith('_anim')else 1)]
with ThreadPoolExecutor(max_workers=3)as pool:
 for p in pool.map(one,tasks):print(p,flush=True)
