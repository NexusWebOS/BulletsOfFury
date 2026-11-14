from pathlib import Path
import json, math, subprocess, hashlib, shutil,sys
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw

W=Path(__file__).resolve().parent; E=W/'exports';E.mkdir(exist_ok=True)
O=(W/'preview')if W.parent.name=='_ART_SOURCES'else W.parents[1]/'outputs/Heavy-hammer-motion';O.mkdir(parents=True,exist_ok=True)
C=512;P=[256,256];FOOT=410
cache={};audit=[]
def source(name,k,rows=2,scale=.76):
 key=(name,k,rows,scale)
 if key in cache:return cache[key]
 path=W/'generated'/(name+'.png')
 if name.startswith('old-'):path=W.parent/'cap_strikes_1111/generated'/(name[4:]+'.png')
 im=Image.open(path).convert('RGBA');cw,ch=im.width/ (2 if name.startswith('old-')else 4),im.height/rows;cols=2 if name.startswith('old-')else 4
 box=(round(k%cols*cw),round(k//cols*ch),round((k%cols+1)*cw),round((k//cols+1)*ch))
 # Some complete poses cross an internal guide line into empty neighboring padding.
 # Recover the full connected drawing; no artwork is synthesized or repaired by cutting parts.
 if '-side-T' in name and k in [7,9]:box=(max(0,box[0]-20),box[1],min(im.width,box[2]+20),box[3])
 a=np.array(im.crop(box));m=a[:,:,3]>180
 labs,n=label(m);sizes=np.bincount(labs.ravel());sizes[0]=0;m=labs==sizes.argmax()
 assert m.any() and not(m[0].any()or m[-1].any()or m[:,0].any()or m[:,-1].any()),('clipped',name,k)
 # Import complete authored figure, discarding transparent RGB noise/disconnected dust only.
 a[:,:,3]=m*255;a[~m]=0;h,w=m.shape;yy,xx=np.indices(m.shape)
 feet=m&(yy>h*.83)
 if '-o2'in name and k>=6 or '-o3'in name and k<=4:feet&=xx<w*.70
 fl,fn=label(feet);candidates=[]
 for part in range(1,fn+1):
  py,px=np.where(fl==part)
  if len(px)>150 and px.max()-px.min()>w*.07:candidates.append((int(px.min()),part))
 candidates.sort()
 # The low contacting hammer is to the right of both boots. Identify both boot
 # components, rather than using the lowest hammer spike as the foot baseline.
 chosen=candidates[:2];assert len(chosen)>=1,('boot components',name,k,candidates)
 feet=np.isin(fl,[q[1]for q in chosen]);fy,fx=np.where(feet);sole=int(fy.max())
 root=[float((fx.min()+fx.max())/2),sole]
 r,g,b=[a[:,:,i].astype(float)for i in range(3)]
 # Weapon center is measured from the largest saturated lightning patch; the body inserts are smaller.
 hot=m&((r>140)&(b>165)&(b>g*1.8)&(r>g*1.6)if 'drac' in name else(b>170)&(b>r*1.8)&(b>g*1.15))
 if '-o0'in name or '-o1'in name:hot&=xx<w*.43
 if '-o2'in name:hot&=(yy<h*.39)if k<=5 else(xx>w*.68)
 if '-o3'in name:hot&=(xx>w*.65)if k<=4 else(xx<w*.4)
 hl,hn=label(hot);hs=np.bincount(hl.ravel());hs[0]=0;hm=hl==hs.argmax();hy,hx=np.where(hm)
 center=[float(hx.mean()),float(hy.mean())] if len(hx)else[w*.25,h*.6]
 # End-cap contact is an actual opaque pixel near the authored cylinder, not a synthetic offset.
 side='side' in name;region=m&(abs(xx-center[0])<(75 if side else 48))&(abs(yy-center[1])<(35 if side else 90))
 ry,rx=np.where(region)
 if side:
  near=abs(ry-center[1])<8;rx,ry=rx[near],ry[near];ix=np.argmin(rx)
 else:
  near=abs(rx-center[0])<8;rx,ry=rx[near],ry[near];ix=np.argmax(ry)
 tip=[float(rx[ix]),float(ry[ix])]
 clean=Image.fromarray(a);clean=clean.resize((round(w*scale),round(h*scale)),Image.Resampling.NEAREST)
 offset=[round(P[0]-root[0]*scale),round(FOOT-root[1]*scale)]
 frame=Image.new('RGBA',(C,C));frame.alpha_composite(clean,tuple(offset));aa=np.array(frame)[:,:,3];ay,ax=np.where(aa)
 assert ax.min()>0 and ay.min()>0 and ax.max()<C-1 and ay.max()<C-1,('export clips',name,k)
 pos=lambda v:[round(offset[0]+v[0]*scale),round(offset[1]+v[1]*scale)]
 tp=pos(tip);ay,ax=np.where(aa>0);j=np.argmin((ax-tp[0])**2+(ay-tp[1])**2);tp=[int(ax[j]),int(ay[j])]
 z=dict(source=name,sourceCell=k,input=str(path),crop=list(box),scale=scale,root=root,tip=tp,headCenter=pos(center),grip=[P[0],FOOT-145],bounds=[int(ax.min()),int(ay.min()),int(ax.max()+1),int(ay.max()+1)],wholeGenerated=True,faceForward=not 'whirl'in name,endCapLeads=True,depth=1,capAxis=[-1,0]if side else[0,1])
 cache[key]=(frame,z);audit.append(z);return frame,z

banks={};spec=[]
for unit,prefix in [('drac','corrupt'),('blue','blue')]:
 over=[]
 for group in range(4):
  for i in range(8):
   name=f'guided-{unit}-o{group}';scale=[.76,.91,.91,.76][group]
   if unit=='drac'and group==1:name+='-alpha'
   if unit=='drac'and group==3:name+='-grip'if i>=5 else''
   if unit=='blue'and group==3:name+='-rejected'if i>=5 else'-right'
   # A deliberate contact hold keeps the end cap planted before the rebound.
   # The rejected second contact drawing slides the head along the floor.
   f,z=source(name,6 if group==2 and i==7 else i,scale=scale);z=dict(z,phase='behind-head'if 14<=group*8+i<=19 else'contact'if group*8+i in[22,23]else'downstroke'if 20<=group*8+i<22 else'recovery'if group==3 else'load')
   over.append((f,z))
 sides=[]
 for i in range(16):
  f,z=source(unit+'-side-T',7 if i==8 else i,4,1.02)
  sides.append((f,dict(z,phase='contact'if 5<=i<=8 else'recovery'if i>8 else'load',capAxis=[-1,0])))
 whirl=[(f,dict(z,phase='whirl',faceForward=False))for f,z in[source(unit+'-whirl',i,4,1.02)for i in range(16)]]
 for suffix,frames in [('overhead',over),('sides',sides),('right',sides),('whirl',whirl)]:
  name=prefix+'-'+suffix;sheet=Image.new('RGBA',(C*4,C*math.ceil(len(frames)/4)));meta=[];fs=[];folder=E/name;folder.mkdir(exist_ok=True)
  for i,(f,z0)in enumerate(frames):
   z=dict(z0)
   if suffix=='right':
    f=f.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    for key in ['tip','headCenter','grip']:z[key]=[C-1-z[key][0],z[key][1]]
    x0,y0,x1,y1=z['bounds'];z['bounds']=[C-x1,y0,C-x0,y1];z['capAxis']=[1,0];z['mirror']=True
   alpha=np.array(f)[:,:,3];z['spans']=[np.flatnonzero(np.diff(np.r_[False,row>0,False])).tolist()for row in alpha]
   sheet.alpha_composite(f,(i%4*C,i//4*C));f.save(folder/f'{i:02}.png');meta.append(z)
   out=Image.new('RGBA',(C,C),'#101820');out.alpha_composite(f);fs.append(out.convert('RGB'))
  sheet.save(E/(name+'_regular.png'))
  base=np.array(sheet);r,g,b=[base[:,:,k].astype(float)for k in range(3)];hi=np.maximum.reduce([r,g,b]);lo=np.minimum.reduce([r,g,b]);opaque=base[:,:,3]>0
  for mat in ([] if '--metadata-only' in sys.argv else ['regular','chrome','red','hit','red_hit']):
   out=base.copy();rr,gg,bb=r.copy(),g.copy(),b.copy()
   if mat in ['hit','red_hit']:rr[opaque]=255;gg[opaque]=255 if mat=='hit' else 35;bb[opaque]=255 if mat=='hit' else 42
   elif mat=='chrome':
    m=opaque&(hi-lo<65)&(hi>30);v=np.minimum(255,hi*1.4+9);rr[m]=v[m];gg[m]=v[m];bb[m]=np.minimum(255,v[m]+5)
   elif mat=='red':
    m=opaque&(b>g*1.4)&((b>r*1.15)|(r>g*1.4))&(b>115);v=np.maximum(r,b);rr[m]=np.minimum(255,v[m]*1.1);gg[m]=v[m]*.12;bb[m]=v[m]*.18
    m=opaque&~m&(hi>40)&(hi-lo<65);rr[m]=np.minimum(255,hi[m]*1.2);gg[m]=g[m]*.48;bb[m]=b[m]*.52
   for k,v in enumerate([rr,gg,bb]):out[:,:,k]=np.floor(v).astype(np.uint8)
   Image.fromarray(out).save(E/(name+'_'+mat+'.webp'),lossless=True,method=1)
  banks[name]=dict(cell=[C,C],pivot=P,cols=4,count=len(frames),folder='heavy_hammer_1111',meta=meta)
  spec.append(dict(name=name,count=len(frames)))
  durations=[55]*len(fs)
  if suffix=='overhead':durations=[30]*8+[55]*8+[60,55,45,40,35,30,100,65]+[50]*8
  fs[0].save(O/(name+'.gif'),save_all=True,append_images=fs[1:],duration=durations,loop=0,disposal=2)
  board=Image.new('RGB',(C*4,C*math.ceil(len(fs)/4)),'#101820');d=ImageDraw.Draw(board)
  for i,f in enumerate(fs):board.paste(f,(i%4*C,i//4*C));d.text((i%4*C+10,i//4*C+10),str(i),fill='white')
  board.save(O/(name+'-poses.png'))
  print(name,len(fs),'complete timeline drawings',flush=True)
(W/'manifest.json').write_text(json.dumps(banks,separators=(',',':')))
(W/'heavy_hammer_art_1111.js').write_text("'use strict';\n/* Reference-led complete held hammer motion. */\nObject.assign(BA119_ART,"+json.dumps(banks,separators=(',',':'))+');\n')
(W/'aseprite-jobs.json').write_text(json.dumps(spec))
(W/'audit.json').write_text(json.dumps(dict(imports=audit,uniqueCompleteSources=len(cache),cell=C,pivot=P,foot=FOOT,normalization='Direct original-master nearest import, one uniform model-unit calibration per source sheet, whole-pose boot registration; no per-frame fitting or body assembly.'),indent=2))
print('Prepared',sum(a['count']for a in banks.values()),'cells from',len(cache),'distinct complete source drawings.',flush=True)
