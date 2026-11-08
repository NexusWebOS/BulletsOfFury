"""Source-preserving articulated Sumpjaw banks. All turns/light/shadows baked offline."""
from pathlib import Path
import json,math,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
W=Path(__file__).resolve().parent
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
O=W/'authored';O.mkdir(exist_ok=True)
REL='assets/game/levels/stage_07/miniboss/sumpjaw_serpents_1104/'
S=R/'_ART_SOURCES/sumpjaw_duo_1031/sources/pixellab/body_01.png'
im=Image.open(S).convert('RGBA');M={'banks':{},'headings':32,'source':str(S.relative_to(R)),'sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'format':'Fixed even native cells;32 baked headings;independent articulated source-pixel head/body/tail;no runtime rotation,scale,filter,alpha FX.'}
allframes={}
def bank(name,frames,pivot=None,poses=None):
 w,h=frames[0].size;assert w%2==h%2==0 and all(f.size==(w,h)for f in frames)
 cols=8;per=64;pages=[]
 for start in range(0,len(frames),per):
  fs=frames[start:start+per];out=Image.new('RGBA',(cols*w,math.ceil(len(fs)/cols)*h))
  for j,f in enumerate(fs):out.alpha_composite(f,(j%cols*w,j//cols*h))
  n=f'{name}_{start//per}.png';out.save(O/n);pages.append(dict(key='ss116_'+name+'_'+str(start//per),path=REL+n,start=start,frames=len(fs)))
 M['banks'][name]=dict(w=w,h=h,cols=cols,frames=len(frames),pivot=pivot or[w//2,h//2],pages=pages,fps=24)
 if poses is not None:M['banks'][name]['poses']=poses
 allframes[name]=frames
mask=Image.new('L',im.size);d=ImageDraw.Draw(mask)
# Follow the actual head's metal silhouette; cut only the narrow neck seam.
d.polygon([(89,55),(121,53),(153,61),(170,80),(181,118),(174,145),(153,170),(127,181),(103,175),(84,154),(66,129),(65,98),(75,78)],fill=255)
head=im.copy();head.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')),np.array(mask))))
head=head.crop((45,40,197,192)) # common152px crop, physical root at(121,116)
root=(76,76);sockets={'mouth':[123-121,144-116],'gillL':[94-121,84-116],'gillR':[151-121,87-116]}
def lit(src,mode):
 a=np.array(src);alpha=a[:,:,3].copy()
 if mode=='hit':a[:,:,:3]=255
 elif mode=='hot':
  rgb=a[:,:,:3].astype(float);g=(rgb[:,:,1]>rgb[:,:,0]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.22)&(alpha>0)
  rgb[g]=np.minimum(255,rgb[g]*1.3+np.array([60,42,20]));a[:,:,:3]=rgb.astype('uint8')
 elif mode=='shadow':a[:,:,:3]=[3,10,8];a[:,:,3]=(alpha.astype(float)*.5).astype('uint8')
 out=Image.fromarray(a)
 if mode=='hot':
  aa=out.getchannel('A');rim=aa.filter(ImageFilter.MaxFilter(5));r=Image.new('RGBA',out.size,(132,242,28,0));r.putalpha(Image.fromarray(np.maximum(0,np.array(rim).astype(int)-np.array(aa).astype(int)).astype('uint8')));r.alpha_composite(out);out=r
 return out
def turn(src,n,cell,physical):
 c=Image.new('RGBA',(cell,cell));c.alpha_composite(src,(cell//2-physical[0],cell//2-physical[1]));return c.rotate(-n*360/32,resample=Image.Resampling.NEAREST,center=(cell//2,cell//2))
for state in range(4):
 src=head.copy();a=np.array(src);yy,xx=np.mgrid[:152,:152]
 for k,key in enumerate(['gillL','gillR']):
  if not state&(1<<k):continue
  x,y=sockets[key];area=((xx-(root[0]+x))/15)**2+((yy-(root[1]+y))/20)**2<1
  g=area&(a[:,:,1]>a[:,:,0].astype(float)*1.1);v=a[:,:,:3].max(2);a[g,0]=(v[g]*.2).astype('uint8');a[g,1]=(v[g]*.23).astype('uint8');a[g,2]=(v[g]*.17).astype('uint8')
 src=Image.fromarray(a)
 # Jaw recoil is an offline metal-mouth articulation; same skull/root in both frames.
 jaw=src.crop((38,104,112,145));opened=src.copy();opened.alpha_composite(jaw,(38,108))
 for mode in ['body','hot']:
  fs=[];poses=[]
  for phase,image in enumerate([src,opened]):
   for n in range(32):
    f=turn(lit(image,mode),n,176,root);fs.append(f);ang=n*math.tau/32;co=math.cos(ang);si=math.sin(ang);ps={}
    for key,(x,y)in sockets.items():
     if key=='mouth'and phase:y+=4
     ps[key]=[round(x*co-y*si,3),round(x*si+y*co,3)]
    bb=f.getbbox();ps['bounds']=[bb[0]-88,bb[1]-88,bb[2]-88,bb[3]-88];poses.append(ps)
  bank(mode+str(state),fs,poses=poses)
open_head=head.copy();open_head.alpha_composite(head.crop((38,104,112,145)),(38,108))
bank('hit',[turn(lit(s,'hit'),n,176,root)for s in [head,open_head]for n in range(32)])
bank('head_shadow',[turn(lit(head,'shadow'),n,176,root)for n in range(32)])
# Actual tail armor, isolated at its connecting collar, with retained metal texture.
seg=im.crop((46,23,76,53));ms=Image.new('L',(30,30));ImageDraw.Draw(ms).polygon([(7,1),(22,1),(29,10),(27,23),(18,29),(5,26),(0,13)],fill=255);seg.putalpha(Image.fromarray(np.minimum(np.array(seg.getchannel('A')),np.array(ms))))
for taper,scale in enumerate([1,.8,.6]):
 s=seg.resize((round(30*scale),round(30*scale)),Image.Resampling.NEAREST)
 for mode in ['body','hot','hit','shadow']:bank('segment'+str(taper)+'_'+mode,[turn(lit(s,mode),n,48,(s.width//2,s.height//2))for n in range(32)])
# Retain BOF's authored toxic orb/splash identities; giant round is72px, acid slug20px.
for name,source,cols,count,size in [('orb','assets/game/shared/combat/encounter_revision_1027/toxic_orb.png',4,16,72),('acid','assets/game/shared/combat/encounter_revision_1027/toxic_orb.png',4,16,20),('muzzle','assets/game/levels/stage_07/miniboss/dredger_final_1029/ooze.png',4,16,80)]:
 image=Image.open(R/source).convert('RGBA');cw=image.width//cols;ch=image.height//4;fs=[]
 raw=[image.crop((i%cols*cw,i//cols*ch,i%cols*cw+cw,i//cols*ch+ch))for i in range(count)]
 boxes=[s.getbbox()for s in raw if s.getbbox()];union=(min(b[0]for b in boxes),min(b[1]for b in boxes),max(b[2]for b in boxes),max(b[3]for b in boxes));side=max(union[2]-union[0],union[3]-union[1]);side+=side%2;cx=(union[0]+union[2])//2;cy=(union[1]+union[3])//2;box=(cx-side//2,cy-side//2,cx+side//2,cy+side//2)
 for s in raw:fs.append(s.crop(box).resize((size,size),Image.Resampling.NEAREST))
 bank(name,fs)
(O/'manifest.json').write_text(json.dumps(M,separators=(',',':')))
(W/'sumpjaw_serpent_art_1104.js').write_text("'use strict';\nconst SS116_ART="+json.dumps(M,separators=(',',':'))+';\n')
lua="""local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for n,a in pairs(M.banks)do local s=Sprite(a.w,a.h,ColorMode.RGB)
for _,p in ipairs(a.pages)do local im=Image{fromFile=D..'/'..p.path:match('([^/]+)$')};for j=0,p.frames-1 do local i=p.start+j;if i>0 then s:newEmptyFrame()end;local c=Image(im,Rectangle(j%a.cols*a.w,math.floor(j/a.cols)*a.h,a.w,a.h));s:newCel(s.layers[1],i+1,c,Point(0,0));s.frames[i+1].duration=1/a.fps end end
s:saveAs(D..'/'..n..'.aseprite');s:close()end"""
(O/'author.lua').write_text(lua)
subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+O.as_posix(),'--script',str(O/'author.lua')],check=True)
review=Image.new('RGBA',(704,528),(11,19,22,255))
for i,(n,f)in enumerate([('body0',0),('body0',4),('body0',8),('body0',16),('body0',24),('hot0',32),('body1',0),('body2',0),('body3',0),('hit',0),('orb',5),('segment0_body',0)]):review.alpha_composite(allframes[n][f],(i%4*176,i//4*176))
review.save(W/'source-review.png');print('BAKED',sum(a['frames']for a in M['banks'].values()),'FRAMES',len(M['banks']),'BANKS')
