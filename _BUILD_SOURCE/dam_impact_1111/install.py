from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).parent;R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/dam-impact';C=W/'candidate';before=json.loads((W/'before.json').read_text());assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in before.items()),'Concurrent source changes';A=R/'_BUILD_SOURCE/dam_impact_1111';A.mkdir(parents=True,exist_ok=True);D=R/'assets/game/shared/combat/dam_impact_1111';D.mkdir(parents=True,exist_ok=True)
for n in ['index.html','assets/helicopter_death_1111.js']:
 backup=A/(Path(n).name+'.before')
 if not backup.exists():shutil.copy2(R/n,backup)
s=(R/'index.html').read_text(encoding='utf-8');tags='<script src="assets/dam_impact_art_1111.js?v=h127-1"></script>\n<script src="assets/dam_impact_1111.js?v=h127-1"></script>\n';assert'dam_impact_1111.js'not in s;(C/'index.html').write_text(s.replace('</body>',tags+'</body>'),encoding='utf-8',newline='\n');shutil.copy2(W/'runtime.js',C/'dam_impact_1111.js')
for p in(C/'art').glob('*.png'):shutil.copy2(p,D/p.name)
for n in ['dam_impact_art_1111.js','dam_impact_1111.js','helicopter_death_1111.js']:shutil.copy2(C/n,R/'assets'/n)
shutil.copy2(C/'index.html',R/'index.html');shutil.copy2(C/'helicopter_death_1111.js',R/'_BUILD_SOURCE/helicopter_death_1111/runtime.js')
for n in ['build.py','runtime.js','install.py','before.json','source-measurements.json']:shutil.copy2(W/n,A/n)
shutil.copy2(O/'art.json',A/'art.json');print('Installed central-dam impact route and authored white-flash transition')
