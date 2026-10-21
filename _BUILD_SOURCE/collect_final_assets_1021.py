from pathlib import Path
from PIL import Image,ImageDraw
import json,re,concurrent.futures,urllib.request,time,sys
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');S=R/'_ART_SOURCES/final_version_1021';T=Path(__file__).parent;O=R/'_shots/final_version_1021'
byname={};receipt_files={p.name:p for p in S.glob('final21_*.json')};receipt_files.update({p.name:p for p in T.glob('final21_*.json')})
for p in receipt_files.values():
 data=json.loads(p.read_text())
 if not isinstance(data,list):continue
 for q in data:
  if isinstance(q,dict) and 'args' in q and q.get('receipt') and not q['receipt'][0].startswith('error'):byname[q['name']]=q
jobs=list(byname.values())
for q in jobs:
 if q['name']=='warp_loop':q['status']='cancelled';q['reason']='Rejected source contained an opaque gray matte; cancelled immediately and replaced by the approved portal animation in the native screen-warp owner.'
(S/'all-generation-jobs.json').write_text(json.dumps(jobs,indent=2));selected=set(sys.argv[1:]);work=[];banks=[]
for row in jobs:
 name=row['name']
 if row.get('status')=='cancelled':continue
 if selected and name not in selected:continue
 txt='\n'.join(row['receipt']);m=re.search(r'job_id: ([\w-]+)|"job_id": "([\w-]+)"',txt)
 if not m:continue
 jid=m.group(1) or m.group(2);n=row['args'].get('frame_count',0);folder=S/'raw'/name;folder.mkdir(parents=True,exist_ok=True);banks.append((name,folder,n or 1))
 for f in range(1,n+1) if n else [0]:work.append((jid,f,folder/f'{(f-1 if n else 0):02}.png'))
def get(w):
 jid,f,p=w
 if p.exists():return
 for attempt in range(3):
  try:
   with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{jid}/download?index={f}',timeout=90) as r:b=r.read()
   assert b.startswith(b'\x89PNG\r\n\x1a\n');p.write_bytes(b);return
  except Exception:
   if attempt==2:raise
   time.sleep(1)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(get,work))
audit=[]
for name,folder,n in banks:
 sheet=Image.new('RGB',(8*180,((n+7)//8)*202),'#101620');d=ImageDraw.Draw(sheet);bounds=[]
 for i,p in enumerate(sorted(folder.glob('*.png'))):
  im=Image.open(p).convert('RGBA');bb=im.getbbox();bounds.append(bb)
  im.thumbnail((176,176),Image.Resampling.NEAREST);x=i%8*180;y=i//8*202;sheet.paste(im,(x,y),im);d.text((x+4,y+180),f'{name} {i}',fill='white')
 sheet.save(O/(name+'-raw-contact.jpg'));audit.append(dict(name=name,frames=n,bounds=bounds))
(S/'collect-last.json').write_text(json.dumps(audit,indent=2));print(json.dumps(dict(downloads=len(work),banks=[b[0] for b in banks])))
