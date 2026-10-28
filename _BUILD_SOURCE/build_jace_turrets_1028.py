"""Measured existing Jace wing-gun mouths; no sprite/cell/scale changes."""
from pathlib import Path
import json,math,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];O=R/'_shots/jace_turrets_1028';O.mkdir(parents=True,exist_ok=True)
P=R/'assets/game/levels/stage_06/boss/air_refit_1021/jace';M=json.loads((P/'manifest.json').read_text());out={}
for kind in ['idle','attack']:
 b=M['banks'][kind];out[b['key']]=dict(cell=128,pivot=[64,64],points=[[[22,72],[102,72]]for _ in range(b['frames'])],source=b['path'])
# Individually measured mouths in each actual banked plate, not a rotation of
# the south offsets: the oblique authored poses change the visible pod geometry.
points=[[[59,106],[133,106]],[[51,91],[115,128]],[[94,61],[94,135]],[[110,56],[58,100]],[[133,86],[59,86]],[[134,104],[88,56]],[[98,132],[101,62]],[[78,133],[134,84]]]
out['air13_s6_jace_heading']=dict(cell=192,pivot=[96,96],points=points,source='assets/game/levels/stage_06/boss/air_motion_1013/jace/headings.webp')
for key,a in out.items():
 src=Image.open(R/a['source']).convert('RGBA');cell=a['cell'];contact=Image.new('RGBA',(cell*4,cell*((len(a['points'])+3)//4)))
 for f,pair in enumerate(a['points']):
  im=src.crop((f*cell,0,(f+1)*cell,cell));g=ImageDraw.Draw(im)
  for x,y in pair:g.ellipse((x-2,y-2,x+2,y+2),outline='#24ffdd',width=1)
  contact.paste(im,(f%4*cell,f//4*cell))
 contact.resize((contact.width*2,contact.height*2),Image.Resampling.NEAREST).save(O/(key+'.png'))
 a['sha256']=hashlib.sha256((R/a['source']).read_bytes()).hexdigest()
(R/'assets/jace_turret_sockets_1028.js').write_text('"use strict";\nconst JR36_TURRETS='+json.dumps(out,separators=(',',':'))+';\n',encoding='utf8')
(O/'manifest.json').write_text(json.dumps(dict(builder='_BUILD_SOURCE/build_jace_turrets_1028.py',sockets=out),indent=2))
print('Jace: source-aligned wing turret mouths for idle, attack and all eight headings')
