from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,copy
from scipy.ndimage import label,binary_fill_holes
W=Path(__file__).resolve().parent;E=W/'exports';E.mkdir(exist_ok=True);C=512;M={};audit=[]
def clean(im,name,k):
 a=np.array(im.convert('RGBA'));threshold=239 if name=='chronus-transform-a' else 180
 mask=a[:,:,3]>threshold
 lab,n=label(mask);sizes=np.bincount(lab.ravel());sizes[0]=0
 # Retain authored detached fragments in the destruction sheet; remove matte specks.
 keep=np.where(sizes>110)[0] if name.endswith('gun-break') else [sizes.argmax()]
 mask=np.isin(lab,keep)
 a[:,:,3]=mask*255;a[~mask]=0
 yy,xx=np.where(mask);assert len(xx),name
 edge=bool(mask[0].any()or mask[-1].any()or mask[:,0].any()or mask[:,-1].any())
 audit.append(dict(source=name,frame=k,bounds=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],sourceClips=edge))
 return Image.fromarray(a)
def cells(name):
 im=Image.open(W/'generated'/(name+'.png'));cw,ch=im.width/4,im.height/2
 return [clean(im.crop((round(k%4*cw),round(k//4*ch),round((k%4+1)*cw),round((k//4+1)*ch))),name,k)for k in range(8)]
def register(im,scale=.70,root=None):
 root=root or [im.width*.5,im.height*.925];f=Image.new('RGBA',(C,C));f.alpha_composite(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST),(round(256-root[0]*scale),round(410-root[1]*scale)));return f
def meta(f,gun=False):
 a=np.array(f);mask=a[:,:,3]>0;yy,xx=np.where(mask);z=dict(bounds=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],spans=[np.flatnonzero(np.diff(np.r_[False,row,False])).tolist()for row in mask],wholeGenerated=True)
 assert xx.min()>0 and yy.min()>0 and xx.max()<511 and yy.max()<511,('export clips',z['bounds'])
 if gun:
  y,x=np.indices(mask.shape);gm=mask&(((abs(x-256)<28)&(y>246))|((abs(x-256)<66)&(y>277)&(y<300)))
  gy,gx=np.where(gm);lower=mask&(abs(x-256)<24)&(y>350);my,mx=np.where(lower);bottom=int(my.max());z.update(muzzle=[256,bottom-13],gunBounds=[int(gx.min()),int(gy.min()),int(gx.max()+1),int(gy.max()+1)],gunSpans=[np.flatnonzero(np.diff(np.r_[False,row,False])).tolist()for row in gm])
 return z
def material(f,mat,gunmask=None):
 out=np.array(f).copy();r,g,b=[out[:,:,v].astype(float)for v in range(3)];hi=np.maximum.reduce([r,g,b]);lo=np.minimum.reduce([r,g,b]);opaque=out[:,:,3]>0;rr,gg,bb=r.copy(),g.copy(),b.copy()
 if mat=='chrome':
  mask=opaque&(hi-lo<65)&(hi>30);v=np.minimum(255,hi*1.4+9);rr[mask]=v[mask];gg[mask]=v[mask];bb[mask]=np.minimum(255,v[mask]+5)
 elif mat=='red':
  mask=opaque&(b>g*1.4)&((b>r*1.15)|(r>g*1.4))&(b>115);v=np.maximum(r,b);rr[mask]=np.minimum(255,v[mask]*1.1);gg[mask]=v[mask]*.12;bb[mask]=v[mask]*.18
  mask=opaque&~mask&(hi>40)&(hi-lo<65);rr[mask]=np.minimum(255,hi[mask]*1.2);gg[mask]=g[mask]*.48;bb[mask]=b[mask]*.52
 elif mat=='hit':rr[opaque]=gg[opaque]=bb[opaque]=255
 elif mat=='gunhit':rr[gunmask]=gg[gunmask]=bb[gunmask]=255
 for k,v in enumerate([rr,gg,bb]):out[:,:,k]=np.floor(v).astype(np.uint8)
 return Image.fromarray(out)
def bank(name,frames,gun=False,cell=C,pivot=None):
 pivot=pivot or [cell//2,cell//2];cols=4;rows=(len(frames)+3)//4;folder=E/name;folder.mkdir(exist_ok=True);metas=[meta(f,gun) if cell==512 else dict(bounds=list(f.getbbox()),spans=[])for f in frames]
 mats=['regular','chrome','red','hit']
 for mat in mats:
  sheet=Image.new('RGBA',(cell*cols,cell*rows));gf=Image.new('RGBA',sheet.size)
  for k,f in enumerate(frames):
   pose=material(f,mat) if cell==512 or name=='gun-prop' else f
   sheet.alpha_composite(pose,(k%cols*cell,k//cols*cell))
   if gun:
    gm=np.zeros((cell,cell),bool)
    for y,span in enumerate(metas[k]['gunSpans']):
     for x0,x1 in zip(span[::2],span[1::2]):gm[y,x0:x1]=True
    gf.alpha_composite(material(pose,'gunhit',gm),(k%cols*cell,k//cols*cell))
   if mat=='regular':f.save(folder/f'{k:02}.png')
  sheet.save(E/f'{name}_{mat}.webp',lossless=True,method=1)
  if mat=='regular':sheet.save(E/f'{name}_regular.png')
  if gun and mat!='hit':gf.save(E/f'{name}_{mat}_gunhit.webp',lossless=True,method=1)
 M[name]=dict(cell=[cell,cell],pivot=pivot,cols=cols,count=len(frames),gun=gun,meta=metas)
 print('Built',name,len(frames),flush=True)
for name,ref in [('chronus','chronos'),('draconus','draconus')]:
 phase={k:cells(name+'-transform-'+k)for k in 'abcd'}
 # Exclude regenerated phase openings that refold the already extended legs.
 # These are complete original drawings, ordered by mechanical deployment.
 raw=phase['a'][:6]+phase['b'][2:]+phase['c'][3:]+phase['d'][2:]
 frames=[register(f)for f in raw]
 ship=clean(Image.open(W/'generated'/(name+'-ship.png')),name+'-ship',0);box=ship.getbbox();scale=300/(box[2]-box[0]);f=Image.new('RGBA',(512,512));res=ship.resize((round(ship.width*scale),round(ship.height*scale)),Image.Resampling.NEAREST);f.alpha_composite(res,(round(256-(box[0]+box[2])/2*scale),round(275-(box[1]+box[3])/2*scale)));frames[0]=f
 frames.append(Image.open(W/'references'/(ref+'-ready-regular.png')).convert('RGBA'))
 bank(name+'-transform',frames)
 # Exact existing Chromium endpoint, not an approximation from a new sheet.
 p=E/(name+'-transform_chrome.webp');s=Image.open(p).convert('RGBA');end=Image.open(W/'references'/(ref+'-ready-chrome.png')).convert('RGBA');k=len(frames)-1;s.paste(end,(k%4*512,k//4*512));s.save(p,lossless=True)
for name in ['draconus-gun-spin','draconus-gun-fire','draconus-catch-pre','draconus-catch-take','draconus-gun-stow','draconus-gun-break']:
 raw=cells(name)
 # First empty throw follow-through has fingers clipped by the generation crop.
 # Use the intact next whole drawing for that anticipation beat.
 if name=='draconus-catch-pre':raw[0]=raw[1].copy()
 if name=='draconus-gun-fire':raw=raw[:6]+raw[7:]
 if name=='draconus-gun-break':raw=raw[:5]+raw[6:]
 bank(name,[register(f)for f in raw],gun=name in ['draconus-gun-spin','draconus-gun-fire','draconus-catch-take'])
base=Image.open(E/'draconus-gun-spin/00.png').convert('RGBA');plain=np.array(base);chrome=np.array(material(base,'chrome'));activation=[]
for k in range(8):
 a=plain.copy();a[:,:,:3]=np.rint(plain[:,:,:3].astype(float)+(chrome[:,:,:3].astype(float)-plain[:,:,:3])*k/7).astype('uint8');activation.append(Image.fromarray(a))
bank('draconus-gun-armor',activation,gun=True)
im=clean(Image.open(W/'generated/draconus-gun-prop.png'),'draconus-gun-prop',0);box=im.getbbox();scale=168/(box[3]-box[1]);f=Image.new('RGBA',(256,256));res=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);f.alpha_composite(res,(round(128-(box[0]+box[2])/2*scale),round(128-(box[1]+box[3])/2*scale)));bank('gun-prop',[f],cell=256,pivot=[128,128])
# The existing exclusive icon box has the approved opening silhouette/icon.
s=Image.open(W/'references/approved-icon-box-opening.webp').convert('RGBA');frames=[]
for k in range(9):
 f=s.crop((k%4*80,k//4*80,k%4*80+80,k//4*80+80));a=np.array(f);r,g,b=[a[:,:,v].copy()for v in range(3)];mask=(b>r*1.2)&(b>g*.95)&(b>75);a[:,:,0][mask]=np.maximum(r[mask],b[mask]*.7).astype('uint8');a[:,:,1][mask]=(g[mask]*.55).astype('uint8');frames.append(Image.fromarray(a))
bank('icon-box',frames,cell=80,pivot=[40,40])
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')));(W/'audit.json').write_text(json.dumps(audit,indent=2))
(W/'boss_ship_forms_art_1111.js').write_text("'use strict';\n/* Original closed ships and whole-actor transform/gun sequences. */\nconst SF1111_ART="+json.dumps(M,separators=(',',':'))+';\n')
# Whole-frame visual inspection, no new production art is drawn here.
for name in M:
 if M[name]['cell'][0]!=512:continue
 s=Image.open(E/(name+'_regular.png')).convert('RGBA');board=Image.new('RGBA',s.size,'#101820');board.alpha_composite(s);board.resize((1024,board.height//2),Image.Resampling.NEAREST).save(W/'reviews'/(name+'.png'))
print('Ready for native installation.',flush=True)
