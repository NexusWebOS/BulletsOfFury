from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
W=Path(__file__).resolve().parent;D=W.parent/'outputs/BOF-Cutscenes-1103';A=D/'overlay/assets/game/shared/cinematics/story_1103';V=D/'verification/revision8';M=json.loads((A/'manifest.json').read_text());C=M['comicScroll'];checks=[]
def ck(name,ok,data=None):checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS 'if ok else 'FAIL ')+name)
before=json.loads((V/'before-assets.json').read_text());changed={p.stem for p in A.glob('*.webp')if p.name in before and hashlib.sha256(p.read_bytes()).hexdigest()!=before[p.name]};expected={prefix+p for prefix in ['comic-scroll-','comic-']for p in C['colors']}
ck('Only backgrounds and stored comic compositions change',changed==expected,sorted(changed));ck('All corrected pilot frames and divider keep identical bytes',all(not n.startswith(('headset-','headset-panel-'))and n!='comic-border'for n in changed))
ck('Nine intro color themes use sixteen shaded tones',len(C['palettes'])==9 and all(len(p)==16 for p in C['palettes'].values()))
ck('Runtime loop is twenty-four authored frames at twelve fps',C['phases']==24 and C['fps']==12)
def indices(rgb,palette):
 out=np.full(rgb.shape[:2],-1,dtype=int)
 for i,color in enumerate(palette):out[np.all(rgb==color,axis=2)]=i
 assert np.all(out>=0),'A color outside the shared palette appeared'
 return out
for pilot,theme in C['colors'].items():
 b=M['banks']['comic-scroll-'+pilot];im=np.array(Image.open(D/'overlay'/b['path']).convert('RGBA'));frames=[];native=[]
 for f in range(24):
  x=f%b['cols']*b['w'];y=f//b['cols']*b['h'];a=im[y:y+b['h'],x:x+b['w']];frames.append(a);native.append(a[::4,::4,:3])
 ck(pilot+' color frames remain crisp opaque four-pixel art',all(np.all(a[:,:,3]==255) and np.all(a.reshape(98,4,228,4,4)==a.reshape(98,4,228,4,4)[:,0:1,:,0:1,:])for a in frames))
 ck(pilot+' color and shaded illumination change throughout the loop',len({hashlib.sha256(a.tobytes()).hexdigest()for a in frames})==24)
 contact='cole'if pilot=='decker'else'decker';lp=C['palettes'][C['colors'][contact]];rp=C['palettes'][theme]
 left=[indices(a[:,:96],lp)for a in native];right=[indices(a[:,144:],rp)for a in native];pairs=[]
 for f in range(24):
  k=(f+1)%24;la=left[f][:,:-8];lb=left[k][:,8:];ra=right[f][:,8:];rb=right[k][:,:-8];lm=(la>0)&(la<15)&(lb>0)&(lb<15);rm=(ra>0)&(ra<15)&(rb>0)&(rb<15)
  ld=C['pulse'][k]-C['pulse'][f];rd=C['pulse'][(k+6)%24]-C['pulse'][(f+6)%24]
  pairs.append(np.count_nonzero(lm)>1000 and np.count_nonzero(rm)>1000 and np.all((lb-la)[lm]==ld)and np.all((rb-ra)[rm]==rd))
 ck(pilot+' sweeps move oppositely with coherent shade cycling and exact loop closure',all(pairs))
report={'passed':sum(c['passed']for c in checks),'total':len(checks),'checks':checks};(V/'neogeo-art-checks.json').write_text(json.dumps(report,indent=2));raise SystemExit(not all(c['passed']for c in checks))
