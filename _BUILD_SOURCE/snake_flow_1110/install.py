from pathlib import Path
import hashlib,json,shutil
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;O=W.parents[1]/'outputs/snake-flow';m=json.loads((O/'manifest.json').read_text());p=R/'assets'/m['owner'];assert hashlib.sha256(p.read_bytes()).hexdigest()==m['expected_source_hash'],'Concurrent snake changes'
A=R/'_BUILD_SOURCE/snake_flow_1110';A.mkdir(parents=True,exist_ok=True)
if not(A/'before.js').exists():shutil.copy2(p,A/'before.js')
for n in ['build.py','install.py']:shutil.copy2(W/n,A/n)
shutil.copy2(O/'manifest.json',A/'manifest.json');shutil.copy2(W/'candidate'/p.name,p);print('Installed continuous whole-body slither and jumping follow-through')
