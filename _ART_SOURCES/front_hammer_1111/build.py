from pathlib import Path
import json,math,hashlib,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
W=Path(__file__).resolve().parent;OLD=W.parent/'heavy_hammer_1111';E=W/'exports';E.mkdir(exist_ok=True)
O=W.parents[1]/'outputs/Front-facing-hammer';O.mkdir(parents=True,exist_ok=True)
C=512;P=[256,256];FOOT=410;cache={};audit=[]
prior_manifest=OLD/'manifest.json'
if not prior_manifest.exists():prior_manifest=W/'references/previous-manifest.json'
old_manifest=json.loads(prior_manifest.read_text())
def legacy(unit,k):
 n=('blue'if unit=='blue'else'corrupt')+'-overhead';a=old_manifest[n];p=W/'references/ready'/n/f'{k:02}.png'
 if not p.exists():p=OLD/'exports'/n/f'{k:02}.png'
 f=Image.open(p).convert('RGBA');return f,dict(a['meta'][k],retainedApproved=True)
def source(name,k,rows=2,scale=.8):
 key=(name,k,rows,scale)
 if key in cache:return cache[key]
 im=Image.open(W/'generated'/(name+'.png')).convert('RGBA');cw,ch=im.width/4,im.height/rows
 box=[round(k%4*cw),round(k//4*ch),round((k%4+1)*cw),round((k//4+1)*ch)]
 # The final lift occupies some empty padding above the internal row guide.
 if 'lift'in name and k==7:box[1]-=28
 a=np.array(im.crop(tuple(box)));m=a[:,:,3]>180;l,n=label(m);sizes=np.bincount(l.ravel());sizes[0]=0;m=l==sizes.argmax()
 assert m.any()and not(m[0].any()or m[-1].any()or m[:,0].any()or m[:,-1].any()),('clipped source',name,k)
 a[:,:,3]=m*255;a[~m]=0;h,w=m.shape;yy,xx=np.indices(m.shape);r,g,b=[a[:,:,i].astype(float)for i in range(3)]
 hot=m&((r>160)&(b>200)&(b>g*1.8)&(r>g*1.6)if name.startswith('drac')else(b>170)&(b>r*1.8)&(b>g*1.15))
 if 'lift'in name:hot&=(xx<w*.43)if k<6 else(yy<h*.37)
 elif 'down'in name:hot&=(yy<h*.40)if k<3 else(yy>h*.64)&(xx>w*.3)&(xx<w*.66)
 elif 'recovery'in name:hot&=(yy>h*.65)&(abs(xx-w*.5)<w*.18)if k<4 else(xx<w*.37)&(yy>h*.43)
 else:hot&=yy<h*.43
 hl,hn=label(hot);hs=np.bincount(hl.ravel());hs[0]=0;assert hs.max()>12,('hammer lightning landmark',name,k);hm=hl==hs.argmax();hy,hx=np.where(hm);seed=[float(hx.mean()),float(hy.mean())]
 hy,hx=np.where(hot&(abs(xx-seed[0])<45)&(abs(yy-seed[1])<70));head=[float(hx.mean()),float(hy.mean())]
 feet=m&(yy>h*.83);full_y,full_x=np.where(feet)
 if ('down'in name or 'recovery'in name and k<4)and head[1]+65>h*.83:feet&=abs(xx-head[0])>58
 fy,fx=np.where(feet);assert len(fx)>180,('boots',name,k)
 root=[float((full_x.min()+full_x.max())/2),float(fy.max())]
 side='sides'in name
 region=m&(abs(xx-head[0])<(75 if side else 48))&(abs(yy-head[1])<(32 if side else 75))
 py,px=np.where(region&(abs(yy-head[1])<8 if side else abs(xx-head[0])<8));assert len(px)
 ix=np.argmin(px)if side else np.argmax(py);tip=[float(px[ix]),float(py[ix])]
 clean=Image.fromarray(a).resize((round(w*scale),round(h*scale)),Image.Resampling.NEAREST);offset=[round(P[0]-root[0]*scale),round(FOOT-root[1]*scale)]
 frame=Image.new('RGBA',(C,C));frame.alpha_composite(clean,tuple(offset));alpha=np.array(frame)[:,:,3];ay,ax=np.where(alpha)
 assert ax.min()>0 and ay.min()>0 and ax.max()<C-1 and ay.max()<C-1,('export clips',name,k)
 pos=lambda v:[round(offset[0]+v[0]*scale),round(offset[1]+v[1]*scale)]
 tp=pos(tip);j=np.argmin((ax-tp[0])**2+(ay-tp[1])**2);tp=[int(ax[j]),int(ay[j])]
 meta=dict(source=name,sourceCell=k,crop=box,scale=scale,root=root,tip=tp,headCenter=pos(head),grip=[P[0],FOOT-145],bounds=[int(ax.min()),int(ay.min()),int(ax.max()+1),int(ay.max()+1)],wholeGenerated=True,faceForward=True,endCapLeads=True,capAxis=[-1,0]if side else[0,1],depth=1)
 cache[key]=(frame,meta);audit.append(meta);return frame,meta

banks={n:a for n,a in old_manifest.items()if n.endswith('whirl')};spec=[]
for unit,prefix in [('drac','corrupt'),('blue','blue')]:
 overhead=[legacy(unit,k)for k in range(8)]
 for group,name,scale in [(1,unit+'-lift-front',.80),(2,unit+'-down',.90),(3,'drac-recovery-center'if unit=='drac'else'blue-recovery',.74)]:
  for i in range(8):
   f,z=source(name,6 if group==2 and i==7 else i,scale=scale);idx=group*8+i
   overhead.append((f,dict(z,phase='behind-head'if 14<=idx<=18 else'downstroke'if 19<=idx<22 else'contact'if idx<=23 else'recovery')))
 sides=[(f,dict(z,phase='load'if i<5 else'contact'if i<9 else'recovery'))for i,(f,z)in enumerate(source(unit+'-sides-front',k,4,1.02)for k in range(16))]
 for suffix,frames in [('overhead',overhead),('sides',sides),('right',sides)]:
  name=prefix+'-'+suffix;sheet=Image.new('RGBA',(C*4,C*math.ceil(len(frames)/4)));meta=[];folder=E/name;folder.mkdir(exist_ok=True);fs=[]
  for i,(f,z0)in enumerate(frames):
   z=dict(z0)
   if suffix=='right':
    f=f.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    for key in ['tip','headCenter','grip']:z[key]=[C-1-z[key][0],z[key][1]]
    x0,y0,x1,y1=z['bounds'];z['bounds']=[C-x1,y0,C-x0,y1];z['capAxis']=[1,0];z['mirror']=True
   alpha=np.array(f)[:,:,3];z['spans']=[np.flatnonzero(np.diff(np.r_[False,row>0,False])).tolist()for row in alpha];meta.append(z)
   sheet.alpha_composite(f,(i%4*C,i//4*C));f.save(folder/f'{i:02}.png');q=Image.new('RGBA',(C,C),'#101820');q.alpha_composite(f);fs.append(q.convert('RGB'))
  sheet.save(E/(name+'_regular.png'));base=np.array(sheet);r,g,b=[base[:,:,k].astype(float)for k in range(3)];hi=np.maximum.reduce([r,g,b]);lo=np.minimum.reduce([r,g,b]);opaque=base[:,:,3]>0
  for mat in ['regular','chrome','red','hit','red_hit']:
   out=base.copy();rr,gg,bb=r.copy(),g.copy(),b.copy()
   if mat in ['hit','red_hit']:rr[opaque]=255;gg[opaque]=255 if mat=='hit'else 35;bb[opaque]=255 if mat=='hit'else 42
   elif mat=='chrome':
    mask=opaque&(hi-lo<65)&(hi>30);v=np.minimum(255,hi*1.4+9);rr[mask]=v[mask];gg[mask]=v[mask];bb[mask]=np.minimum(255,v[mask]+5)
   elif mat=='red':
    mask=opaque&(b>g*1.4)&((b>r*1.15)|(r>g*1.4))&(b>115);v=np.maximum(r,b);rr[mask]=np.minimum(255,v[mask]*1.1);gg[mask]=v[mask]*.12;bb[mask]=v[mask]*.18
    mask=opaque&~mask&(hi>40)&(hi-lo<65);rr[mask]=np.minimum(255,hi[mask]*1.2);gg[mask]=g[mask]*.48;bb[mask]=b[mask]*.52
   for k,v in enumerate([rr,gg,bb]):out[:,:,k]=np.floor(v).astype(np.uint8)
   Image.fromarray(out).save(E/(name+'_'+mat+'.webp'),lossless=True,method=1)
  banks[name]=dict(cell=[C,C],pivot=P,cols=4,count=len(frames),folder='front_hammer_1111',meta=meta);spec.append(dict(name=name,count=len(frames)))
  fs[0].save(O/(name+'.gif'),save_all=True,append_images=fs[1:],duration=55,loop=0,disposal=2)
  board=Image.new('RGB',(C*4,C*math.ceil(len(fs)/4)),'#101820');d=ImageDraw.Draw(board)
  for i,f in enumerate(fs):board.paste(f,(i%4*C,i//4*C));d.text((i%4*C+8,i//4*C+8),str(i),fill='white')
  board.save(O/(name+'-poses.png'));print('Exported',name,len(fs),flush=True)
(W/'manifest.json').write_text(json.dumps(banks,separators=(',',':')));(W/'aseprite-jobs.json').write_text(json.dumps(spec))
(W/'front_hammer_art_1111.js').write_text("'use strict';\n/* Front-facing whole strikes for both native hammer and Chromium forms. */\nObject.assign(BA119_ART,"+json.dumps(banks,separators=(',',':'))+');\n')
(W/'audit.json').write_text(json.dumps(dict(sourceImports=audit,newCompleteDrawings=len(cache),retainedReadyDrawings=16,updatedTimelineCells=128,retainedWhirlBanks=2),indent=2))
print('Finished six frontal attack banks; normal/chrome/red/hit variants; existing whirl banks retained.',flush=True)
