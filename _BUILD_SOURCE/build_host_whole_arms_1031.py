from pathlib import Path
import json,math,hashlib,subprocess
from collections import deque
import numpy as np
from PIL import Image,ImageFilter,ImageChops,ImageDraw
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/host_whole_arms_1031';W.mkdir(parents=True,exist_ok=True);D=R/'assets/game/levels/stage_08/boss/whole_arms_ball_1031';D.mkdir(parents=True,exist_ok=True)
M=json.loads((R/'assets/game/levels/stage_08/boss/possession_1030/manifest.json').read_text());E=json.loads((R/'assets/encounter_revision_art_1023.js').read_text().split('const ER23_ART=',1)[1].strip().rstrip(';'));C=dict(host=M,roll=E['banks']['roll']);P=512;O=256;manifest={};inputs={};cache={}
def cell(a,f):
 path=a['path'];inputs[path]=hashlib.sha256((R/path).read_bytes()).hexdigest()
 key=(path,f)
 if key not in cache:
  im=Image.open(R/path).convert('RGBA');w=a.get('cw',a.get('w'));h=a.get('ch',a.get('h'));cols=a['cols'];cache[key]=im.crop((f%cols*w,f//cols*h,(f%cols+1)*w,(f//cols+1)*h))
 return cache[key].copy()
def pose(side,f):
 im=cell(M['host_dracodia_wind_'+side],f)
 # The original inset-tube patch remains attached to this same source arm.
 T=json.loads((R/'assets/game/levels/stage_08/boss/claw_laser_1030/manifest.json').read_text())['turret_dracodia_wind_'+side]
 patch=cell(T,f);x,y=T['anchors'][f];im.alpha_composite(patch,(round(180+x-T['pivot'][0]),round(180+y-T['pivot'][1])))
 return im
def blank():return Image.new('RGBA',(P,P))
def tx(im,pivot,dest,angle=0,sx=1,sy=None):
 sy=sx if sy is None else sy;c,s=math.cos(angle),math.sin(angle);px,py=pivot;dx,dy=dest
 return im.transform((P,P),Image.Transform.AFFINE,(c/sx,s/sx,px-(dx*c+dy*s)/sx,-s/sy,c/sy,py+(dx*s-dy*c)/sy),Image.Resampling.NEAREST)
def point(p,piv,dest,a=0,sx=1,sy=None):
 sy=sx if sy is None else sy;x=(p[0]-piv[0])*sx;y=(p[1]-piv[1])*sy;c,s=math.cos(a),math.sin(a);return [dest[0]+x*c-y*s,dest[1]+x*s+y*c]
def body(im,sign,lean):return tx(im,(O,O),(O,O),sign*math.radians(4)*lean)
def bodypoint(p,sign,lean):return point(p,(O,O),(O,O),sign*math.radians(4)*lean)
def hand(im):
 al=np.asarray(im)[:,:,3];ys,xs=np.where(al>100);bottom=int(np.percentile(ys,98));take=(ys>bottom-37)&(ys<=bottom);return [float(np.median(xs[take])),bottom-14]
def grip(im,h,g):
 if g<=0:return im
 out=Image.new('RGBA',im.size);hx,hy=h
 for y in range(im.height):
  for x in range(im.width):
   v=im.getpixel((x,y))
   if not v[3]:continue
   shift=round(g*(1 if x<hx-4 else -1 if x>hx+4 else 0))if y>hy-14 and abs(x-hx)<43 else 0
   if 0<=x+shift<im.width:out.putpixel((x+shift,y),v)
 return out
def spans(im):
 a=np.asarray(im)[:,:,3]>64;result=[]
 for row in a:
  z=np.flatnonzero(np.diff(np.concatenate(([False],row,[False])).astype(np.int8)));result.append(z.tolist())
 return result
def register(name,frames,meta=None,hit=True,collision=None):
 bounds=[f.getbbox()for f in frames if f.getbbox()];l=max(0,min(b[0]for b in bounds)-8);t=max(0,min(b[1]for b in bounds)-8);r=min(P,max(b[2]for b in bounds)+8);bot=min(P,max(b[3]for b in bounds)+8)
 w=math.ceil((r-l)/2)*2;h=math.ceil((bot-t)/2)*2;cols=8;sheet=Image.new('RGBA',(w*cols,h*math.ceil(len(frames)/cols)))
 rows=[]
 for i,im in enumerate(frames):
  crop=im.crop((l,t,l+w,t+h));sheet.alpha_composite(crop,(i%cols*w,i//cols*h))
  rows.append(spans((collision[i]if collision else im).crop((l,t,l+w,t+h))))
 sheet.save(D/(name+'.png'));a=dict(key='rd96_'+name,path='assets/game/levels/stage_08/boss/whole_arms_ball_1031/'+name+'.png',cw=w,ch=h,cols=cols,frames=len(frames),pivot=[O-l,O-t],fps=30,spans=rows)
 if meta:a['poses']=meta
 a['sha256']=hashlib.sha256((D/(name+'.png')).read_bytes()).hexdigest();manifest[name]=a
 if hit:
  white=[]
  for im in frames:
   q=Image.new('RGBA',im.size,(255,255,255,0));q.putalpha(im.getchannel('A'));white.append(q)
  sh=Image.new('RGBA',sheet.size)
  for i,im in enumerate(white):sh.alpha_composite(im.crop((l,t,l+w,t+h)),(i%cols*w,i//cols*h))
  sh.save(D/(name+'_hit.png'));manifest[name+'_hit']={k:v for k,v in a.items()if k not in ['spans','poses']};manifest[name+'_hit'].update(key=a['key']+'_hit',path=a['path'].replace('.png','_hit.png'),sha256=hashlib.sha256((D/(name+'_hit.png')).read_bytes()).hexdigest())
def smooth(t):return t*t*(3-2*t)
for side,sign in [('left',-1),('right',1)]:
 root=(96,128)if side=='left'else(264,128);frames=[];metadata=[]
 for i in range(64):
  if i<16:u=i/15;srcf=round(u*8);angle=-sign*12*u;lean=u;g=0
  elif i<28:u=(i-16)/11;srcf=round((1-u)*8);angle=(-sign*12)*(1-u)+sign*18*u;lean=1;g=0
  elif i<32:u=(i-28)/3;srcf=0;angle=sign*(18+14*u);lean=1;g=3*u
  elif i<48:u=(i-32)/15;srcf=0;angle=sign*32*(1-smooth(u));lean=1-smooth(u);g=3*(1-u)
  elif i<56:u=(i-48)/7;srcf=round(u*8);angle=sign*(32-40*u);lean=1;g=3
  else:u=(i-56)/7;srcf=round((1-u)*8);angle=-sign*8*(1-u);lean=1-smooth(u);g=3*(1-u)
  im=pose(side,srcf);h=hand(im);im=grip(im,h,g);a=math.radians(angle);dest=(root[0]+76,root[1]+76);out=body(tx(im,root,dest,a),sign,lean)
  h=bodypoint(point(h,root,dest,a),sign,lean);rt=bodypoint(dest,sign,lean);el=bodypoint(point((root[0],215),root,dest,a),sign,lean)
  metadata.append(dict(lean=round(lean*15),tip=[round(h[0]-O,2),round(h[1]-O,2)],root=[round(rt[0]-O,2),round(rt[1]-O,2)],elbow=[round(el[0]-O,2),round(el[1]-O,2)],sourceFrame=srcf,angle=angle,grip=g));frames.append(out)
 register('arm_'+side,frames,metadata)
 for name in ['core','passive']:
  src=cell(M['host_dracodia_wind_core'],0)if name=='core'else pose('right'if side=='left'else'left',0)
  frames=[]
  for i in range(16):
   im=blank();im.alpha_composite(src,(76,76));frames.append(body(im,sign,i/15))
  register(name+'_'+side,frames)
# Armless torso stays complete. The same source begins the authored shell-closing reel.
core=cell(M['host_dracodia_wind_core'],0);armless=blank();armless.alpha_composite(core,(76,76));register('armless',[armless])
roll=C['roll'];candidates=[]
for f in range(roll['count']):
 im=cell(roll,f);a=np.asarray(im);mask=(a[:,:,0]>190)&(a[:,:,0]>a[:,:,1]*1.8)&(a[:,:,0]>a[:,:,2]*1.3)&(a[:,:,3]>64);yy,xx=np.where(mask);score=(float(np.mean(xx))-128)**2+(float(np.mean(yy))-128)**2 if len(xx)else 1e9;candidates.append((len(xx),score,f))
bright=max(q[0]for q in candidates);ballIndex=min((q for q in candidates if q[0]>=bright*.72),key=lambda q:q[1])[2];ball=cell(roll,ballIndex);fold=[];coll=[]
sectors=[]
for n in range(3):
 a=np.asarray(ball).copy();yy,xx=np.indices(a.shape[:2]);width=24+abs(yy-128)*.18+np.sin(yy*.055)*4;labels=np.where(xx<128-width,0,np.where(xx>128+width,2,1));a[labels!=n]=0;sectors.append(Image.fromarray(a))
for i in range(40):
 u=i/39;im=blank();sil=blank();closing=smooth(max(0,min(1,(u-.26)/.70)));curl=smooth(max(0,min(1,(u-.12)/.75)))
 # Rigid source shell sectors swing inward and enclose the complete torso.
 def shell(front):
  for j,s in enumerate(sectors):
   if (j==1)!=front:continue
   sign=j-1;spread=(1-closing)*35;dest=(O+sign*spread,O-abs(sign)*(1-closing)*12);z=tx(s,(128,128),dest,sign*(1-closing)*.55)
   im.alpha_composite(z);sil.alpha_composite(z)
 if u>.26:shell(False)
 if u<.92:
  torso=tx(core,(180,180),(O+curl*4,O),math.radians(22)*curl,1-.20*curl,1-.38*curl)
  im.alpha_composite(torso);sil.alpha_composite(torso)
 if u>.68:shell(True)
 if u>.28 and u<.94:
  k=math.floor(u*47)%48
  for layer in ['helix_front']:
   code=cell(M[layer],k);code.putalpha(code.getchannel('A').point(lambda a:round(a*.55)));code=tx(code,(192,192),(O,O),u*math.tau,.72-.18*closing,.78-.25*closing);im.alpha_composite(code)
 if i==0:im=armless.copy();sil=armless.copy()
 if i>=38:im=blank();im.alpha_composite(ball,(O-128,O-128));sil=im.copy()
 # Authored material pulse uses only source-alpha outlines, before final solid ball.
 if 25<=i<=36 and i%3==1:
  al=im.getchannel('A');edge=ImageChops.subtract(al.filter(ImageFilter.MaxFilter(5)),al);glow=Image.new('RGBA',im.size,(205,25,255,0));glow.putalpha(edge);glow.alpha_composite(im);im=glow
 fold.append(im);coll.append(sil)
register('fold',fold,hit=True,collision=coll)
manifest['fold']['ballStartFrame']=ballIndex
(D/'manifest.json').write_text(json.dumps(manifest,separators=(',',':')));(D/'inputs.json').write_text(json.dumps(inputs,indent=2));(D/'provenance.json').write_text(json.dumps(dict(method='Whole original RD71 arm poses with fixed shoulder pivots; offline Aseprite/Pillow nearest-neighbor authoring. No telescopic ligament or distal hand replacement. Fold uses current complete armless torso and exact native ball shell sectors.',unit='Original360px host unit; one fixed pivot per bank, one common canvas across frames.',ballStartFrame=ballIndex,frames=sum(a['frames']for a in manifest.values())),indent=2))
(R/'assets/host_whole_arms_art_1031.js').write_text("'use strict';\nconst RD96_ART="+json.dumps(manifest,separators=(',',':'))+';\n')
lua="""local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for n,a in pairs(M)do local im=Image{fromFile=D..'/'..n..'.png'};local s=Sprite(a.cw,a.ch,ColorMode.RGB)
 for i=0,a.frames-1 do if i>0 then s:newEmptyFrame()end;local c=Image(im,Rectangle(i%a.cols*a.cw,math.floor(i/a.cols)*a.ch,a.cw,a.ch));s:newCel(s.layers[1],i+1,c,Point(0,0));s.frames[i+1].duration=1/a.fps end
 s:saveAs(D..'/'..n..'.aseprite');s:close()
end
"""
(D/'author.lua').write_text(lua);subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
# Compact source review plates with stable body origin.
for n,indices in [('arm_left',[0,8,15,20,27,31,39,47]),('fold',[0,6,12,18,24,30,36,39])]:
 a=manifest[n];atlas=Image.open(D/(n+'.png'));plate=Image.new('RGBA',(1024,512),(19,26,34,255))
 for j,f in enumerate(indices):
  c=atlas.crop((f%a['cols']*a['cw'],f//a['cols']*a['ch'],(f%a['cols']+1)*a['cw'],(f//a['cols']+1)*a['ch']));full=Image.new('RGBA',(P,P));full.alpha_composite(c,(O-a['pivot'][0],O-a['pivot'][1]));full.thumbnail((256,256),Image.Resampling.NEAREST);plate.alpha_composite(full,(j%4*256,j//4*256))
 plate.save(W/(n+'-review.png'))
print('Authored',sum(a['frames']for a in manifest.values()),'fixed whole-arm/torso/fold frames; ball starts at',ballIndex)
