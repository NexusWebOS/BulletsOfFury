from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
W=Path(__file__).resolve().parent;D=W.parent/'outputs/BOF-Cutscenes-1103';V=D/'verification/revision7';O=D/'overlay';A=O/'assets/game/shared/cinematics/story_1103'
M=json.loads((A/'manifest.json').read_text());C=M['comicScroll'];checks=[]
def ck(name,ok,data=None):checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS 'if ok else 'FAIL ')+name)
border=np.array(Image.open(A/'comic-border.webp').convert('RGBA'));blocks=border.reshape(128,4,228,4,4)
ck('Divider has exact hard 4px console pixels',np.all(blocks==blocks[:,0:1,:,0:1,:]))
ck('Divider uses only five flat gray shades and binary alpha',len(np.unique(border[border[:,:,3]>0,:3],axis=0))<=5 and set(np.unique(border[:,:,3]))=={0,255})
ck('Full-width pixel footer covers all lower chest edges',np.all(border[396:404,:,3]==255))
ck('All nine requested background colors are assigned',set(C['colors'].values())=={'yellow','blue','red','black','white','purple','orange','brown','gold'},C['colors'])
for pilot in C['colors']:
 bank=M['banks']['comic-scroll-'+pilot];im=np.array(Image.open(O/bank['path']).convert('RGBA'));frames=[]
 for f in range(16):
  x=f%bank['cols']*bank['w'];y=f//bank['cols']*bank['h'];frames.append(im[y:y+bank['h'],x:x+bank['w']])
 ck(pilot+' field frames are opaque flat-color pixels',all(np.all(a[:,:,3]==255) and len(np.unique(a[:,:,:3].reshape(-1,3),axis=0))<=4 for a in frames))
 ck(pilot+' loop contains 16 distinct scrolling phases',len({hashlib.sha256(a.tobytes()).hexdigest()for a in frames})==16)
 pairs=[]
 for f in range(16):
  following=frames[(f+1)%16];prior=frames[f]
  pairs.append(np.array_equal(following[:,16:384],prior[:,:368])and np.array_equal(following[:,576:896],prior[:,592:912]))
 ck(pilot+' left and right fields scroll oppositely and close the loop exactly',all(pairs))
report={'passed':sum(c['passed']for c in checks),'total':len(checks),'checks':checks};(V/'scroll-art-checks.json').write_text(json.dumps(report,indent=2));raise SystemExit(not all(c['passed']for c in checks))
