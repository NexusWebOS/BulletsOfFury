from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,urllib.error
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/arena_download_1020/returned/curtain';D.mkdir(exist_ok=True,parents=True)
job='21c814cd-cf27-443c-ae2f-d8ee9f8ef38a'
def get(i):
 p=D/('frame_'+str(i).zfill(3)+'.png')
 if p.exists():return
 with urllib.request.urlopen('https://api.pixellab.ai/mcp/images/'+job+'/download?index='+str(i),timeout=90) as response:d=response.read()
 assert d.startswith(b'\x89PNG');p.write_bytes(d)
try:get(0)
except urllib.error.HTTPError as e:
 if e.code==423:print('PixelLab curtain is still processing');raise SystemExit(2)
 raise
with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(get,range(1,33)))
print('Saved input plus32 actual PixelLab curtain phases')
