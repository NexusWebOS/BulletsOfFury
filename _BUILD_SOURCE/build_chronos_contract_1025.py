"""Fixed448 whole empty-hand recovery bank from GPT poses, pinned PixelLab interpolation."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
from scipy.ndimage import label
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/chronos_contract_1025';D=R/'assets/game/shared/combat/chronos_contract_1025';D.mkdir(exist_ok=True)
frames=[]
for p in sorted((S/'motion-pinned').glob('*.png')):
 im=Image.open(p).convert('RGBA');assert im.size==(256,256);a=np.array(im);labs,n=label(a[:,:,3]>48);sizes=np.bincount(labs.ravel());sizes[0]=0;keep=sizes>=max(10,sizes.max()*.003);a[~keep[labs]]=0
 frames.append(Image.fromarray(a).resize((448,448),Image.Resampling.NEAREST))
assert len(frames)==9
art={'banks':{},'sheets':{},'source':'GPT kneel/stand -> PixelLab pinned 639ea9e8-d9c6-4f45-8474-55a17c937be1','rejected':'Unpinned793fba39 frames5+ invented a weapon; never registered.'}
for suffix in ['', '_armor','_red']:
 sheet=Image.new('RGBA',(448*4,448*3));hit=Image.new('RGBA',sheet.size)
 for i,im in enumerate(frames):
  a=np.array(im);rgb=a[:,:,:3].astype(float);mx=rgb.max(2);mn=rgb.min(2)
  if suffix=='_armor':
   metal=(mx-mn<40)&(mx>60)&(a[:,:,3]>0);a[metal,0]=np.minimum(255,rgb[metal,0]*.94+9);a[metal,1]=np.minimum(255,rgb[metal,1]*1.02+12);a[metal,2]=np.minimum(255,rgb[metal,2]*1.07+15)
  if suffix=='_red':
   blue=(rgb[:,:,2]>rgb[:,:,0]*1.3)&(rgb[:,:,2]>100)&(mx-mn>45);a[blue,0]=a[blue,2];a[blue,1]=(rgb[blue,1]*.35).astype('uint8');a[blue,2]=(rgb[blue,0]*.5).astype('uint8')
  im=Image.fromarray(a);x=i%4*448;y=i//4*448;sheet.alpha_composite(im,(x,y));w=Image.new('RGBA',im.size,'white');w.putalpha(im.getchannel('A'));hit.alpha_composite(w,(x,y))
 name='empty'+suffix
 for tag,im in [('',sheet),('_hit',hit)]:
  path=D/(name+tag+'.webp');im.save(path,lossless=True);art['sheets'][name+tag]={'key':'nca_c25_'+name+tag,'path':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 art['banks'][name]={'sheet':'c25_'+name,'w':448,'h':448,'pivot':[224,258],'count':9,'cols':4,'scale':1}
# Cleaned opening keeps the original239px silhouette height and common pivot.
im=Image.open(S/'gpt-intro-clean.png').convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>48);sizes=np.bincount(labs.ravel());sizes[0]=0;mask=labs==sizes.argmax();yy,xx=np.where(mask);a[~mask]=0;im=Image.fromarray(a).crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1));k=239/im.height;im=im.resize((round(im.width*k),239),Image.Resampling.NEAREST);out=Image.new('RGBA',(448,448));out.alpha_composite(im,(95,145));a=np.array(out);yy,xx=np.indices((448,448));blue=(a[:,:,2]>120)&(a[:,:,2]>a[:,:,0].astype(float)*1.3)&(a[:,:,3]>100)&(xx<220)&(yy>300);tip=[round(float(xx[blue].mean())),round(float(yy[blue].mean()))]
for tag,img in [('',out),('_hit',Image.new('RGBA',out.size,'white'))]:
 if tag:img.putalpha(out.getchannel('A'))
 path=D/('intro'+tag+'.webp');img.save(path,lossless=True);art['sheets']['intro'+tag]={'key':'nca_c25_intro'+tag,'path':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
art['banks']['intro']={'sheet':'c25_intro','w':448,'h':448,'pivot':[224,258],'count':1,'cols':1,'scale':1,'tip':tip}
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n',encoding='utf8',newline='\n');(R/'assets/chronos_contract_art_1025.js').write_text('"use strict";\nconst C25_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
p=R/'assets/data/ART_TAXONOMY.json';d=json.loads(p.read_text(encoding='utf8'));d['c25_']={'owner':'_BUILD_SOURCE/build_chronos_contract_1025.py','manifest':D.relative_to(R).as_posix()+'/manifest.json','purpose':'Intact empty-handed Chronos kneel, hit and recovery/death identity; uniform448 cells/224,258 pivot, real white hit banks.'};p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n');print('Registered empty-hand recovery and cleaned opening,448x448.')
