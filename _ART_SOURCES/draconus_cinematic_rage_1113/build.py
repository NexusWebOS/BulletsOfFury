from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage
import numpy as np,json,hashlib
W=Path(__file__).resolve().parent;E=W/'exports';E.mkdir(exist_ok=True);C=512
M={};audit=[]

def import_bank(name,file):
 im=Image.open(W/'generated'/file).convert('RGBA');frames=[]
 for i in range(16):
  box=[round(i%4*im.width/4),round(i//4*im.height/4),round((i%4+1)*im.width/4),round((i//4+1)*im.height/4)]
  a=np.array(im.crop(box));mask=a[:,:,3]>=128
  labels,count=ndimage.label(mask,np.ones((3,3)))
  sizes=np.bincount(labels.ravel());sizes[0]=0;keep=labels==sizes.argmax()
  # Remove only detached background residue, never redraw or assemble the actor.
  a[:,:,3]=np.where(keep,255,0).astype('uint8');a[a[:,:,3]==0,:3]=0
  f=Image.new('RGBA',(C,C));f.paste(Image.fromarray(a),(100,110))
  frames.append(f);audit.append(dict(bank=name,source=i,crop=box,offset=[100,110],scale=1,opaque=int(keep.sum()),removedBackground=int((mask&~keep).sum())))
 return frames

raw={n:import_bank(n,f)for n,f in [('rage','rage.png'),('cast','cast-clean.png'),('recoup','recoup.png'),('center','center-clean.png')]}

def recolor(im,to):
 a=np.array(im);r,g,b=[a[:,:,i].astype(float)for i in range(3)];hi=np.maximum.reduce([r,g,b]);lo=np.minimum.reduce([r,g,b]);yy,xx=np.indices(r.shape)
 if to=='chrome':
  red=(r>g*1.38)&(r>b*1.18)&(r>35)&(a[:,:,3]>0)
  # The sternum/abdomen keep their identity color while the metal changes.
  red&=~((abs(xx-256)<25)&(yy>195)&(yy<335))
  v=np.minimum(255,(r*.299+g*.587+b*.114)*1.65+9)
  for i in range(3):a[:,:,i][red]=v[red].astype('uint8')
 elif to=='regular':
  gray=(hi-lo<45)&(hi>26)&(a[:,:,3]>0)
  gray&=~((abs(xx-256)<20)&(yy>180)&(yy<265))
  for i,factor in enumerate([.83,.43,.88]):a[:,:,i][gray]=(hi[gray]*factor).astype('uint8')
 elif to=='hit':a[a[:,:,3]>0,:3]=255
 return Image.fromarray(a)

def meta(im,**extra):
 a=np.array(im)[:,:,3];yy,xx=np.where(a>0)
 return dict(bounds=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],
  spans=[np.flatnonzero(np.diff(np.r_[False,row>0,False])).tolist()for row in a],wholeGenerated=True,faceForward=True,**extra)

def export(name,frames,metadata=None,cell=512,pivot=None):
 folder=E/name;folder.mkdir(exist_ok=True);sheet=Image.new('RGBA',(cell*4,cell*((len(frames)+3)//4)))
 for i,f in enumerate(frames):sheet.paste(f,(i%4*cell,i//4*cell));f.save(folder/f'{i:02}.png')
 sheet.save(E/(name+'.webp'),lossless=True,method=1);sheet.save(E/(name+'.png'))
 M[name]=dict(cw=cell,ch=cell,cols=4,count=len(frames),pivot=pivot or[cell//2,cell//2],meta=metadata or[meta(f)for f in frames])
 return sheet

# Sixteen actual new transformation poses and hard material steps,32 timeline cells.
for mat in ['red','chrome','hit']:
 frames=[recolor(f,mat)if mat!='red'else f for f in raw['rage']]
 export('rage_'+mat,frames)
formation=[];formation_meta=[]
for i in range(32):
 f=min(15,i//2);u=.30+i/31*.70;red=np.array(raw['rage'][f]);plain=np.array(recolor(raw['rage'][f],'chrome'))
 step=0 if u<.38 else min(6,int((u-.38)/.42*6));k=step/6
 out=plain.copy();out[:,:,:3]=np.round(plain[:,:,:3]*(1-k)+red[:,:,:3]*k).astype('uint8')
 formation.append(Image.fromarray(out));formation_meta.append(meta(formation[-1],sourceCell=f,redStep=step,transformationU=u))
export('formation',formation,formation_meta);export('formation_hit',[recolor(f,'hit')for f in formation])
export('recoup',raw['recoup']);export('recoup_hit',[recolor(f,'hit')for f in raw['recoup']])

# Both hands meet at a real measured gap during gather, then thrust together.
ball_source=[[156,195],[119,195],[120,204],[113,197],[91,194],[98,192],[96,198],[104,199],[122,211],[157,205],[158,193],[158,189],[157,187],[157,191],[158,198],[156,194]]
for depth,cell in [('fore',512),('back',224)]:
 scale=cell/512;frames=[f if cell==512 else f.resize((cell,cell),Image.Resampling.NEAREST)for f in raw['cast']]
 rows=[meta(f,ball=[round((p[0]+100)*scale),round((p[1]+110)*scale)],palms=[[round((p[0]+100-12)*scale),round((p[1]+110)*scale)],[round((p[0]+100+12)*scale),round((p[1]+110)*scale)]],sourceCell=i,depth=1 if depth=='fore'else.42)for i,(f,p)in enumerate(zip(frames,ball_source))]
 export('cast_'+depth,frames,rows,cell);export('cast_'+depth+'_hit',[recolor(f,'hit')for f in frames],rows,cell)

# Align lift/down/contact/rebound with the existing32-cell native overhead clock.
# Rejected source13 has a duplicate weapon; it is never exported or selected.
order=[0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,12,12,10,9,8,5,4,14,15]
heads=[[60,205],[60,213],[95,190],[74,157],[62,102],[78,65],[157,31],[157,31],[157,50],[157,106],[157,252],[157,275],[157,278],[0,0],[65,218],[65,218]]
center_meta=[]
for i,src in enumerate(order):
 im=raw['center'][src];h=[heads[src][0]+100,heads[src][1]+110]
 mask=np.array(im)[:,:,3]>0;yy,xx=np.indices(mask.shape)
 region=mask&(abs(xx-h[0])<26)&(abs(yy-h[1])<38)
 ys,xs=np.where(region);bottom=int(ys.max());choices=np.where(ys==bottom)[0];j=choices[np.argmin(abs(xs[choices]-h[0]))]
 tip=[int(xs[j]),bottom]
 if 16<=i<=24:assert abs(tip[0]-256)<12,('centerline',i,tip)
 center_meta.append(meta(im,sourceCell=src,tip=tip,headCenter=h,grip=[256,315],root=[256,410],rigidMetal=True,endCapLeads=True,capAxis=[0,1],direction='center',phase='contact'if i in[22,23,24]else'downstroke'if i>=16 and i<22 else'recovery'if i>24 else'behind-head'if i>=12 else'lift'))
for mat in ['chrome','regular','red','hit','red_hit']:
 frames=[]
 for src in order:
  f=raw['center'][src]
  if mat=='regular':f=recolor(f,'regular')
  elif mat in ['hit','red_hit']:f=recolor(f,'hit')
  elif mat=='red':
   a=np.array(f);r,g,b=[a[:,:,i].astype(float)for i in range(3)];hi=np.maximum.reduce([r,g,b]);gray=(hi-np.minimum.reduce([r,g,b])<45)&(hi>30)&(a[:,:,3]>0)
   for ch,k in enumerate([1,.31,.32]):a[:,:,ch][gray]=(hi[gray]*k).astype('uint8')
   f=Image.fromarray(a)
  frames.append(f)
 export('center_'+mat,frames,center_meta)

# Review at actual detail size without enlarging reduced derivatives.
board=Image.new('RGB',(8*320,8*340),'#15232c');draw=ImageDraw.Draw(board)
for row,(name,frames)in enumerate([('new rage',raw['rage']),('new cast',raw['cast']),('STOP / recoup',raw['recoup']),('center Chromium',[raw['center'][s]for s in order[::2]])]):
 for j,f in enumerate(frames):
  x=j%8;y=row*2+j//8;crop=f.crop((96,100,416,440));board.paste(crop,(x*320,y*340),crop);draw.text((x*320+4,y*340+4),name+' '+str(j),fill='white')
board.save(W/'new-frames-review.png')
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')))
(W/'import-audit.json').write_text(json.dumps(dict(imports=audit,rejectedCenterSource=13,newUsableWholeDrawings=63,frameScale=1,frameCell=[512,512],pivot=[256,256],baseline=410),indent=2))
(W/'draconus_cinematic_rage_art_1113.js').write_text("'use strict';\nconst DCR13_ART="+json.dumps(M,separators=(',',':'))+';\n')
print('Built new full-body banks, clean binary actor alpha, matching hit art and registered ground-cap/ball sockets.',flush=True)
