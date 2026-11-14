from pathlib import Path
import subprocess,json
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Stage5-bomber-assault';results=[]
for name,cmd in [('game-syntax',['node','--check','assets/game.js']),('assault-syntax',['node','--check','assets/stage5_bomber_assault_1114.js']),('art-syntax',['node','--check','assets/stage5_bomber_assault_art_1114.js']),('full-suite',['node','_BUILD_SOURCE/test_fl.js'])]:
 q=subprocess.run(cmd,cwd=R,capture_output=True,text=True,encoding='utf-8',errors='replace');(O/(name+'.log')).write_text(q.stdout+q.stderr,encoding='utf-8');results.append(dict(name=name,returncode=q.returncode,tail=(q.stdout+q.stderr)[-2200:]));print(name,q.returncode,(q.stdout+q.stderr)[-500:],flush=True)
(O/'required-checks.json').write_text(json.dumps(results,indent=2))
assert all(q['returncode']==0 for q in results[:3])
