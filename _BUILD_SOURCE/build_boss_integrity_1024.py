"""GPT key poses -> pinned PixelLab motion -> registered whole-actor banks."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/boss_integrity_1024';D=R/'assets/game/shared/combat/boss_integrity_1024';D.mkdir(parents=True,exist_ok=True)
art={'banks':{},'sheets':{}}
def export(name,frames,pivot):
 w,h=frames[0].size;assert w%2==h%2==0 and all(im.size==(w,h)for im in frames)
 cols=4;rows=(len(frames)+cols-1)//cols;im=Image.new('RGBA',(w*cols,h*rows));white=Image.new('RGBA',im.size)
 for i,f in enumerate(frames):
  im.alpha_composite(f,(i%cols*w,i//cols*h));q=Image.new('RGBA',f.size,'white');q.putalpha(f.getchannel('A'));white.alpha_composite(q,(i%cols*w,i//cols*h))
 path=D/(name+'.webp');hit=D/(name+'_hit.webp');im.save(path,lossless=True);white.save(hit,lossless=True)
 art['sheets'][name]={'key':'nca_bi24_'+name,'path':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 art['sheets'][name+'_hit']={'key':'nca_bi24_'+name+'_hit','path':hit.relative_to(R).as_posix(),'sha256':hashlib.sha256(hit.read_bytes()).hexdigest()}
 art['banks'][name]={'key':'nca_bi24_'+name,'white':'nca_bi24_'+name+'_hit','w':w,'h':h,'pivot':pivot,'count':len(frames),'cols':cols,'sourceScale':1}
for p in sorted((S/'motion').glob('*')):
 if not p.is_dir():continue
 name=p.name;actor=name.split('_')[0];files=sorted(p.glob('*.png'));assert len(files)==17,(name,len(files))
 # Rejected generated frames never reach the runtime. Preserve raw candidates.
 if name=='dracodia_strike':files=[files[i]for i in list(range(10))+[16]]
 if name=='phoenix_wind':files=sorted((S/'phoenix_v3').glob('*.png'))
 if name=='phoenix_strike':files=list(reversed(sorted((S/'phoenix_v3').glob('*.png'))))
 if name=='phoenix_recover':
  base=sorted((S/'phoenix_v3').glob('*.png'));files=[base[i]for i in [0,1,2,1,0]]
 if name=='chronos_cast':files=[files[i]for i in [0,1,2,3]+list(range(8,17))]
 size=448 if actor=='chronos'else 512;target=(136.57,125.14)if actor=='chronos'else(128,128);frames=[];geometry=[]
 for f in files:
  im=Image.open(f).convert('RGBA');assert im.size==(256,256)
  a=np.array(im)
  from scipy.ndimage import label
  labs,num=label(a[:,:,3]>0);sizes=np.bincount(labs.ravel());sizes[0]=0
  keep=sizes>=max(12,sizes.max()*.004);a[~keep[labs]]=0;im=Image.fromarray(a)
  yy,xx=np.indices((256,256));center=(abs(xx-target[0])<22)&(abs(yy-target[1])<18)&(a[:,:,3]>180)
  if actor=='chronos':mask=center&(a[:,:,1]>140)&(a[:,:,2]>170)&(a[:,:,0]<150)
  else:mask=center&(a[:,:,0]>180)&(a[:,:,0]>a[:,:,1]*1.35)&(a[:,:,0]>a[:,:,2]*1.2)
  cx=float(xx[mask].mean())if mask.sum()>5 else target[0];cy=float(yy[mask].mean())if mask.sum()>5 else target[1]
  dx=round(target[0]-cx);dy=round(target[1]-cy)
  assert abs(dx)<20 and abs(dy)<20,(name,f.name,dx,dy)
  out=Image.new('RGBA',(256,256));out.alpha_composite(im,(dx,dy));out=out.resize((size,size),Image.Resampling.NEAREST);frames.append(out);geometry.append({'frame':f.name,'translation':[dx,dy]})
 export(name,frames,[224,258]if actor=='chronos'else[256,256]);(p/'geometry.json').write_text(json.dumps(geometry,indent=2))
 art['banks'][name]['sources']=[f.relative_to(S).as_posix()for f in files]
 if actor=='phoenix':
  sockets=[]
  for im in frames:
   a=np.array(im.resize((256,256),Image.Resampling.NEAREST));yy,xx=np.indices((256,256));row={}
   for side,lo,hi in [('left',62,116),('right',140,198)]:
    mask=(xx>=lo)&(xx<hi)&(yy>112)&(yy<171)&(a[:,:,0]>165)&(a[:,:,1]>95)&(a[:,:,2]<125)&(a[:,:,3]>160)
    cutoff=np.percentile(yy[mask],85);tips=mask&(yy>=cutoff)
    row[side]=[round(float(xx[tips].mean()),2),round(float(yy[tips].mean()),2)]
   sockets.append(row)
  art['banks'][name]['sockets']=sockets
 if actor=='dracodia':
  arms=[]
  for im in frames:
   a=np.array(im.resize((256,256),Image.Resampling.NEAREST));yy,xx=np.indices((256,256));row={}
   for side,lo,hi in [('left',20,110),('right',146,236)]:
    mask=(xx>=lo)&(xx<hi)&(yy>80)&(yy<220)&(a[:,:,3]>160)
    row[side]=[round(float(xx[mask].mean()),2),round(float(yy[mask].mean()),2)]
   arms.append(row)
  art['banks'][name]['arms']=arms
 # Match existing Chronos accent variants; keep grayscale metal and outlines.
 if actor=='chronos':
  red=[];armor=[];tips=[]
  for im in frames:
   a=np.array(im);rgb=a[:,:,:3].astype(float);mx=rgb.max(2);mn=rgb.min(2);blue=(rgb[:,:,2]>rgb[:,:,0]*1.3)&(rgb[:,:,2]>100)&(mx-mn>45)
   yy,xx=np.indices(a.shape[:2]);mask=blue&(((xx-239)**2+(yy-219)**2)>35**2);labs,num=label(mask);sizes=np.bincount(labs.ravel());sizes[0]=0
   chosen=sizes.argmax();hy,hx=np.where(labs==chosen);tips.append([round(float(hx.mean())),round(float(hy.mean()))])
   r=a.copy();r[blue,0]=a[blue,2];r[blue,1]=(a[blue,1]*.35).astype('uint8');r[blue,2]=(a[blue,0]*.5).astype('uint8');red.append(Image.fromarray(r))
   # Chromium retains cyan ordnance and glow; bright neutral metal highlights
   # get the same cooler plated material without suppressing hit feedback.
   ar=a.copy();metal=(mx-mn<38)&(mx>55)&(a[:,:,3]>0);ar[metal,0]=(rgb[metal,0]*.86).astype('uint8');ar[metal,1]=np.minimum(255,rgb[metal,1]*.98+7).astype('uint8');ar[metal,2]=np.minimum(255,rgb[metal,2]*1.06+12).astype('uint8');armor.append(Image.fromarray(ar))
  art['banks'][name]['tips']=tips
  export(name+'_red',red,[224,258]);export(name+'_armor',armor,[224,258])
  for variant in ['_red','_armor']:art['banks'][name+variant]['tips']=tips
(D/'manifest.json').write_text(json.dumps(art,indent=2),encoding='utf8',newline='\n');(R/'assets/boss_integrity_art_1024.js').write_text('"use strict";\nconst BI24_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
p=R/'assets/data/ART_TAXONOMY.json';d=json.loads(p.read_text(encoding='utf8',newline='\n'));d['bi24_']={'owner':'_BUILD_SOURCE/build_boss_integrity_1024.py','manifest':'assets/game/shared/combat/boss_integrity_1024/manifest.json','purpose':'Whole connected GPT Phoenix/Dracodia/Chronos keyposes interpolated in PixelLab, fixed core pivots and actual white hit banks; no cropped-body debris.'};p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n')
print('Registered',len(art['banks']),'whole actor banks')
