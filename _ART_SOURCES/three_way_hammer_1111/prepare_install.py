from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');B=W/'before';B.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
addon=(W/'runtime-addon.js').read_bytes();prepared=(W/'whole_hammer_1110.js').read_bytes();assert prepared.endswith(addon)and prepared[:-len(addon)]==(R/'assets/whole_hammer_1110.js').read_bytes(),'Live whole-hammer source changed; merge before installation'
prior=json.loads((W.parent/'solid_hammer_1111/installation.json').read_text());assert sha(R/'assets/overhead_slam_art_1111.js')==prior['after']['assets/overhead_slam_art_1111.js'],'Live art registration changed; merge before installation'
files=['assets/overhead_slam_art_1111.js','assets/whole_hammer_1110.js'];textures=[f'assets/game/shared/combat/three_way_hammer_1111/{p.name}'for p in(W/'exports').glob('*.webp')];assert len(textures)==30
for n in files:
 p=B/n;p.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(R/n,p)
before={n:sha(R/n)for n in files}
for n in textures:
 if(R/n).exists():
  p=B/n;p.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(R/n,p);before[n]=sha(R/n)
plan=dict(before=before,files=files+textures,protected={n:sha(R/n)for n in ['assets/game.js','assets/boss_animation_1109.js']})
(W/'installation-plan.json').write_text(json.dumps(plan,indent=2));print('Prepared30 art files, two scoped registrations/controllers and matching backups.',flush=True)
