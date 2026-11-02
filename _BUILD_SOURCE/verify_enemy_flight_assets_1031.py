"""Read-only source/registration checks and byte-identical motion-bank rebuilds."""
from pathlib import Path
from io import BytesIO
import json,hashlib,sys
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];O=R/'assets/game/shared/combat/enemy_flight_1031';checks=[]
def ck(name,ok):
 checks.append(dict(name=name,passed=bool(ok)));print('PASS'if ok else'FAIL',name,flush=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for path in[O/'manifest.json',O/'static/manifest.json',O/'ordnance/manifest.json',O/'feedback/manifest.json']:
 meta=json.loads(path.read_text());banks=meta.get('models',{})|meta.get('modules',{})|meta.get('banks',{})|meta.get('glyphs',{})
 for name,B in banks.items():
  p=R/B['path'];im=Image.open(p);ck('registered '+B['key'],digest(p)==B['sha256']and B['cell']%2==0 and im.width==B['dirs']*B['cell']and im.height==B['frames']*B['cell'])
if'--registrations-only'in sys.argv:
 (R/'_shots/enemy_flight_1031/asset-registration-checks.json').write_text(json.dumps(checks,indent=2));assert all(q['passed']for q in checks);print('ALL',len(checks),'final registrations passed');sys.exit(0)
meta=json.loads((O/'manifest.json').read_text())
for name,M in meta['models'].items():
 c=M['cell'];out=Image.new('RGBA',(c*M['dirs'],c*M['frames']));pad=(c-128)//2
 for kind,B in M['banks'].items():
  source=M['sources'][kind];ck(name+' '+kind+' source',digest(R/source['path'])==source['sha256']);im=Image.open(R/source['path']).convert('RGBA')
  for f,(x,y,w,h)in enumerate(source['cells']):
   t=Image.new('RGBA',(c,c));t.alpha_composite(im.crop((x,y,x+w,y+h)),(pad,pad))
   for d in range(M['dirs']):out.alpha_composite(t.rotate(-d*360/M['dirs'],Image.Resampling.NEAREST,center=(c/2,c/2)),(d*c,(B['row']+f)*c))
 if M.get('paletteRatios'):
  # Palette builder reads the canonical lossless base first.
  bio=BytesIO();out.save(bio,format='WEBP',lossless=True,method=4);out=Image.open(BytesIO(bio.getvalue())).convert('RGBA');a=np.array(out);rgb=a[:,:,:3].astype(float);l=rgb@[.2126,.7152,.0722];mask=(a[:,:,3]>0)&(l>23)&(l<224)&((rgb.max(2)-rgb.min(2))<58);mapped=np.stack([np.interp(l,M['paletteKnots'],[q[ch]for q in M['paletteRatios']])*l for ch in range(3)],axis=2);a[:,:,:3][mask]=np.clip(mapped[mask],0,255).astype('uint8');out=Image.fromarray(a)
 bio=BytesIO();out.save(bio,format='WEBP',lossless=True,method=4);ck(name+' byte-identical rebuild',hashlib.sha256(bio.getvalue()).hexdigest()==M['sha256'])
p=R/'_shots/enemy_flight_1031/asset-checks.json';p.write_text(json.dumps(checks,indent=2));assert all(q['passed']for q in checks),'Asset validation failed';print('ALL',len(checks),'asset/source/rebuild checks passed')
