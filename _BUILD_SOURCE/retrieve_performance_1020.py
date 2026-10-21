from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,time,json,sys
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');A=R/'_ART_SOURCES/performance_finish_1020/returned';A.mkdir(exist_ok=True,parents=True)
jobs={'cole_report_face':['19979321-4017-4647-9814-5b07afc3b8f9',16],'cole_horror_face':['76e284ec-b7fc-418d-a7e4-11fa03408836',16],'cole_report_gesture':['041a8c1a-b99c-48be-968a-8bb0670f9eb9',24],'cole_horror_gesture':['41d1aa7e-2a1b-4828-9e07-79b3b5a37736',24],'carrier_turret':['413cfcec-9e9f-47d0-b975-9f87afdf26d8',16],'bomber_cannon':['68add865-4711-4bd1-b4ef-22e940fc937b',16],'laser_terminal':['774921e4-77b4-4af6-87ff-81b52fc85e0f',16],'dark_terminal':['7bcf2847-b15e-45e9-a3ea-5588dfb511ba',16],'ice_shatter':['7d4a44ce-74f7-409b-ab7f-c3f601ca38bf',16]}
names=sys.argv[1:] or list(jobs)
for name in names:
 job,count=jobs[name];d=A/name;d.mkdir(exist_ok=True)
 def get(i):
  p=d/f'{i:03}.png'
  if p.exists():return
  for attempt in range(3):
   try:
    with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',timeout=90) as resp:data=resp.read()
    assert data[:8]==b'\x89PNG\r\n\x1a\n';p.write_bytes(data);return
   except Exception:
    if attempt==2:raise
    time.sleep(2)
 with ThreadPoolExecutor(max_workers=5) as pool:list(pool.map(get,range(count+1)))
 print(name+' saved '+str(count+1),flush=True)
