from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib
W=Path(__file__).parent;M=json.loads((W/'asset-metadata.json').read_text());C=[]
def check(ok,n):C.append({'ok':bool(ok),'name':n})
for id,B in M['banks'].items():
 p=W/'exports'/Path(B['path']).name;im=Image.open(p).convert('RGBA');check(im.size==(B['cw']*B['cols'],B['ch']*((B['frames']+B['cols']-1)//B['cols'])),id+' sheet extent');check(B['cw']%2==B['ch']%2==0,id+' even fixed cells');check((W/'sources'/(id+'.aseprite')).exists(),id+' editable source')
 if id.startswith(('spread_','plasma_')) and id.split('_')[-1]in ['1','2','3','4','5']:
  masks=[];pixels=[]
  for n in range(B['frames']):
   x=n%B['cols']*B['cw'];y=n//B['cols']*B['ch'];cell=im.crop((x,y,x+B['cw'],y+B['ch']));masks.append(cell.getchannel('A').tobytes());pixels.append(cell.tobytes())
  for d in range(B.get('dirs',1)):
   check(len(set(masks[d::B.get('dirs',1)]))==1,id+' static silhouette direction'+str(d));check(len(set(pixels[d::B.get('dirs',1)]))>=3,id+' authored1015 brightness variance direction'+str(d))
 if id.startswith('column_'):
  n=B['frames']-1;x=n%B['cols']*B['cw'];y=n//B['cols']*B['ch'];check(im.crop((x,y,x+B['cw'],y+B['ch'])).getbbox()is None,id+' authored transparent dissolve tail')
for q in M['provenance']:
 check(all(hashlib.sha256(Path(f['path']).read_bytes()).hexdigest()==f['sha256'] for f in q['frames']),q['id']+' original pack unchanged')
(W/'asset-qa.json').write_text(json.dumps({'checks':C,'banks':len(M['banks']),'bytes':sum((W/'exports'/Path(B['path']).name).stat().st_size for B in M['banks'].values())},indent=2),encoding='utf8');print(len(C),'asset checks, failures',[q for q in C if not q['ok']])
