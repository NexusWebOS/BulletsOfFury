from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];W=R/'_shots/nyx_firing_1029';W.mkdir(parents=True,exist_ok=True)
def load(name):
 s=(R/'assets'/name).read_text();return json.JSONDecoder().raw_decode(s[s.index('=')+1:].strip())[0]
M=load('air_refit_art_1021.js')['models']['nyx'];H=load('air_motion_art_1013.js')['nyx'];out={}
heading=[[[76,119],[115,119]],[[64,100],[92,128]],[[71,76],[71,116]],[[92,64],[64,92]],[[116,71],[76,71]],[[128,92],[100,64]],[[121,116],[121,76]],[[100,128],[128,100]]]
def snap(im,p):
 x,y=p
 if im.getpixel((x,y))[3]>220:return p
 candidates=[(xx,yy)for yy in range(max(0,y-9),min(im.height,y+10))for xx in range(max(0,x-9),min(im.width,x+10))if im.getpixel((xx,yy))[3]>220]
 assert candidates,p
 return list(min(candidates,key=lambda q:(q[0]-x)**2+(q[1]-y)**2))
for kind in ['idle','attack','heading']:
 B=H['heading']if kind=='heading'else M['banks'][kind];im=Image.open(R/B['path']).convert('RGBA');points=[];cells=[]
 for f in range(B['frames']):
  c=[f*192,0,192,192]if kind=='heading'else B['cells'][f];cell=im.crop((c[0],c[1],c[0]+c[2],c[1]+c[3]));p=heading[f]if kind=='heading'else[[47,81],[79,81]];points.append([snap(cell,xy)for xy in p]);cells.append(c)
 out[B['key']]=dict(pivot=[96,96]if kind=='heading'else[64,64],points=points,source=B['path'],sha256=hashlib.sha256((R/B['path']).read_bytes()).hexdigest(),cells=cells)
(R/'docs/qa/nyx_firing_sockets_1029.json').write_text(json.dumps(out,indent=2));(R/'assets/nyx_firing_sockets_1029.js').write_text("'use strict';\nconst NY47_SOCKETS="+json.dumps(out,separators=(',',':'))+';\n')
print({k:v['points']for k,v in out.items()})
