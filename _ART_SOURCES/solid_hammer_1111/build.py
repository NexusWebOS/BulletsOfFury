from pathlib import Path
import json, math, hashlib
import numpy as np
from scipy.ndimage import label
from PIL import Image, ImageDraw
W=Path(__file__).resolve().parent; PRIOR=W.parent/'front_hammer_1111'; E=W/'exports'; E.mkdir(exist_ok=True)
O=W.parents[1]/'outputs/Solid-metal-hammers'; O.mkdir(exist_ok=True,parents=True)
M=json.loads((PRIOR/'manifest.json').read_text()); C=512; FOOT=410; P=[256,256]; audit=[]

def imported(unit,move,k):
 im=Image.open(W/'generated'/f'{unit}-{move}.png').convert('RGBA'); cw,ch=im.width/4,im.height/2
 box=[round(k%4*cw),round(k//4*ch),round((k%4+1)*cw),round((k//4+1)*ch)]
 # The lifted head enters blank space above the internal row division; retain it from the master.
 if move=='lift'and k>=4: box[1]-=24
 a=np.array(im.crop(box)); m=a[:,:,3]>180; lab,_=label(m); sizes=np.bincount(lab.ravel()); sizes[0]=0; m=lab==sizes.argmax()
 assert not(m[0].any()or m[-1].any()or m[:,0].any()or m[:,-1].any()),('source clipped',unit,move,k)
 a[:,:,3]=m*255; a[~m]=0; yy,xx=np.indices(m.shape); h,w=m.shape; r,g,b=[a[:,:,v].astype(float)for v in range(3)]
 hot=m&(((b>160)&(b>r*1.7)&(b>g*1.2))if unit=='blue'else((r>150)&(b>180)&(r>g*1.7)&(b>g*1.8)))
 if move=='lift': hot&=(xx<w*.43)if k<6 else(yy<h*.33)
 elif move=='down': hot&=(yy<h*.44)&(xx<w*.55)if k<4 else(yy>h*.6)&(xx<w*.36)
 else: hot&=(xx<w*.34)&(yy>h*.37)
 hl,_=label(hot); hs=np.bincount(hl.ravel()); hs[0]=0; assert hs.max()>10,('no head',unit,move,k)
 hy,hx=np.where(hl==hs.argmax()); seed=[float(hx.mean()),float(hy.mean())]
 hy,hx=np.where(hot&(abs(xx-seed[0])<44)&(abs(yy-seed[1])<65)); head=[float(hx.mean()),float(hy.mean())]
 # Feet are measured below the shins, excluding the low head, rather than fitting each silhouette.
 feet=m&(yy>h*.83)&(xx>w*.27)
 full_y,full_x=np.where(feet)
 if head[1]>h*.64: feet&=~((abs(xx-head[0])<54)&(abs(yy-head[1])<80))
 fy,fx=np.where(feet); assert len(fx)>100,('no boots',unit,move,k)
 root=[float((full_x.min()+full_x.max())/2),float(fy.max())]
 # One calibration for every original sheet of a form. No per-pose resizing.
 scale=.86 if unit=='blue'else .86
 f=Image.new('RGBA',(C,C)); clean=Image.fromarray(a).resize((round(w*scale),round(h*scale)),Image.Resampling.NEAREST)
 off=[round(256-root[0]*scale),round(FOOT-root[1]*scale)]; f.alpha_composite(clean,off)
 ay,ax=np.where(np.array(f)[:,:,3]); assert ax.min()>0 and ay.min()>0 and ax.max()<C-1 and ay.max()<C-1,('export clipped',unit,move,k)
 # Lowest actual opaque cap/spike near the head, consumed by native hit/warning placement.
 reg=m&(abs(xx-head[0])<51)&(abs(yy-head[1])<83); ty,tx=np.where(reg&(abs(xx-head[0])<12)); j=np.argmax(ty); tip=[float(tx[j]),float(ty[j])]
 pos=lambda v:[round(off[0]+v[0]*scale),round(off[1]+v[1]*scale)]
 tp=pos(tip); j=np.argmin((ax-tp[0])**2+(ay-tp[1])**2); tp=[int(ax[j]),int(ay[j])]
 z=dict(source=f'{unit}-{move}',sourceCell=k,crop=box,scale=scale,root=root,tip=tp,headCenter=pos(head),grip=[256,265],bounds=[int(ax.min()),int(ay.min()),int(ax.max()+1),int(ay.max()+1)],wholeGenerated=True,faceForward=True,endCapLeads=True,capAxis=[0,1],depth=1,rigidMetal=True,phase='behind-head'if move=='lift'and k>=5 or move=='down'and k<=2 else'contact'if move=='down'and k>=6 else'downstroke'if move=='down'else'recovery'if move=='recovery'else'load')
 audit.append(z); return f,z

jobs=[]
for unit,prefix in [('blue','blue'),('drac','corrupt')]:
 name=prefix+'-overhead'; frames=[]
 for k in range(8):
  ready=PRIOR/'exports'/name/f'{k:02}.png'
  if not ready.exists(): ready=PRIOR/'references/ready'/name/f'{k:02}.png'
  frames.append((Image.open(ready).convert('RGBA'),dict(M[name]['meta'][k])))
 for move in ['lift','down','recovery']:
  frames.extend(imported(unit,move,k)for k in range(8))
 sheet=Image.new('RGBA',(2048,4096)); meta=[]; d=E/name; d.mkdir(exist_ok=True)
 for i,(f,z)in enumerate(frames):
  a=np.array(f)[:,:,3]; z['spans']=[np.flatnonzero(np.diff(np.r_[False,row>0,False])).tolist()for row in a]; meta.append(z)
  f.save(d/f'{i:02}.png'); sheet.alpha_composite(f,(i%4*C,i//4*C))
 sheet.save(E/(name+'_regular.png')); base=np.array(sheet); r,g,b=[base[:,:,v].astype(float)for v in range(3)]; hi=np.maximum.reduce([r,g,b]); lo=np.minimum.reduce([r,g,b]); opaque=base[:,:,3]>0
 for mat in ['regular','chrome','red','hit','red_hit']:
  out=base.copy(); rr,gg,bb=r.copy(),g.copy(),b.copy()
  if mat in ['hit','red_hit']: rr[opaque]=255; gg[opaque]=255 if mat=='hit'else 35; bb[opaque]=255 if mat=='hit'else 42
  elif mat=='chrome':
   mask=opaque&(hi-lo<65)&(hi>30); v=np.minimum(255,hi*1.4+9); rr[mask]=v[mask]; gg[mask]=v[mask]; bb[mask]=np.minimum(255,v[mask]+5)
  elif mat=='red':
   mask=opaque&(b>g*1.4)&((b>r*1.15)|(r>g*1.4))&(b>115); v=np.maximum(r,b); rr[mask]=np.minimum(255,v[mask]*1.1); gg[mask]=v[mask]*.12; bb[mask]=v[mask]*.18
   mask=opaque&~mask&(hi>40)&(hi-lo<65); rr[mask]=np.minimum(255,hi[mask]*1.2); gg[mask]=g[mask]*.48; bb[mask]=b[mask]*.52
  for k,v in enumerate([rr,gg,bb]): out[:,:,k]=np.floor(v).astype(np.uint8)
  Image.fromarray(out).save(E/(name+'_'+mat+'.webp'),lossless=True,method=1)
 M[name]=dict(cell=[C,C],pivot=P,cols=4,count=32,folder='front_hammer_1111',meta=meta); jobs.append(dict(name=name,count=32)); print('Exported',name,flush=True)
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')))
(W/'aseprite-jobs.json').write_text(json.dumps(jobs))
(W/'front_hammer_art_1111.js').write_text("'use strict';\n/* Complete rigid-metal overhead poses; existing side/whirl banks retained. */\nObject.assign(BA119_ART,"+json.dumps(M,separators=(',',':'))+');\n')
(W/'audit.json').write_text(json.dumps(dict(imports=audit,newWholeDrawings=48,overheadTimelineFrames=64,retainedReady=16,uniformScale=.86),indent=2))
print('Built solid metal overhead banks for all four material forms.',flush=True)
