"""Download only PixelLab animations seeded with the eight actual sonic sprites."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import json,urllib.request,time,argparse
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/sonic_refine_1021';jobs=json.loads((S/'jobs.json').read_text())
ap=argparse.ArgumentParser();ap.add_argument('--only',nargs='*');args=ap.parse_args()
if args.only:jobs={k:v for k,v in jobs.items() if k in args.only}
def get(task):
 name,a,i=task;p=S/'raw'/name/f'{i:02}.png';p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():
  for attempt in range(3):
   try:
    with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{a["job"]}/download?index={i}',timeout=50) as response:data=response.read()
    assert data.startswith(b'\x89PNG\r\n\x1a\n');p.write_bytes(data);break
   except Exception:
    if attempt==2:raise
    time.sleep(2)
 assert Image.open(p).size==(256,256);return p.stat().st_size
tasks=[(n,a,i) for n,a in jobs.items() if not a.get('rawBank') for i in range(a['frames'])]
with ThreadPoolExecutor(max_workers=6) as pool:total=sum(pool.map(get,tasks))
print(json.dumps(dict(banks=len(jobs),frames=len(tasks),bytes=total)))
