from pathlib import Path
import json,shutil,subprocess,hashlib
from PIL import Image
import argparse
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/dracodia_demon_1030';O=R/'assets/game/levels/stage_08/boss/claw_laser_1030';O.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);args=p.parse_args()
subprocess.run([args.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((D/'manifest.json').read_text())
for n,a in m.items():
 shutil.copy2(D/(n+'.png'),O/(n+'.png'));a['sha256']=hashlib.sha256((O/(n+'.png')).read_bytes()).hexdigest()
 if n in ['claw','root_left','root_right']:
  im=Image.open(O/(n+'.png')).convert('RGBA');frames=[]
  for f in range(a['frames']):
   al=im.crop((f%a['cols']*a['cw'],f//a['cols']*a['ch'],(f%a['cols']+1)*a['cw'],(f//a['cols']+1)*a['ch'])).getchannel('A');rows=[]
   for y in range(a['ch']):
    row=[];start=None
    for x in range(a['cw']+1):
     on=x<a['cw']and al.getpixel((x,y))>64
     if on and start is None:start=x
     if not on and start is not None:row.extend([start,x]);start=None
    rows.append(row)
   frames.append(rows)
  a['spans']=frames
(O/'manifest.json').write_text(json.dumps(m,separators=(',',':')));(D/'manifest.json').write_text(json.dumps(m,separators=(',',':')))
(R/'assets/dracodia_demon_art_1030.js').write_text("'use strict';\nconst RD72_ART="+json.dumps(m,separators=(',',':'))+';\n');print('Authored',len(m),'directional claw/tendon/optic/rocket/warning banks')
