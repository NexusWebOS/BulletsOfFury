"""Rebuild the five true barrel-roll reels and shared-baseline dialogue banks."""
from pathlib import Path
import json,subprocess,shutil,hashlib,argparse
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/riders_roll_type_1030';O=R/'assets/game/levels/stage_06/boss/rough_riders_1028';F=R/'assets/game/shared/ui/riders_dialogue_1030'
p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);a=p.parse_args()
subprocess.run([a.aseprite,'--batch','--script-param','work='+D.as_posix(),'--script-param','root='+R.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((O/'manifest.json').read_text())
for k in ['voss','nyx','rook','kaia','jace']:
 name='flight_'+k;shutil.copy2(D/(name+'.png'),O/(name+'.png'));im=Image.open(O/(name+'.png')).convert('RGBA');bounds=[]
 for i in range(88):
  box=im.crop((i%16*192,i//16*192,i%16*192+192,i//16*192+192)).getbbox();assert box and min(box)>0 and box[2]<192 and box[3]<192,(k,i,box);bounds.append(box)
 m['models'][k]['bounds']=bounds;m['banks'][name].update(frames=88,h=1152,roll=[72,16],sha256=hashlib.sha256((O/(name+'.png')).read_bytes()).hexdigest())
(O/'manifest.json').write_text(json.dumps(m,indent=2));(R/'assets/rough_riders_art_1028.js').write_text('"use strict";\nconst RR33_ART='+json.dumps(m,separators=(',',':'))+';\n',encoding='utf8')
meta=json.loads((D/'dialogue-manifest.json').read_text());F.mkdir(exist_ok=True)
for n,a in meta['banks'].items():shutil.copy2(D/(n+'.png'),F/(n+'.png'));a['sha256']=hashlib.sha256((F/(n+'.png')).read_bytes()).hexdigest()
(F/'manifest.json').write_text(json.dumps(meta,indent=2));(R/'assets/riders_dialogue_art_1030.js').write_text('"use strict";\nconst RD64_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf8')
print('Rebuilt all80 padded barrel-roll frames and six aligned dialogue banks')
