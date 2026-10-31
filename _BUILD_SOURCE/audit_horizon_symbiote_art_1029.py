from pathlib import Path
from PIL import Image
import json
R=Path(__file__).resolve().parents[1];W=R/'_shots/horizon_symbiote_1029/art';W.mkdir(parents=True,exist_ok=True);D=R/'assets/game/levels/stage_09/miniboss/horizon_symbiote_1029';m=json.loads((D/'manifest.json').read_text());checks=[];memory=0
for n,a in m.items():
 im=Image.open(R/a['path']).convert('RGBA');memory+=im.width*im.height*4;bad=[]
 for i in range(a['frames']):
  c=im.crop((i%a['cols']*a['cw'],i//a['cols']*a['ch'],(i%a['cols']+1)*a['cw'],(i//a['cols']+1)*a['ch']));b=c.getchannel('A').getbbox()
  if not b or b[0]<=0 or b[1]<=0 or b[2]>=a['cw']or b[3]>=a['ch']:bad.append((i,b))
 good=not bad and a['cw']%2==a['ch']%2==0;checks.append(dict(name=n,passed=good,frames=a['frames'],bad=bad[:4]));print(n,'PASS'if good else'FAIL',bad[:2]if bad else'')
out=dict(checks=checks,decodedMiB=memory/1048576);(W/'art-audit.json').write_text(json.dumps(out,indent=2));print('Decoded MiB',memory/1048576);assert all(q['passed']for q in checks)
