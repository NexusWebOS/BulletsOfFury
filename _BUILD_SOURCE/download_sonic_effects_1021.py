"""Download only this task's five PixelLab result banks; no local files uploaded."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,urllib.request,time
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/sonic_effects_1021'
jobs=json.loads((S/'jobs.json').read_text())
def get(task):
 name,a,i=task;p=S/'raw'/name/f'{i:02}.png';p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():
  for attempt in range(4):
   try:
    with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{a["job"]}/download?index={i}',timeout=50) as response:data=response.read()
    assert data.startswith(b'\x89PNG\r\n\x1a\n');p.write_bytes(data);break
   except Exception:
    if attempt==3:raise
    time.sleep(2)
 im=Image.open(p);assert list(im.size)==a['canvas'],(name,i,im.size)
 return p.stat().st_size
tasks=[(name,a,i) for name,a in jobs.items() for i in range(a['frames'])]
with ThreadPoolExecutor(max_workers=5) as pool:total=sum(pool.map(get,tasks))
print(json.dumps(dict(banks=len(jobs),frames=len(tasks),bytes=total)))
