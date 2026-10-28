from pathlib import Path
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/pixellab_hammer_1023';O=W/'shipping';T=R/'assets/game/shared/combat/pixellab_hammer_1023';T.mkdir(parents=True,exist_ok=True)
A=json.loads((O/'manifest.json').read_text());A['sources']['sideJob']='85c23e09-9c8e-4845-82dc-ee94694dd636';A['owner']='_BUILD_SOURCE/build_pixellab_hammer_candidate_1023.py';A['weaponUnit']=.13
for S in A['sheets'].values():
 name=Path(S['path']).name;S['path']='assets/game/shared/combat/pixellab_hammer_1023/'+name;S['sha256']=hashlib.sha256((O/name).read_bytes()).hexdigest();shutil.copy2(O/name,T/name)
(T/'manifest.json').write_text(json.dumps(A,indent=2));shutil.copy2(O/'rig.json',T/'rig.json')
original=(O/'candidate.js').read_text();tail=original[original.index('for(const s of Object.values'):].replace('MA23_CANDIDATE','PH23_ART')
retire='''const PH23_RETIRED=new Set();let PH23_RETIRED_BYTES=0;
for(const bank of Object.keys(PH23_ART.banks))for(const a of HF22_ART.banks[bank]||[])for(const id of [a.sheet,a.white?a.sheet+'_hit':null]){const s=id&&HF22_ART.sheets[id];if(s&&!PH23_RETIRED.has(s.key)){PH23_RETIRED.add(s.key);PH23_RETIRED_BYTES+=(s.w||0)*(s.h||0)*4;}}
const PH23_KEYS=hf22Keys;hf22Keys=function(n,legacy=false){const keys=PH23_KEYS.apply(this,arguments);return n===8?keys.filter(k=>!PH23_RETIRED.has(k)):keys;};
'''
(R/'assets/pixellab_hammer_1023.js').write_text('"use strict";\n/* Accepted PixelLab body motion; one exact authored weapon, baked offline. */\nconst PH23_ART='+json.dumps(A,separators=(',',':'))+';\n'+retire+tail,encoding='utf-8',newline='\n')
p=R/'index.html';data=p.read_bytes();nl=b'\r\n'if b'\r\n'in data else b'\n'
if b'pixellab_hammer_1023.js'not in data:data=data.replace(b'</body>',b'<script src="assets/pixellab_hammer_1023.js?v=ph23-1"></script>'+nl+b'</body>');p.write_bytes(data)
print("Installed accepted PixelLab actor banks and fixed prop.")
