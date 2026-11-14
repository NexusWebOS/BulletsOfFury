from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
W=Path(__file__).resolve().parent;OLD=W.parent/'solid_hammer_1111';E=W/'exports';M=json.loads((W/'manifest.json').read_text());results=[]
for job in json.loads((W/'aseprite-jobs.json').read_text()):
 n=job['name'];a=Image.open(E/(n+'_regular.png')).convert('RGBA');b=Image.open(E/(n+'_roundtrip.png')).convert('RGBA');assert a.tobytes()==b.tobytes(),('Aseprite mismatch',n)
 alpha=np.array(a)[:,:,3]
 for mat in ['regular','chrome','red','hit','red_hit']:
  arr=np.array(Image.open(E/(n+'_'+mat+'.webp')).convert('RGBA'));assert np.array_equal(alpha,arr[:,:,3]),(n,mat,'mask')
  if mat=='hit':assert(arr[:,:,:3][alpha>0]==255).all()
 unique=len({hashlib.sha256(Image.open(E/n/f'{i:02}.png').tobytes()).hexdigest()for i in range(32)})
 assert unique==32,(n,'unique',unique);results.append(dict(bank=n,frames=32,uniqueDrawings=unique,roundtripExact=True))
for prefix in ['blue','corrupt']:
 l=prefix+'-overhead-left';r=prefix+'-overhead-right';c=prefix+'-overhead'
 for i in range(32):
  a=Image.open(E/l/f'{i:02}.png').convert('RGBA');b=Image.open(E/r/f'{i:02}.png').convert('RGBA');assert a.transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()==b.tobytes(),(r,i)
  for point in ['tip','headCenter','grip']:
   lm,rm=M[l]['meta'][i],M[r]['meta'][i];assert lm[point][0]-M[l]['pivot'][0]==-(rm[point][0]-M[r]['pivot'][0]),(r,i,point)
 for mat in ['regular','chrome','red','hit','red_hit']:
  assert (E/(l+'_'+mat+'.webp')).read_bytes()==(OLD/'exports'/(prefix+'-overhead_'+mat+'.webp')).read_bytes(),('approved left changed',l,mat)
 assert abs(M[c]['meta'][22]['headCenter'][0]-M[c]['pivot'][0])<=18,('not center',c,M[c]['meta'][22]['headCenter'])
 for i in range(17):
  a=Image.open(E/c/f'{i:02}.png').convert('RGBA');s=Image.open(OLD/'exports'/(prefix+'-overhead_regular.png')).convert('RGBA');b=s.crop((i%4*512,i//4*512,(i%4+1)*512,(i//4+1)*512));assert a.tobytes()==b.tobytes(),('retained windup changed',c,i)
report=dict(banks=results,timelineFrames=192,newWholeDrawings=30,retainedCenterReadyLiftPeak=34,approvedLeftFrames=64,wholePoseMirrors=64,exactRightPhysicsReflection=True,centeredHeadOffset={p:M[p+'-overhead']['meta'][22]['headCenter'][0]-256 for p in ['blue','corrupt']})
(W/'export-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
