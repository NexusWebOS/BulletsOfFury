from pathlib import Path
import subprocess,json
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');rows=[]
for name,args in [('game-syntax',['node','--check','assets/game.js']),('cinematic-rage-syntax',['node','--check','assets/draconus_cinematic_rage_1113.js']),('rage-owner-syntax',['node','--check','assets/rage_palm_1110.js']),('full-suite',['node','_BUILD_SOURCE/test_fl.js'])]:
 p=subprocess.run(args,cwd=R,capture_output=True,encoding='utf-8',errors='replace');s=p.stdout+'\n'+p.stderr;(W/(name+'.log')).write_text(s,encoding='utf-8');rows.append(dict(name=name,exit=p.returncode,tail=s[-1700:]));print(name,p.returncode,flush=True)
(W/'broad-checks.json').write_text(json.dumps(rows,indent=2));assert all(q['exit']==0 for q in rows if q['name']!='full-suite')
