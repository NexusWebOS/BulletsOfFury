from pathlib import Path
import shutil,json,hashlib,subprocess
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');A=R/'assets';D=A/'game/shared/combat/boss_ship_forms_1111';D.mkdir(parents=True,exist_ok=True)
protected=['assets/whole_hammer_1110.js','assets/overhead_slam_art_1111.js','assets/rage_palm_1110.js','assets/game.js','assets/hammer_tactical_art_1023.js']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={n:sha(R/n)for n in protected}
subprocess.run(['node','--check',str(W/'boss_ship_forms_1111.js')],check=True)
for p in sorted((W/'exports').glob('*.webp')):shutil.copy2(p,D/p.name)
for n in ['boss_ship_forms_art_1111.js','boss_ship_forms_1111.js']:shutil.copy2(W/n,A/n)
p=R/'index.html';s=p.read_text(encoding='utf-8');h=sha(p);tags='\n<script src="assets/boss_ship_forms_art_1111.js"></script>\n<script src="assets/boss_ship_forms_1111.js"></script>\n'
if 'assets/boss_ship_forms_1111.js'not in s:
 assert '</body>'in s;new=s.replace('</body>',tags+'</body>',1);assert sha(p)==h,'index changed during preparation';p.write_text(new,encoding='utf-8',newline='')
assert before=={n:sha(R/n)for n in protected},'Protected hammer/native files changed'
(W/'install-report.json').write_text(json.dumps(dict(protected=before,artFiles=len(list(D.glob('*.webp'))),index=sha(p)),indent=2))
print('Installed original ships and Draconus gun presentation. Approved hammer and native HP owners preserved.',flush=True)
