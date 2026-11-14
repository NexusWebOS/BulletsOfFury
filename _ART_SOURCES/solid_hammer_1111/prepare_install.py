from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).resolve().parent; R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury'); B=W/'before'; B.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=['assets/overhead_slam_art_1111.js']+[f'assets/game/shared/combat/front_hammer_1111/{n}-overhead_{m}.webp'for n in ['blue','corrupt']for m in ['regular','chrome','red','hit','red_hit']]
protected=['assets/game.js','assets/whole_hammer_1110.js','assets/boss_animation_1109.js']
for n in files:
 p=B/n; p.parent.mkdir(exist_ok=True,parents=True); shutil.copy2(R/n,p)
plan=dict(before={n:sha(R/n)for n in files},protected={n:sha(R/n)for n in protected},files=files)
(W/'installation-plan.json').write_text(json.dumps(plan,indent=2))
print('Prepared11 scoped replacements and matching backups; core gameplay protected.')
