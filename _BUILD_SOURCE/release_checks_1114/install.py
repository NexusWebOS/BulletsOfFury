from pathlib import Path
import hashlib,subprocess,json,shutil
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['difficulty_helpers_1114.js']:
 subprocess.run(['node','--check',str(W/n)],check=True);(R/'assets'/n).write_bytes((W/n).read_bytes())
p=R/'assets/difficulty_rules_1101.js';b=p.read_bytes();s=b.decode()
if 'const DR15='in s:
 start=s.index('const DR15=');end=s.index("for(const key of ['hard','furious'])",start);nl='\r\n'if'\r\n'in s else'\n';s=s[:start]+"DR15.base={EHP,encounterFloor:encounterFloorDifficultyMul};"+nl+s[end:];assert p.read_bytes()==b;p.write_bytes(s.encode())
p=R/'index.html';b=p.read_bytes();s=b.decode()
if 'assets/difficulty_helpers_1114.js'not in s:
 marker='<script src="assets/game.js';assert marker in s;nl='\r\n'if'\r\n'in s else'\n';s=s.replace(marker,'<script src="assets/difficulty_helpers_1114.js?v=1"></script>'+nl+marker,1);p.write_bytes(s.encode())
s=s.replace('assets/difficulty_rules_1101.js?v=compound15-1101','assets/difficulty_rules_1101.js?v=compound15-1114');p.write_bytes(s.encode())
p=R/'_BUILD_SOURCE/test_fl.js';b=p.read_bytes();s=b.decode();nl='\r\n'if'\r\n'in s else'\n'
if "run('assets/difficulty_helpers_1114.js'"not in s:
 marker="run('assets/game.js', 'game');";assert marker in s;s=s.replace(marker,"run('assets/difficulty_helpers_1114.js', 'difficulty_helpers');"+nl+marker,1)
if "require('./test_difficulty_helpers_1114.cjs')"not in s:
 marker="console.log('\\n============================================');";assert marker in s;s=s.replace(marker,"require('./test_difficulty_helpers_1114.cjs')(vm,ctxv,ok);"+nl+marker,1)
assert p.read_bytes()==b;p.write_bytes(s.encode());assert p.read_bytes().count(b'\n')==p.read_bytes().count(b'\r\n'),'Preserve test runner CRLF'
(R/'_BUILD_SOURCE/test_difficulty_helpers_1114.cjs').write_bytes((W/'test_difficulty_helpers_1114.cjs').read_bytes())
for n in ['stage5_bomber_assault_1114.js','stage5_bomber_assault_art_1114.js']:
 subprocess.run(['node','--check',str(W/n)],check=True);(R/'assets'/n).write_bytes((W/n).read_bytes())
shutil.copy2(W/'exports/retina_tracking_1114.webp',R/'assets/game/levels/stage_05/miniboss/assault_1114/retina_tracking_1114.webp')
p=R/'index.html';b=p.read_bytes();s=b.decode().replace('stage5_bomber_assault_1114.js?v=1','stage5_bomber_assault_1114.js?v=2').replace('stage5_bomber_assault_art_1114.js?v=1','stage5_bomber_assault_art_1114.js?v=2');assert p.read_bytes()==b;p.write_bytes(s.encode())
for n in ['assets/difficulty_helpers_1114.js','assets/difficulty_rules_1101.js','_BUILD_SOURCE/test_fl.js','_BUILD_SOURCE/test_difficulty_helpers_1114.cjs']:subprocess.run(['node','--check',str(R/n)],check=True)
print('Installed one shared early helper and regression coverage; live tuning retains its owner.',flush=True)
