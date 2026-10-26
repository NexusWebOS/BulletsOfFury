"""Whole generated acting, original two-hand hold; one scale/pivot per bank."""
from pathlib import Path
from PIL import Image
import json,math,numpy as np
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/chronos_commitment_1025';O=R/'assets/game/shared/combat/chronos_commitment_1025';O.mkdir(parents=True,exist_ok=True)
art={'sheets':{},'banks':{},'source':'Original H22 two-handed plasma hammer. GPT stun and rage keys; PixelLab recovery and power-up interpolation. No modular held hammer.'}
def tint(im,mat):
 a=np.array(im);v=a[:,:,:3].astype(float);hi=v.max(2);lo=v.min(2);l=v@np.array([.2126,.7152,.0722]);m=(hi-lo<35)&(l>30)&(l<230)
 if mat=='chrome':
  z=np.minimum(235,l*1.48+6);target=np.stack([z*.96,z*.99,z],2);mix=m*.68
 elif mat=='red':
  z=np.minimum(250,np.maximum(hi,l*1.8));target=np.stack([z,l*.22,l*.28],2);mix=m*.72
 else:return im.copy()
 a[:,:,:3]=np.clip(v*(1-mix[:,:,None])+target*mix[:,:,None],0,255).astype('uint8');return Image.fromarray(a)
def normalized(im):
 # All acting frames share .85 proportional scale and fixed translation.
 q=Image.new('RGBA',(256,256));q.alpha_composite(im.resize((218,218),Image.Resampling.NEAREST),(19,23));return q
def export(name,frames,pivot,points=None):
 w,h=frames[0].size;assert w%2==h%2==0 and all(f.size==(w,h) for f in frames)
 for hit in [False,True]:
  key='c29_'+name+('_hit' if hit else '');sheet=Image.new('RGBA',(w*4,h*math.ceil(len(frames)/4)));rows=[]
  for i,im in enumerate(frames):
   q=im.copy()
   if hit:q=Image.new('RGBA',im.size,'white');q.putalpha(im.getchannel('A'))
   x=i%4*w;y=i//4*h;sheet.alpha_composite(q,(x,y));a=dict(key=key+'_'+str(i),sheet=key,cell=[x,y,w,h],w=w,h=h,pivot=pivot,bounds=list(im.getbbox()),_hf22=True,_c27=True,_c29=True,frame=i,bank=name)
   if not hit:a['white']='c29_'+name+'_hit_'+str(i)
   if points:a.update(points[i])
   else:a['hand']=[112,35]
   rows.append(a)
  p=O/(key+'.webp');sheet.save(p,lossless=True);art['sheets'][key]=dict(key='nca_'+key,path=p.relative_to(R).as_posix());art['banks'][name+('_hit' if hit else '')]=rows
raw=(R/'assets/hammer_correction_art_1022.js').read_text(encoding='utf8');old=json.JSONDecoder().raw_decode(raw[raw.index('{'):])[0]
for mat in ['regular','chrome','red']:
 frames=[];pts=[]
 for i in [0,1,2,3,4,5,6,7,8]:
  a=old['banks']['blue_slam'+('_armor' if mat=='chrome' else '')][i];sheet=Image.open(R/old['sheets'][a['sheet']]['path']).convert('RGBA');x,y,w,h=a['cell'];im=sheet.crop((x,y,x+w,y+h)).resize((448,448),Image.Resampling.NEAREST)
  if mat=='red':im=tint(im,mat)
  frames.append(im);pts.append({'tip':[v*1.75 for v in a['tip']]})
 export('hold_'+mat,frames,[224,196],pts)
 stun=[normalized(Image.open(D/f'stun-key-{i}.png').convert('RGBA')) for i in range(3)]
 recall=[normalized(Image.open(D/'recall'/f'{i:02}.png').convert('RGBA')) for i in range(9)]
 rage=[normalized(Image.open(D/f'rage-key-{i}.png').convert('RGBA')) for i in [0,1]]+[normalized(Image.open(D/'rage'/f'{i:02}.png').convert('RGBA')) for i in range(9)]+[normalized(Image.open(D/f'rage-key-{i}.png').convert('RGBA')) for i in [6,7]]
 for name,bank in [('stun',stun),('recall',recall),('rage',rage)]:export(name+'_'+mat,[tint(im,mat) for im in bank],[128,90])
(R/'assets/chronos_commitment_art_1025.js').write_text('const C29_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8')
print('Exported',len(art['banks']),'banks; even fixed cells, original held hammer, native hit masks.')

import runpy
runpy.run_path(str(R/'_BUILD_SOURCE/clean_chronos_chromium_1025.py'))
