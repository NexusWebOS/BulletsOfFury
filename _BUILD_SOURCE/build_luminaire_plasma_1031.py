"""Authored red plasma mine/dome frames from generated raster sources. Offline only."""
from pathlib import Path
import json,math,hashlib,shutil,subprocess
import numpy as np
from PIL import Image,ImageFilter,ImageChops,ImageDraw,ImageOps
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/luminaire_plasma_1031';W.mkdir(parents=True,exist_ok=True);D=R/'assets/game/levels/stage_08/boss/luminaire_plasma_1031';D.mkdir(parents=True,exist_ok=True)
for n in ['generated_orb.png','generated_dome.png']:
 if not (D/n).exists():shutil.copy2(W/n,D/n)
orb=Image.open(D/'generated_orb.png').convert('RGBA');orb=orb.crop(orb.getchannel('A').getbbox());dome=Image.open(D/'generated_dome.png').convert('RGBA');dome=dome.crop(dome.getchannel('A').getbbox())
raw=np.array(dome);hot=((raw[:,:,0]>180)&(raw[:,:,1]>100)&(raw[:,:,3]>100)).sum(axis=1);first=round(dome.height*.80);baseline=first+int(np.argmax(hot[first:]));dome=dome.crop((0,0,dome.width,baseline+2));manifest={'banks':{},'maxRadius':384,'floorDrop':64,'safeY':70,'inputMode':'Built-in image generation / two new transparent pixel-art assets; all changes baked offline.'}
def ease(v):v=max(0,min(1,v));return v*v*(3-2*v)
def energy(im,phase,bright=1):
 a=np.array(im);h,w=a.shape[:2];yy,xx=np.indices((h,w));edge=(xx<8)|(xx>w-9)|(yy<8)|(yy>h-9)
 dx=np.where(edge,0,np.rint(np.sin(yy*.09+phase)*1.5)).astype(int);dy=np.where(edge,0,np.rint(np.sin(xx*.075-phase)*1.5)).astype(int);src=a[np.clip(yy+dy,0,h-1),np.clip(xx+dx,0,w-1)].copy();rgb=src[:,:,:3].astype(float)
 rgb[:,:,0]*=bright;rgb[:,:,1]*=.85+.15*bright;rgb[:,:,2]*=.88+.12*bright;src[:,:,:3]=np.clip(rgb,0,255).astype('uint8');return Image.fromarray(src)
def bank(name,frames,w,h,pivot,poses=None):
 cols=4 if w>400 else 8;limit=8 if w>400 else 32;pages=[]
 for start in range(0,len(frames),limit):
  group=frames[start:start+limit];sheet=Image.new('RGBA',(w*cols,h*math.ceil(len(group)/cols)))
  for i,im in enumerate(group):sheet.alpha_composite(im,(i%cols*w,i//cols*h))
  suffix='_'+str(start//limit).zfill(2);p=D/(name+suffix+'.png');sheet.save(p);pages.append(dict(key='rd97_'+name+suffix,path='assets/game/levels/stage_08/boss/luminaire_plasma_1031/'+p.name,start=start,frames=len(group),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 a=dict(w=w,h=h,pivot=pivot,cols=cols,frames=len(frames),fps=30,pages=pages)
 if poses:a['poses']=poses
 manifest['banks'][name]=a
def orbframe(size,canvas,pivot,phase,brightness=1,ground=False):
 src=energy(orb,phase,brightness);k=size/max(src.size);src=src.resize((max(2,round(src.width*k)),max(2,round(src.height*k))),Image.Resampling.NEAREST)
 out=Image.new('RGBA',canvas);x=round(pivot[0]-src.width/2);y=round(pivot[1]-src.height if ground else pivot[1]-src.height/2)
 al=src.getchannel('A');outer=ImageChops.subtract(al.filter(ImageFilter.MaxFilter(5)),al);glow=Image.new('RGBA',src.size,(245,10,40,0));glow.putalpha(outer);glow.alpha_composite(src);out.alpha_composite(glow,(x,y));return out
bank('cast',[orbframe(40+60*ease(i/31),(144,144),(72,72),i*.28,.9+.22*abs(math.sin(i*.65)))for i in range(32)],144,144,[72,72])
bank('flight',[orbframe(96,(144,144),(72,72),i*math.tau/24,1.02+.2*math.sin(i*math.tau/6)**2)for i in range(24)],144,144,[72,72])
bank('mine',[orbframe(100+64*ease(i/31),(208,208),(104,198),i*.45,1+.28*math.sin(i*(.3+i/100))**2,True)for i in range(32)],208,208,[104,198])
CW,CH=832,464;PX,PY=416,400
def domeframe(radius,phase,brightness=1,fade=1):
 k=radius/dome.height;im=energy(dome,phase,brightness).resize((round(dome.width*k),round(dome.height*k)),Image.Resampling.NEAREST);out=Image.new('RGBA',(CW,CH));x=PX-im.width//2;y=PY-im.height
 out.alpha_composite(im,(x,y));drop=max(2,round(64*radius/384))
 # The generated base plasma continues below its landing point, so the bottom
 # edge cannot be used as an invisible hiding strip. This is actual aftermath art.
 tail=ImageOps.flip(im.crop((0,max(0,im.height-max(16,drop)),im.width,max(1,im.height-4)))).resize((im.width,drop),Image.Resampling.NEAREST)
 aa=np.array(tail);weights=np.clip((drop-np.arange(drop))/max(1,drop*.30),0,1);aa[:,:,3]=(aa[:,:,3]*weights[:,None]).astype('uint8');tail=Image.fromarray(aa);out.alpha_composite(tail,(x,PY))
 if fade<1:out.putalpha(out.getchannel('A').point(lambda a:round(a*fade)))
 return out
growth=[];poses=[]
for i in range(40):
 u=i/39;r=160+(384-160)*ease(u);growth.append(domeframe(r,i*.31,1+.2*math.sin(i*.65)**2));poses.append(dict(radius=round(r*dome.width/dome.height/2-8,3),height=round(r-8,3),floor=round(64*r/384,3)))
bank('rise',growth,CW,CH,[PX,PY],poses)
bank('crest',[domeframe(384,i*math.tau/16,1+.22*math.sin(i*math.tau/4)**2)for i in range(16)],CW,CH,[PX,PY])
bank('fall',[domeframe(384-(384-45)*ease(i/23),i*.4,1+.12*math.sin(i)**2,(1-i/23)**.7)for i in range(24)],CW,CH,[PX,PY])
retinaPath=R/'assets/game/levels/stage_08/miniboss/herald_landing_retinas_1030/retina.png';retina=Image.open(retinaPath).convert('RGBA');ret=[]
for i in range(24):ret.append(retina.crop((i%8*64,i//8*32,i%8*64+64,i//8*32+32)).resize((96,48),Image.Resampling.NEAREST))
bank('retina',ret,96,48,[48,24]);manifest['sourceHashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [D/'generated_orb.png',D/'generated_dome.png']};manifest['retinaSource']=dict(path=retinaPath.relative_to(R).as_posix(),sha256=hashlib.sha256(retinaPath.read_bytes()).hexdigest())
(D/'manifest.json').write_text(json.dumps(manifest,separators=(',',':')));(R/'assets/luminaire_plasma_art_1031.js').write_text("'use strict';\nconst RD97_ART="+json.dumps(manifest,separators=(',',':'))+';\n')
lua="""local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for n,a in pairs(M.banks)do local s=Sprite(a.w,a.h,ColorMode.RGB)
 for _,page in ipairs(a.pages)do local path=page.path:match('([^/]+)$');local im=Image{fromFile=D..'/'..path}
  for j=0,page.frames-1 do local i=page.start+j;if i>0 then s:newEmptyFrame()end;local c=Image(im,Rectangle(j%a.cols*a.w,math.floor(j/a.cols)*a.h,a.w,a.h));s:newCel(s.layers[1],i+1,c,Point(0,0));s.frames[i+1].duration=1/a.fps end
 end;s:saveAs(D..'/'..n..'.aseprite');s:close()
end
"""
(D/'author.lua').write_text(lua);subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
review=Image.new('RGBA',(1200,696),(15,20,28,255))
for j,f in enumerate([0,10,20,30,39]):
 im=growth[f].resize((400,232),Image.Resampling.NEAREST);review.alpha_composite(im,(j%3*400,j//3*232))
review.save(W/'rise-review.png');print('Authored',sum(a['frames']for a in manifest['banks'].values()),'plasma/ground-retina frames in seven editable banks.')
