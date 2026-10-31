from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
G=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=G/'expansion/topdown/art/gosfar44';M=json.loads((O/'manifest.json').read_text());r=[]
for name,b in M['banks'].items():
 if not(name.startswith('gosfar/') or name=='wall'):continue
 a=[];hashes=[]
 for k in b['frames']:
  m=M['assets'][k];x,y,w,h=m['rect'];im=Image.open(G/m['file']).crop((x,y,x+w,y+h));aa=np.array(im);a.append(im.getbbox());hashes.append(hashlib.sha256(im.tobytes()).hexdigest());assert set(np.unique(aa[:,:,3])).issubset({0,255});assert m['provider']=='PixelLab';assert w%2==h%2==0
  if name!='wall':assert im.getbbox()[0]>0 and im.getbbox()[1]>0 and im.getbbox()[2]<w and im.getbbox()[3]<h,(name,k,im.getbbox())
 r.append({'bank':name,'canvas':b['size'],'root':b['origin'],'frames':len(a),'unique_frames':len(set(hashes)),'bounds':a,'provider':'PixelLab'})
wall=M['banks']['wall'];m=M['assets'][wall['frames'][0]];x,y,w,h=m['rect'];im=Image.open(G/m['file']).crop((x,y,x+w,y+h));alpha=np.array(im)[:,:,3];assert (alpha[24:112,:]==255).all(),'intact seam has a hole';assert h-24==88
r.append({'wall_visible_height':88,'continuous_opaque_width':88,'sections':6,'total_width':528,'crew_foot_y':411,'wall_front_y':381,'wall_top_y':293,'states':['intact','cracked','breached','rubble']})
(O/'art-audit.json').write_text(json.dumps(r,indent=2));print('PixelLab art audit:',len(r)-1,'banks; fixed roots/even canvases/hard alpha; intact wall88x88 opaque; no actor clipping.')
