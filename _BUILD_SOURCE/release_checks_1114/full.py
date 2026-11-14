from pathlib import Path
import subprocess,json,hashlib,time
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Release-checks-1114';O.mkdir(exist_ok=True);results=[]
for name,cmd in [('game-syntax',['node','--check','assets/game.js']),('health-helper-syntax',['node','--check','assets/difficulty_helpers_1114.js']),('difficulty-rules-syntax',['node','--check','assets/difficulty_rules_1101.js']),('full-suite',['node','_BUILD_SOURCE/test_fl.js'])]:
 start=time.monotonic();q=subprocess.run(cmd,cwd=R,capture_output=True,text=True,encoding='utf-8',errors='replace');text=q.stdout+q.stderr;(O/(name+'.log')).write_text(text,encoding='utf-8');r=dict(name=name,exit=q.returncode,seconds=time.monotonic()-start,passedLines=sum(line.startswith('  ok')for line in text.splitlines()),failures=[line for line in text.splitlines()if'ASSERT FAIL:'in line],tail=text[-6000:]);results.append(r);print(name,q.returncode,'passes',r['passedLines'],text[-4800:]if q.returncode else text[-250:],flush=True)
(O/'full-results.json').write_text(json.dumps(results,indent=2));assert all(q['exit']==0 for q in results)
