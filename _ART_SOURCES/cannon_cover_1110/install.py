from pathlib import Path
import shutil,json,hashlib
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;O=W.parents[1]/'outputs/cannon-cover';m=json.loads((O/'manifest.json').read_text());p=R/'assets/thunderhead_reactor_1105.js';assert hashlib.sha256(p.read_bytes()).hexdigest()==m['expected_source_hash'],'Concurrent cannon changes'
A=R/'_ART_SOURCES/cannon_cover_1110';A.mkdir(parents=True,exist_ok=True);D=R/'assets/game/shared/combat/cannon_cover_1110';D.mkdir(parents=True,exist_ok=True)
if not(A/'before.js').exists():shutil.copy2(p,A/'before.js')
for n in ['build.py']:shutil.copy2(W/n,A/n)
shutil.copy2(O/'manifest.json',A/'manifest.json')
for f in (W/'candidate/frames').glob('*.png'):shutil.copy2(f,D/f.name)
for f in (O/'editable').glob('*.aseprite'):shutil.copy2(f,A/f.name)
shutil.copy2(W/'candidate/thunderhead_reactor_1105.js',p);print('Installed continuous cannon-opening coverage until attack animation finishes')
