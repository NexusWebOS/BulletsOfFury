"""New authored Stage6 strategic carriers, doors, warheads and hazard graphics.
Retain original generation outputs. Normalize with shared even canvases/pivots;
export direction cells offline, never substitute live sprite rotation.
"""
from pathlib import Path
import json,shutil,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,maximum_filter
R=Path(__file__).resolve().parents[1];S=R/'_BUILD_SOURCE/carrier_assault_1101';O=R/'assets/game/levels/stage_06/enemies/carrier_assault_1101';Q=R/'_shots/carrier_assault_1101'
for p in[S,O,Q]:p.mkdir(parents=True,exist_ok=True)
G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
FILES={'nuclear_hull':'exec-ffb83dfc-470e-4942-9ba8-eadc43c5b5c5.png','laser_hull':'exec-074768db-832b-4894-a5f1-1287f74c979e.png','nuclear_door':'exec-fa2ff221-4735-4fd4-ab11-5f05ac210d9b.png','laser_door':'exec-50ae0644-5274-440b-aafc-d503f982846b.png','nuclear_head':'exec-3a73314f-ae1d-4684-8a72-97cffd76b66f.png','laser_head':'exec-347cd693-39d0-434f-a0b8-3a78a18969fe.png','exhaust':'exec-bd945919-b00c-41a1-83a0-505e27b3386e.png','nuclear_blast':'exec-b5c3996c-792d-49bc-b340-f2e06fc20e50.png','laser_tornado':'exec-1a212600-2c2b-4841-a1e5-d60036ed5ddc.png','laser_ray':'exec-41b23f2f-8949-4a8d-967a-77756c70d0cf.png'}
M={'owner':'_BUILD_SOURCE/build_carrier_assault_1101.py','sources':{},'banks':{},'models':{}};previews=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n):
 p=S/(n+'_source.png')
 if not p.exists():shutil.copyfile(G/FILES[n],p)
 im=Image.open(p).convert('RGBA');M['sources'][n]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'size':im.size,'tool':'built-in image_gen','original':FILES[n]};return im
def clean(im,solid=True):
 a=np.array(im);a[:,:,3]=np.where(a[:,:,3]>(180 if solid else 45),a[:,:,3],0)
 if solid:
  ids,_=label(a[:,:,3]>0);sizes=np.bincount(ids.ravel());sizes[0]=0;a[ids!=sizes.argmax(),3]=0;a[:,:,3]=np.where(a[:,:,3]>0,255,0)
 return Image.fromarray(a)
def light(im,warm=False):
 a=np.array(im);r=a[:,:,:3].astype(float);emit=(a[:,:,3]>80)&((r[:,:,0]>100)&(r[:,:,0]>r[:,:,2]*1.3)if warm else(r[:,:,2]>90)&(r[:,:,2]>r[:,:,0]*1.25)&(r[:,:,1]>65));z=np.zeros_like(a);z[:,:,:3]=[255,175,55]if warm else[65,195,255];z[:,:,3]=np.where(emit,180,np.where(maximum_filter(emit,3),55,0));return Image.fromarray(z)
def save(n,frames,cw,ch,dirs=1,extra=None):
 assert cw%2==ch%2==0
 out=Image.new('RGBA',(cw*dirs,ch*len(frames)))
 for i,f in enumerate(frames):
  assert f.size==(cw,ch)
  for d in range(dirs):out.alpha_composite(f.rotate(-d*360/dirs,Image.Resampling.NEAREST)if d else f,(d*cw,i*ch))
 p=O/(n+'.webp');out.save(p,format='WEBP',lossless=True,method=4);b={'key':'ca111_'+n,'path':p.relative_to(R).as_posix(),'cw':cw,'ch':ch,'cell':cw if cw==ch else None,'cols':dirs,'dirs':dirs,'frames':len(frames),'sha256':sha(p),**(extra or{})};M['banks'][n]=b
 previews.append((n,frames));return b
def slices(n,cols,rows,solid=True):
 im=load(n);fs=[];rects=[]
 for y in range(rows):
  for x in range(cols):
   box=[round(x*im.width/cols),round(y*im.height/rows),round((x+1)*im.width/cols),round((y+1)*im.height/rows)];f=im.crop(box)
   if not solid:
    a=np.array(f);a[:3,:,3]=a[-3:,:,3]=a[:,:3,3]=a[:,-3:,3]=0;f=Image.fromarray(a)
   fs.append(clean(f,solid));rects.append(box)
 M['sources'][n]['cells']=rects;return fs
def normalize(fs,w,h,margin=16,pivots=None,anchor=None):
 pivots=pivots or[[(b[0]+b[2])/2,(b[1]+b[3])/2]for b in[f.getbbox()for f in fs]];anchor=anchor or[w/2,h/2]
 k=min(min((anchor[0]-margin)/max(1,p[0]-b[0]),(w-anchor[0]-margin)/max(1,b[2]-p[0]),(anchor[1]-margin)/max(1,p[1]-b[1]),(h-anchor[1]-margin)/max(1,b[3]-p[1]))for f,p in zip(fs,pivots)for b in[f.getbbox()])
 out=[]
 for f,p in zip(fs,pivots):
  z=f.resize((round(f.width*k),round(f.height*k)),Image.Resampling.NEAREST);t=Image.new('RGBA',(w,h));t.alpha_composite(z,(round(anchor[0]-p[0]*k),round(anchor[1]-p[1]*k)));out.append(t)
 return out,k,pivots
for n in['nuclear','laser']:
 src=clean(load(n+'_hull'));fs,k,p=normalize([src],512,512,16);save(n+'_hull',fs,512,512);save(n+'_hull_glow',[light(fs[0],n=='nuclear')],512,512)
 def pt(x,y):return[round(256+(x-p[0][0])*k,3),round(256+(y-p[0][1])*k,3)]
 raw={'nuclear':{'bay':[626,615],'engines':[[451,1210],[560,1210],[685,1210],[805,1210]],'door':[132,270]},'laser':{'bay':[626,690],'engines':[[384,1137],[520,1160],[668,1160],[805,1137]],'door':[132,132]}}[n]
 M['models'][n]={'worldSize':470 if n=='nuclear'else 460,'hull':n+'_hull','glow':n+'_hull_glow','bay':pt(*raw['bay']),'engines':[pt(*q)for q in raw['engines']],'doorWorld':raw['door'],'sourcePivot':p[0],'commonScale':k,'bounds':list(fs[0].getbbox())}
 fs=slices(n+'_door',4,2);w,h=(256,512)if n=='nuclear'else(256,256);ds,k,p=normalize(fs,w,h,16);save(n+'_door',ds,w,h,extra={'sourcePivots':p,'commonScale':k});M['models'][n]['door']=n+'_door'
 fs=slices(n+'_head',4,2);hs,k,p=normalize(fs,256,256,24)
 if n=='nuclear':hs=[f.transpose(Image.Transpose.ROTATE_180)for f in hs]
 sockets=[]
 for f in hs:
  a=np.array(f);blue=(a[:,:,3]>150)&(a[:,:,2]>130)&(a[:,:,1]>100)&(a[:,:,0]<210);yy,xx=np.indices(blue.shape);ids,_=label(blue&(yy>60)&(yy<180)&((xx<105)|(xx>150)));ss=[]
  for j in range(1,ids.max()+1):
   y,x=np.nonzero(ids==j)
   if len(x)>6:ss.append([float(x.mean()),float(y.mean())])
  ss=[min(ss,key=lambda p:(p[0]-v[0])**2+(p[1]-v[1])**2)for v in[[92,99],[163,99],[92,138],[163,138]]]if ss else[];sockets.append(ss)
 save(n+'_head',hs,256,256,32 if n=='nuclear'else 8,{'sourcePivots':p,'commonScale':k,'tail':[128,32],'sockets':sockets})
fs=slices('exhaust',4,2,False);p=[]
for f in fs:
 a=np.array(f);yy,xx=np.nonzero(a[:,:,3]>100);top=yy.min();xs=np.nonzero(a[top:top+15,:,3]>120)[1];p.append([float(np.median(xs)),float(top)])
es,k,p=normalize(fs,256,256,16,p,[128,24]);save('exhaust',es,256,256,8,{'mount':[128,24],'commonScale':k,'sourcePivots':p})
warm=[]
for f in es:
 a=np.array(f);rgb=a[:,:,:3].astype(float);lum=np.max(rgb,axis=2);a[:,:,0]=np.minimum(255,lum*1.1);a[:,:,1]=np.where(lum>230,lum*.96,lum*.54);a[:,:,2]=np.where(lum>230,lum*.77,lum*.08);warm.append(Image.fromarray(a))
save('exhaust_amber',warm,256,256,8,{'mount':[128,24],'derivedFrom':'exhaust','palette':'amber-white; unchanged alpha/luminance maxima'})
for n,rows in[('nuclear_blast',2),('laser_tornado',3)]:
 fs=slices(n,4,rows,False);p=[]
 for i,f in enumerate(fs):
  a=np.array(f)
  if n=='laser_tornado':
   mask=(a[:,:,3]>140)&(a[:,:,0]>225)&(a[:,:,1]>230)&(a[:,:,2]>230);yy,xx=np.nonzero(mask);p.append([float(np.median(xx)),float(np.median(yy))]if len(xx)>4 else[f.width/2,f.height*.46])
  else:p.append([f.width/2,f.height/2])
 bs,k,p=normalize(fs,256,256,16,p);radii=[]
 for f in bs:
  a=np.array(f);yy,xx=np.nonzero((a[:,:,3]>150)&(a[:,:,:3].max(axis=2)>190));radii.append(round(float(np.quantile(np.hypot(xx-128,yy-128),.8)),2))
 save(n,bs,256,256,extra={'sourcePivots':p,'commonScale':k,'visibleRadii':radii})
fs=slices('laser_ray',4,2,False);rs=[]
for f in fs:
 # Keep the repeated beam section at full cell height; no independent x/y fit.
 k=64/f.height;z=f.resize((round(f.width*k),64),Image.Resampling.NEAREST);t=Image.new('RGBA',(64,64));t.alpha_composite(z,(round(32-z.width/2),0));rs.append(t)
save('laser_ray',rs,64,64,8,{'alphaWidth':28,'mount':[32,0],'segmentStep':.70})
for n,fs in previews:
 # One compact inspection plate per bank; full generated originals are retained.
 if 'glow'in n or n=='exhaust_amber':continue
 w=128;h=round(w*fs[0].height/fs[0].width);cols=min(4,len(fs));rows=math.ceil(len(fs)/cols);out=Image.new('RGB',(w*cols,(h+18)*rows),(8,20,32));d=ImageDraw.Draw(out)
 for i,f in enumerate(fs):
  t=f.resize((w,h),Image.Resampling.NEAREST);x=i%cols*w;y=i//cols*(h+18);out.paste(t,(x,y+18),t);d.text((x+4,y+2),str(i),fill='white')
 out.save(Q/(n+'-contact.png'))
(O/'manifest.json').write_text(json.dumps(M,indent=2)+'\n',encoding='utf-8');(R/'assets/carrier_assault_art_1101.js').write_text('"use strict";\nconst CA111_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print('Built',len(M['sources']),'new generated source assets;',len(M['banks']),'registered even-cell banks')
