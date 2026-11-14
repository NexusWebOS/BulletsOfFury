from pathlib import Path
import json,hashlib,shutil,subprocess,sys
from PIL import Image
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Front-facing-hammer'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if '--finalize'in sys.argv:
 subprocess.run([sys.executable,str(W/'finalize.py')],check=True);sys.exit(0)
if '--password-diagnose'in sys.argv:
 subprocess.run([sys.executable,str(W/'verify_password.py'),'--diagnose'],check=True);sys.exit(0)
plan=json.loads((W/'installation-plan.json').read_text());runtime_fix='--runtime-fix'in sys.argv;verify_only='--verify-only'in sys.argv or runtime_fix
expected=json.loads((W/'installation.json').read_text())['after']if verify_only else plan['before']
for n,h in expected.items():assert sha(R/n)==h,('Source changed during preparation',n)
for n in ['whole_hammer_1110.js','front_hammer_art_1111.js']:subprocess.run(['node','--check',str(W/n)],check=True)
if runtime_fix:subprocess.run(['node','--check',str(W/'boss_animation_1109.js')],check=True)
for j in json.loads((W/'aseprite-jobs.json').read_text()):
 a=Image.open(W/'exports'/(j['name']+'_regular.png')).convert('RGBA');b=Image.open(W/'exports'/(j['name']+'_roundtrip.png')).convert('RGBA');assert a.tobytes()==b.tobytes(),j['name']
if not verify_only:
 target=R/'assets/game/shared/combat/front_hammer_1111';target.mkdir(exist_ok=True,parents=True);files=list((W/'exports').glob('*.webp'));assert len(files)==30
 for p in files:shutil.copy2(p,target/p.name)
 shutil.copy2(W/'front_hammer_art_1111.js',R/'assets/overhead_slam_art_1111.js');shutil.copy2(W/'whole_hammer_1110.js',R/'assets/whole_hammer_1110.js')
if runtime_fix:
 for n in ['whole_hammer_1110.js','boss_animation_1109.js']:shutil.copy2(W/n,R/'assets'/n)
assert sha(R/'assets/game.js')==plan['before']['assets/game.js']
(W/'installation.json').write_text(json.dumps(dict(textures=30,updatedTimelineFrames=128,before=plan['before'],after={n:sha(R/n)for n in plan['before']}),indent=2))
print('Installed frontal down/sides for both forms and normal/Chromium/red hammer states.',flush=True)
if runtime_fix:subprocess.run([sys.executable,str(W/'verify_password.py')],check=True)
for stage in [5,8]:
 subprocess.run([sys.executable,str(W.parent/f'verify_front_stage{stage}.py'),str(stage)],check=True)
 q=json.loads((O/f'verification-stage{stage}/checks.json').read_text());assert not q['errors']and all(c['passed']for c in q['checks']),dict(failed=[c['name']for c in q['checks']if not c['passed']],errors=q['errors'])
subprocess.run(['node','--check','assets/game.js'],cwd=R,check=True)
full=subprocess.run(['node','_BUILD_SOURCE/test_fl.js'],cwd=R,capture_output=True,text=True,encoding='utf8',errors='replace');(W/'full-suite.txt').write_text(full.stdout+'\n'+full.stderr,encoding='utf8');(W/'full-suite.json').write_text(json.dumps(dict(exit=full.returncode,lastError=full.stderr[-1600:]),indent=2))
print('Broad suite exit',full.returncode,full.stderr[-500:],flush=True)
