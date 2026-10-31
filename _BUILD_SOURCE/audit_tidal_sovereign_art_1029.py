from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib
R=Path(__file__).resolve().parents[1];W=R/'_shots/tidal_sovereign_1029/art';W.mkdir(parents=True,exist_ok=True);D=R/'assets/game/levels/stage_09/boss/tidal_sovereign_1029';m=json.loads((D/'manifest.json').read_text());cfg=json.loads((D/'inputs.json').read_text());checks=[];memory=0
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,str(d)[:200]if not v else'')
for n,a in m.items():
 im=Image.open(R/a['path']).convert('RGBA');memory+=im.width*im.height*4;bad=[];unique=set()
 for i in range(a['frames']):
  c=im.crop((i%a['cols']*a['cw'],i//a['cols']*a['ch'],(i%a['cols']+1)*a['cw'],(i//a['cols']+1)*a['ch']));b=c.getchannel('A').getbbox();unique.add(hashlib.sha256(c.tobytes()).hexdigest())
  if not b or b[0]<=0 or b[1]<=0 or b[2]>=a['cw']or b[3]>=a['ch']:bad.append((i,b))
 ck(n+' fixed even cells have clear padding',not bad and a['cw']%2==a['ch']%2==0,bad[:3])
 if a['frames']>1:ck(n+' actually animates',len(unique)>1,len(unique))
 if n.startswith('body_')and n!='body_hit':
  row=cfg['ns9_tidal_'+n[5:]];r=row['cell'];src=Image.open(R/row['path']).convert('RGBA').crop((r[1],r[2],r[1]+r[3],r[2]+r[4]));a0=src.getchannel('A');ok=True
  for i in range(a['frames']):
   c=im.crop((i%a['cols']*a['cw'],i//a['cols']*a['ch'],(i%a['cols']+1)*a['cw'],(i//a['cols']+1)*a['ch']));ok &= ImageChops.difference(a0,c.getchannel('A')).getbbox()is None
  ck(n+' preserves original whole-hull alpha',ok)
out=dict(checks=checks,decodedMiB=memory/1048576);(W/'art-audit.json').write_text(json.dumps(out,indent=2));print('Decoded MiB',memory/1048576);assert all(q['passed']for q in checks)
