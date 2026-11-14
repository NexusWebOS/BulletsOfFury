from pathlib import Path
import subprocess,json
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');out=[]
for name,args in [('game-syntax',['node','--check','assets/game.js']),('restoration-syntax',['node','--check','assets/boss_restore_1112.js']),('full-suite',['node','_BUILD_SOURCE/test_fl.js'])]:
 p=subprocess.run(args,cwd=R,capture_output=True,encoding='utf-8',errors='replace');s=p.stdout+'\n'+p.stderr;(W/(name+'.log')).write_text(s,encoding='utf-8');out.append(dict(name=name,exit=p.returncode,tail=s[-1700:]));print(name,p.returncode,flush=True)
(W/'broad-checks.json').write_text(json.dumps(out,indent=2));assert all(x['exit']==0 for x in out if x['name']!='full-suite')
