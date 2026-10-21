from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,urllib.error,json,sys
R=Path(__file__).resolve().parents[1];A=R/'_ART_SOURCES/arena_download_1020'
jobs={'jungle':'35a02631-aef2-4306-b4cf-f1d2a1a5bd97','lava':'81f25a4d-a89c-4c18-992e-e3614dfd0dec','space':'71862fe9-ce9c-4f1f-abc3-a4825f2cd463','sky':'bbc0d4ef-b38b-4cda-a69b-c8823aa7e915'}
jobs.update(wire_jungle='6a4a8f83-c708-4009-a6d4-71d7835ff514',wire_space='ea3050e5-9e60-4a71-9153-17af19dfa36f',wire_sky='ab5d0ac6-2360-4f23-b2d8-801deb09764d',wire_lava='775bd725-004e-4b7c-bf7c-1d9591ea597d')
if len(sys.argv)>2:jobs={sys.argv[1]:sys.argv[2]}
def get(item):
 n,j=item;p=A/'returned'/n/'frame_000.png';p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():return n+' already downloaded'
 try:
  with urllib.request.urlopen('https://api.pixellab.ai/mcp/images/'+j+'/download?index=0',timeout=90) as response:d=response.read()
 except urllib.error.HTTPError as e:
  if e.code==423:return n+' pending'
  raise
 assert d.startswith(b'\x89PNG');p.write_bytes(d);return n+' saved'
with ThreadPoolExecutor(max_workers=4) as pool:
 for s in pool.map(get,jobs.items()):print(s,flush=True)
