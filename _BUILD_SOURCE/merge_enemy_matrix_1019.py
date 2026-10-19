"""Retain unaffected native cases; replace Stage 6 with its isolated factory audit."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];S=R/'_shots/overnight_combat_1019'
baseFolder='enemy_matrix/shipping-final-ai';freshFolder='enemy_matrix/stage6-factory-final';out=S/'enemy_matrix/shipping-final-factory';out.mkdir(exist_ok=True)
base=json.loads((S/baseFolder/'report.json').read_text());fresh=json.loads((S/freshFolder/'report.json').read_text())
assert base['complete'] and not base['errors'] and len(base['rosters'])==27
assert not fresh['errors'] and len(fresh['rosters'])==3 and {r['stage'] for r in fresh['rows']}=={6}
assert len(fresh['rows'])==sum(len(v) for v in fresh['rosters'].values())
assert all(r['state']['finite'] and not r['metrics'].get('waves') for r in fresh['rows'])
assert all(r.get('screenshot') and 'groundTraits' in r['metrics'] for r in fresh['rows'] if r['spec'].get('flight'))
rows=[dict(r,sourceFolder=baseFolder) for r in base['rows'] if r['stage']!=6]+[dict(r,sourceFolder=freshFolder) for r in fresh['rows']]
rosters={k:v for k,v in base['rosters'].items() if not k.startswith('6-')};rosters.update(fresh['rosters']);expected=sum(len(v) for v in rosters.values());assert len(rosters)==27 and len(rows)==expected
method=base['method']+' Stage 6 is replaced by a fresh native factory audit: queued fb2 stealth passes are materialized during collection, distinguished by role/direction, then replayed through their real factory. Pending flight-plan queues are cleared between cases. Plane release clocks start at the actual aircraft spawn; pre-flight plan warnings are outside this isolated actor clock. Unaffected stages retain their verified native rows with per-row sourceFolder provenance.'
data=dict(version=7,complete=True,expected=expected,method=method,sources=[baseFolder+'/report.json',freshFolder+'/report.json'],rows=rows,rosters=rosters,errors=[])
(out/'report.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(version=7,cases=len(rows),newStage6=len(fresh['rows']),errors=[])))
