from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).parent;R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/dracodia-helicopter';C=W/'candidate';before=json.loads((W/'before.json').read_text());assert hashlib.sha256((R/'index.html').read_bytes()).hexdigest()==before['index.html'],'Index changed concurrently';A=R/'_BUILD_SOURCE/helicopter_effects_1111';A.mkdir(parents=True,exist_ok=True);D=R/'assets/game/levels/stage_08/effects/helicopter_1111';D.mkdir(parents=True,exist_ok=True)
if not(A/'index.before').exists():shutil.copy2(R/'index.html',A/'index.before')
s=(R/'index.html').read_text(encoding='utf-8');tags='<script src="assets/helicopter_effects_art_1111.js?v=h125-1"></script>\n<script src="assets/helicopter_effects_1111.js?v=h125-1"></script>\n';assert 'helicopter_effects_1111.js'not in s;(C/'index.html').write_text(s.replace('</body>',tags+'</body>'),encoding='utf-8',newline='\n');shutil.copy2(W/'runtime.js',C/'helicopter_effects_1111.js')
for p in(C/'art').glob('*.png'):shutil.copy2(p,D/p.name)
for n in ['helicopter_effects_art_1111.js','helicopter_effects_1111.js']:shutil.copy2(C/n,R/'assets'/n)
shutil.copy2(C/'index.html',R/'index.html')
for n in ['assets.py','runtime.js','install.py']:shutil.copy2(W/n,A/n)
for n in ['art.json','prompts.json','muzzle-master.png','missile-master.png','tracer-master.png','explosion-master.png']:shutil.copy2(O/n,A/n)
print('Installed H125 helicopter gunfire, missile flight/launch and explosion banks',flush=True)
