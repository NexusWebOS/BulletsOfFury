"""Compile whole palm-volley plates; fixed even cells and measured hand sockets."""
from pathlib import Path
from PIL import Image
import numpy as np
from scipy.ndimage import label
import json,math
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/chronos_volley_1025';O=R/'assets/game/shared/combat/chronos_volley_1025';O.mkdir(parents=True,exist_ok=True)
# Every source uses the same256 canvas, one218 proportional scale and padding.
def norm(im):
 im=im.convert('RGBA');a=np.array(im);mask=a[:,:,3]>=100;lab,_=label(mask);sizes=np.bincount(lab.ravel());mask&=sizes[lab]>=45;a[:,:,3]=np.where(mask,255,0).astype('uint8');im=Image.fromarray(a);out=Image.new('RGBA',(256,256));out.alpha_composite(im.resize((218,218),Image.Resampling.NEAREST),(19,23));return out
src=[D/f'{i:02}.png' for i in range(9)];frames=[norm(Image.open(p))for p in src]
# Source palm centers measured on the whole generated plates, transformed with
# the exact same shared scale/padding. Both sockets are retained every frame.
hands=[[(83,100),(177,100)],[(83,100),(177,100)],[(89,104),(168,104)],[(93,103),(165,103)],[(102,106),(158,106)],[(98,107),(153,107)],[(92,105),(165,105)],[(86,104),(171,104)],[(84,102),(175,102)]]
meta={'sheets':{},'banks':{},'leftFrame':2,'rightFrame':6}
if (D/'key-left.png').exists():
 frames=[];hands=[]
 for name,points in [('left',[(49,77),(185,109)]),('right',[(86,111),(210,82)]),('dual',[(48,80),(206,80)]),('guard',[(80,100),(184,100)])]:
  frames.append(norm(Image.open(D/f'key-{name}.png')));hands.append(points);meta[name+'Frame']=len(frames)-1
if (D/'alternating'/'08.png').exists():
 frames=[norm(Image.open(D/'alternating'/f'{i:02}.png'))for i in range(9)]
 hands=[[(49,77),(185,109)],[(63,80),(180,109)],[(53,84),(179,108)],[(67,83),(179,109)],[(61,84),(187,108)],[(59,85),(191,108)],[(74,105),(203,78)],[(77,106),(218,75)],[(78,106),(211,75)]]
 for name,points in [('dual',[(48,80),(206,80)]),('guard',[(80,100),(184,100)])]:frames.append(norm(Image.open(D/f'key-{name}.png')));hands.append(points)
 meta.update(leftFrame=0,rightFrame=8,dualFrame=9,guardFrame=10,interpolated=True)
for hit in [False,True]:
 name='palms'+('_hit'if hit else '');key='c32_'+name;sheet=Image.new('RGBA',(1024,256*math.ceil(len(frames)/4)));rows=[]
 for i,im in enumerate(frames):
  q=im.copy()
  if hit:q=Image.new('RGBA',im.size,'white');q.putalpha(im.getchannel('A'))
  x=i%4*256;y=i//4*256;sheet.alpha_composite(q,(x,y));row=dict(key=key+'_'+str(i),sheet=key,cell=[x,y,256,256],w=256,h=256,pivot=[128,90],bounds=list(im.getbbox()),_hf22=True,_c26=True,_c32=True,frame=i,palms=[[19+px*218/256,23+py*218/256]for px,py in hands[i]])
  if not hit:row['white']='c32_palms_hit_'+str(i)
  rows.append(row)
 p=O/(key+'.webp');sheet.save(p,lossless=True);meta['sheets'][key]=dict(key='nca_'+key,path=p.relative_to(R).as_posix());meta['banks'][name]=rows
(R/'assets/chronos_volley_art_1025.js').write_text('const C32_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf8')
print('Compiled',len(frames),'whole palm-volley poses with hand sockets.')
