"""Solid airborne carrier plus independently authored circular hatch/cannon reel.
Even cells, fixed physical circle pivot, measured deck wells and actual bores.
"""
from pathlib import Path
import json,shutil,hashlib,math
import numpy as np
from scipy.ndimage import label,maximum_filter
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_BUILD_SOURCE/cloud_carrier_1101';O=R/'assets/game/levels/stage_06/enemies/cloud_carrier_1101';Q=R/'_shots/cloud_carrier_1101'
for p in[S,O,Q]:p.mkdir(parents=True,exist_ok=True)
G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c');F={'hull':'exec-f158df06-9069-429f-8640-263999d7a347.png','cannon':'exec-1c3ecc17-010c-4764-b1cd-d8658c55e4b5.png'}
M={'owner':'_BUILD_SOURCE/build_cloud_carrier_1101.py','sources':{},'banks':{}}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source(n):
 p=S/(n+'_source.png')
 if not p.exists():shutil.copyfile(G/F[n],p)
 im=Image.open(p).convert('RGBA');a=np.array(im);a[:,:,3]=np.where(a[:,:,3]>=80,255,0);M['sources'][n]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'size':im.size,'tool':'built-in image_gen','original':F[n]};return Image.fromarray(a)
def save(n,im,cw,ch,frames=1,dirs=1):
 assert cw%2==0 and ch%2==0;p=O/(n+'.webp');im.save(p,format='WEBP',lossless=True,method=4);B={'key':'sc12_'+n,'path':p.relative_to(R).as_posix(),'cw':cw,'ch':ch,'frames':frames,'dirs':dirs,'cols':dirs,'sha256':sha(p)};M['banks'][n]=B;return B
def light(im):
 a=np.array(im);rgb=a[:,:,:3].astype(float);emit=(a[:,:,3]>80)&(rgb[:,:,2]>90)&(rgb[:,:,2]>rgb[:,:,0]*1.25)&(rgb[:,:,1]>65);g=np.zeros_like(a);g[:,:,:3]=[75,190,255];g[:,:,3]=np.where(emit,155,np.where(maximum_filter(emit,3),55,np.where(maximum_filter(emit,5),18,0)));return Image.fromarray(g)
im=source('hull');b=im.getbbox();pivot=[(b[0]+b[2])/2,(b[1]+b[3])/2];k=min(456/(b[2]-b[0]),960/(b[3]-b[1]));z=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST);t=Image.new('RGBA',(512,1024));t.alpha_composite(z,(round(256-pivot[0]*k),round(512-pivot[1]*k)));save('hull',t,512,1024);save('hull_glow',light(t),512,1024);save('hull_south',t.transpose(Image.Transpose.ROTATE_180),512,1024);save('hull_south_glow',light(t).transpose(Image.Transpose.ROTATE_180),512,1024)
def pt(x,y):return[round(256+(x-pivot[0])*k,3),round(512+(y-pivot[1])*k,3)]
M['hull']={'pivot':[256,512],'worldHeight':470,'scale':k,'sourcePivot':pivot,'bays':[pt(443,y)for y in[438,637,839,1041,1249]],'core':pt(443,223),'engines':[pt(x,1658)for x in[286,389,496,597]],'wellDiameter':164*k}
im=source('cannon');fs=[];pivots=[];bores=[];rects=[]
for y in range(3):
 for x in range(4):
  box=[round(x*im.width/4),round(y*im.height/3),round((x+1)*im.width/4),round((y+1)*im.height/3)];f=im.crop(box);a=np.array(f);ids,count=label(a[:,:,3]>80);sizes=np.bincount(ids.ravel());sizes[0]=0;a[ids!=sizes.argmax(),3]=0;f=Image.fromarray(a);ys,xs=np.nonzero(a[155:185,:,3]>80);left=int(xs.min());right=int(xs.max());px=(left+right)/2;top=np.nonzero(a[:280,:,3]>80)[0].min();py=float(top+(right-left)*.48);pivots.append([px,py]);rects.append(box);fs.append(f)
scale=128/max(np.nonzero(np.array(f)[155:185,:,3]>80)[1].max()-np.nonzero(np.array(f)[155:185,:,3]>80)[1].min()for f in fs[:11])
norm=[]
for i,(f,p)in enumerate(zip(fs,pivots)):
 a=np.array(f);yy,xx=np.indices(a.shape[:2]);blue=(a[:,:,3]>80)&(a[:,:,2]>85)&(a[:,:,2]>a[:,:,0].astype(float)*1.4)&(a[:,:,2]>a[:,:,1].astype(float)*1.08)&(yy>p[1]+20)&(abs(xx-p[0])<60);ids,_=label(blue);candidates=[]
 for j in range(1,ids.max()+1):
  y,x=np.nonzero(ids==j)
  if len(x)>4:candidates.append((float(y.mean()),float(x.mean())))
 by,bx=max(candidates)if candidates else(p[1]+45,p[0]);bores.append([round(96+(bx-p[0])*scale,3),round(96+(by-p[1])*scale,3)])
 z=f.resize((round(f.width*scale),round(f.height*scale)),Image.Resampling.NEAREST);t=Image.new('RGBA',(192,192));t.alpha_composite(z,(round(96-p[0]*scale),round(96-p[1]*scale)));norm.append(t)
dirs=32;sheet=Image.new('RGBA',(192*dirs,192*12));glow=Image.new('RGBA',sheet.size)
for i,t in enumerate(norm):
 g=light(t)
 for d in range(dirs):sheet.alpha_composite(t.rotate(-d*360/dirs,Image.Resampling.NEAREST),(192*d,192*i));glow.alpha_composite(g.rotate(-d*360/dirs,Image.Resampling.NEAREST),(192*d,192*i))
save('cannon',sheet,192,192,12,dirs);save('cannon_glow',glow,192,192,12,dirs);M['cannon']={'pivot':[96,96],'worldSize':68,'rimDiameter':128,'bores':bores,'sourcePivots':pivots,'sourceRects':rects,'commonScale':scale,'poses':{'closed':0,'opening':[0,7],'extended':7,'charge':8,'recoil':9,'return':10,'destroyed':11}}
# Blue/white native authored beam segments; use its full measured alpha width.
V=json.JSONDecoder().raw_decode((R/'assets/stage3_amplify_art_1031.js').read_text().split('const I31_ART=',1)[1])[0];M['beam']=V['banks']['laser'];M['beam']['alphaWidth']=18
out=Image.new('RGB',(192*4,216*3),(8,20,32));d=ImageDraw.Draw(out)
for i,t in enumerate(norm):x=i%4*192;y=i//4*216;out.paste(t,(x,y+18),t);d.text((x+4,y+2),str(i),fill='white');p=bores[i];d.ellipse((x+p[0]-2,y+p[1]+16,x+p[0]+2,y+p[1]+20),fill='#ffdf30')
out.save(Q/'cannon-contact.png');im=Image.new('RGB',(512,1024),(8,20,32));im.paste(Image.open(O/'hull.webp'),(0,0),Image.open(O/'hull.webp'));d=ImageDraw.Draw(im)
for i,p in enumerate(M['hull']['bays']):d.ellipse((p[0]-47,p[1]-47,p[0]+47,p[1]+47),outline='#50ff9a',width=2);d.text((p[0]+48,p[1]),str(i+1),fill='white')
im.save(Q/'hull-sockets.png');(O/'manifest.json').write_text(json.dumps(M,indent=2)+'\n',encoding='utf-8');(R/'assets/cloud_carrier_art_1101.js').write_text('"use strict";\nconst CC111_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print('Registered solid carrier, five measured wells,12 cannon poses/32 headings and native beam')
