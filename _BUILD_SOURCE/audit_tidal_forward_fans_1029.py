from pathlib import Path
from PIL import Image
import json,hashlib,math
R=Path(__file__).resolve().parents[1];W=R/'_shots/tidal_forward_fans_1029/art';W.mkdir(parents=True,exist_ok=True);D=R/'assets/game/levels/stage_09/boss/tidal_sovereign_1029';m=json.loads((D/'manifest.json').read_text());checks=[];memory=0;images={}
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,str(d)[:200]if not v else'')
def cell(n,i):
 a=m[n];im=images[n];return im.crop((i%a['cols']*a['cw'],i//a['cols']*a['ch'],(i%a['cols']+1)*a['cw'],(i//a['cols']+1)*a['ch']))
for n,a in m.items():
 im=images[n]=Image.open(R/a['path']).convert('RGBA');memory+=im.width*im.height*4;ok=True;unique=set()
 for i in range(a['frames']):
  c=cell(n,i);bb=c.getchannel('A').getbbox();unique.add(hashlib.sha256(c.tobytes()).hexdigest());ok &= bool(bb)and bb[0]>0 and bb[1]>0 and bb[2]<a['cw']and bb[3]<a['ch']
 ck(n+' has fixed even cells and clear padding',ok and a['cw']%2==a['ch']%2==0)
 if n in ['forward_slug','forward_muzzle','fan_muzzle','jet','rain','grenade_charge','grenade_burst']:ck(n+' contains actual animated source phases',len(unique)>1,len(unique))
ck('Forward bullets have five headings by sixteen authored phases',m['forward_slug']['frames']==80)
ck('Northbound jet base is anchored at the actual fan mouth',m['jet']['pivot']==[40,144]and m['jet']['ch']==176)
ck('Descending rain tip uses the impact anchor',m['rain']['pivot']==[40,144])
ck('Water grenade burst is a sixteen-frame one-shot bank',m['grenade_burst']['frames']==16)
ck('Corrected Stage2 wave bank is retained',m['wave']['frames']==48 and m['wave']['cw']==480)
for state in ['intact','damaged','critical']:
 ck(state+' retains the sixteen-phase actual fan rotation',len({hashlib.sha256(cell('body_'+state,i).crop((82,73,111,102)).tobytes()).hexdigest()for i in range(16)})==16)
(W/'art-audit.json').write_text(json.dumps(dict(checks=checks,decodedMiB=memory/1048576),indent=2));print('Decoded MiB',memory/1048576);assert all(q['passed']for q in checks)
