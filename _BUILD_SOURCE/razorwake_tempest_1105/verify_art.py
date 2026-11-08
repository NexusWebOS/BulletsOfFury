from pathlib import Path
import json,subprocess
import numpy as np
from PIL import Image
W=Path(__file__).resolve().parent;A=W/'authored';O=W/'art-checks';O.mkdir(exist_ok=True);M=json.loads((A/'manifest.json').read_text());checks=[];pages={};count=0;bits=(A/'opaque_masks.bin').read_bytes();maskcount=0;maskok=True
for name,B in M['banks'].items():
 subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch',str(A/(name+'.aseprite')),'--sheet',str(O/(name+'.png')),'--sheet-columns','8','--data',str(O/(name+'.json')),'--format','json-array'],check=True)
 meta=json.loads((O/(name+'.json')).read_text());im=Image.open(O/(name+'.png')).convert('RGBA');source=Image.open(A/'strips'/(name+'.png')).convert('RGBA');ok=len(meta['frames'])==B['frames'];runtime=True;edge=[]
 for i,f in enumerate(meta['frames']):
  r=f['frame'];out=np.array(im.crop((r['x'],r['y'],r['x']+r['w'],r['y']+r['h'])));ref=np.array(source.crop((i%8*B['w'],i//8*B['h'],i%8*B['w']+B['w'],i//8*B['h']+B['h'])))
  equal=lambda a,b:np.array_equal(a[:,:,3],b[:,:,3])and np.array_equal(a[:,:,:3][b[:,:,3]>0],b[:,:,:3][b[:,:,3]>0])
  ok=ok and equal(out,ref);c=B['cells'][i]
  if c[0]not in pages:pages[c[0]]=Image.open(A/Path(M['pages'][c[0]]['path']).name).convert('RGBA')
  packed=Image.new('RGBA',(B['w'],B['h']));packed.alpha_composite(pages[c[0]].crop((c[1],c[2],c[1]+c[3],c[2]+c[4])),(c[5],c[6]));runtime=runtime and equal(np.array(packed),ref)
  if name!='storm_grade'and max(ref[0,:,3].max(),ref[-1,:,3].max(),ref[:,0,3].max(),ref[:,-1,3].max())>64:edge.append(i)
  if name in M['masks']:
   x,y,w,h,off=M['masks'][name][i];a=np.unpackbits(np.frombuffer(bits[off:off+(w*h+7)//8],dtype='uint8'),bitorder='little')[:w*h].reshape(h,w);maskok=maskok and np.array_equal(a,ref[y:y+h,x:x+w,3]>80);maskcount+=1
  count+=1
 checks.append(dict(bank=name,frames=B['frames'],roundtrip=bool(ok),runtime=bool(runtime),even=B['w']%2==B['h']%2==0,unclipped=not edge,edgeFrames=edge));print('PASS'if ok and runtime and not edge else'FAIL',name,flush=True)
result=dict(checks=checks,frames=count,masks=maskcount,maskExact=bool(maskok),passed=maskok and all(c['roundtrip']and c['runtime']and c['even']and c['unclipped']for c in checks));(O/'report.json').write_text(json.dumps(result,indent=2));print('ART_RESULT',result['passed'],count,'frames',maskcount,'masks');raise SystemExit(0 if result['passed']else 1)
