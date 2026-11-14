from pathlib import Path
import subprocess,shutil,json,hashlib
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=['assets/game.js','assets/combat_polish_0927b.js','assets/hardcorps_bosses_1007.js','assets/pursuit_bomber_1027.js','assets/stage5_bomber_gate_1027.js','assets/stage6_roster_1017.js','assets/difficulty_rules_1101.js','assets/draconus_cinematic_rage_1113.js','assets/draconus_cinematic_rage_art_1113.js','assets/chronos_rageform_1026.js','assets/boss_restore_1112.js'];before={n:sha(R/n)for n in protected}
dest=R/'assets/game/levels/stage_05/miniboss/assault_1114';dest.mkdir(exist_ok=True)
for p in(W/'exports').glob('*.webp'):shutil.copy2(p,dest/p.name)
for name in ['stage5_bomber_assault_art_1114.js','stage5_bomber_assault_1114.js']:
 subprocess.run(['node','--check',str(W/name)],check=True);shutil.copy2(W/name,R/'assets'/name)
p=R/'index.html';old=p.read_bytes();s=old.decode('utf-8');nl='\r\n'if'\r\n'in s else'\n'
if 'assets/stage5_bomber_assault_1114.js'not in s:
 (W/'index.before.html').write_bytes(old);added='<script src="assets/stage5_bomber_assault_art_1114.js?v=1"></script>'+nl+'<script src="assets/stage5_bomber_assault_1114.js?v=1"></script>'+nl;new=s.replace('</body>',added+'</body>');assert new!=s and p.read_bytes()==old;p.write_bytes(new.encode('utf-8'))
assert before=={n:sha(R/n)for n in protected}
(W/'installation.json').write_text(json.dumps(dict(protected=before,installed={n:sha(R/'assets'/n)for n in ['stage5_bomber_assault_1114.js','stage5_bomber_assault_art_1114.js']},textures={p.name:sha(p)for p in dest.glob('*.webp')}),indent=2));print('Installed Stage5 bomber assault, preserved native pools/gates/death and other stages.',flush=True)
