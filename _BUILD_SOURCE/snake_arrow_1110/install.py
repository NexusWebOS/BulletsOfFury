from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).parent;O=W.parents[1]/'outputs/snake-arrow';m=json.loads((O/'manifest.json').read_text());R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');A=R/'_BUILD_SOURCE/snake_arrow_1110';A.mkdir(parents=True,exist_ok=True)
for r in m['targets']:assert hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['before_sha256'],'Concurrent warning edits'
for r in m['targets']:
 p=Path(r['path']);bk=A/(r['name']+'.before');
 if not bk.exists():shutil.copy2(p,bk)
 shutil.copy2(W/'candidate'/(r['name']+'.js'),p)
for n in ['build.py','install.py']:shutil.copy2(W/n,A/n)
shutil.copy2(O/'manifest.json',A/'manifest.json');print('Installed one arrow per living snake at its entry side')
