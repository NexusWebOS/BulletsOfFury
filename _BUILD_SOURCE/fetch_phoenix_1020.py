from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,sys
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/dracodia_phoenix_1020';jobs=[]
def add(name,job,indices):
 d=S/name;d.mkdir(exist_ok=True)
 for i in indices:jobs.append((d/f'{i:02}.png',job,i))
add('wing-charge','40f92480-fd27-4286-b87e-db372e4e0298',range(9))
add('head-charge','01ab246b-e121-4006-9ef4-238e0d34d4d9',range(1,17))
jobs.extend([(S/'head-charge.png','01ab246b-e121-4006-9ef4-238e0d34d4d9',16),(S/'beam.png','2696c0f4-6a51-456c-b7c1-dbf413216375',0)])
if '--effects' in sys.argv:
 add('plume-motion','8fae5f5b-d5fd-4b27-b977-789be6c7420b',range(1,17));add('beam-motion','84fa5caa-2910-42de-8cf7-2bc8469ae631',range(1,17))
def fetch(row):
 p,job,i=row
 if not p.exists():p.write_bytes(urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',timeout=90).read())
 return p.name
with ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(fetch,jobs))
if '--effects' in sys.argv:
 import runpy
 runpy.run_path(str(R/'_BUILD_SOURCE/clean_phoenix_beam_1020.py'),run_name='__main__')
print(json.dumps(dict(downloaded=len(jobs))),flush=True)
