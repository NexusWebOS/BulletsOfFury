from pathlib import Path
import subprocess,json,sys
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.stdout.reconfigure(encoding='utf-8');out=[]
for name,cmd in [('game-syntax',['node','--check','assets/game.js']),('modular-syntax',['node','--check','assets/draconus_modular_1111.js']),('capture-syntax',['node','--check',str(W/'record-capture.js')]),('input-syntax',['node','--check',str(W/'record-input.js')]),('full-suite',['node','_BUILD_SOURCE/test_fl.js'])]:
 p=subprocess.run(cmd,cwd=R,capture_output=True,encoding='utf-8',errors='replace');(W/(name+'.log')).write_text(p.stdout+'\n'+p.stderr,encoding='utf-8');out.append(dict(name=name,exit=p.returncode,tail=(p.stdout+'\n'+p.stderr)[-1500:]));print(name,'exit',p.returncode,flush=True)
(W/'preflight.json').write_text(json.dumps(out,indent=2));assert all(x['exit']==0 for x in out if x['name']!='full-suite')
