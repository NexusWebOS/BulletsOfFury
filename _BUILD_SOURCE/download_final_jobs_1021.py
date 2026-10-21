from pathlib import Path
from PIL import Image,ImageDraw
import json,re,concurrent.futures,urllib.request,time,sys
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');S=R/'_ART_SOURCES/final_version_1021';O=R/'_shots/final_version_1021';T=Path(__file__).parent
jobs=json.loads((T/'final21_accepted.json').read_text());status=json.loads((T/'final21_status.json').read_text());done={q['id'] for q in status if q['done']};work=[];banks=[]
for row in jobs:
 txt='\n'.join(row['receipt']);jid=re.search(r'job_id: ([\w-]+)',txt).group(1)
 if jid not in done and row['name']!='corrupt_tool':continue
 n=row['args'].get('frame_count',0);folder=S/'raw'/row['name'];folder.mkdir(parents=True,exist_ok=True);banks.append((row['name'],folder,n or 1))
 for f in range(1,n+1) if n else [0]:work.append((jid,f,folder/f'{(f-1 if n else 0):02}.png'))
def get(w):
 jid,f,p=w
 if p.exists():return
 url=f'https://api.pixellab.ai/mcp/images/{jid}/download?index={f}'
 for attempt in range(3):
  try:
   with urllib.request.urlopen(url,timeout=90) as r:b=r.read()
   assert b.startswith(b'\x89PNG\r\n\x1a\n');p.write_bytes(b);return
  except Exception:
   if attempt==2:raise
   time.sleep(1)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(get,work))
audit=[]
for name,folder,n in banks:
 sheet=Image.new('RGB',(8*180,((n+7)//8)*202),'#101620');d=ImageDraw.Draw(sheet);bounds=[]
 for i,p in enumerate(sorted(folder.glob('*.png'))):
  im=Image.open(p).convert('RGBA');bb=im.getbbox();bounds.append(bb);assert im.width%2==0 and im.height%2==0
  im.thumbnail((176,176),Image.Resampling.NEAREST);x=i%8*180;y=i//8*202;sheet.paste(im,(x,y),im);d.text((x+4,y+180),f'{name} {i}',fill='white')
 sheet.save(O/(name+'-raw-contact.jpg'));audit.append(dict(name=name,frames=n,bounds=bounds))
(S/'raw-alpha-audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(dict(downloads=len(work),banks=[b[0] for b in banks])))
