from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,urllib.request,sys
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/boss_redesign_1020';jobs=json.loads((S/'jobs.json').read_text());rows=[]
selected=set(sys.argv[1:])
for name,row in jobs.items():
 if selected and name not in selected:continue
 p=S/name;p.mkdir(exist_ok=True)
 for i in range(row['count']):rows.append((p/f'{i:02}.png',row['id'],i))
def fetch(row):
 p,job,index=row
 if not p.exists():p.write_bytes(urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={index}',timeout=120).read())
 return p.name
with ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(fetch,rows))
print(json.dumps({'frames':len(rows),'banks':len(selected) if selected else len(jobs)}),flush=True)
