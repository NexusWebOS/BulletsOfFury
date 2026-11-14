from pathlib import Path
import json,copy,shutil
import numpy as np
from scipy.ndimage import label
from PIL import Image
W=Path(__file__).resolve().parent; OLD=W.parent/'solid_hammer_1111'; E=W/'exports'; E.mkdir(exist_ok=True); C=512; FOOT=410
M=json.loads((OLD/'manifest.json').read_text()); jobs=[]; imports=[]
def oldpose(prefix,i):
 p=OLD/'exports'/(prefix+'-overhead')/f'{i:02}.png'
 if p.exists(): f=Image.open(p).convert('RGBA')
 else:
  s=Image.open(OLD/'exports'/(prefix+'-overhead_regular.png')).convert('RGBA'); f=s.crop((i%4*C,i//4*C,(i%4+1)*C,(i//4+1)*C))
 return f,copy.deepcopy(M[prefix+'-overhead']['meta'][i])
def imported(unit,move,k):
 im=Image.open(W/'generated'/f'{unit}-{move}.png').convert('RGBA'); cw,ch=im.width/4,im.height/2
 box=[round(k%4*cw),round(k//4*ch),round((k%4+1)*cw),round((k//4+1)*ch)]
 a=np.array(im.crop(box)); mask=a[:,:,3]>180; lab,_=label(mask); sz=np.bincount(lab.ravel());sz[0]=0;mask=lab==sz.argmax()
 assert not(mask[0].any()or mask[-1].any()or mask[:,0].any()or mask[:,-1].any()),('source clips',unit,move,k)
 a[:,:,3]=mask*255;a[~mask]=0;yy,xx=np.indices(mask.shape);h,w=mask.shape;r,g,b=[a[:,:,j].astype(float)for j in range(3)]
 hot=mask&(((b>160)&(b>r*1.7)&(b>g*1.2))if unit=='blue'else((r>150)&(b>180)&(r>g*1.7)&(b>g*1.8)))
 if move=='down':hot&=(abs(xx-w*.5)<w*.25)&((yy<h*.76)if k<4 else(yy>h*.60))
 else:hot&=((abs(xx-w*.5)<w*.24)&(yy>h*.50))if k<5 else((xx<w*.44)&(yy>h*.4))
 hl,_=label(hot);ss=np.bincount(hl.ravel());ss[0]=0;assert ss.max()>10,('no head',unit,move,k);hy,hx=np.where(hl==ss.argmax());seed=[hx.mean(),hy.mean()]
 hy,hx=np.where(hot&(abs(xx-seed[0])<46)&(abs(yy-seed[1])<70));head=[float(hx.mean()),float(hy.mean())]
 feet=mask&(yy>h*.82)&(xx>w*.13)&(xx<w*.92)
 if head[1]>h*.60:feet&=~((abs(xx-head[0])<57)&(abs(yy-head[1])<85))
 fy,fx=np.where(feet);assert len(fx)>150,('boots',unit,move,k);root=[float((fx.min()+fx.max())/2),float(fy.max())]
 scale=.86; off=[round(256-root[0]*scale),round(FOOT-root[1]*scale)];f=Image.new('RGBA',(C,C));f.alpha_composite(Image.fromarray(a).resize((round(w*scale),round(h*scale)),Image.Resampling.NEAREST),off)
 ay,ax=np.where(np.array(f)[:,:,3]);assert ax.min()>0 and ay.min()>0 and ax.max()<511 and ay.max()<511,('export clips',unit,move,k)
 reg=mask&(abs(xx-head[0])<12)&(abs(yy-head[1])<83);ty,tx=np.where(reg);ix=np.argmax(ty);tip=[float(tx[ix]),float(ty[ix])]
 pos=lambda v:[round(off[0]+v[0]*scale),round(off[1]+v[1]*scale)]; tp=pos(tip);ix=np.argmin((ax-tp[0])**2+(ay-tp[1])**2);tp=[int(ax[ix]),int(ay[ix])]
 z=dict(source=f'{unit}-{move}',sourceCell=k,crop=box,scale=scale,root=root,tip=tp,headCenter=pos(head),grip=[256,265],bounds=[int(ax.min()),int(ay.min()),int(ax.max()+1),int(ay.max()+1)],wholeGenerated=True,faceForward=True,endCapLeads=True,rigidMetal=True,capAxis=[0,1],depth=1,direction='center',phase='behind-head'if move=='down'and k<3 else'contact'if move=='down'and k>=6 else'downstroke'if move=='down'else'recovery')
 imports.append(z);return f,z
def materials(name,sheet):
 base=np.array(sheet);r,g,b=[base[:,:,v].astype(float)for v in range(3)];hi=np.maximum.reduce([r,g,b]);lo=np.minimum.reduce([r,g,b]);opaque=base[:,:,3]>0
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
for unit,prefix in [('blue','blue'),('drac','corrupt')]:
 left=[oldpose(prefix,i)for i in range(32)]
 center=[oldpose(prefix,i)for i in range(17)]
 for k in range(1,8):center.append(imported(unit,'down',k))
 center.extend(imported(unit,'recovery',k)for k in range(8))
 for direction,frames in [('left',left),('center',center),('right',left)]:
  name=prefix+'-overhead'+(''if direction=='center'else'-'+direction);sheet=Image.new('RGBA',(2048,4096));folder=E/name;folder.mkdir(exist_ok=True);meta=[];pivot=[255,256]if direction=='right'else[256,256]
  for i,(original,z0)in enumerate(frames):
   f=original;z=copy.deepcopy(z0);z['direction']=direction
   if direction=='right':
    f=f.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    for key in ['tip','headCenter','grip']:z[key]=[511-z[key][0],z[key][1]]
    x0,y0,x1,y1=z['bounds'];z['bounds']=[512-x1,y0,512-x0,y1];z['mirroredFrom']=prefix+'-overhead-left';z['wholePoseMirror']=True
   alpha=np.array(f)[:,:,3];z['spans']=[np.flatnonzero(np.diff(np.r_[False,row>0,False])).tolist()for row in alpha];meta.append(z);sheet.alpha_composite(f,(i%4*C,i//4*C));f.save(folder/f'{i:02}.png')
  sheet.save(E/(name+'_regular.png'))
  if direction=='left':
   for mat in ['regular','chrome','red','hit','red_hit']:shutil.copy2(OLD/'exports'/(prefix+'-overhead_'+mat+'.webp'),E/(name+'_'+mat+'.webp'))
  else:materials(name,sheet)
  M[name]=dict(cell=[512,512],pivot=pivot,cols=4,count=32,folder='three_way_hammer_1111',meta=meta);jobs.append(dict(name=name,count=32,pivot=pivot));print('Exported',name,flush=True)
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')));(W/'aseprite-jobs.json').write_text(json.dumps(jobs))
(W/'front_hammer_art_1111.js').write_text("'use strict';\n/* Whole authored centered, approved-left and exact mirrored-right overheads. */\nObject.assign(BA119_ART,"+json.dumps(M,separators=(',',':'))+');\n')
(W/'audit.json').write_text(json.dumps(dict(imports=imports,newWholeDrawings=len(imports),retainedPeakDrawings=2,overheadTimelineFrames=192,mirroredFrames=64,scale=.86),indent=2))
print('Finished three directions for both characters, five material exports each.',flush=True)
