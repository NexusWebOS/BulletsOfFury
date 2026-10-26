"""Whole unarmed red casting, true rotor phases, clean charge alpha and wave FX."""
from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import numpy as np,json,math
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/chronos_beam_1025';O=R/'assets/game/shared/combat/chronos_beam_1025';O.mkdir(parents=True,exist_ok=True)
A={'banks':{},'sheets':{}}
def clean(im,threshold=96):
 a=np.array(im.convert('RGBA'));mask=a[:,:,3]>=threshold;labs,n=label(mask);sizes=np.bincount(labs.ravel());mask&=sizes[labs]>=5;a[:,:,3]=np.where(mask,255,0).astype('uint8');a[:,:,:3][~mask]=0;return Image.fromarray(a)
def readjs(p):
 s=(R/p).read_text(encoding='utf8');return json.JSONDecoder().raw_decode(s[s.index('{'):])[0]
def oldcell(a,row):
 im=Image.open(R/a['sheets'][row['sheet']]['path']).convert('RGBA');x,y,w,h=row['cell'];return im.crop((x,y,x+w,y+h))
def export(name,frames,pivot,points=None,hit=True):
 w,h=frames[0].size;assert w%2==h%2==0 and all(q.size==(w,h)for q in frames)
 for ishit in ([False,True] if hit else [False]):
  key='c30_'+name+('_hit' if ishit else '');sheet=Image.new('RGBA',(w*4,h*math.ceil(len(frames)/4)));rows=[]
  for i,im in enumerate(frames):
   q=im.copy()
   if ishit:q=Image.new('RGBA',im.size,'white');q.putalpha(im.getchannel('A'))
   x=i%4*w;y=i//4*h;sheet.alpha_composite(q,(x,y));row=dict(key=key+'_'+str(i),sheet=key,cell=[x,y,w,h],w=w,h=h,pivot=pivot,bounds=list(im.getbbox()),_hf22=True,_c26=True,_c30=True,frame=i,bank=name)
   if not ishit and hit:row['white']='c30_'+name+'_hit_'+str(i)
   if points:row.update(points[i])
   rows.append(row)
  p=O/(key+'.webp');sheet.save(p,lossless=True);A['sheets'][key]=dict(key='nca_'+key,path=p.relative_to(R).as_posix());A['banks'][name+('_hit' if ishit else '')]=rows
# Keep the original receiver and grips. Copy the complete rotating cluster,
# including its actual muzzle face (the old pass froze everything below y187).
ch=readjs('assets/chronos_modular_art_1023.js');base=oldcell(ch,ch['banks']['barrel'][0]);gun=[base]
for i in range(1,17):
 q=Image.open(D/'rotor'/f'{i:02}.png').convert('RGBA').crop((12,8,116,216));out=base.copy();out.paste((0,0,0,0),(0,80,104,208));out.alpha_composite(q.crop((0,80,104,208)),(0,80));gun.append(clean(out))
export('rotor',gun,[54,46],hit=True)
# Actor normalization is one .85 scale and translation, shared with the charge.
def norm(q):
 out=Image.new('RGBA',(256,256));out.alpha_composite(clean(q).resize((218,218),Image.Resampling.NEAREST),(19,23));return out
keys=[norm(Image.open(D/f'cast-key-{i}.png'))for i in range(8)]
# Landmarks are the center between both palms in each approved generated key.
tips=[[128,132],[79,128],[94,130],[84,126],[128,130],[128,110],[128,110],[128,136]]
export('cast',keys,[128,90],[{'tip':t}for t in tips])
thrust=[norm(Image.open(D/'thrust'/f'{i:02}.png'))for i in range(9)]
export('thrust',thrust,[128,90],[{'tip':[84+(128-84)*i/8,126+(110-126)*i/8]}for i in range(9)])
c29=readjs('assets/chronos_commitment_art_1025.js')
for mat in ['regular','chrome','red']:
 frames=[clean(oldcell(c29,row),150)for row in c29['banks']['rage_'+mat]];export('power_'+mat,frames,[128,90])
im=Image.open(D/'wave-gpt.png').convert('RGBA');fx=[]
for i in range(8):
 x=round(i%4*im.width/4);y=round(i//4*im.height/2);w=round(im.width/4);h=round(im.height/2);q=im.crop((x,y,x+w,y+h));q=clean(q,32);out=Image.new('RGBA',(192,384));out.alpha_composite(q.resize((188,376),Image.Resampling.NEAREST),(2,4));fx.append(out)
export('wave',fx,[96,28],hit=False)
(R/'assets/chronos_beam_art_1025.js').write_text('const C30_ART='+json.dumps(A,separators=(',',':'))+';\n',encoding='utf8')
print('Built rotor, whole unarmed casting/thrust, cleaned power-up and wave sheets.')
