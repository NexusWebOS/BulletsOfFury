"""Render the checklist and easiest-to-hardest queue from the editable JSON."""
from pathlib import Path
from collections import Counter
import json
R=Path(__file__).resolve().parents[1];D=R/'docs';data=json.loads((D/'REQUEST_CHECKLIST_0914.json').read_text(encoding='utf-8'));items=data['items'];counts=Counter(x['status']for x in items)
assert len({x['id']for x in items})==len(items)
assert set(counts)<= {'complete','partial','pending'}
for x in items:
 if x['status']=='complete':assert x['evidence'],x['id']
 if x['evidence']:assert (D/x['evidence']).is_file(),x['evidence']
queue=sorted((x for x in items if x['status']!='complete'),key=lambda x:x['workOrder'])
assert len({x['workOrder']for x in queue})==len(queue)
assets=sum(x['status']!='complete'and x['dependency']=='SpriteCook'for x in items)
naming=sum(x['status']!='complete'and x['dependency']=='Mike naming'for x in items)
tally=f"**{len(items)} entries: {counts['complete']} complete / {counts['partial']} partial / {counts['pending']} pending.**"
lines=['# Bullets of Fury — request checklist','',f"Updated {data['updated']}. "+tally,'',f"**{len(queue)} remain unfinished.** {assets} depend on SpriteCook production assets; {naming} needs a model-name decision. These are included in the totals.",'',data['scope'],'','Complete gameplay entries mean implementation and recorded native-browser proof. Source-identification entries mean the approved file was located and visually inspected; they do not certify asset production or integration. Evidence records the checked version and limitations; earlier scenes are not all re-recorded in each batch. Partial means a limited pass exists and the remaining work is stated. Unchecked rows are unfinished.','', 'Detailed specifications: [original request ledger](OVERNIGHT_REQUESTS_0914.md). Execution sequence: [easiest-to-hardest work order](WORK_ORDER_0914.md).','', '## Current batch and next work','']
b=data['latestBatch'];lines += [f"Just verified: {b['description']} [Proof]({b['evidence']}).",'',data['queuePolicy'],'','Mike selected furyship_somersault_13.png and approved image_gen for its replacement family. The new ship, rolls, somersaults, parts, transition effects, all nine palettes and SPCBOY legacy selection are integrated. His latest assembly direction uses solid top views, rotation and individual bottom arrivals; perspective blending is superseded. SPACE-12 remains partial for flight silhouette/width consistency and exact component fit. The remaining encounter and feature queue is preserved.','', '## Tally by area','', '| Area | Complete | Partial | Pending | Total |','| --- | ---: | ---: | ---: | ---: |']
groups=list(dict.fromkeys(x['group']for x in items))
for g in groups:
 rows=[x for x in items if x['group']==g];c=Counter(x['status']for x in rows);lines.append(f"| {g} | {c['complete']} | {c['partial']} | {c['pending']} | {len(rows)} |")
lines+=['', '## Checklist','']
for g in groups:
 lines+=['### '+g,'']
 for x in items:
  if x['group']!=g:continue
  line=f"- [{'x' if x['status']=='complete' else ' '}] **{x['id']} · {x['status'].title()}** — {x['request']}"
  if x['dependency']:line+=' Dependency: '+x['dependency']+'.'
  if x['evidence']:line+=f" [Evidence]({x['evidence']})."
  lines.append(line)
 lines.append('')
lines+=['## Keeping this tally current','', 'Edit stable IDs in [REQUEST_CHECKLIST_0914.json](REQUEST_CHECKLIST_0914.json), then run `python _BUILD_SOURCE/update_request_checklist.py`. Update status, evidence and workOrder together. The renderer checks IDs, evidence files and unique queue order, then recomputes totals. Do not split finished details merely to inflate completion.','']
(D/'REQUEST_CHECKLIST_0914.md').write_bytes('\n'.join(lines).encode('utf-8'))
q=['# Bullets of Fury — easiest-to-hardest work order','',tally,'',data['queuePolicy'],'','Completed entries are excluded. The list below contains every unfinished item exactly once. Partial items retain that status. Difficulty bands are estimates, not promises that an unchecked feature already works. Asset/naming dependencies can be skipped until available.','']
band=None
for n,x in enumerate(queue,1):
 if x['difficultyBand']!=band:band=x['difficultyBand'];q+=['## '+band,'']
 line=f"{n}. **{x['id']} · {x['status'].title()}** — {x['request']}"
 if x['dependency']:line+=' Dependency: '+x['dependency']+'.'
 q.append(line)
 if n==len(queue)or queue[n]['difficultyBand']!=band:q.append('')
q+=['Full completed list and evidence: [request checklist](REQUEST_CHECKLIST_0914.md).','']
(D/'WORK_ORDER_0914.md').write_bytes('\n'.join(q).encode('utf-8'))
print(dict(counts),'total',len(items),'queued',len(queue),'SpriteCook-dependent',assets)
