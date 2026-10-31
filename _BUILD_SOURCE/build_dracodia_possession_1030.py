from pathlib import Path
import json,shutil,subprocess,hashlib
from PIL import Image
import argparse
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/dracodia_possession_1030';O=R/'assets/game/levels/stage_08/boss/possession_1030';O.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);args=p.parse_args()
subprocess.run([args.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((D/'manifest.json').read_text())
for n,a in m.items():
 shutil.copy2(D/(n+'.png'),O/(n+'.png'));a['sha256']=hashlib.sha256((O/(n+'.png')).read_bytes()).hexdigest()
 if n.startswith('host_')and not n.endswith('_hit'):
  im=Image.open(O/(n+'.png')).convert('RGBA');spans=[];points=[]
  for f in range(a['frames']):
   cell=im.crop((f%a['cols']*360,f//a['cols']*360,(f%a['cols']+1)*360,(f//a['cols']+1)*360));alpha=cell.getchannel('A');rows=[];pts=[]
   for y in range(360):
    runs=[];start=None
    for x in range(361):
     on=x<360 and alpha.getpixel((x,y))>64
     if on and start is None:start=x
     if not on and start is not None:runs.extend([start,x]);start=None
    rows.append(runs)
   # Alpha-bearing shoulder, elbow and claw anchors for whole-limb explosions.
   box=alpha.getbbox()
   for frac in [.10,.28,.47,.66,.84]:
    yy=round(box[1]+(box[3]-box[1])*frac);row=rows[yy]
    if row:pts.append([round((row[0]+row[-1])/2)-180,yy-180])
   spans.append(rows);points.append(pts)
  a['spans']=spans;a['blasts']=points
(O/'manifest.json').write_text(json.dumps(m,separators=(',',':')));(D/'manifest.json').write_text(json.dumps(m,separators=(',',':')))
(R/'assets/dracodia_possession_art_1030.js').write_text("'use strict';\nconst RD71_ART="+json.dumps(m,separators=(',',':'))+';\n')
print('Exported',len(m),'authored portal/drone/code/whole-shoulder banks')
