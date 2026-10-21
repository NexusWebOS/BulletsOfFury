from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,urllib.error,sys,json
R=Path(__file__).resolve().parents[1];A=R/'_ART_SOURCES/instructor_bob_1020'
jobs={'view_whole':'df276f68-503c-492a-a390-0a74d4b79faf','view_missile':'dea0653a-d720-4ad3-82cc-a27191636145','view_core':'e888373d-7be1-4d63-9d67-6696b254d794','view_cannon':'aa7861b6-67e2-4722-9eb1-c487ee7295fb'}
if len(sys.argv)>2:jobs={sys.argv[1]:sys.argv[2]}
count=int(sys.argv[3]) if len(sys.argv)>3 else 0
def get(item):
 name,job=item;D=A/'returned'/name;D.mkdir(exist_ok=True,parents=True)
 def frame(i):
  p=D/('frame_'+str(i).zfill(3)+'.png')
  if p.exists():return
  with urllib.request.urlopen('https://api.pixellab.ai/mcp/images/'+job+'/download?index='+str(i),timeout=90) as r:data=r.read()
  assert data.startswith(b'\x89PNG');p.write_bytes(data)
 try:frame(0)
 except urllib.error.HTTPError as e:
  if e.code==423:return name+' pending'
  raise
 if count:
  with ThreadPoolExecutor(max_workers=5) as pool:list(pool.map(frame,range(1,count+1)))
 return name+' saved'
with ThreadPoolExecutor(max_workers=4) as pool:
 for s in pool.map(get,jobs.items()):print(s,flush=True)
