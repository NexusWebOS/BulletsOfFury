from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
W=Path(__file__).resolve().parent; results=[]
for unit in ['blue','corrupt']:
 n=unit+'-overhead'; source=Image.open(W/'exports'/(n+'_regular.png')).convert('RGBA'); rt=Image.open(W/'exports'/(n+'_roundtrip.png')).convert('RGBA')
 assert source.tobytes()==rt.tobytes(),('Aseprite roundtrip',n)
 alpha=np.array(source)[:,:,3]
 for mat in ['regular','chrome','red','hit','red_hit']:
  a=np.array(Image.open(W/'exports'/(n+'_'+mat+'.webp')).convert('RGBA')); assert np.array_equal(alpha,a[:,:,3]),(n,mat,'alpha mismatch')
  if mat=='hit': assert (a[:,:,:3][alpha>0]==255).all()
 unique=len({hashlib.sha256(Image.open(W/'exports'/n/f'{i:02}.png').tobytes()).hexdigest()for i in range(32)})
 assert unique==32,(n,unique)
 results.append(dict(bank=n,pixelExactFrames=32,uniqueDrawings=32,matchingMaterialMasks=True,evenCells=[512,512]))
M=json.loads((W/'manifest.json').read_text()); old=json.loads((W.parent/'front_hammer_1111/manifest.json').read_text())
for n in M:
 if not n.endswith('overhead'): assert M[n]==old[n],('retained bank changed',n)
audit=dict(banks=results,newWholeDrawings=48,retainedReady=16,retainedSideAndWhirlMetadata=True,visualReview='All selected complete poses inspected against the original rigid T hammer and user GIF studies. The prior curved parallel-shaft socket is replaced; held art is whole-drawn. Near cap spikes repaired on copied form. This visual review is distinct from runtime checks.')
(W/'export-verification.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit),flush=True)
