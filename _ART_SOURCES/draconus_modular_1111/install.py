from pathlib import Path
import shutil,json,hashlib,subprocess
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['assets/game.js','assets/boss_ship_forms_1111.js','assets/whole_hammer_1110.js','assets/chronos_rotor_1025.js','assets/overhead_slam_art_1111.js','assets/rage_palm_1110.js'];before={n:sha(R/n)for n in names}
for name in ['draconus_modular_art_1111.js','draconus_modular_1111.js']:subprocess.run(['node','--check',str(W/name)],check=True)
D=R/'assets/game/shared/combat/draconus_modular_1111';D.mkdir(parents=True,exist_ok=True)
for p in (W/'exports').glob('*.webp'):shutil.copy2(p,D/p.name)
for n in ['draconus_modular_art_1111.js','draconus_modular_1111.js']:shutil.copy2(W/n,R/'assets'/n)
p=R/'index.html';s=p.read_text(encoding='utf-8');h=sha(p)
if 'assets/draconus_modular_1111.js'not in s:
 assert '</body>'in s;new=s.replace('</body>','\n<script src="assets/draconus_modular_art_1111.js"></script>\n<script src="assets/draconus_modular_1111.js"></script>\n</body>',1);assert sha(p)==h;p.write_text(new,encoding='utf-8',newline='')
assert before=={n:sha(R/n)for n in names};(W/'installation.json').write_text(json.dumps(dict(protected=before,runtime=sha(R/'assets/draconus_modular_1111.js'),art=sha(R/'assets/draconus_modular_art_1111.js'),index=sha(p)),indent=2));print('Wired Draconus modular gun. Existing hammer/ship/native health owners preserved.',flush=True)
