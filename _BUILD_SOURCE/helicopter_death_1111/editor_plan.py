from pathlib import Path
import json
W=Path(__file__).parent;O=W.parents[1]/'outputs/helicopter-death';a=json.loads((O/'art.json').read_text());groups={}
for name,rows in a['banks'].items():
 group='real-airframe-debris'if name.startswith('chunk-')else name;groups.setdefault(group,[]).append(name)
plan={g:{'banks':sorted(b),'logical':a['banks'][b[0]][0]['logical']}for g,b in groups.items()};(O/'editor-plan.json').write_text(json.dumps(plan,indent=2))
