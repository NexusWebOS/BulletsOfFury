from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).parent;R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/helicopter-death';C=W/'candidate';before=json.loads((W/'before.json').read_text());assert hashlib.sha256((R/'index.html').read_bytes()).hexdigest()==before['index.html'],'Concurrent index change';A=R/'_BUILD_SOURCE/helicopter_death_1111';A.mkdir(parents=True,exist_ok=True);D=R/'assets/game/shared/combat/helicopter_death_1111';D.mkdir(parents=True,exist_ok=True)
if not(A/'index.before').exists():shutil.copy2(R/'index.html',A/'index.before')
s=(R/'index.html').read_text(encoding='utf-8');tags='<script src="assets/helicopter_death_art_1111.js?v=h126-1"></script>\n<script src="assets/helicopter_death_1111.js?v=h126-1"></script>\n';assert 'helicopter_death_1111.js'not in s;(C/'index.html').write_text(s.replace('</body>',tags+'</body>'),encoding='utf-8',newline='\n');shutil.copy2(W/'runtime.js',C/'helicopter_death_1111.js')
for p in(C/'art').glob('*.png'):shutil.copy2(p,D/p.name)
for n in ['helicopter_death_art_1111.js','helicopter_death_1111.js']:shutil.copy2(C/n,R/'assets'/n)
shutil.copy2(C/'index.html',R/'index.html');shutil.copytree(W/'sources',A/'sources',dirs_exist_ok=True)
for n in ['assets.py','runtime.js','install.py','export.py','reference.json','before.json']:shutil.copy2(W/n,A/n)
for n in ['art.json','explosion-master.png']:shutil.copy2(O/n,A/n)
print('Installed actual-airframe helicopter death spirals, escalating trails and shatter banks')
