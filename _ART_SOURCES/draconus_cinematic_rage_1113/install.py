from pathlib import Path
import json,hashlib,subprocess,shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=['assets/game.js','assets/boss_restore_1112.js','assets/draconus_front_rage_1113.js','assets/rage_palm_1110.js','assets/boss_ship_forms_1111.js','assets/draconus_modular_1111.js','assets/overhead_slam_art_1111.js','assets/whole_hammer_1110.js','assets/chronos_rageform_1026.js','assets/chronos_kamehameha_1026.js','assets/chronos_energy_audio_1026.js','assets/chronos_lightning_audio_1026.js','assets/chronos_rage_presentation_1026.js']
before={n:sha(R/n)for n in protected};(W/'protected.json').write_text(json.dumps(before,indent=2))
for name in ['draconus_cinematic_rage_art_1113.js','draconus_cinematic_rage_1113.js']:
 subprocess.run(['node','--check',str(W/name)],check=True);shutil.copy2(W/name,R/'assets'/name)
dest=R/'assets/game/shared/combat/draconus_cinematic_rage_1113';dest.mkdir(exist_ok=True)
for p in(W/'exports').glob('*.webp'):shutil.copy2(p,dest/p.name)
p=R/'index.html';old=p.read_bytes();text=old.decode('utf-8');nl='\r\n'if'\r\n'in text else'\n'
if 'assets/draconus_cinematic_rage_1113.js'not in text:
 (W/'index.before.html').write_bytes(old);added='<script src="assets/draconus_cinematic_rage_art_1113.js?v=1"></script>'+nl+'<script src="assets/draconus_cinematic_rage_1113.js?v=1"></script>'+nl
 text=text.replace('</body>',added+'</body>');assert p.read_bytes()==old;p.write_bytes(text.encode('utf-8'))
assert before=={n:sha(R/n)for n in protected}
(W/'installation.json').write_text(json.dumps(dict(protected=before,installed={n:sha(R/'assets'/n)for n in ['draconus_cinematic_rage_1113.js','draconus_cinematic_rage_art_1113.js']},textures={p.name:sha(p)for p in dest.glob('*.webp')}),indent=2))
print('Installed new whole Draconus center, recoup, rage and two-handed casting art with original baked Stage5 effects.',flush=True)
