from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/profile';p=json.loads((O/'stage6-profile.json').read_text(encoding='utf8'));nodes={n['id']:n for n in p['nodes']};parent={c:n['id']for n in p['nodes']for c in n.get('children',[])};weighted={}
for n,t in zip(p['samples'],p['timeDeltas']):weighted[n]=weighted.get(n,0)+t
def label(n):
 f=nodes[n]['callFrame'];return f['functionName']+' '+f['url'].split('/')[-1]+':'+str(f['lineNumber']+1)
rows=[]
for n,t in sorted(weighted.items(),key=lambda a:-a[1])[:25]:
 chain=[];q=n
 for i in range(20):
  chain.append(label(q));q=parent.get(q)
  if not q:break
 rows.append({'selfMs':round(t/1000,1),'stack':chain})
(O/'hot-stacks.json').write_text(json.dumps(rows,indent=2),encoding='utf8');print(json.dumps(rows[:10],indent=2))
