"""RD76: fixed-size authored main-body and code-wire cells, from existing art."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
O=R/'assets/game/levels/stage_08/boss/return_download_1030';O.mkdir(parents=True,exist_ok=True)
def data(file):
 s=(R/'assets'/file).read_text(encoding='utf-8-sig');return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
model=data('stage8_pixellab_art_1018.js')['models']['colossus'];art={'banks':{},'size':410,'pivot':[205,205],'source':'Existing approved V18 colossus layers; offline fixed-size body/code-wire frames. No paid generation.'};sources=[]
for part in ['left','core','right']:
 sheets={k:Image.new('RGBA',(1640,1640)) for k in ['body','wire']}
 for i,f in enumerate(model['frames']):
  p=R/f[part]['path'];im=Image.open(p).convert('RGBA').resize((410,410),Image.Resampling.NEAREST);a=np.array(im);y,x=np.indices(a.shape[:2]);l=a[:,:,:3].max(2);m=(a[:,:,3]>0)&(((x+i*2)%11<2)|((y+i)%9<2)|((l>205)&((x+y)%3==0)))
  w=np.zeros_like(a);w[m]=[202,100,255,255];hot=m&((x+y+i*9)%37<7);w[hot]=[255,218,255,255]
  sheets['body'].paste(im,((i%4)*410,(i//4)*410));sheets['wire'].paste(Image.fromarray(w),((i%4)*410,(i//4)*410))
  sources.append({'path':str(p.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 for kind,sheet in sheets.items():
  key='rd76_'+part+'_'+kind;p=O/(key+'.webp');sheet.save(p,lossless=True,method=6);art['banks'][part+'_'+kind]={'key':key,'path':str(p.relative_to(R)).replace('\\','/'),'w':410,'h':410,'cols':4,'count':16,'pivot':[205,205]}
(R/'assets/dracodia_return_art_1030.js').write_text('"use strict";\nconst RD76_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
audit={'sources':sources,'banks':len(art['banks']),'frames':96,'evenCells':True,'size':[410,410],'bodySourcePixels':'native nearest-neighbor410/320; stable205 pivot'}
(O/'provenance.json').write_text(json.dumps(audit,indent=2));print('Built96 authored return cells in6 fixed-size sheets')
