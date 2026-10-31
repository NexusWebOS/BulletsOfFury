from pathlib import Path
import argparse,subprocess,json,shutil,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/herald_gothic_1030';O=R/'assets/game/levels/stage_08/miniboss/herald_gothic_1030';O.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);a=p.parse_args()
for script in ['author.lua','glass.lua']:
 subprocess.run([a.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script',str(D/script)],check=True)
m=json.loads((D/'manifest.json').read_text())
for name in ['yaw','spiral']:
 b=m[name];im=Image.open(D/(name+'.png')).convert('RGBA');spans=[]
 for f in range(b['frames']):
  alpha=im.crop((f%b['cols']*b['cw'],f//b['cols']*b['ch'],(f%b['cols']+1)*b['cw'],(f//b['cols']+1)*b['ch'])).getchannel('A');rows=[]
  for y in range(b['ch']):
   runs=[];start=None
   for x in range(b['cw']+1):
    on=x<b['cw']and alpha.getpixel((x,y))>80
    if on and start is None:start=x
    if not on and start is not None:runs.extend([start,x]);start=None
   rows.append(runs)
  spans.append(rows)
 b['spans']=spans
for n,b in m.items():
 shutil.copy2(D/(n+'.png'),O/(n+'.png'));b['sha256']=hashlib.sha256((O/(n+'.png')).read_bytes()).hexdigest()
(O/'manifest.json').write_text(json.dumps(m,indent=2));(D/'manifest.json').write_text(json.dumps(m))
(R/'assets/herald_gothic_art_1030.js').write_text("'use strict';\nconst HG70_ART="+json.dumps(m,separators=(',',':'))+";\nfor(const [n,a]of Object.entries(HG70_ART))if(!['yaw','yaw_hit','spiral','spiral_hit','spin_hit','charge_hit'].includes(n))HH52_ART[n]=a;\n")
print('Rebuilt78 fixed-cell Herald banks and exact rotating collision masks')
