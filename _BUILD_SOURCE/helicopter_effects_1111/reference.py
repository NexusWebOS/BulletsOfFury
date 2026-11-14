from pathlib import Path
from PIL import Image
import json,hashlib
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;O=W.parents[1]/'outputs/dracodia-helicopter';O.mkdir(parents=True,exist_ok=True)
def meta(name):
 s=(R/'assets'/name).read_text(encoding='utf-8');return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
A=meta('dracodia_helicopter_art_1030.js');im=Image.new('RGBA',(512,512))
for name,f,at in [('core_6',0,[256,256]),('pod_left',0,[256+A['mounts'][6]['left'][0],256+A['mounts'][6]['left'][1]]),('pod_right',0,[256+A['mounts'][6]['right'][0],256+A['mounts'][6]['right'][1]])]:
 a=A['banks'][name][f];page=Image.open(R/A['pages'][a['key']]['path']).convert('RGBA');x,y,w,h=a['rect'];im.alpha_composite(page.crop((x,y,x+w,y+h)),(round(at[0]+a['offset'][0]),round(at[1]+a['offset'][1])))
im.save(W/'helicopter-reference.png')
files=['game.js','dracodia_helicopter_1030.js','dracodia_helicopter_art_1030.js','dracodia_energy_1110.js','dracodia_energy_art_1110.js','index.html'];before={n:hashlib.sha256((R/n if n=='index.html'else R/'assets'/n).read_bytes()).hexdigest()for n in files};(W/'before.json').write_text(json.dumps(before,indent=2));print('Source helicopter extracted; bank keys',list(A['banks'])[:8]);print('reference',str(W/'helicopter-reference.png'))
