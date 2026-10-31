from pathlib import Path
from collections import Counter,defaultdict
import json,sys
W=Path(__file__).resolve().parent;O=W/'review'
rows=[]
for line in (O/'host-telemetry.jsonl').read_text(encoding='utf-8').splitlines():
 try:rows.append(json.loads(line))
 except json.JSONDecodeError:pass
book=defaultdict(list)
for r in rows:book['X-HARRIER'if r.get('xrun')else str(r['stage'])].append(r)
summary=[]
for stage,rs in book.items():
 transitions=[];last=None
 for r in rs:
  label=r['phase']
  if label!=last:transitions.append({'t':r['t'],'phase':label,'hp':r.get('hp')});last=label
 summary.append({'stage':stage,'start':rs[0]['t'],'last':rs[-1]['t'],'elapsed':round(rs[-1]['t']-rs[0]['t'],2),'states':dict(Counter(r['state']for r in rs)),'minLives':min(r['lives']for r in rs),'maxWeaponLevel':max(r['level']for r in rs),'lastScore':rs[-1]['score'],'transitions':transitions})
out={'recordedSeconds':rows[-1]['t'],'stages':summary,'last':rows[-1]}
(O/'analysis-live.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'time':out['recordedSeconds'],'stages':[{k:v for k,v in x.items()if k!='transitions'}for x in summary],'last':{k:rows[-1].get(k)for k in ['state','stage','phase','hp','sim','god','level','bombs','score']}},indent=2))
