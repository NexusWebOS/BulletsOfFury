"""SJ120: source-pixel toxic mouth animation and one fixed split health frame."""
from pathlib import Path
import json,math,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W/'authored';O.mkdir(exist_ok=True)
REL='assets/game/levels/stage_07/miniboss/sumpjaw_tandem_1105/'
S=json.loads((R/'assets/game/levels/stage_07/miniboss/sumpjaw_serpents_1104/manifest.json').read_text())
OLD=json.loads((R/'assets/game/levels/stage_07/miniboss/sumpjaw_duo_1031/manifest.json').read_text())
M={'banks':{},'pages':{},'masks':{},'contract':'Fixed even frames; mouth-only source-pixel emission; one authored health frame with independent fixed 50 percent halves.'};cache={};frames={};pageid=0
def source(meta,n,i=0):
 b=meta['banks'][n];p=next(p for p in b['pages']if p['start']<=i<p['start']+p['frames']);k=p['key']
 if k not in cache:cache[k]=Image.open(R/p['path']).convert('RGBA')
 j=i-p['start'];return cache[k].crop((j%b['cols']*b['w'],j//b['cols']*b['h'],j%b['cols']*b['w']+b['w'],j//b['cols']*b['h']+b['h']))
def bank(n,images,pivot=None):
 global pageid
 w,h=images[0].size;assert w%2==h%2==0 and all(f.size==(w,h)for f in images)
 b={'w':w,'h':h,'frames':len(images),'pivot':pivot or[w//2,h//2],'cells':[]};page=Image.new('RGBA',(1024,1024));x=y=rowh=0;pending=[]
 def save():
  global pageid
  if not pending:return
  bb=page.getbbox()or(0,0,2,2);pw=math.ceil(bb[2]/2)*2;ph=math.ceil(bb[3]/2)*2;k='sj120_page_'+str(pageid);file='page_'+str(pageid)+'.png';page.crop((0,0,pw,ph)).save(O/file);M['pages'][k]={'path':REL+file,'w':pw,'h':ph}
  for c in pending:c[0]=k
  pageid+=1
 for f in images:
  l,t,r,bottom=f.getbbox()or(0,0,2,2);sw=r-l;sh=bottom-t
  if x+sw+2>1024:x=0;y+=rowh+2;rowh=0
  if y+sh+2>1024:save();page=Image.new('RGBA',(1024,1024));x=y=rowh=0;pending=[]
  page.alpha_composite(f.crop((l,t,r,bottom)),(x,y));c=[None,x,y,sw,sh,l,t];b['cells'].append(c);pending.append(c);x+=sw+2;rowh=max(rowh,sh)
 save();M['banks'][n]=b;frames[n]=images;(O/'strips').mkdir(exist_ok=True);out=Image.new('RGBA',(w*min(8,len(images)),h*math.ceil(len(images)/8)))
 for i,f in enumerate(images):out.alpha_composite(f,(i%8*w,i//8*h))
 out.save(O/'strips'/(n+'.png'))

mouth=[]
for level in range(4):
 for phase in range(8):
  for jaw in[0,1]:
   im=source(S,'body0',jaw*32);a=np.array(im);yy,xx=np.indices(a.shape[:2]);cx,cy=90,116+jaw*4
   inside=((xx-cx)/17)**2+((yy-cy)/16)**2<1;energy=inside&(a[:,:,1]>a[:,:,0].astype(float)*1.12)&(a[:,:,1]>a[:,:,2].astype(float)*1.22)&(a[:,:,3]>0)
   tex=source(S,'orb',phase*2).resize((32,32),Image.Resampling.NEAREST);layer=Image.new('RGBA',im.size);layer.alpha_composite(tex,(cx-16,cy-16));flow=np.array(layer)
   out=np.zeros_like(a);mix=.45+level*.15;rgb=a[:,:,:3].astype(float)*(1-mix)+flow[:,:,:3].astype(float)*mix;rgb+=np.array([level*10,level*23,level*7]);out[energy,:3]=np.minimum(255,rgb[energy]).astype('uint8');out[energy,3]=a[energy,3]
   src=Image.fromarray(out)
   for d in range(32):mouth.append(src.rotate(-d*360/32,Image.Resampling.NEAREST,center=(88,88)))
bank('mouth',mouth)
flash=[]
for i in range(16):
 im=source(S,'muzzle',i).resize((40,40),Image.Resampling.NEAREST);c=Image.new('RGBA',(48,48));c.alpha_composite(im,(4,4));flash.append(c)
bank('mouth_flash',flash)

# Keep the approved original cap and border material; tile its centre offline.
src=source(OLD,'health_frame');bar=Image.new('RGBA',(400,28));bar.alpha_composite(src.crop((0,0,16,28)),(0,0));bar.alpha_composite(src.crop((144,0,160,28)),(384,0))
for x in range(16,384,16):bar.alpha_composite(src.crop((64,0,64+min(16,384-x),28)),(x,0))
d=ImageDraw.Draw(bar);d.rectangle((198,17,201,25),fill=(35,50,22,255));d.line((199,18,199,24),fill=(192,240,72,255))
bank('health_frame',[bar],pivot=[200,14])
src=source(OLD,'health_fill');fill=Image.new('RGBA',(190,4))
for x in range(0,190,16):fill.alpha_composite(src.crop((0,0,min(16,190-x),4)),(x,0))
bank('health_half',[fill],pivot=[0,0])
M['health']={'width':400,'half':190,'left':[-192,5],'right':[2,5],'centreDivider':4}
M['sources']={n:hashlib.sha256((R/p).read_bytes()).hexdigest()for n,p in [('SS116','assets/game/levels/stage_07/miniboss/sumpjaw_serpents_1104/manifest.json'),('SJ98','assets/game/levels/stage_07/miniboss/sumpjaw_duo_1031/manifest.json')]}
(O/'manifest.json').write_text(json.dumps(M,separators=(',',':')));(W/'sumpjaw_tandem_art_1105.js').write_text("'use strict';\nconst SJ120_ART="+json.dumps(M,separators=(',',':'))+';\n')
lua="""local D=app.params.out;local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for n,a in pairs(M.banks)do local im=Image{fromFile=D..'/strips/'..n..'.png'};local s=Sprite(a.w,a.h,ColorMode.RGB)
for i=0,a.frames-1 do if i>0 then s:newEmptyFrame()end;s:newCel(s.layers[1],i+1,Image(im,Rectangle(i%8*a.w,math.floor(i/8)*a.h,a.w,a.h)),Point(0,0));s.frames[i+1].duration=1/24 end;s:saveAs(D..'/'..n..'.aseprite');s:close()end"""
(O/'author.lua').write_text(lua);subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+O.as_posix(),'--script',str(O/'author.lua')],check=True)
print('ART',sum(b['frames']for b in M['banks'].values()),len(M['banks']),len(M['pages']))
