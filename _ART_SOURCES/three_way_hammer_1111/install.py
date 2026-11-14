from pathlib import Path
import json,hashlib,shutil,subprocess,sys
from PIL import Image
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Three-way-hammer';O.mkdir(exist_ok=True,parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if '--finalize'in sys.argv:subprocess.run([sys.executable,str(W/'finalize.py')],check=True);sys.exit(0)
plan=json.loads((W/'installation-plan.json').read_text());verify='--verify-only'in sys.argv
expected=json.loads((W/'installation.json').read_text())['after']if verify else plan['before']
for n,h in {**expected,**plan['protected']}.items():assert sha(R/n)==h,('Changed during preparation',n)
for n in ['front_hammer_art_1111.js','whole_hammer_1110.js']:subprocess.run(['node','--check',str(W/n)],check=True)
if not verify:
 subprocess.run([sys.executable,str(W/'audit.py')],check=True)
 for n in plan['files']:
  p=R/n;p.parent.mkdir(exist_ok=True,parents=True);source=W/'front_hammer_art_1111.js'if n.endswith('overhead_slam_art_1111.js')else W/'whole_hammer_1110.js'if n.endswith('whole_hammer_1110.js')else W/'exports'/Path(n).name;shutil.copy2(source,p)
 (W/'installation.json').write_text(json.dumps(dict(before=plan['before'],after={n:sha(R/n)for n in plan['files']},protected=plan['protected']),indent=2))
 print('Installed center/right/left whole hammer cycles in all four forms.',flush=True)
for stage in [5,8]:
 subprocess.run([sys.executable,str(W/f'verify_stage{stage}.py'),str(stage)],check=True)
 q=json.loads((O/f'verification-stage{stage}/checks.json').read_text());assert not q['errors']and all(c['passed']for c in q['checks']),dict(failed=[c['name']for c in q['checks']if not c['passed']],errors=q['errors'])
subprocess.run([sys.executable,str(W/'verify_password.py')],check=True)
subprocess.run(['node','--check','assets/game.js'],cwd=R,check=True)
full=subprocess.run(['node','_BUILD_SOURCE/test_fl.js'],cwd=R,capture_output=True,text=True,encoding='utf8',errors='replace');(W/'full-suite.txt').write_text(full.stdout+'\n'+full.stderr,encoding='utf8');(W/'full-suite.json').write_text(json.dumps(dict(exit=full.returncode,lastError=full.stderr[-1600:]),indent=2));print('Broad suite exit',full.returncode,full.stderr[-550:],flush=True)
