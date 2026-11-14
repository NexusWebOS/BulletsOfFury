from pathlib import Path
import json,hashlib,shutil,subprocess
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=['assets/game.js','assets/whole_hammer_1110.js','assets/rage_palm_1110.js','assets/boss_ship_forms_1111.js','assets/draconus_modular_1111.js','assets/overhead_slam_art_1111.js','assets/playtest_repairs_1108.js'];before={p:sha(R/p)for p in protected}
for name in ['boss_restore_art_1112.js','boss_restore_1112.js']:
 subprocess.run(['node','--check',str(W/name)],check=True);shutil.copy2(W/name,R/'assets'/name)
dest=R/'assets/game/shared/combat/boss_restore_1112';dest.mkdir(exist_ok=True)
for p in (W/'exports').glob('*.webp'):shutil.copy2(p,dest/p.name)
p=R/'index.html';old=p.read_bytes();s=old.decode('utf-8');nl='\r\n'if'\r\n'in s else'\n'
if 'assets/boss_restore_1112.js'not in s:
 marker='<script src="assets/boss_animation_1109.js?v=whole-1110-2"></script>';assert s.count(marker)==1
 s=s.replace(marker,'<script src="assets/boss_restore_art_1112.js?v=1"></script>'+nl+marker)
 s=s.replace('</body>','<script src="assets/boss_restore_1112.js?v=1"></script>'+nl+'</body>')
 (W/'index.before.html').write_bytes(old);assert p.read_bytes()==old;p.write_bytes(s.encode('utf-8'))
assert all(sha(R/p)==h for p,h in before.items())
(W/'installation.json').write_text(json.dumps(dict(protected=before,runtime=sha(R/'assets/boss_restore_1112.js'),art=sha(R/'assets/boss_restore_art_1112.js')),indent=2))
print('Installed recovered sideways banks and restored original Stage5 formation/wave owners; protected current ships, guns and overheads.')
