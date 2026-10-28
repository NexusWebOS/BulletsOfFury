from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,time,json
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/chronos_modular_1023';J={'barrel':'82cdddc4-d026-43b0-a12b-ff08d7bd1757','body':'39117169-f35c-4fbe-b669-b19f24d64f37','grip':'d9c920f4-e2aa-4059-a655-54b6fb335abb'}
def get(item):
 bank,job,i=item;p=W/'raw'/bank/f'{i:02}.png';p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():return
 for retry in range(3):
  try:
   with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',timeout=25)as r:data=r.read()
   assert data.startswith(b'\x89PNG');p.write_bytes(data);return
  except Exception:
   if retry==2:raise
   time.sleep(1)
with ThreadPoolExecutor(max_workers=3)as pool:list(pool.map(get,[(n,j,i)for n,j in J.items()for i in range(1 if n=='grip'else 9)]))
(W/'jobs.json').write_text(json.dumps(J,indent=2));print('Downloaded 19 source frames including corrected two-hand grip.')
