from pathlib import Path
import json,shutil,hashlib,os,re
W=Path(__file__).resolve().parents[2]/'_ART_SOURCES/whole_hammer_1110';R=Path(os.environ.get('BOF_ROOT',r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury'));D=R/'assets/game/shared/combat/whole_hammer_1110';D.mkdir(exist_ok=True)
M=json.loads((W/'manifest.json').read_text());H=json.loads((W/'flight-meta.json').read_text())
for p in(W/'exports').glob('*.webp'):shutil.copy2(p,D/p.name)
p=R/'assets/boss_animation_1109.js';current=p.read_text(encoding='utf8');prior=(Path(__file__).resolve().parent/'boss_animation_before.js').read_text(encoding='utf8');candidate=(Path(__file__).resolve().parent/'boss_animation_1109.js').read_text(encoding='utf8');assert current in [prior,candidate],'Boss animation owner changed concurrently; inspect before applying.'
p.write_text(candidate,encoding='utf8')
(R/'assets/rigid_hammer_art_1110.js').write_text("'use strict';\nObject.assign(BA119_ART,"+json.dumps(M,separators=(',',':'))+');\nconst RH1110_HEADS='+json.dumps(H,separators=(',',':'))+';\n',encoding='utf8')
shutil.copy2(Path(__file__).resolve().parent/'whole_hammer_1110.js',R/'assets/whole_hammer_1110.js')
p=R/'index.html';s=p.read_bytes();marker=b'<script src="assets/boss_preview_loading_1109.js';assert marker in s
if b'assets/whole_hammer_1110.js'not in s:
 eol=b'\r\n'if b'\r\n'in s else b'\n';s=s.replace(marker,b'<script src="assets/whole_hammer_1110.js?v=1"></script>'+eol+marker);p.write_bytes(s)
for asset in [b'rigid_hammer_art_1110',b'boss_animation_1109',b'whole_hammer_1110']:
 s=re.sub(rb'(assets/'+asset+rb'\.js)(?:\?[^\"]*)?',rb'\1?v=whole-1110-2',s)
if p.read_bytes()!=s:p.write_bytes(s)
print('Installed complete generated held-weapon poses:',len(M),'banks;',len(list(D.glob('*.webp'))),'material textures. No held weapon assembly.')
