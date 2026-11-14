from pathlib import Path
import json,hashlib,shutil,subprocess,sys
from PIL import Image
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if '--finalize'in sys.argv:
 subprocess.run([sys.executable,str(W/'finalize.py')],check=True)
 sys.exit(0)
plan=json.loads((W/'installation-plan.json').read_text())
runtime_fix='--runtime-fix'in sys.argv
expected=json.loads((W/'installation.json').read_text())['after']if runtime_fix else plan['before']
for n,digest in expected.items():assert sha(R/n)==digest,('Source changed while preparing',n)
for n in ['boss_animation_1109.js','whole_hammer_1110.js','heavy_hammer_art_1111.js']:subprocess.run(['node','--check',str(W/n)],check=True)
for j in json.loads((W/'aseprite-jobs.json').read_text()):
 a=Image.open(W/'exports'/(j['name']+'_regular.png')).convert('RGBA');b=Image.open(W/'exports'/(j['name']+'_roundtrip.png')).convert('RGBA');assert a.tobytes()==b.tobytes(),j['name']
if not runtime_fix:
 target=R/'assets/game/shared/combat/heavy_hammer_1111';target.mkdir(exist_ok=True,parents=True)
 files=list((W/'exports').glob('*.webp'));assert len(files)==40,len(files)
 for p in files:shutil.copy2(p,target/p.name)
for n in ['boss_animation_1109.js','whole_hammer_1110.js']:shutil.copy2(W/n,R/'assets'/n)
if not runtime_fix:shutil.copy2(W/'heavy_hammer_art_1111.js',R/'assets/overhead_slam_art_1111.js')
assert sha(R/'assets/game.js')==plan['before']['assets/game.js']
(W/'installation.json').write_text(json.dumps(dict(textures=40,sourceFrames=160,uniqueOriginalDrawings=124,coreUnchanged=True,before=plan['before'],after={n:sha(R/n)for n in plan['before']}),indent=2))
print('Installed complete motion for both forms. Core game.js unchanged. Editable-source roundtrips pixel-exact.',flush=True)
for stage in [5,8]:
 subprocess.run([sys.executable,str(W.parent/f'verify_heavy_stage{stage}.py'),str(stage)],check=True)
 checks=json.loads((W.parents[1]/f'outputs/Heavy-hammer-motion/verification-stage{stage}/checks.json').read_text());assert all(c['passed']for c in checks['checks'])and not checks['errors'],checks
full=subprocess.run(['node','_BUILD_SOURCE/test_fl.js'],cwd=R,capture_output=True,text=True,encoding='utf8',errors='replace')
(W/'full-suite.txt').write_text(full.stdout+'\n'+full.stderr,encoding='utf8')
(W/'full-suite.json').write_text(json.dumps(dict(exit=full.returncode,lastError=full.stderr[-1000:]),indent=2))
print('Broad suite exit',full.returncode,full.stderr[-500:],flush=True)
