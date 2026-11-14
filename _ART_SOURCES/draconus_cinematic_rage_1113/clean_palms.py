from pathlib import Path
from PIL import Image
import json,numpy as np
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');E=W/'exports';M=json.loads((W/'manifest.json').read_text())
text=(R/'assets/rage_palm_art_1110.js').read_text();old=json.JSONDecoder().raw_decode(text[text.index('const RF1110_ART=')+len('const RF1110_ART='):].lstrip())[0];audit=[]
for depth in ['fore','back']:
 spec=old['banks']['drac_palms_'+depth];im=np.array(Image.open(R/f'assets/game/shared/combat/rage_palm_1110/drac_palms_{depth}_power.webp').convert('RGBA'));r,g,b=[im[:,:,i].astype(float)for i in range(3)]
 matte=(r>80)&(b>80)&(r>b*.7)&(b>r*.7)&(g<np.maximum(r,b)*.18)&(im[:,:,3]>0)
 # Remove the identified pink generation matte; preserve all non-matte pixels,
 # including blue-dominant purple palm energy and the original native gestures.
 im[matte]=0;im[im[:,:,3]<128]=0;im[im[:,:,3]>=128,3]=255
 cw,ch=spec['cw'],spec['ch'];rows=[]
 for i in range(spec['count']):
  a=im[i//4*ch:i//4*ch+ch,i%4*cw:i%4*cw+cw];mask=a[:,:,3]>0;ys,xs=np.where(mask)
  rows.append(dict(**{k:v for k,v in spec['meta'][i].items()if k not in['spans','bounds']},bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],spans=[np.flatnonzero(np.diff(np.r_[False,row,False])).tolist()for row in mask]))
 for mat in ['power','hit']:
  name='palms_'+depth+'_'+mat;a=im.copy()
  if mat=='hit':a[a[:,:,3]>0,:3]=255
  sheet=Image.fromarray(a);sheet.save(E/(name+'.webp'),lossless=True,method=1);d=E/name;d.mkdir(exist_ok=True)
  for i in range(spec['count']):sheet.crop((i%4*cw,i//4*ch,i%4*cw+cw,i//4*ch+ch)).save(d/f'{i:02}.png')
  M[name]=dict(cw=cw,ch=ch,count=spec['count'],cols=4,pivot=spec['pivot'],meta=rows)
 audit.append(dict(depth=depth,removedPinkMatte=int(matte.sum()),preservedNonMatteRGB=True))
(W/'palm-matte-audit.json').write_text(json.dumps(audit,indent=2));(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')));(W/'draconus_cinematic_rage_art_1113.js').write_text("'use strict';\nconst DCR13_ART="+json.dumps(M,separators=(',',':'))+';\n')
print('Removed identified magenta matte from retained native palm gestures without changing their non-matte RGB pixels.')
